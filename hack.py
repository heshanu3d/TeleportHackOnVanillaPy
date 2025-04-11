import ctypes
from ctypes import *
from ctypes import wintypes
from enum_window import *
from log import *

OpenProcess         = windll.kernel32.OpenProcess
CloseHandle         = windll.kernel32.CloseHandle
ReadProcessMemory   = windll.kernel32.ReadProcessMemory
WriteProcessMemory  = windll.kernel32.WriteProcessMemory

class HandleHack:
    def __init__(self, handle):
        self.handle = handle
        self.write_byte   = self._wrap_write(ctypes.c_byte)
        self.write_int    = self._wrap_write(ctypes.c_int)
        self.write_uint32 = self._wrap_write(ctypes.c_uint32)
        self.write_uint64 = self._wrap_write(ctypes.c_uint64)
        self.write_float  = self._wrap_write(ctypes.c_float)
        self.write_double = self._wrap_write(ctypes.c_double)

        self.read_byte    = self._wrap_read(ctypes.c_byte)
        self.read_int     = self._wrap_read(ctypes.c_int)
        self.read_uint32  = self._wrap_read(ctypes.c_uint32)
        self.read_uint64  = self._wrap_read(ctypes.c_uint64)
        self.read_float   = self._wrap_read(ctypes.c_float)
        self.read_double  = self._wrap_read(ctypes.c_double)

        self.is_64bit = ctypes.sizeof(ctypes.c_void_p) == 8

    def get_string(self, address, max_length=18):
        # 创建缓冲区
        buf = (ctypes.c_ubyte * max_length)()
        bytes_read = ctypes.c_size_t(0)
        
        # 读取内存
        if not ReadProcessMemory(self.handle, address, buf, max_length, ctypes.byref(bytes_read)):
            raise ctypes.WinError(ctypes.get_last_error())
        
        # 获取实际读取的字节数据
        data = bytes(buf[:bytes_read.value])

        # 查找第一个'\0'字符的位置
        null_pos = data.find(b'\0')
        if null_pos != -1:
            data = data[:null_pos]
        
        try:
            # 尝试UTF-8解码（常见编码）
            playername = data.decode('utf-8')
            logger.info("read playername " + playername)
            return playername
        except UnicodeDecodeError:
            try:
                # 尝试GBK解码（常见的中文编码）
                playername = data.decode('gbk')
                logger.info("read playername " + playername)
                return playername
            except UnicodeDecodeError:
                # 如果都失败，返回原始字节的十六进制表示
                playername_hex = data.hex()
                logger.info("read playername failed :" + playername_hex)
                return playername_hex

    def set_string(self, address, text, encoding='utf-8', max_length=18):
        try:
            encoded_text = text.encode(encoding)
        except UnicodeEncodeError:
            # 如果默认编码失败，尝试GBK
            try:
                encoded_text = text.encode('gbk')
            except UnicodeEncodeError as e:
                raise ValueError(f"无法编码字符串: {e}")

        # 检查长度是否超限
        if len(encoded_text) > max_length:
            raise ValueError(f"编码后的字符串过长 {len(encoded_text)}（最大允许 {max_length} 字节）")

        # 添加NULL终止符（'\0'）
        encoded_text_with_null = encoded_text + b'\0'

        # 写入内存
        bytes_written = ctypes.c_size_t(0)
        success = WriteProcessMemory(self.handle,address,encoded_text_with_null,len(encoded_text_with_null),ctypes.byref(bytes_written))

        if not success:
            logger.error(f'address {address}')
            raise ctypes.WinError(ctypes.get_last_error())
        return True

    def write_data(self, address, data):
        bytes_written = ctypes.c_size_t(0)
        success = WriteProcessMemory(self.handle, ctypes.c_void_p(address), ctypes.byref(data), ctypes.sizeof(data), ctypes.byref(bytes_written))
        if not success:
            raise ctypes.WinError(ctypes.get_last_error())
        return True

    def _wrap_write(self, ctype):
        def wrapper(address, value):
            data = ctype(value)
            return self.write_data(address, data)
        return wrapper

    def read_data(self, address, buf):
        bytes_read = ctypes.c_size_t(0)
        success = ReadProcessMemory(self.handle, ctypes.c_void_p(address), buf, 1, ctypes.byref(bytes_read))
        if not success:
            raise ctypes.WinError(ctypes.get_last_error())
        return buf[0]

    def _wrap_read(self, ctype):
        def wrapper(address):
            buf = (ctype * 1)()
            return self.read_data(self.handle, address, buf)
        return wrapper

    def read_pointer(self, address):
        if self.is_64bit:
            return self._wrap_read(ctypes.c_uint64)(address)
        else:
            return self._wrap_read(ctypes.c_uint32)(address)

