from rdflib import Graph, RDFS, BNode
from rdflib.namespace import split_uri

def get_label(uri):
    try:
        _, name = split_uri(uri)
        return name
    except ValueError:
        return str(uri)  # fallback for weird cases


def graph_to_puml(g: Graph, filename: str = "diagram.puml"):
    lines = ["@startuml"]

    for child, _, parent in g.triples((None, RDFS.subClassOf, None)):
        if isinstance(parent, BNode):
            continue  # skip parent blank nodes
        child_name = get_label(child)
        parent_name = get_label(parent)
        lines.append(f'"{parent_name}" <|-- "{child_name}"')

    lines.append("@enduml")

    puml = "\n".join(lines)

    with open(filename, "w", encoding="utf-8") as f:
        f.write(puml)

    return filename

sosa = Graph()
sosa.parse(
    "https://raw.githubusercontent.com/Pritz96/ontology-library/refs/heads/main/serialised-ontologies/sosa-editors-edition.ttl",
    format="turtle"
)
graph_to_puml(sosa, "sosa_diagram.puml")

sosa_ssn = Graph()
sosa_ssn.parse(
    "https://raw.githubusercontent.com/Pritz96/ontology-library/refs/heads/main/serialised-ontologies/sosa-ssn-editors-edition.ttl",
    format="turtle"
)
graph_to_puml(sosa_ssn, "sosa_ssn_diagram.puml")