import yaml
import sys
import os.path
from os import path
import yaml

with open(r"info.yaml") as file:
    info = yaml.load(file, Loader=yaml.FullLoader)

def modificarLinea(archivo,buscar,reemplazar):
	with open(archivo, "r") as f:
		lines = (line.rstrip() for line in f)
		altered_lines = [reemplazar if line==buscar else line for line in lines]
	with open(archivo, "w") as f:
		f.write('\n'.join(altered_lines) + '\n')

conddb = {}
dddb = {}
pol = ['md', 'mu']


for i in info['Stripping']['samples'].keys():
    conddb[i] = {}; dddb[i] = {} 
    for j in info['Stripping']['samples'][i].keys():
      conddb[i][j] = {}; dddb[i][j] = {} 
      for k in info['Stripping']['samples'][i][j].keys(): 
          dddb[i][j][k] = info['Stripping']['samples'][i][j][k].get('dddb')
          conddb[i][j][k] = {}
          for l in pol:
            conddb[i][j][k][l] = info['Stripping']['samples'][i][j][k].get('conddb').replace('{{ pol }}', l) 
            os.system(f'cp stripping/data_options.py stripping/data_options_{i}_{j}_{k}_{l}.py')
            modificarLinea(f'stripping/data_options_{i}_{j}_{k}_{l}.py', "DaVinci().DataType = '2017'", f"DaVinci().DataType = '{j}'")
            modificarLinea(f'stripping/data_options_{i}_{j}_{k}_{l}.py', "DaVinci().CondDBtag = 'sim-20190430-1-vc-md100'", f"DaVinci().CondDBtag = '{conddb[i][j][k][l]}'")
            modificarLinea(f'stripping/data_options_{i}_{j}_{k}_{l}.py', "DaVinci().DDDBtag = 'dddb-20170721-3'", f"DaVinci().DDDBtag = '{dddb[i][j][k]}'")
            os.system(f'cp stripping/data_options_{i}_{j}_{k}_{l}.py tuples/samples_stripped_{i}_{j}_{k}_{l}.py')
            with open(f'tuples/samples_stripped_{i}_{j}_{k}_{l}.py', 'a') as f:
                 f.write("DaVinci().TupleFile = 'DVntuple.root'\n")





