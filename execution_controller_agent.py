from agent_state import AgentState
from agent_reasoner import AgentReasoner
from agent_memory import AgentMemory
from agent_transitions import ALLOWED_TRANSITIONS
from runtime_resources import configure_runtime

import whisper
import torch
import os


class ExecutionControllerAgent:
    """
    Owns:
    - Agent state transitions
    - Reasoning decisions
    - Runtime configuration
    - CPU thread control (ACT state only)
    - Whisper model lifecycle (single source of truth)
    """

    def __init__(self, name="execution_controller_agent"):
        self.name = name
        self.state = AgentState.IDLE
        self.reasoner = AgentReasoner()
        self.memory = AgentMemory()
        self.model = None

    # ==============================
    # CPU THREAD CONTROL (CRITICAL)
    # ==============================
    def _configure_cpu_threads_for_act(self):
        """
        Configure CPU threads for heavy compute (transcription).
        This affects Whisper inference latency, not just model loading.
        """
        # Recommended for 10–12 logical processors
        target_threads = 4

        before = torch.get_num_threads()

        torch.set_num_threads(target_threads)
        torch.set_num_interop_threads(1)

        after = torch.get_num_threads()

        print(
            f"[{self.name}] CPU threads configured for ACT: "
            f"{before} → {after}"
        )

    # ==============================
    # STATE MACHINE STEP
    # ==============================
    def step(self, observation=None):
        """
        Move agent to the next valid state based on reasoning.
        Thread scaling is applied ONLY when entering ACT.
        """
        if observation is None:
            observation = {}

        next_state, reason = self.reasoner.decide_next_state(
            self.state, observation
        )

        if next_state not in ALLOWED_TRANSITIONS[self.state]:
            raise RuntimeError(
                f"Illegal transition: {self.state.name} → {next_state.name}"
            )

        self.state = next_state
        self.memory.record(self.state, reason)

        # Runtime config (CPU governor, affinity, etc.)
        configure_runtime(self.name, self.state)

        # THREAD SCALING HAPPENS HERE
        if self.state == AgentState.ACT:
            print(f"[DEBUG] Entered ACT state")
            self._configure_cpu_threads_for_act()

        return self.state

    # ==============================
    # WHISPER MODEL LIFECYCLE
    # ==============================
    def load_model(self, model_name="large-v1", device="cpu"):
        """
        Load Whisper model ONLY in ACT state.
        Thread configuration is already applied before inference.
        """
        if self.state != AgentState.ACT:
            raise RuntimeError(
                "Model loading attempted outside ACT state"
            )

        if self.model is None:
            print(
                f"[{self.name}] Loading Whisper model: {model_name} on {device}"
            )
            self.model = whisper.load_model(model_name, device=device)
            print(f"[{self.name}] Whisper model loaded successfully")

        return self.model

    def get_model(self):
        """
        Safe accessor for already-loaded model.
        """
        if self.model is None:
            raise RuntimeError("Model requested before loading")
        return self.model
