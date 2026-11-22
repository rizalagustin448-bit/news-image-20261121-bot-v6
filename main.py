import os
import shutil
from pathlib import Path


def main():
    out = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out.mkdir(parents=True, exist_ok=True)
    src = Path(__file__).resolve().parent / "entry.png"
    shutil.copyfile(src, out / "entry.png")


if __name__ == "__main__":
    main()
