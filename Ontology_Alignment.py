# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import rdflib
from owlready2 import *
from rdflib import Graph, RDF, Namespace
from rdflib.namespace import OWL, URIRef
from saving_manager import Manager

class Ontology_Alignment(object):

    def __init__(self, uri_file, uri_file_2):
        self.uri_file = uri_file
        self.uri_file_2 = uri_file_2
        self.graph = Graph()


    def getClasses(self,ontologies):
        onto_1, onto_2 = ontologies
        ontologies = (list(onto_1.classes()), list(onto_2.classes()))
        return ontologies
    def getdataProp(self,ontologies):
        onto_1,onto_2 = ontologies
        ontologies = (list(onto_1.data_properties()), list(onto_2.data_properties()))
        return ontologies
    def getobjectProp(self,ontologies):
        onto_1,onto_2 = ontologies
        ontologies = (list(onto_1.object_properties()), list(onto_2.object_properties()))
        return ontologies
    def getInd(self,ontologies):
        onto_1, onto_2 = ontologies
        ontologies = (list(onto_1.individuals()), list(onto_2.individuals()))
        return ontologies

    def allEntities(self, ontologies):

        a, b = self.getClasses(ontologies), self.getdataProp(ontologies)
        c, d = self.getobjectProp(ontologies), self.getInd(ontologies)
        return [a, b, c, d]
    def load_n_compare(self):
        graph = self.graph
        tp = 0
        fp = 0
        fn = 0
        onto1 = get_ontology(self.uri_file).load()
        onto2 = get_ontology(self.uri_file_2).load()
        entities = self.allEntities((onto1, onto2))
        pizza_res_uri = onto1.get_base_iri()
        pizza_uri = onto2.get_base_iri()
        graph.bind("res", Namespace(pizza_res_uri))
        graph.bind("pizza", Namespace(pizza_uri))

        for i,en in enumerate(entities):
            for x in en[0]:
                for y in en[1]:
                    temp = str(x).split(".")
                    temp_1 = str(y).split(".")
                    print("temp 1 {}       temp 2 {}".format(temp[1], temp_1[1]))
                    if temp[1] == temp_1[1]:
                      #  print("pizza: {} pizza-rstaurant: {}".format(x, y))
                        tp += 1
                        print("true positive {}".format(tp))
                        subject = URIRef(pizza_res_uri+temp[1])
                        object = URIRef(pizza_uri+temp_1[1])
                        if i == 0:
                            graph.add((subject, OWL.equivalentClass, object))
                        if i == 1:
                            graph.add((subject, OWL.equivalentProperty, object))
                        if i == 2:
                            graph.add((subject, OWL.equivalentProperty, object))
                        if i == 3:
                            graph.add((subject, OWL.equivalentProperty, object))
                    else:
                        fp += 1


        for en in entities:
            for x in en[1]:
                for y in en[0]:
                    temp = str(x).split(".")
                    temp_1 = str(y).split(".")
                    if not temp[1] == temp_1[1]:
                        fn += 1

        precision = tp / (tp + fp)
        recall = tp / (tp + fn)
        f_score = (2 * precision * recall) / (precision + recall)
        print(tp)
        print(fp)
        print(fn)
        print("Comparing '" + self.uri_file + "' with '" + self.uri_file_2)
        print("\tPrecision: " + str(precision))
        print("\tRecall: " + str(recall))
        print("\tF-Score: " + str(f_score))
        print(graph.serialize(format="ttl"))

    def save(self):
        manage = Manager("cw_onto_align.owl", "cw_onto_align_reason.owl", self.graph)
        manage.saveGraph()




