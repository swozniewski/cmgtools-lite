import ROOT

from PhysicsTools.Heppy.physicsutils.TauDecayModes import tauDecayModes
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle

from CMGTools.H2TauTau.proto.analyzers.H2TauTauTreeProducerBase import H2TauTauTreeProducerBase

from CMGTools.H2TauTau.proto.analyzers.HTTGenAnalyzer import HTTGenAnalyzer

class TauTreeProducer(H2TauTauTreeProducerBase):
    ''' Tree producer for tau POG study.
    '''

    def __init__(self, *args):
        super(TauTreeProducer, self).__init__(*args)

    def declareHandles(self):
        super(TauTreeProducer, self).declareHandles()


    def declareVariables(self, setup):

        self.bookTau(self.tree, 'tau')
        self.tree.vector()


    def process(self, event):
        # needed when doing handle.product(), goes back to
        # PhysicsTools.Heppy.analyzers.core.Analyzer
        self.readCollections(event.input)

        if not eval(self.skimFunction):
            return False



        for i_tau, tau in enumerate(event.selectedTaus):
            
            self.tree.reset()
            self.fillTau(self.tree, 'tau', tau)
    
            self.fillTree(event)
