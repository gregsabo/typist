import py_compile
import random
import string

with open("/usr/share/dict/words", "r") as f:
    WORDS = f.readlines()

with open("/usr/share/dict/connectives", "r") as f:
    CONNECTIVES = f.readlines()

SOFTWARE_PREFIXES = ("is", "num", "count")

def random_identifier():
    if random.random() > 0.5:
        return random.choice(WORDS).strip().lower()

    i = random.choice(CONNECTIVES).strip()
    if random.random() < 0.2:
        i = random.choice(SOFTWARE_PREFIXES)
    i = i + "_"
    i = i + random.choice(WORDS).strip()
    return i.lower()

ri = random_identifier

def random_literal():
    choice = random.randint(0, 2)
    if choice is 0:
        return str(random.randint(0, 100))
    if choice is 1:
        return "\"%s\"" % random_identifier()
    if choice is 2:
        return random.choice(["True", "False"])

def random_value(depth=1):
    rv = random_value
    choices = (0, 1, 2, 3, 4, 5)
    if depth >= 3:
        choices = (0, 1)

    choice = random.choice(choices)
    if choice is 0:
        return random_literal()
    if choice is 1:
        return "%s()" % random_identifier()
    if choice is 2:
        return "(%s and %s)" % (rv(depth+1), rv(depth+1))
    if choice is 3:
        return "(%s or %s)" % (rv(depth+1), rv(depth+1))
    if choice is 4:
        return "%s(%s)" % (random_identifier(), rv(depth+1))
    if choice is 5:
        return "%s(%s, %s=%s)" % (random_identifier(), rv(depth+1), random_identifier(), rv(depth+1))

def random_statement(indent=1):
    pad = "    " * indent

    choice = random.randint(0, 3)
    if choice is 0 or indent >= 3:
        return "%s%s = %s" % (pad, random_identifier(), random_value())

    if choice is 1:
        return """%sif %s:
%s
%selse:
%s""" % (
        pad, random_identifier(),
        random_statement(indent+1),
        pad,
        random_statement(indent+1))

    if choice is 2:
        return "%s%s()" % (pad, random_identifier())
    if choice is 3:
        return """%sfor %s in %s:
%s""" % (
        pad, random_identifier(),
        random_value(indent+1),
        random_statement(indent+1))

class Cursor(object):
    def __init__(self):
        self.indent_levels = 0


class FakeFunc(object):
    def __init__(self, scope):
        self.scope = scope
        self.num_args = random.randint(0, 3)
        self.name = random_identifier()
        self.uses = []

    def render(self):
        args = ", ".join(random_identifier() for i in range(self.num_args))
        body = "\n".join(random_statement() for i in range(random.randint(0, 5)))
        return """def %s(%s):
%s
    return %s

""" % (self.name, args, body, random_value())

def random_program():
    scope = []
    for i in range(100):
        scope.append(FakeFunc(scope))
    return "\n".join(f.render() for f in scope)

def save_random_program():
    with open("output.py", "w") as f:
        f.write("".join(random_program()))

if __name__ == "__main__":
    print save_random_program()
    py_compile.compile('output.py')
