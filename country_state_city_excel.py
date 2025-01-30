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
            if country and state and city:
                data[country][state].append(city)
            elif country and state: data[country][state]
    else:
        pd.DataFrame(columns=["Country", "State", "City"]).to_excel(file_path, index=False)

def get_valid_input(prompt: str, input_type=str) -> str:
    while True:
        try:
            value = input(prompt).strip()
            if input_type == str and value.isalpha(): return value
            if input_type == int and int(value) > 0: return int(value)
        except ValueError: pass
        print("Invalid input, please try again.")

def add_entry(type_: str):
    if type_ == "country": num_entries = get_valid_input("How many countries to add? ", int)
    elif type_ == "state": country = get_valid_input("Enter country for state: "); num_entries = get_valid_input(f"How many states for {country}? ", int)
    else: country, state = get_valid_input("Enter country for city: "), get_valid_input("Enter state for city: "); num_entries = get_valid_input(f"How many cities for {state}, {country}? ", int)
    for _ in range(num_entries):
        if type_ == "country": value = get_valid_input(f"Enter country: ")
        elif type_ == "state": value = get_valid_input(f"Enter state in {country}: ")
        else: value = get_valid_input(f"Enter city in {state}, {country}: ")
        if type_ == "country" and value not in data: data[value]
        elif type_ == "state" and value not in data[country]: data[country][value]
        elif type_ == "city" and value not in data[country][state]: data[country][state].append(value)

def update_entry(type_: str):
    def decorator(func):
        def wrapper(*args, **kwargs):
            parent = kwargs.get('parent')
            if type_ == "country" and parent not in data or type_ == "state" and parent not in data[kwargs.get('country')] or type_ == "city" and parent not in data[kwargs.get('country')][kwargs.get('state')]: 
                print(f"{parent} does not exist. Add first.")
                return
            return func(*args, **kwargs)
        return wrapper
    return decorator

@update_entry("country")
def update_country(parent: str): data[get_valid_input(f"New name for {parent}: ")] = data.pop(parent)

@update_entry("state")
def update_state(country: str, parent: str): data[country][get_valid_input(f"New name for {parent}: ")] = data[country].pop(parent)

@update_entry("city")
def update_city(country: str, state: str, parent: str): data[country][state][data[country][state].index(parent)] = get_valid_input(f"New name for {parent}: ")

def remove_entry(type_: str):
    if type_ == "country": country = get_valid_input("Enter country to remove: ")
    elif type_ == "state": country, state = get_valid_input("Enter country for state: "), get_valid_input("Enter state to remove: ")
    else: country, state, city = get_valid_input("Enter country for city: "), get_valid_input("Enter state for city: "), get_valid_input("Enter city to remove: ")
    if type_ == "country" and country in data: del data[country]
    elif type_ == "state" and state in data[country]: del data[country][state]
    elif type_ == "city" and city in data[country][state]: data[country][state].remove(city)

def print_countires():
    if data: 
        print("Countries: ",end="")
        for country, states in data.items():
            print(f"{country}",end="")
    else: print("No data available.")

def print_states(country: str):
    if country in data:
        print(f"{country}:")
        for state in data[country]:
            print(f"  {state}")
    else:
        print(f"No states available for {country}.")

def print_cities(country: str, state: str):
    if country in data and state in data[country]:
        print(f"{country} -> {state}:")
        for city in data[country][state]:
            print(f"  {city}")
    else:
        print(f"No cities available for {state}, {country}.")

def print_all_data() -> None:
    if not data:
        print("No data available.")
        return
    for country, states in data.items():
        print(f"\n{country}:")
        for state, cities in states.items():
            print(f"  {state}: {', '.join(cities) if cities else 'No cities added'}")

def save_to_excel():
    countries = [[country, state, city] for country, states in data.items() for state, cities in states.items() for city in cities]
    pd.DataFrame(countries, columns=["Country", "State", "City"]).to_excel(file_path, index=False)

def save_to_csv():
    countries = [[country, state, city] for country, states in data.items() for state, cities in states.items() for city in cities]
    pd.DataFrame(countries, columns=["Country", "State", "City"]).to_csv(file_path.replace(".xlsx", ".csv"), index=False)

load_from_excel()

while True:
    opt1 = get_valid_input('''\n1. Add\n2. Update\n3. Delete\n4. Print all Data\n5. Exit\nEnter a number(1 to 5): ''', int)
    if opt1 == 1:
        while True:
            opt2 = get_valid_input('''\n1. Add Country\n2. Add State\n3. Add City\n4. Exit\nEnter a number(1 to 4): ''', int)
            if opt2 == 1: 
                print_countires()
                add_entry("country")
                continue
            elif opt2 == 2: 
                print_countires()
                country = get_valid_input("\nEnter country for state: ")
                print_states(country)
                add_entry("state")
                continue
            elif opt2 == 3: 
                print_countires()
                country = get_valid_input("\nEnter country for city: ")
                print_states(country)
                state = get_valid_input("Enter state for city: ")
                print_cities(country, state)
                add_entry("city")
                continue
            save_to_excel()
            save_to_csv()
    elif opt1 == 2:
        opt2 = get_valid_input('''\n1. Update Country\n2. Update State\n3. Update City\n4. Exit\nEnter a number(1 to 4): ''', int)
        if opt2 == 1: 
            print_countires(country)
            update_country(get_valid_input("\nEnter country to update: "))
        elif opt2 == 2: 
            print_countires()
            country = get_valid_input("\nEnter country for state: ")
            print_states(country)
            update_state(country, get_valid_input("Enter state to update: "))
        elif opt2 == 3: 
            print_countires()
            country = get_valid_input("\nEnter country for city: ")
            print_states(country)
            state = get_valid_input("Enter state for city: ")
            print_cities(country, state)
            update_city(country, state, get_valid_input("Enter city to update: "))
        save_to_excel()
        save_to_csv()
    elif opt1 == 3:
        opt4 = get_valid_input('''\n1. Remove Country\n2. Remove State\n3. Remove City\n4. Exit\nEnter a number(1 to 4): ''', int)
        if opt4 == 1: 
            print_countires()  
            remove_entry("country")
        elif opt4 == 2: 
            print_countires()
            country = get_valid_input("\nEnter country for state: ")
            print_states(country)  
            remove_entry("state")
        elif opt4 == 3: 
            country = get_valid_input("\nEnter country for city: ")
            state = get_valid_input("Enter state for city: ")
            print_cities(country, state) 
            remove_entry("city")
        save_to_excel()
        save_to_csv()
    elif opt1 == 4: 
        print_all_data()
    elif opt1 == 5: 
        break
    else: 
        print("Invalid input!")
