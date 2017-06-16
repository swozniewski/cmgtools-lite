from PhysicsTools.HeppyCore.utils.deltar import deltaR
from PhysicsTools.Heppy.physicsutils.TauDecayModes import tauDecayModes
from CMGTools.H2TauTau.proto.analyzers.TauGenTreeProducer import TauGenTreeProducer
from CMGTools.H2TauTau.proto.analyzers.H2TauTauTreeProducerBase import H2TauTauTreeProducerBase
from CMGTools.H2TauTau.proto.analyzers.TauHLTAnalyzer import TauHLTAnalyzer

class HLTTauTreeProducer(H2TauTauTreeProducerBase):
    ''' Tree producer for tau POG study.
    '''
    triggers = ['MC_LooseIsoPFTau20_v1',  'MC_LooseIsoPFTau50_Trk30_eta2p1_v1', 'HLT_DoubleMediumIsoPFTau35_Trk1_eta2p1_Reg_v3', 'HLT_DoubleMediumIsoPFTau35_Trk1_eta2p1_Reg_v5']

    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(HLTTauTreeProducer, self).__init__(cfg_ana, cfg_comp, looperName)
        self.debug =  getattr(cfg_ana, 'debug', False)

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

        for var in ['ptSumIso', 'chargedPtSumIso', 'chargedPtSumIsoOutsideSignalCone', 'chargedPUPtSumIso', 'gammaPtSumIso', 'neutralPtSumIso', 'ptSumSignal', 'chargedCandsPtSumSignal', 'gammaCandsPtSumSignal', 'neutralCandsPtSumSignal', 'dm', 'loose_db_iso', 'nphotons', 'decayMode', 'leadChargedHadrPt', 'leadChargedHadrId',
            'gammaPtSumOutsideSignalCone', 'gammaPtSumIso04Pt1', 'gammaPtSumIso04', 'chargedPtSumIso04', 'chargedPtSumIso03']:
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

        for var in ['ptSumIso', 'chargedPtSumIso', 'chargedPtSumIsoOutsideSignalCone', 'chargedPUPtSumIso', 'gammaPtSumIso', 'neutralPtSumIso', 'ptSumSignal', 'chargedCandsPtSumSignal', 'gammaCandsPtSumSignal', 'neutralCandsPtSumSignal', 'dm', 'loose_db_iso', 'nphotons', 'gammaPtSumOutsideSignalCone', 'gammaPtSumIso04Pt1', 'gammaPtSumIso04', 'chargedPtSumIso04', 'chargedPtSumIso03']:
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

        gen_taus = [tau for tau in event.genTauJets if tau.pt() > 20. and abs(tau.eta()) < 2.3]

        i_tau = 0

        if self.debug:
            for hlt_tau in event.hlt_single_taus:
                for hlt_classic_single_tau in hlt_classic_single_taus:
                    if deltaR(hlt_classic_single_tau, hlt_tau) < 0.3:
                        if hlt_tau.genp and abs(hlt_tau.genp.pdgId()) == 15 and hlt_tau.genp.pt() > 30. and hlt_classic_single_tau.pt()/hlt_tau.genp.pt() > 0.8 and hlt_tau.pt()/hlt_tau.genp.pt() < 0.8:
                            found_offline = False
                            for tau in event.taus:
                                if deltaR(tau, hlt_tau) < 0.3 and tau.pt()/hlt_tau.genp.pt() > 0.8 and tau.decayMode() in [0, 1, 10, 11] and tau.loose_db_iso > 0.5:
                                    found_offline = True
                                    break
                            if not found_offline:
                                continue

                            if hlt_classic_single_tau.neutralCandsPtSumSignal/hlt_classic_single_tau.pt() > 0.4:
                                print '  FOUND BUT CAUSE TOO MUCH NEUTRAL ENERGY, break'
                                continue

                            print '\n##### FOUND\nGen pT, DM', hlt_tau.genp.pt(), tauDecayModes.genDecayModeInt(hlt_tau.genp.daughters)
                            print 'run, lumi, event', event.input.eventAuxiliary().id().run(), event.input.eventAuxiliary().id().luminosityBlock(), event.input.eventAuxiliary().id().event()

                            print '  ### HLT\n', hlt_tau
                            print 'charged/gamma/neutral', '{:.2f}/{:.2f}/{:.2f}'.format(hlt_tau.chargedCandsPtSumSignal/hlt_tau.pt(), hlt_tau.gammaCandsPtSumSignal/hlt_tau.pt(), hlt_tau.neutralCandsPtSumSignal/hlt_tau.pt())
                            print ' CH:', ['{:.1f} {:.1f} {:.1f}'.format(c.pt(), c.eta(), c.phi()) for c in hlt_tau.signalPFChargedHadrCands()]
                            print ' PH:', ['{:.1f} {:.1f} {:.1f}'.format(c.pt(), c.eta(), c.phi()) for c in hlt_tau.signalPFGammaCands()]
                            print ' ### CONE\n', hlt_classic_single_tau
                            print 'charged/gamma/neutral', '{:.2f}/{:.2f}/{:.2f}'.format(hlt_classic_single_tau.chargedCandsPtSumSignal/hlt_classic_single_tau.pt(), hlt_classic_single_tau.gammaCandsPtSumSignal/hlt_classic_single_tau.pt(), hlt_classic_single_tau.neutralCandsPtSumSignal/hlt_classic_single_tau.pt())

                            print ' CH:', ['{:.1f} {:.1f} {:.1f}'.format(c.pt(), c.eta(), c.phi()) for c in hlt_classic_single_tau.signalPFChargedHadrCands()]
                            print ' PH:', ['{:.1f} {:.1f} {:.1f}'.format(c.pt(), c.eta(), c.phi()) for c in hlt_classic_single_tau.signalPFGammaCands()]

                            print '  ### OFF\n', tau
                            print 'charged/gamma/neutral', '{:.2f}/{:.2f}/{:.2f}'.format(tau.chargedCandsPtSumSignal/tau.pt(), tau.gammaCandsPtSumSignal/tau.pt(), tau.neutralCandsPtSumSignal/tau.pt())
                            print ' CH:', ['{:.1f} {:.1f} {:.1f}'.format(c.pt(), c.eta(), c.phi()) for c in tau.signalPFChargedHadrCands()]
                            print ' PH:', ['{:.1f} {:.1f} {:.1f}'.format(c.pt(), c.eta(), c.phi()) for c in tau.signalPFGammaCands()]
                            
                            combo_taus = [c for c in event.hlt_combo_taus if deltaR(c, hlt_tau) < 0.3]
                            good_c_taus = []
                            for c_tau in combo_taus:
                                if c_tau.pt()/hlt_tau.genp.pt() > 0.8:
                                    print '### Found a combo tau with decent pT'
                                    print c_tau
                                    print 'charged/gamma/neutral', '{:.2f}/{:.2f}/{:.2f}'.format(sum(c.pt() for c in c_tau.signalPFChargedHadrCands())/c_tau.pt(), sum(c.pt() for c in c_tau.signalPFGammaCands())/c_tau.pt(), sum(c.pt() for c in c_tau.signalPFNeutrHadrCands())/c_tau.pt())
                                    good_c_taus.append(c_tau)
                                    print ' CH:', ['{:.1f} {:.1f} {:.1f}'.format(c.pt(), c.eta(), c.phi()) for c in c_tau.signalPFChargedHadrCands()]
                                    print ' PH:', ['{:.1f} {:.1f} {:.1f}'.format(c.pt(), c.eta(), c.phi()) for c in c_tau.signalPFGammaCands()]
                            import pdb; pdb.set_trace()

        for tau in event.taus:
            self.tree.reset()

            self.fillTau(tau, 'tau')
            self.fillEvent(event)

            for hlt_tau in hlt_taus:
                if deltaR(tau, hlt_tau) < 0.3:
                    self.fillTau(hlt_tau, 'hlt_tau')
                    hlt_taus.remove(hlt_tau)
                    break

            found_classic = False
            new_str = ''
            classic_tau = None
            for hlt_tau in hlt_classic_single_taus:
                if deltaR(tau, hlt_tau) < 0.3:
                    self.fillTau(hlt_tau, 'hlt_classic_single_tau')
                    new_str = hlt_tau.__str__()
                    hlt_classic_single_taus.remove(hlt_tau)
                    if hlt_tau.pt() > 25.:
                        found_classic = True
                        classic_tau = hlt_tau
                    break

            found_new = False
            new_tau = None
            
            for hlt_tau in hlt_single_taus:
                if deltaR(tau, hlt_tau) < 0.3:
                    self.fillTau(hlt_tau, 'hlt_single_tau')
                    hlt_single_taus.remove(hlt_tau)
                    found_new = True
                    new_tau = hlt_tau
                    break

            # if found_classic and found_new and tau.genp and abs(tau.genp.pdgId()) == 15 and tau.decayMode() == 10 and new_tau.decayMode() == 10 and tauDecayModes.genDecayModeInt(tau.genp.daughters) == 10:
            #     print 'Found a very nice gen tau :-) Investigating isolation...'

            #     print 'Taus:'
            #     print '   ', tau
            #     print '   ', classic_tau
            #     print '   ', new_tau

            #     print ' Gamma pT sum isos:'
            #     print '    ', tau.gammaPtSumIso, ['{:.2f} {:.2f}'.format(cand.pt(), deltaR(tau, cand)) for cand in tau.isolationPFGammaCands() if cand.pt() > 0.5]
            #     print '    ', classic_tau.gammaPtSumIso, ['{:.2f} {:.2f}'.format(cand.pt(), deltaR(classic_tau, cand)) for cand in classic_tau.isolationPFGammaCands() if cand.pt() > 0.5]
            #     print '    ', new_tau.gammaPtSumIso, ['{:.2f} {:.2f}'.format(cand.pt(), deltaR(new_tau, cand)) for cand in new_tau.isolationPFGammaCands() if cand.pt() > 0.5]

            #     print ' Charged pT sum isos:'
            #     print '    ', tau.chargedPtSumIso, ['{:.2f} {:.2f} {}'.format(cand.pt(), deltaR(tau, cand), not TauHLTAnalyzer.filterTrack(cand.trackRef().get(), tau.vertex())) for cand in tau.isolationPFChargedHadrCands() if cand.pt() > 0.5]
            #     print '    ', classic_tau.chargedPtSumIso, ['{:.2f} {:.2f} {}'.format(cand.pt(), deltaR(classic_tau, cand), not TauHLTAnalyzer.filterTrack(cand.trackRef().get(), classic_tau.vertex())) for cand in classic_tau.isolationPFChargedHadrCands() if cand.pt() > 0.5]
            #     print '    ', new_tau.chargedPtSumIso, ['{:.2f} {:.2f} {}'.format(cand.pt(), deltaR(new_tau, cand), not TauHLTAnalyzer.filterTrack(cand.trackRef().get(), new_tau.vertex())) for cand in new_tau.isolationPFChargedHadrCands() if cand.pt() > 0.5]
            #     import pdb; pdb.set_trace()

            # if found_classic and tau.decayMode()==10 and not found_new and tau.genp and abs(tau.genp.pdgId()) == 15 and tauDecayModes.genDecayModeInt(tau.genp.daughters) == 10 and tau.genp.pt()>30. and abs(tau.genp.eta())<2.3:
            #         print '\n ### Found a tau'
            #         print 'Reco:', tau
            #         print 'Cone', new_str

            #         for hlt_c_tau in event.hlt_combo_taus:
            #             if deltaR(hlt_c_tau, tau) < 0.3:
            #                 print hlt_c_tau
            #                 # print 'Cleaner info'
            #                 print ' Charged iso:', hlt_c_tau.isolationPFChargedHadrCandsPtSum()
            #                 print ' Neutral iso', hlt_c_tau.isolationPFGammaCandsEtSum()
            #                 # print '  Algo for each CH:'
            #                 # for ch in hlt_c_tau.signalTauChargedHadronCandidates():
            #                 #     print '  ', hlt_c_tau.algo, ch.pt()
            #                 # import pdb; pdb.set_trace()

            #         for hlt_c_tau in event.all_hlt_single_taus:
            #             if deltaR(hlt_c_tau, tau) < 0.3:
            #                 print '# There is an HLT HPS tau', hlt_c_tau


            #         print 'Offline PF', [(pf.pdgId(), pf.pt(), pf.eta(), pf.phi()) for pf in event.pfCandidates if deltaR(pf, tau) < 0.2]
            #         print 'HLT PF', [(pf.pdgId(), pf.pt(), pf.eta(), pf.phi()) for pf in event.hltSinglePfCandidates if deltaR(pf, tau) < 0.2]
            #         print 'HLT tracks', [(pf.charge(), pf.pt(), pf.eta(), pf.phi()) for pf in event.hltPixelTracks if deltaR(pf, tau) < 0.2]
            #         import pdb; pdb.set_trace() 


            for hlt_tau in hlt_classic_taus:
                if deltaR(tau, hlt_tau) < 0.3:
                    self.fillTau(hlt_tau, 'hlt_classic_tau')
                    hlt_classic_taus.remove(hlt_tau)
                    break


            
            for gen_tau in gen_taus:
                if deltaR(tau, gen_tau) < 0.3:
                    gen_taus.remove(gen_tau)

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

            for gen_tau in gen_taus:
                if deltaR(tau, hlt_tau) < 0.3:
                    gen_taus.remove(gen_tau)

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

            for gen_tau in gen_taus:
                if deltaR(tau, hlt_tau) < 0.3:
                    gen_taus.remove(gen_tau)

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

            for gen_tau in gen_taus:
                if deltaR(tau, hlt_tau) < 0.3:
                    gen_taus.remove(gen_tau)

            self.fill(self.tree, 'i_tau', i_tau)
            i_tau += 1
            self.fillTree(event)

        for hlt_tau in hlt_classic_single_taus:
            self.tree.reset()


            self.fillEvent(event)
            self.fillTau(hlt_tau, 'hlt_classic_single_tau')

            for gen_tau in gen_taus:
                if deltaR(tau, hlt_tau) < 0.3:
                    gen_taus.remove(gen_tau)

            # if hlt_tau.genp and abs(hlt_tau.genp.pdgId()) == 15 and tauDecayModes.genDecayModeInt(hlt_tau.genp.daughters) == 0 and hlt_tau.genp.pt()>30. and abs(hlt_tau.genp.eta())<2.3:
            #     for tau in event.taus:
            #         if deltaR(hlt_tau, tau) < 0.3:
            #             print 'WARNING, Found reco tau for remaining HLT tau, should not happen!'


            #     for tau in event.hlt_combo_taus:
            #         if deltaR(hlt_tau, tau) < 0.3:
            #             print tau
            #             print 'Cleaner info'
            #             print tau.isolationPFChargedHadrCandsPtSum() + tau.isolationPFGammaCandsEtSum()
            #             print '  Algo for each CH:'
            #             for ch in tau.signalTauChargedHadronCandidates():
            #                 print '  ', ch.algo, ch.pt()
            #             import pdb; pdb.set_trace()

            #     print [(pf.pdgId(), pf.pt()) for pf in event.pfCandidates if deltaR(pf, hlt_tau) < 0.2]
            #     print [(pf.pdgId(), pf.pt()) for pf in event.hltSinglePfCandidates if deltaR(pf, hlt_tau) < 0.2]

            #     # print pf.trackRef().get().normalizedChi2()
            #     # print pf.trackRef().get().hitPattern().numberOfValidHits()
            #     # tau.vertex().z(), pf.trackRef().get().vertex().z()

            #     import pdb; pdb.set_trace()

            self.fill(self.tree, 'i_tau', i_tau)
            i_tau += 1
            self.fillTree(event)

        for gen_tau in gen_taus:
            self.tree.reset()
            gen_tau.setPdgId(-15 * gen_tau.charge())
            self.fillGenParticle(self.tree, 'tau_gen', gen_tau)
            self.fill(self.tree, 'tau_gen_decayMode', tauDecayModes.genDecayModeInt(gen_tau))
            self.fillEvent(event)
            self.fillTree(event)
