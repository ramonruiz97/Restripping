import argparse
import sys
import os.path
from os import path
import yaml

with open(r"info.yaml") as file:
    info = yaml.load(file, Loader=yaml.FullLoader)

#Local Path
local_path = os.path.abspath(os.getcwd())

#parser
parser = argparse.ArgumentParser(description="prepare Re-stripping")

parser.add_argument('mode', 
                    choices=['Bs2JpsiPhi', 'Bs2JpsiPhi_dG0', 'Lb2JpsipK', 'Bd2JpsiKstar'],
                    help='MC mode')

parser.add_argument('year', 
		    help='submission year')

parser.add_argument('stripping', 
		    help='stripping version')

parser.add_argument('polarity', 
                    choices=['MagUp', 'MagDown'],
                    help='submission polarity')

args = parser.parse_args()


#setting variables from argparser
mode = args.mode
year = args.year
stripping = args.stripping
polarity = args.polarity

#Different sintaxis conddDBB and bkgcat ...
pols = {
        'MagDown' : 'md',
        'MagUp' : 'mu'
        }

bkPath = info['Stripping']['samples'][mode][year][stripping]['bk_path'].replace('{{ polarity }}', polarity) 

# #Task configuration
task         = CoreTask()
task.name    = f"{mode}{year}_{stripping}_{pols[polarity]}" 


# #Data
data  = BKQuery(bkPath, dqflag=['OK']).getDataset()


#Step1: Re-stripping 
trf1 = CoreTransform(name="Restripping")
trf1.application = GaudiExec(platform = 'x86_64-centos7-gcc62-opt' ,directory = f"./DaVinciDev_{info['Stripping']['DaVinci'][year]}")
if "Bd" in mode:
  trf1.application.options = [f'stripping/data_options_{mode}_{year}_{stripping}_{pols[polarity]}.py',  'stripping/stripping_setup_Bd.py'] 
else:
  trf1.application.options = [f'stripping/data_options_{mode}_{year}_{stripping}_{pols[polarity]}.py',  'stripping/stripping_setup.py'] 
trf1.addInputData(data)
trf1.submit_with_threads = True
trf1.splitter = SplitByFiles(filesPerJob=1)
trf1.backend = Dirac()
trf1.backend.settings['BannedSites'] = ['LCG.Beijing.cn', 'LCG.CPPM.fr']
trf1.outputfiles = [DiracFile('*.dst')]
task.appendTransform(trf1)

#Step2: Making some tuples 
trf2 = CoreTransform(name="Making tuples",backend=Dirac())
trf2.application = GaudiExec(platform = 'x86_64_v2-centos7-gcc10-opt' ,directory="./DaVinciDev_v45r8")
trf2.inputfiles = [LocalFile(os.path.join(local_path, 'tuples/tuple_maker.py'))]
d = TaskChainInput()
d.input_trf_id = trf1.getID()
trf2.addInputData(d)
if "Bd" in mode:
  trf2.application.options = [f'tuples/samples_stripped_{mode}_{year}_{stripping}_{pols[polarity]}.py', 'tuples/sequence_setup.py', 'tuples/Bd2JpsiKstar.py'] 
elif "Lb2Jpsi" in mode:
  trf2.application.options = [f'tuples/samples_stripped_{mode}_{year}_{stripping}_{pols[polarity]}.py', 'tuples/sequence_setup.py', 'tuples/LbJpsipK.py'] 
else:
  trf2.application.options = [f'tuples/samples_stripped_{mode}_{year}_{stripping}_{pols[polarity]}.py', 'tuples/sequence_setup.py', 'tuples/Bs2JpsiPhi.py'] 
trf2.splitter = GangaDatasetSplitter()
trf2.splitter.files_per_subjob = 1
trf2.outputfiles = [LocalFile("*.root")]
# trf2.submit_with_threads = True
#trf2.postprocessors.append(RootMerger(files = ['DVntuple.root'], ignorefailed = False, overwrite = False))
task.appendTransform(trf2)

#Get job done!
task.float = 2000
task.run()


