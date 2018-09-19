from SPARQLWrapper import SPARQLWrapper, JSON
import config

sparql = SPARQLWrapper("http://rdf.insee.fr/sparql")
sparql.setReturnFormat(JSON)

# SPARQL endpoint with pop5
sparql_pop5 = SPARQLWrapper(config.sparql_pop5_endpoint)
sparql_pop5.setReturnFormat(JSON)


def department_list():
    query = """
    PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX igeo:<http://rdf.insee.fr/def/geo#>

    SELECT ?dep ?nom ?codedep WHERE {
        ?dep rdf:type igeo:Departement .
        ?dep igeo:nom ?nom .
        ?dep igeo:codeDepartement ?codedep .
    }
    order by ?nom
    """

    sparql.setQuery(query)
    results = sparql.query().convert()

    return [{
        'label': result['nom']['value'],
        'value': result['codedep']['value']
        } for result in results["results"]["bindings"]]


def liste_communes(code_dep):
    query = f"""
    PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX igeo:<http://rdf.insee.fr/def/geo#>

    SELECT ?commune ?nom ?codecom WHERE {{
        ?commune rdf:type igeo:Commune .
        ?commune igeo:nom ?nom .
        ?commune igeo:subdivisionDe ?dep .
        ?dep igeo:codeDepartement "{code_dep}"^^xsd:token .
        ?commune igeo:codeCommune ?codecom
    }}
    """

    sparql.setQuery(query)
    results = sparql.query().convert()
    return [{
        'label': result['nom']['value'],
        'value': result['codecom']['value']
        } for result in results["results"]["bindings"]]


def activity_list(input_str):
    query = f"""
    PREFIX skos:<http://www.w3.org/2004/02/skos/core#>

    SELECT ?poste ?libelle ?notation WHERE {{
            ?poste skos:inScheme <http://id.insee.fr/codes/nafr2/naf> .
            ?poste skos:prefLabel ?libelle .
            ?poste skos:notation ?notation .
            FILTER(lang(?libelle) = 'fr') .
            FILTER(regex(?libelle, '{input_str}')) .
            }}
    """
    sparql.setQuery(query)
    results = sparql.query().convert()

    return [{
        'label': result['libelle']['value'],
        'value': result['notation']['value']
        } for result in results["results"]["bindings"]]


def population(codecom):
    query = f"""
    PREFIX idemo:<http://rdf.insee.fr/def/demo#>
    PREFIX igeo:<http://rdf.insee.fr/def/geo#>

    SELECT ?commune ?nom ?popTotale ?date WHERE {{
        ?commune igeo:codeCommune "{codecom}"^^xsd:token .
        ?commune igeo:nom ?nom .
        ?commune idemo:population ?popLeg .
        ?popLeg idemo:populationTotale ?popTotale ; idemo:date ?date .
        }}
    """
    sparql.setQuery(query)
    results = sparql.query().convert()

    return {
            'x': [result['date']['value']
                  for result in results["results"]["bindings"]],
            'y': [result['popTotale']['value']
                  for result in results["results"]["bindings"]],
            'type': 'bar',
            'name': results["results"]["bindings"][0]['nom']['value']}


def population_structure(codecom, gender):
    query = f"""
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    PREFIX measure: <http://id.insee.fr/meta/mesure/>
    PREFIX geo-dim: <http://id.insee.fr/meta/cog2017/dimension/>
    PREFIX dim: <http://id.insee.fr/meta/dimension/>

    SELECT ?areacode (sum(?pop) as ?popTotale)
    ?tactrNotation ?tactrLabel WHERE {{
        ?obs ?p <http://id.insee.fr/meta/demo/pop5/dataSet/2015-depcomarm> .
        ?obs geo-dim:DepartementOuCommuneOuArrondissementMunicipal ?area .
        ?obs measure:pop15Plus ?pop .
        ?obs dim:sexe ?sexe .
        ?obs dim:tactr ?tactr .
        ?tactr skos:notation ?tactrNotation .
        ?tactr skos:prefLabel ?tactrLabel .
        ?sexe skos:notation "{gender}" .
        ?area skos:notation ?areacode .
        FILTER(?areacode = "{codecom}")
    }}
    GROUP BY ?tactrLabel ?tactrNotation ?areacode
    """
    sparql_pop5.setQuery(query)
    results = sparql_pop5.query().convert()
    return {
            'x': [result['tactrLabel']['value']
                  for result in results["results"]["bindings"]],
            'y': [result['popTotale']['value']
                  for result in results["results"]["bindings"]],
            'type': 'bar',
            'name': results["results"]["bindings"][0]['areacode']['value']
         }


if __name__ == "__main__":
    print(population('70285'))
