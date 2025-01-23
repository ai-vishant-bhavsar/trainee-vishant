countries = []
states = []
cities = []

def add_country():
    num_countries = int(input("How many countries do you want to add? "))
    for _ in range(num_countries):
        while True:
            country = input("Enter the name of the country: ").strip()
            if not country.isalpha():
                print("\nInvalid input, please enter a valid country name.")
                continue
            if country in countries:
                print(f"\n{country} is already added.")
            else:
                countries.append(country)
                print(f"{country} added successfully!")
            break

def update_country():
    old_name = input("Enter the country name to update: ").strip()
    if old_name not in countries:
        print(f"{old_name} does not exist in the country list.")
        return
    new_name = input("Enter the new country name: ").strip()
    if new_name in countries:
        print(f"{new_name} already exists. Update not performed.")
    else:
        countries[countries.index(old_name)] = new_name
        print(f"{old_name} updated to {new_name} successfully!")

def remove_country():
    country = input("Enter the name of the country to remove: ").strip()
    if country not in countries:
        print(f"{country} does not exist in the country list.")
        return
    countries.remove(country)
    states[:] = [state for state in states if state[0] != country]
    cities[:] = [city for city in cities if city[0] != country]
    print(f"{country} removed successfully!")

def add_state():
    if not countries:
        print("\nNo countries available. Add countries first.")
        return
    print("Available countries: ", ", ".join(countries))
    country = input("Enter the name of country to add states: ").strip()
    if country not in countries:
        print(f"{country} does not exist. Please add the country first.")
        return

    num_states = int(input(f"How many states do you want to add to {country}: "))
    for _ in range(num_states):
        while True:
            state = input(f"Enter the name of a state for {country}: ").strip()
            if not state.isalpha():
                print("\nInvalid input, please enter a valid state name.")
                continue
            if any(state_info[0] == country and state_info[1] == state for state_info in states):
                print(f"\n{state} is already added to {country}.")
            else:
                states.append([country, state])
                print(f"{state} added successfully!")
            break

def update_state():
    country = input("Enter the country name to update state: ").strip()
    if country not in countries or not any(state_info[0] == country for state_info in states):
        print(f"No states found for {country}.")
        return
    old_name = input(f"Enter the state name to update in {country}: ").strip()
    if not any(state_info[0] == country and state_info[1] == old_name for state_info in states):
        print(f"{old_name} does not exist in {country}.")
        return
    new_name = input("Enter the new state name: ").strip()
    if any(state_info[0] == country and state_info[1] == new_name for state_info in states):
        print(f"{new_name} already exists. Update not performed.")
    else:
        for state_info in states:
            if state_info[0] == country and state_info[1] == old_name:
                state_info[1] = new_name
                print(f"{old_name} updated to {new_name} successfully!")
                break

def remove_state():
    country = input("Enter the country name to remove state: ").strip()
    if country not in countries or not any(state_info[0] == country for state_info in states):
        print(f"No states found for {country}.")
        return
    state = input(f"Enter the state name to remove from {country}: ").strip()
    if not any(state_info[0] == country and state_info[1] == state for state_info in states):
        print(f"{state} does not exist in {country}.")
        return
    states[:] = [state_info for state_info in states if state_info != [country, state]]
    print(f"{state} removed successfully!")

def add_city():
    if not states:
        print("\nNo states available. Add states first.")
        return
    print("Available states: ", ", ".join([f"{state_info[0]}: {state_info[1]}" for state_info in states]))
    country = input("Enter the name of country to add cities: ").strip()
    if country not in countries or not any(state_info[0] == country for state_info in states):
        print(f"No states found for {country}. Please add the states first.")
        return
    state = input(f"Enter the name of state to add cities for {country}: ").strip()
    if not any(state_info[0] == country and state_info[1] == state for state_info in states):
        print(f"No such state {state} in {country}. Please add the state first.")
        return

    num_cities = int(input(f"How many cities do you want to add to {state}, {country}: "))
    for _ in range(num_cities):
        while True:
            city = input(f"Enter the name of city for {state}, {country}: ").strip()
            if not city.isalpha():
                print("\nInvalid input, please enter a valid city name.")
                continue
            if any(city_info[0] == country and city_info[1] == state and city_info[2] == city for city_info in cities):
                print(f"\n{city} is already added to {state}, {country}.")
            else:
                cities.append([country, state, city])
                print(f"{city} added successfully!")
            break

