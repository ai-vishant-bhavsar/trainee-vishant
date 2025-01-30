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

def handle_entry(action, entry_type, parent=None):
    if entry_type == "country":
        name = get_valid_input(f"Enter the name of the {entry_type}: ")
        if action == "add": 
            data[name]
        elif action == "update":
            new_name = get_valid_input(f"Enter the new name for {name}: ")
            data[new_name] = data.pop(name, {})
        elif action == "remove":
            data.pop(name, None)
        print(f"{action.capitalize()} {entry_type} complete.")
        
    elif entry_type == "state" or entry_type == "city":
        country = get_valid_input(f"Enter the country for the {entry_type}: ")
        if country not in data:
            print(f"{country} does not exist. Add country first.")
            return
        parent_data = data[country]
        if entry_type == "state":
            name = get_valid_input(f"Enter the name of the {entry_type} in {country}: ")
        elif entry_type == "city":
            state = get_valid_input(f"Enter the state for the {entry_type} in {country}: ")
            if state not in parent_data:
                print(f"{state} does not exist in {country}. Add state first.")
                return
            name = get_valid_input(f"Enter the name of the {entry_type} in {state}, {country}: ")

        if action == "add" and name not in parent_data:
            if entry_type == "state":
                parent_data[name] = []
            elif entry_type == "city":
                parent_data[state].append(name)
        elif action == "update":
            new_name = get_valid_input(f"Enter the new name for {name}: ")
            if entry_type == "state":
                parent_data[new_name] = parent_data.pop(name)
            elif entry_type == "city":
                for state_name in parent_data:
                    if name in parent_data[state_name]:
                        parent_data[state_name].remove(name)
                        parent_data[state_name].append(new_name)
        elif action == "remove" and name in parent_data:
            if entry_type == "state":
                parent_data.pop(name)
            elif entry_type == "city":
                parent_data[state].remove(name)
        print(f"{action.capitalize()} {entry_type} complete.")

def print_all_data() -> None:
    if not data:
        print("No data available.")
        return
    for country, states in data.items():
        print(f"\n{country}:")
        for state, cities in states.items():
            print(f"  {state}: {', '.join(cities) if cities else 'No cities added'}")

def menu():
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
            for option, entry_type in [(1, "country"), (2, "state"), (3, "city")]:
                print(f'{option}. Add {entry_type.capitalize()}')
            option = int(input("Select an option: "))
            if option in [1, 2, 3]:
                handle_entry("add", ["country", "state", "city"][option-1])

        elif opt1 == 2:
            for option, entry_type in [(1, "country"), (2, "state"), (3, "city")]:
                print(f'{option}. Update {entry_type.capitalize()}')
            option = int(input("Select an option: "))
            if option in [1, 2, 3]:
                handle_entry("update", ["country", "state", "city"][option-1])

        elif opt1 == 3:
            for option, entry_type in [(1, "country"), (2, "state"), (3, "city")]:
                print(f'{option}. Remove {entry_type.capitalize()}')
            option = int(input("Select an option: "))
            if option in [1, 2, 3]:
                handle_entry("remove", ["country", "state", "city"][option-1])

        elif opt1 == 4:
            print_all_data()

        elif opt1 == 5:
            print("Exiting the program...")
            break
        else:
            print("Invalid input! Please select a valid option.")

menu()
