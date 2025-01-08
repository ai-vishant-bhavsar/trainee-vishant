def fectorial(n):
	if n == 1:
		return 1
		
	if n > 1:
		return fectorial(n-1) * fectorial(n-2)
		

n = int(input("Enter a number: "))
print(f"{n}! = {fectorial(n)}")
