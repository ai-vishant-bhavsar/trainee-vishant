def fun(fun1):
	print("*" * 5)
	print("%" * 5)
	fun1()
	print("*" * 5)
	print("%" * 5)


@fun
def fun1():
	print("Hello!")
