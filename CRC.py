"""
CRC Calculation
Author: Yogyui (SeungHee-Lee)
"""
from typing import Union, List

REFLECT_BIT_ORDER_TABLE = [
    0x00, 0x80, 0x40, 0xC0, 0x20, 0xA0, 0x60, 0xE0,
    0x10, 0x90, 0x50, 0xD0, 0x30, 0xB0, 0x70, 0xF0,
    0x08, 0x88, 0x48, 0xC8, 0x28, 0xA8, 0x68, 0xE8,
    0x18, 0x98, 0x58, 0xD8, 0x38, 0xB8, 0x78, 0xF8,
    0x04, 0x84, 0x44, 0xC4, 0x24, 0xA4, 0x64, 0xE4,
    0x14, 0x94, 0x54, 0xD4, 0x34, 0xB4, 0x74, 0xF4,
    0x0C, 0x8C, 0x4C, 0xCC, 0x2C, 0xAC, 0x6C, 0xEC,
    0x1C, 0x9C, 0x5C, 0xDC, 0x3C, 0xBC, 0x7C, 0xFC,
    0x02, 0x82, 0x42, 0xC2, 0x22, 0xA2, 0x62, 0xE2,
    0x12, 0x92, 0x52, 0xD2, 0x32, 0xB2, 0x72, 0xF2,
    0x0A, 0x8A, 0x4A, 0xCA, 0x2A, 0xAA, 0x6A, 0xEA,
    0x1A, 0x9A, 0x5A, 0xDA, 0x3A, 0xBA, 0x7A, 0xFA,
    0x06, 0x86, 0x46, 0xC6, 0x26, 0xA6, 0x66, 0xE6,
    0x16, 0x96, 0x56, 0xD6, 0x36, 0xB6, 0x76, 0xF6,
    0x0E, 0x8E, 0x4E, 0xCE, 0x2E, 0xAE, 0x6E, 0xEE,
    0x1E, 0x9E, 0x5E, 0xDE, 0x3E, 0xBE, 0x7E, 0xFE,
    0x01, 0x81, 0x41, 0xC1, 0x21, 0xA1, 0x61, 0xE1,
    0x11, 0x91, 0x51, 0xD1, 0x31, 0xB1, 0x71, 0xF1,
    0x09, 0x89, 0x49, 0xC9, 0x29, 0xA9, 0x69, 0xE9,
    0x19, 0x99, 0x59, 0xD9, 0x39, 0xB9, 0x79, 0xF9,
    0x05, 0x85, 0x45, 0xC5, 0x25, 0xA5, 0x65, 0xE5,
    0x15, 0x95, 0x55, 0xD5, 0x35, 0xB5, 0x75, 0xF5,
    0x0D, 0x8D, 0x4D, 0xCD, 0x2D, 0xAD, 0x6D, 0xED,
    0x1D, 0x9D, 0x5D, 0xDD, 0x3D, 0xBD, 0x7D, 0xFD,
    0x03, 0x83, 0x43, 0xC3, 0x23, 0xA3, 0x63, 0xE3,
    0x13, 0x93, 0x53, 0xD3, 0x33, 0xB3, 0x73, 0xF3,
    0x0B, 0x8B, 0x4B, 0xCB, 0x2B, 0xAB, 0x6B, 0xEB,
    0x1B, 0x9B, 0x5B, 0xDB, 0x3B, 0xBB, 0x7B, 0xFB,
    0x07, 0x87, 0x47, 0xC7, 0x27, 0xA7, 0x67, 0xE7,
    0x17, 0x97, 0x57, 0xD7, 0x37, 0xB7, 0x77, 0xF7,
    0x0F, 0x8F, 0x4F, 0xCF, 0x2F, 0xAF, 0x6F, 0xEF,
    0x1F, 0x9F, 0x5F, 0xDF, 0x3F, 0xBF, 0x7F, 0xFF
]
LUT_SIZE = 256


