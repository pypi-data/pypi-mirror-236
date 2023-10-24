from cffi import FFI
from sys import platform
import pathlib
import atexit

_lib = None
_ffi = None

def _initSaldo():

    global _ffi

    _ffi = FFI()
    _ffi.cdef("void saldoInit();")
    _ffi.cdef("void saldoExit();")
    _ffi.cdef("void c_paradigm(char*, char*, uint64_t*, char***, uint64_t**, char***);")
    _ffi.cdef("void c_free_int_arr(uint64_t*);")
    _ffi.cdef("void c_free_arr(char**, uint64_t);")
    libdir = pathlib.Path(__file__).parent.resolve().joinpath("lib")

    global _lib

    if platform == "darwin":
        _lib = _ffi.dlopen(str(libdir.joinpath("libsaldo.dylib")))
    elif platform == "linux":
        _lib = _ffi.dlopen(str(libdir.joinpath("libsaldo.so")))
    else:
        raise ValueError("Unsupported OS")
    
    _lib.saldoInit() # type: ignore

@atexit.register
def _exitSaldo():
    assert _lib is not None
    _lib.saldoExit() # type: ignore

def paradigm(paradigm_name: str, word: str) -> dict[str, list[str]] | None:

    # Assert that saldo loaded correctly

    assert _ffi is not None
    assert _lib is not None

    # Allocate caller-allocated structures

    form_names_qty = _ffi.new("uint64_t*") # Gets GC'd

    # Allocate handles to callee-allocated structures

    form_names = _ffi.new("char***")
    form_names[0] = _ffi.NULL

    forms_qty = _ffi.new("uint64_t**")
    forms_qty[0] = _ffi.NULL

    inflected_forms = _ffi.new("char***")
    inflected_forms[0] = _ffi.NULL

    # Call

    _lib.c_paradigm(paradigm_name.encode("utf-8"), word.encode("utf-8"), form_names_qty, form_names, forms_qty, inflected_forms) # type: ignore

    if form_names[0] == _ffi.NULL:

        # GC takes care of deallocating our pointers
        # Callee never allocated anything

        return None

    else:

        # Extract result

        result = []
        form_value_idx = 0

        for i in range(form_names_qty[0]):
            name = _ffi.string(form_names[0][i]).decode("utf-8") # type: ignore
            values = []
            for _ in range(forms_qty[0][i]):
                values.append(_ffi.string(inflected_forms[0][form_value_idx]).decode("utf-8")) # type: ignore
                form_value_idx += 1
            result.append((name, values))
        
        # Deallocate callee-allocated structures

        _lib.c_free_int_arr(forms_qty[0]) # type: ignore
        _lib.c_free_arr(inflected_forms[0], form_value_idx) # type: ignore
        _lib.c_free_arr(form_names[0], form_names_qty[0]) # type: ignore

        # form_names_qty gets GC'd

        return dict(result)

_initSaldo()