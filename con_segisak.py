import segysak
import pandas as pd
import matplotlib.pyplot as plt
import pathlib
import xarray as xr

from segysak.segy import segy_header_scan
from segysak.segy import segy_loader
from IPython.display import display
from google.colab import drive

drive.mount('/content/drive')
filename = '/content/drive/MyDrive/samples/3D_gathers_pstm_nmo.sgy'
V3D_path = pathlib.Path(filename)

scan = segy_header_scan(long_data)
with pd.option_context("display.max_rows", 91):
    display(scan) #con esto se pintan los metadatos
#en este caso la salida de metadatos tira
#CDP_X=181
#CDP_Y=185
#inline_3d=189
#crossline_3d=193
#shotpoint=197
#entre otros
#esos datos se ingresan a continuación

V3D = xr.open_dataset(
    V3D_path,
    dim_byte_fields={"ILINE_3D":189, "CROSSLINE_3D": 193, "ShotPoint":197},
    extra_byte_fields={"CDP_X":181, "CDP_Y":185 },
)
V3D #esto para ver el iline y xline que se utilizam en la grafica
#en este caso es ILINE_3D=1290 y CROSSLINE_3D=1150

fig, ax1 = plt.subplots(ncols=1, figsize=(15, 8))
V3D.data.transpose("ILINE_3D", "CROSSLINE_3D", "ShotPoint", "samples", transpose_coords=True).sel(
    ILINE_3D=1290, CROSSLINE_3D=1150
).plot(yincrease=False, cmap="seismic_r")
plt.grid("grey")
plt.ylabel("TWT")
plt.xlabel("XLINE")
