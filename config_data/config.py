import configparser
import os

if not os.path.exists("config.ini"):
    print("ERR> Отсутствует файл конфигурации 'config.ini'")
    input()
    exit(1)
config = configparser.ConfigParser()
config.read("config.ini")


PARTS_OF_GIGA = int(config["Parts"]["parts_of_giga"])
COUNT_THREADS = int(config["Parts"]["count_threads"])

PROGRESS_BAR_WIDTH = int(config["Progress_bar"]["width"])
CLEAR_DELAY = float(config["Progress_bar"]["clear_delay_seconds"])

RANDOM_KEY_LENGTH_MIN = int(config["EnDecode"]["random_key_length_min"])  
RANDOM_KEY_LENGTH_MAX = int(config["EnDecode"]["random_key_length_max"])