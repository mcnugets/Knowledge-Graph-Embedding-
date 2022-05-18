from Ontology_Alignment import Ontology_Alignment
from Main_Ontology import Ontology
from queries import Query


if __name__ == '__main__':
    pizza_res = "pizza-restaurants-ontology.ttl"
    dataset = "IN3067-INM713_coursework_data_pizza_500.csv"
    my_onto = Ontology(dataset, pizza_res)
    my_onto.rdf_creation()
    my_onto.save()

    pizza_restaurant = "pizza-restaurants-ontology.owl"
    pizza = "pizza.owl"
    alignment = Ontology_Alignment(pizza_restaurant, pizza)
    alignment.load_n_compare()
    alignment.save()
#-------QUERIES
    q = Query("cw_ontology_reason.owl")
    q.performSPARQLQuery_1("queries/hawaiianPizza.csv")
    q.performSPARQLQuery_2("queries/avgPriceTomato.csv")
    q.performSPARQLQuery_3("queries/numRestaurants.csv")
    q.performSPARQLQuery_4("queries/avPizzaPrice.csv")
    q.performSPARQLQuery_5("queries/noPrice.csv")