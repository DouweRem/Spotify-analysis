import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.special import gamma

from playlist_download import download_metadata


def gaussian(x, mu, sigma):
    return 1 / (sigma * (2 * np.pi) ** 0.5) * np.exp(-0.5 * ((x - mu) / sigma) ** 2)


def poisson(x, mu):
    return np.exp(-mu) * mu ** x / gamma(x + 1)


def fit_gaussian(array, label, bins=20):
    hist, bins = np.histogram(array, bins=bins, density=True)

    p0 = [np.mean(array), np.std(array)]
    popt, pcov = curve_fit(gaussian, hist, (bins[0] + bins[: -1])/2, p0=p0)

    x = np.linspace(bins[0], bins[-1], 1000)
    y = gaussian(x, *popt)
    plt.plot(x, y, label=label + ' fit')

    print(p0)
    print(f'For {label}, mu = {popt[0]}, sigma = {popt[1]}')
    return popt


def fit_poisson(array, label, bins=20):
    hist, bins = np.histogram(array, bins=bins, density=True)

    p0 = [np.mean(array)]
    popt, pcov = curve_fit(poisson, hist, (bins[0] + bins[: -1])/2, p0=p0)

    x = np.linspace(bins[0], bins[-1], 1000)
    y = poisson(x, *popt)
    plt.plot(x, y, label=label + ' fit')

    print(p0)
    print(f'For {label}, mu = {popt[0]}')
    return popt


douwe = download_metadata('https://open.spotify.com/playlist/3MxcUIKi9Iz1toP2ioB7h8?si=da6bba824d1f4ce8')
prog = download_metadata('https://open.spotify.com/playlist/75viG6EUzwGyN09AxnBd2c?si=69b00b75fdcc4f4b')
chill = download_metadata('https://open.spotify.com/playlist/3WLfY9PJqpptZzo5vKfhzV?si=72c1be4b4e9c4137')
zomer = download_metadata('https://open.spotify.com/playlist/01k1CQah7sqAYvRnO9oT39?si=0da67c75f06b4346')
top2000 = download_metadata('https://open.spotify.com/playlist/04Prkjzzv8Rz1kA3MIZbkO?si=69aa7ef7eb6540f6')

print(f'For Douwe: {round(douwe["duration"].mean()/60000, 2)} m')
print(f'For Prog: {round(prog["duration"].mean()/60000, 2)} m')
print(f'For Chill: {round(chill["duration"].mean()/60000, 2)} m')
print(f'For Zomer: {round(zomer["duration"].mean()/60000, 2)} m')
print(f'For Top 2000: {round(top2000["duration"].mean()/60000, 2)} m')

# plt.hist(douwe['duration']/60000, 50, density=True, label='Douwe', alpha=0.5)
# plt.hist(prog['duration']/60000, 20, density=True, label='Prog', alpha=0.5)
# # plt.hist(chill['duration']/60000, 20, density=True, label='Chill', alpha=0.5)
# # plt.hist(zomer['duration']/60000, 20, density=True, label='Zomer', alpha=0.5)
# plt.hist(top2000['duration']/60000, 20, density=True, label='Top 2000', alpha=0.5)
#
# plt.xlabel('Duration (min)')
# plt.ylabel('Frequency')
# plt.legend()
# plt.grid(alpha=0.4)
# plt.show()

plt.hist(douwe['release_date'], bins=60, density=True, label='Douwe', alpha=0.5)
plt.hist(prog['release_date'], bins=60, density=True, label='Prog', alpha=0.5)
plt.hist(chill['release_date'], bins=60, density=True, label='Chill', alpha=0.5)
plt.hist(zomer['release_date'], bins=60, density=True, label='Zomer', alpha=0.5)
plt.hist(top2000['release_date'], bins=60, density=True, label='Top 2000', alpha=0.5)

plt.xlabel('Release date')
plt.ylabel('Frequency')
plt.legend()
plt.grid(alpha=0.4)
plt.show()
