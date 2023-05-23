activation = lambda x: x.activation
unhappiness = lambda x: x.unhappiness
salience = lambda x: x.salience
quality_and_activation = lambda x: x.quality * x.activation

unchunkedness = lambda x: x.unchunkedness
uncorrespondedness = lambda x: x.uncorrespondedness
unlabeledness = lambda x: x.unlabeledness
unrelatedness = lambda x: x.unrelatedness

chunking_salience = lambda x: x.chunking_salience
corresponding_salience = lambda x: x.corresponding_salience
labeling_salience = lambda x: x.labeling_salience
relating_salience = lambda x: x.relating_salience
