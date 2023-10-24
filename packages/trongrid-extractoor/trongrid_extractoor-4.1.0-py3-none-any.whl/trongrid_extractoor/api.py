'''
API wrapper for TronGrid.
'''
import tempfile
from io import StringIO
from itertools import chain
from pathlib import Path
from typing import Any, Dict, Iterator, List, Optional, Type, Union

import pendulum
from pendulum import DateTime
from requests.exceptions import JSONDecodeError
from rich.pretty import pprint

from trongrid_extractoor.config import log
from trongrid_extractoor.exceptions import *
from trongrid_extractoor.helpers.address_helpers import coerce_to_base58, is_tron_base58_address
from trongrid_extractoor.helpers.csv_helper import output_csv_path
from trongrid_extractoor.helpers.rich_helpers import console
from trongrid_extractoor.helpers.string_constants import *
from trongrid_extractoor.models.trc20_txn import Trc20Txn
from trongrid_extractoor.models.tron_account import TronAccount
from trongrid_extractoor.models.tron_contract import TronContract
from trongrid_extractoor.models.tron_event import TronEvent
from trongrid_extractoor.output.file_output_writer import FileOutputWriter
from trongrid_extractoor.output.string_io_writer import StringIOWriter
from trongrid_extractoor.progress_tracker import ProgressTracker
from trongrid_extractoor.request_params import EventRequestParams
from trongrid_extractoor.response import Response

RESCUE_DURATION_WALKBACK_SECONDS = [
    20,
    200,
    1000,
]

ONE_SECOND_MS = 1000.0
EMPTY_RESPONSE_RETRY_AFTER_SECONDS = 60

# Currently we poll from the most recent to the earliest events which is perhaps non optimal
ORDER_BY_BLOCK_TIMESTAMP_ASC = 'block_timestamp,asc'
ORDER_BY_BLOCK_TIMESTAMP_DESC = 'block_timestamp,desc'


