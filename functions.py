import re
import itertools

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
					#E.g --> 400ml
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
				#E.g ---> 5.5 x 200ml
				if 'x' in unit:
					for v in range(0, len(possible_units)):
						if possible_units[v] in unit:
							temp_units = possible_units[v]
							temp_size = unit.replace(temp_units, "")

					for n in range(0, len(possible_units)):
						if possible_units[n] == temp_units:
							size = temp_size
							units = temp_units

				else:
					#E.g ---> 5.5ml
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
			#If units are separated from the size. E.g: 5.5 ml
			units = unit
			position = name_container.index(units)
			size_container = name_container[position - 1]
			
			if size_container.isnumeric() or full_stop in size_container:
			 	size = size_container
			 	units = unit

	actual_product_name = product_name #" ".join(name_container).replace(container, "").capitalize()

	return units, size, quantity, actual_product_name

def shoprite_splitter(product_name):
	size = ""
	temp_size = ""
	units = ""
	temp_units = ""
	container = ""
	quantity = 1
	full_stop = "."
	name_container = product_name.lower().split(' ')
	possible_units = ["kg","mm","ml","mg","cm","tb","kw","inch","inches","m","g","l","w"]

	for unit in name_container:
		if not unit.isnumeric() and not unit.isalpha():
			if unit.isalnum(): #E.g ---> 400ml / 400mlx12 / 12 x 400ml / 400mlx400ml 
				container = unit
				temp_position = name_container.index(container)

				try:
					temp = name_container[temp_position + 1]

					if temp == "x": #E.g ---> 400ml x 12 / 12ml x 400ml
						next_container = name_container[temp_position + 2]

						if next_container.isnumeric(): #E.g 400ml x 12 [next_container = 12]
							for a in range(0, len(possible_units)):
								if possible_units[a] in container:
									temp_size = container.replace(possible_units[a], "")
									temp_units = possible_units[a]

							for b in range(0, len(possible_units)):
								if possible_units[b] == temp_units:
									units = temp_units
									size = temp_size
									quantity = next_container

						else: #E.g ---> 12ml x 400ml
							temp_container = container + temp + next_container
							for c in range(0, len(possible_units)):
								if possible_units[c] in temp_container:
									temp_size = temp_container.replace(possible_units[c], "")
									temp_units = possible_units[c]

							for d in range(0, len(possible_units)):
								if possible_units[d] == temp_units:
									units = temp_units
									size = temp_size

							break
				except IndexError:
					pass

				if 'x' in container:
					temp_position = container.index('x')
					temp_container = container[temp_position + 1:]

					if not temp_container.isnumeric() and not temp_container.isalpha(): #E.g ---> 12x400ml
						if temp_container.isalnum():
							for e in range(0, len(possible_units)):
								if possible_units[e] in temp_container:
									temp_size = temp_container.replace(possible_units[e], "")
									temp_units = possible_units[e]
									temp_quantity = container[0:temp_position]

							for f in range(0, len(possible_units)):
								if possible_units[f] == temp_units:
									units = temp_units
									size = temp_size
									quantity = temp_quantity

					elif temp_container.isnumeric(): #E.g ---> 400mlx12
						temp_con = 'x' + temp_container
						units_container = container.replace(temp_con, "")

						for h in range(0, len(possible_units)):
							if possible_units[h] in units_container:
								temp_size = units_container.replace(possible_units[h], "")
								temp_units = possible_units[h]
								temp_quantity = temp_container

						for i in range(0, len(possible_units)):
							if possible_units[i] == temp_units:
								size = temp_size
								units = temp_units
								quantity = temp_quantity

				else: #E.g ---> 400ml
					for j in range(0, len(possible_units)):
						if possible_units[j] in container:
							temp_units = possible_units[j]
							temp_size = container.replace(temp_units, "")
							break
					
					for k in range(0, len(possible_units)):
						if possible_units[k] == temp_units:
							units = temp_units
							size = temp_size

			elif full_stop in unit: #Contains special characters. E.g ---> 5.5kg / 5.5kg x 20 / 5.5kg
				position = name_container.index(unit)

				try:
					temp = name_container[position + 1]

					if temp == 'x':
						next_container = name_container[position + 2]

						if next_container.isnumeric(): #5.5kg x 20
							for a in range(0, len(possible_units)):
								if possible_units[a] in unit:
									temp_units = possible_units[a]
									temp_size = unit.replace(temp_units, "")
									temp_quantity = next_container

							for z in range(0, len(possible_units)):
								if possible_units[z] == temp_units:
									units = temp_units
									size = temp_size
									quantity = temp_quantity

						else: #5.5kg x 20kg
							temp_container = unit + temp + next_container
							for i in range(0, len(possible_units)):
								if possible_units[i] in temp_container:
									temp_units = possible_units[i]
									temp_size = temp_container.replace(possible_units[i], "")

							for x in range(0, len(possible_units)):
								if possible_units[x] == temp_units:
									size = temp_size
									units = temp_units

							break

				except IndexError:
					pass

				if 'x' in unit:
					position = unit.index('x')
					cont1 = unit[0:position]
					cont2 = unit[position + 1:]

					if cont2.isnumeric(): #5.5kgx20
						for e in range(0, len(possible_units)):
							if possible_units[e] in cont1:
								temp_units = possible_units[e]
								temp_size = cont1.replace(temp_units, "")
								temp_quantity = cont2

						for t in range(0, len(possible_units)):
							if possible_units[t] == temp_units:
								size = temp_size
								units = temp_units
								quantity = temp_quantity

					else: #5.5kgx20kg
						temp_container = cont1 + 'x' + cont2
						for v in range(0, len(possible_units)):
							if possible_units[v] in temp_container:
								temp_units = possible_units[v]
								temp_units = temp_container.replace(temp_units, "")

						for j in range(0, len(possible_units)):
							if possible_units[j] == temp_units:
								size = temp_size
								units = temp_units

				else: #5.5kg
					for l in range(0, len(unit)):
						if ord(unit[l]) >= 65 and ord(unit[l]) <= 90:
							temp_units += unit[l]
						elif ord(unit[l]) >= 97 and ord(unit[l]) <= 122:
							temp_units += unit[l]
						else:
							temp_size += unit[l]

					for m in range(0, len(possible_units)):
						if possible_units[m] == temp_units:
							units = temp_units
							size = temp_size

		elif unit in possible_units:
			#If units are separated from the size. E.g: 5.5 ml
			units = unit
			position = name_container.index(units)
			size_container = name_container[position - 1]
			
			if size_container.isnumeric() or full_stop in size_container:
			 	size = size_container
			 	units = unit

		elif unit.isnumeric():
			temp_position = name_container.index(unit)

			try:
				temp = name_container[temp_position + 1]

				if temp == 'x':
					next_container = name_container[temp_position + 2]

					if not next_container.isalpha() and not next_container.isnumeric():
						if next_container.isalnum():
							for n in range(0, len(next_container)):
								if ord(next_container[n]) >= 65 and ord(next_container[n]) <= 90:
									temp_units += next_container[n]
								elif ord(next_container[n]) >= 97 and ord(next_container[n]) <= 122:
									temp_units += next_container[n]
								else:
									temp_size += next_container[n]

							for p in range(0, len(possible_units)):
								if possible_units[p] == temp_units:
									size = temp_size
									units = temp_units
									quantity = unit
							break
				else:
					for q in range(0, len(possible_units)):
						if possible_units[q] == temp:
							units = temp
							size = unit 

			except IndexError:
				pass

		elif unit == "pack":
			position = name_container.index(unit)
			temp_quantity = name_container[position - 1]

			if temp_quantity.isnumeric():
				size = ""
				units = unit
				quantity = temp_quantity

	actual_product_name = product_name

	return units, size, quantity, actual_product_name

