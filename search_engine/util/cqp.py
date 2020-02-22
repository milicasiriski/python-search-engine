from parglare import Grammar, Parser

from util.intermrepr import ir_actions


class ComplexQueryParser():
    def __init__(self):
        self.grammar = Grammar.from_file("gramatika.pg")
        self.parser = Parser(self.grammar, actions=ir_actions)

    def parse(self, query):
        return self.parser.parse(query)
