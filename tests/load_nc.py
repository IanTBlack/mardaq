import numpy as np
import xarray as xr
import matplotlib.pyplot as plt

from mardaq.core import wavelength_to_rgb
import matplotlib

file = '/media/sel/flowthrough/data/netcdf/acs_test20230613h.nc'
acs_ds = xr.open_dataset(file, group = 'acs_data')
tsg_ds = xr.open_dataset(file, group = 'tsg_data')
gps_ds = xr.open_dataset(file, group = 'gps_data')
sw_ds = xr.open_dataset(file, group = 'filtration_data')


new_c_wvls = np.arange(np.ceil(acs_ds.wavelength_c.min()),np.floor(acs_ds.wavelength_c.max()),1)
new_a_wvls = np.arange(np.ceil(acs_ds.wavelength_a.min()),np.floor(acs_ds.wavelength_a.max()),1)
acs_interp = acs_ds.interp({'wavelength_c':new_c_wvls,'wavelength_a': new_a_wvls})

X1 = np.array(acs_interp.wavelength_a.values)
Y1 = np.array(acs_interp.time.values).astype(np.int64)
X1,Y1 = np.meshgrid(X1,Y1)
Z1 = np.array(acs_interp.a.values)

X2 = np.array(acs_interp.wavelength_c.values)
Y2 = np.array(acs_interp.time.values).astype(np.int64)
X2,Y2 = np.meshgrid(X2,Y2)
Z2 = np.array(acs_interp.c.values)



fig = plt.figure(figsize = (11,8.5))
grid = (1,2)

ax1 = plt.subplot2grid(grid, (0,0), colspan = 1, rowspan = 1, projection = '3d')
surf1 = ax1.plot_surface(X1,Y1,Z1, cmap = 'jet', antialiased = True)
# ax1.set_xlabel('Wavelength (nm)')
# ax1.set_ylabel('Time')
# ax1.set_zlabel(r'Absorption ($\frac{1}{m}$)')

ax2 = plt.subplot2grid(grid, (0,1), colspan = 1, rowspan = 1, projection = '3d')
surf2 = ax2.plot_surface(X2,Y2,Z2, cmap = 'jet', antialiased = True)
# ax2.set_xlabel('Wavelength (nm)')
# ax2.set_ylabel('Time')
# ax2.set_zlabel(r'Attenuation ($\frac{1}{m}$)')

plt.show()

fig, ax = plt.subplots(1,1,figsize = (11,8.5))
for t in acs_interp.time.values:
    _ds = acs_interp.sel(time = t)
    ax.plot(_ds.wavelength_a, _ds.a)

plt.show()



# combo_ds = xr.concat([acs_interp, tsg_ds, gps_ds, sw_ds], dim = 'time', combine_attrs = 'drop_conflicts')
# combo_ds = combo_ds.sortby('time')

# binned_ds = combo_ds.resample({'time': '1S'}).mean()

