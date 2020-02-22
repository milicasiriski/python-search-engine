class Or:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return "Or(" + str(self.left) + ", " + str(self.right) + ")"


class And:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return "And(" + str(self.left) + ", " + str(self.right) + ")"


class Not:
    def __init__(self, child):
        self.child = child

    def __str__(self):
        return "Not(" + str(self.child) + ")"


ir_actions = {
    "or_exp": [
        lambda _, n: n[0],
        lambda _, n: Or(n[0], n[2])
    ],

    "and_exp": [
        lambda _, n: n[0],
        lambda _, n: And(n[0], n[2])
    ],

    "not_exp": [
        lambda _, n: n[0],
        lambda _, n: Not(n[1])
    ],

    "exp": [
        lambda _, n: n[0],
        lambda _, n: n[1]
    ],

    "word": lambda _, value: str(value)
}


