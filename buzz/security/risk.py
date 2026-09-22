"""Risk classifications for Buzz actions."""

from enum import IntEnum


class RiskLevel(IntEnum):
    READ = 0
    LOW = 1
    CHANGE = 2
    HIGH = 3
    CRITICAL = 4
