import logging
import string

import rdflib
import sys
sys.path.append("../")
from rdflib import URIRef, BNode, Literal, Namespace, Graph
from rdflib.namespace import FOAF, DCTERMS, XSD, RDF, SDO, OWL, RDFS
import csv
import pandas as pd
import owlrl
import re
from saving_manager import Manager

class Ontology(object):

    def __init__(self, dataset,parse_d):
        self.dataset = dataset
        self.we_check = pd.read_csv(dataset)
        self.graph = Graph()
        # for later---------------------------------------
        self.graph.parse(parse_d)
        self.uri = "http://www.semanticweb.org/in3067-inm713/restaurants#"
        # if true

        self.cw_uri = Namespace(self.uri)
        self.graph.bind("cw", self.cw_uri)

        self.df = pd.DataFrame(self.we_check)



    def relevant_cleaning(self, subject,  object):
        subject = str(subject)
        object = str(object)
        if subject == "nan":
            subject = " "
        if object == "nan":
            object = " "
        subject = subject.replace(" ", "")
        object = object.replace(" ", "")
        subject = re.sub(r'[^\w]', '', subject)
        object = re.sub(r'[^\w]', '', object)
        return subject,object

    def ayo(self,value):
        value = str(value)
        value = value.split(',')
        temp = []
        for s in value:
            a = s.split('and')
            for aa in a:
                temp.append(aa)
        return temp


    def clean_row(self,subject_col,object_col):
        bob = []
        for subject, object in zip(self.df[subject_col], self.df[object_col]):
            subject, object = str(subject), str(object)
            if ',' in object:
                o = self.ayo(object)
            else:
                o = [object]

            if ',' in subject:
                s = subject.split(',')
            else:
                s = [subject]

            for x in s:
                for y in o:
                    x, y = self.relevant_cleaning(x, y)
                    if (x, y) not in bob:
                        bob.append((x, y))
        return bob




    def tuple_relationships(self,subject_col, object_col):
        relations = []

        for subject,object in zip(self.df[subject_col], self.df[object_col]):

            subject,object = self.relevant_cleaning(subject,object)
            if subject == "" or object == "":  #maybe change in the future as it may collide with some issues
                continue

            if (subject, object) not in relations:
                relations.append((subject, object))
        return relations

    def create_property(self,subject, object):
        self.graph.add((subject, RDF.type, object))

    def object_creation(self,subject_object, predicate):
        object_triple = []
        for subject, object in subject_object:
            object_triple.append((URIRef(self.cw_uri+subject), predicate, URIRef(self.cw_uri+object)))

        self.create_property(predicate, OWL.ObjectProperty)
        return object_triple

    def type_creation(self, tuple_argument_list):
        triple_creation = []
        for L in tuple_argument_list:
            a, b = L
            triple_creation.append((URIRef(self.cw_uri+a), RDF.type, URIRef(self.cw_uri+b)))
        return triple_creation

    #literal creation
    def literal_creatioin(self,subject_column, predicate, datatype):
        triple_literal = []
        for a,b in subject_column:
            literal = Literal(b, datatype=datatype)
            triple_literal.append((URIRef(self.cw_uri+a), predicate,literal))

        self.create_property(predicate, OWL.DatatypeProperty)
        return triple_literal


    def for_shortened(self,packed_arrays):
        for unpack in packed_arrays:
            for s in unpack:
                self.graph.add(s)


    def type_create(self,subject_col, class_type):
        return_arr = []
        temp = []
        if subject_col == "item description":
            for x in self.df[subject_col]:
                spt = self.ayo(x)
                for y in spt:
                    temp.append(y)
        else:
            temp = self.df[subject_col].tolist()
        for subjects in temp:
            subjects, empty = self.relevant_cleaning(subjects, "")
            return_arr.append((URIRef(self.cw_uri+subjects), RDF.type, class_type))
        self.create_property(class_type, OWL.Class)
        return return_arr

    def rdf_creation(self):
        # RESTAURANT
        cw_uri = self.cw_uri
        res_type = self.type_create("name", cw_uri.Restaurant)
        res_type_cat = self.type_creation(self.clean_row("name", "categories"))
        res_object_address = self.object_creation(self.tuple_relationships("name", "address"), cw_uri.locatedInAddress)
        res_object_menuitem = self.object_creation(self.tuple_relationships("name", "menu item"), cw_uri.servesMenuItem)
        res_literal = self.literal_creatioin(self.tuple_relationships("name", "name"), cw_uri.restaurantName, XSD.string)
        self.for_shortened([res_type, res_type_cat, res_object_address, res_object_menuitem, res_literal])
        # MENU
        menu_type = self.type_create("menu item", cw_uri.MenuItem)
        menu_item = self.object_creation(self.clean_row("menu item", "item description"), cw_uri.hasIngredient)
        menu_served = self.object_creation(self.clean_row("menu item", "name"), cw_uri.servedInRestaurant)
        menu_value = self.object_creation(self.clean_row("menu item", "item value"), cw_uri.hasValue)
        menu_literal = self.literal_creatioin(self.tuple_relationships("menu item", "menu item"), cw_uri.ItemName, XSD.string)
        self.for_shortened([menu_type, menu_item, menu_served, menu_value, menu_literal])
        # ITEM VALUE
        item_value = self.type_create("item value", cw_uri.ItemValue)
        itemvalue_ob = self.object_creation(self.tuple_relationships("item value", "currency"), cw_uri.amountCurrency)
        itemvalue_literal = self.literal_creatioin(self.tuple_relationships("item value", "item value"), cw_uri.amount,XSD.double)
        self.for_shortened([item_value, itemvalue_ob, itemvalue_literal])
        # ADDRESS
        add_type = self.type_create("address", cw_uri.Address)
        add_object = self.object_creation(self.tuple_relationships("address", "city"), cw_uri.locatedInCity)
        add_literal1 = self.literal_creatioin(self.tuple_relationships("address", "postcode"), cw_uri.postCode, XSD.string)
        add_literal2 = self.literal_creatioin(self.tuple_relationships("address", "address"), cw_uri.firstLineAddress, XSD.string)
        self.for_shortened([add_type,add_object, add_literal1, add_literal2])
        # CITY
        city_type = self.type_create("city", cw_uri.City)
        city_object = self.object_creation(self.tuple_relationships("city","country"), cw_uri.locatedInCountry)
        city_object_1 = self.object_creation(self.tuple_relationships("city","state"), cw_uri.locatedInState)
        self.for_shortened([city_type, city_object, city_object_1])

        # STATE
        state_type = self.type_create("state", cw_uri.State)
        state_object = self.object_creation(self.tuple_relationships("state", "country"), cw_uri.locatedInCountry)
        self.for_shortened([state_type, state_object])
        # INGREDIENTS
        ingred = self.type_create("item description", cw_uri.Ingredient)
        self.for_shortened([ingred])

    def save(self):
        manage = Manager("cw_ontology.owl", "cw_ontology_reason.owl", self.graph)
        manage.saveGraph()


    #----------------------------------------QUERIES--------------------------------------------------------------------------


