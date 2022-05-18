from rdflib import Graph
from rdflib.util import guess_format
class Query(object):
    def __init__(self, ttl_file):
        self.graph = Graph()
        self.graph.load(ttl_file, format=guess_format(
            ttl_file))

    def query1(self):
        qres = self.graph.query(
            """ PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                PREFIX cw: <http://www.semanticweb.org/in3067-inm713/restaurants#>
                PREFIX : <http://www.semanticweb.org/in3067-inm713/restaurants#>
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                PREFIX owl: <http://www.w3.org/2002/07/owl#>

                PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                SELECT ?Restaurant ?City ?State ?Address ?postcode ?MenuItem 
                where
                {

                    ?Restaurant cw:locatedInAddress ?Address .
                    ?Address cw:postCode ?postcode .
                    ?Restaurant cw:servesMenuItem ?MenuItem .
                    ?Address cw:locatedInCity ?City .
                    ?City cw:locatedInState ?State .
                    ?State cw:locatedInCountry ?Country .

                    FILTER(?MenuItem=cw:HawaiianPizza)
                } group by  ?Restaurant ?City ?State ?Address ?postcode ?MenuItem
        """)
        return qres

    def query2(self):
        qres = self.graph.query(
            """ PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                PREFIX cw: <http://www.semanticweb.org/in3067-inm713/restaurants#>
                PREFIX : <http://www.semanticweb.org/in3067-inm713/restaurants#>
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                PREFIX owl: <http://www.w3.org/2002/07/owl#>
                
                PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                SELECT (AVG(?amount) as ?iv)
                where
                {
                   
                    ?MenuItem cw:hasValue ?ItemValue .
                    ?MenuItem cw:hasIngredient ?Ingredient .
                    ?ItemVAlue cw:amount ?amount .
                    
                        FILTER NOT EXISTS{?Tomato rdf:type ?Ingredient}
                   
                }
        """)
        return qres

    def query3(self):
        qres = self.graph.query(
            """ PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                PREFIX cw: <http://www.semanticweb.org/in3067-inm713/restaurants#>
                PREFIX : <http://www.semanticweb.org/in3067-inm713/restaurants#>
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                PREFIX owl: <http://www.w3.org/2002/07/owl#>
                PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                SELECT ?City (count(?Restaurant) as ?num_of_Restaurants) ?State
                where
                {

                    ?Restaurant cw:locatedInAddress ?Address .
                    ?Address cw:locatedInCity ?City . 
                    ?City cw:locatedInState ?State .    
                }
                group by ?City ?State
                order by asc(?num_of_Restaurants) asc(?State)
        """)
        return qres

    def query4(self):
        qres = self.graph.query(
            """ PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                PREFIX cw: <http://www.semanticweb.org/in3067-inm713/restaurants#>
                PREFIX : <http://www.semanticweb.org/in3067-inm713/restaurants#>
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                PREFIX owl: <http://www.w3.org/2002/07/owl#>
                
                PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                SELECT ?Restaurant (AVG(?amount) as ?avg_price) ?City
                where 
                { 
                    ?Restaurant cw:servesMenuItem ?MenuItem .
                    ?MenuItem cw:hasValue ?ItemValue .
                    ?ItemValue cw:amount ?amount .
                    ?Restaurant cw:locatedInAddress ?Address .
                    ?Address cw:locatedInCity ?City .
                }
                group by ?Restaurant ?City
                order by asc(?City)
        """)
        return qres

    def query5(self):
        qres = self.graph.query(
            """ PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                PREFIX cw: <http://www.semanticweb.org/in3067-inm713/restaurants#>
                PREFIX : <http://www.semanticweb.org/in3067-inm713/restaurants#>
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                PREFIX owl: <http://www.w3.org/2002/07/owl#>

                PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                SELECT ?MenuItem ?ItemValue
                where 
                { 
                    ?MenuItem cw:servedInRestaurant ?Restaurant .
                    ?MenuITem cw:hasValue ?ItemValue .
                    FILTER(?ItemValue=cw:) .

                }
                group by ?MenuItem ?ItemValue
        """)
        return qres

    def performSPARQLQuery_1(self, file_query_out):
        # print("%s capitals satisfying the query." % (str(len(qres))))

        f_out = open(file_query_out, "w+")
        # query 1
        for row in self.query1():
            # Row is a list of matched RDF terms: URIs, literals or blank nodes
            line_str = '\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\"\n' % (
                row.Restaurant, row.City, row.State, row.Address, row.postcode, row.MenuItem)

            f_out.write(line_str)

        f_out.close()
    def performSPARQLQuery_2(self, file_query_out):
        # print("%s capitals satisfying the query." % (str(len(qres))))

        f_out = open(file_query_out, "w+")
        # query 1
        for row in self.query2():
            # Row is a list of matched RDF terms: URIs, literals or blank nodes
            line_str = '\"%s\"\n' % (
                row.iv)

            f_out.write(line_str)

        f_out.close()

    def performSPARQLQuery_3(self, file_query_out):
        # print("%s capitals satisfying the query." % (str(len(qres))))

        f_out = open(file_query_out, "w+")
        # query 1
        for row in self.query3():
            # Row is a list of matched RDF terms: URIs, literals or blank nodes
            line_str = '\"%s\",\"%s\",\"%s\"\n' % (
                row.City, row.num_of_Restaurants,row.State )

            f_out.write(line_str)

        f_out.close()

    def performSPARQLQuery_4(self, file_query_out):
        # print("%s capitals satisfying the query." % (str(len(qres))))

        f_out = open(file_query_out, "w+")
        # query 1
        for row in self.query4():
            # Row is a list of matched RDF terms: URIs, literals or blank nodes
            line_str = '\"%s\",\"%s\",\"%s\"\n' % (
                row.Restaurant, row.avg_price, row.City)

            f_out.write(line_str)

        f_out.close()


    def performSPARQLQuery_5(self, file_query_out):
        # print("%s capitals satisfying the query." % (str(len(qres))))

        f_out = open(file_query_out, "w+")
        # query 1
        for row in self.query5():
            # Row is a list of matched RDF terms: URIs, literals or blank nodes
            line_str = '\"%s\",\"%s\"\n' % (
                row.MenuItem, row.ItemValue)

            f_out.write(line_str)

        f_out.close()








