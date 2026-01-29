from execution_controller_agent import ExecutionControllerAgent
from data_pipeline.run_phase_B import run_phase_B


def main():
    print("🚀 Starting system")

    # Initialize execution controller agent
    agent = ExecutionControllerAgent()

    # -----------------------------
    # STATE FLOW
    # -----------------------------

    # IDLE → THINK
    agent.step()

    # THINK → ACT
    agent.step(observation={"task_ready": True})

    # -----------------------------
    # MODEL LOADING (Agent-owned)
    # -----------------------------

    whisper_model = agent.load_model(
        model_name="large-v1",
        device="cpu"
    )

    # -----------------------------
    # PIPELINE EXECUTION
    # -----------------------------

    run_phase_B(whisper_model)

    print("✅ System finished cleanly")


if __name__ == "__main__":
    main()

# new_p_voice_ai_v3.python_main

