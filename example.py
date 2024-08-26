# example.py

def greet(name):
    if name:
        print(f"Hello, {name}!")
    else:
        print("Hello, World!")

def add_numbers(a, b):
    return a + b

class Calculator:
    def __init__(self):
        self.history = []

    def add(self, a, b):
        result = a + b
        self.history.append(result)
        return result

    def subtract(self, a, b):
        result = a - b
        self.history.append(result)
        return result

if __name__ == "__main__":
    greet("Alice")
    calc = Calculator()
    print(calc.add(5, 3))
    print(calc.subtract(10, 7))
