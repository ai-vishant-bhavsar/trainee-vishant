def fun1(num):
	while(True): 
		print('''
	1. Addition
	2. Subtraction
	3. Multiplication
	4. Division
	5. Modulo
	6. Flore Divison
	7. Exit''')
		opt = int(input("Enter a number(1 to 7): "))
		if opt == 1:
			x = num()
			y = num()
			print(f"{x} + {y} = {x+y}")
		elif opt == 2:
			x = num()
			y = num()
			print(f"{x} - {y} = {x-y}")
		elif opt == 3:
			x = num()
			y = num()
			print(f"{x} * {y} = {x*y}")
		elif opt == 4:
			x = num()
			while(True):
				y = num()
				if y > 0:
					break 
				else:
					print("Invalid input!")
					continue 
			print(f"{x} / {y} = {x/y}")
		elif opt == 5:
			x = num()
			while(True):
				y = num()
				if y > 0:
					break 
				else:
					print("Invalid input!")
					continue 
			print(f"{x} % {y} = {x%y}")
		elif opt == 6:
			x = num()
			while(True):
				y = num()
				if y > 0:
					break 
				else:
					print("Invalid input!")
					continue 
			print(f"{x} // {y} = {x//y}")
		elif opt == 7:
			break 
		else:
			print("Invalid input!")
			continue 


@fun1
def num():
	x = int(input("Enter a value: "))
	return x
