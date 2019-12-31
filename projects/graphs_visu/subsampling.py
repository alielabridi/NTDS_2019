import pandas as pd
import numpy as np
import networkx as nx
from ipywidgets import IntProgress
from IPython.display import display


def get_samples_from_relation(file, num_of_nodes = 20000):
    '''
    getting samples from the graph by randomly picking a source node
    looking for its neighbors. Then getting the neighbors of its neighbors.
    By iteration we obtain a subsample of the relations.

    Parameters:
    file (string): the .csv file path of the relation dataframe
    num_of_nodes (int): threshold representing the minimum of nodes expected in the sampled dataframe
    Returns:
    pd.Dataframe, pd.Dataframe: users dataframe, relation dataframe
    '''
    np.random.seed(1)
    relation_df= pd.read_csv(file,delimiter=',').rename(columns = {'Unnamed: 0':'index'}).set_index('index')
    usersdata = pd.read_csv('data/usersdata.csv', delimiter = '\t', names = ['userId', 'sex', 'timePassedValidation', 'ageGroup', 'label'])

    c_relations = relation_df.groupby(['src','dst']).agg({'time_ms':'sum'})
    c_relations.reset_index(inplace = True)

    node_list = []
    neighbors = [c_relations.sample()['src'].values[0]]
    node_list.extend(neighbors)
    while len(node_list) < num_of_nodes:
        neighbors = c_relations[c_relations['src'].isin(neighbors)]['dst'].tolist() + c_relations[c_relations['dst'].isin(neighbors)]['src'].tolist()
        node_list = list(set(node_list).union(set(neighbors)))
    print('number of users acquired: {}'.format(len(node_list)))
    subrels = c_relations[(c_relations['src'].isin(node_list)) & (c_relations['dst'].isin(node_list))]
    subrels.loc[:,'time_s'] = subrels['time_ms']/1000.
    fusers = usersdata[usersdata.userId.isin(node_list)]

    nodes = fusers
    edges = subrels[['src', 'dst', 'time_s']].rename(columns = {'time_s':'weight'})
    nodes.reset_index(level=0, inplace=True)
    nodes = nodes.drop(columns={'index'})
    nodes.reset_index(level=0, inplace=True)
    nodes = nodes.rename(columns = {'index':'node_idx'})
    uid2idx = nodes[['node_idx', 'userId']]
    uid2idx = uid2idx.set_index('userId')
    edges_renumbered = edges.join(uid2idx, on = 'src').join(uid2idx, on = 'dst', rsuffix = '_dst').drop(columns = ['src', 'dst'])
    edgelist = edges_renumbered[['node_idx','node_idx_dst','weight']]
    return fusers, edgelist

def get_samples_from_relation_with_chunks(file, num_of_nodes=20000, chunksize = 10000):
    '''
    getting samples from the graph by picking the first node as a source 
    looking for its neighbors. Then getting the neighbors of its neighbors.
    By iteration we obtain a subsample of the relations. This methods uses
    chunks to process on huge .csv files.

    Parameters:
    file (string): the .csv file path of the relation dataframe
    num_of_nodes (int): threshold representing the minimum of nodes expected in the sampled dataframe
    chunksize (int): number of chunks
    Returns:
    pd.Dataframe, pd.Dataframe: users dataframe, relation dataframe
    '''
    usersdata = pd.read_csv('data/usersdata.csv', delimiter = '\t', names = ['userId', 'sex', 'timePassedValidation', 'ageGroup', 'label'])

    f = IntProgress(min=0, max=chunksize, description = 'Process') # instantiate the bar
    display(f) # display the bar

    node_list = []
    neighbors = [pd.read_csv(file,delimiter=',', nrows = 1)['src'].values[0]]

    node_list.extend(neighbors)
    print('Start sampling')
    while len(node_list) < num_of_nodes:
        count = 0
        previous = neighbors
        neighbors = []
        for chunk in pd.read_csv(file,iterator=True,delimiter=',', chunksize=chunksize):
            f.value = count # signal to increment the progress bar
            count += 1
            neighbors.extend(chunk[chunk['src'].isin(previous)]['dst'].tolist() + chunk[chunk['dst'].isin(previous)]['src'].tolist())
            node_list.extend(neighbors)
            node_list = list(set(node_list))
        print('number of users acquired: {}'.format(len(node_list)))
    print('number of users finally acquired: {}'.format(len(node_list)))

    print('sub sampling relations:')
    relation_df= pd.read_csv(file,iterator=True,delimiter=',', chunksize=chunksize)
    subrels = pd.concat([chunk[(chunk['src'].isin(node_list)) & (chunk['dst'].isin(node_list))] for chunk in relation_df])

    subrels = subrels.rename(columns={'Unnamed: 0':'index'}).set_index('index').groupby(['src','dst']).agg({'time_ms':'sum'})
    subrels.reset_index(inplace = True)
    subrels.loc[:,'time_s'] = subrels['time_ms']/1000.
    fusers = usersdata[usersdata.userId.isin(node_list)]

    nodes = fusers
    edges = subrels[['src', 'dst', 'time_s']].rename(columns = {'time_s':'weight'})
    nodes.reset_index(level=0, inplace=True)
    nodes = nodes.drop(columns={'index'})
    nodes.reset_index(level=0, inplace=True)
    nodes = nodes.rename(columns = {'index':'node_idx'})
    uid2idx = nodes[['node_idx', 'userId']]
    uid2idx = uid2idx.set_index('userId')
    edges_renumbered = edges.join(uid2idx, on = 'src').join(uid2idx, on = 'dst', rsuffix = '_dst').drop(columns = ['src', 'dst'])
    edgelist = edges_renumbered[['node_idx','node_idx_dst','weight']]
    return fusers, edgelist


def create_graph(nodes, edgelist, output):
    '''
    from edgelist, create the .gexf graph for gephi.

    Parameters:
    nodes (pd.Dataframe): nodes attributes
    edgelist (pd.Dataframe): read by networkx
    output (string): saving path for the graph
    '''
    graph = nx.from_pandas_edgelist(edgelist, 'node_idx', 'node_idx_dst', 'weight', create_using=nx.DiGraph())
    attributes = nodes[['ageGroup', 'timePassedValidation', 'label']]
    attributes.rename(columns = {'label':'spammer'}, inplace = True)
    node_props = attributes.to_dict() #, 'timePassedValidation', 'ageGroup'
    for key in node_props:
        nx.set_node_attributes(graph, node_props[key], key)
    nx.write_gexf(graph, output)
