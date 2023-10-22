# -*- coding: utf-8 -*-

import torch
import torch.nn.functional as F
import numpy as np
import networkx as nx
#
from .GIN import GIN
from .Utils import read_data_from_file, read_data_from_nx

class PyMulSim:

  def __init__(self, verbose=False):
    self.verbose = verbose
    self.channels = 64
    self.epochs = 1
    pass

  def __compute_similarities(self, data_multi_graph1:[], data_multi_graph2:[], graph1_node_labels:[]=None, graph2_node_labels:[]=None):

    num_layers = len(data_multi_graph1)

    # GNN model
    model = GIN(in_channels=self.channels, hidden_channels=self.channels, out_channels=self.channels, num_layers=num_layers)

    if self.verbose: print(model)
    
    output = {}
    #output_old = [] 
    for layer_i in range(0, num_layers):
      if self.verbose: print("-- Processing Layer " + str(layer_i))
      layer_i_graph1 = data_multi_graph1[layer_i]
      layer_i_graph2 = data_multi_graph2[layer_i]

      optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
      for epoch in range(self.epochs):
          model.train()
          optimizer.zero_grad()
          embeddings_layer_i_graph1 = model(layer_i_graph1.x, layer_i_graph1.edge_index, layer_i_graph1.edge_index_inter)
          embeddings_layer_i_graph2 = model(layer_i_graph2.x, layer_i_graph2.edge_index, layer_i_graph2.edge_index_inter)
          loss = F.mse_loss(embeddings_layer_i_graph1, embeddings_layer_i_graph2)
          #loss = custom_loss(embeddings_layer_i_graph1, embeddings_layer_i_graph2)
          loss.backward()
          optimizer.step()
          if self.verbose: print("Epoch %d (loss=%d)" % (epoch, float(loss)))

      with torch.no_grad():
        model.eval()

        if self.verbose: print("--- Node embedding...")
        # Using GNNAlignmentModel for processing aligned features of each layer
        embeddings_layer_i_graph1 = model(layer_i_graph1.x, layer_i_graph1.edge_index, layer_i_graph1.edge_index_inter)
        embeddings_layer_i_graph2 = model(layer_i_graph2.x, layer_i_graph2.edge_index, layer_i_graph2.edge_index_inter)

        # Normalization
        if self.verbose: print("--- Normalization...")
        embeddings_layer_i_graph1 = embeddings_layer_i_graph1 / embeddings_layer_i_graph1.norm(dim=1)[:, None]
        embeddings_layer_i_graph2 = embeddings_layer_i_graph2 / embeddings_layer_i_graph2.norm(dim=1)[:, None]

        # Calculate Jaccard similarity between node neighborhoods
        jaccard_similarities = np.zeros((len(embeddings_layer_i_graph1), len(embeddings_layer_i_graph2)))
        for i, embedding_i in enumerate(embeddings_layer_i_graph1):
            for j, embedding_j in enumerate(embeddings_layer_i_graph2):
                neighbors_i = set(np.where(layer_i_graph1.edge_index[0] == i)[0])
                neighbors_j = set(np.where(layer_i_graph2.edge_index[0] == j)[0])
                union_size = len(neighbors_i.union(neighbors_j))
                if union_size == 0:
                    jaccard_sim = 0.0
                else:
                    jaccard_sim = len(neighbors_i.intersection(neighbors_j)) / union_size
                jaccard_similarities[i, j] = jaccard_sim

        # Print all Jaccard similarities
        for i in range(len(embeddings_layer_i_graph1)):
            for j in range(len(embeddings_layer_i_graph2)):
                node_name_graph1 = graph1_node_labels[layer_i][i]
                node_name_graph2 = graph2_node_labels[layer_i][j]
                similarity = jaccard_similarities[i, j]
                if similarity > 0:
                  output[(node_name_graph1, node_name_graph2)] = similarity
                  # output_old.append([node_name_graph1, node_name_graph2, similarity])
                  if self.verbose: print(f"{node_name_graph1} (Graph1) - {node_name_graph2} (Graph2) : {similarity}")

    return output # np.asarray(output_old), 

  ####
        
  def compute_similarities_from_file(self,source_path:str, target_path:str, layer_ids:[], interlayer_ids:[]):
    data_multi_graph1, data_multi_graph2, graph1_node_labels, graph2_node_labels = read_data_from_file(source_path, target_path, layer_ids, interlayer_ids, self.channels)
    return self.__compute_similarities(data_multi_graph1, data_multi_graph2, graph1_node_labels, graph2_node_labels)

  def compute_similarities_from_nx(self,graph1_layers:nx.Graph, graph2_layers:nx.Graph, layer_ids:[], interlayer_ids:[]):
    data_multi_graph1, data_multi_graph2, graph1_node_labels, graph2_node_labels = read_data_from_nx(graph1_layers, graph2_layers, layer_ids, interlayer_ids, self.channels)
    return self.__compute_similarities(data_multi_graph1, data_multi_graph2, graph1_node_labels, graph2_node_labels)
  