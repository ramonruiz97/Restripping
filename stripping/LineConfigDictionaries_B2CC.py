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
################################################################################
##                          S T R I P P I N G  2 9 r 2 p 2                    ##
##                                                                            ##
##  Configuration for B2CC WG                                                 ##
##  Contact person: Muzzetto Piera        (piera.muzzetto@cern.ch)            ##
################################################################################

from GaudiKernel.SystemOfUnits import *

######################################################################
## StrippingB2JpsiHHBs2Jpsif0PrescaledLine (MicroDST)
## StrippingB2JpsiHHBs2JpsiKstarLin(MicroDST)
## StrippingB2JpsiHHLb2JpsipHLine(MicroDST)
## StrippingB2JpsiHHBs2Jpsif0Line (FullDST)
## StrippingB2JpsiHHBs2Jpsif0KaonLine(FullDST)
## StrippingB2JpsiHHBs2Jpsif0wsLine(FullDST)
## -------------------------------------------------------------------
## Lines defined in StrippingB2JpsiHH.py
## Authors: Liming Zhang, Xuesong Liu
## Last changes made by Xuesong Liu
######################################################################

B2JpsiHH = {
    "BUILDERTYPE": "B2JpsiHHConf",
    "CONFIG"     : {
                   "Bs2Jpsif0Prescale" : 0.3,
			 "DTF_CTAU"		   : 0.0598,
                   "HLTCuts"           : "HLT_PASS_RE('Hlt2DiMuonJPsiDecision')",
                   "JpsiMassWindow"    : 80,
                   "MVACut"            : "-0.1",
                   "TRCHI2DOF"         : 5,
                   "VCHI2PDOF"         : 10,
			 "PROBNNk"		   : 0.05,
			 "PROBNNp"		   : 0.05,
			 "PROBNNpi"		   : 0.05,
			 "PIDKforKaon"	   : 0.0,
			 "PIDKforPion"	   : 10.0,
			 "PIDpforProton"	   : 0.0,
			 "PIDKpforKaon"	   : -10.0,
			 "PIDpKforProton"	   : -10.0,
                   "XmlFile"           : "$TMVAWEIGHTSROOT/data/Bs2Jpsif0_BDT_v1r1.xml"
                   },
    "STREAMS"    : {
                   "Dimuon"   : [
                                "StrippingB2JpsiHHBs2Jpsif0Line",
                                "StrippingB2JpsiHHBs2Jpsif0KaonLine",
                                "StrippingB2JpsiHHBs2Jpsif0wsLine"
                                ],
                   "Leptonic" : [
                                "StrippingB2JpsiHHBs2Jpsif0PrescaledLine",
                                "StrippingB2JpsiHHBs2JpsiKstarLine",
                                "StrippingB2JpsiHHLb2JpsipHLine"
                                ]
                   },
    "WGs": [ "B2CC" ]
    }


#############################################################################################
## StrippingBetaSBu2JpsiKDetachedLine (FullDST)
## StrippingBetaSBd2JpsiKstarDetachedLine (FullDST)
## StrippingBetaSBs2JpsiPhiDetachedLine (FullDST)
## StrippingBetaSBd2JpsiKsDetachedLine (FullDST)
## StrippingBetaSJpsi2MuMuLine (FullDST)
## StrippingBetaSLambdab2JpsiLambdaUnbiasedLine (MicroDST)
## StrippingBetaSBu2JpsiKPrescaledLine (MicroDST)
## StrippingBetaSBs2JpsiPhiPrescaledLine (MicroDST)
## StrippingBetaSBd2JpsiKstarPrescaledLine (MicroDST)
## StrippingBetaSBd2JpsiKsPrescaledLine (MicroDST)
## StrippingBetaSBd2JpsiKsLDDetachedLine (MicroDST)
## StrippingBetaSBs2JpsiKstarWideLine (MicroDST)
## ----------------------------------------------------------------------------
## Lines defined in StrippingB2JpsiXforBeta_s.py
## Authors: Greig Cowan, Juan Palacios, Francesca Dordei, Carlos Vazquez Sierra, Xuesong Liu
## Last changes made by Xuesong Liu
#############################################################################################

BetaS = {
        "BUILDERTYPE": "B2JpsiXforBeta_sConf",
        "CONFIG"     : { "DTF_CTAU": 0.0598,
                         "Bd2JpsiKsPrescale": 1.0,
                         "Bd2JpsiKstarPrescale": 1.0,
                         "Bs2JpsiPhiPrescale": 1.0,
                         "Bu2JpsiKPrescale": 1.0,
                         "DaughterPT": 1000,
                         "HLTCuts": "HLT_PASS_RE('Hlt2DiMuonJPsiDecision')",
                         "Jpsi2MuMuPrescale": 0.04,
                         "JpsiMassWindow": 80,
				         "PIDKCuts": -999.,
				         "PIDpiCuts": 999.,
                         "TRCHI2DOF": 5,
                         "VCHI2PDOF": 10
                       },
        "STREAMS"    : { "Dimuon"   : [ "StrippingBetaSBu2JpsiKDetachedLine",
                                        "StrippingBetaSBd2JpsiKstarDetachedLine",
                                        "StrippingBetaSBs2JpsiPhiDetachedLine",
                                        "StrippingBetaSJpsi2MuMuLine",
                                        "StrippingBetaSBd2JpsiKsDetachedLine"
                                      ],
                         "Leptonic" : [ "StrippingBetaSBu2JpsiKPrescaledLine",
                                        "StrippingBetaSBs2JpsiPhiPrescaledLine",
                                        "StrippingBetaSBd2JpsiKstarPrescaledLine",
                                        "StrippingBetaSBd2JpsiKsPrescaledLine",
                                        "StrippingBetaSBd2JpsiKsLDDetachedLine",
                                        "StrippingBetaSBs2JpsiKstarWideLine",
                                        "StrippingBetaSLambdab2JpsiLambdaUnbiasedLine"
                                      ]
                       },
        "WGs"        : [ "B2CC" ]
        }

