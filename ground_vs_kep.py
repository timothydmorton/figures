#!/usr/bin/env python

import matplotlib.pyplot as plt
from astropy import constants as const

RJUP = const.R_jup.cgs.value
REARTH = const.R_earth.cgs.value

from settings import tableau20
from data import exo,DR24

DR24.Vmag = DR24.koi_gmag - 0.59*(DR24.koi_gmag - DR24.koi_rmag) - 0.01

fig, ax = plt.subplots(1,1, figsize=(12,8))

ax.spines["top"].set_visible(False)    
ax.spines["right"].set_visible(False)  
#ax.spines["left"].set_visible(False)    
#ax.spines["bottom"].set_visible(False)  
ax.get_xaxis().tick_bottom()  
ax.get_yaxis().tick_left()  

ground_pre_kepler = ~(exo.NAME.str.contains('Kepler') |
                       exo.NAME.str.contains('KOI') |
                       exo.NAME.str.contains('CoRoT')) & (exo.DATE < 2012) & (exo.STARDISCMETH=='Transit')

ax.plot(exo[ground_pre_kepler].V, exo[ground_pre_kepler].R, '+', color='w', ms=11, mew=4, zorder=2)
ax.plot(exo[ground_pre_kepler].V, exo[ground_pre_kepler].R, '+', color=tableau20[0], ms=10, mew=3, zorder=2)
ax.plot(DR24.Vmag, DR24.koi_prad*REARTH/RJUP, 'o', color=tableau20[2], mew=1, alpha=0.3, zorder=1)
ax.set_ylim(ymin=0, ymax=2)
ax.set_xlim(xmin=7.8, xmax=18)
ax.xaxis.set_tick_params(width=3)
ax.yaxis.set_tick_params(width=3)
ax.tick_params(labelsize=16)

ax.set_xlabel('V-band magnitude', size=20);
ax.set_ylabel('Planet radius [Jupiter]', size=20);
fig.savefig('ground_vs_kep.png', transparent=True)