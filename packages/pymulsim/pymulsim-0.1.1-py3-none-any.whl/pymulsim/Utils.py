# -*- coding: utf-8 -*-

import torch
import torch.nn.functional as F
from torch_geometric.data import Data

import networkx as nx
import numpy as np

"""# Utils"""

def __parse_nx_edgelist(graph, layer_ids, intralayer_ids, in_channels):
  graph_layers = []

  # Layers
  for l in layer_ids:
    layer_edges = [(u,v) for u,v,e in graph.edges(data=True) if e['layer'] == l]
    layer = nx.Graph()
    layer.add_edges_from(layer_edges)
    nx.set_node_attributes(layer, values=np.random.rand(layer.number_of_nodes(), in_channels), name='features')
    graph_layers.append(layer)

  # Interlayer edges
  for layer1, layer2 in zip(graph_layers[:-1], graph_layers[1:]):
    interlayer_edges = [(u,v) for u,v,e in graph.edges(data=True) if e['layer'] in intralayer_ids]
    layer1.add_edges_from(interlayer_edges, interlayer=True)
    layer2.add_edges_from(interlayer_edges, interlayer=True)
    # Featuring all nodes (also nodes in the interlayer edges)
    nx.set_node_attributes(layer1, values=np.random.rand(layer.number_of_nodes(), in_channels), name='features')
    nx.set_node_attributes(layer2, values=np.random.rand(layer.number_of_nodes(), in_channels), name='features')

  # Convert to Data
  data, data_idx_mapping = __layers_to_data_list(graph_layers)
  return data, data_idx_mapping, graph_layers

def __layers_to_data_list(graph_layers):
  data_list = []
  data_idx_mapping = []
  enumerate_start = 0
  for layer in graph_layers:
    data, idx_mapping = __graph_to_data(layer)
    data_list.append(data)
    data_idx_mapping.append(idx_mapping)
    enumerate_start += len(layer.nodes())
  return data_list, data_idx_mapping

def __graph_to_data(graph):
  idx_mapping = { node: idx for idx, node in enumerate(graph.nodes()) }
  edge_index = []
  edge_index_inter = []
  for src, dst in graph.edges():
      if src in idx_mapping and dst in idx_mapping:
          edge_index.append((idx_mapping[src], idx_mapping[dst]))
          if graph[src][dst].get('interlayer', False):
              edge_index_inter.append((idx_mapping[src], idx_mapping[dst]))

  edge_index = torch.tensor(edge_index, dtype=torch.long).t().contiguous()
  edge_index_inter = torch.tensor(edge_index_inter, dtype=torch.long).t().contiguous()

  features_list = list(nx.get_node_attributes(graph, 'features').values())
  x = torch.tensor(np.array(features_list), requires_grad=True) ## eventually, remove requires_grad=True

  data = Data(x=x, edge_index=edge_index, edge_index_inter=edge_index_inter)
  data.validate()
  # inverse mapping for key-value
  idx_mapping = {v : k for k, v in idx_mapping.items()}
  return data, idx_mapping

"""
# Reading data
"""

def read_data_from_nx(graph1_layers:nx.Graph, graph2_layers:nx.Graph, layer_ids:[], interlayer_ids:[], in_channels:int):
  data_multi_graph1, graph1_node_labels, _ = __parse_nx_edgelist(graph1_layers, layer_ids, interlayer_ids, in_channels)
  data_multi_graph2, graph2_node_labels, _ = __parse_nx_edgelist(graph2_layers, layer_ids, interlayer_ids, in_channels)
  return data_multi_graph1, data_multi_graph2, graph1_node_labels, graph2_node_labels

def read_data_from_file(source_path:str, target_path:str, layer_ids:[], interlayer_ids:[], in_channels:int, delimiter:str=" "):
  source = nx.read_edgelist( source_path, delimiter=delimiter, data=True )
  target = nx.read_edgelist( target_path, delimiter=delimiter, data=True )
  return read_data_from_nx(source, target, layer_ids, interlayer_ids, in_channels)