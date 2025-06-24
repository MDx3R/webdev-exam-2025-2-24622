from abc import ABC, abstractmethod
from datetime import date, datetime, time, timezone


class Clock(ABC):
    def __init__(self) -> None:
        self._tzinfo = timezone.utc

    @abstractmethod
    def now(self) -> datetime: ...

    def timezone(self) -> timezone:
        return self._tzinfo

    def combine(self, date: date, time: time) -> datetime:
        return datetime.combine(date, time, tzinfo=self._tzinfo)


class SystemClock(Clock):
    def now(self) -> datetime:
        return datetime.now(self._tzinfo)


class FixedClock(Clock):
    def __init__(self, fixed_time: datetime):
        super().__init__()
        if fixed_time.tzinfo != self._tzinfo:
            fixed_time = fixed_time.replace(tzinfo=self._tzinfo)
        self._fixed_time = fixed_time

    def now(self) -> datetime:
        return self._fixed_time


class GlobalClock:
    _clock: Clock | None = None

    @classmethod
    def set_clock(cls, clock: Clock):
        cls._clock = clock

    @classmethod
    def now(cls) -> datetime:
        if cls._clock is None:
            # По умолчанию системное время UTC
            return datetime.now(timezone.utc)
        return cls._clock.now()
