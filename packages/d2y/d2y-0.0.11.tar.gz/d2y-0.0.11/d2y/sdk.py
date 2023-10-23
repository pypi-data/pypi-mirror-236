import json
import requests
from dataclasses import dataclass, asdict
from typing import Dict, Any, List, Optional, Union

from enum import Enum
from d2y.models import *
from d2y.enums import *
from datetime import datetime, timezone
from d2y.utils import sign_order, generate_random_uint64, convert_datetime_to_iso


class Error(Exception):
    pass


class AuthenticationError(Error):
    pass


class TradingClient:
    """
    A class that represents a trading client, which allows the user to connect and interact with the trading API.

    Attributes
    ----------
    api_key : str
        The API key used for authentication.
    api_secret : str
        The API secret used for authentication.
    wallet_address : str
        The wallet address of the user.
    signer_key : str
        The linked signer key of the user's wallet.
    base_url : str
        The base URL for the API.
    user : object
        The current user's account information (default is None).
    """

    def __init__(
        self,
        api_key: str,
        api_secret: str,
        wallet_address: str,
        linked_signer_key: str,
        base_url: str = "https://api.dev.d2y.exchange",
        chain_id: int = 421613,
        exchange_contract_address="0xFdd1b4B596825B7C2E9Bd181B83C928c0Aa0ba67",
    ):
        """
        The constructor for the TradingClient class.

        Parameters
        ----------
        api_key : str
            The API key used for authentication.
        api_secret : str
            The API secret used for authentication.
        base_url : str
            The base URL for the API (default is "https://api.dev.d2y.exchange").
        wallet_address : str
            The wallet address of the user.
        signer_key : str
            The private key OR linked signer key of the user's wallet.
        chain_id : int
            The chain ID of the blockchain network (default is 421613).
        exchange_contract_address : str
            The address of the exchange contract (default is "0xFdd1b4B596825B7C2E9Bd181B83C928c0Aa0ba67").
        """
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = base_url
        self.wallet_address = wallet_address
        self.signer_key = linked_signer_key
        self.user = None
        self.chain_id = chain_id
        self.exchange_contract_address = exchange_contract_address

        if not self.api_key or not self.api_secret:
            raise ValueError("API key and secret are required.")

    def _headers(self):
        headers = {
            "d2y-api-key": self.api_key,
            "d2y-api-secret": self.api_secret,
        }
        return headers

    # __________________Helpers____________________

    def _request(self, method, url, params=None, data=None, obj_class=None):
        params = {k: v for k, v in params.items() if v is not None} if params else {}
        data = convert_datetime_to_iso(data)
        response = method(url, headers=self._headers(), params=params, json=data)

        if response.status_code not in [200, 204]:
            error = response.json().get("error") or {
                "message": "Unknown error",
                "code": None,
            }
            raise Exception(
                f"Request failed with status code {response.status_code}: {response.content}. "
                f"Error code: {error['code']}, message: {error['message']}"
            )

        if method == requests.delete:
            return {
                "status": response.status_code,
                "message": "Delete operation completed.",
            }

        data = response.json().get("data", [])
        return [obj_class(**item) for item in data] if obj_class else data

    def _get_helper(self, url, params=None, obj_class=None):
        return self._request(requests.get, url, params=params, obj_class=obj_class)

    def _post_helper(self, url, body=None, params=None, obj_class=None):
        return self._request(
            requests.post, url, params=params, data=body, obj_class=obj_class
        )

    def _delete_helper(self, url, body=None, params=None, obj_class=None):
        return self._request(requests.delete, url, data=body, obj_class=obj_class)

    @staticmethod
    def _list_to_string(lst):
        return ",".join(map(str, lst))

    def _build_params(self, **kwargs):
        params = {}
        for k, v in kwargs.items():
            if isinstance(v, list):
                if all(isinstance(item, str) for item in v):
                    params[k] = ",".join(
                        v
                    )  # If all items in list are strings, join them with commas
                else:
                    params[k] = self._list_to_string(
                        v
                    )  # Otherwise, use the _list_to_string function
            elif isinstance(v, Enum):
                params[k] = v.value  # If value is an Enum, get its value
            else:
                params[k] = v  # In all other cases, just assign the value as it is
        return {k: v for k, v in params.items() if v is not None}  # Remove None values

    # __________________Accounts____________________
    def get_profile(self) -> Profile:
        """
        Retrieves the user's profile information.

        Returns
        -------
        Profile
            An object containing the user's profile information.
        """
        url = f"{self.base_url}/accounts/account"
        data = self._get_helper(url)
        profile_data = data.get("profile", {})
        return Profile.from_dict(profile_data) if profile_data else None

    def get_account(self) -> Account:
        """
        Retrieves the user's account information.

        Returns
        -------
        Account
            An object containing the user's account information.
        """
        url = f"{self.base_url}/accounts/account"
        data = self._get_helper(url)
        account_data = data.get("account", {})
        self.user = Account.from_dict(account_data) if account_data else None
        return self.user

    def get_transfers(self) -> List[Transfer]:
        """
        Retrieves the user's transfer history.

        Returns
        -------
        List[Transfer]
            A list of Transfer objects representing the user's transfer history.
        """
        url = f"{self.base_url}/accounts/transfers"
        data = self._get_helper(url)
        return [Transfer.from_dict(transfer) for transfer in data]

    def get_portfolio(self) -> Portfolio:
        """
        Retrieves the user's portfolio information.

        Returns
        -------
        Portfolio
            An object containing the user's portfolio information.
        """
        url = f"{self.base_url}/accounts/portfolio"
        data = self._get_helper(url)
        return Portfolio.from_dict(data)

    # _________________________________________________

    def get_info(self) -> D2yInfo:
        """
        Retrieves information about the D2Y exchange.

        Returns
        -------
        D2yInfo
            An object containing information about the D2Y exchange.
        """
        url = f"{self.base_url}/info"
        data = self._get_helper(url)
        return D2yInfo.from_dict(data)

    def get_assets(self) -> List[Asset]:
        """
        Retrieves asset information for available options.

        Returns
        -------
        List[Asset]
            A list of Asset objects representing available options in the market.
        """
        url = f"{self.base_url}/assets"
        data = self._get_helper(url)
        return [Asset.from_dict(asset) for asset in data]

    def get_markets(
        self,
        expiration_timestamp: Optional[Union[str, List[str]]] = None,
        instrument_id: Optional[Union[int, List[int]]] = None,
        instrument_name: Optional[Union[str, List[str]]] = None,
        instrument_type: Optional[Union[InstrumentType, List[InstrumentType]]] = None,
        is_expired: Optional[bool] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        option_type: Optional[Union[OptionType, List[OptionType]]] = None,
        strike_price: Optional[Union[float, List[float]]] = None,
        settlement_period: Optional[Union[str, List[str]]] = None,
    ) -> List[Instrument]:
        """
        Retrieves a list of instruments with optional filters.

        Parameters
        ----------
        expiration_timestamp : Optional[Union[str, List[str]]]
            Filter by expiration timestamp (default is None).
        instrument_id : Optional[Union[int, List[int]]]
            Filter by instrument ID (default is None).
        instrument_name : Optional[Union[str, List[str]]]
            Filter by instrument name (default is None).
        instrument_type : Optional[Union[InstrumentType, List[InstrumentType]]]
            Filter by instrument type (default is None).
        is_expired : Optional[bool]
            Filter by expired status (default is None).
        limit : Optional[int]
            Limit the number of results (default is None).
        offset : Optional[int]
            Offset the results (default is None).
        option_type : Optional[Union[OptionType, List[OptionType]]]
            Filter by option type (default is None).
        strike_price : Optional[Union[float, List[float]]]
            Filter by strike price (default is None).
        settlement_period : Optional[Union[str, List[str]]]
            Filter by settlement_period (default is None).

        Returns
        -------
        List[Instrument]
            A list of Instrument objects representing the filtered instruments.
        """
        url = f"{self.base_url}/markets"
        params = self._build_params(
            expiration_timestamp=expiration_timestamp,
            instrument_id=instrument_id,
            instrument_name=instrument_name,
            instrument_type=instrument_type,
            is_expired=is_expired,
            limit=limit,
            offset=offset,
            option_type=option_type,
            strike_price=strike_price,
            settlement_period=settlement_period,
        )
        data = self._get_helper(url, params=params)

        return [Instrument.from_dict(instrument) for instrument in data]

    def get_orderbook(
        self,
        instrument_id: Optional[Union[int, List[int]]] = None,
        instrument_name: Optional[Union[str, List[str]]] = None,
        depth: Optional[int] = None,
    ) -> Orderbook:
        """
        Retrieves the orderbook for a given instrument.

        Parameters
        ----------
        instrument_id : Optional[Union[int, List[int]]]
            Instrument ID(s) to filter by (default is None).
        instrument_name : Optional[Union[str, List[str]]]
            Instrument name(s) to filter by (default is None).
        depth : Optional[int]
            The maximum number of levels to retrieve (default is None).

        Returns
        -------
        Orderbook
            An Orderbook object containing bids and asks for the specified instrument(s).
        """

        if (instrument_id is None and instrument_name is None) or (
            instrument_id is not None and instrument_name is not None
        ):
            raise ValueError(
                "Either instrument_id or instrument_name must be provided, but not both."
            )
        url = f"{self.base_url}/orderbook"
        params = self._build_params(
            instrument_id=instrument_id, instrument_name=instrument_name, depth=depth
        )
        data = self._get_helper(url, params=params)
        bids = [BidAsk.from_dict(bid) for bid in data.get("bids", [])]
        asks = [BidAsk.from_dict(ask) for ask in data.get("asks", [])]
        return Orderbook(bids=bids, asks=asks)

    def get_orders(
        self,
        expiration_timestamp: Optional[Union[str, List[str]]] = None,
        instrument_id: Optional[Union[int, List[int]]] = None,
        instrument_name: Optional[Union[str, List[str]]] = None,
        instrument_type: Optional[Union[InstrumentType, List[InstrumentType]]] = None,
        is_expired: Optional[bool] = None,
        option_type: Optional[Union[OptionType, List[OptionType]]] = None,
        ordering: Optional[str] = None,
        status: Optional[Union[OrderStatus, List[OrderStatus]]] = None,
        strike_price: Optional[Union[float, List[float]]] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> List[Order]:
        url = f"{self.base_url}/orders"
        params = self._build_params(
            expiration_timestamp=expiration_timestamp,
            instrument_id=instrument_id,
            instrument_name=instrument_name,
            instrument_type=instrument_type,
            is_expired=is_expired,
            option_type=option_type,
            ordering=ordering,
            status=status,
            strike_price=strike_price,
            limit=limit,
            offset=offset,
        )
        """
        Retrieves a list of orders with optional filters.
        
        Parameters
        ----------
        expiration_timestamp : Optional[Union[str, List[str]]]
            Filter by expiration timestamp (default is None).
        instrument_id : Optional[Union[int, List[int]]]
            Filter by instrument ID (default is None).
        instrument_name : Optional[Union[str, List[str]]]
            Filter by instrument name (default is None).
        instrument_type : Optional[Union[InstrumentType, List[InstrumentType]]]
            Filter by instrument type (default is None).
        is_expired : Optional[bool]
            Filter by expired status (default is None).
        option_type : Optional[Union[OptionType, List[OptionType]]]
            Filter by option type (default is None).
        ordering : Optional[str]
            Ordering of the results (default is None).
        status : Optional[Union[OrderStatus, List[OrderStatus]]]
            Filter by order status (default is None).
        strike_price : Optional[Union[float, List[float]]]
            Filter by strike price (default is None).
        limit : Optional[int]
            Limit the number of results (default is None).
        offset : Optional[int]
            Offset the results (default is None).

        Returns
        -------
        List[Order]
            A list of Order objects representing the filtered orders.
        """
        data = self._get_helper(url, params=params)
        return [Order.from_dict(order) for order in data]

    def place_order(self, orders: Union[OrderInput, List[OrderInput]]) -> List[Order]:
        """
        Places one or multiple orders on the options exchange.

        Parameters
        ----------
        orders : Union[OrderInput, List[OrderInput]]
            A single order (OrderInput) or a list of orders (List[OrderInput]) to be placed.

        Returns
        -------
        List[Order]
            A list of fulfilled Order objects, each containing information about the placed order.
        """
        if not isinstance(orders, list):
            orders = [orders]

        # apply default values and sign
        for order in orders:
            if not order.expiry_timestamp:
                order.expiry_timestamp = datetime(
                    2100, 1, 1, 0, 0, 0, tzinfo=timezone.utc
                )
            if not order.unique_reference_id:
                order.unique_reference_id = generate_random_uint64()
            signature = sign_order(
                signer_key=self.signer_key,
                wallet_address=self.wallet_address,
                option_address=order.address,
                price=order.price,
                amount=order.quantity,
                expiry_timestamp=order.expiry_timestamp,
                unique_reference_id=order.unique_reference_id,
                chain_id=self.chain_id,
                exchange_contact_address=self.exchange_contract_address,
                side=order.side,
            ).signature.hex()
            order.signature = signature
            order.one_click_trade = True

        filtered_orders = [
            {
                **{k: v for k, v in asdict(order).items() if v is not None},
                **{
                    "signature": order.signature,
                    "one_click_trade": order.one_click_trade,
                },
            }
            for order in orders
        ]

        url = f"{self.base_url}/orders"
        data = self._post_helper(url, body=filtered_orders)
        return [Order.from_dict(order) for order in data]

    def cancel_order(self, order_id: str) -> Dict[str, Any]:
        """
        Cancel a single order by its order_id.

        Parameters
        ----------
        order_id : str
            The ID of the order that should be canceled.

        Returns
        -------
        Dict[str, Any]
            A dictionary containing a status code and a message confirming the order cancellation.
        """

        url = f"{self.base_url}/orders/{order_id}"
        data = self._delete_helper(url)
        return data

    def cancel_all_orders(
        self,
        expiration_timestamp: Optional[Union[str, List[str]]] = None,
        instrument_id: Optional[Union[int, List[int]]] = None,
        instrument_name: Optional[Union[str, List[str]]] = None,
        instrument_type: Optional[Union[str, List[str]]] = None,
        strike_price: Optional[Union[float, List[float]]] = None,
        option_id: Optional[Union[float, List[float]]] = None,
    ) -> Dict[str, Any]:
        """
        Cancel all orders that match the given filters.

        Parameters
        ----------
        expiration_timestamp : Optional[Union[str, List[str]]], optional
            The expiration timestamp of the options to be canceled, by default None
        instrument_id : Optional[Union[int, List[int]]], optional
            The ID of the instrument(s) whose orders should be canceled, by default None
        instrument_name : Optional[Union[str, List[str]]], optional
            The name of the instrument(s) whose orders should be canceled, by default None
        instrument_type : Optional[Union[str, List[str]]], optional
            The type of instrument(s) whose orders should be canceled, by default None
        strike_price : Optional[Union[float, List[float]]], optional
            The strike price(s) of the options to be canceled, by default None
        option_id : Optional[Union[float, List[float]]], optional
            The option id of the options to be canceled, by default None

        Returns
        -------
        Dict[str, Any]
            A dictionary containing a status code and a message confirming the cancellation of all matching orders.
        """

        url = f"{self.base_url}/orders-all"

        params = self._build_params(
            expiration_timestamp=expiration_timestamp,
            instrument_id=instrument_id,
            instrument_name=instrument_name,
            instrument_type=instrument_type,
            strike_price=strike_price,
            option_id=option_id,
        )

        return self._delete_helper(url, params=params)

    def reduce_order(self, order_id: int, quantity: int) -> Dict[str, Any]:
        """
        Reduce the quantity of a single order by the given amount.

        Parameters
        ----------
        order_id : int
            The ID of the order that should be reduced.
        quantity : int
            The amount by which the order quantity should be reduced.

        Returns
        -------
        Dict[str, Any]
            A dictionary containing a status code and a message confirming the reduction of the order quantity.
        """

        url = f"{self.base_url}/orders/{order_id}"

        body = {"quantity": quantity}

        return self._post_helper(url, body=body)

    def get_trades(
        self,
        instrument_id: Optional[Union[int, List[int]]] = None,
        instrument_name: Optional[Union[str, List[str]]] = None,
        instrument_type: Optional[Union[str, List[str]]] = None,
        strike_price: Optional[Union[float, List[float]]] = None,
        expiration_timestamp: Optional[Union[str, List[str]]] = None,
        option_type: Optional[Union[str, List[str]]] = None,
        limit: int = None,
        offset: int = None,
    ) -> List[Trade]:
        """
        Retrieve a list of trades that match the given filters.

        Parameters
        ----------
        instrument_id : Optional[Union[int, List[int]]], optional
            The ID of the instrument(s) to retrieve trades for, by default None
        instrument_name : Optional[Union[str, List[str]]], optional
            The name of the instrument(s) to retrieve trades for, by default None
        instrument_type : Optional[Union[str, List[str]]], optional
            The type of instrument(s) to retrieve trades for, by default None
        strike_price : Optional[Union[float, List[float]]], optional
            The strike price(s) of the instruments to retrieve trades for, by default None
        expiration_timestamp : Optional[Union[str, List[str]]], optional
            The expiration timestamp(s) of the options to retrieve trades for, by default None
        option_type : Optional[Union[str, List[str]]], optional
            The type(s) of options to retrieve trades for, by default None
        limit : int, optional
            The maximum number of trades to return, by default None
        offset : int, optional
            The initial index of the list of trades to return, by default None

        Returns
        -------
        List[Trade]
            A list of Trade objects that match the given filters.
        """

        url = f"{self.base_url}/trades"

        params = self._build_params(
            instrument_id=instrument_id,
            instrument_name=instrument_name,
            instrument_type=instrument_type,
            strike_price=strike_price,
            expiration_timestamp=expiration_timestamp,
            option_type=option_type,
            limit=limit,
            offset=offset,
        )

        data = self._get_helper(url, params=params)
        return [Trade.from_dict(trade) for trade in data]

    def get_all_trades(
        self,
        instrument_id: Optional[Union[int, List[int]]] = None,
        instrument_name: Optional[Union[str, List[str]]] = None,
        instrument_type: Optional[Union[str, List[str]]] = None,
        strike_price: Optional[Union[float, List[float]]] = None,
        expiration_timestamp: Optional[Union[str, List[str]]] = None,
        option_type: Optional[Union[str, List[str]]] = None,
        limit: int = None,
        offset: int = None,
    ) -> List[Trade]:
        """
        Retrieve a list of all trades across instruments that match the given filters.

        Parameters
        ----------
        instrument_id : Optional[Union[int, List[int]]], optional
            The ID of the instrument(s) to retrieve all trades for, by default None
        instrument_name : Optional[Union[str, List[str]]], optional
            The name of the instrument(s) to retrieve all trades for, by default None
        instrument_type : Optional[Union[str, List[str]]], optional
            The type of instrument(s) to retrieve all trades for, by default None
        strike_price : Optional[Union[float, List[float]]], optional
            The strike price(s) of the instruments to retrieve all trades for, by default None
        expiration_timestamp : Optional[Union[str, List[str]]], optional
            The expiration timestamp(s) of the options to retrieve all trades for, by default None
        option_type : Optional[Union[str, List[str]]], optional
            The type(s) of options to retrieve all trades for, by default None
        limit : int, optional
            The maximum number of trades to return, by default None
        offset : int, optional
            The initial index of the list of trades to return, by default None

        Returns
        -------
        List[Trade]
            A list of Trade objects for all matching instruments.
        """

        url = f"{self.base_url}/trades-all"

        params = self._build_params(
            instrument_id=instrument_id,
            instrument_name=instrument_name,
            instrument_type=instrument_type,
            strike_price=strike_price,
            expiration_timestamp=expiration_timestamp,
            option_type=option_type,
            limit=limit,
            offset=offset,
        )

        data = self._get_helper(url, params=params)
        return [Trade.from_dict(trade) for trade in data]

    def get_positions(
        self,
        instrument_id: Optional[Union[int, List[int]]] = None,
        instrument_name: Optional[Union[str, List[str]]] = None,
        instrument_type: Optional[Union[str, List[str]]] = None,
        strike_price: Optional[Union[float, List[float]]] = None,
        expiration_timestamp: Optional[Union[str, List[str]]] = None,
        option_type: Optional[Union[str, List[str]]] = None,
        limit: int = None,
        offset: int = None,
    ) -> List[Position]:

        """
        Retrieve a list of positions that match the given filters.

        Parameters
        ----------
        instrument_id : Optional[Union[int, List[int]]], optional
            The ID of the instrument(s) to retrieve positions for, by default None
        instrument_name : Optional[Union[str, List[str]]], optional
            The name of the instrument(s) to retrieve positions for, by default None
        instrument_type : Optional[Union[str, List[str]]], optional
            The type of instrument(s) to retrieve positions for, by default None
        strike_price : Optional[Union[float, List[float]]], optional
            The strike price(s) of the instruments to retrieve positions for, by default None
        expiration_timestamp : Optional[Union[str, List[str]]], optional
            The expiration timestamp(s) of the options to retrieve positions for, by default None
        option_type : Optional[Union[str, List[str]]], optional
            The type(s) of options to retrieve positions for, by default None
        limit : int, optional
            The maximum number of positions to return, by default None
        offset : int, optional
            The initial index of the list of positions to return, by default None

        Returns
        -------
        List[Position]
            A list of Position objects that match the given filters.
        """

        url = f"{self.base_url}/positions"

        params = self._build_params(
            instrument_id=instrument_id,
            instrument_name=instrument_name,
            instrument_type=instrument_type,
            strike_price=strike_price,
            expiration_timestamp=expiration_timestamp,
            option_type=option_type,
            limit=limit,
            offset=offset,
        )

        data = self._get_helper(url, params=params)
        return [Position.from_dict(position) for position in data]

    def close_position(
        self, instrument_id: Optional[int] = None, instrument_name: Optional[str] = None
    ):
        """
        Close a position by instrument_id or instrument_name.

        Parameters
        ----------
        instrument_id : Optional[int], optional
            The ID of the instrument to close the position for, by default None
        instrument_name : Optional[str], optional
            The name of the instrument to close the position for, by default None

        Returns
        -------
        Dict[str, Any]
            A dictionary containing a status code and a message confirming the position closure.
        """
        if not instrument_id and not instrument_name:
            raise ValueError(
                "Either instrument_id or instrument_name must be provided."
            )
        elif instrument_id and instrument_name:
            raise ValueError(
                "Only one of instrument_id or instrument_name should be provided."
            )

        url = f"{self.base_url}/positions"
        body = (
            {"instrument_id": instrument_id}
            if instrument_id
            else {"instrument_name": instrument_name}
        )

        return self._delete_helper(url, body=body)
