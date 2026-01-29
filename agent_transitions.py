# agent core 2 : Deterministic State Machine: State machine 2
# if it is allowed

"""
Narration : 

This block enforces which state transitions are legal, acting as the safety guardrail for the agent.
Even if reasoning makes a mistake, illegal transitions are blocked here.

"""

from agent_state import AgentState

ALLOWED_TRANSITIONS = {
    AgentState.IDLE: {AgentState.THINK},
    AgentState.THINK: {AgentState.ACT, AgentState.IDLE},
    AgentState.ACT: {AgentState.THINK, AgentState.EMERGENCY},
    AgentState.EMERGENCY: {AgentState.IDLE},
}
