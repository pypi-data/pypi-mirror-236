__title__ = 'luminalog'
__author__ = 'Zappy'
__version__ = '1.0.0.0'

CURRENT_VERSION = '1.0.0.0'

from .consolelog import core

lumina = core()

if __version__ < CURRENT_VERSION:
    lumina.consolelog('Version Out-of-Date! Please upgrade by using: \"python.exe -m pip install -U luminalog\"', type="input"); exit()