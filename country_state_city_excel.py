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
            if pd.isna(country) or country == "": country = ''
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
        if level == 'country':
            print("Country: ", end='')
            for country in data:
                print(f"{country}, ", end='')
            print("")
        elif level == 'state':
            if data[country]:
                print("State: ", end='')
                for state in data[country]:
                    print(f"{state}, ", end='')
                print("")
        elif level == 'city':
            if data[country][state]:
                print(f"    Cities: {', '.join(data[country][state])}")


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
            print_current_data("country", country)
            if not any(data):
                print("No countries exist to add a state.")
                return
            country = get_valid_input("Enter the country for the state: ")
            if country not in data:
                print(f"{country} does not exist. Add country first.")
                return
            for _ in range(int(get_valid_input(f"How many states to add to {country}? ", False))):
                state = get_valid_input(f"Enter the name of the state in {country}: ")
                if state not in data[country]:
                    data[country][state]
                else:
                    print(f"{state} already exists in {country}.")
        elif type_ == "city":
            print_current_data("country", country)
            if not any([bool(data[country]) for country in data]):
                print("No states exist to add a city.")
                return
            country = get_valid_input("Enter the country for the city: ")
            print_current_data("state")
            state = get_valid_input(f"Enter the state in {country}: ")
            if country not in data or state not in data[country]:
                print(f"Add the country and state first.")
                return
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
    if not data: return 'No data available'
    for country, states in data.items():
        print(f"{country}: ")
        for state, cities in states.items():
            print(f"{state}: {', '.join(cities) if cities else 'No cities added'}")
        print("")


def save_to_file():
    df = pd.DataFrame(columns=['Country', 'State', 'City'])
    for country, states in data.items():
        if country not in df['Country'].values:
            country_col = {'Country': country}
            df = pd.concat([df, pd.DataFrame([country_col])], ignore_index=True)
        for state, cities in states.items():
            if state not in df['State'].values:
                state_col = {'State': state}
                df = pd.concat([df, pd.DataFrame([state_col])], ignore_index=True)
            for city in cities:
                if city not in df['City'].values:
                    city_col = {'City': city}
                    df = pd.concat([df, pd.DataFrame([city_col])], ignore_index=True)

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
                if not any(data):
                    print("No countries exist to add a state or city.")
                else:
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
                print("No data available")
                break
            else:
                print('''\n1. Update Country\n2. Update State\n3. Update City\n4. Exit''')
                sub_choice = get_valid_input("Select an option: ", False)
                if sub_choice == "1":
                    print_current_data("country")
                    update_entry("country", get_valid_input("Enter country to update: "), None, None)
                    save_to_file()
                    continue
                elif sub_choice == "2":
                    print_current_data("country")
                    country = get_valid_input("Enter country for state: ")
                    if country in data and not data[country]:
                        print(f"No states exist in {country}. Cannot update state.")
                    else:
                        print_current_data("state", country)
                        update_entry("state", country, get_valid_input("Enter state to update: "), None)
                    save_to_file()
                    continue
                elif sub_choice == "3":
                    print_current_data("country")
                    country = get_valid_input("Enter country for city: ")
                    print_current_data("state", country)
                    state = get_valid_input("Enter state for city: ")
                    if country in data and state in data[country] and not data[country][state]:
                        print(f"No cities exist in {state}, {country}. Cannot update city.")
                    else:
                        print_current_data("city", country, state)
                        update_entry("city", country, state, get_valid_input("Enter city to update: "))
                    continue
                elif sub_choice == "4":
                    break
                else:
                    break

    elif choice == "3":
        while True:
            if not data:
                print("No data available")
                break
            else:
                print('''\n1. Remove Country\n2. Remove State\n3. Remove City\n4. Exit''')
                sub_choice = get_valid_input("Select an option: ", False)
                if sub_choice == "1":
                    print_current_data("country")
                    remove_entry("country", get_valid_input("Enter country to remove: "))
                elif sub_choice == "2":
                    print_current_data("country")
                    country = get_valid_input("Enter country for state removal: ")
                    if country in data and not data[country]:
                        print(f"No states exist in {country}. Cannot remove state.")
                    else:
                        print_current_data("state", country)
                        remove_entry("state", country, get_valid_input("Enter state to remove: "), None)
                elif sub_choice == "3":
                    print_current_data("country")
                    country = get_valid_input("Enter country for city removal: ")
                    print_current_data("state", country)
                    state = get_valid_input("Enter state for city removal: ")
                    if country in data and state in data[country] and not data[country][state]:
                        print(f"No cities exist in {state}, {country}. Cannot remove city.")
                    else:
                        print_current_data("city", country, state)
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
