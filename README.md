# CAFA beyond #
Evaluating the feasibility of expanding the scope of protein GO annotation in Critical Assessment of Function Annotation (CAFA).
In particular, we test the suitability of:
1. Including/excluding certain GO terms, e.g. [GO:0005515 protein binding](https://www.ebi.ac.uk/QuickGO/term/GO:0005515).
2. Including prior knowledge (PK) targets with existing GO annotation for the evaluated aspect.
3. Expanding target source from a few selected model organisms to the whole [Swiss-Prot](https://www.uniprot.org/uniprot/?query=reviewed:yes), [UniRef50](https://www.uniprot.org/uniref/?query=&fil=identity:0.5), [UniRef90](https://www.uniprot.org/uniref/?query=&fil=identity:0.9), or [UniProt reference proteome](https://www.uniprot.org/uniprot/?query=proteome%3a(reference%3ayes)).
4. Including GO annotations with high-throughput experimental evidences, as well as UniProt keyword-derived IEA terms associated with experimental literature.

## Dataset ##
* UniProt 2021_02 (April 7, 2021)
* UniProt-GOA [2021-04-08](ftp://ftp.ebi.ac.uk/pub/databases/GO/goa/old/UNIPROT/goa_uniprot_all.gpa.203.gz) and [2020-06-16](ftp://ftp.ebi.ac.uk/pub/databases/GO/goa/old/UNIPROT/goa_uniprot_all.gaf.198.gz)
* Gene Ontology [2020-06-01](http://release.geneontology.org/2020-06-01/ontology/go-basic.obo)

Unless mentioned otherwise, all analysis are for new GO annotations at t1=20210408 compared to t0=20200616. For section 1, 2, and 3, experimental GO terms are defined the same as in CAFA2 to CAFA4 (EXP, IDA, IPI, IMP, IGI, IEP, TAS, IC). Inclusion of additional types of evidence will be discussed in section 4. Information content (IC) of a term is calculated using annotations at t0 with evidence codes EXP, IDA, IPI, IMP, IGI, IEP, TAS, IC, excluding MF annotations where GO:0005515 "protein binding" is the only leaf term.

## [1. GO term exclusion](1_exclude_protein_binding/) ##

Currently, GO:0005515 "protein binding" is the only GO term considered for exclusion by CAFA. According to the [CAFA3 report](http://dx.doi.org/10.1186/s13059-019-1835-8), "Protein binding is a highly generalized function description, does not provide more specific information about the actual function of a protein, and in many cases may indicate a non-functional, non-specific binding. If it is the only annotation that a protein has gained, then it is hardly an advance in our understanding of that protein." This deletion is only for removal of MF target if "protein binding" is the only MF leaf term. It does not apply to the assessment of prediction accuracy if the selected target has other MF leaf terms in addition to "protein binding".

We calculte the number of proteins and IC for two different groups of UniProt proteins with MF terms: those with only "protein binding" and those with other MF terms.
Only proteins without any prior MF annotations are included in this table.
Unlike the following sections, IC in this section is calculated using all proteins annotated at t0, including those with "protein binding" as the only MF term.

| MF target group                | Number of proteins | Average IC per protein | Total IC  |
| :--:                           |  :--:              |  :--:                  |  :--:     |
| "protein binding"-only targets |  1091              |  0.474                 |   517.388 |
| Other targets                  |  1415              |  8.565                 | 12118.955 |

As shown in the above table, whether or not "protein binding" exclusion must be applied depends on the evaluation metric.
For non-IC-based evaluation metrics, e.g. precision-recall and Fmax, "protein binding"-only targets must be excluded as they would have account for 43.5% of all MF targets.
For IC-weighted evaluation metrics. e.g. MI-RU and Smin, removal of "protein binding"-only target is optional (but probably still advantageous), as they account for only 4.1% of total IC of all MF targets. An IC differences of 4.1% is large enough to affect the ranking of different predictors. In [CAFA3](https://genomebiology.biomedcentral.com/articles/10.1186/s13059-019-1835-8/figures/4), for example, the first and second ranked predictor only differs by ~3% in terms of Smin for MF prediction. Therefore, in the following section, we will not consider the MF aspect annotated if "protein binding" is the only leaf term.

## 2. Target type ##

CAFA considers two target types:
* No knowledge (NK) targets do not have any previous experimental annotation.
* Limited knowledge (LK) targets do have at least one previous experimental annotation, but not for the evaluated GO aspect.

When defining NK/LK targets, the "protein binding" term is not considered a previous annotation.
It is of interest to check if another type of target should also be considered:
* Prior knowledge (PK) targets do have at least one previous experimental annotation for the evaluated GO aspect, but gain an unrelated or a more specific child term in the same GO aspect.

We check the number of targets (average per-target IC) in the whole UniProt-GOA with new annotations at t1=20210408, compared to t0=20200616. When calculating IC for PK targets, only newly annotated terms are considered.

| Proteins  |      NK       |      LK       |     PK        |
| :--:      |     :--:      |     :--:      |     :--:      |
| MF        |  958  (8.609) |  809  (7.316) | 1708  (4.186) |
| BP        | 1386 (14.960) |  365 (14.937) | 4266 (10.444) |
| CC        | 1372  (5.516) |  335  (5.103) | 2085  (4.532) |
| All 3     | 3716  (9.836) | 1509  (8.668) | 8059  (7.588) |

For the "All 3" row above, if a protein is a target in more than one Aspect, it is counted more than once.
As shown in the above table, most (60%) new annotations are on PK targets with old (and shallower) annotations.
The lower but non-trivial average IC for PK targets suggest that while PK targets might be easier to predict that NK and LK targets, they are nontheless not trivial to predict.

## 3. Target database ##

We check, for the five subsets of UniProt (Swiss-Prot proteins from CAFA-selected species, Swiss-Prot, UniRef50, UniProt reference proteome, UniRef90), the coverage of NK/LK/PK targets.
In the following table, the number of NK+LK+PK targets is larger than the number of proteins with new annotations. This is because, from a CAFA perspective, a single protein with new annotations in more than one GO Aspects is counted as more than one targets.

| Database           | Number of entries | Proteins with new terms | Species with new annotations | NK targets  | LK targets  | PK targets  |
|   :--:             |  :--:             | :--:                    | :--:                         | :--:        | :--:        | :--:        |
| CAFA4              |     97999 (0.05%) | 6666   (65%)            |  15   (4%)                   |  945  (25%) | 1114  (74%) | 6485  (80%) |
| Swiss-Prot         |    564638 (0.26%) | 7803   (76%)            | 339  (88%)                   | 2197  (59%) | 1208  (80%) | 6925  (86%) |
| UniRref50          |  50105705   (23%) | 6840   (67%)            | 261  (67%)                   | 1945  (52%) | 1097  (73%) | 5942  (74%) |
| Reference Proteome |  60181258   (28%) | 9211   (90%)            | 149  (39%)                   | 2782  (75%) | 1436  (95%) | 7548  (94%) |
| UniRref90          | 133971487   (62%) | 8238   (80%)            | 320  (83%)                   | 2697  (73%) | 1297  (86%) | 6820  (85%) |
| UniProt            | 214971037  (100%) | 10270 (100%)            | 387 (100%)                   | 3716 (100%) | 1509 (100%) | 8059 (100%) |

While the CAFA4 dataset already includes the majority (65%) of proteins with new terms, especially LK targets (74%) and PK targets (80%), it only covers a relative small fractions (25% and 4% respectively) of NK targets and species with new annotations. Expansion of CAFA4 dataset to the whole Swiss-Prot and/or UniProt Reference Proteome is needed for more comprehesive assessment of NK targets in more diverse species.

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

## License ##

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 2 of the License, or (at your option) any later
version.