class Api:
    def __init__(self, network: str = MAINNET, api_key: str = '') -> None:
        network = '' if network == MAINNET else f".{network}"
        self.base_uri = f"https://api{network}.trongrid.io/"
        self.api_key = api_key

    def contract_events(
            self,
            progress_tracker: ProgressTracker,
            event_name: Optional[str] = None,
            since: Optional[DateTime] = None,
            until: Optional[DateTime] = None
        ) -> Iterator[List[TronEvent]]:
        """
        Iterate lists of events by contract address. This is the endpoint that actually works
        to get all transactions (unlike the '[CONTRACT_ADDRESS]/transactions' endpoint).

          - contract_address:  On-chain address of the token
          - event_name:        The event to poll for ('None' for all events)
          - since:             Start time to retrieve
          - until:             Start time to retrieve

        Test harness: https://developers.tron.network/v4.0/reference/events-by-contract-address
        """
        endpoint_url = self._build_endpoint_url(f"v1/contracts/{progress_tracker.contract_address}/events")
        params = EventRequestParams(endpoint_url, since, until, event_name=event_name)
        params.max_timestamp = progress_tracker.earliest_timestamp_seen() or params.max_timestamp
        yield self._extract_events_from_response(endpoint_url, progress_tracker, params)

        # Pull the next record from the provided next URL until there's nothing left to pull
        while progress_tracker.last_response.is_continuable_response():
            yield self._extract_events_from_response(progress_tracker.last_response.next_url(), progress_tracker)

            if progress_tracker.last_response.is_paging_complete():
                log.info(f"Paging complete for {params} so will end loop...")

        progress_tracker.log_state(progress_tracker.last_response)

    def get_all_contract_events(self, contract_address: str, event_name: Optional[str] = None) -> List[TronEvent]:
        """
        Returns list of all events of a given type (or all events if 'event_name' is None).
        Transfers will be returned as events. Use with caution on contracts with lots of event logs.
        """
        progress_tracker = ProgressTracker(contract_address, event_name)
        event_lists = (events for events in self.contract_events(progress_tracker, event_name))
        return [e for e in chain(*event_lists)]

    def write_contract_events(
            self,
            contract_address: Optional[str] = None,
            event_name: str = 'Transfer',
            since: Optional[DateTime] = None,
            until: Optional[DateTime] = None,
            output_to: Optional[Union[Path, StringIO]] = None,
            filename_suffix: Optional[str] = None,
            resume_from_csv: Optional[Path] = None
        ) -> Optional[Path]:
        """
        Get events by contract address and write to CSV or JSON format in either a file or StringIO object.

          - contract_address:  On-chain address of the token
          - event_name:        The event to poll for ('None' for all events)
          - since:             Start time to retrieve
          - until:             Start time to retrieve
          - output_to          Either a dir to write a file to or a StringIO object to receive file as string
          - filename_suffix:   Optional string to append to the filename
          - resume_from_csv:   Path to a CSV you want to resume writing
          - event_name:        Type of event to retrieve
        """
        # Resume from CSV if requested
        if resume_from_csv is None and not is_tron_base58_address(contract_address):
            raise ValueError(f"Must provide a valid contract address or a CSV to resume.")

        progress_tracker = ProgressTracker(contract_address, event_name)

        if isinstance(output_to, StringIO):
            writer = StringIOWriter(output_stream, progress_tracker.event_cls)
            output_path = None
        else:
            if resume_from_csv is not None:
                output_path = resume_from_csv
                progress_tracker.load_csv_progress(output_path)
            elif output_to is None or isinstance(output_to, (str, Path)):
                output_to = output_to or Path('')
                output_to = Path(output_to)

                if not output_to.is_dir():
                    raise ValueError(f"'{output_to}' is not a directory")

                output_path = output_csv_path(contract_address, output_to, filename_suffix)
            else:
                raise ValueError(f"output_to arg of wrong type: '{output_to}' ({type(output_to).__name__})")

            writer = FileOutputWriter(output_path, progress_tracker.event_cls)
            log.info(f"Output CSV: '{output_path}'")

        for events in self.contract_events(progress_tracker, event_name, since, until):
            writer.write_rows(events)

        return output_path

    def txn_events(self, tx_hash: str) -> List[TronEvent]:
        """Get TronEvents and Trc20Txns etc for a given 'tx_hash'."""
        endpoint_url = self._build_endpoint_url(f"v1/transactions/{tx_hash}/events")
        response = Response.get_response(url=endpoint_url).response

        if len(response[DATA]) == 0:
            pprint(response, expand_all=True, indent_guides=False)
            raise NoEventsFoundError(f"No events found for '{tx_hash}'!")

        return [
            Trc20Txn.from_event_dict(e) \
                  if e[EVENT_NAME] == TRANSFER \
                else TronEvent.from_event_dict(e)
            for e in response[DATA]
        ]

    def get_contract(self, address: str) -> Optional[TronContract]:
        """
        Get information about contract at a given address.
        Test harness: https://developers.tron.network/v4.0/reference/get-contract
        """
        log.info(f"Retrieving contract at '{address}'...")
        endpoint_url = self._build_endpoint_url('wallet/getcontract')
        params = {VALUE: coerce_to_base58(address), VISIBLE: True}
        response = Response.post_response(endpoint_url, params).response

        if len(response) > 0:
            return TronContract.from_response_dict(response)

    def get_account(self, address: str) -> Optional[TronAccount]:
        """
        Get information about an account. Things like self tags, balances, etc. Note that 'getaccount' endpoint
        only returns human readable tag information if you request info for base58 form of address with
        'visible'=True args. Test harness: https://developers.tron.network/v4.0/reference/walletgetaccount
        """
        log.debug(f"Retrieving account at '{address}'...")
        endpoint_url = self._build_endpoint_url('wallet/getaccount')
        params = {ADDRESS: coerce_to_base58(address), VISIBLE: True}

        try:
            response = Response.post_response(endpoint_url, params).response
        except JSONDecodeError:
            log.warning(f"Unparseable JSON reponse for address '{address}'!")
            return
        except Exception:
            console.print_exception()
            raise

        if len(response) != 0:
            return TronAccount.from_response_dict(response, self)

    def _extract_events_from_response(
            self,
            endpoint_url: str,
            progress_tracker: ProgressTracker,
            params: Optional[EventRequestParams] = None,
            internal_txns: bool = False
        ) -> List[TronEvent]:
        """Extract events from API response."""
        try:
            request_params = params.request_params() if params is not None else {}
            progress_tracker.last_response = Response.get_response(endpoint_url, request_params)
            rows = progress_tracker.last_response.response[DATA]
            events = [progress_tracker.event_cls.from_event_dict(row) for row in rows]

            if internal_txns:
                events += [
                    progress_tracker.event_cls.from_event_dict(row)
                    for event in chain(*events)
                    for row in self.txn_events(event.transaction_id)
                ]

            return progress_tracker.remove_already_processed_txns(events)
        except Exception:
            console.print_exception()
            raise

    def _build_endpoint_url(self, url_path: str) -> str:
        return f"{self.base_uri}{url_path}"
