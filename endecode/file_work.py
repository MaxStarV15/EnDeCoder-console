from random import choice
import re

from .file_moves import Moves
from config_data import RANDOM_KEY_LENGTH_MIN, RANDOM_KEY_LENGTH_MAX


class EnDeFile:
	""" 
	Шифрует файлы по ключу-коду
	"""
	commands_list = [
		"ia", "ra", "mp", "rp", "d", "ser", "sel", "spr", "spl", "sbr", "sbl"
	]
	commands = {
		"ia":  Moves.invert_all, 
		"ra":  Moves.reverse_all,  
		"mp":  Moves.mirror_pairs,  
		"rp":  Moves.reverse_pairs, 
		"d":   Moves.difference, 
		"ser": Moves.shift_eleven_right, 
		"sel": Moves.shift_eleven_left, 
		"spr": Moves.shift_pairs_right, 
		"spl": Moves.shift_pairs_left,
		"sbr": Moves.shift_bit_right,
		"sbl": Moves.shift_bit_left
	}
	commands_reverse = {
		"ia":  Moves.invert_all, 
		"ra":  Moves.reverse_all,  
		"mp":  Moves.mirror_pairs,  
		"rp":  Moves.reverse_pairs, 
		"d":   Moves.difference, 
		"ser": Moves.shift_eleven_left, 
		"sel": Moves.shift_eleven_right, 
		"spr": Moves.shift_pairs_left, 
		"spl": Moves.shift_pairs_right,
		"sbr": Moves.shift_bit_left,
		"sbl": Moves.shift_bit_right
	}

	random_key_lenght_min = RANDOM_KEY_LENGTH_MIN
	random_key_lenght_max = RANDOM_KEY_LENGTH_MAX


	@classmethod
	def generate_random_key(cls) -> str:
		""" Генерирует случайный ключ """
		return ''.join(choice(cls.commands_list) for i in range(cls.random_key_lenght_min, cls.random_key_lenght_max))


	@classmethod
	def key_to_commands(cls, key: str):
		""" Из ключа получить команды """
		# pattern = r'ia|ra|spr|spl|mp|rp|d|ser|sel|sbr|sbl'
		pattern = '|'.join(cls.commands_list)
		return re.findall(pattern, key)


	@classmethod
	def encode_bytes(cls, key: str, byte: bytes) -> bytes:
		""" Зашифровать байты по ключу """
		for command in cls.key_to_commands(key):
			byte = cls.commands[command](byte)
		return byte
	

	@classmethod
	def decode_bytes(cls, key: str, byte: bytes) -> bytes:
		""" Расшифровать байты по ключу """
		for command in cls.key_to_commands(key)[::-1]:
			byte = cls.commands_reverse[command](byte)
		return byte
	

	@classmethod
	def check_key(cls, key: str) -> bool:
		""" Проверить правильность ключа """
		exp = re.compile('^({})+$'.format(
			'|'.join(cls.commands_list)
		))

		return bool(exp.fullmatch(key))