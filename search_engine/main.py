import os
from datetime import datetime

from parglare import ParseError

from util.graph import Graph
from util.page_sorter import heapSort, Page
from util.parserHTML import Parser
from util.rank_calculator import RankValues
from util.set import MySet
from util.trie import Trie

from util.cqp import ComplexQueryParser

t = Trie()
g = Graph()
all_files = MySet()


def main():
   #path = "C:\\Users\\Luka Doric\\Desktop\\python-2.7.7-docs-html"  # IZMENITI PUTANJU!
   # path = "C:\\Users\\Milica\\Desktop\\python-2.7.7-docs-html"

    while True:
        path = input("Unesite korenski direktorijum.\n")

        try:
            start = datetime.now()
            print("Starting search engine \n")
            print("Loading files, please wait.")
            load_files(path)
            end = datetime.now()
            break
        except OSError:
            print("Nije pravilno uneta putanja unesite opet!")

    print("Vreme ucitavanja: ", end - start)

    for file in g.outgoing:
        all_files.add(file)

    while True:

        choice_menu_one = input("Za pretragu .html dokumenata unesite Y/y\n"
                                "za izlazak iz programa unesite X/x.\n")

        if choice_menu_one.lower() == "x":
            break
        elif choice_menu_one.lower() == "y":

            while True:

                choice_menu_two = input("Za pretragu jedne reci unesite A/a\n"
                                        "Za pretragu vise reci odvojene razmakom unesite B/b\n"
                                        "Za pretragu dve reci odvojenih sa AND/OR/NOT unesite C/c\n"
                                        "Za kompleksnu pretragu unesite D/d\n"
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

                    search_results = calculate_ranks(files)
                    heapSort(search_results)
                    paginate(search_results)

                elif choice_menu_two.lower() == "b":
                    search_text = input("Unesite reci koje zelite da pretrazite razdvojene razmakom:\n")

                    result_set = MySet()
                    search_words = search_text.split()

                    for word in search_words:
                        found, files = t.search(word.lower().strip())
                        result_set = result_set | files

                    search_results = calculate_ranks(result_set)

                    for page in search_results:
                        contains_words = 0
                        for word in search_words:
                            _, files = t.search(word.lower().strip())
                            if page.path in files:
                                contains_words += 1
                        page.rank *= contains_words

                    heapSort(search_results)
                    paginate(search_results)

                elif choice_menu_two.lower() == "c":
                    query = input("Unesite dve reci koje zelite odvojene separatorom AND/OR/NOT:\n"
                                  "Primer unosa: word1 AND word2\n"
                                  "Operator NOT moze biti unaran\n"
                                  "Primer unosa: NOT word1\n")

                    length_check = query.split()

                    if not (len(length_check) == 2 or len(length_check) == 3):
                        print("Niste uneli ispravan format! Unos se moze sastojati samo od 2 ili 3 reci ukljucujuci i AND/OR/NOT")
                        continue

                    if len(length_check) == 2 and length_check[0].upper() != "NOT":
                        print("Niste uneli ispravan format! Ukoliko unosite dve reci prva mora biti NOT")
                        continue

                    if len(length_check) == 2 and length_check[0].upper() == "NOT":
                        search_word = length_check[1].strip()
                        found, files = t.search(search_word.lower())

                        result_set = all_files - files

                        search_results = calculate_ranks(result_set)
                        heapSort(search_results)
                        paginate(search_results)

                    elif len(length_check) == 3 and length_check[1].upper() == "OR":

                        found1, files1 = t.search(length_check[0].lower().strip())
                        found2, files2 = t.search(length_check[2].lower().strip())

                        result_set = files1 | files2
                        search_results = calculate_ranks(result_set)

                        for result in search_results:
                            if result.path in files1 and result.path in files2:
                                result.rank *= 2

                        heapSort(search_results)
                        paginate(search_results)

                    elif len(length_check) == 3 and length_check[1].upper() == "NOT":

                        found1, files1 = t.search(length_check[0].lower().strip())
                        found2, files2 = t.search(length_check[2].lower().strip())

                        result_set = files1 - files2

                        search_results = calculate_ranks(result_set)
                        heapSort(search_results)
                        paginate(search_results)

                    elif len(length_check) == 3 and length_check[1].upper() == "AND":

                        found1, files1 = t.search(length_check[0].lower().strip())
                        found2, files2 = t.search(length_check[2].lower().strip())

                        result_set = files1 & files2

                        search_results = calculate_ranks(result_set)
                        heapSort(search_results)
                        paginate(search_results)

                    else:
                        print("Nije ispravno unet upit. Proverite da li ste ispravno uneli separatore AND/OR/NOT!\n")

                elif choice_menu_two.lower() == "d":
                    print("Usli ste u naprednu pretragu! Operatori su &&/||/! takodje je dozvoljena upotreba zagradi!")
                    cqp = ComplexQueryParser()
                    complex_query = input("Kompleksan upit:\n")
                    try:
                        ir_tree = cqp.parse(complex_query)
                        print(ir_tree)
                    except ParseError:
                        print("Niste ispravno uneli kompleksan upit!")


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
    if len(search_results) == 0:
        return []
    pages = {}  # key - putanja fajla, value - RankValues sluzi za racunanje ukupnog ranga
    total = search_results.words_in_total  # ukupan broj reci u skupu
    average = search_results.words_on_average  # prosecan broj reci u skupu
    n = len(g.outgoing)
    d = 0.85  # damping factor
    # ucitavanje stranica u tabelu i postavljanje pocetnih vrednosti
    for page in g.outgoing.keys():
        pages[page] = RankValues(float(1 / total))
    # racunanje ranga
    # klasican PageRank algoritam racuna rang stranice u odnosu na broj linkova koji na nju ukazuju kao i njihove
    # "jacine"
    for i in range(max_iter):
        for page in pages.keys():
            if g.num_of_outgoing(page) != 0:
                value = float(pages[page].old_value / g.num_of_outgoing(page))
                if page in search_results:
                    value *= 1.2
                else:
                    value *= 0.8
                for link in g.outgoing[page]:
                    pages[link].new_value += value

        # d - faktor prigusenja, sprecava velike oscilacije u vrednostima
        # na novu vrednost ranga stranice dodaje se broj reci koji sadrzi ta stranica u odnosu na prosecan broj trazene
        # reci po stranici kako bi se povecao uticaj linka koji sadrzi tu rec u odnosu na linkove koji ne sadrze rec
        for page in pages:
            if page in search_results:
                pages[page].old_value = (1-d) + d*(pages[page].new_value + (search_results[page] / average))
            else:
                pages[page].old_value = (1 - d) + d * pages[page].new_value
            pages[page].new_value = 0

    final_list = []
    for page in pages:
        # konacan rang se dobija mnozenjem sa brojem ponavljanja reci u odnosu na prosecan broj ponavljanja reci kako
        # bi se uzeo u obzir uticaj samog broja reci koji sadrzi stranica
        if page in search_results:
            final_list.append(Page(page, pages[page].old_value))
    return final_list


def paginate(search_results):
    answer = ""
    curr_page = 0
    n = 10  # broj putanja koje ce se prikazati po stranici default=10
    num_of_pages = int(len(search_results) / n) + 1
    while answer.lower() != "x":

        for i in range(n):
            index = curr_page*n + i
            if index < len(search_results):
                print(search_results[i].path, search_results[index].rank)

        print("")
        print("Trenutno ste na stranici:", curr_page+1, "/", num_of_pages)
        if curr_page != 0:
            print("P - povratak na prethodnu stranicu")
        if curr_page != num_of_pages - 1:
            print("N - odlazak na sledecu stranicu")
        print("G - odlazak na zadatu stranicu")
        print("C - promena broja putanja koje se prikazuju po stranici")
        answer = input("X - povratak na meni za pretragu\n")

        if answer.lower() == "p" and curr_page != 0:
            curr_page -= 1
        elif answer.lower() == "n" and curr_page != num_of_pages-1:
            curr_page += 1
        elif answer.lower() == "g":
            while True:
                user_input = input("Unesite broj stranice koju zelite da prikazete:\n")
                try:
                    new_curr = int(user_input)
                    if new_curr <= 0 or new_curr > num_of_pages:
                        print("Stranica koju ste uneli nije dostupna.")
                    else:
                        curr_page = new_curr - 1
                        break
                except ValueError:
                    print("Neispravan unos. Molim Vas unesite prirodan broj.")

        elif answer.lower() == "c":
            while True:
                user_input = input("Unesite novi broj putanja za prikaz:\n")
                try:
                    new_n = int(user_input)
                    if new_n <= 0:
                        print("Neispravan unos. Molim Vas unesite prirodan broj.")
                    else:
                        n = new_n
                        num_of_pages = int(len(search_results) / n) + 1
                        curr_page = 0
                        break
                except ValueError:
                    print("Neispravan unos. Molim Vas unesite prirodan broj.")


main()
