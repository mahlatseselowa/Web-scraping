import re
import itertools

def attached_last(product_name):
	#If the size and the units are attached and they appear at the end.
	name_container = product_name.split(' ')
	units_container = name_container[-1]
	units = ""
	size = ""

	for unit in units_container:
		#ord(unit)[>=65 & <=90] returns the ascii value of an upper case letter.
		if ord(unit) >= 65 and ord(unit) <= 90:
			units += unit
		elif ord(unit) >= 97 and ord(unit) <= 122: #ord(unit)[>=65 & <=90] returns an ascii value of an lower case.
			units += unit
		elif unit.isnumeric():
			size += unit

	del name_container[-1]
	actual_product_name = " ".join(name_container)

	return units, size, actual_product_name


def attached_first(product_name):
	#If the units and the size are attached and they appear at the beginning.
	name_container = product_name.split(' ')
	units_container = name_container[0]
	size = ""
	units = ""

	for unit in units_container:
		#ord(unit)[>=65 & <=90] returns an ascii value of an upper case.
		if ord(unit) >= 65 and ord(unit) <= 90:
			units += unit
		elif ord(unit) >= 97 and ord(unit) <= 122:
			##ord(unit)[>=97 & <=122] returns an ascii value of a lower() case.
			units += unit
		elif unit.isnumeric():
			size += unit

	del name_container[0]
	actual_product_name = " ".join(name_container)

	return units, size, actual_product_name


def unattached_first(product_name):
	#If the size is not attached to the units and they appear at the beginning.
    name_container = product_name.split(' ')
    units = name_container[1]
    size = name_container[0]
    del name_container[0]
    del name_container[0]
    actual_product_name = " ".join(name_container)

    return units, size, actual_product_name

def unattached_last(product_name):
	"""
    If the size is not attached to the units and they appear at the end.
    """
	name_container = product_name.split(' ')
	units = name_container[-1]
	size = name_container[-2]
	del name_container[-1]
	del name_container[-1]
	actual_product_name = " ".join(name_container)

	return units, size, actual_product_name

def appear_middle(product_name):
	#If the size and the units appear in the anywhere, anyhow.

	container = ""
	units = ""
	size = ""
	sub_string = ""
	comma = ","
	full_stop = ""
	name_container = product_name.lower().split(' ')
	possible_units = ["mg","kg","ml","m","g","mm","pce","Pack","pk","inch","Tb","Pce","l","xl","Pc Set", "Set","Piece","Pair","Pack"]

	for unit in name_container:
		if not unit.isalpha() and not unit.isnumeric():
			if unit.isalnum():
				container += unit

				if 'x' in container or 'X' in container:
					for i in range(0, len(possible_units)):
						sub_string = possible_units[i]
						if sub_string in container:
							size = container.replace(sub_string, "")
							units = sub_string
				else:
					for x in container:
						for w in range(0, len(possible_units)):
							if possible_units[w] in container:
								if ord(x) >= 65 and ord(x) <= 90: #ord(unit)[>=65 & <=90] returns an ascii value of an upper case.
									units += x
								elif ord(x) >= 97 and ord(x) <= 122: #ord(unit)[>=65 & <=90] returns an ascii value of an lower case.
									units += x
								elif x.isnumeric():
									size += x

			elif full_stop in unit or comma in unit:
				for t in range(0, len(unit)):
					if ord(unit[t]) >= 65 and ord(unit[t]) <= 90:
						units += unit[t]
					elif ord(unit[t]) >= 97 and ord(unit[t]) <= 122:
						units += unit[t]
					else:
						size += unit[t]
			else:
				for a in range(0, len(unit)):
					if unit[a].isnumeric():
						size += unit[a]
					elif size == "":
						units = ""
					else:
						units += unit[a]
		elif unit.isnumeric():
			size = unit
		elif unit in possible_units:
			units = unit
			position = name_container[name_container.index(units)]
			size = name_container[name_container.index(position - 1)]

	if units == "":
		size = ""
	actual_product_name = " ".join(name_container).replace(container,"").capitalize()

	return units, size, actual_product_name

def name_splitter(product_name):
	size = ""
	temp_size = ""
	units = ""
	temp_units = ""
	comma = ","
	full_stop = "."
	hyphen = "-"
	plus = "+"
	position = 0
	container_position = 0
	quantity = 1
	name_container = product_name.lower().split(' ')
	possible_units = ["kg","mm","ml","m","cm","mg","l","g","Tb","inch","inches","G","ML","pack","kw","w"]

	for unit in name_container:
		if not unit.isalpha() and not unit.isnumeric():
			if unit.isalnum():
				container = unit
				container_position = name_container.index(container)
				try:
					temp = name_container[container_position + 1] 
					#list_cycle = itertools.cycle(name_container)
					#temp = next(list_cycle)

					if temp == 'x':
						next_container = name_container[container_position + 2]
						temp_container = container + 'x' + next_container

						for r in range(0, len(possible_units)):
							if possible_units[r] in temp_container:
								temp_size = temp_container.replace(possible_units[r], "")
								temp_units = possible_units[r]

						for t in range(0, len(possible_units)):
							if possible_units[t] == temp_units:
								units = temp_units
								size = temp_size
						break
				except IndexError:
					pass
				
				if 'x' in container:
					for i in range(0, len(possible_units)):
						if possible_units[i] in container:
							temp_size = container.replace(possible_units[i], "")
							temp_units = possible_units[i]

					for d in range(0, len(possible_units)):
						if possible_units[d] == temp_units:
							units = temp_units
							size = temp_size
				else:
					for a in range(0, len(container)):
						if ord(container[a]) >= 65 and ord(container[a]) <= 90:
							temp_units += container[a]
						elif ord(container[a]) >= 97 and ord(container[a]) <= 122:
							temp_units += container[a]
						else:
							temp_size += container[a]

					for b in range(0, len(possible_units)):
						if possible_units[b] == temp_units:
							units = temp_units
							size = temp_size

			elif comma in unit or full_stop in unit or hyphen in unit or plus in unit:
				for e in range(0, len(unit)):
					if ord(unit[e]) >= 65 and ord(unit[e]) <= 90:
						temp_units += unit[e]
					elif ord(unit[e]) >= 97 and ord(unit[e]) <= 122:
						temp_units += unit[e]
					else:
						temp_size += unit[e]

				for c in range(0, len(possible_units)):
					if possible_units[c] == temp_units:
						units = temp_units.replace(plus,"")
						size = temp_size 

		elif unit in possible_units:
			units = unit
			position = name_container.index(units)
			size_container = name_container[position - 1]
			
			if size_container.isnumeric() or full_stop in size_container:
			 	size = size_container
			 	units = unit

	actual_product_name = product_name #" ".join(name_container).replace(container, "").capitalize()

	return units, size, quantity, actual_product_name