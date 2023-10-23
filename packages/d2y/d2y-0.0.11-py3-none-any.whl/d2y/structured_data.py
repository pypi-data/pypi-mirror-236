from datetime import datetime
from eth_account.messages import encode_structured_data
from d2y.enums import OrderSide


def create_structured_order_data(
    option_address,
    wallet_address,
    price,
    amount,
    expiry_timestamp: datetime,
    unique_reference_id,
    chain_id,
    exchange_contact_address,
    side,
):
    typed_data = {
        "types": {
            "EIP712Domain": [
                {"name": "name", "type": "string"},
                {"name": "version", "type": "string"},
                {"name": "chainId", "type": "uint256"},
                {"name": "verifyingContract", "type": "address"},
            ],
            "Order": [
                {"name": "price", "type": "uint256"},
                {"name": "amount", "type": "int256"},
                {"name": "orderId", "type": "uint64"},
                {"name": "optionId", "type": "uint64"},
                {"name": "orderExpiryTimestamp", "type": "uint64"},
                {"name": "user", "type": "address"},
            ],
        },
        "primaryType": "Order",
        "domain": {
            "name": "D2Y",
            "version": "1.0.0",
            "chainId": chain_id,
            "verifyingContract": exchange_contact_address,
        },
        "message": {
            "price": int(price * 10**6),
            "amount": int(amount * 10**2)
            if side == OrderSide.BUY
            else -(int(amount * 10**2)),
            "orderId": int(unique_reference_id),
            "optionId": int(option_address),
            "orderExpiryTimestamp": int(expiry_timestamp.timestamp()),
            "user": wallet_address,
        },
    }

    return encode_structured_data(typed_data)
