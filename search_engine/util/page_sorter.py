from functools import total_ordering


@total_ordering
class Page:
    def __init__(self, path, rank):
        self._path = path
        self._rank = rank

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, p):
        self._path = p

    @property
    def rank(self):
        return self._rank

    @rank.setter
    def rank(self, r):
        self._rank = r

    def __eq__(self, other):
        return self.rank == other.rank

    def __lt__(self, other):
        return self.rank < other.rank


# metoda koja formira minheap
def heapify(arr, n, i):
    smallest = i  # Inicijalizacija korena
    left_child = 2 * i + 1  # odredjivanje indeksa levog deteta
    right_child = 2 * i + 2  # odredjivanje indeksa desnog deteta

    # Da li postoji levo dete korena i da li je ono manje od korena
    if left_child < n and arr[i] > arr[left_child]:
        smallest = left_child

    # Da li postoji desno dete korena i da li je ono manje od korena i levog deteta
    if right_child < n and arr[smallest] > arr[right_child]:
        smallest = right_child

    # zameniti mesta korenu i najmanjem ukoliko je potrebno
    if smallest != i:
        arr[i], arr[smallest] = arr[smallest], arr[i]  # swap

        # Ukoliko je doslo do zamene rekurzivno se poziva metoda
        # kako bi podstablo u kom je uradjena zamena takodje bilo u dobrom poretku
        heapify(arr, n, smallest)


# Glavna funkcija za sortiranje
def heapSort(arr):
    n = len(arr)

    # Napravi minheap
    for i in range(n, -1, -1):
        heapify(arr, n, i)

    # ukloni elemente iz heap-a jedan po jedan
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]  # swap
        heapify(arr, i, 0)