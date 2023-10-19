# experiment.py

from typing import Iterable, List, Tuple, Optional, Sequence, Union

from attrs import define

import numpy as np

from market_break.process import array

__all__ = [
    "minimum_maximum_index",
    "long_short_results",
    "TradingRecord",
    "ShortTradingRecord",
    "LongTradingRecord",
    "Backtester"
]

def minimum_maximum_index(
        data: Sequence[float], up: Sequence[int], down: Sequence[int]
) -> Tuple[List[int], List[int]]:
    """
    Calculates the minimum and maximum signals from the trends.

    :param data: The data for the indicator.
    :param up: The up-trends indexes.
    :param down: The down-trends indexes.

    :return: The minimum and maximum indexes.
    """

    buy = []
    sell = []

    for i in range(len(data)):
        if (i in up) and (len(buy) == len(sell)):
            up = up[up.index(i) + 1:]

            buy.append(i)

        elif (i in down) and (len(buy) > len(sell)):
            down = down[down.index(i) + 1:]

            sell.append(i)
        # end if
    # end for

    return buy, sell
# end minimum_maximum_index

@define
class TradingRecord:
    """A class to represent the trading record."""

    returns: np.ndarray
    entries: np.ndarray
    exits: np.ndarray
    data: Iterable[float]
    minimum: Iterable[int]
    maximum: Iterable[int]
    long: Optional[bool] = True
    short: Optional[bool] = True
    volume: Optional[float] = 1.0
    fee: Optional[float] = 0.0
    take: Optional[float] = None
    stop: Optional[float] = None
# end TradingRecord

class LongTradingRecord(TradingRecord):
    """A class to represent the trading record."""
# end LongTradingRecord

class ShortTradingRecord(TradingRecord):
    """A class to represent the trading record."""
# end ShortTradingRecord

def difference(
        current: float, previous: float, fee: Optional[float] = 0.0
) -> float:
    """
    Calculates the relative difference between the values, with fee.

    :param current: The curren value.
    :param previous: The last value.
    :param fee: The fee to take off.

    :return: The difference.
    """

    return ((current - previous) / previous) * (1 - fee)
# end difference

