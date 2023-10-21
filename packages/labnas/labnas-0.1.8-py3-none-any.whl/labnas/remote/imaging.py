"""NAS interactions specific to imaging data."""
import re
from pathlib import Path

from tqdm import tqdm

from labnas.remote.base import SftpNas
from labnas.local.base import identify_tif_origin


class ImagingNas(SftpNas):
    """Extends SftpNas for imaging data."""

    def sort_folder(self, remote_folder: Path) -> None:
        """Sort a folder with imaging .tif files."""
        print(f"---Sorting {remote_folder}---")
        needs_sorting, stacks, single_tifs = self.check_folder_structure(remote_folder)
        if needs_sorting:
            print(f"Sorting {remote_folder}")
            print(f"{len(stacks)} stacks found in {remote_folder}")
            for stack_name, stack_tifs in stacks.items():
                self.sort_single_stack(stack_name, remote_folder, stack_tifs)
        else:
            if len(stacks) > 0:
                stack_name = list(stacks.keys())[0]
                stack_size = len(stacks[stack_name])
                print(f"{remote_folder} is sorted (stack '{stack_name}' with {stack_size} tifs)")
            elif len(single_tifs) > 0:
                print(f"{remote_folder} is sorted ({len(single_tifs)} single tifs).")
            else:
                print(f"No tifs in {remote_folder}")

    def sort_single_stack(self, stack_name: str, remote_folder: Path, stack_files: list[Path]) -> None:
        """Move .tif files belonging to a single stack into a dedicated folder."""
        print(f"{len(stack_files)} tifs in stack {stack_name}.")
        parent_directory = remote_folder / stack_name
        if parent_directory.is_dir():
            raise FileExistsError(f"{parent_directory}")
        self.connection.mkdir(str(parent_directory))
        for file in tqdm(stack_files):
            new_path = parent_directory / file.name
            self.move_file(file, new_path)
        print(f"Moved {len(stack_files)} tifs into {parent_directory}.")

    def check_folder_structure(self, remote_folder: Path) -> tuple[bool, dict, list]:
        """
        Check if a folder contains .tif files belonging to more than 1 stack.
        Also return stacks and tifs because scanning large folders takes time.
        """
        tifs = self.find_tifs_in_folder(remote_folder)
        if len(tifs) == 0:
            print(f"No tifs - will not look for stacks in {remote_folder}.")
            needs_sorting = False
            stacks = {}
            single_tifs = []
        elif len(tifs) == 1:
            print(f"Only 1 tif - will not look for stacks in {remote_folder}.")
            needs_sorting = False
            stacks = {}
            single_tifs = tifs
        else:
            print(f"{len(tifs)} tifs in {remote_folder} - looking for stacks.")
            needs_sorting, stacks, single_tifs = self.divide_into_single_and_stacks(tifs)
        return needs_sorting, stacks, single_tifs

    def divide_into_single_and_stacks(self, tifs: list) -> tuple[bool, dict, list]:
        """Check if tifs belong to one or more stacks."""
        stacks, single_tifs = self.identify_stacks_in_tifs(tifs)
        print(f"{len(stacks)} stacks and {len(single_tifs)} single tifs in {tifs[0].parent}.")
        is_multiple_stacks = len(stacks) > 1
        is_one_stack_and_singles = (len(stacks) > 0) and (len(single_tifs) > 0)
        needs_sorting = is_multiple_stacks or is_one_stack_and_singles
        return needs_sorting, stacks, single_tifs

    def identify_stacks_in_tifs(self, tifs: list[Path]) -> tuple[dict, list]:
        tif_origin = identify_tif_origin(tifs[0])
        if tif_origin == "leica":
            print(f"Tifs (e.g. {tifs[0].name}) identified as leica tifs")
            stacks, single_tifs = self.identify_leica_stacks_in_tifs(tifs)
        elif tif_origin == "basler":
            print(f"Tifs (e.g. {tifs[0].name}) identified as basler tifs")
            stacks, single_tifs = self.identify_basler_stacks_in_tifs(tifs)
        elif tif_origin == "leica_metadata":
            print(f"{tifs[0].parent} includes leica metadata tifs. Will not sort.")
            single_tifs = tifs
            stacks = {}
        else:
            print(f"Could not identify stacks: neither leica nor basler.")
            single_tifs = tifs
            stacks = {}
        return stacks, single_tifs

    def find_stacks_in_folder(self, remote_folder: Path) -> dict:
        tifs = self.find_tifs_in_folder(remote_folder)
        if len(tifs) == 1:
            print(f"Only a single tif {tifs[0]}, will not check for stacks.")
            stacks = {}
        elif len(tifs) > 1:
            stacks, single_tifs = self.identify_stacks_in_tifs(tifs)
        else:
            stacks = {}
        return stacks

    def find_tifs_in_folder(self, remote_folder: Path) -> list[Path]:
        """Find tif files in a remote folder."""
        files, folders = self.list_files_and_folders(remote_folder)
        tifs = self.identify_tifs_in_files(files)
        return tifs

    def identify_tifs_in_files(self, files: list[Path]) -> list[Path]:
        """Identify tif files in a list of files."""
        tifs = []
        for file in files:
            if file.suffix in [".tif", ".tiff"]:
                tifs.append(file)
        return tifs

    def identify_leica_stacks_in_tifs(self, tifs: list[Path]) -> tuple[dict, list]:
        """Sort tif files into stacks belonging to a single recording."""
        stacks = {}
        single_tifs = []
        for file in tifs:
            file_name = file.name
            findings = re.findall("_[zt][0-9]+_", file_name)
            if findings:
                splitter = findings[0]
                parts = file_name.split(splitter)
                stack_name = parts[0]
                if stack_name not in stacks.keys():
                    print(f"Stack in {tifs[0].parent}: {stack_name}")
                    stacks[stack_name] = []
                stacks[stack_name].append(file)
            else:
                single_tifs.append(file)
        keys_to_delete = []
        for stack_name, stack_list in stacks.items():
            if len(stack_list) == 1:
                single_tifs.append(stack_list[0])
                keys_to_delete.append(stack_name)
                print(f"Only 1 tif in stack {stack_name} -> Appending to single tifs.")
        for key in keys_to_delete:
            del stacks[key]
        return stacks, single_tifs

    def identify_basler_stacks_in_tifs(self, tifs: list[Path]) -> tuple[dict, list]:
        """Sort tif files into stacks belonging to a single recording."""
        stacks = {}
        single_tifs = []
        for file in tifs:
            parts = file.name.split("_")
            index_part = parts[-1]
            stack_name = "_".join(parts[:-1])
            if stack_name not in stacks.keys():
                stacks[stack_name] = []
            stacks[stack_name].append(file)
        return stacks, single_tifs
