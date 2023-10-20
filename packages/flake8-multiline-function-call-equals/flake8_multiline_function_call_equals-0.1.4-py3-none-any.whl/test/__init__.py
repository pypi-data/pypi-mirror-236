import enum
import os

from SocialCollector import lib


config_path = os.environ['RANDOM_QBIT_CONFIG_PATH']
lib.PLATFORM_ID = lib.get_platform_ids(config_path)

platform_names = sorted(map(str.lower, lib.PLATFORM_ID.__members__.keys()))
platform_enums = [p.upper() for p in platform_names]
lib.Platforms = enum.Enum('Platforms', dict(zip(platform_enums, platform_names)))
lib.Platforms.__str__ = lambda self: str(self.value)
lib.Platforms.__repr__ = lambda self: str(self.value)

lib.PLATFORM_CODES = lib.get_platform_codes(config_path)
