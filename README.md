# CAFA beyond #
Evaluating the feasibility of expanding the scope of GO prediction in Critical Assessment of Function Annotation (CAFA).
In particular, we test the suitability of:
1. Including/excluding certain GO terms, e.g. [GO:0005515 protein binding](https://www.ebi.ac.uk/QuickGO/term/GO:0005515).
2. Including GO annotations with high-throughput experimental evidences, as well as UniProt keyword-derived IEA terms associated with experimental literature.
3. Expanding target source from a few selected model organisms to the whole [Swiss-Prot](https://www.uniprot.org/uniprot/?query=reviewed:yes), [UniRef50](https://www.uniprot.org/uniref/?query=&fil=identity:0.5), [UniRef90](https://www.uniprot.org/uniref/?query=&fil=identity:0.9), [UniRef100](https://www.uniprot.org/uniref/?query=&fil=identity:1.0), or [UniProt reference proteome](https://www.uniprot.org/uniprot/?query=proteome%3a(reference%3ayes)).
4. Including prior knowledge (PK) targets with existing GO annotation for the evaluated aspect.

## Dataset ##
1. UniProt 2021_02 (April 7, 2021)
2. UniProt-GOA [2021-04-08](ftp://ftp.ebi.ac.uk/pub/databases/GO/goa/old/UNIPROT/goa_uniprot_all.gpa.203.gz) and [2020-06-16](ftp://ftp.ebi.ac.uk/pub/databases/GO/goa/old/UNIPROT/goa_uniprot_all.gaf.198.gz)
3. Gene Ontology [2020-06-01](http://release.geneontology.org/2020-06-01/ontology/go-basic.obo)
