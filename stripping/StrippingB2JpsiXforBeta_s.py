###############################################################################
# (c) Copyright 2000-2019 CERN for the benefit of the LHCb Collaboration      #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "COPYING".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
# $Id: StrippingB2JpsiXforBeta_s.py,v 1.3 2010-09-05 21:31:13 wouter Exp $
'''
Module for construction of B->JpsiX roadmap lifetime unbiased 
stripping Selections and StrippingLine.
Provides functions to build Bs, Jpsi, Phi selections.
Provides class Bs2JpsiPhiConf, which constructs the Selections and 
StrippingLines given a configuration dictionary.
Exported symbols (use python help!):
   B2JpsiXLines
'''

__author__ = ['Greig Cowan', 'Juan Palacios', 'Francesca Dordei', 'Carlos Vazquez Sierra', 'Xuesong Liu']
__date__ = '26/05/2017'
__version__ = '$Revision: 4.0$'

__all__ = ('B2JpsiXforBeta_sConf','default_config')

from Gaudi.Configuration import *
from GaudiConfUtils.ConfigurableGenerators import FilterDesktop, CombineParticles
from CommonParticles.Utils import updateDoD
from StandardParticles import StdLoosePions
from StandardParticles import StdLooseKaons
from StandardParticles import StdAllLooseKaons, StdAllLooseMuons
from StandardParticles import StdAllNoPIDsKaons, StdAllNoPIDsMuons, StdAllNoPIDsPions 
from StandardParticles import StdNoPIDsKaons, StdNoPIDsMuons
from PhysSelPython.Wrappers import Selection, DataOnDemand, MergedSelection
from StrippingConf.StrippingLine import StrippingLine
from StrippingUtils.Utils import LineBuilder
from GaudiKernel.SystemOfUnits import MeV

default_config = {
    'NAME'              : 'BetaS',
    'WGs'               : ['B2CC'],
    'BUILDERTYPE'       : 'B2JpsiXforBeta_sConf',
    'CONFIG'    : {
                         'TRCHI2DOF'                 :       5
		     ,	 'DTF_CTAU'			     :       0.2*0.299
                 ,       'JpsiMassWindow'            :       80
                 ,       'DaughterPT'                :       1000
                 ,       'VCHI2PDOF'                 :       10
                 ,       'HLTCuts'                   :       "HLT_PASS_RE('Hlt2DiMuonJPsiDecision')"
		     ,	 'PIDKCuts'			     :	 -999.
		     ,	 'PIDpiCuts'		     :	 999.
                 ,       'Jpsi2MuMuPrescale'         :       0.04   # 2017: 0.04 2016: 0.074  2015: 0.3 2011: 0.014, 2012: 0.075
                 ,       'Bd2JpsiKstarPrescale'      :       1.0     # 2017: 1.0 2016: 1.0 2015: 1.0 2011: 0.065, 2012: 0.29
                 ,       'Bd2JpsiKsPrescale'         :       1.0     # 2017: 1.0 2016: 1.0 2015: 1.0 2011: 1.0, 2012: 1.0
                 ,       'Bs2JpsiPhiPrescale'        :       1.0     # 2017: 1.0 2016: 1.0 2015: 1.0 2011: 0.13, 2012: 0.62
                 ,       'Bu2JpsiKPrescale'          :       1.0     # 2017: 1.0 2016: 1.0 2015: 1.0 2011: 0.04, 2012: 0.2
                         },
    'STREAMS' : {
        'Leptonic' : [
         'StrippingBetaSBu2JpsiKPrescaledLine',
         'StrippingBetaSBs2JpsiPhiPrescaledLine',
         'StrippingBetaSBd2JpsiKstarPrescaledLine',
         'StrippingBetaSBd2JpsiKsPrescaledLine',
         'StrippingBetaSBd2JpsiKsLDDetachedLine',
         'StrippingBetaSBs2JpsiKstarWideLine',
         'StrippingBetaSLambdab2JpsiLambdaUnbiasedLine'
        ],
        'Dimuon' : [
         'StrippingBetaSBu2JpsiKDetachedLine',
         'StrippingBetaSBd2JpsiKstarDetachedLine',
         'StrippingBetaSBs2JpsiPhiDetachedLine',
         'StrippingBetaSJpsi2MuMuLine',
         'StrippingBetaSBd2JpsiKsDetachedLine'
        ]
    }
    }

