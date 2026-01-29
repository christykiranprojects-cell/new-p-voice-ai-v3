class AgentMemory:
    """
    Stores the history of agent decisions for traceability
    and future reflection.

    This step allows the agent to remember what decisions it made and why.
    Without memory, the agent cannot explain its behavior, debug issues, or 
    reflect on past actions.
    This is not learning memory — it is decision trace memory.

    """

    def __init__(self):
        self.history = []

    def record(self, state, reason):
        """
        Records a decision made by the agent.

        Parameters:
        - state: AgentState
        - reason: str
        """
        self.history.append({
            "state": state.name,
            "reason": reason
        })

    def last(self, n=5):
        """
        Returns the last n memory entries.
        """
        return self.history[-n:]

"""
What Agent Memory Is (And Is Not)
SCOPE: 

Agent Memory IS:
- A log of past states
- A log of reasons for decisions
- A tool for debugging and reflection

Agent Memory IS NOT:

- A database
- A vector store
- Long-term learning

Model weights
For now, it is simple and local by design.

Data definition : 
+++++++++++++++++
Each memory entry will contain:
The state the agent moved into
The reason why it moved there

Example entry:
THINK → "System idle, starting reasoning"

What this code represents? 
This class stores a chronological history of the agent’s decisions in memory.
It is intentionally minimal so it is easy to inspect and reason about.

"""
