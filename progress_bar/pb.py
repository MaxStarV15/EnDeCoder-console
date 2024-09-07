

def prog_bar(name: str, value: int, max_value: int, k: int=100):
	pattern = "{name}: \t[{full}{empty}] \t{percent}%"

	percent = value * 100 // max_value

	showed_percent = percent // (100//k)
	# ▌█
	print(pattern.format(
		name=name, 
		full="█"*showed_percent, 
		empty="."*(k-showed_percent), 
		percent=percent)
	)
	return percent