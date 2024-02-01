task = CoreTask(name = 'full phis restripping pipeline')



step0 = CoreTransform( name = 'restripping')
myApp = GaudiExec()
myApp.directory = "./DaVinciDev_v42r10"
myApp.platform = 'x86_64-centos7-gcc62-opt'
myApp.options = ['stripping/data_options.py', 'stripping/stripping_setup.py'] 
step0.application = myApp
bkPath = '/MC/2017/Beam6500GeV-2017-MagDown-Nu1.6-25ns-Pythia8/Sim09g/Trig0x62661709/Reco17/Turbo04a-WithTurcal/Stripping29r2NoPrescalingFlagged/13144011/ALLSTREAMS.DST'
data =  BKQuery(bkPath, dqflag=['OK']).getDataset()
step0.addInputData(data[0:2])
step0.submit_with_threads = True
step0.splitter = SplitByFiles(filesPerJob=10)
step0.backend = Dirac()
#step0.splitter = GangaDatasetSplitter()
#step0.splitter.files_per_subjob = 1
step0.outputfiles = [DiracFile('*.dst')]

task.appendTransform(step0)

step1 = CoreTransform( name = 'tupling' , backend = Dirac())
myApp2 = GaudiExec()
myApp2.directory = "./DaVinciDev_v45r8"
myApp2.platform = 'x86_64_v2-centos7-gcc10-opt'
myApp2.options = [ 'tuples/data_options.py', 'tuples/sequence_setup.py', 'tuples/Bs2JpsiPhi.py'] 
step1.application = myApp2
step1.inputfiles = ['tuples/tuple_maker.py']
step1.submit_with_threads = True 

#d.treat_as_inputfiles = True  
d = TaskChainInput()
d.input_trf_id = step0.getID()
step1.addInputData(d)

step1.splitter = GangaDatasetSplitter()
step1.splitter.files_per_subjob = 1
step1.outputfiles = [LocalFile('stdout'),DiracFile('*.root')]

task.appendTransform(step1)
task.float = 1
task.run()
