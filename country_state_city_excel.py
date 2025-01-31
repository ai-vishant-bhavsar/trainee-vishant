import pandas as pd
import os
from collections import defaultdict

data = defaultdict(lambda: defaultdict(list))
file_path = "country_state_city_excel.xlsx"

def load_from_excel():
    if os.path.exists(file_path):
        df = pd.read_excel(file_path)
        for _, row in df.iterrows():
            country, state, city = row['Country'], row['State'], row['City']
            if pd.isna(state) or state == "": state = ''
            if pd.isna(city) or city == "": city = ''
            if country and state and city:
                data[country][state].append(city)
            elif country and state:
                data[country][state]
            elif country:
                data[country]
    else:
        pd.DataFrame(columns=["Country", "State", "City"]).to_excel(file_path, index=False)
        print(f"Created Excel file {file_path}")

def get_valid_input(prompt: str, is_alpha=True) -> str:
    while True:
        value = input(prompt).strip()
        if (is_alpha and value.isalpha()) or (not is_alpha and value.isdigit() and int(value) > 0):
            return value
        print(f"Invalid input! Please enter a valid {'name' if is_alpha else 'number'}.")

def print_current_data(level, country=None, state=None):
    if not data:
        print("No data available right now.\n")
    else:
        print("\nCurrent Data:")
        if level == 'country':
            for country in data:
                print(f"Country: {country}")
        elif level == 'state':
            if country in data:
                print(f"{country}:")
                if data[country]:
                    for state in data[country]:
                        print(f"  State: {state}")
                        print(f"    Cities: {', '.join(data[country][state]) if data[country][state] else 'No cities added'}")
                else:
                    print(f"No states added in {country}.")
            else:
                print(f"{country} does not exist.")
        elif level == 'city':
            if country in data:
                print(f"{country}:")
                for state in data[country]:
                    print(f"  State: {state}")
                    if data[country][state]:
                        print(f"    Cities: {', '.join(data[country][state])}")
                    else:
                        print(f"    No cities added in {state}.")

def add_entry(type_: str):
    load_from_excel()

    def add_fn(country=None, state=None, city=None):
        if type_ == "country":
            print_current_data(type_)
            for _ in range(int(get_valid_input("How many countries do you want to add? ", False))):
                country = get_valid_input("Enter country name: ")
                if country not in data:
                    data[country]
                else:
                    print(f"{country} already exists.")
        elif type_ == "state":
            print_current_data("country")
            if not any(data):
                print("No countries exist to add a state.")
                return
            country = get_valid_input("Enter the country for the state: ")
            if country not in data:
                print(f"{country} does not exist. Add country first.")
                return
            print_current_data("state")
            for _ in range(int(get_valid_input(f"How many states to add to {country}? ", False))):
                state = get_valid_input(f"Enter the name of the state in {country}: ")
                if state not in data[country]:
                    data[country][state]
                else:
                    print(f"{state} already exists in {country}.")
        elif type_ == "city":
            print_current_data("state")
            if not any([bool(data[country]) for country in data]):
                print("No states exist to add a city.")
                return
            country = get_valid_input("Enter the country for the city: ")
            state = get_valid_input(f"Enter the state in {country}: ")
            if country not in data or state not in data[country]:
                print(f"Add the country/state first.")
                return
            print_current_data("city")
            for _ in range(int(get_valid_input(f"How many cities to add in {state}, {country}? ", False))):
                city = get_valid_input(f"Enter the name of the city: ")
                if city not in data[country][state]:
                    data[country][state].append(city)
                else:
                    print(f"{city} already exists in {state}, {country}.")

    add_fn()
    save_to_file()

def update_entry(type_: str, country=None, state=None, city=None):
    def update_fn(country, state, city, new_name):
        if type_ == "country" and new_name not in data:
            data[new_name] = data.pop(country)
        elif type_ == "state":
            if state not in data[country]:
                print(f"State {state} does not exist in {country}. Cannot update.")
                return
            if new_name not in data[country]:
                data[country][new_name] = data[country].pop(state)
            else:
                print(f"{new_name} already exists in {country}.")
        elif type_ == "city":
            if city not in data[country][state]:
                print(f"City {city} does not exist in {state}, {country}. Cannot update.")
                return
            data[country][state][data[country][state].index(city)] = new_name
        else:
            print(f"{new_name} already exists in the same level.")

    new_name = get_valid_input(f"Enter new name for the {type_}: ")
    update_fn(country, state, city, new_name)
    save_to_file()

