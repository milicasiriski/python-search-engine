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
    def union(self, other):
        result_set = MySet()

        for element in self.elements:
            if element not in other.elements:
                result_set.add(element, self.elements[element])
            else:
                result_set.add(element, self.elements[element] + other.elements[element])

        for element in other.elements:
            if element not in self.elements:
                result_set.add(element, other.elements[element])

        return result_set

    # n1 broj elemenata u prvom skupu, n2 broj elemenata u drugom skupu
    # O(min(n1, n2))
    def intersect(self, other):
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
    def minus(self, other):
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
