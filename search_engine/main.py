import os
from datetime import datetime

from search_engine.util.parserHTML import Parser
from search_engine.util.trie import Trie

t = Trie()


def main():

    path = "C:\\Users\\Luka Doric\\Desktop\\python-2.7.7-docs-html"  # IZMENITI PUTANJU!

    print("Starting search engine \n")
    print("Loading files, please wait.")
    start = datetime.now()
    load_files(path)
    end = datetime.now()
    print("Vreme ucitavanja:", end - start)


def load_files(path):  # ubacivanje reci iz html fajlova
    for file_name in os.listdir(path):
        current = os.path.join(path, file_name)
        if os.path.isdir(current):
            load_files(current)
        elif file_name.endswith('.html'):
            p = Parser()
            links, words = p.parse(current)
            for word in words:
                t.add(word.lower(), current)  # ubacivanje reci u Trie stablo


main()
