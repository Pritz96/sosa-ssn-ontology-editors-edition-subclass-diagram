# SOSA/SSN Ontology (Editors Edition) Subclass Diagram

These diagrams visualise all `owl:Class` instances that are not blank nodes, as well as `owl:Class` instances that are linked to other `owl:Class` instances via `rdf:subClassOf`.

The following `rdf:subClassOf` relationship is an example of relationship that is not visualised (as sosa:Result is a subclass of something that is not an `owl:Class`):
```
sosa:Result a owl:Class ;
    rdfs:label "Result"@en ;
    rdfs:isDefinedBy sosa-common: ;
    rdfs:subClassOf [ a owl:Restriction ;
            owl:onProperty sosa:isResultOf ;
            owl:someValuesFrom sosa:Execution ] ;
    owl:deprecated true ;
    skos:definition """
  outcome of an Observation, Actuation, or act of Sampling. 
```

## SOSA
![SOSA Subclass Diagram](https://raw.githubusercontent.com/Pritz96/sosa-ssn-ontology-editors-edition-subclass-diagram/refs/heads/main/sosa_diagram.svg)


## SOSA/SSN
![SOSA/SSN Subclass Diagram](https://raw.githubusercontent.com/Pritz96/sosa-ssn-ontology-editors-edition-subclass-diagram/refs/heads/main/sosa_ssn_diagram.svg)