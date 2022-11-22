import matplotlib.pyplot as plt
import numpy as np

def graph_category_distribution(feature, varying_color = False, bar_cmap = 'GnBu', **kwargs):
    counts = feature.value_counts()
    fig, ax = plt.subplots()
    bar_colors = plt.get_cmap(bar_cmap)(counts.values / np.max(counts.values))
    ax.set_ylabel(feature.name.capitalize())
    ax.set_xlabel("Occurences")
    ax.set_title("Distribution of {}".format(feature.name))
    ax.barh(counts.index, counts.values, color=bar_colors, **kwargs)
    plt.show()