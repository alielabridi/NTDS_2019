Here we can partition `relations.csv` by type of relations in order to obtain a dataframe for each type thanks to `relations_parsing.ipynb`. This allows sequencing the information is to obtain a sampling of the initial database, too large to be processed at once. From this parsing we can get an idea of the difference of these relationships by creating graphs available in the `graphs` folder.
To create the graphs, you can run `relations_sampling.ipynb`.
Then we created gephi projects such as `subsampled_rel1_gephi_project.gephi`

We used force-directed layout to spatialize the graphs : Mutligravity Force Atlas 2 and we dissuade hubs to apply stronger repulsive forces to hubs.

### Dependencies
```
conda install -c anaconda ipywidgets

jupyter nbextension enable --py widgetsnbextension

jupyter labextension install @jupyter-widgets/jupyterlab-manager
```
