import py_compile
import random
import string

def random_identifier():
    def gen():
        for i in range(random.randint(3, 15)):
            yield random.choice(string.lowercase)
    return ''.join(gen())

def random_literal():
    choice = random.randint(0, 3)
    if choice is 0:
        return str(random.randint(0, 100))
    if choice is 1:
        return "\"%s\"" % random_identifier()
    if choice is 2:
        return random.choice("True", "False")

class FakeFunc(object):
    def __init__(self):
        self.num_args = random.randint(0, 3)
        self.name = random_identifier()
        self.uses = []

    def render(self):
        args = ", ".join(random_identifier() for i in range(self.num_args))
        return """
def %s(%s):
    %s()
    return %s
""" % (self.name, args, random_identifier(), random_literal())

def random_program():
    return FakeFunc().render()

def save_random_program():
    with open("output.py", "w") as f:
        f.write("".join(random_program()))

if __name__ == "__main__":
    print save_random_program()
    py_compile.compile('output.py')
