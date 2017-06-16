import PhysicsTools.HeppyCore.framework.config as cfg
from PhysicsTools.HeppyCore.framework.config import printComps
from PhysicsTools.HeppyCore.framework.heppy_loop import getHeppyOption
from PhysicsTools.HeppyCore.framework.eventsfwlite import Events

from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator

from CMGTools.H2TauTau.proto.analyzers.TauHLTAnalyzer import TauHLTAnalyzer
from CMGTools.H2TauTau.proto.analyzers.HLTTauTreeProducer import HLTTauTreeProducer

production = getHeppyOption('production', False)

c = ComponentCreator()

ggH135_0 = c.makeMCComponentFromEOS('ggH135_rawaod', 'ggH135_rawaod', '/store/group/phys_tau/HLT2016/HPSatHLT_91X_relax_1p2p/GluGluHToTauTau_M125_13TeV_powheg_pythia8/HPSatHLT/170530_131503/0000/')
ggH135_1 = c.makeMCComponentFromEOS('ggH135_rawaod_1', 'ggH135_rawaod', '/store/group/phys_tau/HLT2016/HPSatHLT_91X_relax_1p2p/GluGluHToTauTau_M125_13TeV_powheg_pythia8/HPSatHLT/170530_131503/0001/')
ggH135_2 = c.makeMCComponentFromEOS('ggH135_rawaod_2', 'ggH135_rawaod', '/store/group/phys_tau/HLT2016/HPSatHLT_91X_relax_1p2p/GluGluHToTauTau_M125_13TeV_powheg_pythia8/HPSatHLT/170530_131503/0002/')
ggH135_3 = c.makeMCComponentFromEOS('ggH135_rawaod_3', 'ggH135_rawaod', '/store/group/phys_tau/HLT2016/HPSatHLT_91X_relax_1p2p/GluGluHToTauTau_M125_13TeV_powheg_pythia8/HPSatHLT/170530_131503/0003/')

# ggH135_0 = c.makeMCComponentFromEOS('ggH135_rawaod', 'ggH135_rawaod', '/store/group/phys_tau/HLT2016/HPSatHLT_91X_relax/GluGluHToTauTau_M125_13TeV_powheg_pythia8/HPSatHLT/170517_130841/0000/')
# ggH135_1 = c.makeMCComponentFromEOS('ggH135_rawaod_1', 'ggH135_rawaod', '/store/group/phys_tau/HLT2016/HPSatHLT_91X_relax/GluGluHToTauTau_M125_13TeV_powheg_pythia8/HPSatHLT/170517_130841/0001/')
# ggH135_2 = c.makeMCComponentFromEOS('ggH135_rawaod_2', 'ggH135_rawaod', '/store/group/phys_tau/HLT2016/HPSatHLT_91X_relax/GluGluHToTauTau_M125_13TeV_powheg_pythia8/HPSatHLT/170517_130841/0002/')
# ggH135_3 = c.makeMCComponentFromEOS('ggH135_rawaod_3', 'ggH135_rawaod', '/store/group/phys_tau/HLT2016/HPSatHLT_91X_relax/GluGluHToTauTau_M125_13TeV_powheg_pythia8/HPSatHLT/170517_130841/0003/')

# ggH135_0 = c.makeMCComponentFromEOS('ggH135_rawaod', 'ggH135_rawaod', '/store/group/phys_tau/HLT2016/HPSatHLT_91X_dm11_relaxmass/GluGluHToTauTau_M125_13TeV_powheg_pythia8/HPSatHLT/170515_141943/0000/')
# ggH135_1 = c.makeMCComponentFromEOS('ggH135_rawaod_1', 'ggH135_rawaod', '/store/group/phys_tau/HLT2016/HPSatHLT_91X_dm11_relaxmass/GluGluHToTauTau_M125_13TeV_powheg_pythia8/HPSatHLT/170515_141943/0001/')
# ggH135_2 = c.makeMCComponentFromEOS('ggH135_rawaod_2', 'ggH135_rawaod', '/store/group/phys_tau/HLT2016/HPSatHLT_91X_dm11_relaxmass/GluGluHToTauTau_M125_13TeV_powheg_pythia8/HPSatHLT/170515_141943/0002/')
# ggH135_3 = c.makeMCComponentFromEOS('ggH135_rawaod_3', 'ggH135_rawaod', '/store/group/phys_tau/HLT2016/HPSatHLT_91X_dm11_relaxmass/GluGluHToTauTau_M125_13TeV_powheg_pythia8/HPSatHLT/170515_141943/0003/')


# ggH135_0 = c.makeMCComponentFromEOS('ggH135_rawaod', 'ggH135_rawaod', '/store/group/phys_tau/HLT2016/HPSatHLT_91X/GluGluHToTauTau_M125_13TeV_powheg_pythia8/HPSatHLT/170509_091925/0000/')
# ggH135_1 = c.makeMCComponentFromEOS('ggH135_rawaod_1', 'ggH135_rawaod', '/store/group/phys_tau/HLT2016/HPSatHLT_91X/GluGluHToTauTau_M125_13TeV_powheg_pythia8/HPSatHLT/170509_091925/0001/')
# ggH135_2 = c.makeMCComponentFromEOS('ggH135_rawaod_2', 'ggH135_rawaod', '/store/group/phys_tau/HLT2016/HPSatHLT_91X/GluGluHToTauTau_M125_13TeV_powheg_pythia8/HPSatHLT/170509_091925/0002/')


selectedComponents = [ggH135_0, ggH135_1, ggH135_2, ggH135_3]


tauHLTAna = cfg.Analyzer(
    TauHLTAnalyzer,
    name='TauHLTAnalyzer',
)

tauHLTTree = cfg.Analyzer(
    HLTTauTreeProducer,
    name='HLTTauTreeProducer',
    debug=True
)

sequence = cfg.Sequence([
    tauHLTAna,
    tauHLTTree
])


if not production:
    selectedComponents = selectedComponents[:1]
    for comp in selectedComponents:
        comp.splitFactor = 1
        comp.fineSplitFactor = 1
    # comp.files = comp.files[:1]
else:
    for comp in selectedComponents:
        comp.splitFactor = 200

config = cfg.Config(components=selectedComponents,
                    sequence=sequence,
                    services=[],
                    events_class=Events
                    )

printComps(config.components, True)