### Lines stored in this file:
# StrippingBetaSJpsi2MuMuLine
# StrippingBetaSBu2JpsiKDetachedLine
# StrippingBetaSBu2JpsiKPrescaledLine
# StrippingBetaSBs2JpsiPhiPrescaledLine
# StrippingBetaSBs2JpsiPhiDetachedLine
# StrippingBetaSBd2JpsiKstarPrescaledLine
# StrippingBetaSBd2JpsiKstarDetachedLine
# StrippingBetaSBd2JpsiKsPrescaledLine
# StrippingBetaSBd2JpsiKsDetachedLine
# StrippingBetaSBd2JpsiKsLDDetachedLine
# StrippingBetaSBs2JpsiKstarWideLine
# StrippingBetaSLambdab2JpsiLambdaUnbiasedLine

class B2JpsiXforBeta_sConf(LineBuilder) :
    __configuration_keys__ = default_config['CONFIG'].keys()

    def __init__(self, name, config) :
        LineBuilder.__init__(self, name, config)
        self.name = name
        self.config = config
	
        #### Input selections:

        # ------------------------------------------------------------ J/Psi:
        
        self.WideJpsiList = DataOnDemand(Location = "Phys/StdMassConstrainedJpsi2MuMu/Particles")

        self.JpsiList = self.createSubSel( OutputList = 'NarrowJpsiForBetaS' + self.name,
                                           InputList = self.WideJpsiList,
                                           Cuts = "(PFUNA(ADAMASS('J/psi(1S)')) < %(JpsiMassWindow)s * MeV)" % self.config)

        self.MuonList = self.createSubSel( OutputList = 'MuonsForBetaS' + self.name, 
                                           InputList = DataOnDemand( Location =  "Phys/StdLooseMuons/Particles"),
                                           Cuts = "(PT > 0.5*GeV)")

        self.JpsiForCheck = self.createCombinationsSel( OutputList = "JpsiFoCheckForBetaS" + self.name,
                                                                 DaughterLists = [ StdAllNoPIDsMuons, StdAllNoPIDsMuons ],
                                                                 DecayDescriptors = [ "J/psi(1S) -> mu+ mu-" ],
                                                                 DaughterCuts = { "mu-"  : " (PT > 500 *MeV) " % self.config,
                                                                                  "mu+"  : " (PT > 500 *MeV) " % self.config},
                                                                 PreVertexCuts = "(ADAMASS('J/psi(1S)') < 150.*MeV) & (ADOCACHI2CUT(20, ''))",
                                                                 PostVertexCuts = "(VFASPF(VCHI2) < 16) & (MFIT)",
                                                                 ReFitPVs = False )
    

        # ------------------------------------------------------------ Kaons:
       
        self.KaonList = self.createSubSel( OutputList = "KaonsForBetaS" + self.name,
                                           InputList = DataOnDemand(Location = "Phys/StdNoPIDsKaons/Particles"),
                                           Cuts = "(TRCHI2DOF < %(TRCHI2DOF)s ) & (PIDK > %(PIDKCuts)s )" % self.config )  

        self.NoIPKaonList = self.createSubSel( OutputList = "NoIPKaonsForBetaS" + self.name,
                                               InputList = DataOnDemand(Location = "Phys/StdAllNoPIDsKaons/Particles"),
                                               Cuts = "(TRCHI2DOF < %(TRCHI2DOF)s ) & (PIDK > %(PIDKCuts)s )" % self.config )

        # -------------------------------------------------------------- Phi:

        self.PhiList = self.createCombinationsSel( OutputList = "Phi2KKForBetaS" + self.name,
                                                  DaughterLists = [ StdAllNoPIDsKaons, StdAllNoPIDsKaons ],
                                                  DecayDescriptors = [ "phi(1020) -> K+ K-" ],
                                                  PreVertexCuts = "(AM < 1100.*MeV) & (ADOCACHI2CUT(30, ''))",
                                                  PostVertexCuts = "(in_range(980,M,1060))" \
                                          "& (PT > 500.*MeV) " \
                                          "& (VFASPF(VCHI2) < 25)" \
                                          "& (MAXTREE('K+'==ABSID, TRCHI2DOF) < %(TRCHI2DOF)s )" % self.config,
                                          ReFitPVs = False)

        # ------------------------------------------------------------ Kstar:
        
        self.KstarList = self.createCombinationsSel( OutputList = "Kstar2KpiForBetaS" + self.name,
                                            DaughterLists = [ StdAllNoPIDsKaons, StdAllNoPIDsPions ],
                                            DecayDescriptors = [ "[K*(892)0 -> K+ pi-]cc"],
                                            PreVertexCuts = "(APT > 500.*MeV) & (ADAMASS('K*(892)0') < 300.*MeV) & (ADOCACHI2CUT(30, ''))",
                                            PostVertexCuts = "(in_range(826,M,966))" \
                                            "& (PT > 1300.*MeV) " \
                                            "& (VFASPF(VCHI2) < 25)" \
                                            "& (MAXTREE('K+'==ABSID,  TRCHI2DOF) < %(TRCHI2DOF)s )" \
                                            "& (MAXTREE('pi-'==ABSID, TRCHI2DOF) < %(TRCHI2DOF)s )" \
							                % self.config, ReFitPVs = False)

        self.DetachedKstarWideList = self.createCombinationsSel( OutputList = "DetachedKstarWideListForBetaS" + self.name,
                                                                 DaughterLists = [ StdLooseKaons, StdLoosePions ],
                                                                 DecayDescriptors = [ "[K*(892)0 -> K+ pi-]cc", "[K*_0(1430)0 -> K+ pi-]cc"  ],
                                                                 DaughterCuts = { "pi-" : " (PT > 500 *MeV) & (PIDK < %(PIDpiCuts)s ) & (TRGHOSTPROB < 0.8)" % self.config,
                                                                                  "K+"  : " (PT > 500 *MeV) & (PIDK > %(PIDKCuts)s ) & (TRGHOSTPROB < 0.8)" % self.config},
                                                                 PreVertexCuts = "(in_range(750,AM,1900))  & (ADOCACHI2CUT(30, ''))",
                                                                 PostVertexCuts = "(VFASPF(VCHI2) < 25)",
                                                                 ReFitPVs = False )

        # --------------------------------------------------------------- KS:
        
        self.KsListLoose = MergedSelection("StdLooseKsMergedForBetaS" + self.name,
                                           RequiredSelections = [DataOnDemand(Location = "Phys/StdLooseKsDD/Particles"),
                                                                 DataOnDemand(Location = "Phys/StdLooseKsLL/Particles")] )

        self.KsList = self.createSubSel(OutputList = "KsForBetaS" + self.name,
                                        InputList = self.KsListLoose,
                                        Cuts = "(VFASPF(VCHI2)<20) & (BPVDLS>5)")

        self.KsLDList = self.createSubSel( OutputList =  "KsLDForBetaS" + self.name,
                                           InputList = DataOnDemand(Location = "Phys/StdLooseKsLD/Particles"),
                                           Cuts = "(VFASPF(VCHI2)<20) & (BPVDLS>5)")

        # ----------------------------------------------------------- Lambda:

        self.LambdaListLoose = MergedSelection("StdLooseLambdaMergedForBetaS" + self.name,
                                               RequiredSelections =  [DataOnDemand(Location = "Phys/StdLooseLambdaDD/Particles"),
                                                                      DataOnDemand(Location = "Phys/StdLooseLambdaLL/Particles")])
        self.LambdaList =  self.createSubSel(OutputList = "LambdaForBetaS" + self.name,
                                             InputList = self.LambdaListLoose ,
                                             Cuts = "(MAXTREE('p+'==ABSID, PT) > 500.*MeV) & (MAXTREE('pi-'==ABSID, PT) > 100.*MeV) & (ADMASS('Lambda0') < 15.*MeV) & (VFASPF(VCHI2) < 20)")

        # -------------------------------------------------------------------

        self.makeInclJpsi()
        self.makeBd2JpsiKsLD()
        self.makeBu2JpsiK()
        self.makeBs2JpsiPhi()
        self.makeBs2JpsiKstarWide()
        self.makeBd2JpsiKstar()
        self.makeBd2JpsiKs()
        self.makeLambdab2JpsiLambda()

    ### Stripping lines:

    # ---------------------- Inclusive J/Psi:

    def makeInclJpsi( self ):
        '''Inclusive J/psi. We keep it for as long as we can.'''
        Jpsi2MuMuForBetasLine = StrippingLine( self.name + "Jpsi2MuMuLine", algos = [ self.WideJpsiList ], HLT2 = self.config['HLTCuts'], prescale = self.config["Jpsi2MuMuPrescale"],RequiredRawEvents = ["Trigger","Muon","Calo","Rich","Velo","Tracker","HC"] )
        self.registerLine(Jpsi2MuMuForBetasLine)

    # --------------------------- Bu->J/PsiK:

    def makeBu2JpsiK( self ):
        Bu2JpsiK = self.createCombinationSel( OutputList = "Bu2JpsiK" + self.name,
                                 DecayDescriptor = "[B+ -> J/psi(1S) K+]cc",
                                 DaughterLists = [ self.WideJpsiList, self.NoIPKaonList ],
                                 DaughterCuts  = {"K+": "(PT > 500.*MeV)" },
                                 PreVertexCuts = "in_range(5050,AM,5550)",
                                 PostVertexCuts = "in_range(5150,M,5450) & (VFASPF(VCHI2PDOF) < %(VCHI2PDOF)s)" % self.config )

        Bu2JpsiKPrescaledLine = StrippingLine( self.name + "Bu2JpsiKPrescaledLine", algos = [ Bu2JpsiK ] , HLT2 = self.config['HLTCuts'], prescale = self.config["Bu2JpsiKPrescale"], EnableFlavourTagging = True, RequiredRawEvents = ["Trigger","Muon","Calo","Rich","Velo","Tracker","HC"])#, MDSTFlag = True )

        Bu2JpsiKDetached = self.createSubSel( InputList = Bu2JpsiK, OutputList = Bu2JpsiK.name() + "Detached" + self.name,
                                              Cuts = "(CHILD('Beauty -> ^J/psi(1S) X', PFUNA(ADAMASS('J/psi(1S)'))) < %(JpsiMassWindow)s * MeV) & "\
                                              "(DTF_CTAU(0,True) > %(DTF_CTAU)s ) & "\
                                              "(MINTREE('K+'==ABSID, PT) > 500.*MeV)" % self.config )

        Bu2JpsiKDetachedLine  = StrippingLine( self.name + "Bu2JpsiKDetachedLine", algos = [ Bu2JpsiKDetached ], EnableFlavourTagging = False, RequiredRawEvents = ["Trigger","Muon","Calo","Rich","Velo","Tracker","HC"] )
    
        self.registerLine(Bu2JpsiKDetachedLine)
        self.registerLine(Bu2JpsiKPrescaledLine)

    # ------------------------- Bs->J/PsiPhi:

    def makeBs2JpsiPhi( self ):
        Bs2JpsiPhi = self.createCombinationSel( OutputList = "Bs2JpsiPhi" + self.name,
                                   DecayDescriptor = "B_s0 -> J/psi(1S) phi(1020)",
                                   DaughterLists  = [ self.JpsiForCheck, self.PhiList ],
                                   PreVertexCuts = "in_range(5050,AM,5650)",
	                           PostVertexCuts = "in_range(5150,M,5550) & (VFASPF(VCHI2PDOF) < 20)" % self.config ) # for the other particles is 10.
				   
        Bs2JpsiPhiPrescaledLine = StrippingLine( self.name + "Bs2JpsiPhiPrescaledLine", algos = [ Bs2JpsiPhi ] , HLT2 = self.config['HLTCuts'], prescale = self.config['Bs2JpsiPhiPrescale'], EnableFlavourTagging = True , RequiredRawEvents = ["Trigger","Muon","Calo","Rich","Velo","Tracker","HC"] )#, MDSTFlag = True )

        Bs2JpsiPhiDetached = self.createSubSel( InputList = Bs2JpsiPhi,
                                                OutputList = Bs2JpsiPhi.name() + "Detached" + self.name,
                                                Cuts = "(CHILD('Beauty -> ^J/psi(1S) X', PFUNA(ADAMASS('J/psi(1S)'))) < %(JpsiMassWindow)s * MeV) & "\
                                                "(DTF_CTAU(0,True) > %(DTF_CTAU)s )" % self.config )

        Bs2JpsiPhiDetachedLine  = StrippingLine( self.name + "Bs2JpsiPhiDetachedLine", algos = [ Bs2JpsiPhiDetached ], EnableFlavourTagging = False, RequiredRawEvents = ["Trigger","Muon","Calo","Rich","Velo","Tracker","HC"] )
        
        self.registerLine(Bs2JpsiPhiPrescaledLine)
        self.registerLine(Bs2JpsiPhiDetachedLine)

    # -------------------------- Bd->J/PsiK*:

    def makeBd2JpsiKstar( self ):
        Bd2JpsiKstar = self.createCombinationSel( OutputList = "Bd2JpsiKstar" + self.name,
                                     DecayDescriptor = "[B0 -> J/psi(1S) K*(892)0]cc",
                                     DaughterLists  = [ self.JpsiForCheck, self.KstarList ],
                                     PreVertexCuts = "in_range(5050,AM,5550)",
                                     PostVertexCuts = "in_range(5150,M,5450) & (VFASPF(VCHI2PDOF) < 20)" % self.config) # for the other particles is 10.

        Bd2JpsiKstarPrescaledLine = StrippingLine( self.name + "Bd2JpsiKstarPrescaledLine", algos = [ Bd2JpsiKstar ] , HLT2 = self.config['HLTCuts'], prescale = self.config['Bd2JpsiKstarPrescale'], EnableFlavourTagging = True , RequiredRawEvents = ["Trigger","Muon","Calo","Rich","Velo","Tracker","HC"])#, MDSTFlag = True )


        Bd2JpsiKstarDetached = self.createSubSel( InputList = Bd2JpsiKstar,
                                                  OutputList = Bd2JpsiKstar.name() + "Detached" + self.name,
                                                  Cuts = "(CHILD('Beauty -> ^J/psi(1S) X', PFUNA(ADAMASS('J/psi(1S)'))) < %(JpsiMassWindow)s * MeV) & "\
                                                  "(DTF_CTAU(0,True) > %(DTF_CTAU)s )" % self.config )

        Bd2JpsiKstarDetachedLine  = StrippingLine( self.name + "Bd2JpsiKstarDetachedLine",
                                          algos = [ Bd2JpsiKstarDetached ], EnableFlavourTagging = False , RequiredRawEvents = ["Trigger","Muon","Calo","Rich","Velo","Tracker","HC"] )

        self.registerLine(Bd2JpsiKstarPrescaledLine)
        self.registerLine(Bd2JpsiKstarDetachedLine)

    # -------------------------- Bd->J/PsiKS:

    def makeBd2JpsiKs( self ):
        Bd2JpsiKs = self.createCombinationSel( OutputList = "Bd2JpsiKS" + self.name,
                                  DecayDescriptor = "B0 -> J/psi(1S) KS0",
                                  DaughterLists  = [ self.WideJpsiList, self.KsList ],
                                  PreVertexCuts = "in_range(5000,AM,5650)",
                                  PostVertexCuts = "in_range(5150,M,5550) & (VFASPF(VCHI2PDOF) < %(VCHI2PDOF)s)" % self.config
                                  )

        Bd2JpsiKsPrescaledLine = StrippingLine( self.name + "Bd2JpsiKsPrescaledLine", algos = [ Bd2JpsiKs ] , HLT2 = self.config['HLTCuts'], prescale = self.config['Bd2JpsiKsPrescale'], EnableFlavourTagging = True , RequiredRawEvents = ["Trigger","Muon","Calo","Rich","Velo","Tracker","HC"])#, MDSTFlag = True )

        Bd2JpsiKsDetached = self.createSubSel( InputList = Bd2JpsiKs,
                                               OutputList = Bd2JpsiKs.name() + "Detached" + self.name,
                                               Cuts = "(CHILD('Beauty -> ^J/psi(1S) X', PFUNA(ADAMASS('J/psi(1S)'))) < %(JpsiMassWindow)s * MeV) & "\
                                               "(DTF_CTAU(0,True) > %(DTF_CTAU)s )" % self.config)

        Bd2JpsiKsDetachedLine = StrippingLine( self.name + "Bd2JpsiKsDetachedLine",
                                        algos = [ Bd2JpsiKsDetached ], EnableFlavourTagging = False  , RequiredRawEvents = ["Trigger","Muon","Calo","Rich","Velo","Tracker","HC"])#, MDSTFlag = True )

        self.registerLine(Bd2JpsiKsPrescaledLine)
        self.registerLine(Bd2JpsiKsDetachedLine)

    def makeBd2JpsiKsLD( self ):
        Bd2JpsiKsLD = self.createCombinationSel( OutputList = "Bd2JpsiKSLD" + self.name,
                                  DecayDescriptor = "B0 -> J/psi(1S) KS0",
                                  DaughterLists  = [ self.JpsiList, self.KsLDList ],
                                  PreVertexCuts = "in_range(5000,AM,5650)",
                                  PostVertexCuts = "in_range(5150,M,5550) & (VFASPF(VCHI2PDOF) < %(VCHI2PDOF)s)" % self.config
                                  )
        

        Bd2JpsiKsLDDetached = self.createSubSel( InputList = Bd2JpsiKsLD,
                                    OutputList = Bd2JpsiKsLD.name() + "Detached" + self.name,
                                                 Cuts = "(DTF_CTAU(0,True) > %(DTF_CTAU)s )" % self.config)

        Bd2JpsiKsLDDetachedLine = StrippingLine( self.name + "Bd2JpsiKsLDDetachedLine",
                                                 algos = [ Bd2JpsiKsLDDetached ], EnableFlavourTagging = True , RequiredRawEvents = ["Trigger","Muon","Calo","Rich","Velo","Tracker","HC"])#, MDSTFlag = True )

        self.registerLine(Bd2JpsiKsLDDetachedLine)

    # -------------------------- Bs->J/PsiK*:
   
    def makeBs2JpsiKstarWide( self ):
        Bs2JpsiKstarWide      = self.createCombinationSel( OutputList = "Bs2JpsiKstarWide" + self.name,
                                DecayDescriptor = "[B_s~0 -> J/psi(1S) K*(892)0]cc",
                                DaughterLists  = [ self.JpsiList, self.DetachedKstarWideList ],
                                PreVertexCuts = "in_range(5100,AM,5700)",
                                PostVertexCuts = "(VFASPF(VCHI2PDOF) < 10) & (BPVDIRA >0.999) & (BPVVD > 1.5 *mm)" )

        Bs2JpsiKstarWideLine = StrippingLine( self.name + "Bs2JpsiKstarWideLine", algos = [ Bs2JpsiKstarWide ], EnableFlavourTagging = True , RequiredRawEvents = ["Trigger","Muon","Calo","Rich","Velo","Tracker","HC"])#, MDSTFlag = True )

        self.registerLine(Bs2JpsiKstarWideLine)

    # -------------------------- Lb->J/PsiLb:
        
    def makeLambdab2JpsiLambda( self ):
        Lambdab2JpsiLambda = self.createCombinationSel( OutputList = "Lambdab2JpsiLambda" + self.name,
                                    DecayDescriptor = "[Lambda_b0 -> Lambda0 J/psi(1S) ]cc",
                                    DaughterLists  = [ self.JpsiList, self.LambdaList ],
                                    PreVertexCuts = "in_range(5020,AM,6220)",
                                    PostVertexCuts = "in_range(5120,M,6120) & (VFASPF(VCHI2PDOF) < %(VCHI2PDOF)s)" % self.config
                                    )

        Lambdab2JpsiLambdaUnbiasedLine = StrippingLine( self.name + "Lambdab2JpsiLambdaUnbiasedLine", algos = [ Lambdab2JpsiLambda ] , RequiredRawEvents = ["Trigger","Muon","Calo","Rich","Velo","Tracker","HC"])
    
        self.registerLine(Lambdab2JpsiLambdaUnbiasedLine)

    ### Common tools:

    def createSubSel( self, OutputList, InputList, Cuts ) :
        '''create a selection using a FilterDesktop'''
        filter = FilterDesktop(Code = Cuts)
        return Selection( OutputList,
                      Algorithm = filter,
                      RequiredSelections = [ InputList ] )

    def createCombinationSel( self, OutputList,
                          DecayDescriptor,
                          DaughterLists,
                          DaughterCuts = {} ,
                          PreVertexCuts = "ALL",
                          PostVertexCuts = "ALL",
                          ReFitPVs = True ) :
        '''create a selection using a ParticleCombiner with a single decay descriptor'''
        combiner = CombineParticles( DecayDescriptor = DecayDescriptor,
                                     DaughtersCuts = DaughterCuts,
                                     MotherCut = PostVertexCuts,
                                     CombinationCut = PreVertexCuts,
                                     ReFitPVs = ReFitPVs)
        return Selection ( OutputList,
                           Algorithm = combiner,
                           RequiredSelections = DaughterLists)
        
    def createCombinationsSel( self, OutputList,
	                  DecayDescriptors,
                          DaughterLists,
                          DaughterCuts = {} ,
                          PreVertexCuts = "ALL",
                          PostVertexCuts = "ALL",
                          ReFitPVs = True ) :
        '''For taking in multiple decay descriptors'''
        combiner = CombineParticles( DecayDescriptors = DecayDescriptors,
                                 DaughtersCuts = DaughterCuts,
                                 MotherCut = PostVertexCuts,
                                 CombinationCut = PreVertexCuts,
                                 ReFitPVs = ReFitPVs)
        return Selection ( OutputList,
                       Algorithm = combiner,
                       RequiredSelections = DaughterLists)

    def filterTisTos( self, name, DiMuonInput, myTisTosSpecs ) :
        from Configurables import TisTosParticleTagger
    
        myTagger = TisTosParticleTagger(name + "_TisTosTagger")
        myTagger.TisTosSpecs = myTisTosSpecs
        
        # To speed it up, TisTos only with tracking system:
        myTagger.ProjectTracksToCalo = False
        myTagger.CaloClustForCharged = False
        myTagger.CaloClustForNeutral = False
        myTagger.TOSFrac = { 4:0.0, 5:0.0 }
        
        return Selection(name + "_SelTisTos",
                     Algorithm = myTagger,
                     RequiredSelections = [ DiMuonInput ] )

