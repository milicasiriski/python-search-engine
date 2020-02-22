class Or:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return "Or(" + str(self.left) + ", " + str(self.right) + ")"

    def evaluate(self, trie, global_set):
        if isinstance(self.left, str):
            found, left = trie.search(self.left)  # u projektu ce se ovde pozivati pretraga
        else:
            left = self.left.evaluate(trie, global_set)
        if isinstance(self.right, str):
            found, right = trie.search(self.right) # u projektu ce se ovde pozivati pretraga
        else:
            right = self.right.evaluate(trie, global_set)

        return left | right


class And:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return "And(" + str(self.left) + ", " + str(self.right) + ")"

    def evaluate(self, trie, global_set):
        if isinstance(self.left, str):
            found, left = trie.search(self.left)  # u projektu ce se ovde pozivati pretraga
        else:
            left = self.left.evaluate(trie, global_set)
        if isinstance(self.right, str):
            found, right = trie.search(self.right)  # u projektu ce se ovde pozivati pretraga
        else:
            right = self.right.evaluate(trie, global_set)

        return left & right


class Not:
    def __init__(self, child):
        self.child = child

    def __str__(self):
        return "Not(" + str(self.child) + ")"

    def evaluate(self, trie, global_set):
        if isinstance(self.child, str):
            found, child = trie.search(self.child)  # u projektu ce se ovde pozivati pretraga
        else:
            child = self.child.evaluate(trie, global_set)

        return global_set - child


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


