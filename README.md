# C/C++ CRC Library
CRC(Cyclic Redundancy Check) 8/16/32 Calculation Library for C/C++.<br>
 

How to use?
---
Already built library files (CRC.dll, CRC.lib) for x32, x64 are ready for use.<br>
[x32_Debug](./CRC/Debug ), 
[x32_Release](https://github.com/YOGYUI/CRC/Release )<br>
[x64_Debug](https://github.com/YOGYUI/CRC/x64/Debug ), 
[x64_Release](https://github.com/YOGYUI/CRC/x64/Release )<br>
Just link lib file in your project and put dll file in output directory.
<br>
Also, you can refer to [example code](https://github.com/YOGYUI/CRC/Validation/Validation.cpp ) which I made.<br><br>
You can use Look-up Table option to reduce calculation time or instant calculation option to reduce memory usage.<br>
Option can be configured with constructor argument(use_lut).
```cpp
#include "CRC.h"

int main()
{
    CRC16_ARC obj = CRC16_ARC(true);    // use look up table
//  CRC16_ARC obj = CRC16_ARC(false);   // instant calculation
    
    uint16_t result;
    result = obj.calculate("hello,world!");  // argument - string
    
    char string[] = "hello,world!";
    uint8_t* ptr = new uint8_t[strlen(string)];
	memcpy(ptr, string, strlen(string));
	result = obj.calculate(ptr, strlen(string)); // argument - pointer of array
    
    std::vector<uint8_t> array{ 'h','e','l','l','o' };
    result = obj.calculate(array);  // argument - vector
}
```
You can make your own customized algorithm with constructor arguments.<br>
```cpp
CRC8(uint8_t polynomial, uint8_t init_value, bool reflect_input, bool reflect_output, uint8_t xor_output, bool use_lut);
CRC16(uint16_t polynomial, uint16_t init_value, bool reflect_input, bool reflect_output, uint16_t xor_output, bool use_lut);
CRC32(uint32_t polynomial, uint32_t init_value, bool reflect_input, bool reflect_output, uint32_t xor_output, bool use_lut);
```
Example
```cpp
obj = CRC32(0x04C11DB7, 0xFFFFFFFF, true, true, 0x00000000, false);
```

Implemented Algorithms
---
CRC8
```
CRC-8/CDMA2000
CRC-8/DARC
CRC-8/DVB-S2
CRC-8/EBU
CRC-8/I-CODE
CRC-8/ITU
CRC-8/MAXIM
CRC-8/ROHC
CRC-8/WCMDA
```
CRC16
```
CRC-16/CCITT-FALSE
CRC-16/ARC
CRC-16/AUG-CCITT
CRC-16/BUYPASS
CRC-16/CDMA2000
CRC-16/DDS-110
CRC-16/DECT-R
CRC-16/DECT-X
CRC-16/DNP
CRC-16/EN-13757
CRC-16/GENIBUS
CRC-16/MAXIM
CRC-16/MCRF4XX
CRC-16/RIELLO
CRC-16/T10-DIF
CRC-16/TELEDISK
CRC-16/TMS37157
CRC-16/USB
CRC-A
CRC16/KERMIT
CRC16/MODBUS
CRC16/X-25
CRC16/XMODEM
```
CRC32
```
CRC-32/BZIP2
CRC-32C
CRC-32D
CRC-32/MPEG-2
CRC-32/POSIX
CRC-32Q
CRC-32/JAMCRC
CRC-32/XFER
```
