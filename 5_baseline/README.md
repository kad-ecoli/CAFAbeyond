# Alternative implement of baseline methods #

## Methods ##
In naive baseline (``bin/predict_naive.py``), the confidence score of
predicting a GO term ``g`` for a target protein is calculated as:
```
Cscore_naive1(g) = K(g) / K   ... (1)
```
Here, ``K`` is the total number of proteins in the whole training database;
and ``K(g)`` is the number of proteins annotated with ``g`` in the training
database. Therefore, equation (1) represents the background probability
of a GO term in the training database, regardless of target protein.
The difference between naive1 and naive2 is that the former considers all
training proteins regardless of species, while the latter only considers
proteins in the same species as the target protein. For consistency with
[information content in official CAFA assessment](https://github.com/yuxjiang/CAFA2/blob/master/matlab/pfp_eia.m),
both nominator and denominator of equation (1) are pseudo-counted by 1.

``naive2`` is species-specific version of ``naive1`` as ``naive2`` only considers
training proteins from the same species as the target protein. ``naive3`` is
conditioned on prior existing annotations of the target protein:
```
Cscore_naive3(g) =   max         { K(g) / K(p) }   ... (2)
                  p in parent(g)
```
where ``p`` is any parent term of ``g`` annotated to the target at t0.
If the target does not have prior existing GO terms, ``naive3`` is the
same as ``naive1``.

In the blast baseline (``bin/predict_blast.py``), 9 different scoring functions
are implemented, as shown in equations (3) to (11) below. In the official
assessment of CAFA1-3, the "blast" baseline predictor uses confidence score
based on local sequence identity:
```
Cscore_local(g) =      max        { localID_t(g) }   ... (3)
                    t=1, ... , N(g)
```
Here, ``t`` is the index of blast hits in a default blast run; ``N(g)`` is the
number of blast hits annotated with GO term ``g``; and ``localID_t(g)`` is the
local sequence identity between target sequence and the ``t``-th blast hit 
with term ``g``. Local identity is calculated as
``localID_t=nident_t/length_t``, where ``nident_t`` is the number of identical
residues between target and ``t``-th hit while ``length_t`` is the number of
aligned residues between the target and the hit. See our
[wiki page on blastp](https://github.com/kad-ecoli/CAFAbeyond/wiki/Scores-in-blastp)
for details on various scores reported by blastp, including local identity.

Another three scores based on global seuqence identities are also implemented:
```
Cscore_global1(g) =     max        { globalID1_t(g) }   ... (4)
                     t=1, ... , N(g)

Cscore_global2(g) =     max        { globalID2_t(g) }   ... (5)
                     t=1, ... , N(g)

Cscore_global3(g) =     max        { globalID1_t(g) }   ... (6)
                     t=1, ... , N(g)
```
Here, ``globalID1_t=nident_t/qlen`` is the global sequence identity normalized
by the target protein length ``qlen``; ``globalID2_t=nident_t/slen`` is
normalized by the blast hit length ``slen``;
``globalID3_t=nident_t/max(qlen,slen)`` is normalized by the maximum of target
and hit length.

The fifth score is based on  ``evalue_t(g)``, the evalue for the ``t``-th hit 
with term ``g``.  Since evalue is in the range of [0,inf) rather than (0,1], a
sigmoid function is used to rescale it into (0,1]:
```
                                       2* exp( - evalue_t(g) )
Cscore_evalue(g) =     max        {  --------------------------   }   ... (7)
                  t=1, ... , N(g)     1 + exp( - evalue_t(g) )
```
Here, ``evalue_t(g)`` is the evalue for the ``t``-th hit with term ``g``.

The sixth score is based on ``rank_t(g)``, the ranking of ``t``-th hit with
term ``g`` among all hits:
```
Cscore_rank(g) =     max        { 1 - ( rank_t(g) - 1 ) / N }   ... (8)
                t=1, ... , N(g)
```
Here, ``N`` is the number of all hits (with and without ``g``.)

The seventh score is based on frequency of a GO term among hits:
```
Cscore_freq(g) = N(g) / N   ... (9)
```

The next two scores are advanced version of frequency, weighted by either
``globalID1_t`` and ``bitscore_t``, which are the global sequence identity
and bitscore of the ``t``-th blast hit:
```
                     N(g)                         N
Cscore_metago(g) = ( sum ( globalID1_t(g) )) / ( sum ( globalID_t ))   ... (10)
		                 t=1                         t=1

                     N(g)                        N
Cscore_netgo(g)  = ( sum ( bitscore_t(g) )) / ( sum ( bitscore_t ))   ... (11)
	                   t=1                        t=1
```
Equations (10) and (11) are implemented by the sequence-based submodule of
MetaGO and NetGO, respecitvely, and probably should not be considered
"baseline" due to mathematical complexity. All scoring schemes from equation
(3) to (11) are based on blast local alignment using **default blast search
parameters**, except for a change of output format (``-outfmt 6``) for easy
parsing.

The ``bin/predict_blastbitscore.py`` script implement an alternative scoring
based on bitscore:
```
Cscore_score1(g) =     max       { score_t(g) / score_self(target) }  ... (13)
                    t=1, ... , N(g)

Cscore_bitscore2(g) =     max       { score_t(g) / score_self(t) }       ... (14)
                    t=1, ... , N(g)

Cscore_bitscore3(q) =     max       { score_t(g) / max{ score_self(target),
                    t=1, ... , N(g)                     score_self(t)} } ... (15)
```
Here, ``score_self(target)`` and ``score_self(t)`` are the bitscores of
aligning the target to itself and template ``t`` to itself, respectively.

In ``uniprotgoa`` baseline (``bin/predict_iea.py``), the GO term of a protein is copied
from its full set of uniprot-goa, which mainly includes (but is not limited) 
electronically inferred annotations with IEA evidence.
The confidence score of the GO term is determined by the evidence code from
in the uniprot-goa annotation. 
In [our previous study](https://doi.org/10.1093/bioinformatics/btaa548),
we obtained statistics on the portion of GO terms with the same evidence
code ``e`` that are either experimentally confirmed (``N_confirm(e)``) or 
rejected with a "NOT" qualifier in a later release (``N_reject(e)``). The 
confidence score of the evidence code ``e`` is therefore:
```
Cscore_uniprotgoa(e) = N_confirm(e) / ( N_confirm(e) + N_reject(e) )   ... (16)
```

## Results ##
The performance is evaluated on newly acquired GO annotations at t0 compared to t1.
Prior existing GO annotations from t0 are excluded from both ground-truth and
predictions. Fmax, wFmax, and Smin are defined the same as in CAFA, where all
targets have the same weight. In contrast, F'max, wF'max and S'max weights each
target by the total IC of its ground-truth annotations.

![Fmax_full.png](Fmax_full.png?raw=true "Fmax_full.png")
![Smin_full.png](Smin_full.png?raw=true "Smin_full.png")
![wFmax_full.png](wFmax_full.png?raw=true "wFmax_full.png")
![Fpmax_full.png](Fpmax_full.png?raw=true "Fpmax_full.png")
![Spmin_full.png](Spmin_full.png?raw=true "Spmin_full.png")
![wFpmax_full.png](wFpmax_full.png?raw=true "wFpmax_full.png")
