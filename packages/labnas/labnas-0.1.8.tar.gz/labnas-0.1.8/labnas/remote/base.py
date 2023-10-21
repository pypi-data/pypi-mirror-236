"""Basic connection to a network-associated server (NAS)."""
import os
from pathlib import Path

import pysftp
from tqdm import tqdm


class SftpNas:
    """Basic SFTP connection (wrapper around pysftp)"""

    def __init__(self, host_name: str, user_name: str, pwd: str) -> None:
        """Create pysftp.Connection to server."""
        self.connection: pysftp.Connection = pysftp.Connection(
            host=host_name,
            username=user_name,
            password=pwd,
        )
        print(f"Connection established: {host_name}@{user_name}")
        self._host_name = host_name
        self._user_name = user_name
        self._pwd = pwd

    def close(self) -> None:
        """Close connection."""
        self.connection.close()

    def reconnect(self) -> None:
        try:
            self.connection.close()
        except Exception as e:
            print(f"Could not close connection: {e}")
        self.connection: pysftp.Connection = pysftp.Connection(
            host=self._host_name,
            username=self._user_name,
            password=self._pwd,
        )

    def list_contents(self, remote_folder: Path) -> list[Path]:
        """List contents of a remote folder"""
        if not self.is_dir(remote_folder):
            raise FileNotFoundError(f"{remote_folder} not found.")
        contents: list[str] = self.connection.listdir(str(remote_folder))
        contents: list[Path] = [remote_folder / name for name in contents]
        return contents

    def is_dir(self, remote_path: Path) -> bool:
        """Check whether a remote path is a directory."""
        return self.connection.isdir(str(remote_path))

    def list_files_and_folders(self, remote_folder: Path) -> tuple:
        """List contents of a remote folder sorted into files and folders"""
        files = []
        folders = []
        contents = self.list_contents(remote_folder)
        for element in contents:
            if self.is_file(element):
                files.append(element)
            elif self.is_dir(element):
                folders.append(element)
            else:
                raise ValueError(f"{element} is neither file nor folder?")
        return files, folders

    def is_file(self, remote_path: Path) -> bool:
        """Check whether a remote path is a file."""
        return self.connection.isfile(str(remote_path))

    def download_file(self, remote_file: Path, local_file: Path, overwrite: bool = False) -> None:
        """Download a single file from the server"""
        if not self.is_file(remote_file):
            raise FileNotFoundError(f"{remote_file} does not exist.")
        if not local_file.parent.is_dir():
            raise FileNotFoundError(f"Target parent folder {local_file.parent} does not exist.")
        if local_file.is_file() and not overwrite:
            raise FileExistsError(f"{local_file} already exists.")
        self.connection.get(str(remote_file), str(local_file))

    def upload_file(self, local_file: Path, remote_file: Path) -> None:
        """Upload a single file to the server"""
        if not local_file.is_file():
            raise FileNotFoundError(f"{local_file} does not exist.")
        if not self.is_dir(remote_file.parent):
            raise FileNotFoundError(f"Target parent folder {remote_file.parent} does not exist.")
        if self.is_file(remote_file):
            raise FileExistsError(f"{remote_file} already exists.")
        self.connection.put(str(local_file), str(remote_file))

    def download_folder(self, remote_folder: Path, local_parent: Path, recursive: bool = True) -> Path:
        """Download a whole folder from the server"""
        if not self.is_dir(remote_folder):
            raise FileNotFoundError(f"{remote_folder} does not exist.")
        if not local_parent.is_dir():
            raise FileNotFoundError(f"Target parent folder {local_parent} does not exist.")
        local_folder = local_parent / remote_folder.name
        if local_folder.is_dir():
            raise FileExistsError(f"{local_folder} already exists.")
        os.mkdir(local_folder)
        files, folders = self.list_files_and_folders(remote_folder)
        print(f"{len(files)} files found in {remote_folder}.")
        print(f"{len(folders)} folders found in {remote_folder}.")
        for remote_file in tqdm(files):
            local_file = local_folder / remote_file.name
            self.download_file(remote_file, local_file)
        if recursive:
            for remote_sub_folder in folders:
                self.download_folder(remote_sub_folder, local_folder, recursive=recursive)
        return local_folder

    def upload_folder(self, local_source: Path, remote_parent: Path, recursive: bool = True, make_tree: bool = False) -> Path:
        """Upload a folder to the NAS"""
        if not local_source.is_dir():
            raise FileNotFoundError(f"{local_source} does not exist.")
        if not self.is_dir(remote_parent):
            if make_tree:
                self.connection.makedirs(str(remote_parent))
                print(f"Folder tree to {remote_parent} created.")
            else:
                raise FileNotFoundError(f"{remote_parent} does not exist.")

        # create remote folder
        remote_target = remote_parent / local_source.name
        if self.connection.isdir(str(remote_target)):
            raise FileExistsError(f"{remote_target} already exists.")
        self.connection.mkdir(str(remote_target))
        print(f"Remote folder {remote_target} created.")

        # get contents of local folder
        files, folders = self.list_local_files_and_folders(local_source)

        # upload files
        for local_file in files:
            remote_file = remote_target / local_file.name
            self.upload_file(local_file, remote_file)
            print(f"{local_file} -> {remote_file}")

        # upload sub-folders
        if recursive:
            for local_sub_folder in folders:
                self.upload_folder(local_sub_folder, remote_target)
        return remote_target

    def print_tree(self, remote_folder: Path, recursive: bool = True, level: int = 0, max_level: int = 3) -> None:
        """Print file tree."""
        if level < max_level:
            files, folders = self.list_files_and_folders(remote_folder)
            indent = f"\t" * level
            for file in files:
                print(f"{indent} {file.name}")

            for folder in folders:
                print(f"{indent} {folder.name}")
                if recursive:
                    self.print_tree(folder, level=level + 1, max_level=max_level)

    def list_local_files_and_folders(self, local_folder: Path) -> tuple:
        """List local files and folders."""
        elements = local_folder.iterdir()
        files = []
        folders = []
        for element in elements:
            if element.is_file():
                files.append(element)
            elif element.is_dir():
                folders.append(element)
            else:
                raise ValueError(f"{element} is neither file nor folder?")
        return files, folders

    def move_file(self, remote_source: Path, remote_target: Path) -> None:
        """Move a file around."""
        if not self.is_file(remote_source):
            raise FileNotFoundError(f"{remote_source}")
        if self.is_file(remote_target):
            raise FileExistsError(f"{remote_target}")
        if not self.is_dir(remote_target.parent):
            raise FileNotFoundError(f"{remote_target.parent}")
        self.connection.rename(str(remote_source), str(remote_target))

    def move_folder(self, remote_source: Path, remote_target: Path) -> None:
        """Move a folder from one remote location to another."""
        if not self.is_dir(remote_source):
            raise FileNotFoundError(f"{remote_source} does not exist.")
        if self.is_dir(remote_target):
            raise FileExistsError(f"{remote_target} already exists.")
        self.connection.rename(str(remote_source), str(remote_target))

    def create_empty_folder(self, remote_folder: Path) -> None:
        """Create empty folder on NAS."""
        if self.is_dir(remote_folder):
            raise FileExistsError(f"{remote_folder} already exists.")
        self.connection.makedirs(str(remote_folder))
