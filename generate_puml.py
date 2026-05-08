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
        child_name = get_label(child)
        parent_name = get_label(parent)
        classes_with_parent_or_child.add(child_name)
        classes_with_parent_or_child.add(parent_name)
        lines.append(f'{parent_name} <|-- {child_name}')

    # identify classes without a parent/child and that aren't a blank node
    classes_without_parent_or_child = set()
    for cls in g.subjects(RDF.type, OWL.Class):
        if (get_label(cls) not in classes_with_parent_or_child) and not isinstance(cls,BNode):
            classes_without_parent_or_child.add(get_label(cls))
    
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