# agent core 1: Deterministic State Machine : State machine 1

"""
NARRATION : 
This block defines a fixed, safe set of system-level states using an Enum.
Enums prevent invalid states, typos, and unsafe comparisons.
"""

from enum import Enum, auto


class AgentState(Enum):
    IDLE = auto()
    THINK = auto()
    ACT = auto()
    EMERGENCY = auto()

"""
One-Line Summary

Enum defines safe, fixed states; auto() assigns values automatically we can 
focus on meaning, not numbers.

✔ Enum = creates named system states
✔ auto() = automatically assigns unique values
✔ Used to prevent bugs and enforce correctness
✔ Perfect choice for agents state machine

STATES : 
- IDLE → System is waiting, doing nothing.
- THINK → System is reasoning about the next action.
- ACT → System is executing a chosen action.
- EMERGENCY → System entered a safety or error condition.

auto() ensures:
- Unique values
- No reliance on numbers
- Safe future extensions
"""