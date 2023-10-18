from .nxTree import compact_edge, get_dad, set_sparce_matrix,get_leaf2color, is_leaf
from .nhxx_tools import read_nhxx, get_nhx
from .triplets import get_triplets

import time
import networkx as nx
from networkx import dfs_postorder_nodes
import pandas as pd
from itertools import chain
from tqdm import tqdm
tqdm.pandas()

def correct_tree(Tg, Rs, root= 1,
                 label_attr= 'label',
                 species_attr= 'species',
                 event_attr= 'event',
                 algorithm= 'prune_L',
                 force_phylogeny= True,
                 update_lca= True, 
                 inplace= True,
                ):

    # Inconsistent gene triples
    leaf_2_color= {Tg.nodes[x][label_attr] : Tg.nodes[x][species_attr]
                   for x in Tg if is_leaf(Tg, x)}
    F= lambda x: leaf_2_color[x]
    g2c_triple= lambda triple: tuple(sorted(map(F, triple[:2]))) + (F(triple[-1]),)

    R_I= set()
    R_C= set()
    for rg in get_triplets(Tg, event=event_attr, color=label_attr, root_event='S'):
        if g2c_triple(rg) in Rs:
            R_C.add(rg)
        else:
            R_I.add(rg)

    # From label to node
    leaf_2_node= {Tg.nodes[x][label_attr] : x
                  for x in Tg if is_leaf(Tg, x)}
    F= lambda triple: tuple(leaf_2_node[x] for x in triple)
    R_C= set(map(F, R_C))
    R_I= set(map(F, R_I))

    # Prune
    if algorithm=='prune_R':
        ret= prune_triples(Tg, R_I, force_phylogeny= force_phylogeny, update_lca= update_lca, inplace= inplace)
    elif algorithm=='prune_L':
        ret= prune_leaves(Tg, R_C, R_I, force_phylogeny= force_phylogeny, update_lca= update_lca, inplace= inplace, root= 1)
    else:
        raise ValueError(f'"{algorithm}" is not a valid algorithm for tree edition')

    return ret, len(R_I)

def prune_leaves(T, R_C, R_I, w_r= None, force_phylogeny= True, update_lca= True, inplace= True, root= 1):

    if not inplace:
        T= T.copy()
    if w_r==None:
        w_r= {r:1 for r in chain(R_C,R_I)}
    # Invert wheight of consistent triples
    w_r.update({rg:-w_r[rg] for rg in R_C})
    # Function for leaf prune-weight
    out_w= lambda x,G: sum((w_r[y] for y in G[x]))
    #out_w= lambda x,G: 0
    in_w= lambda x,G: sum((w_r[y[0]] for y in G.in_edges(x)))
    #in_w= lambda x,G: 0
    prune_w= lambda x,G: (out_w(x, G), in_w(x, G), x)

    # Construct three-partite graph
    leafs= set(filter(lambda x: is_leaf(T,x) , T))
    G= nx.DiGraph()
    G.add_nodes_from(chain(leafs,R_C,R_I))
    G.add_edges_from(((x,ri)
                      for x in leafs
                      for ri in R_I
                      if x in ri
                     ))
    G.add_edges_from(((rc,x)
                      for x in leafs
                      for rc in R_C
                      if x in rc
                     ))

    print("\n\n")
    LL= len(R_I)
    t0= time.time()
    print(len(leafs), len(R_I), len(R_C))

    # Choose subset of leafs
    prune= []
    while len(R_I)>0:
        leaf= _choose_best(G, leafs, prune_w)
        prune+= [leaf]
        t0= time.time()
        leafs= leafs-{leaf}
        t1= time.time()
        R_I= R_I-set(G[leaf])
        t2= time.time()
        R_C= R_C-set((y[0] for y in G.in_edges(leaf)))
        t3= time.time()
        G= nx.induced_subgraph(G, leafs.union(R_I).union(R_C) )
        t4= time.time()
        print('>>>>> ', t1-t0, t2-t1, t3-t2, t4-t3)

    t1= time.time()
    if LL==0:
        print('total per triple: ', '-----')
    else:
        print('total per triple: ', (t1-t0)/LL)

    # Obtain induced tree
    for x in prune:
        T.remove_node(x)
    # Compcat edges if necesary
    if force_phylogeny:
        nodes= list(filter(lambda x: len(T[x])==1,
                           dfs_postorder_nodes(T, root)
                          ))
        for x_node in nodes:
            x1= list(T[x_node])[0]
            compact_edge(T, x_node, x1, delete= 'upper', update_lca= False)

    # Update LCA
    if update_lca:
        set_sparce_matrix(T)
    return T

def _choose_best(G, leafs, prune_w):
    t0= time.time()
    df= [prune_w(x,G) for x in leafs]
    t1= time.time()
    best= sorted(df, reverse= True)[0][2]
    t2= time.time()
    print(">>> ", len(leafs), t1-t0, t2-t1)
    return best

