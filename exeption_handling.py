from collections import defaultdict

data = defaultdict(lambda: defaultdict(list))


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
    elif type_ == "state":
        country = get_valid_input("Enter the country for the state: ")
        if country not in data:
            print(f"{country} does not exist. Add country first.")
            return
        num_entries = get_valid_number(f"How many states do you want to add to {country}? ")
        for _ in range(num_entries):
            state = get_valid_input(f"Enter the name of the state in {country}: ")
            if state not in data[country]:
                data[country][state]
            else:
                print(f"{state} already exists in {country}.")
    elif type_ == "city":
        country = get_valid_input("Enter the country for the city: ")
        if country not in data:
            print(f"{country} does not exist. Add country first.")
            return
        state = get_valid_input(f"Enter the state for the city in {country}: ")
        if state not in data[country]:
            print(f"{state} does not exist in {country}. Add state first.")
            return
        num_entries = get_valid_number(f"How many cities do you want to add to {state}, {country}? ")
        for _ in range(num_entries):
            city = get_valid_input(f"Enter the name of the city in {state}, {country}: ")
            if city not in data[country][state]:
                data[country][state].append(city)


def update_entry(type_: str, country=None, state=None, city=None):
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


while True:
    print('''1. Add
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
            elif opt2 == 2:
                add_entry("state")
            elif opt2 == 3:
                add_entry("city")
            else:
                break

    elif opt1 == 2:
        print('''\n1. Update Country\n2. Update State\n3. Update City\n4. Exit''')
        sub_choice = get_valid_input("Select an option: ")
        if sub_choice == "1":
            update_entry("country", get_valid_input("Enter country to update: "), None, None)
        elif sub_choice == "2":
            update_entry("state", get_valid_input("Enter country for the state: "),
            get_valid_input("Enter state to update: "), None)
        elif sub_choice == "3":
            update_entry("city", get_valid_input("Enter country for city: "), get_valid_input("Enter state for city: "),
            get_valid_input("Enter city to update: "))
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
            elif opt4 == 2:
                remove_entry("state")
            elif opt4 == 3:
                remove_entry("city")
            else:
                break

    elif opt1 == 4:
        print_all_data()

    elif opt1 == 5:
        print("Exiting the program...")
        break
    else:
        print("Invalid input! Please select a valid option.")
