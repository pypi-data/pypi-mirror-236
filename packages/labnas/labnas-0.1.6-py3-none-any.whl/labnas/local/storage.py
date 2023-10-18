from pathlib import Path

import numpy as np
import tifffile
import zarr
from tqdm import tqdm

from labnas.local.base import list_tif_files, sort_tif_files


def convert_to_tif(source_folder: Path, target_file: Path) -> None:
    """Convert a folder with multiple tifs into a single tif file."""
    if not source_folder.is_dir():
        raise FileNotFoundError(f"{source_folder} is not a directory.")
    if target_file.is_dir():
        raise FileExistsError(f"{target_file} already exists.")
    tif_files = list_tif_files(source_folder)
    tif_files = sort_tif_files(tif_files)
    n_files = tif_files.size
    for i_file in tqdm(range(n_files)):
        image = tifffile.imread(tif_files[i_file])
        if i_file == 0:
            shape = (n_files, image.shape[0], image.shape[1])
            tifffile.imwrite(
                target_file,
                shape=shape,
                dtype=np.uint8,
            )
            store = tifffile.imread(target_file, mode="r+", aszarr=True)
            z = zarr.open(store, mode="r+")
            print(f"Empty tif created: {shape}")
        z[i_file, :, :] = image
    store.close()