class Hack():
    def __init__(self, config, handle, pid, hwnd):
        self.config = config
        self.handle = handle
        self.pid    = pid
        self.hwnd   = hwnd
        self.handle_hack = HandleHack(handle)
        self.playername = self.get_playername()
    def get_playername(self):
        return self.handle_hack.get_string(self.config.PlayerName)
    def set_playername(self, text):
        if self.handle_hack.set_string(self.config.PlayerName, text):
            self.playername = text
    def get_pos(self):
        hh = self.handle_hack
        config = self.config
        if config.version == "3.3.5":
            PB1        = hh.read_pointer(config.StaticPlayer)
            PB2        = hh.read_pointer(config.PbPointer1 + PB1)
            PlayerBase = hh.read_pointer(config.PbPointer2 + PB2)
            # $MapId = Round(_MemoryRead($MapID, $g_singleWowProcess, "dword"))
            CurrX = round(hh.read_float(PlayerBase + config.PosX), 3)
            CurrY = round(hh.read_float(PlayerBase + config.PosY), 3)
            CurrZ = round(hh.read_float(PlayerBase + config.PosZ), 3)

            return [CurrX, CurrY, CurrZ]
        else:
            CurrX = hh.read_float(config.CurrPosX)
            CurrY = hh.read_float(config.CurrPosY)
            CurrZ = hh.read_float(config.CurrPosZ)

            if config.version == "1.12.1":
                return [CurrY, CurrX, CurrZ]
            else:
                return [CurrX, CurrY, CurrZ]
    def set_pos(self, x, y, z):
        hh = self.handle_hack
        config = self.config
        if config.version == "3.3.5":
            PB1        = hh.read_pointer(config.StaticPlayer)
            PB2        = hh.read_pointer(config.PbPointer1 + PB1)
            PlayerBase = hh.read_pointer(config.PbPointer2 + PB2)
            hh.write_float(PlayerBase + config.PosX, y)
            hh.write_float(PlayerBase + config.PosY, x)
            hh.write_float(PlayerBase + config.PosZ, z)
        else:
            addrX = config.StaticPlayer
            addrY = config.StaticPlayer
            addrZ = config.StaticPlayer

            for i in range(len(config.DstXOffsetArray)):
                addrX = hh.read_pointer(addrX) + config.DstXOffsetArray[i]
                addrY = hh.read_pointer(addrY) + config.DstYOffsetArray[i]
                addrZ = hh.read_pointer(addrZ) + config.DstZOffsetArray[i]

            hh.write_float(addrX, x)
            hh.write_float(addrY, y)
            hh.write_float(addrZ, z)


class HackMgr():
    def __init__(self, config, window_name="魔兽世界"):
        PROCESS_ALL_ACCESS = 0x1F0FFF
        hp = HwndPids(window_name)
        self.hack_infos = dict()
        self.config = config
        for hwnds_pid in hp.get_hwnd_pids():
            hwnd = hwnds_pid[0]
            pid = hwnds_pid[1]
            # print(hwnd, pid)
            handle = OpenProcess(PROCESS_ALL_ACCESS, False, pid)
            hack = Hack(self.config, handle, pid, hwnd)

            playername = hack.playername

            if playername not in self.hack_infos.keys():
                self.hack_infos[playername] = [hack, handle, pid, hwnd]

    def close_handles(self):
        for infos in self.handles.values():
            handle = infos[1]
            CloseHandle(handle)
    def get_hack(self, name):
        if name in self.hack_infos.keys():
            return self.hack_infos[name]
        return None
    def get_hack_infos(self):
        return self.hack_infos

if __name__ == '__main__':
    mgr = HackMgr("魔兽世界")
    # hacks = Hacks("D:\\code\\c++\\cmake_test\\build\\main.exe")
    for name, info in mgr.get_hack_infos().items():
        logger.info(f'{name} - {info}')
