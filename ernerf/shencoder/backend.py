import os
from torch.utils.cpp_extension import load

_src_path = os.path.dirname(os.path.abspath(__file__))

nvcc_flags = [
    "-O3",
    "-U__CUDA_NO_HALF_OPERATORS__",
    "-U__CUDA_NO_HALF_CONVERSIONS__",
    "-U__CUDA_NO_HALF2_OPERATORS__",
]

if os.name == "posix":
    c_flags = ["-O3", "-std=c++14", "-finput-charset=utf-8"]
elif os.name == "nt":
    c_flags = ["/O2", "/std:c++17", "/source-charset:utf-8"]

    # find cl.exe
    def find_cl_path():
        import glob

        # Directories to search
        search_paths = [r"C:\Program Files", r"C:\Program Files (x86)"]

        # Editions to check
        editions = ["Enterprise", "Professional", "BuildTools", "Community"]

        for base_path in search_paths:
            for edition in editions:
                # Construct the search pattern for the current edition
                pattern = os.path.join(
                    base_path,
                    "Microsoft Visual Studio",
                    "*",
                    edition,
                    "VC",
                    "Tools",
                    "MSVC",
                    "*",
                    "bin",
                    "Hostx64",
                    "x64",
                )
                # Perform the search
                paths = sorted(glob.glob(pattern), reverse=True)
                if paths:
                    return paths[0]

        # If no path is found, return None or raise an error
        return None

    # If cl.exe is not on path, try to find it.
    if os.system("where cl.exe >nul 2>nul") != 0:
        cl_path = find_cl_path()
        if cl_path is None:
            raise RuntimeError(
                "Could not locate a supported Microsoft Visual C++ installation"
            )
        os.environ["PATH"] += ";" + cl_path

_backend = load(
    name="_sh_encoder",
    extra_cflags=c_flags,
    extra_cuda_cflags=nvcc_flags,
    sources=[
        os.path.join(_src_path, "src", f)
        for f in [
            "shencoder.cu",
            "bindings.cpp",
        ]
    ],
)

__all__ = ["_backend"]
