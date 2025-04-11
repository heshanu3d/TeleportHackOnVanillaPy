import config as cf
import hack as hk
from log import *
from ui import ui_main

def test(config):
    mgr = hk.HackMgr(config, "D:\\code\\c++\\cmake_test\\build\\main.exe")
    for name, info in mgr.get_hack_infos().items():
        hack = info[0]
        # ret = hack.set_playername(0x4445464748494A5051525354)
        ret = hack.set_playername("新名字")
        logger.info(f'set_playername - {ret} - {hack.playername}')
        logger.info(f'{name} - {info}')

if __name__ == "__main__":
    config = cf.load_config('offset/test.yml')
    test(config)
    # ui_main()
