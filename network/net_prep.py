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
1281277547251142657 in user_df.index

#%%
def common_member(a, b):
    a_set = set(a)
    b_set = set(b)
    if (a_set & b_set):
        return True 
    else:
        return False

#%%
N_tweets_p_person = []
for tweed_ids in user_df["tweet_ids"]:
    lis = []
    for id in tweed_ids:
        print(id)
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

G = nx.DiGraph()

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
        mention_list = re.findall(re_quote,ment)
        if mention_list != []:
            ids += [int(m) for m in mention_list[::2]]
        # print(m[::2])

    # print(ids)
    ll += len(set(ids))
    for target_id in set(ids):
        # print(target_id)
        if target_id in user_df.index:
            if target_id == 393190461:
                f = 22
                ged = True
            edges[(user_id,target_id)] += 1
            if user_id == target_id:
                print(user_id,target_id)
                c+= 1
            cc += 1
            if ged == True:
                f = 33



print(counter()-start)
print("ll",ll)
print("c",c)
print("cc",cc)
#%%

user_df.loc[393190461]
edges[(393190461,1497838731314843650)]
#%%
type(int(user_df.iloc[0,1][0]))
# type(user_df.iloc[0,0][0])


#%%

# laver graf mellem alle der har komminikation mellem hinanden

uG = G.to_undirected(reciprocal = True)
# uG = G.to_undirected(reciprocal = False)




# #%%
# # check if it hsa the correct sum
# sum(N_tweets_p_person) == sum(sum(sum(adjacency_matrix)))/2

# #%%
# plt.imshow(np.sum(adjacency_matrix,axis=2), cmap='hot', interpolation='nearest')
# plt.show()

#%%

## GET for directed

# total number of edges
# total number of nodes

# density of network

# stats for in and out degrees (avg, median osv.)
# List most active users (out degree)
# List most popular useres (in degree)
# in vs out degree for all users

tG = nx.DiGraph()
edges = [(1,2,1),(2,3,2),(3,1,3),(1,1,2)]
tG.add_weighted_edges_from(edges)


# M = nx.adjacency_matrix(G).todense()

# plt.imshow(M, cmap='hot', interpolation='nearest')

# N_edges = len(G.edges)
# N_nodes = len(G.nodes)

# G_dens = nx.density(G)

# avg_in_degree = np.mean(list(dict(G.in_degree()).values()))
# avg_out_degree = np.mean(list(dict(G.out_degree()).values()))

# median_in_degree = np.median(list(dict(G.in_degree()).values()))
# median_out_degree = np.median(list(dict(G.out_degree()).values()))



#%%

## GET for undirected

# total number of edges
# total number of nodes

# density of network
# modualrity of network


## Visualize network

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