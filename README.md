# CAFA beyond #
Evaluating the feasibility of expanding the scope of  protein GO prediction in Critical Assessment of Function Annotation (CAFA).
In particular, we test the suitability of:
1. Including/excluding certain GO terms, e.g. [GO:0005515 protein binding](https://www.ebi.ac.uk/QuickGO/term/GO:0005515).
2. Including prior knowledge (PK) targets with existing GO annotation for the evaluated aspect.
3. Expanding target source from a few selected model organisms to the whole [Swiss-Prot](https://www.uniprot.org/uniprot/?query=reviewed:yes), [UniRef50](https://www.uniprot.org/uniref/?query=&fil=identity:0.5), [UniRef90](https://www.uniprot.org/uniref/?query=&fil=identity:0.9), or [UniProt reference proteome](https://www.uniprot.org/uniprot/?query=proteome%3a(reference%3ayes)).
4. Including GO annotations with high-throughput experimental evidences, as well as UniProt keyword-derived IEA terms associated with experimental literature.

## Dataset ##
* UniProt 2021_02 (April 7, 2021)
* UniProt-GOA [2021-04-08](ftp://ftp.ebi.ac.uk/pub/databases/GO/goa/old/UNIPROT/goa_uniprot_all.gpa.203.gz) and [2020-06-16](ftp://ftp.ebi.ac.uk/pub/databases/GO/goa/old/UNIPROT/goa_uniprot_all.gaf.198.gz)
* Gene Ontology [2020-06-01](http://release.geneontology.org/2020-06-01/ontology/go-basic.obo)

All analysis are for new GO annotations at t1=20210408 compared to t0=20200616. For section 1, 2, and 3, experimental GO terms are defined the same as in CAFA2 to CAFA4 (EXP, IDA, IPI, IMP, IGI, IEP, TAS, IC). Inclusion of additional types of evidence will be discussed in section 4.

## 1. GO term exclusion ##

Currently, GO:0005515 "protein binding" is the only GO term considered for exclusion by CAFA. According to the [CAFA3 report](http://dx.doi.org/10.1186/s13059-019-1835-8), "Protein binding is a highly generalized function description, does not provide more specific information about the actual function of a protein, and in many cases may indicate a non-functional, non-specific binding. If it is the only annotation that a protein has gained, then it is hardly an advance in our understanding of that protein." This deletion is only for removal of MF target if "protein binding" is the only MF leaf term. It does not apply to the assessment of prediction accuracy if the selected target has other MF leaf terms in addition to "protein binding".

We calculte the number of proteins and information content (IC) for two different groups of UniProt proteins with MF terms: those with only "protein binding" and those with other MF terms.
Only proteins without prior MF annotations (i.e. NK and LK targets as defined below) are included in this table:

| MF terms                              | Number of proteins | Average IC | Total IC |
| :--:                                  | :--:               |  :--:      |  :--:    |
| GO:0005515 only                       |                    |            |          |
| At least 1 term other than GO:0005515 |                    |            |          |

## 2. Target type ##

CAFA considers two target types:
* No knowledge (NK) targets do not have any previous experimental annotation.
* Limited knowledge (LK) targets do have at least one previous experimental annotation, but not for the evaluated GO aspect.

It is of interest to check if another type of target should also be considered:
* Prior knowledge (PR) targets do have at least one previous experimental annotation for the evaluated GO aspect, but gain an unrelated or a more specific child term in the same GO aspect.

We check the number of targets in the whole UniProt-GOA with new annotations at t1=20210408, compared to t0=20200616.

| Proteins  | NK   | LK   | PK   |
| :--:      | :--: | :--: | :--: |
| MF        |      |      |      |
| BP        |      |      |      |
| CC        |      |      |      |
| All 3     |      |      |      |

## 3. Target database ##

| Database           | Number of entries | New annotations | Proteins with new annotations | Species with new annotations |
|   :--:             |  :--:             | :--:            | :--:                          | :--:                         |
| Swiss-Prot         |    564638 (0.26%) |                 |                               |                              |
| UniRref50          |  50105705 (  23%) |                 |                               |                              |
| Reference Proteome |  60181258 (  28%) |                 |                               |                              |
| UniRref90          | 133971487 (  62%) |                 |                               |                              |
| UniProt            | 214971037 ( 100%) |                 |                               |                              |


## 4. GO evidence ##

CAFA1 defined "experimental" (EXP) annotations slightly differently from subsequent CAFA rounds:

| CAFA  | Evidence codes considered             |
| :--:  | :--:                                  |
| CAFA1 | EXP, IDA,      IMP, IGI, IEP, TAS, IC |
| CAFA2 | EXP, IDA, IPI, IMP, IGI, IEP, TAS, IC |
| CAFA3 | EXP, IDA, IPI, IMP, IGI, IEP, TAS, IC |

CAFA excludes high-throughput (HTP) evidence codes, including: HTP, HDA, HMP, HGI, HEP.

| Evidence | Proteins | Terms | Annotations | Average IC per annotation | Average number of proteins per term |
| :--:     | :--:     | :--:  | :--:        |  :--:                     |  :--:                               |
| EXP      |          |       |             |                           |                                     |
| HTP      |          |       |             |                           |                                     |
| EXP+HTP  |          |       |             |                           |                                     |
