#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 23 00:06:31 2023

@author: qiuyulian
"""

import numpy as np
import pandas as pd
from scipy.stats import binned_statistic
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
import scanpy as sc
from multiprocessing import Pool
import random
import matplotlib.pyplot as plt
from scipy.spatial import distance_matrix


def initial_detection(adata, dbl_rate, nPCs=10, pN = 0.25, num_cores=1, vis=False,inplace=True):
    
    sweep_list = paramSweep_v3(adata,num_cores=num_cores)
    sweep_stats = summarizeSweep(sweep_list)
    bcmvn = find_pK(sweep_stats,vis=vis)
    pK = bcmvn["pK"][bcmvn["BCmetric"].values.argmax()]
    nExp = round(dbl_rate*adata.n_obs)
    doubletFinder_v3(adata, nPCs = nPCs, pN = pN, pK=pK, nExp = nExp, inplace=inplace)
    


def doubletFinder_v3(adata, nPCs, pN=0.25, pK=None, nExp=None, anno_by=None, inplace=True):

    # Make merged real-artificial data
    real_cells = adata.obs_names
    #data = adata.copy()
    n_real_cells = adata.n_obs
    n_doublets = round(n_real_cells / (1 - pN) - n_real_cells)
    print(f"Creating {n_doublets} artificial doublets...")
    real_cells1 = np.random.choice(real_cells, n_doublets, replace=True)
    real_cells2 = np.random.choice(real_cells, n_doublets, replace=True)
    doublets = (adata[real_cells1, :].X + adata[real_cells2, :].X) / 2
    doublets = sc.AnnData(doublets)
    doublets.obs_names = ['X'+str(i) for i in range(n_doublets)]
    doublets.var_names = adata.var_names
    
    if anno_by is not None:
        annotations = adata.obs[anno_by]
    else:
        annotations = None
    
    if annotations is not None:
        assert isinstance(annotations, pd.Series) , "annotations must be a character series"
        assert len(annotations) == n_real_cells, "annotations and seu must have the same length"
        assert not any(annotations.isna()), "annotations must not contain any missing values"

        annotations = annotations.astype("category")
        annotations.index = real_cells  
        doublet_types1 = annotations[real_cells1]
        doublet_types2 = annotations[real_cells2]    

    # Pre-process adata object
    print("Creating adata object...")
    adata_w_doublets = sc.concat([adata,doublets])

    print("Normalizing adata object...")
    sc.pp.normalize_total(adata_w_doublets)
    sc.pp.log1p(adata_w_doublets)
    
    print("Finding variable genes...")
    #sc.pp.highly_variable_genes(adata_w_doublets)
    sc.pp.highly_variable_genes(adata_w_doublets, min_mean=0.0125, max_mean=3, min_disp=0.5)
    adata_w_doublets.raw = adata_w_doublets
    adata_w_doublets = adata_w_doublets[:, adata_w_doublets.var.highly_variable]
    
    print("Scaling data...")
    sc.pp.scale(adata_w_doublets)

    print("Running PCA...")
    sc.tl.pca(adata_w_doublets, svd_solver='arpack',n_comps=nPCs)
    pca_coords = adata_w_doublets.obsm['X_pca']
    
    # Compute PC distance matrix
    print("Calculating PC distance matrix...")
    dist_mat = np.linalg.norm(pca_coords[:, None] - pca_coords, axis=2)

    # Compute pANN
    print("Computing pANN...")
    pANN = np.zeros(n_real_cells)
    neighbor_types = None
    if annotations is not None:
        #neighbor_types = np.zeros((n_real_cells, len(np.unique(annotations))))
        neighbor_types = pd.DataFrame(np.zeros((n_real_cells, len(np.unique(annotations)))),
                              columns=annotations.value_counts().index.values.tolist(),
                              index=real_cells
                             )

    k = round(adata_w_doublets.n_obs * pK)
    for i in range(n_real_cells):
        neighbors = np.argsort(dist_mat[i])
        neighbors = neighbors[1:(k + 1)]
        pANN[i] = len(neighbors[neighbors > n_real_cells]) / k

        if annotations is not None:
            neighbors_that_are_doublets = neighbors[neighbors > n_real_cells]
            if len(neighbors_that_are_doublets) > 0:
                dbl_idx = neighbors_that_are_doublets-n_real_cells
                neighbor_types.iloc[i,:] = doublet_types1[dbl_idx].value_counts().reindex(neighbor_types.columns,fill_value=0)+\
                doublet_types2[dbl_idx].value_counts().reindex(neighbor_types.columns,fill_value=0)
                neighbor_types.iloc[i,:] = neighbor_types.iloc[i,:]/sum(neighbor_types.iloc[i,:])
            #else:
            #    neighbor_types[i] = np.nan

    print("Classifying doublets...")
    classifications = np.repeat("Singlet", n_real_cells)
    top_doublets_idx = np.argsort(-pANN)[:nExp]
    classifications[top_doublets_idx] = "Doublet"
    
    #adata.obs[f"DF.pANN_{pN}_{pK}_{nExp}"] = pANN
    #adata.obs[f"DF.classifications_{pN}_{pK}_{nExp}"] = classifications
    adata.obs["DF.pANN"] = pANN
    adata.obs["DF.classifications"] = classifications

    if annotations is not None:
        adata.obs_names_make_unique()
        for ct in np.unique(annotations):
            #adata.obs[f"DF.doublet.contributors_{pN}_{pK}_{nExp}_{ct}"] = neighbor_types[ct]
            adata.obs["DF.doublet.contributors_"+ct] = neighbor_types[ct]
            
    if inplace:
        return adata
    else:
        meta = adata.obs[[s for s in adata.obs.columns if s.startswith('DF.')]].copy()
        adata.obs.drop(columns=[s for s in adata.obs.columns if s.startswith('DF.')])
        return meta



def paramSweep_v3(adata, nPCs=10, num_cores=1):
    
    # Set pN-pK param sweep ranges
    pK = [0.0005, 0.001, 0.005] + list(np.arange(0.01, 0.31, 0.01))  # top closest cells to count pseudo-doublets
    pN = list(np.arange(0.05, 0.31, 0.05))   # percent of pseudo-doublets  

    # Remove pK values with too few cells
    # Hypothetical method to get number of rows in seu's metadata
    min_cells = round(adata.n_obs / (1-0.05) - adata.n_obs)
    pK_test = [round(val * min_cells) for val in pK]
    pK = [pK[i] for i, val in enumerate(pK_test) if val >= 1]

    # Extract pre-processing parameters from original data analysis workflow
    # orig_commands = seu.get_commands()  # Hypothetical method

    # Down-sample cells to 10000 (when applicable) for computational efficiency
    if adata.n_obs > 100000:
        real_cells = random.sample(adata.obs_names.values.tolist(), 1000)
        data = adata[real_cells,:].copy() # Hypothetical method
    else:
        real_cells = adata.obs_names
        data = adata.copy() # Hypothetical method

    #n_real_cells = data.shape[0]
    n_real_cells = data.n_obs

    if num_cores > 1:
        pool = Pool(processes=num_cores)
        output2 = pool.map(parallel_paramSweep_v3, [(i,n_real_cells, real_cells, pK, pN, data, nPCs) for i in range(len(pN))])
        pool.close()
        pool.join()
    else:
        output2 = [parallel_paramSweep_v3(i,n_real_cells, real_cells, pK, pN, data, nPCs) for i in range(len(pN))]

    # Write parallelized output into list
    sweep_res_list = []
    for i in range(len(output2)):
        for j in range(len(output2[i])):
            sweep_res_list.append(output2[i][j])

    # Assign names to list of results
    name_vec = []
    for pN_val in pN:
        for pK_val in pK:
            name_vec.append(f"pN_{pN_val}_pK_{pK_val}")

    return dict(zip(name_vec, sweep_res_list))




def parallel_paramSweep_v3(n, n_real_cells, real_cells, pK, pN, data, nPCs):
    '''
    Sweep all pK given pN[n]
    '''
    
    sweep_res_list = []
    list_ind = 0

    # Make merged real-artificial data
    print(f"Creating artificial doublets for pN = {pN[n]*100}%")
    n_doublets = round(n_real_cells / (1 - pN[n]) - n_real_cells)
    real_cells1 = np.random.choice(real_cells, size=n_doublets, replace=True)
    real_cells2 = np.random.choice(real_cells, size=n_doublets, replace=True)
    doublets = (data[real_cells1, :].X + data[real_cells2, :].X) / 2
    doublets = sc.AnnData(doublets)
    doublets.obs_names = ['X'+str(i) for i in range(n_doublets)]
    doublets.var_names = data.var_names
    data_wdoublets = sc.concat([data,doublets])

    sc.pp.normalize_total(data_wdoublets, target_sum=1e4)
    sc.pp.log1p(data_wdoublets)
    sc.pp.highly_variable_genes(data_wdoublets, min_mean=0.0125, max_mean=3, min_disp=0.5)
    data_wdoublets = data_wdoublets[:, data_wdoublets.var.highly_variable]
    sc.pp.scale(data_wdoublets, max_value=10)
    sc.tl.pca(data_wdoublets, svd_solver='arpack',n_comps=nPCs)

    # Compute PC distance matrix
    print("Calculating PC distance matrix...")
    pca_coord = data_wdoublets.obsm['X_pca'] #seu_wdoublets[:, PCs].values
    n_cells = pca_coord.shape[0]
    dist_mat = distance_matrix(pca_coord, pca_coord)#[:n_real_cells, :]


    # Pre-order PC distance matrix prior to iterating across pK for pANN computations
    print("Defining neighborhoods...")
    dist_order_mat = np.zeros([n_real_cells,n_real_cells])
    for i in range(n_real_cells):
        dist_order_mat[:, i] = np.argsort(dist_mat[:, i])[:n_real_cells]

    # Trim PC distance matrix for faster manipulations
    ind = round(n_cells * max(pK)) + 5
    dist_order_mat = dist_order_mat[:ind, :]

    # Compute pANN across pK sweep
    print("Computing pANN across all pK...")
    for k in range(len(pK)):
        #print(f"pK = {pK[k]}...")
        pk_temp = round(n_cells * pK[k])
        pANN = pd.DataFrame(np.zeros((n_real_cells, 1), dtype=int), columns=['pANN'], index=real_cells)
        list_ind += 1

        #for i in range(n_real_cells):
        #    neighbors = dist_order_mat[1:(pk_temp + 1), i]
        #    pANN.iloc[i, 0] = len(np.where(neighbors > n_real_cells)[0]) / pk_temp
        pANN.iloc[:, 0] = (dist_order_mat[1:(pk_temp + 1),:] > n_real_cells).sum(0)/pk_temp
        sweep_res_list.append(pANN)
    
    return sweep_res_list


def find_pK(sweep_stats,vis=True):
    # Implementation for data without ground-truth doublet classifications
    if "AUC" not in sweep_stats.columns:
        # Initialize data structure for results storage
        bc_mvn = pd.DataFrame(columns=["ParamID", "pK", "MeanBC", "VarBC", "BCmetric"])
        bc_mvn["pK"] = sorted(sweep_stats["pK"].unique())
        bc_mvn["ParamID"] = np.arange(1, len(bc_mvn) + 1)

        # Compute bimodality coefficient mean, variance, and BCmvn across pN-pK sweep results
        for i, pK_val in enumerate(bc_mvn["pK"]):
            ind = sweep_stats[sweep_stats["pK"] == pK_val].index
            bc_mvn.at[i, "MeanBC"] = np.mean(sweep_stats.loc[ind, "BCreal"])
            bc_mvn.at[i, "VarBC"] = np.var(sweep_stats.loc[ind, "BCreal"])
            bc_mvn.at[i, "BCmetric"] = np.mean(sweep_stats.loc[ind, "BCreal"]) / np.var(sweep_stats.loc[ind, "BCreal"])
        if vis:
            # Plot for visual validation of BCmvn distribution
            plt.figure(figsize=(6, 4))
            plt.plot(bc_mvn["ParamID"], bc_mvn["BCmetric"], marker='o', color='#41b6c4', markersize=6)
            plt.xlabel("ParamID")
            plt.ylabel("BCmetric")
            plt.show()

        return bc_mvn

    # Implementation for data with ground-truth doublet classifications
    if "AUC" in sweep_stats.columns:
        # Initialize data structure for results storage
        bc_mvn = pd.DataFrame(columns=["ParamID", "pK", "MeanAUC", "MeanBC", "VarBC", "BCmetric"])
        bc_mvn["pK"] = sorted(sweep_stats["pK"].unique())
        bc_mvn["ParamID"] = np.arange(1, len(bc_mvn) + 1)

        # Compute bimodality coefficient mean, variance, and BCmvn across pN-pK sweep results
        for i, pK_val in enumerate(bc_mvn["pK"]):
            ind = sweep_stats[sweep_stats["pK"] == pK_val].index
            bc_mvn.at[i, "MeanAUC"] = np.mean(sweep_stats.loc[ind, "AUC"])
            bc_mvn.at[i, "MeanBC"] = np.mean(sweep_stats.loc[ind, "BCreal"])
            bc_mvn.at[i, "VarBC"] = np.var(sweep_stats.loc[ind, "BCreal"])
            bc_mvn.at[i, "BCmetric"] = np.mean(sweep_stats.loc[ind, "BCreal"]) / np.var(sweep_stats.loc[ind, "BCreal"])
        
        if vis:
            # Plot for visual validation of BCmvn distribution
            plt.figure(figsize=(6, 4))
            plt.plot(bc_mvn["ParamID"], bc_mvn["MeanAUC"], marker='o', color='black', linestyle='dotted', markersize=6, label="Mean AUC")
            plt.xlabel("ParamID")
            plt.ylabel("Mean AUC")
            plt.twinx()
            plt.plot(bc_mvn["ParamID"], bc_mvn["BCmetric"], marker='o', color='#41b6c4', markersize=6, label="BCmetric")
            plt.ylabel("BCmetric")
            plt.legend(loc="upper right")
            plt.show()

        return bc_mvn



def bimodality_coefficient(values, bins=30):
    _, edges, _ = binned_statistic(values, values, statistic='count', bins=bins)
    n = len(edges)
    mid = n // 2
    first_half = np.sum(edges[:mid])
    second_half = np.sum(edges[mid:])
    bc = abs(first_half - second_half) / np.sum(edges)
    return bc

def summarizeSweep(sweep_list, GT=False, GT_calls=None):
    # Set pN-pK param sweep ranges
    name_vec = [name.split("_pK_") for name in sweep_list.keys()]
    pN = sorted(set(float(name[0].split("pN_")[1]) for name in name_vec))
    pK = sorted(set(float(name[1]) for name in name_vec))

    # Initialize data structure with or without AUC column, depending on whether ground-truth doublet classifications are available
    if GT:
        sweep_stats = pd.DataFrame(columns=["pN", "pK", "AUC", "BCreal"])
        sweep_stats["pN"] = np.repeat(pN, len(pK))
        sweep_stats["pK"] = np.tile(pK, len(pN))
    else:
        sweep_stats = pd.DataFrame(columns=["pN", "pK", "BCreal"])
        sweep_stats["pN"] = np.repeat(pN, len(pK))
        sweep_stats["pK"] = np.tile(pK, len(pN))

    # Perform pN-pK parameter sweep summary
    for i, (name, res_temp) in enumerate(sweep_list.items()):
        # Use Gaussian kernel density estimation of pANN vector to compute bimodality coefficient
        pANN_values = res_temp["pANN"]
        bc_real = bimodality_coefficient(pANN_values)
        sweep_stats.loc[i, "BCreal"] = bc_real

        if not GT:
            continue

        # If ground-truth doublet classifications are available, perform ROC analysis on logistic regression model trained using pANN vector
        meta = pd.DataFrame(columns=["SinDub", "pANN"])
        meta["SinDub"] = GT_calls
        meta["pANN"] = pANN_values
        train_ind = np.random.choice(range(len(meta)), size=len(meta) // 2, replace=False)
        test_ind = np.setdiff1d(range(len(meta)), train_ind)
        model = LogisticRegression(solver='liblinear')
        model.fit(meta.iloc[train_ind][["pANN"]], meta.iloc[train_ind]["SinDub"])
        prob = model.predict_proba(meta.iloc[test_ind][["pANN"]])[:, 1]
        auc = roc_auc_score(meta.iloc[test_ind]["SinDub"], prob)
        sweep_stats.loc[i, "AUC"] = auc

    return sweep_stats