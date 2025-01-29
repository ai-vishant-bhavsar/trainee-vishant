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
    print("\nCurrent Data:")
    if level == 'country':
        for country in data:
            print(f"Country: {country}")
    elif level == 'state':
        if country in data:
            print(f"{country}:")
            for state in data[country]:
                print(f"  State: {state}")
                print(f"    Cities: {', '.join(data[country][state]) if data[country][state] else 'No cities added'}")
        else:
            print(f"{country} does not exist.")
    elif level == 'city':
        if country in data:
            for state in data[country]:
                print(f"{country} -> {state}: {', '.join(data[country][state]) if data[country][state] else 'No cities added'}")

def add_entry(type_: str):
    print_current_data(type_)
    def add_fn(country=None, state=None, city=None):
        if type_ == "country":
            for _ in range(int(get_valid_input("How many countries do you want to add? ", False))):
                country = get_valid_input("Enter country name: ")
                if country not in data:
                    data[country]
                else:
                    print(f"{country} already exists.")
        elif type_ == "state":
            country = get_valid_input("Enter the country for the state: ")
            if country not in data: print(f"{country} does not exist. Add country first."); return
            for _ in range(int(get_valid_input(f"How many states to add to {country}? ", False))):
                state = get_valid_input(f"Enter the name of the state in {country}: ")
                if state not in data[country]:
                    data[country][state]
                else:
                    print(f"{state} already exists in {country}.")
        elif type_ == "city":
            country, state = get_valid_input("Enter the country for the city: "), get_valid_input(f"Enter the state in {country}: ")
            if country not in data or state not in data[country]: print(f"Add the country/state first."); return
            for _ in range(int(get_valid_input(f"How many cities to add in {state}, {country}? ", False))):
                city = get_valid_input(f"Enter the name of the city: ")
                if city not in data[country][state]:
                    data[country][state].append(city)
                else:
                    print(f"{city} already exists in {state}, {country}.")
        print_all_data()

    add_fn()

def update_entry(type_: str, country=None, state=None, city=None):
    print_current_data(type_, country, state)
    def update_fn(country, state, city, new_name):
        if type_ == "country" and new_name not in data:
            data[new_name] = data.pop(country)
        elif type_ == "state" and new_name not in data[country]:
            data[country][new_name] = data[country].pop(state)
        elif type_ == "city":
            data[country][state][data[country][state].index(city)] = new_name
        else:
            print(f"{new_name} already exists in the same level.")
        print_all_data()

    new_name = get_valid_input(f"Enter new name for the {type_}: ")
    update_fn(country, state, city, new_name)

def remove_entry(type_: str, country=None, state=None, city=None):
    print_current_data(type_, country, state)
    def remove_fn(country, state, city):
        if type_ == "country" and country in data:
            del data[country]
        elif type_ == "state" and state in data[country]:
            del data[country][state]
        elif type_ == "city" and city in data[country][state]:
            data[country][state].remove(city)
        else:
            print(f"{type_} does not exist in the specified location.")
        print_all_data()

    remove_fn(country, state, city)

def print_all_data():
    for country, states in data.items():
        print(f"{country}: ", end="")
        for state, cities in states.items():
            print(f"{state} -> {', '.join(cities) if cities else 'No cities added'}", end=" | ")
        print()

def save_to_file():
    df = pd.DataFrame(
        [[country, state, city] for country, states in data.items() for state, cities in states.items() for city in cities],
        columns=["Country", "State", "City"]
    )
    df.to_excel(file_path, index=False)
    df.to_csv("country_state_city_excel.csv", index=False)
    print(f"Data saved to {file_path} and CSV file.")

load_from_excel()

while True:
    print('''\n1. Add\n2. Update\n3. Remove\n4. Print All Data\n5. Exit\n''')
    choice = get_valid_input("Select an option: ", False)

    if choice == "1":
        print('''\n1. Add Country\n2. Add State\n3. Add City\n4. Exit''')
        sub_choice = get_valid_input("Select an option: ", False)
        if sub_choice == "1": add_entry("country")
        elif sub_choice == "2": add_entry("state")
        elif sub_choice == "3": add_entry("city")
        else: break
    elif choice == "2":
        print('''\n1. Update Country\n2. Update State\n3. Update City\n4. Exit''')
        sub_choice = get_valid_input("Select an option: ", False)
        if sub_choice == "1": update_entry("country", get_valid_input("Enter country to update: "), None, None)
        elif sub_choice == "2": update_entry("state", get_valid_input("Enter country for the state: "), get_valid_input("Enter state to update: "), None)
        elif sub_choice == "3": update_entry("city", get_valid_input("Enter country for city: "), get_valid_input("Enter state for city: "), get_valid_input("Enter city to update: "))
        else: break
    elif choice == "3":
        print('''\n1. Remove Country\n2. Remove State\n3. Remove City\n4. Exit''')
        sub_choice = get_valid_input("Select an option: ", False)
        if sub_choice == "1": remove_entry("country", get_valid_input("Enter country to remove: "))
        elif sub_choice == "2": remove_entry("state", get_valid_input("Enter country for state removal: "), get_valid_input("Enter state to remove: "))
        elif sub_choice == "3": remove_entry("city", get_valid_input("Enter country for city removal: "), get_valid_input("Enter state for city removal: "), get_valid_input("Enter city to remove: "))
        else: break
    elif choice == "4":
        print_all_data()
    elif choice == "5":
        print("Exiting the program...")
        break
    else:
        print("Invalid input! Please select a valid option.")
    save_to_file()
