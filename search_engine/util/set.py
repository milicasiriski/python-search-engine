from util.page_sorter import Page


class MySet:
    def __init__(self):
        self._elements = {}  # key - putanja fajla, value - broj ponavljanja reci u fajlu

    @property
    def elements(self):
        return self._elements

    @elements.setter
    def elements(self, elements):
        self._elements = elements

    # O(1)
    def add(self, element, value=1):
        if element not in self.elements:
            self._elements[element] = value

    # n1 broj elemenata u prvom skupu, n2 broj elemenata u drugom skupu
    # O(n1 + n2)
    def __or__(self, other):
        result_set = MySet()

        for element in self:
            if element not in other:
                result_set.add(element, self[element])
            else:
                result_set.add(element, self[element] + other[element])

        for element in other:
            if element not in self:
                result_set.add(element, other[element])

        return result_set

    # n1 broj elemenata u prvom skupu, n2 broj elemenata u drugom skupu
    # O(min(n1, n2))
    def __and__(self, other):
        result_set = MySet()

        # proveravamo velicine skupova kako bismo iterirali po manjem
        if len(self.elements) < len(other.elements):
            set1 = self
            set2 = other
        else:
            set1 = other
            set2 = self

        for element in set1.elements:
            if element in set2.elements:
                result_set.add(element, set1.elements[element] + set2.elements[element])

        return result_set

    # n1 broj elemenata u prvom skupu, n2 broj elemenata u drugom skupu
    # O(n1)
    def __sub__(self, other):
        result_set = MySet()

        for element in self.elements:
            if element not in other.elements:
                result_set.add(element, self.elements[element])

        return result_set

    # n - broj elemenata u skupu
    # O(n)
    # Koliko puta se rec ukupno ponavlja unutar skupa
    def words_in_total(self):
        return sum(self.elements.values())

    def union(self, other):
        return self | other

    def intersect(self, other):
        return self & other

    def minus(self, other):
        return self - other

    def __len__(self):
        return len(self.elements)

    def __getitem__(self, item):
        return self.elements[item]

    def __setitem__(self, key, value):
        self.elements[key] = value

    def __iter__(self):
        return iter(self.elements)

    def __reversed__(self):
        return reversed(self.elements)

    def __contains__(self, item):
        return item in self.elements

    def words_in_total(self):
        return sum(self.elements.values())

    def __repr__(self):
        return repr(self.elements)

    def __str__(self):
        return str(self.elements)

    def toList(self):
        list_repr = []
        for element in self:
            list_repr.append(Page(element, self[element]))

        return list_repr