def remove_entry(type_: str, country=None, state=None, city=None):
    def remove_fn(country, state, city):
        if type_ == "country" and country in data:
            del data[country]
        elif type_ == "state":
            if state not in data[country]:
                print(f"State {state} does not exist in {country}. Cannot remove.")
                return
            del data[country][state]
        elif type_ == "city":
            if city not in data[country][state]:
                print(f"City {city} does not exist in {state}, {country}. Cannot remove.")
                return
            data[country][state].remove(city)
        else:
            print(f"{type_} does not exist in the specified location.")

    remove_fn(country, state, city)
    save_to_file()

def print_all_data():
    if not data: return add_entry
    for country, states in data.items():
        print(f"{country}: ")
        for state, cities in states.items():
            print(f"{state}{', '.join(cities) if cities else 'No cities added'}")
        print()

def save_to_file():
    df = pd.DataFrame(
        [[country, state, city] for country, states in data.items() for state, cities in states.items() for city in cities],
        columns=["Country", "State", "City"]
    )
    df.to_excel(file_path, index=False)
    df.to_csv("country_state_city_excel.csv", index=False)

load_from_excel()

while True:
    print('''\n1. Add\n2. Update\n3. Remove\n4. Print All Data\n5. Exit\n''')
    choice = get_valid_input("Select an option: ", False)
    
    if choice == "1":
        while True:
            print('''\n1. Add Country\n2. Add State\n3. Add City\n4. Exit''')
            sub_choice = get_valid_input("Select an option: ", False)
            
            if sub_choice == "1":
                add_entry("country")
                save_to_file()
                continue
            elif sub_choice == "2":
                if not any(data):
                    print("No countries exist to add a state.")
                else:
                    add_entry("state")
                save_to_file()
                continue
            elif sub_choice == "3":
                country = get_valid_input("Enter the country for the city: ")
                if country not in data or not data[country]:
                    print(f"No states exist in {country}. Cannot add a city.")
                else:
                    add_entry("city")
                save_to_file()
                continue
            elif sub_choice == "4":
                break
            else:
                continue

    elif choice == "2":
        while True:
            if not data: 
                print("No data available"); break
            else:
                print('''\n1. Update Country\n2. Update State\n3. Update City\n4. Exit''')
                sub_choice = get_valid_input("Select an option: ", False)
                if sub_choice == "1":
                    update_entry("country", get_valid_input("Enter country to update: "), None, None)
                    save_to_file()
                    continue
                elif sub_choice == "2":
                    country = get_valid_input("Enter country for state: ")
                    if country in data and not data[country]:
                        print(f"No states exist in {country}. Cannot update state.")
                    else:
                        update_entry("state", country, get_valid_input("Enter state to update: "), None)
                    save_to_file()
                    continue
                elif sub_choice == "3":
                    country = get_valid_input("Enter country for city: ")
                    state = get_valid_input("Enter state for city: ")
                    if country in data and state in data[country] and not data[country][state]:
                        print(f"No cities exist in {state}, {country}. Cannot update city.")
                    else:
                        update_entry("city", country, state, get_valid_input("Enter city to update: "))
                    continue
                elif sub_choice == "4":
                    break
                else:
                    break

    elif choice == "3":
        while True:
            if not data: 
                print("No data available"); break
            else:
                print('''\n1. Remove Country\n2. Remove State\n3. Remove City\n4. Exit''')
                sub_choice = get_valid_input("Select an option: ", False)
                if sub_choice == "1":
                    remove_entry("country", get_valid_input("Enter country to remove: "))
                elif sub_choice == "2":
                    country = get_valid_input("Enter country for state removal: ")
                    if country in data and not data[country]:
                        print(f"No states exist in {country}. Cannot remove state.")
                    else:
                        remove_entry("state", country, get_valid_input("Enter state to remove: "), None)
                elif sub_choice == "3":
                    country = get_valid_input("Enter country for city removal: ")
                    state = get_valid_input("Enter state for city removal: ")
                    if country in data and state in data[country] and not data[country][state]:
                        print(f"No cities exist in {state}, {country}. Cannot remove city.")
                    else:
                        remove_entry("city", country, state, get_valid_input("Enter city to remove: "))
                elif sub_choice == "4":
                    break
                else:
                    break

    elif choice == "4":
        print_all_data()

    elif choice == "5":
        print("Exiting the program...")
        break
    else:
        print("Invalid input! Please select a valid option.")
    save_to_file()
