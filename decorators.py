import time

def fun1(num):
    global start, end
    start = time.time()
    
    while True:
        print('''
        1. Addition
        2. Subtraction
        3. Multiplication
        4. Division
        5. Modulo
        6. Floor Division
        7. Exit''')
        
        try:
            opt = int(input("Enter a number (1 to 7): "))
        except (ValueError, TypeError):
            print("Invalid input! Please enter a valid number between 1 and 7.")
            continue
        
        if opt == 1:
            try:
                x = num()
                y = num()
                print(f"{x} + {y} = {x + y}")
            except (ValueError, TypeError):
                print("Invalid input! Please enter valid integers for the operation.")
        elif opt == 2:
            try:
                x = num()
                y = num()
                print(f"{x} - {y} = {x - y}")
            except (ValueError, TypeError):
                print("Invalid input! Please enter valid integers for the operation.")
        elif opt == 3:
            try:
                x = num()
                y = num()
                print(f"{x} * {y} = {x * y}")
            except (ValueError, TypeError):
                print("Invalid input! Please enter valid integers for the operation.")
        elif opt == 4:
            try:
                x = num()
                while True:
                    try:
                        y = num()
                        if y == 0:
                            print("Division by zero is not allowed! Please enter a valid value for y.")
                            continue
                        break
                    except (ValueError, TypeError):
                        print("Invalid input! Please enter a valid number for y.")
                print(f"{x} / {y} = {x / y}")
            except (ValueError, TypeError):
                print("Invalid input! Please enter valid integers for the operation.")
        elif opt == 5:
            try:
                x = num()
                while True:
                    try:
                        y = num()
                        if y == 0:
                            print("Modulo by zero is not allowed! Please enter a valid value for y.")
                            continue
                        break
                    except (ValueError, TypeError):
                        print("Invalid input! Please enter a valid number for y.")
                print(f"{x} % {y} = {x % y}")
            except (ValueError, TypeError):
                print("Invalid input! Please enter valid integers for the operation.")
        elif opt == 6:
            try:
                x = num()
                while True:
                    try:
                        y = num()
                        if y == 0:
                            print("Floor division by zero is not allowed! Please enter a valid value for y.")
                            continue
                        break
                    except (ValueError, TypeError):
                        print("Invalid input! Please enter a valid number for y.")
                print(f"{x} // {y} = {x // y}")
            except (ValueError, TypeError):
                print("Invalid input! Please enter valid integers for the operation.")
        elif opt == 7:
            end = time.time()
            break
        else:
            print("Invalid input! Please enter a number between 1 and 7.")
            continue
    
    print(f"Total time taken for the operations: {end - start:.4f} seconds")

@fun1
def num():
    while True:
        try:
            x = int(input("Enter a value: "))
            return x
        except (ValueError, TypeError):
            print("Invalid input! Please enter a valid integer.")