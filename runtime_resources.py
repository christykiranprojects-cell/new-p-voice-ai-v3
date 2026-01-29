import os
import torch


def configure_runtime(agent_name: str, agent_state):
    """
    Configures runtime resources based on agent intent.
    CPU-only, student-safe implementation.
    """

    if agent_state.name == "ACT":
        threads = 4
    else:
        threads = 2

    torch.set_num_threads(threads)
    os.environ["OMP_NUM_THREADS"] = str(threads)
    os.environ["MKL_NUM_THREADS"] = str(threads)

    print(
        f"[{agent_name}] Runtime configured → "
        f"CPU threads = {threads} (state={agent_state.name})"
    )
