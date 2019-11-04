import pandas as pd
from pyMCDS import *

# Change things here ***********************************************************

# If file has output00012345*.mat set out_num to '00012345' as a string
out_num = '00003696'
out_dir = 'matlab_example'
# ******************************************************************************

fin = 'output'+out_num+'.xml'

mcds = pyMCDS(fin, out_dir, load_microenv=False)
cell_df = mcds.get_cell_df()

cell_df.to_csv('output'+out_num+'_cells.csv')
