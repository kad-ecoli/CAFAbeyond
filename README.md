# CAFA beyond #
Evaluating the feasibility of expanding the scope of protein GO annotation in Critical Assessment of Function Annotation (CAFA).
In particular, we test the suitability of:
1. Including/excluding certain GO terms, e.g. [GO:0005515 protein binding](https://www.ebi.ac.uk/QuickGO/term/GO:0005515).
2. Including prior knowledge (PK) targets with existing GO annotation for the evaluated aspect.
3. Expanding target source from a few selected model organisms to the whole [Swiss-Prot](https://www.uniprot.org/uniprot/?query=reviewed:yes), [UniRef50](https://www.uniprot.org/uniref/?query=&fil=identity:0.5), [UniRef90](https://www.uniprot.org/uniref/?query=&fil=identity:0.9), or [UniProt reference proteome](https://www.uniprot.org/uniprot/?query=proteome%3a(reference%3ayes)).
4. Including GO annotations with high-throughput experimental evidences, as well as UniProt keyword-derived IEA terms associated with experimental literature.
5. Implementation of alternative baseline methods.
6. Inclusion of RNA.

## Dataset ##
* UniProt 2021_02 (April 7, 2021)
* UniProt-GOA [2021-04-08](ftp://ftp.ebi.ac.uk/pub/databases/GO/goa/old/UNIPROT/goa_uniprot_all.gpa.203.gz) and [2020-06-16](ftp://ftp.ebi.ac.uk/pub/databases/GO/goa/old/UNIPROT/goa_uniprot_all.gaf.198.gz)
* Gene Ontology [2020-06-01](http://release.geneontology.org/2020-06-01/ontology/go-basic.obo)

Unless mentioned otherwise, all analysis are for new GO annotations at t1=20210408 compared to t0=20200616. For section 1, 2, and 3, experimental GO terms are defined the same as in CAFA2 to CAFA4 (EXP, IDA, IPI, IMP, IGI, IEP, TAS, IC). Inclusion of additional types of evidence will be discussed in section 4. Information content (IC) of a term is calculated using annotations at t0 with evidence codes EXP, IDA, IPI, IMP, IGI, IEP, TAS, IC.

## Run the analysis ##
This repository already include pre-generated result. If you want to reproduce the result included herein, execute the following commands:
```bash
./download.sh
./curate.sh
cd 1_exclude_protein_binding/; ./main.py > readme.md ; cd ..
cd 2_target_type/            ; ./main.py > readme.md ; cd ..
cd 3_target_database/        ; ./main.py > readme.md ; cd ..
cd 4_HTP/                    ; ./main.sh             ; cd ..
cd 5_baseline/               ; ./main.sh             ; cd ..
cd 6_RNA/                    ; ./main.sh             ; cd ..
```

## [1. GO term exclusion](1_exclude_protein_binding/) ##

Currently, GO:0005515 "protein binding" is the only GO term considered for exclusion by CAFA. According to the [CAFA3 report](http://dx.doi.org/10.1186/s13059-019-1835-8), "Protein binding is a highly generalized function description, does not provide more specific information about the actual function of a protein, and in many cases may indicate a non-functional, non-specific binding. If it is the only annotation that a protein has gained, then it is hardly an advance in our understanding of that protein." This deletion is only for removal of MF target if "protein binding" is the only MF leaf term. It does not apply to the assessment of prediction accuracy if the selected target has other MF leaf terms in addition to "protein binding".

We calculte the number of proteins and IC for two different groups of UniProt proteins with MF terms: those with only "protein binding" and those with other MF terms.
Only proteins without any prior MF annotations are included in this table.

| MF target group                | Number of proteins | Average IC per protein | Total IC  |
| :--:                           |  :--:              |  :--:                  |  :--:     |
| "protein binding"-only targets |  1091              |  0.697                 |   760.143 |
| Other targets                  |  1415              |  8.079                 | 11431.620 |

As shown in the above table, whether or not "protein binding" exclusion must be applied depends on the evaluation metric.
For non-IC-based evaluation metrics, e.g. precision-recall and Fmax, "protein binding"-only targets must be excluded as they would have account for 43.5% of all MF targets.
For IC-weighted evaluation metrics. e.g. MI-RU and Smin, removal of "protein binding"-only target is optional (but probably still advantageous), as they account for only 6.2% of total IC of all MF targets. This is an IC difference large enough to affect the ranking of different predictors. In [CAFA3](https://genomebiology.biomedcentral.com/articles/10.1186/s13059-019-1835-8/figures/4), for example, the first and second ranked predictor only differs by ~3% in terms of Smin for MF prediction. Therefore, in the following section, we will not consider the MF aspect annotated if "protein binding" is the only leaf term.

## [2. Target type](2_target_type) ##

CAFA considers two target types:
* No knowledge (NK) targets do not have any previous experimental annotation.
* Limited knowledge (LK) targets do have at least one previous experimental annotation, but not for the evaluated GO aspect.

When defining NK/LK targets, the "protein binding" term is not considered a previous annotation.
It is of interest to check if another type of target should also be considered:
* Prior knowledge (PK) targets do have at least one previous experimental annotation for the evaluated GO aspect, but gain an unrelated or a more specific child term in the same GO aspect.

We check the number of targets (average per-target IC) in the whole UniProt-GOA with new annotations at t1=20210408, compared to t0=20200616. When calculating IC for PK targets, only newly annotated terms are considered.

| Proteins  |      NK       |      LK       |      PK       |      All 3     |
| :--:      |     :--:      |     :--:      |     :--:      |      :--:      |
| MF        |  958  (8.570) |  809  (7.064) | 1708  (4.186) |  3475  (6.065) |
| BP        | 1386 (14.960) |  365 (14.937) | 4266 (10.444) |  6017 (11.757) |
| CC        | 1372  (5.516) |  335  (5.103) | 2085  (4.532) |  3792  (4.938) |
| All 3     | 3716  (9.836) | 1509  (8.668) | 8059  (7.588) | 13284  (8.340) |

For the "All 3" row above, if a protein is a target in more than one Aspect, it is counted more than once.
As shown in the above table, most (60%) new annotations are on PK targets with old (and shallower) annotations.
The lower but non-trivial average IC of 7.588 for PK targets suggest that while PK targets might be easier to predict that NK and LK targets, they are nontheless not trivial to predict. An IC of 7.588 for a GO term corresponding to a posterior probability of only exp(-7.588)=0.0005 for this GO term given that all its parents are present, suggesting that a simple Bayesian approach of propagating the child terms based on previously annotated parent terms is far from sufficient for accurate prediction of PK targets.

## [3. Target database](3_target_database) ##

We check, for the five subsets of UniProt (Swiss-Prot proteins from CAFA-selected species, Swiss-Prot, UniRef50, UniProt reference proteome, UniRef90), the coverage of NK/LK/PK targets.
In the following table, the number of NK+LK+PK targets is larger than the number of proteins with new annotations. This is because, from a CAFA perspective, a single protein with new annotations in more than one GO Aspects is counted as more than one targets.

| Database           | Number of entries | Proteins with new terms | Species with new annotations | NK targets  | LK targets  | PK targets  |
|   :--:             |  :--:             | :--:                    | :--:                         | :--:        | :--:        | :--:        |
| CAFA4              |     97999 (0.05%) | 6666   (65%)            |  15   (4%)                   |  945  (25%) | 1114  (74%) | 6485  (80%) |
| Swiss-Prot         |    564638 (0.26%) | 7803   (76%)            | 339  (88%)                   | 2197  (59%) | 1208  (80%) | 6925  (86%) |
| UniRef50           |  50105705   (23%) | 6840   (67%)            | 261  (67%)                   | 1945  (52%) | 1097  (73%) | 5942  (74%) |
| Reference Proteome |  60181258   (28%) | 9211   (90%)            | 149  (39%)                   | 2782  (75%) | 1436  (95%) | 7548  (94%) |
| UniRef90           | 133971487   (62%) | 8238   (80%)            | 320  (83%)                   | 2697  (73%) | 1297  (86%) | 6820  (85%) |
| UniProt            | 214971037  (100%) | 10270 (100%)            | 387 (100%)                   | 3716 (100%) | 1509 (100%) | 8059 (100%) |

Although the CAFA4 dataset already includes the majority (65%) of proteins with new terms, especially LK targets (74%) and PK targets (80%), it only covers a relative small fractions (25% and 4% respectively) of NK targets and species with new annotations. Expansion of CAFA4 dataset to the whole Swiss-Prot and/or UniProt Reference Proteome, if not the whole UniProt, is needed for more comprehesive assessment of NK targets in more diverse species. While this means many of the included species will have <10 evaluated targets and cannot be used for reliable species-specific statistics, it is not a problem for obtaining overall statistics across all species.

## [4. GO evidence](4_HTP) ##

Different CAFA rounds defined "experimental" (EXP) annotations slightly differently:

| CAFA          | Evidence codes considered                                          |
| :--:          | :--:                                                               |
| CAFA1         | EXP, IDA,      IMP, IGI, IEP, TAS, IC                              |
| CAFA2 & CAFA3 | EXP, IDA, IPI, IMP, IGI, IEP, TAS, IC                              |
| CAFA-PI       | high throughput experiments for GO:0042710, GO:0001539, GO:0007616 |

CAFA excludes high-throughput (HTP) evidence codes, including: HTP, HDA, HMP, HGI, HEP. We check how many more proteins, terms, and annotations could have been included if HTP is included in addition to EXP.

| Evidence | MF targets | BP targets | CC targets |
| :--:     | :--:       | :--:       | :--:       |
| EXP      | 3475       | 6017       | 3792       |
| HTP      |   24       |   70       |  128       |
| EXP+HTP  | 3477       | 6077       | 3750       |

The exclusion of HTP annotation denies the inclusion of certain targets for term-centric assessment, which was based on high throughput experiments previously, e.g. in CAFA-PI. More importantly, it creates problems for protein-centric assessment as well. Some targets defined solely by an EXP evidence may not be a valid target defined by EXP+HTP evidences due to existence of old HTP annotations later confirmed by EXP evidence, especially in the case of CC as shown above. For example, O74456 was annotated with CC term GO:0005634 "nucleus" at t0 by HDA evidence; at t0, GO:0005634 is annotated to O74456 by both HDA and IPI evidence. Therefore, if HTP is not considered, O74456 is a valid CC target for prediction of GO:0005634, even though this term was already present at t0.

## [5. Baseline](5_baseline) ##

We test 14 different baseline methods based on database statistics (``naive1``, ``naive2``, ``naive3``), prior existing computational annotation (``uniprotgoa``) or sequence homology search (``blastevalue``, ``blastlocal``, ``blastevalue``, ``blastscore1``, ``blastscore2``, ``blastscore3``, ``blastglobal1``, , ``blastglobal2``, , ``blastglobal3``, , ``blastrank``, , ``blastfreq``), as well as two more advanced homology based predictor (``blastmetago``, ``blastnetgo``), as defined [here](5_baseline). 
The homology based baseline only uses blast here; Needleman-Wunsch global sequence alignment (NW-align) and Diamond were separately tested on the smaller CAFA3 dataset but were found not to introduce much improvement over blast under the default searching parameter settings, as shown [here](https"//github.com/kad-ecoli/baseline).
The prediction performance is evaluated on newly acquired GO annotations on t1 compared to t0. Prior existing GO annotations available at t0 are excluded from both ground truth and prediction during assessment. As shown in the following figures for Fmax, IC-weighted Fmax (wFmax), and a modified IC-weighted Fmax where weighing is applied to both GO terms and targets (w'Fmax), the current blast baseline (``blastlocal``, which is based on maximum local sequence identity) implemented by CAFA is consistently outperformed by ``blastfreq``, which predicts GO terms based on the number of blast hits annotated to a GO term divided by all hits.

![5_baseline/Fmax_full.png](5_baseline/Fmax_full.png?raw=true "Fmax_full.png")
![5_baseline/wFmax_full.png](5_baseline/wFmax_full.png?raw=true "wFmax_full.png")
![5_baseline/wFpmax_full.png](5_baseline/wFpmax_full.png?raw=true "wFpmax_full.png")

## [6. RNA](6_RNA) ##

Apart from proteins function annotation, GO terms are also used for RNA function annotation in the RNAcentral database. We calculate the number of targets  (average per-target IC) that can be used for function assessment based on growth period of t0 to t1:

| RNA (IC) |    NK        |    LK       |    PK        |    All       |
|  :--:    |   :--:       |   :--:      |   :--:       |   :--:       |
|    F     |  47 ( 3.195) |  13 (2.839) |  70 ( 2.070) | 130 ( 2.554) |
|    P     |  57 (11.823) |   2 (9.282) |  93 (11.875) | 152 (11.821) |
|    C     |  39 ( 4.822) |  11 (4.822) |   5 ( 4.424) |  55 ( 4.786) |
|  All     | 143 ( 7.078) |  26 (4.174) | 168 ( 7.568) | 337 ( 7.098) |

This table suggests that there are enough non-coding RNAs aquiring new GO annotations for assessment purpose, at least for the BP aspect. We note, however, that newly acquired annotations for MF and CC are highly redundant. In particular, among the 130 MF targets, 108 (83%) of them have GO:0003730 "mRNA 3'-UTR binding" and GO:1903231 "mRNA binding involved in posttranscriptional gene silencing" as the only leaf terms. Among the 55 CC targets, 50 (91%) of them have GO:0070062 "extracellular exosome" as the only leaf term. On the other hand, newly acquired BO terms are diverse and can be used for evaluation purpose.

Note that unlike the above analyses on proteins where MF targets with GO:0005515 "protein binding" as the only leaf term are excluded, no exclusion of the "protein binding" term is performed for RNA MF targets. This is because "protein binding" is not a particularly common leaf term for RNA (IC=2.17) and is associated with ~11% experimentally annotated MF targets, 

## License ##

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 2 of the License, or (at your option) any later
version.