class CRCBase:
    _name: str = 'CRC-Base'
    _bit_count: int = 8

    def __init__(
            self,
            polynomial: int,
            init_value: int,
            reflect_input: bool,
            reflect_output: bool,
            xor_output: int,
            use_lut: bool = False
    ):
        self._max_value = int.from_bytes(bytearray([0xFF] * (self._bit_count // 8)), 'big')
        self.polynomial: int = polynomial & self._max_value
        self.init_value: int = init_value & self._max_value
        self.reflect_input: bool = reflect_input
        self.reflect_output: bool = reflect_output
        self.xor_output: int = xor_output & self._max_value
        self.use_lut: bool = use_lut
        self.lookup_table: List[int] = [0] * LUT_SIZE
        if self.use_lut:
            self.create_lookup_table()

    def create_lookup_table(self):
        t = 1 << (self._bit_count - 1)
        for i in range(LUT_SIZE):
            x = (i << (self._bit_count - 8)) & self._max_value
            for j in range(8):
                x = (x << 1) ^ self.polynomial if (x & t) else (x << 1)
            self.lookup_table[i] = x & self._max_value

    def reflect(self, value: int) -> int:
        reflected = 0
        for i in range(self._bit_count):
            if value & 0x1:
                reflected |= (1 << ((self._bit_count - 1) - i))
            value = (value >> 1)
        return reflected

    def calculate(self, data: Union[bytes, bytearray, str]):
        crc = self.init_value
        if self.use_lut:
            for i in range(len(data)):
                index = ord(data[i]) if isinstance(data[i], str) else data[i]
                temp = REFLECT_BIT_ORDER_TABLE[index] if self.reflect_input else index
                crc = ((crc << 8) ^ self.lookup_table[(crc >> (self._bit_count - 8)) ^ temp]) & self._max_value
        else:
            t = 1 << (self._bit_count - 1)
            for i in range(len(data)):
                index = ord(data[i]) if isinstance(data, str) else data[i]
                temp = REFLECT_BIT_ORDER_TABLE[index] if self.reflect_input else index
                crc ^= (temp << (self._bit_count - 8))
                for j in range(8):
                    crc = (crc << 1) ^ self.polynomial if (crc & t) else (crc << 1)
        if self.reflect_output:
            crc = self.reflect(crc)
        crc = (crc ^ self.xor_output) & self._max_value
        return crc


class CRC8Base(CRCBase):
    _name: str = 'CRC-8-Base'
    _bit_count: int = 8

    def __repr__(self):
        txt = '<{} : Poly(0x{:02X}), Init(0x{:02X}), Ref_In({}), Ref_Out({}), XorOut(0x{:02X}), LUT({})>'.format(
            self._name, self.polynomial, self.init_value,
            self.reflect_input, self.reflect_output, self.xor_output, self.use_lut)
        return txt


class CRC8(CRC8Base):
    def __init__(self, use_lut: bool = False):
        super().__init__(0x07, 0x00, False, False, 0x00, use_lut)
        self._name = 'CRC-8'


class CRC8_CDMA2000(CRC8Base):
    def __init__(self, use_lut: bool = False):
        super().__init__(0x9B, 0xFF, False, False, 0x00, use_lut)
        self._name = 'CRC-8/CDMA2000'


class CRC8_DARC(CRC8Base):
    def __init__(self, use_lut: bool = False):
        super().__init__(0x39, 0x00, True, True, 0x00, use_lut)
        self._name = 'CRC-8/DARC'


class CRC8_DVB_S2(CRC8Base):
    def __init__(self, use_lut: bool = False):
        super().__init__(0xD5, 0x00, False, False, 0x00, use_lut)
        self._name = 'CRC-8/DVB-S2'


class CRC8_EBU(CRC8Base):
    def __init__(self, use_lut: bool = False):
        super().__init__(0x1D, 0xFF, True, True, 0x00, use_lut)
        self._name = 'CRC-8/EBU'


class CRC8_ICODE(CRC8Base):
    def __init__(self, use_lut: bool = False):
        super().__init__(0x1D, 0xFD, False, False, 0x00, use_lut)
        self._name = 'CRC-8/I-CODE'


class CRC8_ITU(CRC8Base):
    def __init__(self, use_lut: bool = False):
        super().__init__(0x07, 0x00, False, False, 0x55, use_lut)
        self._name = 'CRC-8/ITU'


class CRC8_MAXIM(CRC8Base):
    def __init__(self, use_lut: bool = False):
        super().__init__(0x31, 0x00, True, True, 0x00, use_lut)
        self._name = 'CRC-8/MAXIM'


class CRC8_ROHC(CRC8Base):
    def __init__(self, use_lut: bool = False):
        super().__init__(0x07, 0xFF, True, True, 0x00, use_lut)
        self._name = 'CRC-8/ROHC'


class CRC8_WCDMA(CRC8Base):
    def __init__(self, use_lut: bool = False):
        super().__init__(0x9B, 0x00, True, True, 0x00, use_lut)
        self._name = 'CRC-8/WCDMA'


class CRC16Base(CRCBase):
    _name: str = 'CRC-16-Base'
    _bit_count: int = 16

    def __repr__(self):
        txt = '<{} : Poly(0x{:04X}), Init(0x{:04X}), Ref_In({}), Ref_Out({}), XorOut(0x{:04X}), LUT({})>'.format(
            self._name, self.polynomial, self.init_value,
            self.reflect_input, self.reflect_output, self.xor_output, self.use_lut)
        return txt


class CRC16_CCITT_FALSE(CRC16Base):
    def __init__(self, use_lut: bool = False):
        super().__init__(0x1021, 0xFFFF, False, False, 0x0000, use_lut)
        self._name = 'CRC-16/CCITT-FALSE'


class CRC16_ARC(CRC16Base):
    def __init__(self, use_lut: bool = False):
        super().__init__(0x8005, 0x0000, True, True, 0x0000, use_lut)
        self._name = 'CRC-16/ARC'


class CRC16_AUG_CCITT(CRC16Base):
    def __init__(self, use_lut: bool = False):
        super().__init__(0x1021, 0x1D0F, False, False, 0x0000, use_lut)
        self._name = 'CRC-16/AUG-CCITT'


class CRC16_BUYPASS(CRC16Base):
    def __init__(self, use_lut: bool = False):
        super().__init__(0x8005, 0x0000, False, False, 0x0000, use_lut)
        self._name = 'CRC-16/BUYPASS'


class CRC16_CDMA2000(CRC16Base):
    def __init__(self, use_lut: bool = False):
        super().__init__(0xC867, 0xFFFF, False, False, 0x0000, use_lut)
        self._name = 'CRC-16/CDMA2000'


class CRC16_DDS_110(CRC16Base):
    def __init__(self, use_lut: bool = False):
        super().__init__(0x8005, 0x800D, False, False, 0x0000, use_lut)
        self._name = 'CRC-16/DDS-110'


class CRC16_DECT_R(CRC16Base):
    def __init__(self, use_lut: bool = False):
        super().__init__(0x0589, 0x0000, False, False, 0x0001, use_lut)
        self._name = 'CRC-16/DECT-R'


class CRC16_DECT_X(CRC16Base):
    def __init__(self, use_lut: bool = False):
        super().__init__(0x0589, 0x0000, False, False, 0x0000, use_lut)
        self._name = 'CRC-16/DECT-X'


class CRC16_DNP(CRC16Base):
    def __init__(self, use_lut: bool = False):
        super().__init__(0x3D65, 0x0000, True, True, 0xFFFF, use_lut)
        self._name = 'CRC-16/DNP'


class CRC16_EN_13757(CRC16Base):
    def __init__(self, use_lut: bool = False):
        super().__init__(0x3D65, 0x0000, False, False, 0xFFFF, use_lut)
        self._name = 'CRC-16/EN-13757'


class CRC16_GENIBUS(CRC16Base):
    def __init__(self, use_lut: bool = False):
        super().__init__(0x1021, 0xFFFF, False, False, 0xFFFF, use_lut)
        self._name = 'CRC-16/GENIBUS'


class CRC16_MAXIM(CRC16Base):
    def __init__(self, use_lut: bool = False):
        super().__init__(0x8005, 0x0000, True, True, 0xFFFF, use_lut)
        self._name = 'CRC-16/MAXIM'


class CRC16_MCRF4XX(CRC16Base):
    def __init__(self, use_lut: bool = False):
        super().__init__(0x1021, 0xFFFF, True, True, 0x0000, use_lut)
        self._name = 'CRC-16/MCRF4XX'


class CRC16_RIELLO(CRC16Base):
    def __init__(self, use_lut: bool = False):
        super().__init__(0x1021, 0xB2AA, True, True, 0x0000, use_lut)
        self._name = 'CRC-16/RIELLO'


class CRC16_T10_DIF(CRC16Base):
    def __init__(self, use_lut: bool = False):
        super().__init__(0x8BB7, 0x0000, False, False, 0x0000, use_lut)
        self._name = 'CRC-16/T10-DIF'


class CRC16_TELEDISK(CRC16Base):
    def __init__(self, use_lut: bool = False):
        super().__init__(0xA097, 0x0000, False, False, 0x0000, use_lut)
        self._name = 'CRC-16/TELEDISK'


class CRC16_TMS37157(CRC16Base):
    def __init__(self, use_lut: bool = False):
        super().__init__(0x1021, 0x89EC, True, True, 0x0000, use_lut)
        self._name = 'CRC-16/TMS37157'


class CRC16_USB(CRC16Base):
    def __init__(self, use_lut: bool = False):
        super().__init__(0x8005, 0xFFFF, True, True, 0xFFFF, use_lut)
        self._name = 'CRC-16/USB'


class CRC_A(CRC16Base):
    def __init__(self, use_lut: bool = False):
        super().__init__(0x1021, 0xC6C6, True, True, 0x0000, use_lut)
        self._name = 'CRC-A'


class CRC16_KERMIT(CRC16Base):
    def __init__(self, use_lut: bool = False):
        super().__init__(0x1021, 0x0000, True, True, 0x0000, use_lut)
        self._name = 'CRC-16/KERMIT'


class CRC16_MODBUS(CRC16Base):
    def __init__(self, use_lut: bool = False):
        super().__init__(0x8005, 0xFFFF, True, True, 0x0000, use_lut)
        self._name = 'CRC-16/MODBUS'


class CRC16_X_25(CRC16Base):
    def __init__(self, use_lut: bool = False):
        super().__init__(0x1021, 0xFFFF, True, True, 0xFFFF, use_lut)
        self._name = 'CRC-16/X-25'


class CRC16_XMODEM(CRC16Base):
    def __init__(self, use_lut: bool = False):
        super().__init__(0x1021, 0x0000, False, False, 0x0000, use_lut)
        self._name = 'CRC-16/XMODEM'


class CRC32Base(CRCBase):
    _name: str = 'CRC-32-Base'
    _bit_count: int = 32

    def __repr__(self):
        txt = '<{} : Poly(0x{:08X}), Init(0x{:08X}), Ref_In({}), Ref_Out({}), XorOut(0x{:08X}), LUT({})>'.format(
            self._name, self.polynomial, self.init_value,
            self.reflect_input, self.reflect_output, self.xor_output, self.use_lut)
        return txt


class CRC32(CRC32Base):
    def __init__(self, use_lut: bool = False):
        super().__init__(0x04C11DB7, 0xFFFFFFFF, True, True, 0xFFFFFFFF, use_lut)
        self._name = 'CRC-32'


class CRC32_BZIP2(CRC32Base):
    def __init__(self, use_lut: bool = False):
        super().__init__(0x04C11DB7, 0xFFFFFFFF, False, False, 0xFFFFFFFF, use_lut)
        self._name = 'CRC-32/BZIP2'


class CRC32_C(CRC32Base):
    def __init__(self, use_lut: bool = False):
        super().__init__(0x1EDC6F41, 0xFFFFFFFF, True, True, 0xFFFFFFFF, use_lut)
        self._name = 'CRC-32C'


class CRC32_D(CRC32Base):
    def __init__(self, use_lut: bool = False):
        super().__init__(0xA833982B, 0xFFFFFFFF, True, True, 0xFFFFFFFF, use_lut)
        self._name = 'CRC-32D'


class CRC32_JAMCRC(CRC32Base):
    def __init__(self, use_lut: bool = False):
        super().__init__(0x04C11DB7, 0xFFFFFFFF, True, True, 0x00000000, use_lut)
        self._name = 'CRC-32/JAMCRC'


class CRC32_MPEG_2(CRC32Base):
    def __init__(self, use_lut: bool = False):
        super().__init__(0x04C11DB7, 0xFFFFFFFF, False, False, 0x00000000, use_lut)
        self._name = 'CRC-32/MPEG-2'


class CRC32_POSIX(CRC32Base):
    def __init__(self, use_lut: bool = False):
        super().__init__(0x04C11DB7, 0x00000000, False, False, 0xFFFFFFFF, use_lut)
        self._name = 'CRC-32/POSIX'


class CRC32_Q(CRC32Base):
    def __init__(self, use_lut: bool = False):
        super().__init__(0x814141AB, 0x00000000, False, False, 0x00000000, use_lut)
        self._name = 'CRC-32Q'


class CRC32_XFER(CRC32Base):
    def __init__(self, use_lut: bool = False):
        super().__init__(0x000000AF, 0x00000000, False, False, 0x00000000, use_lut)
        self._name = 'CRC-32/XFER'
