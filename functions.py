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
		elif ord(unit) >= 97 and ord(unit) <= 122:
			units += unit
		elif unit.isnumeric():
			size += unit

	del name_container[-1]
	actual_product_name = " ".join(name_container)

	return units, size, actual_product_name


def attached_first(product_name):
	#If the units and the size are attached and they appear at the beginning.
	name_container = product_name.split(' ')
	units_container = name_container[1]
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

	del name_container[1]
	actual_product_name = " ".join(name_container)

	return units, size, actual_product_name


def unattached_first(product_name):
	#If the size is not attached to the units and they appear at the beginning.
    name_container = product_name.split(' ')
    units = name_container[0]
    size = name_container[1]
    del name_container[1]
    del name_container[1]
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
 