def makro_splitter(product_name):
	size =""
	units = ""
	quantity = ""
	hyphen = "-"
	full_stop = "."
	possible_units = ["kg","mm","ml","mg","cm","tb","kw","inch","inches","m","g","l","w"]

	bracket_container = product_name.lower().find("(") #Get the position of the opening bracket.
	product_name = product_name.lower()
	container = product_name[bracket_container:]
	x_position = container.find("x")
	quantity = container[1:x_position - 1]

	units_container = container[x_position + 2:].replace(")", "").replace("(", "")
	
	if not units_container.isalpha() and not units_container.isnumeric():
		if units_container.isalnum():
			for x in range(0, len(units_container)):
				if ord(units_container[x]) >= 65 and ord(units_container[x]) <= 90:
					units += units_container[x]
				elif ord(units_container[x]) >= 97 and ord(units_container[x]) <= 122:
					units += units_container[x]
				else:
					size += units_container[x]

		elif hyphen in units_container or full_stop in units_container:
			for x in range(0, len(units_container)):
				if ord(units_container[x]) >= 65 and ord(units_container[x]) <= 90:
					units += units_container[x]
				elif ord(units_container[x]) >= 97 and ord(units_container[x]) <= 122:
					units += units_container[x]
				else:
					size += units_container[x]

		else:
			if units_container.isalnum():
				for x in range(0, len(units_container)):
					if ord(units_container[x]) >= 65 and ord(units_container[x]) <= 90:
						units += units_container[x]
					elif ord(units_container[x]) >= 97 and ord(units_container[x]) <= 122:
						units += units_container[x]
					else:
						size += units_container[x]

	if units == 'lt':
		units = 'l'
	return units, quantity, size
