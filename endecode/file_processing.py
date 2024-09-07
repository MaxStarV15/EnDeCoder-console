from threading import Thread, Semaphore, Lock, RLock
from multiprocessing import Process
import os
import time
from typing import List

from .file_work import EnDeFile
from progress_bar import prog_bar, check_bar, get_volume
from get_file import get_file
from config_data import CLEAR_DELAY, PROGRESS_BAR_WIDTH


class NumLock(Semaphore):
	def __init__(self, count: int):
		super().__init__()
		self.count_threads = count
		self.now_in = 0


	def can_write(self, num: int) -> bool:
		if self.now_in == self.count_threads:
			return False
		elif num == self.now_in:
			self.now_in += 1
			return True
		

	def reset(self):
		self.now_in = 0


class ByteThread(Thread):
	def __init__(self, number: int, filename: str, bytes_: bytes, key: str, lock: NumLock, encode: bool = True):
		super().__init__()

		self.daemon = True

		self.number: int = number
		self.filename: str = filename
		self.bytes: bytes = bytes_
		self.key: str = key
		self.lock: NumLock = lock
		self.encode: bool = encode

		self.done: bool = False
		self.done_endecoding: bool = False


	def run(self):
		
		if self.done:
			return
		
		# En/Decoding
		endecoded_bytes = bytes()
			
		if self.encode:
			endecoded_bytes: bytes = EnDeFile.encode_bytes(self.key, self.bytes)
		else:
			endecoded_bytes: bytes = EnDeFile.decode_bytes(self.key, self.bytes)

		self.done_endecoding = True

		# try to write
		while True:
			with self.lock:
				if self.lock.can_write(self.number):
					with open(self.filename, 'ab') as f:
						f.write(endecoded_bytes)
					break

		self.done = True
	
	def reset(self, new_bytes: bytes):
		self.done = False
		self.bytes = new_bytes


class FileProcess():
	def __init__(self, filepath: str, result_path: str, key: str, parts_of_giga: int, count_threads: int, encode: bool=True):
		# super().__init__()
		self.filepath: str = filepath
		self.result_path: str = result_path
		self.key: str = key
		self.giga_part_size: int = 1_073_741_824//parts_of_giga # Сколько байт отдаётся группе потоков
		self.count_threads: int = count_threads
		self.encode: bool = encode
		self.threads: List[ByteThread] = list()


	def run(self):
		lock = NumLock(self.count_threads)

		size: int = os.path.getsize(self.filepath) # Размер файла
		filepart_size = self.giga_part_size // self.count_threads # Сколько байтов даётся потоку
		
		max_work: int = (size//filepart_size)+1 # Число потоков на размер файла
		now_threads_done: int = 0
		percent: int = 0
	
		running = True

		self.threads = list()


		start = time.time()

		with open(self.filepath, 'rb') as f:
			while running:

				for i in range(self.count_threads):
					bytes_ = f.read(filepart_size)
					if not bytes_:
						running = False
						if i < len(self.threads):
							self.threads[i].done = True
						break
					
					thread = ByteThread(i, self.result_path, bytes_, self.key, lock, self.encode)
					self.threads.append(thread)
					thread.start()


				# Print progressbars
				while True:
					os.system('cls')

					prog_bar("Общий прогресс", percent+now_threads_done, max_work, PROGRESS_BAR_WIDTH)
					print()
					check_bar("(Де)Шифрование", [int(t.done_endecoding) for t in self.threads])
					prog_bar(" Запись в файл", sum([int(t.done) for t in self.threads]), len(self.threads)+1, PROGRESS_BAR_WIDTH)
					

					now_threads_done = sum([th.done for th in self.threads])

					if now_threads_done == self.count_threads or not running:
						break
					time.sleep(CLEAR_DELAY)
				

				percent += now_threads_done

				for th in self.threads:
					if not th.done:
						th.join()

				lock.reset()
				self.threads = list()

		print("\n> \tПрограмма завершилась")
		print(f"\n\tЗанятое время: {time.time() - start:.2f}s")