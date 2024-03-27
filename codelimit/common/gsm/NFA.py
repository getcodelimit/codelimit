from dataclasses import dataclass

from codelimit.common.gsm.State import State


@dataclass
class NFA:
    start: State
    accepting: State