def prune_triples(T, R, force_phylogeny= True, update_lca= True, inplace= True):
    if not inplace:
        T= T.copy()
    # Remove leafs present in the triples
    leaves= set(chain.from_iterable(R))
    for x in leaves:
        T.remove_node(x)

    # Compcat edges if necesary
    if force_phylogeny:
        nodes= list(filter(lambda x: len(T[x])==1,
                           dfs_postorder_nodes(T, T.root)
                          ))
        for x_node in nodes:
            x1= list(T[x_node])[0]
            compact_edge(T, x_node, x1, delete= 'upper', update_lca= False)

    # Update LCA
    if update_lca:
        set_sparce_matrix(T)

    return T

def correct_tree_df(df, Ts, tree_col= 'tree',
                    root= 1,
                    label_attr= 'label',
                    species_attr= 'species',
                    event_attr= 'event',
                    algorithm= 'prune_L',
                    inplace= False
                   ):
    if not inplace:
        df= df.copy()
    # Prepare species triples
    for y in Ts:
        if len(Ts[y])>0:
            Ts.nodes[y][event_attr]= 'S'
    Ts_triples= set(get_triplets(Ts, event=event_attr, color=species_attr, root_event='S'))


    # Correct trees
    out= df[tree_col].progress_apply(lambda T: correct_tree(T, Ts_triples, root= root,
                                                            label_attr= label_attr,
                                                     species_attr= species_attr,
                                                     event_attr= event_attr,
                                                     algorithm= algorithm,
                                                     force_phylogeny= True,
                                                     update_lca= True, 
                                                     inplace= True,
                ))
    df[tree_col]= out.str[0]
    df['edited']= out.str[1]
    return df

# Standalone usage
##################

if __name__ == "__main__":
    import pandas as pd

    import argparse
    parser = argparse.ArgumentParser(prog= 'revolutionhtl.tree_correction',
                                     description='Correction for gene tree with respect to a species tree',
                                     usage='python -m revolutionhtl.tree_correction <arguments>',
                                     formatter_class=argparse.MetavarTypeHelpFormatter,
                                    )

    # Arguments
    ###########

    # Input data
    # ..........

    parser.add_argument('gene_trees',
                        help= 'A .tsv file containing gene trees in the column specified by "-tree_column" in nhxx format',
                        type= str,
                       )

    parser.add_argument('species_tree',
                        help= '.nhxx file containing a species tree.',
                        type= str,
                       )

    # Parameters
    # ..........
    parser.add_argument('-alg', '--algorithm',
                        help= 'Algorithm for tree correction (default: prune_L).',
                        type= str,
                        choices= ['prune_L', 'prune_R'],
                        default= 'prune_L',
                       )

    # Format parameters
    # .................

    parser.add_argument('-T', '--tree_column',
                        help= 'Column containing trees in nhxx format at the "gene_trees" file. (default: tree).',
                        type= str,
                        default= 'tree'
                       )

    parser.add_argument('-o', '--output_prefix',
                        help= 'Prefix used for output files (default "tl_project").',
                        type= str,
                        default= 'tl_project',
                       )

    parser.add_argument('-T_attr', '--T_attr_sep',
                        help= 'String used to separate attributes in the gene trees. (default: ";").',
                        type= str,
                        default= ';',
                       )

    parser.add_argument('-S_attr', '--S_attr_sep',
                        help= 'String used to separate attributes in the species tree. (default: ";").',
                        type= str,
                        default= ';',
                       )

    args= parser.parse_args()

    # Perform edition
    #################

    print('\n---------------------------')
    print('\nREvolutionH-tl tree edition')
    print('---------------------------\n')

    print('Reading gene trees...')
    gTrees= pd.read_csv(args.gene_trees, sep= '\t')
    gTrees[args.tree_column]= gTrees[args.tree_column].progress_apply(
        lambda x: read_nhxx(x, name_attr= 'accession', attr_sep= args.T_attr_sep))

    print('Reading species tree...')
    with open(args.species_tree) as F:
        sTree= read_nhxx(''.join( F.read().strip().split('\n') ),
                         name_attr= 'species',
                         attr_sep= args.S_attr_sep
                        )

    print('Editing trees...')
    gTrees= correct_tree_df(gTrees, sTree, tree_col= args.tree_column,
                    root= 1,
                            label_attr= 'accession',
                    species_attr= 'species',
                    event_attr= 'accession',
                    algorithm= args.algorithm,
                    inplace= False
                   )

    print('Writting corrected trees...')
    opath= f'{args.output_prefix}.corrected_trees.tsv'
    gTrees.to_csv(opath, sep= '\t', index= False)
    print(f'Successfully written to {opath}')
