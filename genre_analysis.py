import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from playlist_download import download_metadata

df = download_metadata('Douwe')

genres = []

for genre_list in df['genres']:
    for genre in genre_list:
        genres.append(genre)

print(df['genres'][24])


# uniques, counts = np.unique(genres, return_counts=True)
#
#
#
# mask = counts > 4
# print(uniques[mask])
# print(counts[mask])