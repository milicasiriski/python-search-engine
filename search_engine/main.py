import os
from datetime import datetime

from util.graph import Graph
from util.parserHTML import Parser
from util.rank_calculator import RankValues
from util.set import MySet
from util.trie import Trie

t = Trie()
g = Graph()
all_files = MySet()




def main():

    path = "C:\\Users\\Luka Doric\\Desktop\\python-2.7.7-docs-html"  # IZMENITI PUTANJU!
    # path = "C:\\Users\\Milica\\Desktop\\python-2.7.7-docs-html"

    print("Starting search engine \n")
    print("Loading files, please wait.")
    start = datetime.now()
    load_files(path)
    end = datetime.now()
    print("Vreme ucitavanja:", end - start)

    for file in g.outgoing:
        all_files.add(file)

    while True:

        choice_menu_one = input ("Za pretragu .html dokumenata unesite Y/y\n"
                                 "za izlazak iz programa unesit X/x.\n")

        if choice_menu_one.lower() == "x":
            break
        elif choice_menu_one.lower() == "y":

            while True:

                choice_menu_two = input ("Za pretragu jedne reci unesite A/a\n"
                                         "Za pretragu vise reci odvojene razmakom unesite B/b\n"
                                         "Za pretragu dve reci odvojenih sa AND/OR/NOT unesite C/c\n"
                                         "Za povratak na prethodni meni unesite X/x\n")

                if choice_menu_two.lower() == "x":
                    break

                if choice_menu_two.lower() == "a":
                    search_word = input("Unesite rec koju zelite da pretrazite:\n")  # osnovna pretraga sa jednom reci

                    length_check = search_word.split()
                    if len(length_check) != 1:
                        print("Neispravan unos!")
                        continue

                    search_word = search_word.strip()

                    found, files = t.search(search_word.lower())

                    if found:
                        calculate_ranks(files)
                        for f in files:
                            print("\n", f, files[f])

                elif choice_menu_two.lower() == "b":
                    search_text = input("Unesite reci koje zelite da pretrazite razdvojene razmakom:\n")

                    result_set = MySet()
                    search_words = search_text.split()

                    for word in search_words:
                        found, files = t.search(word.lower().strip())
                        result_set = result_set | files

                    calculate_ranks(result_set)

                    for f in result_set:
                        print("\n", f, result_set[f])

                elif choice_menu_two.lower() == "c":
                    query = input("Unesite dve reci koje zelite odvojene separatorom AND/OR/NOT:\n"
                                  "Primer unosa: word1 AND word2\n"
                                  "Operator NOT moze biti unaran\n"
                                  "Primer unosa: NOT word1\n")

                    length_check = query.split()

                    if not (len(length_check) != 2 or len(length_check) != 3):
                        print("Niste uneli ispravan format!")
                        continue

                    if len(length_check) == 2 and length_check[0] != "NOT":
                        print("Niste uneli ispravan format!")
                        continue

                    elif len(length_check) == 2 and length_check[0] == "NOT":
                        search_word = length_check[1].strip()
                        found, files = t.search(search_word.lower())
                        result_set = all_files

                        result_set = all_files - files

                        calculate_ranks(result_set)

                        for f in result_set:
                            print("\n", f, result_set[f])

                    elif len(length_check) == 3 and length_check[1] == "OR":

                        found1, files1 = t.search(length_check[0].lower().strip())
                        found2, files2 = t.search(length_check[2].lower().strip())

                        result_set = files1 | files2

                        calculate_ranks(result_set)

                        for f in result_set:
                            print("\n", f, result_set[f])

                    elif len(length_check) == 3 and length_check[1] == "NOT":

                        found1, files1 = t.search(length_check[0].lower().strip())
                        found2, files2 = t.search(length_check[2].lower().strip())

                        result_set = files1 - files2

                        calculate_ranks(result_set)

                        for f in result_set:
                            print("\n", f, result_set[f])

                    elif len(length_check) == 3 and length_check[1] == "AND":

                        found1, files1 = t.search(length_check[0].lower().strip())
                        found2, files2 = t.search(length_check[2].lower().strip())

                        result_set = files1 & files2

                        calculate_ranks(result_set)

                        for f in result_set:
                            print("\n", f, result_set[f])

                    else:
                        print("Nije ispravno unet upit."
                              " Proverite da li ste uneli separatore AND/OR/NOT velikim slovima!\n")

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


def calculate_ranks(search_results: MySet, max_iter=100):
    pages = {}  # key - putanja fajla, value - RankValues sluzi za racunanje ukupnog ranga
    total = search_results.words_in_total()  # ukupan broj reci u skupu

    # ucitavanje stranica u tabelu i postavljanje pocetnih vrednosti srazmerno broju ponavljanja reci u fajlu
    for page in g.outgoing.keys():
        if page in search_results.elements:
            value = float(search_results.elements[page] / total)
        else:
            value = 0
        pages[page] = RankValues(value)

    # racunanje ranga
    for i in range(max_iter):
        for page in pages.keys():
            if g.num_of_outgoing(page) != 0:
                value = float(pages[page].old_value / g.num_of_outgoing(page))
                for link in g.outgoing[page]:
                    pages[link].new_value += value

        for page in pages:
            pages[page].old_value, pages[page].new_value = pages[page].new_value, 0

    for page in search_results.elements:
        search_results.elements[page] = pages[page].old_value


main()
