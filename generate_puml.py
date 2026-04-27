from rdflib import Graph, RDFS
from rdflib.namespace import split_uri

def get_label(uri):
    try:
        _, name = split_uri(uri)
        return name
    except ValueError:
        return str(uri)  # fallback for weird cases

g = Graph()
# Load SOSA
g.parse("https://raw.githubusercontent.com/w3c/sdw-sosa-ssn/refs/heads/gh-pages/ssn/rdf/ontology/core/sosa-actuation.ttl", format="turtle")
g.parse("https://raw.githubusercontent.com/w3c/sdw-sosa-ssn/refs/heads/gh-pages/ssn/rdf/ontology/core/sosa-common.ttl", format="turtle")
g.parse("https://raw.githubusercontent.com/w3c/sdw-sosa-ssn/refs/heads/gh-pages/ssn/rdf/ontology/core/sosa-deprecated.ttl", format="turtle")
g.parse("https://raw.githubusercontent.com/w3c/sdw-sosa-ssn/refs/heads/gh-pages/ssn/rdf/ontology/core/sosa-observation.ttl", format="turtle")
g.parse("https://raw.githubusercontent.com/w3c/sdw-sosa-ssn/refs/heads/gh-pages/ssn/rdf/ontology/core/sosa-sampling.ttl", format="turtle")
g.parse("https://raw.githubusercontent.com/w3c/sdw-sosa-ssn/refs/heads/gh-pages/ssn/rdf/ontology/core/sosa.ttl", format="turtle")

lines = ["@startuml"]

for child, _, parent in g.triples((None, RDFS.subClassOf, None)):
    child_name = get_label(child)
    parent_name = get_label(parent)
    lines.append(f'"{parent_name}" <|-- "{child_name}"')

lines.append("@enduml")
puml= "\n".join(lines)
with open("diagram.puml", "w", encoding="utf-8") as f:
    f.write(puml)