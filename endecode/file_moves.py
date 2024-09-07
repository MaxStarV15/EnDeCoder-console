
class Moves:
	# "ia", "ra", "sp", "rp", "d", "ser", "sel", "spr", "spl", "sbr", "sbl"
	
	@classmethod
	def invert_all(cls, byte: bytes):
		""" Инвертровать все биты """
		# будет шифровать байты, а не 1 байт, чтобы мог потом просто надумать по сколько шифровать
		result = list()
		for b in byte: # b - int
			b = bin(b)[2:].zfill(8) # to bin
			b = ''.join('0' if symbol == '1' else '1' for symbol in b) # inverting
			b = int(f"0b{b}", 2) # back to int
			result.append(b)
		return bytes(result)
	

	@classmethod
	def reverse_all(cls, byte: bytes):
		""" развернуть всё задом на перёд """
		# (Aa Bb Cc Dd -> dD cC bB aA)
		result = list()
		for b in byte: # b - int
			b = bin(b)[2:].zfill(8) # to bin
			b = ''.join(b[::-1]) # reversing
			b = int(f"0b{b}", 2) # back to int
			result.append(b)
		return bytes(result)


	@classmethod
	def mirror_pairs(cls, byte: bytes):
		""" Переставить пары задом на перёд """
		# (Aa Bb Cc Dd -> Dd Cc Bb Aa)
		result = list()
		for b in byte: # b - int
			b = bin(b)[2:].zfill(8) # to bin
			b = [b[i:i+2] for i in range(0, len(b), 2)]
			b = ''.join(b[::-1]) # reversing
			b = int(f"0b{b}", 2) # back to int
			result.append(b)
		return bytes(result)


	@classmethod
	def reverse_pairs(cls, byte: bytes):
		""" Каждую пару разввернуть относительно себя """
		# (Aa Bb Cc Dd -> aA bB cC dD)
		result = list()
		for b in byte: # b - int
			b = bin(b)[2:].zfill(8) # to bin
			b = [b[i:i+2][::-1] for i in range(0, len(b), 2)]
			b = ''.join(b) # reversing
			b = int(f"0b{b}", 2) # back to int
			result.append(b)
		return bytes(result)


	@classmethod
	def difference(cls, byte: bytes):
		""" Байты вычетаются из FF(255) """
		return bytes( 255 - b for b in byte )
	

	@classmethod
	def shift_eleven_right(cls, byte: bytes):
		"""
		'Сдвиг одиннадцати вправо'
		представляется символы 0110 и рамка на 2 символа
		пары байта подставляются в рамку и сдвигаются вправо
		"""
		table = {
			"00":"01", 
			"01":"11", 
			"10":"00", 
			"11":"10"}
		result = list()

		for b in byte: # b - int
			b = bin(b)[2:].zfill(8) # to bin
			b = ''.join(table[b[i:i+2]] for i in range(0, len(b), 2))
			b = int(f"0b{b}", 2) # back to int
			result.append(b)

		return bytes(result)
	

	@classmethod
	def shift_eleven_left(cls, byte: bytes):
		"""
		'Сдвиг одиннадцати влево'
		представляется символы 0110 и рамка на 2 символа
		пары байта подставляются в рамку и сдвигаются влево
		"""
		table = {
			"00":"10", 
			"01":"00", 
			"10":"11", 
			"11":"01"}
		result = list()

		for b in byte: # b - int
			b = bin(b)[2:].zfill(8) # to bin
			b = ''.join(table[b[i:i+2]] for i in range(0, len(b), 2))
			b = int(f"0b{b}", 2) # back to int
			result.append(b)

		return bytes(result)
	
	
	@classmethod
	def shift_pairs_right(cls, byte: bytes):
		""" Сдвиг вправо парами (Aa Bb Cc Dd -> Dd Aa Bb Cc) """
		result = list()
		for b in byte: # b - int
			b = bin(b)[2:].zfill(8) # to bin
			b = [b[i:i+2] for i in range(0, len(b), 2)] # to list

			end_el = b[-1]
			b = b[:-1]
			b.insert(0, end_el)
			b = ''.join(b)

			b = int(f"0b{b}", 2) # back to int
			result.append(b)
		return bytes(result)
	

	@classmethod
	def shift_pairs_left(cls, byte: bytes):
		""" Сдвиг влево парами  (Aa Bb Cc Dd -> Bb Cc Dd Aa) """
		result = list()
		for b in byte: # b - int
			b = bin(b)[2:].zfill(8) # to bin
			b = [b[i:i+2] for i in range(0, len(b), 2)] # to list

			first_el = b[0]
			b = b[1:]
			b.append(first_el)
			b = ''.join(b)

			b = int(f"0b{b}", 2) # back to int
			result.append(b)
		return bytes(result)


	@classmethod
	def shift_bit_right(cls, byte: bytes):
		""" Сдвиг вправо на бит (Aa Bb Cc Dd -> dA aB bC cD) """
		result = list()
		for b in byte: # b - int
			b = bin(b)[2:].zfill(8) # to bin

			end_el = b[-1]
			b = b[:-1]
			b = end_el + b

			b = int(f"0b{b}", 2) # back to int
			result.append(b)
		return bytes(result)


	@classmethod
	def shift_bit_left(cls, byte: bytes):
		""" Сдвиг влево на бит  (Aa Bb Cc Dd -> aB bC cD dA) """
		result = list()
		for b in byte: # b - int
			b = bin(b)[2:].zfill(8) # to bin
			
			first_el = b[0]
			b = b[1:]
			b = b + first_el

			b = int(f"0b{b}", 2) # back to int
			result.append(b)
		return bytes(result)

