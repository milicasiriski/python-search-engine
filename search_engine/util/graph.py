class Graph:
    def __init__(self):
        self._outgoing = {}
        self._incoming = {}

    @property
    def outgoing(self):
        return self._outgoing

    @outgoing.setter
    def outgoing(self, o):
        self._outgoing = o

    @property
    def incoming(self):
        return self._incoming

    @incoming.setter
    def incoming(self, i):
        self._incoming = i

    def insert_vertex(self, filename):
        if filename not in self._outgoing:
            self._outgoing[filename] = []
        if filename not in self._incoming:
            self._incoming[filename] = []

    def insert_edge(self, origin, destination):
        self.insert_vertex(origin)
        self.insert_vertex(destination)

        found_edge = False
        for edge in self._outgoing[origin]:
            if edge == destination:
                found_edge = True
                break
        if not found_edge:
            self._outgoing[origin].append(destination)

        found_edge = False
        for edge in self._incoming[destination]:
            if edge == origin:
                found_edge = True
                break
        if not found_edge:
            self._incoming[destination].append(origin)

    def incoming_edges(self, v):
        return self._incoming[v]

    def outgoing_edges(self, v):
        return self._outgoing[v]

    def num_of_incoming(self, v):
        return len(self._incoming[v])

    def num_of_outgoing(self, v):
        return len(self._outgoing[v])
