import argparse
import re
import logging
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from shutil import move

parser = argparse.ArgumentParser(description="Sorting folder")
parser.add_argument("--source", "-s", help="Source folder", required=True)
parser.add_argument("--output", "-o", help="Output folder", default="dist")

args = vars(parser.parse_args())
source = Path(args.get("source"))
output = Path(args.get("output"))


def generate_new_name(file_path: Path):
    file_name = file_path.stem
    file_extension = file_path.suffix
    match = re.search(r"\((\d+)\)$", file_name)
    n = 1
    if match:
        n = int(match.group(1)) + 1
        file_name = file_name[: match.start()]
    new_file = file_path.parent / f"{file_name}({n}){file_extension}"
    return new_file


def move_file(el):
    ext = el.suffix[1:]
    ext_folder = output / ext

    try:
        ext_folder.mkdir(exist_ok=True, parents=True)
        dest_file = ext_folder / el.name
        is_exists_file = dest_file.exists()
        is_need_rename = is_exists_file and (
            el.stat().st_size != dest_file.stat().st_size
            or el.stat().st_mtime != dest_file.stat().st_mtime
        )

        if is_need_rename:
            while dest_file.exists():
                dest_file = generate_new_name(dest_file)

        if not is_exists_file or is_need_rename:
            # copy2(el, dest_file)
            move(el, dest_file)
        else:
            el.unlink()

    except OSError as err:
        logging.error(err)


def scan_folder(folder: Path, executor: ThreadPoolExecutor) -> None:
    logging.info(f"Scanning folder {folder}")
    for el in folder.iterdir():
        if el.is_dir():
            # logging.info(f"Add dir({el}) to executer")
            future = executor.submit(scan_folder, el, executor)
            # logging.info(f"!!! executor: {executor._threads}")
            future.result()
            # futures.append(future)
        else:
            move_file(el)

    logging.info(f"Scanning folder {folder} finished successfully")
    # logging.info(f"### executor: {executor._threads}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(threadName)s: %(message)s")

    with ThreadPoolExecutor(max_workers=10) as executor:
        future = executor.submit(scan_folder, source, executor)
        future.result()

    logging.info("End program")
    executor.shutdown(wait=True)
