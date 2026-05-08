from rdflib import Graph, RDF, OWL, RDFS, BNode
from rdflib.namespace import split_uri

def get_label(uri):
    try:
        _, name = split_uri(uri)
        return name
    except ValueError:
        return str(uri)  # fallback for weird cases


def graph_to_puml(g: Graph, filename: str = "diagram.puml"):
    lines = ["@startuml"]

    # for classes that are a parent/child then add this relationship to the puml
    classes_with_parent_or_child = set()
    for child, _, parent in g.triples((None, RDFS.subClassOf, None)):
        if isinstance(parent, BNode):
            continue  # skip parent blank nodes
        classes_with_parent_or_child.add(child)
        classes_with_parent_or_child.add(parent)
        child_name = get_label(child)
        parent_name = get_label(parent)
        lines.append(f'"{parent_name}" <|-- "{child_name}"')

    # identify classes without a parent/child
    classes_without_parent_or_child = set()
    for cls in g.subjects((None, RDF.type, OWL.Class)):
        if cls not in classes_with_parent_or_child:
            classes_without_parent_or_child.add(cls)
    
    for x in classes_without_parent_or_child:
        lines.append(f"class {get_label(x)}")

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