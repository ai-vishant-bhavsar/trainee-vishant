countries = []
states = []
cities = []

def add_country():
    num_countries = int(input("How many coutries you want to add : "))
    for _ in range(num_countries):
        while True:
            country = input("Enter the name of country : ").strip()
            if not country.isalpha():
                print("\nInvalid input, please enter a valid country name.")
                continue
            if country in countries:
                print(f"\n{country} is already added.")
            else:
                countries.append(country)
            break


def update_country():
    old_name = input("Enter a name of country that you want to update : ").strip()
    
    if old_name not in countries:
        print(f"{old_name} does not exist in the country list.")
        return
    new_name = input("Enter a name of country that you want to add    : ").strip()
    if new_name in countries:
        print(f"{new_name} already exists. Update not perform")
    else:
        countries[countries.index(old_name)] = new_name
        print(f"{old_name} updated to {new_name} successfully!")


def remove_country():
    country = input("Enter the name of the country you want to remove: ").strip()
    if country not in countries:
        print(f"{country} dose not exist in the country list")
        return
    countries.remove(country)
    print(f"{country} removed successfully!")


def add_state():
    if not countries:
        print("\nNo countries available. Add countries first.")
        return
    print("Available countries: ", ", ".join(countries))
    country = input("Enter the name of country to add states: ").strip()
    if country not in countries:
        print(f"{country} dose not exist. Please add the country first")
        return
    
    print(f"Enter {countries}'s states")
    num_states = int(input("How many states do you want to add in it : "))
    for _ in range(num_states):
        while True:
            state = input("Enter the name of country : ").strip()
            if not state.isalpha():
                print("\nInvalid input, please enter a valid state name.")
                continue
            if state in states:
                print(f"\n{state} is already added.")
            else:
                countries.append(state)
            break


def update_state():
    old_name = input("Enter a name of state that you want to update : ").strip()
    
    if old_name not in states:
        print(f"{old_name} does not exist in the state list.")
        return
    new_name = input("Enter a name of state that you want to add    : ").strip()
    if new_name in states:
        print(f"{new_name} already exists. Update not perform")
    else:
        states[states.index(old_name)] = new_name
        print(f"{old_name} updated to {new_name} successfully!")


def remove_state():
    state = input("Enter the name of the state you want to remove: ").strip()
    if state not in states:
        print(f"{state} dose not exist in the state list")
        return
    countries.remove(state)
    print(f"{state} removed successfully!")


def add_city():
    if not states:
        print("\nNo state available. Add countries first.")
        return
    print("Available states: ", ", ".join(countries))
    state = input("Enter the name of state to add cities: ").strip()
    if state not in countries:
        print(f"{state} dose not exist. Please add the country first")
        return

    print(f"Enter {state}'s states")
    num_states = int(input("How many states do you want to add in it : "))
    for _ in range(num_states):
        while (True):
            city = input("Enter name of city : ").strip()
            if not city.isalpha():
                print("\n Invalid input, please enter a valid city name...")
                continue
            if city in cities:
                print(f"\n{city} is already added.")
            else:
                states.append(city)
                print(f"{city} added successfully!")
            break


def update_city():
    old_name = input("Enter a name of city that you want to update : ").strip()
    
    if old_name not in cities:
        print(f"{old_name} does not exist in the city list.")
        return
    new_name = input("Enter a name of city that you want to add    : ").strip()
    if new_name in states:
        print(f"{new_name} already exists. Update not perform")
    else:
        cities[cities.index(old_name)] = new_name
        print(f"{old_name} updated to {new_name} successfully!")


def remove_city():
    city = input("Enter the name of the city you want to remove: ").strip()
    if city not in cities:
        print(f"{city} dose not exist in the city list")
        return
    countries.remove(city)
    print(f"{city} removed successfully!")


def print_all_date():
    data = {
		country : {
			state : [city for city in cities if city.startswith(state[0])]
   			for state in states if state.startswith(country[0])
		}
		for country in countries
	}
    print("\nCurrent Data: ")
    print(data)


while (True):
	print('''
    1. Add
    2. Update
    3. Delete
    4. Print all Data
    5. Exit\n''')
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
		print_all_date()
	elif opt1 == 5:
		print("Exiting the program...")
		break
	else:
		continue
