import json
from datetime import datetime
from uuid import uuid4
from eth_account.datastructures import SignedMessage
from datetime import datetime
from d2y.structured_data import create_structured_order_data
from web3 import Web3


def generate_random_uint64():
    return uuid4().int & (1 << 64) - 1


def sign_order(
    signer_key: str,
    wallet_address,
    option_address,
    price,
    amount,
    expiry_timestamp: datetime,
    unique_reference_id,
    chain_id,
    exchange_contact_address,
    side,
) -> SignedMessage:
    message_to_sign = create_structured_order_data(
        option_address,
        wallet_address,
        price,
        amount,
        expiry_timestamp,
        unique_reference_id,
        chain_id,
        exchange_contact_address,
        side,
    )

    return Web3().eth.account.sign_message(message_to_sign, signer_key)


def convert_datetime_to_iso(data):
    if isinstance(data, datetime):
        return data.isoformat()

    if isinstance(data, list):
        return [convert_datetime_to_iso(item) for item in data]

    if isinstance(data, dict):
        return {key: convert_datetime_to_iso(value) for key, value in data.items()}

    return data
