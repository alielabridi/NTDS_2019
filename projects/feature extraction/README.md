# Feature extraction process

## Strategy
Given the previous projects realised on this dataset it was found that tackling the data in its entirety might be interesting. Therefore not simply considering seven independent graphs but rather finding measures allowing also to specify the intergraph relations. Or in other words the given relations that are assigned to the graph are treated similarly to weight of the edge that can only attain descrete values of a finite set. However, because of the size this means accepting several restrictions on the form of the features. Mainly this consists in restricting to local features.

## Preprocessing
The given dataset (relations.csv) includes the features [day, time\_ms, src, dst, relation]. Since this project is about networks we can remove the time component for our purposes and the convenience of having a smaller dataset (the original dataset is about 25Gb). Furthermore the graph is directed, meaning that every edge has a source node (src) and a destination node (dst). The given data is sorted along the src of the edges. Therefore an operation wanting to compute a feature of the local neighborhood of a node will have to gather all edges where the node appears as dst in the whole dataset. This means sorting 858,247,099 numbers which obviously takes some time. However, this could be done once and then each edge can be stored twice, once grouped next to the src edges and once grouped next to the dst edge. Naturally a flag for each edge as in-going or out-going has to be added in order to still be able to distinguish between them which can conveniently be done storage efficiently by adding for example the value 10 to the relations of the in-going relations. Thus allowing a simple modulo 10 operation to retrieve relation and direction of the edge.

## Feature extraction
### Full dataset
The preprocessed file is being loaded in individual chunks and in each chunk the features are calculated.

The following features are extracted:

* dtot: degree of a node
* dout: degree for outgoing edges (deg_in = deg_tot - deg_out)
* duni: number of unique neighbors of a node
* n_bidir: number of bidirectional (in & out) relations

### sampling_extractions.ipynb
To extract other features we chose to use networkx. In order to create graphs, some relations needed to be sampled.
This notebook has an **exploration** part where we analyse :
* degree distributions,
* in/out_degree distributions,
* average clustering coefficients,
of the graphs (one graph per relation), define them. Furthermore it has an **extraction** part where we extract the features for the classification. The features depend on the relation type.

#### Dependencies for sampling_extractions.ipynb
```
conda install -c anaconda ipywidgets

jupyter nbextension enable --py widgetsnbextension

jupyter labextension install @jupyter-widgets/jupyterlab-manager
```
