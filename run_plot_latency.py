import subprocess
import sys

def main():
    subprocess.run(
        [
            sys.executable,
            "-m",
            "data_pipeline.plot_latency_from_consolidated"
        ],
        check=True
    )

if __name__ == "__main__":
    main()
