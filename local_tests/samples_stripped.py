rom Configurables import DaVinci



#13144011

DaVinci().InputType = 'DST'
DaVinci().Simulation = True
DaVinci().Lumi = not DaVinci().Simulation
DaVinci().EvtMax = -1
DaVinci().DataType = '2017'
DaVinci().CondDBtag = 'sim-20190430-1-vc-md100' 
DaVinci().DDDBtag = 'dddb-20170721-3'
DaVinci().TupleFile = 'DV_tuple.root'
DaVinci().PrintFreq = 1000

from GaudiConf import IOHelper

IOHelper().inputFiles([
    './SelAllStreams.localprod_bstojpsiphi.dst'
], clear=True)
