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

#%%
# df_uk_ru = pd.read_pickle("only_ru_uk_data.pkl")
user_df = pd.read_pickle("./../preprocessing/dfs/user_trans_senti_ru_uk.pkl")

#%%
user_df["president"]
#%%
user_df.loc["2522682982"]


# #%%
# def common_member(a, b):
#     a_set = set(a)
#     b_set = set(b)
#     if (a_set & b_set):
#         return True 
#     else:
#         return False

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
# fig,ax = plt.subplots()
# ax.hist(N_tweets_p_person)
# ax.set_yscale("log")
#%%
# user_df.where(user_df.index == 1498643025475649540)

#%%
# user_df["user_i"] = list(np.arange(len(user_df)))
# N= len(user_df.index)
# adjacency_matrix = np.zeros((N,N,2))

dG = nx.DiGraph()

re_quote = r"\'(.*?)\'"


start = counter()
c = 0
cc = 0
ll = 0
# edges = []
edges = defaultdict(int)
for i,(user_id,parents,mentions) in enumerate(zip(user_df.index,user_df["parent_ids"],user_df["mentions"])):
    
    ids = []
    for par in parents:
        if par is not None:
           ids.append(int(par))

    for ment in mentions:
        if ment != []:
            ids += [int(m[0]) for m in ment]
            # print(i,[int(m[0]) for m in ment])
        # print(m[::2])

    # print(ids)
    ll += len(set(ids))
    for target_id in set(ids):
        if str(target_id) in user_df.index:
            edges[(int(user_id),target_id)] += 1
            if int(user_id) == target_id:
                # print(user_id,target_id)
                c+= 1
            cc += 1




print(counter()-start)
print("ll",ll)
print("c",c)
print("cc",cc)
#%%

dG.add_edges_from(list(edges))

#%%
# nw.visualize(dG)
len(dG.edges())
# uG = G.to_undirected(reciprocal = True)
# len(uG.edges())

#%%

# laver graf mellem alle der har komminikation mellem hinanden

#%%

## GET for directed

# total number of edges
# total number of nodes

# density of network

# stats for in and out degrees (avg, median osv.)
# List most active users (out degree)
# List most popular useres (in degree)
# in vs out degree for all users

M = nx.adjacency_matrix(dG).todense()

fig,ax = plt.subplots(figsize = (10,10))
ax.imshow(M, cmap='hot', interpolation='nearest')
plt.title("Adjacency matric heatmap", fontsize = 22)
plt.xlabel("user number")
plt.ylabel("user number")

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

#%%
#%%

## GET for undirected

# total number of edges
# total number of nodes

# density of network
#%%

## Visualize network

nw.visualize(dG)


#%%

## Random network analysis

# Create random networks, to see if stuff changes
# compare degree distribution to real network
# compare clustering to real network

## Modularity

# compute modularity of graph
# compute modularity of random graph

# double edge swap?
# std and average deviation of the modularity vs the actual modularity (plot modularity for all random networks)

## Communities
# Find communities using the louvian algo
# compare modularity osv with actal graph

# confusion matrix??


#%%