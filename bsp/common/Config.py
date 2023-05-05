from dataclasses import dataclass

@dataclass
class Config:
    RETRY: int = 5
    TIME_WAIT_EXCEPTION: int = 1
    TIMEOUT_MODBUS: int = 30