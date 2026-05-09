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

    # set for all owl classes that aren't blank nodes
    all_classes = set()
    # set for owl classes that are either a child or a parent owl (related via subClassOf) class that aren't a blank node
    child_or_parent_classes = set()

    for cls in g.subjects(RDF.type, OWL.Class):
        if isinstance(cls, BNode):
            continue  # skip blank nodes
        all_classes.add(cls)
        parents = set(g.objects(cls, RDFS.subClassOf))
        for x in parents:
            if isinstance(x, BNode) or (x, RDF.type, OWL.Class) not in g:
                continue  # skip blank nodes or parents that aren't of type owl:Class
            child_or_parent_classes.update((cls, x))
            lines.append(f"{get_label(x)} <|-- {get_label(cls)}")

    # identify classes without a parent/child and that aren't a blank node
    classes_without_parent_or_child = all_classes - child_or_parent_classes

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
    format="turtle",
)
graph_to_puml(sosa, "sosa_diagram.puml")

sosa_ssn = Graph()
sosa_ssn.parse(
    "https://raw.githubusercontent.com/Pritz96/ontology-library/refs/heads/main/serialised-ontologies/sosa-ssn-editors-edition.ttl",
    format="turtle",
)
graph_to_puml(sosa_ssn, "sosa_ssn_diagram.puml")
