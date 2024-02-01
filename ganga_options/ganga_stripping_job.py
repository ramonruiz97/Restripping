j = Job(name='Stripping ganga job')
myApp = GaudiExec()
myApp.directory = "./DaVinciDev_v42r10"
j.application = myApp
j.application.options = ['data_options.py', 'stripping_setup.py']
j.application.platform = 'x86_64-centos7-gcc62-opt'
bkPath = '/MC/2017/Beam6500GeV-2017-MagDown-Nu1.6-25ns-Pythia8/Sim09g/Trig0x62661709/Reco17/Turbo04a-WithTurcal/Stripping29r2NoPrescalingFlagged/13144011/ALLSTREAMS.DST'
data  = BKQuery(bkPath, dqflag=['OK']).getDataset()
j.inputdata = data[0:2]     # access only the first 2 files of data
j.backend = Dirac()
j.splitter = SplitByFiles(filesPerJob=1)
j.outputfiles = [DiracFile('*.dst')]
j.submit()
