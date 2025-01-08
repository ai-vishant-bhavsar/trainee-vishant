        
def decor1(func):
        def star():
               print("* " * 5)
               func()
               print("* " * 5)
        return star
def decor2(func):
        def modulo():
               print("% " * 5)
               func()
               print("% " * 5)
        return modulo
    
@decor1
       
@decor2
def hello():
         print("Hello")

hello()
