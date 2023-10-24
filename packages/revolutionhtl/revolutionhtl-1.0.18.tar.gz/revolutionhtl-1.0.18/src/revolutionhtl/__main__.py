if __name__ == "__main__":
    from .reconciliation import reconciliate_many, recon_table_to_str
    from .error import InconsistentTrees, MissedData, ParameterError
    from .orthology import orthologs_from_trees_df
    from .supertree import from_gene_forest
    from .constants import _df_matches_cols, _default_f
    from .hug_free import build_graph_series
    from .parse_prt import _parse, normalization_modes, normalization_smallest
    from .common_tools import norm_path
    from .cBMG_tools import analyze_digraphs_list
    from .nhxx_tools import read_nhxx, get_nhx
    from .in_out import read_tl_digraph, tl_digraph_from_pandas

    from tqdm import tqdm
    from numpy import argsort
    import pandas as pd
    import os

    import argparse
    parser = argparse.ArgumentParser(prog= 'revolutionhtl',
                                     description='Reconstruction of Evolutionaty Histories TooL.\n1. Best hit selection 2. Orthology and gene tree reconstruction 3. Species tree reconstruction 4. Tree reconciliation\nhttps://pypi.org/project/revolutionhtl/',
                                     usage='python -m revolutionhtl <arguments>',
                                     formatter_class=argparse.MetavarTypeHelpFormatter,
                                    )

    # Arguments
    ###########

    # Input data
    # ..........

    parser.add_argument('-steps',
                        help= 'List of steps to run (default: 1 2 3 4).',
                        type= int,
                        nargs= '*',
                        default= [1, 2, 3, 4]
                       )

    parser.add_argument('-alignment_h', '--alignment_hits',
                        help= 'Directory containing alignment hits, the input of step 1. (default: ./).',
                        type= str,
                        default= './'
                       )

    parser.add_argument('-best_h', '--best_hits',
                        help= '.tsv file containing best hits, the input of step 2. (default: use output of step 1).',
                        type= str,
                       )

    parser.add_argument('-T', '--gene_trees',
                        help= '.tsv file containing gene trees, the input of steps 3 and 4. (default: use output of step 2).',
                        type= str,
                       )

    parser.add_argument('-S', '--species_tree',
                        help= '.nhx file containing a species tree, an input of step 4. (default: use output of step 3).',
                        type= str,
                        default= 'BUILD_FROM_GENE_FOREST',
                       )

    # Parameters
    # ..........
    parser.add_argument('-bh_heuristic', '--besthit_heuristic',
                        help= 'string, indicates how to normalize bit-score in step 1 (default: normal). Normal: no normalization, prt: use proteinortho auxiliary files, smallest: use length of the smallest sequence, target: use target sequence, query: use query sequence, directed: x->y hit, bidirectional: use x->y and y->x hits..',
                        type= str,
                        choices= ['normal', 'prt']+normalization_smallest+normalization_modes,
                        default= 'normal',
                       )

    parser.add_argument('-f', '--f_value',
                        help= f'Real number between 0 and 1, a parameter of step 1. Defines the adaptative threshhold as: f*max_bit_score (default: {_default_f}).',
                        type= float,
                        default= _default_f,
                       )

    parser.add_argument('-bmg_h', '--bmg_heuristic',
                        help= f'Comunity detection method, an heuristic of step 2. (default: Louvain).',
                        type= str,
                        default= 'Louvain',
                        choices= ['Mincut', 'BPMF', 'Karger', 'Greedy', 'Gradient_Walk', 'Louvain', 'Louvain_Obj'],
                       )

    parser.add_argument('-no_binary_R', '--no_binary_triples',
                        help= 'Flag, specifies if use binary triples in step 2. (no flag: use binary triples, flag: do not use binary triples).',
                        action= 'store_false',
                       )


    parser.add_argument('-f_bT', '--force_binary_gene_tree',
                        help= 'Flag, specifies if force binary tree in step 2. (no flag: do not force binary, flag: force binary).',
                        action= 'store_true',
                       )

    parser.add_argument('-T_no_db', '--gene_tree_no_double_build',
                        help= 'Flag, specifies if run build algorithm twice to obtain less resolved tree in step 2. (no flag: double build, flag: single build).',
                        action= 'store_false',
                       )

    parser.add_argument('-stree_h', '--species_tree_heuristic',
                        help= 'Comunity detection method, an heuristic of step 3. (default: louvain_weight).',
                        type= str,
                        default= 'louvain_weight',
                        choices= ['naive', 'louvain', 'mincut', 'louvain_weight']
                       )

    parser.add_argument('-streeh_repeats', '--stree_heuristic_repeats',
                        help= 'integer, specifies how many times run the heuristic of step 3. (default: 3)',
                        type= int,
                        default= 3
                       )

    parser.add_argument('-streeh_b', '--streeh_binary',
                        help= 'Flag, specifies if force binary tree in step 3. (no flag: do not force binary, flag: force binary).',
                        action= 'store_true',
                       )

    parser.add_argument('-streeh_ndb', '--streeh_no_doble_build',
                        help= 'Flag, specifies if run build algorithm twice to obtain less resolved tree in step 3. (no flag: double build, flag: single build).',
                        action= 'store_false',
                       )

    # Format parameters
    # .................

    parser.add_argument('-o', '--output_prefix',
                        help= 'Prefix used for output files (default "tl_project").',
                        type= str,
                        default= 'tl_project',
                       )

    parser.add_argument('-og', '--orthogroup_column',
                        help= 'Column in -best_h, -T, and output files specifying orthogroups (default: OG).',
                        type= str,
                        default= 'OG',
                       )

    parser.add_argument('-Nm', '--N_max',
                        help= 'Indicates the maximum number of genes in a orthogroup, bigger orthogroups are splitted. If 0, no orthogroup is splitted. (default= 2000).',
                        type= int,
                        default= 2000,
                       )

    parser.add_argument('-k', '--k_size_partition',
                        help= 'Integer indicatng how many best hit graphs will be processed in bunch:: first graphs with <k genes, then <2k. then <3k, and so on. (default: k=100)',
                        type= int,
                        default= 100,
                       )

    parser.add_argument('-S_attr', '--S_attr_sep',
                        help= 'String used to separate attributes in the species tree at step 4.',
                        type= str,
                        default= ';',
                       )

    args= parser.parse_args()

    ################
    # Process data #
    ################

    from .hello import hello5
    print(hello5)

    allowed_steps= {1, 2, 3, 4}
    bad_steps= set(args.steps) - allowed_steps
    if len(bad_steps) > 0:
        raise ParameterError(f'Only steps 1, 2, and 3 are allowed to be used in the parameter -steps. ')
    else:
        args.steps= sorted(set(args.steps))

    print(f'Running steps {", ".join(map(str, args.steps))}')

    # 1. Convert proteinortho output to a best-hit list
    #################################################
    if 1 in args.steps:
        print("\nStep 1: Convert proteinortho output to a best-hit list")
        print("------------------------------------------------------")
        if args.alignment_hits==None:
            raise MissedData('Step 0 needs a value for the parameter -alignment_hits.')

        args.alignment_hits= norm_path(args.alignment_hits)
        opath= args.output_prefix+'.best_hits.tsv'
        df_hits, OGs_table= _parse(args.alignment_hits, args.f_value, opath, args.besthit_heuristic, N_max= args.N_max)
        print('This file will be used as input for step 2.')

        print('Writing orthogroups...')
        opath= args.output_prefix+'.orthogroups.tsv'
        OGs_table.to_csv(opath, sep='\t', index= False)
        print(f'Successfully written to {opath}')
    else:
        df_hits= None

    # 2. Conver best hit graphs to cBMGs and gene trees
    ##################################################
    if 2 in args.steps:
        print("\nStep 2: Conver best-hit graphs to cBMGs and gene trees")
        print("------------------------------------------------------")
        readHs= type(df_hits)!=pd.DataFrame
        if readHs and (args.best_hits==None):
            raise MissedData('Step 2 needs a value for the parameter -best_hits. Create it by running step 1.')

        if readHs:
            print('Reading hit graphs...')
            G= read_tl_digraph(args.best_hits, og_col= args.orthogroup_column)
        else:
            print('Creating graphs...')
            G= tl_digraph_from_pandas(df_hits, og_col= args.orthogroup_column)

        Tg= build_graph_series(G, args)

        # Print orthologs
        TTg= Tg.reset_index()
        df_orthologs= orthologs_from_trees_df(TTg,
                                forbidden_leaf_name= 'X', tree_col= 'tree')
        opath= f'{args.output_prefix}.orthologs.tsv'
        df_orthologs.to_csv(opath, sep= '\t', index= False)
        print(f'Orthologs successfully written to {opath}')


    else:
        Tg= None

    # 3. Reconstruct species tree
    #############################
    if 3 in args.steps:
        print("\nStep 3: Species tree reconstruction")
        print("-----------------------------------")
        readTg= type(Tg)!=pd.Series
        if readTg and (args.gene_trees==None):
            raise MissedData('Step 3 needs a value for the parameter -gene_trees. Create it by running step 2.')
        if readTg:
            print('Reading trees...')
            gTrees= pd.read_csv(args.gene_trees,
                                sep= '\t').set_index(
                args.orthogroup_column).tree.apply(lambda x: read_nhxx(x, name_attr= 'accession'))
        else:
            gTrees= Tg

        print("Reconstructing species tree...")
        species_tree= from_gene_forest(gTrees,
                                       method= args.species_tree_heuristic,
                                       numb_repeats= args.stree_heuristic_repeats,
                                       doble_build= args.streeh_no_doble_build,
                                       binary= args.streeh_binary,
                                      )

        print("Writing species tree...")
        s_newick= get_nhx(species_tree, root= 1, name_attr= 'species', ignore_inner_name= True)
        opath= f'{args.output_prefix}.species_tree.tsv'
        with open(opath, 'w') as F:
            F.write(s_newick)
        print(f'Successfully written to {opath}')
    else:
        species_tree= None

    # 4. Reconciliate gene trees and species tree
    ##############################################
    if 4 in args.steps:
        print("\nStep 4: Reconciliation of gene species trees")
        print("--------------------------------------------")
        readTg= type(Tg)!=pd.Series
        if readTg:
            if args.gene_trees==None:
                raise MissedData('Step 4 needs a value for the parameter -gene_trees. You can create it by running step 2.')
            print('Reading trees...')
            gTrees= pd.read_csv(args.gene_trees,
                                sep= '\t').set_index(
                args.orthogroup_column).tree.apply(lambda x: read_nhxx(x, name_attr= 'accession'))
        else:
            gTrees= Tg

        readTs= species_tree == None
        if readTs:
            if args.species_tree=='BUILD_FROM_GENE_FOREST':
                raise MissedData('Step 4 needs a species tree, run step 3 to construct one or set a value for the parameter -species_tree')
            print('Reading species tree...')
            with open(args.species_tree) as F:
                sTree= read_nhxx(''.join( F.read().strip().split('\n') ),
                                 name_attr= 'species',
                                 attr_sep= args.S_attr_sep
                                )
        else: 
            sTree= species_tree

        print('Reconciling trees...')
        df_recs= reconciliate_many(gTrees, sTree)

        # Write resolved trees
        df_r= recon_table_to_str(sTree, df_recs, args.orthogroup_column)
        print("Writing to file...")
        opath= f'{args.output_prefix}.reconciliation.tsv'
        df_r.to_csv(opath, sep= '\t', index= False)
        print(f'Reconciliation were successfully written to {opath}')

        # Write labeled species tree
        nhx_s= get_nhx(sTree, name_attr= 'species', root= 1, ignore_inner_name= True)
        opath= f'{args.output_prefix}.labeled_species_tree.nhxx'
        with open(opath, 'w') as F:
            F.write(nhx_s)
        print(f'Indexed species tree successfully written to {opath}')

        """
        # Write orthology relations
        df_orthologs, df_pseudo= orthologs_from_trees_df(df_recs, forbidden_leaf_name= 'X', tree_col= 'reconciliated_tree')

        opath= f'{args.output_prefix}.orthologs.tsv'
        df_orthologs.to_csv(opath, sep= '\t', index= False)
        print(f'Orthologs successfully written to {opath}')

        opath= f'{args.output_prefix}.pseudo_orthologs.tsv'
        df_pseudo.to_csv(opath, sep= '\t', index= False)
        print(f'Pseudo-orthologs successfully written to {opath}')
        """

    print("\nREvolutionH-tl finished all the tasks without any problem")
    print("---------------------------------------------------------")
