import os
from progress_bar import get_volume


def get_file() -> str:
	""" Получение пути файла """
	files = os.listdir()
	files = [path_ for path_ in files if os.path.isfile(path_)]
	files.sort()
	files = {str(i+1):(files[i], os.path.getsize(files[i])) for i in range(len(files))}

	while True:
		for key, value in files.items():
			print("\t{}:  {}   {}".format(key, value[0], get_volume(value[1])))
	
		ind = input("Введите номер файла: ")

		if ind.isdigit() and (ind in files):
			return files[ind][0]
		
		print("Такого индекса нет\n")