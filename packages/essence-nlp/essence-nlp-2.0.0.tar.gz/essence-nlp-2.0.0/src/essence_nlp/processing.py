import ctypes
import platform
import subprocess
import os

def setup_rust():
    subprocess.run(["cargo", "build", "--release"], cwd=os.path.join(os.path.dirname(__file__), 'essence'))

def get_shared_library():
    # Determine the correct shared library extension for the current platform
    ext = {'Darwin': '.dylib', 'Linux': '.so', 'Windows': '.dll'}[platform.system()]
    
    # Construct the path to the shared library
    lib_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'essence/target/release', f'libessence{ext}'))
    
    if not os.path.exists(lib_path):
        setup_rust()
        lib_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'essence/target/release', f'libessence{ext}'))
    


    lib = ctypes.CDLL(lib_path)

    lib.get_keywords.restype = ctypes.c_void_p
    lib.get_keywords.argtypes = [ctypes.c_char_p]
    lib.free_string.argtypes = [ctypes.c_void_p]

    lib.get_corrected.restype = ctypes.c_void_p
    lib.get_corrected.argtypes = [ctypes.c_char_p]

    lib.get_cleaned.restype = ctypes.c_void_p
    lib.get_cleaned.argtypes = [ctypes.c_char_p]
    return lib

def keywords(s: str) -> str:
    # Convert Python string to bytes, and then to C string
    lib = get_shared_library()
    c_string = ctypes.c_char_p(s.encode('utf-8'))
    # Call the Rust function
    result_ptr = lib.get_keywords(c_string)
    result = ctypes.cast(result_ptr, ctypes.c_char_p).value.decode('utf-8')
    lib.free_string(result_ptr)
    return result

def corrected(s: str) -> str:
    # Convert Python string to bytes, and then to C string
    lib = get_shared_library()
    c_string = ctypes.c_char_p(s.encode('utf-8'))
    # Call the Rust function
    result_ptr = lib.get_corrected(c_string)
    result = ctypes.cast(result_ptr, ctypes.c_char_p).value.decode('utf-8')
    lib.free_string(result_ptr)
    return result

def cleaned(s: str) -> str:
    # Convert Python string to bytes, and then to C string
    lib = get_shared_library()
    c_string = ctypes.c_char_p(s.encode('utf-8'))
    # Call the Rust function
    result_ptr = lib.get_cleaned(c_string)
    result = ctypes.cast(result_ptr, ctypes.c_char_p).value.decode('utf-8')
    lib.free_string(result_ptr)
    return result

