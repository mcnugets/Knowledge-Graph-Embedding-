from rdflib.util import guess_format
import owlrl


class Manager(object):
    def __init__(self, file, reasoner_file, graph):
        self.file = file
        self.reasoner_file = reasoner_file
        self.graph = graph

    def saveGraph(self):
        # SAVE/SERIALIZE GRAPH
        # print(self.g.serialize(format="turtle").decode("utf-8"))
        self.graph.serialize(destination=self.file, format="xml")
        self.performReasoning()
        self.graph.serialize(destination=self.reasoner_file, format="xml")


    def performReasoning(self):
        # We expand the graph with the inferred triples
        # We use owlrl library with OWL2 RL Semantics (instead of RDFS semantic as we saw in lab 4)
        # More about OWL 2 RL Semantics in lecture/lab 7
        graph = self.graph
        file = self.file
        print("Data triples from CSV: '" + str(len(graph)) + "'.")

        # We should load the ontology first
        # print(guess_format(ontology_file))

        graph.load(file, format=guess_format(
            file))  # e.g., format=ttl

        print("Triples including ontology: '" + str(len(graph)) + "'.")

        # We apply reasoning and expand the graph with new triples
        owlrl.DeductiveClosure(
            owlrl.OWLRL_Semantics, axiomatic_triples=True, datatype_axioms=True).expand(graph)

        print("Triples after OWL 2 RL reasoning: '" + str(len(graph)) + "'.")






