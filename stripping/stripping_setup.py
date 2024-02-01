"""Set up the main and tuple sequences.

The MainSeq sequence is set as the sole member of DaVinci().UserAlgorithms.
It contains:

1. CheckPV algorithm.
2. TrackSmearState algorithm if MC, else TrackScaleState.
3. Tuple sequence, as returned by helpers.tuple_maker.tuple_sequence.

Ntuple algorithms should be added to the TupleSeq sequence, which runs in
non-lazy OR mode.

The DaVinci().Simulation property must be set before this options file is run.
"""
from __future__ import print_function

from Gaudi.Configuration import *

from Configurables import (
    DaVinci,
    GaudiSequencer,
    EventNodeKiller,
    ProcStatusCheck
)
from StrippingConf.Configuration import (
    StrippingConf,
    StrippingStream
)

from StrippingSelections import buildersConf

from StrippingSelections.Utils import lineBuilder, buildStreamsFromBuilder

from DSTWriters.microdstelements import *
from DSTWriters.Configuration import (
    SelDSTWriter,
    stripDSTStreamConf,
    stripDSTElements
)



def apply_stripping():
    confname = 'BetaS'
    stripTESPrefix = 'Strip'
    enablePacking = True

    confs = buildersConf()
    #confs[confname]["CONFIG"]["SigmaPPi0CalPrescale"] = 0.5 ## 
    streams = buildStreamsFromBuilder(confs, confname)

    custom_stream = StrippingStream('AllStreams')
    custom_line = 'StrippingBetaSBs2JpsiPhiDetachedLine'

    for stream in streams:
        for sline in stream.lines:
            if sline.name() == custom_line:
                sline._prescale = 1.0
                custom_stream.appendLines([sline])


    event_node_killer = EventNodeKiller('StripKiller')
    event_node_killer.Nodes = ['/Event/AllStreams', '/Event/Strip']

    from Configurables import ProcStatusCheck
    filterBadEvents = ProcStatusCheck()


    sc = StrippingConf( Streams = [custom_stream],
                    MaxCandidates = 2000,
                    AcceptBadEvents = False,
                    BadEventSelection = filterBadEvents )
    enablePacking = False

    SelDSTWriterElements = {'default': stripDSTElements(pack=enablePacking)}

    input_type=DaVinci().InputType 
    if input_type == "DST":
        print("Checking the extension: DST " , input_type)
        file_extension = '.localprod_bstojpsiphi.dst'
    elif input_type == "LDST":
        print("Checking the extension: LDST ", input_type)
        file_extension = '.localprod_bstojpsiphi.ldst'

    SelDSTWriterConf = {'default': stripDSTStreamConf(pack=enablePacking,
                                                      selectiveRawEvent=False,
                                                      fileExtension=file_extension)}

    dstWriter = SelDSTWriter('MyDSTWriter',
                             StreamConf=SelDSTWriterConf,
                             MicroDSTElements=SelDSTWriterElements,
                             OutputFileSuffix='',
                             SelectionSequences=sc.activeStreams()
                             )

    DaVinci().ProductionType = 'Stripping'
    seq = GaudiSequencer('TupleSeq')
    seq.IgnoreFilterPassed = True
    seq.Members += [event_node_killer, sc.sequence()] + [dstWriter.sequence()]

    return seq




seq = apply_stripping()
DaVinci().UserAlgorithms = [seq]

