from Configurables import DaVinci



#13144011

DaVinci().InputType = 'DST'
DaVinci().Simulation = True
DaVinci().Lumi = not DaVinci().Simulation
DaVinci().EvtMax = -1
DaVinci().DataType = '2017'
DaVinci().CondDBtag = 'sim-20190430-1-vc-md100' 
DaVinci().DDDBtag = 'dddb-20170721-3'
#DaVinci().HistogramFile = 'DV_stripping_histos.root'
DaVinci().PrintFreq = 1000

from GaudiConf import IOHelper

IOHelper().inputFiles([
    './00092543_00000287_7.AllStreams.dst'
], clear=True)
