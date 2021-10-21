/*
* CRC Calculation Library (DLL)
* Author: Yogyui (SeungHee-Lee)
*/
#ifndef _CRC_H_
#define _CRC_H_

#ifdef CRCPROJ_EXPORTS
#define CRC_API __declspec(dllexport)
#else
#define CRC_API __declspec(dllimport)
#endif

#include <vector>

#define LUT_SIZE 256

extern "C"
{
	/*
	* CRC-8
	*/
	class CRC_API CRC8
	{
	public:
		CRC8(uint8_t polynomial, uint8_t init_value, bool reflect_input, bool reflect_output, uint8_t xor_output, bool use_lut);
		CRC8(bool use_lut = false) : CRC8(0x07, 0x00, false, false, 0x00, use_lut) {};

	public:
		uint8_t calculate(const char* string);
		uint8_t calculate(const uint8_t* data_in, const int length);
		uint8_t calculate(std::vector<uint8_t> data);
		void printLookupTable();

	private:
		uint8_t polynomial;
		uint8_t init_value;
		bool reflect_input;
		bool reflect_output;
		uint8_t xor_output;

		uint8_t reflect(uint8_t value);

		bool use_lut;
		uint8_t lookup_table[LUT_SIZE];
		void create_lookup_table();
	};

	class CRC_API CRC8_CDMA2000 : public CRC8
	{
	public:
		CRC8_CDMA2000(bool use_lut = false) : CRC8(0x9B, 0xFF, false, false, 0x00, use_lut) {};
	};

	class CRC_API CRC8_DARC : public CRC8
	{
	public:
		CRC8_DARC(bool use_lut = false) : CRC8(0x39, 0x00, true, true, 0x00, use_lut) {};
	};

	class CRC_API CRC8_DVB_S2 : public CRC8
	{
	public:
		CRC8_DVB_S2(bool use_lut = false) : CRC8(0xD5, 0x00, false, false, 0x00, use_lut) {};
	};

	class CRC_API CRC8_EBU : public CRC8
	{
	public:
		CRC8_EBU(bool use_lut = false) : CRC8(0x1D, 0xFF, true, true, 0x00, use_lut) {};
	};

	class CRC_API CRC8_I_CODE : public CRC8
	{
	public:
		CRC8_I_CODE(bool use_lut = false) : CRC8(0x1D, 0xFD, false, false, 0x00, use_lut) {};
	};

	class CRC_API CRC8_ITU : public CRC8
	{
	public:
		CRC8_ITU(bool use_lut = false) : CRC8(0x07, 0x00, false, false, 0x55, use_lut) {};
	};

	class CRC_API CRC8_MAXIM : public CRC8
	{
	public:
		CRC8_MAXIM(bool use_lut = false) : CRC8(0x31, 0x00, true, true, 0x00, use_lut) {};
	};

	class CRC_API CRC8_ROHC : public CRC8
	{
	public:
		CRC8_ROHC(bool use_lut = false) : CRC8(0x07, 0xFF, true, true, 0x00, use_lut) {};
	};

	class CRC_API CRC8_WCDMA : public CRC8
	{
	public:
		CRC8_WCDMA(bool use_lut = false) : CRC8(0x9B, 0x00, true, true, 0x00, use_lut) {};
	};

	/*
	* CRC-16
	*/
	class CRC_API CRC16
	{
	public:
		CRC16(uint16_t polynomial, uint16_t init_value, bool reflect_input, bool reflect_output, uint16_t xor_output, bool use_lut);
		CRC16(bool use_lut = false) : CRC16(0x1021, 0x0000, false, false, 0x0000, use_lut) {};

	public:
		uint16_t calculate(const char* string);
		uint16_t calculate(const uint8_t* data_in, const int length);
		uint16_t calculate(std::vector<uint8_t> data);
		void printLookupTable();

	private:
		uint16_t polynomial;
		uint16_t init_value;
		bool reflect_input;
		bool reflect_output;
		uint16_t xor_output;

		uint16_t reflect(uint16_t value);

		bool use_lut;
		uint16_t lookup_table[LUT_SIZE];
		void create_lookup_table();
	};

	class CRC_API CRC16_ARC : public CRC16
	{
	public:
		CRC16_ARC(bool use_lut = false) : CRC16(0x8005, 0x0000, true, true, 0x0000, use_lut) {};
	};

	class CRC_API CRC16_CCITT_FALSE : public CRC16
	{
	public:
		CRC16_CCITT_FALSE(bool use_lut = false) : CRC16(0x1021, 0xFFFF, false, false, 0x0000, use_lut) {};
	};

	class CRC_API CRC16_AUG_CCITT : public CRC16
	{
	public:
		CRC16_AUG_CCITT(bool use_lut = false) : CRC16(0x1021, 0x1D0F, false, false, 0x0000, use_lut) {};
	};

	class CRC_API CRC16_BUYPASS : public CRC16
	{
	public:
		CRC16_BUYPASS(bool use_lut = false) : CRC16(0x8005, 0x0000, false, false, 0x0000, use_lut) {};
	};

	class CRC_API CRC16_CMDA2000 : public CRC16
	{
	public:
		CRC16_CMDA2000(bool use_lut = false) : CRC16(0xC867, 0xFFFF, false, false, 0x0000, use_lut) {};
	};

	class CRC_API CRC16_DDS_110 : public CRC16
	{
	public:
		CRC16_DDS_110(bool use_lut = false) : CRC16(0x8005, 0x800D, false, false, 0x0000, use_lut) {};
	};

	class CRC_API CRC16_DECT_R : public CRC16
	{
	public:
		CRC16_DECT_R(bool use_lut = false) : CRC16(0x0589, 0x0000, false, false, 0x0001, use_lut) {};
	};

	class CRC_API CRC16_DECT_X : public CRC16
	{
	public:
		CRC16_DECT_X(bool use_lut = false) : CRC16(0x0589, 0x0000, false, false, 0x0000, use_lut) {};
	};

	class CRC_API CRC16_DNP : public CRC16
	{
	public:
		CRC16_DNP(bool use_lut = false) : CRC16(0x3D65, 0x0000, true, true, 0xFFFF, use_lut) {};
	};

	class CRC_API CRC16_EN_13757 : public CRC16
	{
	public:
		CRC16_EN_13757(bool use_lut = false) : CRC16(0x3D65, 0x0000, false, false, 0xFFFF, use_lut) {};
	};

	class CRC_API CRC16_GENIBUS : public CRC16
	{
	public:
		CRC16_GENIBUS(bool use_lut = false) : CRC16(0x1021, 0xFFFF, false, false, 0xFFFF, use_lut) {};
	};

	class CRC_API CRC16_MAXIM : public CRC16
	{
	public:
		CRC16_MAXIM(bool use_lut = false) : CRC16(0x8005, 0x0000, true, true, 0xFFFF, use_lut) {};
	};

	class CRC_API CRC16_MCRF4XX : public CRC16
	{
	public:
		CRC16_MCRF4XX(bool use_lut = false) : CRC16(0x1021, 0xFFFF, true, true, 0x0000, use_lut) {};
	};

	class CRC_API CRC16_RIELLO : public CRC16
	{
	public:
		CRC16_RIELLO(bool use_lut = false) : CRC16(0x1021, 0xB2AA, true, true, 0x0000, use_lut) {};
	};

	class CRC_API CRC16_T10_DIF : public CRC16
	{
	public:
		CRC16_T10_DIF(bool use_lut = false) : CRC16(0x8BB7, 0x0000, false, false, 0x0000, use_lut) {};
	};

	class CRC_API CRC16_TELEDISK : public CRC16
	{
	public:
		CRC16_TELEDISK(bool use_lut = false) : CRC16(0xA097, 0x0000, false, false, 0x0000, use_lut) {};
	};

	class CRC_API CRC16_TMS37157 : public CRC16
	{
	public:
		CRC16_TMS37157(bool use_lut = false) : CRC16(0x1021, 0x89EC, true, true, 0x0000, use_lut) {};
	};

	class CRC_API CRC16_USB : public CRC16
	{
	public:
		CRC16_USB(bool use_lut = false) : CRC16(0x8005, 0xFFFF, true, true, 0xFFFF, use_lut) {};
	};

	class CRC_API CRC_A : public CRC16
	{
	public:
		CRC_A(bool use_lut = false) : CRC16(0x1021, 0xC6C6, true, true, 0x0000, use_lut) {};
	};

	class CRC_API CRC16_KERMIT : public CRC16
	{
	public:
		CRC16_KERMIT(bool use_lut = false) : CRC16(0x1021, 0x0000, true, true, 0x0000, use_lut) {};
	};

	class CRC_API CRC16_MODBUS : public CRC16
	{
	public:
		CRC16_MODBUS(bool use_lut = false) : CRC16(0x8005, 0xFFFF, true, true, 0x0000, use_lut) {};
	};

	class CRC_API CRC16_X_25 : public CRC16
	{
	public:
		CRC16_X_25(bool use_lut = false) : CRC16(0x1021, 0xFFFF, true, true, 0xFFFF, use_lut) {};
	};

	class CRC_API CRC16_XMODEM : public CRC16
	{
	public:
		CRC16_XMODEM(bool use_lut = false) : CRC16(0x1021, 0x0000, false, false, 0x0000, use_lut) {};
	};

	/*
	* CRC-32
	*/
	class CRC_API CRC32
	{
	public:
		CRC32(uint32_t polynomial, uint32_t init_value, bool reflect_input, bool reflect_output, uint32_t xor_output, bool use_lut);
		CRC32(bool use_lut = false) : CRC32(0x04C11DB7, 0xFFFFFFFF, true, true, 0xFFFFFFFF, use_lut) {};

	public:
		uint32_t calculate(const char* string);
		uint32_t calculate(const uint8_t* data_in, const int length);
		uint32_t calculate(std::vector<uint8_t> data);
		void printLookupTable();

	private:
		uint32_t polynomial;
		uint32_t init_value;
		bool reflect_input;
		bool reflect_output;
		uint32_t xor_output;

		uint32_t reflect(uint32_t value);

		bool use_lut;
		uint32_t lookup_table[LUT_SIZE];
		void create_lookup_table();
	};

	class CRC_API CRC32_BZIP2 : public CRC32
	{
	public:
		CRC32_BZIP2(bool use_lut = false) : CRC32(0x04C11DB7, 0xFFFFFFFF, false, false, 0xFFFFFFFF, use_lut) {};
	};

	class CRC_API CRC32_C : public CRC32
	{
	public:
		CRC32_C(bool use_lut = false) : CRC32(0x1EDC6F41, 0xFFFFFFFF, true, true, 0xFFFFFFFF, use_lut) {};
	};

	class CRC_API CRC32_D : public CRC32
	{
	public:
		CRC32_D(bool use_lut = false) : CRC32(0xA833982B, 0xFFFFFFFF, true, true, 0xFFFFFFFF, use_lut) {};
	};

	class CRC_API CRC32_MPEG_2 : public CRC32
	{
	public:
		CRC32_MPEG_2(bool use_lut = false) : CRC32(0x04C11DB7, 0xFFFFFFFF, false, false, 0x00000000, use_lut) {};
	};

	class CRC_API CRC32_POSIX : public CRC32
	{
	public:
		CRC32_POSIX(bool use_lut = false) : CRC32(0x04C11DB7, 0x00000000, false, false, 0xFFFFFFFF, use_lut) {};
	};

	class CRC_API CRC32_Q : public CRC32
	{
	public:
		CRC32_Q(bool use_lut = false) : CRC32(0x814141AB, 0x00000000, false, false, 0x00000000, use_lut) {};
	};

	class CRC_API CRC32_JAMCRC : public CRC32
	{
	public:
		CRC32_JAMCRC(bool use_lut = false) : CRC32(0x04C11DB7, 0xFFFFFFFF, true, true, 0x00000000, use_lut) {};
	};

	class CRC_API CRC32_XFER : public CRC32
	{
	public:
		CRC32_XFER(bool use_lut = false) : CRC32(0x000000AF, 0x00000000, false, false, 0x00000000, use_lut) {};
	};
}
#endif