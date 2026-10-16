import subprocess
import sys

def run_script(script: str) -> None:
    print(f"\n=== Running {script} ===")
    result = subprocess.run(
        [sys.executable, script],
        check=False,
    )

    if result.returncode != 0:
        raise SystemExit(f"The script {script} failed with code {result.returncode} ")

def main() -> None:
    run_script("extract.py")
    run_script("transform.py")
    run_script("load.py")
    print("\nPipeline completed correctly")


if __name__ == "__main__":
    main()