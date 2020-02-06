import os
from datetime import datetime

from util.graph import Graph
from util.parserHTML import Parser
from util.trie import Trie

t = Trie()
g = Graph()


def main():

    path = "C:\\Users\\Luka Doric\\Desktop\\python-2.7.7-docs-html"  # IZMENITI PUTANJU!
    # path = "C:\\Users\\Milica\\Desktop\\python-2.7.7-docs-html"

    print("Starting search engine \n")
    print("Loading files, please wait.")
    start = datetime.now()
    load_files(path)
    end = datetime.now()
    print("Vreme ucitavanja:", end - start)

    while True:

        choice_menu_one = input ("Za pretragu .html dokumenata unesite Y/y\n"
                                 "za izlazak iz programa unesit X/x.\n")

        if choice_menu_one.lower() == "x":
            break
        elif choice_menu_one.lower() == "y":
            search_word = input("Unesite rec koju zelite da pretrazite:\n")  # osnovna pretraga sa jednom reci

            found, files = t.search(search_word.lower())

            if found:
                for file in files.elements:
                    print("\n", file, files.elements[file])


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
            for link in links:
                g.insert_edge(current, link)  # ubacivanje html stranica u graf


main()
