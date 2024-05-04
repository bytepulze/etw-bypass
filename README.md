# ETW Bypass LtcFlip
- Bypassing Event Tracing for Windows (ETW) in golang.
---

# ETW-Bypass
- A simple Python script that first checks if `NtProtectVirtualMemory` and `NtAllocateVirtualMemory` are hooked or not. Then it loads the `ntdll.dll` with LoadLibrary and gets the address of the function `EtwEventWrite` using GetProcAddress. Finally, it writes the patch bytes into the process.

### (Without) Before Patch:
![image](https://github.com/EvilBytecode/ETW-Bypass-Codepulze/assets/151552809/6aa9dd95-54bd-407b-be3a-02c33e0dbae1)

### (After) Patch:
![image](https://github.com/EvilBytecode/ETW-Bypass-Codepulze/assets/151552809/fe270bcf-9e67-4484-84c6-ae7aa460d401)
---
