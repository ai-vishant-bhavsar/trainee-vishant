import pandas as pd
import os
from collections import defaultdict

data = defaultdict(lambda: defaultdict(list))


def load_from_excel():
    file_path = "country_state_city_excel.xlsx"

    if os.path.exists(file_path):
        df = pd.read_excel(file_path)
        for _, row in df.iterrows():
            country = row['Country']
            state = row['State']
            city = row['City']

            if pd.isna(state) or state == "":
                state = ''
            if pd.isna(city) or city == "":
                city = ''

            if country and state and city:
                data[country][state].append(city)
            elif country and state:
                data[country][state]
            elif country:
                data[country]
    else:
        print("No existing Excel file found, creating a new one with headers.")
        df = pd.DataFrame(columns=["Country", "State", "City"])
        df.to_excel(file_path, index=False)
        print(f"Created Excel file {file_path}")


def get_valid_input(prompt: str) -> str:
    while True:
        value = input(prompt).strip()
        if value.isalpha():
            return value
        print("Invalid input, please enter a valid name.")


def get_valid_number(prompt: str) -> int:
    while True:
        try:
            num = int(input(prompt))
            if num > 0:
                return num
            print("Please enter a valid number greater than 0.")
        except ValueError:
            print("Invalid input! Please enter a valid number.")


def add_entry(type_: str, parent: str = None) -> None:
    if type_ == "country":
        num_entries = get_valid_number("How many countries do you want to add? ")
        for _ in range(num_entries):
            country = get_valid_input("Enter the name of the country: ")
            if country not in data:
                data[country]
            else:
                print(f"{country} is alredy exists")
                add_entry("country")
    elif type_ == "state":
        country = get_valid_input("Enter the country for the state: ")
        if country not in data:
            print(f"{country} does not exist. Add country first.")
            return add_entry("country")
        num_entries = get_valid_number(f"How many states do you want to add to {country}? ")
        for _ in range(num_entries):
            state = get_valid_input(f"Enter the name of the state in {country}: ")
            if state not in data[country]:
                data[country][state]
            else:
                print(f"{state} already exists in {country}.")
                add_entry("state")
    elif type_ == "city":
        country = get_valid_input("Enter the country for the city: ")
        if country not in data:
            print(f"{country} does not exist. Add country first.")
            return add_entry("country")
        state = get_valid_input(f"Enter the state for the city in {country}: ")
        if state not in data[country]:
            print(f"{state} does not exist in {country}. Add state first.")
            return add_entry("state")
        num_entries = get_valid_number(f"How many cities do you want to add to {state}, {country}? ")
        for _ in range(num_entries):
            city = get_valid_input(f"Enter the name of the city in {state}, {country}: ")
            if city not in data[country][state]:
                data[country][state].append(city)
            else:
                print(f"{city} is alrady exists in the {country} in {state}.")
                return add_entry("city")


def update_entry(type_: str):
    def decorator(func):
        def wrapper(*args, **kwargs):
            parent = kwargs.get('parent')
            if type_ == "country":
                if parent not in data:
                    print(f"{parent} does not exist. Add the country first.")
                    return
            elif type_ == "state":
                country = kwargs.get('country')
                if country not in data:
                    print(f"{country} does not exist. Add the country first.")
                    return
                if parent not in data[country]:
                    print(f"{parent} does not exist in {country}. Add the state first.")
                    return
            elif type_ == "city":
                country = kwargs.get('country')
                state = kwargs.get('state')
                if country not in data:
                    print(f"{country} does not exist. Add the country first.")
                    return
                if state not in data[country]:
                    print(f"{state} does not exist in {country}. Add the state first.")
                    return
                if parent not in data[country][state]:
                    print(f"{parent} does not exist in {state}, {country}. Add the city first.")
                    return
            return func(*args, **kwargs)

        return wrapper

    return decorator


@update_entry("country")
def update_country(parent: str):
    new_name = get_valid_input(f"Enter the new name for the country {parent}: ")
    if new_name not in data:
        data[new_name] = data.pop(parent)
        print(f"{parent} has been updated to {new_name}.")
    else:
        print(f"{new_name} already exists. Update failed.")


@update_entry("state")
def update_state(country: str, parent: str):
    new_state = get_valid_input(f"Enter the new name for the state {parent}: ")
    if new_state not in data[country]:
        data[country][new_state] = data[country].pop(parent)
        print(f"{parent} has been updated to {new_state}.")
    else:
        print(f"{new_state} already exists in {country}. Update failed.")


@update_entry("city")
def update_city(country: str, state: str, parent: str):
    new_city = get_valid_input(f"Enter the new name for the city {parent}: ")
    data[country][state][data[country][state].index(parent)] = new_city
    print(f"{parent} has been updated to {new_city}.")


