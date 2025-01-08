def add_country():
	num_countries = int(input("How many coutries you want to add : "))
	for i in range(num_countries):
		while (True):
			country = input("Enter name of country : ")
			if country.isalpha():
				break
			else:
				print("\n Invalid input")
				continue
		countries.append(country)


def update_country():
    old_name = input("Enter a name of country that you want to update : ")
    new_name = input("Enter a name of country that you want to add    : ")
    for i in range(len(countries)):
        if countries[i] == old_name:
            countries[i] == new_name


def remove_country():
    rm_country_name = input("Enter a country name that you want to remove : ")
    countries.remove(rm_country_name)


def add_state():
	for i in range(len(countries)):
		print(f"Enter {countries[i]}'s states")
		num_states = int(input("How many states do you want to add in it : "))
		for i in range(num_states):
			while (True):
				state = input("Enter name of state : ")
				if state.isalpha():
					break
				else:
					print("\n Invalid input")
					continue
			states.append(state)


def update_state():
    old_name = input("Enter a name of state that you want to update : ")
    new_name = input("Enter a name of state that you want to add    : ")
    for i in range(len(states)):
        if states[i] == old_name:
            states[i] == new_name


def remove_state():
    rm_state_name = input("Enter a state name that you want to remove : ")
    states.remove(rm_state_name)


def add_city():
	for i in range(len(states)):
		print(f"Enter {states[i]}'s cities")
		num_cities = int(input("How many city do you want to add in it : "))
		for i in range(num_cities):
			while (True):
				city = input("Enter name of city : ")
				if citty.isalpha():
					break
				else:
					continue
			cities.append(city)


def update_city():
    old_name = input("Enter a name of city that you want to update : ")
    new_name = input("Enter a name of city that you want to add    : ")
    for i in range(len(cities)):
        if cities[i] == old_name:
            cities[i] == new_name


def remove_city():
    rm_city_name = input("Enter a city name that you want to remove : ")
    cities.remove(rm_city_name)


while (True):
	countries = []
	states = []
	cities = []
	print('''
    1. Add
    2. Update
    3. Delete
    4. Exit\n''')
	opt1 = int(input("Select any option what do you want(1 to 4) : "))
	if opt1 == 1:
		while (True):
			print('''
    1. Do you want to add countries
	2. Do you want to add states
	3. Do you want to add cities
	4. Exit\n''')
			opt2 = int(input("Select any option what do you want(1 to 4) : "))
			if opt2 == 1:
				add_country()
				continue
			elif opt2 == 2:
				add_state()
				continue
			elif opt2 == 3:
				add_city()
				continue
			else:
				break
	elif opt1 == 2:
		while (True):
			state_cityDict = {key: value for key in states for value in cities}
			myDict = {key: value for key in countries for value in state_cityDict}
			print(myDict)
			print('''
	1. Do you want to Update countries
	2. Do you want to Update states
	3. Do you want to Update cities
	4. Exit\n''')
			opt3 = int(input("Select any option what do you want(1 to 4) : "))
			if opt3 == 1:
				update_country()
				continue
			elif opt3 == 2:
				update_state()
				continue
			elif opt3 == 3:
				update_state()
				continue
			else:
				break
	elif opt1 == 3:
		while (True):
			state_cityDict = {key: value for key in states for value in cities}
			myDict = {key: value for key in countries for value in state_cityDict}
			print(myDict)
			print('''
	1. Do you want to Delete countries
	2. Do you want to Delete states
	3. Do you want to Delete cities
	4. Exit\n''')
			opt4 = int(input("Select any option what do you want(1 to 4) : "))
			if opt4 == 1:
				remove_country()
				continue
			elif opt4 == 2:
				remove_state()
				continue
			elif opt4 == 3:
				remove_state()
				continue
			else:
				break
	elif opt1 == 4:
		break
	else:
		continue
