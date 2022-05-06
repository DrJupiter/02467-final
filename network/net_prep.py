#%%
from itertools import count
import pandas as pd
import pickle
import numpy as np
from time import perf_counter as counter
import matplotlib.pyplot as plt
import re

import networkx as nx
import netwulf as nw

from collections import defaultdict

from sympy import degree

#%%
# df_uk_ru = pd.read_pickle("only_ru_uk_data.pkl")
user_df = pd.read_pickle("./../preprocessing/dfs/user_trans_senti_ru_uk.pkl")
#%%
user_df
#%%
N_tweets_p_person = []
for tweed_ids in user_df["tweet_ids"]:
    lis = []
    for id in tweed_ids:
        if id is not None:
            lis.append(id)
    N_tweets_p_person.append(len(lis))

sum(N_tweets_p_person)

#%%


re_quote = r"\'(.*?)\'"

def get_graph(small = False):

    edges = defaultdict(int)
    for i,(user_id,parents,mentions) in enumerate(zip(user_df.index,user_df["parent_ids"],user_df["mentions"])):
        
        ids = []
        for par in parents:
            if par is not None:
                ids.append(int(par))

        for ment in mentions:
            if ment != []:
                ids += [int(m[0]) for m in ment]

        for target_id in set(ids):
            if str(target_id) in user_df.index or not small:
                edges[(int(user_id),target_id)] += 1

    dG_func = nx.DiGraph()
    dG_func.add_edges_from(list(edges))
    return dG_func

dG_small = get_graph(small = True)
dG_big = get_graph(small = False)


#%%

## GET for directed

def get_graph_info(dG):
    N_edges = len(dG.edges)
    N_nodes = len(dG.nodes)

    print(f"N nodes: {N_nodes}\nN_edges: {N_edges}")

    dG_dens = nx.density(dG)

    print(f"Graph density: {dG_dens}")

    avg_in_degree = np.mean(list(dict(dG.in_degree()).values()))
    avg_out_degree = np.mean(list(dict(dG.out_degree()).values()))

    print(f"avg in degree: {avg_in_degree}\navg out degree: {avg_out_degree}")

    median_in_degree = np.median(list(dict(dG.in_degree()).values()))
    median_out_degree = np.median(list(dict(dG.out_degree()).values()))

    print(f"median in degree: {median_in_degree}\nmedian out degree: {median_out_degree}")

    max_in_degree = sorted(list(dict(dG.in_degree()).values()))[-5:]
    max_out_degree = sorted(list(dict(dG.out_degree()).values()))[-5:]

    print(f"top 5 in degree: {max_in_degree}\ntop 5 out degree: {max_out_degree}")

get_graph_info(dG_small)

#%%
# x_i = np.array(dG.in_degree)[:,1].reshape(-1,1)
# x_o = np.array(dG.out_degree)[:,1].reshape(-1,1)

# degrees = np.hstack((x_i,x_o))
# sort_idx = np.argsort(degrees[:,1],axis=0)
# sorted_degrees = degrees[sort_idx]
# # sorted_degrees

# fig,ax = plt.subplots(figsize = (15,5))
# ax.plot(np.cumsum(sorted_degrees[:,0]),"-o", label = "in degree", ms = 1)
# ax.plot(np.cumsum(sorted_degrees[:,1]),"-o", label = "out degree", ms = 1)

# # ax.set_yscale("symlog")


# ax.legend()
# fig.show()


# ax.plot(sorted(dG.in_degree))


#%%

def get_degree_group_info(dG):
    x_i = np.array(dG.in_degree)[:,1].reshape(-1,1)
    x_o = np.array(dG.out_degree)[:,1].reshape(-1,1)

    colours = ["grey","red","blue","black","lightgray"]
    x_c = []
    x_g = {}
    groups = [[],[],[],[],[]]
    for id in np.array(dG.out_degree)[:,0]:
        if str(id) in user_df.index:
            idx = user_df.loc[str(id)]["anti-war-class"]
            if not np.isnan(idx):
                x_c.append(colours[int(idx)])
                x_g[id] = colours[int(idx)]
                groups[int(idx)].append(id)
            else:
                x_c.append(colours[-1])
                x_g[id] = colours[-1]
                groups[-1].append(id)
            
        else:
            x_c.append(colours[0])
            x_g[id] = colours[0]
            groups[0].append(id)

    return x_i, x_o ,x_c, x_g, groups

def in_out_plot(dG,sorted=False):

    x_i, x_o ,x_c, x_g, groups = get_degree_group_info(dG)
    tweet_colours_ordered = np.array(x_c)
    degrees = np.hstack((x_i,x_o))
    if sorted:
        sort_idx = np.argsort(degrees[:,0],axis=0)
        sorted_degrees = degrees[sort_idx]
        degrees = sorted_degrees

    fig,ax = plt.subplots(figsize = (25,25))
    n1 =np.random.normal(np.zeros(len(degrees)),0.1)
    n2 =np.random.normal(np.zeros(len(degrees)),0.1)
    ax.scatter(degrees[:,0]+n1,degrees[:,1]+n2,color = tweet_colours_ordered)

    ax.set_xscale("symlog")
    ax.set_yscale("symlog")
    ax.set_xlabel("in degree",fontsize = 25)
    ax.set_ylabel("out degree",fontsize = 25)

in_out_plot(dG_small)

#%%
## Visualize network

def visualize_net(dG):
    x_i, x_o ,x_c, x_g, groups = get_degree_group_info(dG)
    for k, v in dG.nodes(data=True):
        v['group'] = x_g[k]

    nw.visualize(dG)

visualize_net(dG_small)


#%%
import seaborn as sns
sns.set_theme(style="white", palette='pastel', font = 'Arial', font_scale=1)

def modularity_tests(dG, N = 10000):

    x_i, x_o ,x_c, x_g, groups = get_degree_group_info(dG)
    uG = dG.to_undirected(reciprocal = False)

    real_modularity = nx.community.modularity(uG,groups)

    random_modularities = []
    for _ in range(N):
        g = nx.double_edge_swap(uG)
        random_modularities.append( nx.community.modularity(g,groups))

    rand_modul_mean = np.mean(random_modularities)
    rand_modul_std = np.std(random_modularities)

    # fig,ax = plt.subplots()
    ax = sns.histplot(random_modularities,kde=True)
    ax.axvline(real_modularity,color="black",label="True modularity")

    ax.legend()
    ax.set_title("Modularity of random network (double swap algorithm)")
    ax.set_ylabel("Number of networks with the given modularity")
    ax.set_xlabel("Modularity")
    print(f"Modularity for random nets: {rand_modul_mean} pm {rand_modul_std}")

modularity_tests(dG_small,N=10000)
#%%


# confusion matrix??
import community as lou

def get_louvain_graph(dG, visualize = False):
    uG = dG.to_undirected(reciprocal = False)
    lou_partition = lou.best_partition(uG) 
    lou_mod = lou.modularity(lou_partition,uG)
    lou_mod
    
    uG_lou = uG
    for k, v in uG_lou.nodes(data=True):
        v['group'] = lou_partition[k]

    if visualize:
        nw.visualize(uG_lou)

    return uG_lou

ug_small_lou = get_louvain_graph(dG_small, visualize = False)