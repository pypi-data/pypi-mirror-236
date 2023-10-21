import re
from pathlib import Path

import numpy as np


def assert_single_stack(tif_files: list[Path]) -> str:
    tif_origin = identify_tif_origin(tif_files[0])
    if tif_origin == "leica":
        stack_names = get_leica_stack_names(tif_files)
    else:
        raise NotImplementedError(f"{tif_origin=} not implemented.")
    assert len(stack_names) == 1, f"More than 1 stack in {tif_files[0].parent}: {stack_names}"
    print(f"Only one stack: {stack_names[0]}")
    return stack_names[0]


def identify_tif_origin(tif: Path) -> str:
    if "ch00" in tif.name:
        origin = "leica"
    elif "LUT" in tif.name:
        origin = "leica_metadata"
    else:
        origin = "basler"
    return origin


def get_leica_stack_names(tif_files: list[Path]) -> list:
    stack_names = []
    for file in tif_files:
        stack_name = re.findall(r".+(?=_[tz][0-9]+)", file.name)[0]
        if stack_name not in stack_names:
            stack_names.append(stack_name)
    return stack_names


def list_tif_files(folder: Path) -> list:
    """List all tif files in a local folder."""
    tif_files = []
    for element in folder.iterdir():
        if element.is_file():
            if element.suffix in [".tif", ".tiff"]:
                tif_files.append(element)
    return tif_files


def sort_tif_files(tif_files: list[Path]) -> np.ndarray:
    if "ch00" in tif_files[0].name:
        frame_numbers = [get_leica_frame_number(x) for x in tif_files]
    else:
        frame_numbers = [get_basler_frame_number(x) for x in tif_files]
    check_completeness(frame_numbers)
    sort_vector = np.argsort(frame_numbers)
    tif_files = np.asarray(tif_files)
    tif_files = tif_files[sort_vector]
    return tif_files


def get_leica_frame_number(leica_file: Path) -> int:
    frame_number = re.findall(r"(?<=[tz])[0-9]+", leica_file.name)[0]
    # print(leica_file.name, frame_number)
    frame_number = int(frame_number)
    return frame_number


def get_basler_frame_number(basler_file: Path) -> int:
    frame_number = re.findall(r"[0-9]+(?=.tif)", basler_file.name)[0]
    frame_number = int(frame_number)
    return frame_number


def check_completeness(frame_numbers: list, verbose: bool = True) -> None:
    lowest = np.min(frame_numbers)
    highest = np.max(frame_numbers)
    all_possible = np.arange(lowest, highest)
    assert np.all(np.isin(all_possible, frame_numbers)), "Some frame numbers are missing!"
    if verbose:
        print(f"Frame numbers: {lowest} -> {highest} (count: {len(frame_numbers)})")