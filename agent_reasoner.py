from agent_state import AgentState


class AgentReasoner:
    def decide_next_state(self, current_state, observation):
        if observation.get("error", False):
            return AgentState.EMERGENCY, "Error detected in system"

        if current_state == AgentState.IDLE:
            return AgentState.THINK, "System idle, starting reasoning"

        if current_state == AgentState.THINK:
            if observation.get("task_ready", False):
                return AgentState.ACT, "Task identified, ready to act"
            return AgentState.IDLE, "No task found, returning to idle"

        if current_state == AgentState.ACT:
            return AgentState.THINK, "Action completed, reflecting"

        return AgentState.IDLE, "Default fallback decision"
