# Feature extraction process

In order to extract features from the given dataset it is being preprocessed using a shell script so that the actuall feature extraction in python then can be done easier.

## Preprocessing
The given data, which is already sorted along the column "src" is being fully copied and sorted along the column "dst". The columns "src" and "dst" in the copied dataset are then swapped and the numerical value 10 is added to the last column (5) in order to being able to identify the _doubled_ data. Both files are then being sort merged into a new file which then consist of all edges (in and outgoing) for each node gathered together. Since each edge is therefore listed twice the file size is double, however performing local feature extraction reduces to simple algebraic computations that can be done fast. Furthermore this way of processing the data allows to extract the features from the whole dataset rather than sampling first which would alter the feature space.

## Feature extraction
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
