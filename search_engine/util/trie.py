from search_engine.util.set import MySet


class TrieNode:
    def __init__(self):
        self.children = {}  # mapa u sebi sadrzi kljuc(char) i value node
        self.word_finished = False  # indikator da li je rec zavrsena
        self.files = MySet()


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def add(self, word: str, file):

        node = self.root  # pozicioniranje na koren stabla
        for char in word:
            new_node = node.children.get(char)
            if new_node is None:  # ako nije pronadjen Node sa zadatim kljucen(char) pravi se novi node
                new_node = TrieNode()
                node.children[char] = new_node
            node = new_node
        node.word_finished = True  # rec je zavrsena

        if file in node.files.elements:
            node.files.elements[file] += 1  # uvecava se broj pronadjenih reci za taj fajl
        else:
            node.files.add(file)

    def search(self, word: str):

        node = self.root  # pozicioniranje na korenski cvor
        for char in word:
            child = node.children.get(char)
            if child is None:
                return False, None
            node = child

        if not node.word_finished:
            return False, None

        return True, node.files
