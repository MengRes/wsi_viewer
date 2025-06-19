# PyInstaller hook for OpenSlide
from PyInstaller.utils.hooks import collect_dynamic_libs, collect_data_files
import os
import glob

binaries = collect_dynamic_libs('openslide')
datas = collect_data_files('openslide')

# Manually add dynamic libraries from openslide_bin to avoid symlink issues
try:
    import openslide_bin
    openslide_bin_path = os.path.dirname(openslide_bin.__file__)
    if os.path.exists(openslide_bin_path):
        # Collect all dynamic library files
        for ext in ['*.dylib', '*.so', '*.dll']:
            for lib_file in glob.glob(os.path.join(openslide_bin_path, ext)):
                lib_name = os.path.basename(lib_file)
                # Ensure using absolute path to avoid symlink
                binaries.append((os.path.abspath(lib_file), lib_name))
except ImportError:
    pass 