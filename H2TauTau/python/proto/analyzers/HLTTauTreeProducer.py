from PhysicsTools.HeppyCore.utils.deltar import deltaR
from PhysicsTools.Heppy.physicsutils.TauDecayModes import tauDecayModes
from CMGTools.H2TauTau.proto.analyzers.TauGenTreeProducer import TauGenTreeProducer
from CMGTools.H2TauTau.proto.analyzers.H2TauTauTreeProducerBase import H2TauTauTreeProducerBase

class HLTTauTreeProducer(H2TauTauTreeProducerBase):
    ''' Tree producer for tau POG study.
    '''
    triggers = ['MC_LooseIsoPFTau20_v1',  'MC_LooseIsoPFTau50_Trk30_eta2p1_v1', 'HLT_DoubleMediumIsoPFTau35_Trk1_eta2p1_Reg_v3', 'HLT_DoubleMediumIsoPFTau35_Trk1_eta2p1_Reg_v5']

    def __init__(self, *args):
        super(HLTTauTreeProducer, self).__init__(*args)

    def declareHandles(self):
        super(HLTTauTreeProducer, self).declareHandles()

    def bookEvent(self):
        self.var(self.tree, 'min_max_iso_to_pass_25')
        self.var(self.tree, 'min_max_iso_to_pass_30')
        self.var(self.tree, 'min_max_iso_to_pass_35')
        self.var(self.tree, 'min_max_iso_to_pass_40')
        self.var(self.tree, 'min_max_iso_to_pass_dm_35')
        self.var(self.tree, 'rho')
        self.var(self.tree, 'gen_taus_35')
        self.var(self.tree, 'offline_35')
        self.var(self.tree, 'offline_30')
        self.var(self.tree, 'offline_20')
        self.var(self.tree, 'offline_nojet_35')
        self.var(self.tree, 'offline_nojet_30')
        self.var(self.tree, 'offline_nojet_20')
        self.var(self.tree, 'i_tau')
        self.var(self.tree, 'tau_gen_decayMode')

        for trigger in self.triggers:
            self.var(self.tree, trigger)

    def bookTau(self, tau_name):
        self.bookParticle(self.tree, tau_name)

        for var in ['ptSumIso', 'chargedPtSumIso', 'chargedPUPtSumIso', 'gammaPtSumIso', 'neutralPtSumIso', 'ptSumSignal', 'chargedCandsPtSumSignal', 'gammaCandsPtSumSignal', 'neutralCandsPtSumSignal', 'dm', 'loose_db_iso', 'nphotons', 'decayMode', 'leadChargedHadrPt', 'leadChargedHadrId']:
            self.var(self.tree, '_'.join([tau_name, var]))

    def fillEvent(self, event):
        self.fill(self.tree, 'rho', event.rho)
        self.fill(self.tree, 'min_max_iso_to_pass_25', event.min_max_iso_to_pass_25)
        self.fill(self.tree, 'min_max_iso_to_pass_30', event.min_max_iso_to_pass_30)
        self.fill(self.tree, 'min_max_iso_to_pass_35', event.min_max_iso_to_pass_35)
        self.fill(self.tree, 'min_max_iso_to_pass_40', event.min_max_iso_to_pass_40)
        self.fill(self.tree, 'min_max_iso_to_pass_dm_35', event.min_max_iso_to_pass_dm_35)
        self.fill(self.tree, 'gen_taus_35', event.gen_taus_35)
        self.fill(self.tree, 'offline_35', event.offline_35)
        self.fill(self.tree, 'offline_30', event.offline_30)
        self.fill(self.tree, 'offline_20', event.offline_20)
        self.fill(self.tree, 'offline_nojet_35', event.offline_nojet_35)
        self.fill(self.tree, 'offline_nojet_30', event.offline_nojet_30)
        self.fill(self.tree, 'offline_nojet_20', event.offline_nojet_20)

        for trigger in self.triggers:
            self.fill(self.tree, trigger, getattr(event, trigger))

    def fillTau(self, tau, tau_name):
        self.fillParticle(self.tree, tau_name, tau)

        # Some redundancey as may be filled multiple times, but that shouldn't do any harm
        if tau.genp:
            self.fillGenParticle(self.tree, 'tau_gen', tau.genp)
            if abs(tau.genp.pdgId()) == 15:
                self.fill(self.tree, 'tau_gen_decayMode', tauDecayModes.genDecayModeInt(tau.genp.daughters))

        for var in ['ptSumIso', 'chargedPtSumIso', 'chargedPUPtSumIso', 'gammaPtSumIso', 'neutralPtSumIso', 'ptSumSignal', 'chargedCandsPtSumSignal', 'gammaCandsPtSumSignal', 'neutralCandsPtSumSignal', 'dm', 'loose_db_iso', 'nphotons']:
            try:
                self.fill(self.tree, '_'.join([tau_name, var]), getattr(tau, var))
            except TypeError:
                import pdb; pdb.set_trace()
        for var in ['decayMode']:
            try:
                self.fill(self.tree, '_'.join([tau_name, var]), getattr(tau, var)())
            except TypeError:
                import pdb; pdb.set_trace()

        
        if tau.leadPFChargedHadrCand().isNonnull():
            ch = tau.leadPFChargedHadrCand().get()
            self.fill(self.tree, '_'.join([tau_name, 'leadChargedHadrPt']), ch.pt())
            self.fill(self.tree, '_'.join([tau_name, 'leadChargedHadrId']), ch.pdgId())


    def declareVariables(self, setup):
        self.bookTau('tau')
        self.bookTau('hlt_tau')
        self.bookTau('hlt_single_tau')
        self.bookTau('hlt_classic_tau')
        self.bookTau('hlt_classic_single_tau')
        self.bookGenParticle(self.tree, 'tau_gen')
        self.bookEvent()

    def process(self, event):
        # needed when doing handle.product(), goes back to
        # PhysicsTools.Heppy.analyzers.core.Analyzer
        self.readCollections(event.input)

        if not eval(self.skimFunction):
            return False


        hlt_taus = [tau for tau in event.hlt_taus] # it's a vector
        hlt_single_taus = [tau for tau in event.hlt_single_taus] # it's a vector
        hlt_classic_taus = [tau for tau in event.hlt_classic_taus] # it's a vector
        hlt_classic_single_taus = [tau for tau in event.hlt_classic_single_taus] # it's a vector

        i_tau = 0

        for tau in event.taus:
            self.tree.reset()

            self.fillTau(tau, 'tau')
            self.fillEvent(event)

            for hlt_tau in hlt_taus:
                if deltaR(tau, hlt_tau) < 0.3:
                    self.fillTau(hlt_tau, 'hlt_tau')
                    hlt_taus.remove(hlt_tau)
                    break

            for hlt_tau in hlt_single_taus:
                if deltaR(tau, hlt_tau) < 0.3:
                    self.fillTau(hlt_tau, 'hlt_single_tau')
                    hlt_single_taus.remove(hlt_tau)
                    break

            for hlt_tau in hlt_classic_taus:
                if deltaR(tau, hlt_tau) < 0.3:
                    self.fillTau(hlt_tau, 'hlt_classic_tau')
                    hlt_classic_taus.remove(hlt_tau)
                    break

            for hlt_tau in hlt_classic_single_taus:
                if deltaR(tau, hlt_tau) < 0.3:
                    self.fillTau(hlt_tau, 'hlt_classic_single_tau')
                    hlt_classic_single_taus.remove(hlt_tau)
                    break
            
            self.fill(self.tree, 'i_tau', i_tau)
            i_tau += 1
            self.fillTree(event)

        for hlt_tau in hlt_taus:
            self.tree.reset()

            self.fillEvent(event)
            self.fillTau(hlt_tau, 'hlt_tau')
            for single_tau in hlt_single_taus:
                if deltaR(single_tau, hlt_tau) < 0.3:
                    self.fillTau(single_tau, 'hlt_single_tau')
                    hlt_single_taus.remove(single_tau)
                    break

            for hlt_classic_tau in hlt_classic_taus:
                if deltaR(hlt_classic_tau, hlt_tau) < 0.3:
                    self.fillTau(hlt_classic_tau, 'hlt_classic_tau')
                    hlt_classic_taus.remove(hlt_classic_tau)
                    break

            for hlt_classic_single_tau in hlt_classic_single_taus:
                if deltaR(hlt_classic_single_tau, hlt_tau) < 0.3:
                    self.fillTau(hlt_classic_single_tau, 'hlt_classic_single_tau')
                    hlt_classic_single_taus.remove(hlt_classic_single_tau)
                    break

            self.fill(self.tree, 'i_tau', i_tau)
            i_tau += 1
            self.fillTree(event)

        # for hlt_tau in hlt_classic_taus:
        #     self.tree.reset()

        #     if hlt_tau.pt() < 20.:
        #         continue

        #     self.fillEvent(event)
        #     self.fillTau(hlt_tau, 'hlt_tau')
        #     for single_tau in hlt_single_taus:
        #         if deltaR(single_tau, hlt_tau) < 0.3:
        #             self.fillTau(single_tau, 'hlt_single_tau')
        #             hlt_single_taus.remove(single_tau)
        #             break

        #     self.fill(self.tree, 'i_tau', i_tau)
        #     i_tau += 1
        #     self.fillTree(event)

        for hlt_tau in hlt_single_taus:
            self.tree.reset()
            
            self.fillEvent(event)
            self.fillTau(hlt_tau, 'hlt_single_tau')

            for hlt_classic_tau in hlt_classic_taus:
                if deltaR(hlt_classic_tau, hlt_tau) < 0.3:
                    self.fillTau(hlt_classic_tau, 'hlt_classic_tau')
                    hlt_classic_taus.remove(hlt_classic_tau)
                    break

            for hlt_classic_single_tau in hlt_classic_single_taus:
                if deltaR(hlt_classic_single_tau, hlt_tau) < 0.3:
                    self.fillTau(hlt_classic_single_tau, 'hlt_classic_single_tau')
                    hlt_classic_single_taus.remove(hlt_classic_single_tau)
                    break

            self.fill(self.tree, 'i_tau', i_tau)
            i_tau += 1
            self.fillTree(event)

        for hlt_tau in hlt_classic_taus:
            self.tree.reset()

            self.fillEvent(event)
            self.fillTau(hlt_tau, 'hlt_classic_tau')

            for hlt_classic_single_tau in hlt_classic_single_taus:
                if deltaR(hlt_classic_single_tau, hlt_tau) < 0.3:
                    self.fillTau(hlt_classic_single_tau, 'hlt_classic_single_tau')
                    hlt_classic_single_taus.remove(hlt_classic_single_tau)
                    break

            self.fill(self.tree, 'i_tau', i_tau)
            i_tau += 1
            self.fillTree(event)

        for hlt_tau in hlt_classic_single_taus:
            self.tree.reset()


            self.fillEvent(event)
            self.fillTau(hlt_tau, 'hlt_classic_single_tau')

            self.fill(self.tree, 'i_tau', i_tau)
            i_tau += 1
            self.fillTree(event)