class Backtester:
    """A class to run a backtest."""

    def __init__(self) -> None:
        """Defines the attributes of the backtester."""

        self.long_returns = []
        self.short_returns = []

        self.is_long = False
        self.is_short = False
        self.long_allowed = False
        self.short_allowed = False

        self.parallel: Optional[bool] = None

        self.last_long = 0
        self.last_short = 0

        self.i = 0
        self.fee = 0

        self.take: Optional[float] = None
        self.stop: Optional[float] = None

        self.long_entries = []
        self.short_entries = []
        self.long_exits = []
        self.short_exits = []

        self.data: Optional[Sequence[float]] = None
        self.minimum: Optional[List[int]] = None
        self.maximum: Optional[List[int]] = None
    # end __init__

    def should_take_profit_long(self, take: Optional[float] = None) -> bool:
        """
        Checks if the backtester should exit to take long profit.

        :param take: The take profit value.

        :return: The validation flag.
        """

        if take is None:
            take = self.take
        # end if

        return (take is not None) and (self.last_long * take <= self.data[self.i])
    # end should_take_profit_long

    def should_stop_loss_long(self, stop: Optional[float] = None) -> bool:
        """
        Checks if the backtester should exit to stop long loss.

        :param stop: The stop loss value.

        :return: The validation flag.
        """

        if stop is None:
            stop = self.stop
        # end if

        return (stop is not None) and (self.last_long * (1 - stop) >= self.data[self.i])
    # end should_stop_loss_long

    def should_take_profit_short(self, take: Optional[float] = None) -> bool:
        """
        Checks if the backtester should exit to take short profit.

        :param take: The take profit value.

        :return: The validation flag.
        """

        if take is None:
            take = self.take
        # end if

        return (take is not None) and (self.last_short * take >= self.data[self.i])
    # end should_take_profit_short

    def should_stop_loss_short(self, stop: Optional[float] = None) -> bool:
        """
        Checks if the backtester should exit to stop short long.

        :param stop: The stop loss value.

        :return: The validation flag.
        """

        if stop is None:
            stop = self.stop
        # end if

        return (stop is not None) and (self.last_short * (1 - stop) <= self.data[self.i])
    # end should_stop_loss_short

    def enter_long(self) -> None:
        """Enters a long position."""

        self.minimum = self.minimum[self.minimum.index(self.i) + 1:]

        self.is_long = True
        self.last_long = self.data[self.i]

        self.long_entries.append(self.i)
        self.long_returns.append(self.long_returns[-1])

        self.long_allowed = False
    # end enter_long

    def step_long(self) -> None:
        """Steps for the long data."""

        if self.is_long:
            self.long_returns.append(
                self.long_returns[-1] +
                difference(
                    current=self.data[self.i],
                    previous=self.data[self.i - 1]
                )
            )

        else:
            self.long_returns.append(self.long_returns[-1])
        # end if
    # end step_long

    def exit_long(self, fee: Optional[Union[float, bool]] = None) -> None:
        """
        Exits a long position.

        :param fee: The fee to add to the calculation.
        """

        if fee in (None, True):
            fee = self.fee
        # end if

        if fee is False:
            fee = 0.0
        # end if

        self.is_long = False

        self.long_exits.append(self.i)
        self.long_returns.append(
            self.long_returns[-1] +
            difference(
                current=self.data[self.i],
                previous=self.data[self.i - 1],
                fee=fee
            )
        )

        self.long_allowed = False
    # end step_long

    def enter_short(self) -> None:
        """Enters a short position."""

        self.maximum = self.maximum[self.maximum.index(self.i) + 1:]

        self.is_short = True
        self.last_short = self.data[self.i]

        self.short_entries.append(self.i)
        self.short_returns.append(self.short_returns[-1])

        self.short_allowed = False
    # end enter_short

    def step_short(self) -> None:
        """Steps the short data."""

        if self.is_short:
            self.short_returns.append(
                self.short_returns[-1] -
                difference(
                    current=self.data[self.i],
                    previous=self.data[self.i - 1]
                )
            )

        else:
            self.short_returns.append(self.short_returns[-1])
        # end if
    # end step_short

    def exit_short(self, fee: Optional[Union[float, bool]] = None) -> None:
        """"
        Exits a short position.

        :param fee: The fee to add to the calculation.
        """

        if fee in (None, True):
            fee = self.fee
        # end if

        if fee is False:
            fee = 0.0
        # end if

        self.is_short = False

        self.short_exits.append(self.i)
        self.short_returns.append(
            self.short_returns[-1] -
            difference(
                current=self.data[self.i],
                previous=self.data[self.i - 1],
                fee=fee
            )
        )

        self.short_allowed = False
    # end exit_short

    def next(self) -> None:
        """Takes the next iteration step."""

        self.long_allowed = True
        self.short_allowed = True

        exit_long = (
            self.is_long and
            (
                self.should_take_profit_long() or
                self.should_stop_loss_long()
            )
        )
        exit_short = (
            self.is_short and
            (
                self.should_take_profit_short() or
                self.should_stop_loss_short()
            )
        )
        enter_long = (
            self.long_allowed and
            (not self.is_long) and
            (not self.parallel or not self.is_short) and
            (self.i in self.minimum)
        )
        enter_short = (
            self.short_allowed and
            (not self.is_short) and
            (not self.parallel or not self.is_long) and
            (self.i in self.maximum)
        )
        step_long = (
            (not enter_long) and
            (not exit_long) and
            ((not self.long_exits) or (self.long_exits[-1] != self.i)) and
            ((not self.long_entries) or (self.long_entries[-1] != self.i))
        )
        step_short = (
            (not enter_short) and
            (not exit_short) and
            ((not self.short_exits) or (self.short_exits[-1] != self.i)) and
            ((not self.short_entries) or (self.short_entries[-1] != self.i))
        )

        if enter_long and enter_short:
            self.step_long()
            self.step_short()

            return
        # end if

        if step_long:
            self.step_long()

        elif enter_long:
            self.enter_long()

        elif exit_long:
            self.exit_long(fee=False)
        # end if

        if step_short:
            self.step_short()

        elif enter_short:
            self.enter_short()

        elif exit_short:
            self.exit_short(fee=False)
        # end if
    # end next

    def results(
            self,
            data: Iterable[float],
            minimum: Iterable[int],
            maximum: Iterable[int],
            volume: Optional[float] = 1.0,
            fee: Optional[float] = 0.0,
            take: Optional[float] = None,
            stop: Optional[float] = None,
            parallel: Optional[bool] = False
    ) -> Tuple[LongTradingRecord, ShortTradingRecord]:
        """
        Calculates the long and short signals from the indexes.

        :param data: The data for the indicator.
        :param minimum: The minimum indexes.
        :param maximum: The maximum indexes.
        :param volume: The initial investment volume.
        :param fee: The fee for an action.
        :param take: The take profit threshold.
        :param stop: The stop loss threshold.
        :param parallel: The value to allow multiple positions at once.

        :return: The long and short indexes.
        """

        self.fee = fee
        self.stop = stop
        self.take = take
        self.parallel = parallel

        self.data = array(data)

        saved_minimum = minimum
        self.minimum = list(minimum)

        saved_maximum = maximum
        self.maximum = list(maximum)

        self.long_returns.append(volume)
        self.short_returns.append(volume)

        for i in range(1, len(self.data)):
            self.i = i

            self.next()
        # end for

        return (
            LongTradingRecord(
                returns=np.array(self.long_returns),
                entries=np.array(self.long_entries).astype(int),
                exits=np.array(self.long_exits).astype(int),
                data=data, minimum=saved_minimum, maximum=saved_maximum,
                volume=volume, fee=fee, take=take, stop=stop
            ),
            ShortTradingRecord(
                returns=np.array(self.short_returns),
                entries=np.array(self.short_entries).astype(int),
                exits=np.array(self.short_exits).astype(int),
                data=data, minimum=saved_minimum, maximum=saved_maximum,
                volume=volume, fee=fee, take=take, stop=stop
            )
        )
    # end results
# end Backtester

def long_short_results(
        data: Iterable[float],
        minimum: Iterable[int],
        maximum: Iterable[int],
        volume: Optional[float] = 1.0,
        fee: Optional[float] = 0.0,
        take: Optional[float] = None,
        stop: Optional[float] = None,
        parallel: Optional[bool] = False
) -> Tuple[LongTradingRecord, ShortTradingRecord]:
    """
    Calculates the long and short signals from the indexes.

    :param data: The data for the indicator.
    :param minimum: The minimum indexes.
    :param maximum: The maximum indexes.
    :param volume: The initial investment volume.
    :param fee: The fee for an action.
    :param take: The take profit threshold.
    :param stop: The stop loss threshold.
    :param parallel: The value to allow multiple positions at once.

    :return: The long and short indexes.
    """

    return Backtester().results(
        data=data, minimum=minimum, maximum=maximum,
        volume=volume, fee=fee,
        take=take, stop=stop,
        parallel=parallel
    )
# end long_short_results