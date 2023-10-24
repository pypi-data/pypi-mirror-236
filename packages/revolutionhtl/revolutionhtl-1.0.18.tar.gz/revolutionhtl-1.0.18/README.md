![REvolutionH-tl logo.](https://gitlab.com/jarr.tecn/revolutionh-tl/-/raw/master/docs/images/Logo_horizontal.png)

Bioinformatics tool for the reconstruction of evolutionary histories. Input: fasta files or sequence alignment hits, Output: orthology. event-labeled gene trees, and reconciliations.

[Bioinformatics & complex networks lab](https://ira.cinvestav.mx/ingenieriagenetica/dra-maribel-hernandez-rosales/bioinformatica-y-redes-complejas/)

- José Antonio Ramírez-Rafael [jose.ramirezra@cinvestav.mx]
- Maribel Hernandez-Rosales [maribel.hr@cinvestav.mx ]

<img src="https://gitlab.com/jarr.tecn/revolutionh-tl/-/raw/master/docs/images/revolution_diagram.png" alt="pipeline" style="zoom:25%;" />

# Install

```bash
pip install revolutionhtl
```

**Requirements**

[Python >=3.7 ](https://www.python.org/)

If you want to run sequence alignments using revolutionhtl, then install [Diamond](https://github.com/bbuchfink/diamond):

```bash
wget http://github.com/bbuchfink/diamond/releases/download/v2.1.8/diamond-linux64.tar.gz
tar xzf diamond-linux64.tar.gz
```

# Usage

> For an example with data  [click here](https://gitlab.com/jarr.tecn/revolutionh-tl/-/blob/master/docs/example.md?ref_type=heads).

```bash
python -m revolutionhtl <arguments>
```

Below are described the steps of the program, arguments needed to run REvolutionH-tl, and description of output files.

## Steps

1. **Orthogroup & best hit selection.** Input: alignment hits (generate this using `revolutionhtl.diamond`) .
2. **Orthology and gene tree reconstruction.** Input: best hits (generate this at step 1).
3. **Species tree reconstruction.** Input: gene trees (generate this at step 2).
4. **Tree reconciliation.** Input: gene and species trees (generate this at steps 2 and 3).

## Arguments


<details>
  <summary> <b>Input data</b> (Click to expand)  </summary> 
  <b>- -h    --help </b> <br/> show this help message and exit <br/> <br/>
  <b>-steps [integers] </b> <br/> List of steps to run (default: 1 2 3 4).  <br/> <br/>
  <b>-alignment_h   --alignment_hits [string]</b> <br/> Directory containing alignment hits, the input of step 1. (default: ./). <br/> <br/>
  <b>-best_h      --best_hits [string]</b> <br/> .tsv file containing best hits, the input of step 2. (default: use output of step 1). <br/> <br/>
  <b>-T      --gene_trees [string]</b> <br/> .tsv file containing gene trees, the input of steps 3 and 4. (default: use output of step 2). <br/> <br/>
  <b>-S     --species_tree [string]</b> <br/> .nhx file containing a species tree, an input of step 4. (default: use output of step 3). <br/> <br/>
</details>
<details>
  <summary> <b>File names</b> (Click to expand)  </summary> 
  <b>-o      --output_prefix [string] </b> <br/>
  Prefix used for output files (default "tl_project").<br/><br/>
  <b>-og      --orthogroup_column [string]</b> <br/>
  Column in -best_h     -T, and output files specifying orthogroups (default: OG).<br/><br/>
  <b>-Nm      --N_max [integer] </b> <br/>
  Indicates the maximum number of genes in a orthogroup, bigger orthogroups are splitted. If 0, no orthogroup is splitted. (default= 2000).<br/><br/>
  <b>-k      --k_size_partition [integer]</b> <br/>
  Integer indicatng how many best hit graphs will be processed in bunch:: first graphs with <k genes, then <2k. then <3k, and so on. (default: k=100)<br/><br/>
</details>

<details>
  <summary> <b>Algorithm parameters</b> (Click to expand)  </summary> 
  <b>-bh_heuristic     --besthit_heuristic  [string] </b> <br/>
  Indicates how to normalize bit-score in step 1 (default: normal). Normal: no normalization, prt: use proteinortho auxiliary files, smallest: use length of the smallest sequence, target: use target sequence, query: use query sequence, directed: x->y hit, bidirectional: use x->y and y->x hits.<br/>
  Options: normal, prt, smallest_bidirectional, smallest_directed, query_directed, target_directed, alignment_directed, query_bidirectional, target_bidirectional, alignment_bidirectional<br/><br/>
  <b>-f      --f_value [float]</b> <br/>
  Real number between 0 and 1, a parameter of step 1. Defines the adaptative threshhold as: f\*max_bit_score (default: 0.95).<br/><br/>
  <b>-bmg_h     --bmg_heuristic [string] </b> <br/>
  Comunity detection method, an heuristic of step 2. (default: Louvain).<br/>
  Options: Mincut, BPMF, Karger, Greedy, Gradient_Walk, Louvain, Louvain_Obj<br/><br/>
  <b>-bmgh_nb      --bmgh_no_binary [bool]</b> <br/>
  Flag, specifies if force binary tree in step 2. (no flag: force binary, flag: do not force binary).<br/><br/>
  <b>-stree_h     --species_tree_heuristic [string]</b> <br/>
  Comunity detection method, an heuristic of step 3. (default: louvain_weight).<br/>
  Options: naive, louvain, mincut, louvain_weight<br/><br/>
  <b>-streeh_repeats     --stree_heuristic_repeats [integer]</b> <br/>
  integer, specifies how many times run the heuristic of step 3. (default: 3)<br/><br/>
  <b>-streeh_b     --streeh_binary [bool]</b> <br/>
  Flag, specifies if force binary tree in step 3. (no flag: do not force binary, flag: force binary).<br/><br/>
  <b>-streeh_ndb     --streeh_no_doble_build [bool]</b> <br/>
  Flag, specifies if run build algorithm twice to obtain less resolved tree in step 3. (no flag: double build, flag: single build).<br/><br/>
</details>

## Output files

### Step 1 | Best hit & orthogroup selection

#### Best hits

For every gene in the analysis, step 1 aims to recover all the most similar genes based on sequence similarity. This procedure uses the normalized bit-score of the alignment hits and an adaptive threshold to create a subselection of alignment hits. We call *best hits* to this subselection. See section 3.1.2 of reference [1] for a deeper explanation of this analysis.

A best hit (x-->y) is a directed relationship from one gene x to gene y, where the former is called *query* and the latter is called *target*.

Best hits are output as a table in a file with extension `.best_hits.tsv` ([Click here](https://gitlab.com/jarr.tecn/revolutionh-tl/-/blob/master/docs/example%20results/tl_project.best_hits.tsv?ref_type=heads) for an example file). Each row of this table describes a best hit throughout 10 columns: "OG" indicates the ID of the orthogroup containing the best hit, and the six columns containing "Query\_" and "Target\_" contain information about the query and target genes. Finally, alignment statistics are shown in the columns "Alignment_length", "Bit_score", and "Evalue".

#### Orthogroups

An orthogroup is a collection of homologous genes, which means that they appear as leaves of the same gene tree. We say that two genes are in the same orthogroup if we can construct a path of best hits connecting them.

Orthogroups are output as a table in a file with the extension `.orthogroups.tsv`. Here, each row indicates one orthogroup, the first column "OG" indicates the ID, the second and third columns "n_genes", and "n_sepecies" contain the number of genes in the orthogroup and the number of species represented by those genes. Then, there is one column per each species of the analysis, those columns contain the genes of the orthogroup that are present in those species.

### Step 2 | Gene tree reconstruction & orthology

#### Gene trees

Gene trees are output in the file with extension `.gene_trees.tsv`, for each row of this file there is an orthogroup ID, and a gene tree in NHXX format, which is a generalized newick ([Click here](https://gitlab.com/jarr.tecn/revolutionh-tl/-/blob/master/docs/nhxx.md?ref_type=heads) for a description and examples of newick format).

The inner nodes of the gene tree are labeled as speciation events with the letter "S", or as duplication events with the letter "D".

The leaves of the gene tree represent the genes of the orthogroup.

The gene trees output here are the least resolved trees that can be reconstructed from the best hits. If you want fully resolved trees, look at the output of step 4.

#### Orthology

Orthology is saved in the file with the extension `.orthologs.tsv`. Each row identifies a single orthology relationship between genes in the columns "a" and "b". Additionally, the column "OG" specifies the orthogroup containing the genes.

Two genes are orthologous if they diverge at a speciation event.

#### Best matches

For each gene in the gene trees, we return the best matches, i.e. the most evolutionarily related genes in other species. Best matches are defined concerning a gene tree. See section 3.1.1 [1] for a deeper explanation.

A best match (x-->y) is a directed relationship from gene "x" to gene "y". The main difference with "best hits" in the previous step is that a best match is consistent with a gene tree, while a best hit is based on the bit-score of sequence alignments.

### Step 3 | Species tree reconstruction

We reconstruct a species tree as a consensus of all the gene trees obtained in step 2, the procedure is detailed in section 3.1.4 of [1]. This species tree is saved in NHXX format in the file with the extension `.species_tree.tsv `. NHXX format is a generalized Newick ([Click here](https://gitlab.com/jarr.tecn/revolutionh-tl/-/blob/master/docs/nhxx.md?ref_type=heads) for a description and examples of Newick format).

### Step 4 | Tree reconciliation

The reconciliation shows how genes evolved across species and time. This can be represented as a map of the nodes in the gene tree to nodes and edges of the species tree. The figure below shows a reconciliation. On the left side, the nodes of a gene tree are mapped to the species tree using arrows. On the right side, the reconciliation is shown explicitly by drawing the gene tree inside of the species tree. Red circles correspond to speciation events, while blue squares correspond to gene duplication. Note that duplication nodes in the gene tree are mapped to edges of the species tree, on the other hand, speciation nodes of the gene tree are mapped to nodes of the species tree.

![Reconciliation](https://gitlab.com/jarr.tecn/revolutionh-tl/-/raw/master/docs/images/recon_example.png?ref_type=heads)

To represent a reconciliation map REvolutionH-tl uses a comma-separated list, where each element takes the form `x:y`, where `x` is a node ID in the gene tree, and `y` is a node ID in the species tree. In the example of the figure above we have the reconciliation map `0:0,1:1,2:1`. As in the example of the figure, the reconciled gene tree can include extra speciation events and gene loss. In section 3.1.5 of [1], the procedure to compute this map is detailed.

REvolutionH-tl performs a reconciliation of the reconstructed gene and species trees. To this end, we add a node ID to all the nodes of the gene tree and the species tree using the attribute "node_id". The species tree with nodes ID is written to the file with the extension `.labeled_species_tree.nhxx`. On the other hand, the reconciliations are saved in the file with the extension `.reconciliation.tsv`, this file contains the following columns:

- OG: Specifies the orthogroup ID
- tree: reconciled gene tree in NHXX format.
- reconciliation_map: a comma-separated list of pair of nodes.
- flipped_nodes: nodes of the gene tree flipped from speciation to duplication. The number of flipped nodes is a metric for discordance between the non-reconciled gene tree and the species tree.

# References

[1] Ramirez-Rafael J. A. (2023). *REvolutionH-tl: a tool for the fast reconstruction of evolutionary histories using graph theory* [Master dissertation, Cinvestav Irapuato]. Avaliable at https://drive.google.com/file/d/1NckRmpvxeOdoJG3ugbZSKsHyYEua4eYG/view?usp=sharing.