def update_city():
    country = input("Enter the country name to update city: ").strip()
    if country not in countries or not any(state_info[0] == country for state_info in states):
        print(f"No states found for {country}.")
        return
    state = input(f"Enter the state name to update city: ").strip()
    if not any(state_info[0] == country and state_info[1] == state for state_info in states):
        print(f"No such state {state} in {country}. Please add the state first.")
        return
    old_name = input(f"Enter the city name to update in {state}, {country}: ").strip()
    if not any(city_info[0] == country and city_info[1] == state and city_info[2] == old_name for city_info in cities):
        print(f"{old_name} does not exist in {state}, {country}.")
        return
    new_name = input("Enter the new city name: ").strip()
    if any(city_info[0] == country and city_info[1] == state and city_info[2] == new_name for city_info in cities):
        print(f"{new_name} already exists. Update not performed.")
    else:
        for city_info in cities:
            if city_info[0] == country and city_info[1] == state and city_info[2] == old_name:
                city_info[2] = new_name
                print(f"{old_name} updated to {new_name} successfully!")
                break

def remove_city():
    country = input("Enter the country name to remove city: ").strip()
    if country not in countries or not any(state_info[0] == country for state_info in states):
        print(f"No states found for {country}.")
        return
    state = input(f"Enter the state name to remove city: ").strip()
    if not any(state_info[0] == country and state_info[1] == state for state_info in states):
        print(f"No such state {state} in {country}. Please add the state first.")
        return
    city = input(f"Enter the city name to remove from {state}, {country}: ").strip()
    if not any(city_info[0] == country and city_info[1] == state and city_info[2] == city for city_info in cities):
        print(f"{city} does not exist in {state}, {country}.")
        return
    cities[:] = [city_info for city_info in cities if city_info != [country, state, city]]
    print(f"{city} removed successfully!")

def print_all_data():
    print("\nCurrent Data:")
    
    for country in countries:
        print(f"{country}:")
        country_states = [state_info[1] for state_info in states if state_info[0] == country]
        
        if country_states:
            for state in country_states:
                print(f"    {state}:")
                state_cities = [city_info[2] for city_info in cities if city_info[0] == country and city_info[1] == state]
                
                if state_cities:
                    for city in state_cities:
                        print(f"        {city}")
                else:
                    print(f"        No cities added")
        else:
            print(f"    No states added")

while True:
    print('''
    1. Add
    2. Update
    3. Delete
    4. Print all Data
    5. Exit\n''')
    opt1 = int(input("Select an option: "))
    
    if opt1 == 1:
        while True:
            print('''
    1. Add Country
    2. Add State
    3. Add City
    4. Exit\n''')
            opt2 = int(input("Select an option: "))
            if opt2 == 1:
                add_country()
            elif opt2 == 2:
                add_state()
            elif opt2 == 3:
                add_city()
            else:
                break
                
    elif opt1 == 2:
        while True:
            print('''
    1. Update Country
    2. Update State
    3. Update City
    4. Exit\n''')
            opt3 = int(input("Select an option: "))
            if opt3 == 1:
                update_country()
            elif opt3 == 2:
                update_state()
            elif opt3 == 3:
                update_city()
            else:
                break
                
    elif opt1 == 3:
        while True:
            print('''
    1. Remove Country
    2. Remove State
    3. Remove City
    4. Exit\n''')
            opt4 = int(input("Select an option: "))
            if opt4 == 1:
                remove_country()
            elif opt4 == 2:
                remove_state()
            elif opt4 == 3:
                remove_city()
            else:
                break
                
    elif opt1 == 4:
        print_all_data()
    elif opt1 == 5:
        print("Exiting the program...")
        break
    else:
        continue
