import pandas as pd
import os

#exo = pd.read_csv('data/exoplanets.csv')
#exo.to_hdf('data/exoplanets.h5','df')
exo = pd.read_hdf('data/exoplanets.h5', 'df')
DR24 = pd.read_hdf(os.path.expanduser('~/.keputils/q1_q17_dr24_koi.h5'), 'q1_q17_dr24_koi')