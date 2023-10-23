from enum import Enum


class OrderType(str, Enum):
    """
    This enum represents the type of an order.
    """

    LIMIT = "Limit"
    MARKET = "Market"


class OptionType(str, Enum):
    """
    This enum represents the type of an option.
    """

    CALL = "Call"
    PUT = "Put"


class SettlementPeriodType(str, Enum):
    """
    This enum represents the settlement period of an instrument.
    """

    Hour = "Hour"
    DAILY = "Day"
    WEEKLY = "Week"
    MONTHLY = "Month"
    QUARTER = "Quarter"
    OTHER = "Other"


class OrderSide(str, Enum):
    """
    This enum represents the side of an order (buy or sell).
    """

    BUY = "Buy"
    SELL = "Sell"


class OrderStatus(str, Enum):
    """
    This enum represents the status of an order.
    """

    OPEN = "Open"
    FILLED = "Filled"
    CANCELLED = "Cancelled"


class TransferType(str, Enum):
    """
    This enum represents the type of a transfer.
    """

    DEPOSIT = "Deposit"
    WITHDRAWAL = "Withdrawal"


class TransferStatus(str, Enum):
    """
    This enum represents the status of a transfer.
    """

    PENDING = "Pending"
    COMPLETED = "Completed"
    FAILED = "Failed"


class InstrumentType(Enum):
    """
    This enum represents the type of an instrument.
    """

    OPTION = "Option"
    FUTURE = "Future"
