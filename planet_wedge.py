#!/usr/bin/env python
import sys
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.interpolate import UnivariateSpline as interpolate

from settings import tableau20
from data import exo

m_nep = 0.0539531012
r_nep = 0.35219064

# Set dates for KOIs
# KOI -> 1609: 2011
# -> 2841: 2012
# -> 3149: 2012.5
# -> 4914: 2013
# -> 6251: 2014
# -> 7620: 2015
B11 = exo.KOI < 1610# & kepname
Q6 = exo.KOI <= 2841# & kepname
Q8 = exo.KOI <= 3149# & kepname
Q12 = exo.KOI <= 4914# & kepname
Q16 = exo.KOI <= 6251# & kepname
Q17 = exo.KOI <= 7620# & kepname

exo.loc[Q17, 'DATE'] = 2015
exo.loc[Q16, 'DATE'] = 2014
exo.loc[Q12, 'DATE'] = 2013
exo.loc[Q8, 'DATE'] = 2012.5
exo.loc[Q6, 'DATE'] = 2012
exo.loc[B11, 'DATE'] = 2011

kepname = (exo.NAME.str.contains('Kepler')).values
koiname = (exo.NAME.str.contains('KOI')).values

kepler = exo[kepname].copy()
koi = exo[koiname].copy()
all_kepler = exo[koiname | kepname].copy()
no_kepler = exo[~(kepname | koiname)].copy()

def cum_draw(df=exo,color='k',mindate=1995,maxdate=2015,ax=None,norm=False,fill=True, kois=False,
             alpha=0.2,interp=False,kepler=False,kepsmall=False,label=None,xylabel=(0.1,0.8),
            zorder=0):
    if ax is None:
        fig, ax = plt.subplots(1,1)
    else:
        fig = ax.figure

    dates = np.sort(df.DATE)
    ds = np.unique(dates).astype(float)
    ns = np.zeros(len(ds))
    for i,d in enumerate(ds):
        ns[i] = (dates<=d).sum()
    if norm:
        ns /= ns.max()
        ns *= norm
    
    if interp:
        dgrid = np.arange(mindate,maxdate,0.1)
        fn = interpolate(ds,ns,s=0)
        y1 = fn(dgrid)
        y2 = -y1
    else:
        dgrid = ds
        y1 = ns
        y2 = -ns
    #ax.plot(dgrid,y1,color=color)
    #ax.plot(dgrid,y2,color=color)
    ax.fill_between(dgrid,y1,y2,alpha=alpha,color=color, zorder=zorder)
    ax.set_xlim(xmin=mindate,xmax=maxdate)
    ax.set_yticks([])
    
    date_ticks = np.arange(mindate,maxdate+1,2)
    
    #for d in date_ticks:
    #    ax.axvline(d, ls=':', color='k', alpha=0.2)
    ax.set_xticks(date_ticks)
    ax.tick_params(labelsize=16)
    
    ax.spines["top"].set_visible(False)    
    ax.spines["bottom"].set_visible(False)    
    ax.spines["right"].set_visible(False)    
    ax.spines["left"].set_visible(False)  
    
    ax.get_xaxis().tick_bottom()    
    ax.xaxis.set_tick_params(width=3, length=10)
    
    if label is not None:
        label = '%s (%i)' % (label,ns.max())
        pl.annotate(label,xy=xylabel,xycoords='axes fraction',fontsize=18,color=color)

    return fig


if __name__=='__main__':
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument('--nosmall', action='store_true')

    args = parser.parse_args()

    if args.nosmall:
        small_m = 0
        small_r = 0
    else:
        small_m = m_nep
        small_r = r_nep

    no_kepler_small = no_kepler.query('MASS < {}'.format(small_m))
    all_kepler_small = all_kepler.query('R < {}'.format(small_r))

    fig, ax = plt.subplots(1,1, figsize=(12,8))

    subsets = [no_kepler, no_kepler_small, all_kepler, all_kepler_small]
    
    n = len(subsets)

    for i,d in enumerate(subsets):
        fig = cum_draw(d, ax=ax, color=tableau20[i], alpha=1, zorder=-len(d));

    tag = ''
    if args.nosmall:
        tag = '_nosmall'
    filename = 'planet_wedge{}.png'.format(tag)

    fig.savefig(filename, transparent=True)
    