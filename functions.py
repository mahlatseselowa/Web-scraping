import re

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
	name_container = product_name.lower().split(' ')
	possible_units = ["mg","kg","ml","m","g","G","pce","Pack","mm","l","Pk","pk","inch","Tb","Pce","l","xl","Pc Set", "Set","Piece","Pair","Pack"]

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
		elif unit.isnumeric():
			size = unit
		elif unit in possible_units:
			units = unit

	actual_product_name = " ".join(name_container).replace(container,"")

	return units, size, actual_product_name

def set_product(product_name):
	container = ""
	name_container = product_name.split(' ')

	for unit in name_container:
		if not unit.isalpha() or not unit.isnumeric():
			if unit.isalnum():
				container = unit
		else:
			container = ""

	actual_product_name = " ".join(name_container, "").replace(container, "")

	return container, actual_product_name