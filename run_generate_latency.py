import subprocess
import sys

def main():
    subprocess.run(
        [
            sys.executable,
            "-m",
            "data_pipeline.generate_latency_report"
        ],
        check=True
    )

if __name__ == "__main__":
    main()
