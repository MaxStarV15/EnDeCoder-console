import art
import os

from get_file import get_file
from endecode import EnDeFile, FileProcess
from progress_bar import get_volume
from config_data import PARTS_OF_GIGA, COUNT_THREADS


def welcome() -> None:
	art.tprint("[ EnDeCoder ]")

	print("- by MaxStarV15\n\n")
	print(">>> Это программа для шифрования файлов по ключу <<<\n")
	print('! Файл должен находиться в той же папке, что и программа !\n')


def config() -> None:
	print("[ CONFIG ]")
	print("\tПамяти в оперативке: ~", get_volume(1_073_741_824//PARTS_OF_GIGA))
	print("\tВ одном потоке: ~", get_volume(1_073_741_824//PARTS_OF_GIGA//COUNT_THREADS))

	print()


def en_or_de() -> bool:
	while True:
		inp = input("> шифровать(e) или расшифровывать(d) ? (e/d): ")
		if inp == 'e':
			return True
		elif inp == 'd':
			return False
		else:
			print("ERR: Неизвестная команда")


def get_result_filepath(en: bool, path: str) -> str:
	p = path.split('/')[-1]

	pattern_en = "{}_encoded.{}"
	pattern_de = "{}_decoded.{}"

	p = p.split(".")

	name = p[0]
	exp = p[1]

	if en:
		return pattern_en.format(name, exp)
	else:
		return pattern_de.format(name, exp)


def get_key(en: bool) -> str:

	print("\nКоманды:", *EnDeFile.commands_list)

	if en:
		while True:
			print("\n(оставьте поле пустым, чтобы сгенерировать случайный ключ)")
			key = input("Введите ключ: ")

			if not key:
				key = EnDeFile.generate_random_key()
				return key
			else:
				if EnDeFile.check_key(key):
					return key
				else:
					print("> Ключ не правильный !!!")
					continue
	else:
		while True:
			key = input("Введите ключ: ")

			if EnDeFile.check_key(key):
				return key
			else:
				print("> Ключ не правильный !!!")
				continue


def show_input(en, filepath, result_filepath, key) -> None:
	en = "кодирование" if en else "расшифровка"

	# pattern = "\n\t{:15<}\nТип шифрования{:5>};\nФайл:\t{};\nРезультативный файл:\t{};\nКлюч:\t{};\n"
	
	pattern = (
		f"",
		f"                 [Данные]",
		f"     Тип операции    : {en}",
		f"         Файл        : {filepath}",
		f" Результативный файл : {result_filepath}",
		f"         Ключ        : {key}\n",
	)

	for line in pattern:
		print(line)


def yes_or_no() -> bool:
	while True:
		inp = input("Подтверждаете данные? (y/n): ")
		if inp == "y":
			return True
		elif inp == "n":
			return False


def main():
	""" Основаная программа """
	welcome()
	config()

	en = en_or_de()
	filepath = get_file()
	result_filepath = get_result_filepath(en, filepath)
	key = get_key(en)

	show_input(en, filepath, result_filepath, key)

	if os.path.exists(result_filepath):
		print(f"ERR>\tРезультативный файл уже есть в этой папке ({result_filepath}), переместите или удалите его")
		return
	
	if not yes_or_no():
		print("\n>\tКодирование отменено")
		return

	fp = FileProcess(filepath, result_filepath, key, PARTS_OF_GIGA, COUNT_THREADS, en)

	fp.run()


if __name__ == "__main__":
	main()
	
	input()