def remove_entry(type_: str, parent: str = None) -> None:
    if type_ == "country":
        country = get_valid_input("Enter the country to remove: ")
        if country in data:
            del data[country]
            print(f"{country} removed successfully!")
        else:
            print(f"{country} does not exist.")
    elif type_ == "state":
        country = get_valid_input("Enter the country to remove state from: ")
        if country in data:
            state = get_valid_input(f"Enter the state to remove from {country}: ")
            if state in data[country]:
                del data[country][state]
                print(f"{state} removed from {country}!")
            else:
                print(f"{state} does not exist in {country}.")
        else:
            print(f"{country} does not exist.")
    elif type_ == "city":
        country = get_valid_input("Enter the country to remove city from: ")
        if country in data:
            state = get_valid_input(f"Enter the state to remove city from in {country}: ")
            if state in data[country]:
                city = get_valid_input(f"Enter the city to remove from {state}, {country}: ")
                if city in data[country][state]:
                    data[country][state].remove(city)
                    print(f"{city} removed from {state}, {country}!")
                else:
                    print(f"{city} does not exist in {state}, {country}.")
            else:
                print(f"{state} does not exist in {country}.")
        else:
            print(f"{country} does not exist.")


def print_all_data() -> None:
    if not data:
        print("No data available.")
        return
    for country, states in data.items():
        print(f"\n{country}:")
        for state, cities in states.items():
            print(f"  {state}: {', '.join(cities) if cities else 'No cities added'}")


def save_to_excel():
    countries = []
    seen_combinations = set()

    for country, states in data.items():
        if not states:
            combination = (country, "", "")
            if combination not in seen_combinations:
                countries.append([country, "", ""])
                seen_combinations.add(combination)
        else:
            for state, cities in states.items():
                if not cities:
                    combination = (country, state, "")
                    if combination not in seen_combinations:
                        countries.append([country, state, ""])
                        seen_combinations.add(combination)
                else:
                    for city in cities:
                        combination = (country, state, city)
                        if combination not in seen_combinations:
                            countries.append([country, state, city])

    df = pd.DataFrame(countries, columns=["Country", "State", "City"])

    file_path = "country_state_city_excel.xlsx"
    df.to_excel(file_path, index=False)

    print(f"Data has been saved to {file_path} successfully.")


def save_to_csv():
    countries = []
    for country, states in data.items():
        for state, cities in states.items():
            for i, city in enumerate(cities):
                if i == 0:
                    countries.append([country, state, city])
                else:
                    countries.append(["", state, city])

    df = pd.DataFrame(countries, columns=["Country", "State", "City"])
    file_path = "country_state_city_excel.csv"
    df.to_csv(file_path, index=False)


def save_to_excel_and_csv():
    save_to_excel()
    save_to_csv()


load_from_excel()

while True:
    print('''\n
1. Add
2. Update
3. Delete
4. Print all Data
5. Exit\n''')
    try:
        opt1 = int(input("Select an option: "))
    except ValueError:
        print("Invalid input! Please enter a number.")
        continue

    if opt1 == 1:
        while True:
            print_all_data()
            print('''\n
1. Add Country
2. Add State
3. Add City
4. Exit''')
            try:
                opt2 = int(input("Select an option: "))
            except ValueError:
                print("Invalid input! Please enter a number.")
                continue
            if opt2 == 1:
                add_entry("country")
                save_to_excel_and_csv()
            elif opt2 == 2:
                add_entry("state")
                save_to_excel_and_csv()
            elif opt2 == 3:
                add_entry("city")
                save_to_excel_and_csv()
            else:
                break

    elif opt1 == 2:
        print('''\n
1. Update Country
2. Update State
3. Update City
4. Exit''')
        try:
            opt2 = int(input("Select an option: "))
        except ValueError:
            print("Invalid input! Please enter a number.")
            continue

        if opt2 == 1:
            country = get_valid_input("Enter the country to update: ")
            update_country(parent=country)
            save_to_excel_and_csv()
        elif opt2 == 2:
            country = get_valid_input("Enter the country for the state: ")
            state = get_valid_input(f"Enter the state to update in {country}: ")
            update_state(country=country, parent=state)
            save_to_excel_and_csv()
        elif opt2 == 3:
            country = get_valid_input("Enter the country for the city: ")
            state = get_valid_input(f"Enter the state for the city in {country}: ")
            city = get_valid_input(f"Enter the city to update in {state}, {country}: ")
            update_city(country=country, state=state, parent=city)
            save_to_excel_and_csv()
        else:
            break

    elif opt1 == 3:
        while True:
            print('''\n
1. Remove Country
2. Remove State
3. Remove City
4. Exit''')
            try:
                opt4 = int(input("Select an option: "))
            except ValueError:
                print("Invalid input! Please enter a number.")
                continue
            if opt4 == 1:
                remove_entry("country")
                save_to_excel_and_csv()
            elif opt4 == 2:
                remove_entry("state")
                save_to_excel_and_csv()
            elif opt4 == 3:
                remove_entry("city")
                save_to_excel_and_csv()
            else:
                break

    elif opt1 == 4:
        print_all_data()

    elif opt1 == 5:
        print("Exiting the program...")
        break
    else:
        print("Invalid input! Please select a valid option.")
