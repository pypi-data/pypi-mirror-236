import os
from pathlib import Path

import numpy as np
import tifffile
import zarr
from tqdm import tqdm

from labnas.remote.imaging import ImagingNas
from labnas.local.base import assert_single_stack, sort_tif_files


def download_as_single_tif(remote_folder: Path, local_folder: Path, nas: ImagingNas) -> Path:
    """Download each tif of a stack, save into a singe local tif."""
    temp_local = local_folder / "temp.tif"
    large_local = local_folder / f"{remote_folder.name}.tif"

    tif_files = nas.find_tifs_in_folder(remote_folder)
    n_files = len(tif_files)
    print(f"{len(tif_files)} tif files in {remote_folder}")
    assert n_files > 1, f"Not enough files in {remote_folder}: {n_files} < 1"
    assert_single_stack(tif_files)
    tif_files = sort_tif_files(tif_files)
    for i_file in tqdm(range(n_files)):
        file = tif_files[i_file]
        nas.download_file(file, temp_local, overwrite=True)
        image = tifffile.imread(temp_local)
        if i_file == 0:
            shape = (n_files, image.shape[0], image.shape[1])
            tifffile.imwrite(
                large_local,
                shape=shape,
                dtype=np.uint8,
            )
            store = tifffile.imread(large_local, mode="r+", aszarr=True)
            z = zarr.open(store, mode="r+")
            print(f"Empty tif created: {shape}")
        z[i_file, :, :] = image
    os.remove(local_folder / "temp.tif")
    return large_local
