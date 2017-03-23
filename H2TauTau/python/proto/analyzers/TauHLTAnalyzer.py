from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.Heppy.physicsobjects.Tau import Tau

from PhysicsTools.HeppyCore.utils.deltar import deltaR
from CMGTools.H2TauTau.proto.analyzers.HTTGenAnalyzer import HTTGenAnalyzer
from CMGTools.H2TauTau.proto.analyzers.TriggerAnalyzer import TriggerInfo

class TauHLTAnalyzer(Analyzer):

    '''Gets tau decay mode efficiency weight and puts it in the event'''

    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(TauHLTAnalyzer, self).__init__(cfg_ana, cfg_comp, looperName)

        self.triggers = ['MC_LooseIsoPFTau20_v1',  'MC_LooseIsoPFTau50_Trk30_eta2p1_v1', 'HLT_DoubleMediumIsoPFTau35_Trk1_eta2p1_Reg_v3', 'HLT_DoubleMediumIsoPFTau35_Trk1_eta2p1_Reg_v5']

    def declareHandles(self):

        super(TauHLTAnalyzer, self).declareHandles()
        self.handles['rho'] = AutoHandle(
            ('fixedGridRhoFastjetAll', '', 'RECO'),
            'double'
            )

        self.handles['taus'] = AutoHandle(
            ('hpsPFTauProducer', '', 'RECO'),
            'std::vector<reco::PFTau>'
        )

        self.handles['DM'] = AutoHandle(
            ('hpsPFTauDiscriminationByDecayModeFindingNewDMs', '', 'RECO'),
            'reco::PFTauDiscriminator'
        )

        self.handles['looseDBIso'] = AutoHandle(
            ('hpsPFTauDiscriminationByLooseCombinedIsolationDBSumPtCorr3Hits', '', 'RECO'),
            'reco::PFTauDiscriminator'
        )

        self.handles['genParticles'] = AutoHandle(
            'genParticles',
            'std::vector<reco::GenParticle>')

        self.handles['hlt_taus'] = AutoHandle(
            ('hltHpsPFTauProducer', '', 'TEST'),
            'std::vector<reco::PFTau>',
            lazy=False,
            mayFail=True,
            disableAtFirstFail=False
        )

        self.handles['hlt_classic_taus'] = AutoHandle(
            ('hltPFTausReg', '', 'TEST'),
            'std::vector<reco::PFTau>',
            lazy=False,
            mayFail=True,
            disableAtFirstFail=False
        )
        
        self.handles['hlt_classic_single_taus'] = AutoHandle(
            ('hltPFTaus', '', 'TEST'),
            'std::vector<reco::PFTau>',
            lazy=False,
            mayFail=True,
            disableAtFirstFail=False
        )

        self.handles['hltDM'] = AutoHandle(
            ('hltHpsPFTauDiscriminationByDecayModeFindingNewDMs', '', 'TEST'),
            'reco::PFTauDiscriminator',
            lazy=False,
            mayFail=True,
            disableAtFirstFail=False
        )

        self.handles['hltLooseDB'] = AutoHandle(
            ('hltHpsPFTauDiscriminationByLooseCombinedIsolationDBSumPtCorr3Hits', '', 'TEST'),
            'reco::PFTauDiscriminator',
            lazy=False,
            mayFail=True,
            disableAtFirstFail=False
        )

        self.handles['hltSingle_taus'] = AutoHandle(
            ('hltHpsPFTauProducerSingleTau', '', 'TEST'),
            'std::vector<reco::PFTau>',
            lazy=False,
            mayFail=True,
            disableAtFirstFail=False
        )

        self.handles['hltSingleDM'] = AutoHandle(
            ('hltHpsPFTauDiscriminationByDecayModeFindingNewDMsSingleTau', '', 'TEST'),
            'reco::PFTauDiscriminator',
            lazy=False,
            mayFail=True,
            disableAtFirstFail=False
        )

        self.handles['hltSingleLooseDB'] = AutoHandle(
            ('hltHpsPFTauDiscriminationByLooseCombinedIsolationDBSumPtCorr3HitsSingleTau', '', 'TEST'),
            'reco::PFTauDiscriminator',
            lazy=False,
            mayFail=True,
            disableAtFirstFail=False
        )

        self.handles['pfCandidates'] = AutoHandle(
            ('particleFlow', '', 'RECO'),
            'std::vector<reco::PFCandidate>'
        )

        self.handles['hltPfCandidates'] = AutoHandle(
            ('hltParticleFlowReg', '', 'TEST'),
            'std::vector<reco::PFCandidate>',
            lazy=False,
            mayFail=True,
            disableAtFirstFail=False
        )

        self.handles['hltSinglePfCandidates'] = AutoHandle(
            ('hltParticleFlowForTaus', '', 'TEST'),
            'std::vector<reco::PFCandidate>',
            lazy=False,
            mayFail=True,
            disableAtFirstFail=False
        )

        self.handles['TriggerResults'] = AutoHandle(
            ('TriggerResults', '', 'TEST'), 'edm::TriggerResults')

        # self.handles['TriggerResults'] = AutoHandle(
            # ('TriggerResults', '', 'HLT'), 'edm::TriggerResults')

        self.handles['triggerObjects'] = AutoHandle(
            ('selectedPatTriggerCustom', '', 'TEST'),
            'std::vector<pat::TriggerObjectStandAlone>'
            )

    def beginLoop(self, setup):
        print self, self.__class__
        super(TauHLTAnalyzer, self).beginLoop(setup)

    def process(self, event):
        self.readCollections(event.input)

        event.rho = self.handles['rho'].product()[0]

        event.taus = [Tau(tau) for tau in self.handles['taus'].product()]
        dms = self.handles['DM'].product() 
        loose_db_isos = self.handles['looseDBIso'].product()

        if len(event.taus) != len(dms) or len(event.taus) != len(loose_db_isos):
            import pdb; pdb.set_trace()

        for i_tau, tau in enumerate(event.taus):
            tau.dm = dms.value(i_tau)
            tau.loose_db_iso = loose_db_isos.value(i_tau)
            if tau.dm > 1:
                import pdb; pdb.set_trace()

        event.hlt_taus = []
        if self.handles['hlt_taus'].isValid():
            event.hlt_taus = [Tau(tau) for tau in self.handles['hlt_taus'].product()]

        if event.hlt_taus:
            hlt_dms = self.handles['hltDM'].product() 
            hlt_loose_db_isos = self.handles['hltLooseDB'].product()
            for i_tau, tau in enumerate(event.hlt_taus):
                tau.dm = hlt_dms.value(i_tau)
                tau.loose_db_iso = hlt_loose_db_isos.value(i_tau)
        else:
            # print self.handles['hlt_taus']._exception
            if self.handles['hlt_taus']._exception is None:
                import pdb; pdb.set_trace()

        event.hlt_classic_taus = []
        if self.handles['hlt_classic_taus'].isValid():
            event.hlt_classic_taus = [Tau(tau) for tau in self.handles['hlt_classic_taus'].product()]
            for tau in event.hlt_classic_taus:
                tau.dm = -10 # dummy so it behaves as the other taus
                tau.loose_db_iso = -10. # dummy so it behaves as the other taus

        event.hlt_classic_single_taus = []
        if self.handles['hlt_classic_single_taus'].isValid():
            event.hlt_classic_single_taus = [Tau(tau) for tau in self.handles['hlt_classic_single_taus'].product()]
            for tau in event.hlt_classic_single_taus:
                tau.dm = -10 # dummy so it behaves as the other taus
                tau.loose_db_iso = -10. # dummy so it behaves as the other taus

        event.hlt_single_taus = []
        if self.handles['hltSingle_taus'].isValid():
            event.hlt_single_taus = [Tau(tau) for tau in self.handles['hltSingle_taus'].product()]

        if event.hlt_single_taus:
            hlt_dms = self.handles['hltSingleDM'].product() 
            hlt_loose_db_isos = self.handles['hltSingleLooseDB'].product()
            for i_tau, tau in enumerate(event.hlt_single_taus):
                tau.dm = hlt_dms.value(i_tau)
                tau.loose_db_iso = hlt_loose_db_isos.value(i_tau)
        else:
            # print self.handles['hlt_taus']._exception
            if self.handles['hltSingle_taus']._exception is None:
                print 'No single HLT taus'
                # import pdb; pdb.set_trace()

        event.taus = [tau for tau in event.taus if tau.pt() > 10. and abs(tau.eta()) < 2.3]
        event.hlt_taus = [tau for tau in event.hlt_taus if tau.pt() > 10. and abs(tau.eta()) < 2.3]
        event.hlt_classic_taus = [tau for tau in event.hlt_classic_taus if tau.pt() > 10. and abs(tau.eta()) < 2.3]
        event.hlt_classic_single_taus = [tau for tau in event.hlt_classic_single_taus if tau.pt() > 10. and abs(tau.eta()) < 2.3]
        event.hlt_single_taus = [tau for tau in event.hlt_single_taus if tau.pt() > 10. and abs(tau.eta()) < 2.3]


        event.genParticles = self.handles['genParticles'].product()

        event.genleps = [p for p in event.genParticles if abs(p.pdgId()) in [11, 13] and p.statusFlags().isPrompt()]
        event.gentauleps = [p for p in event.genParticles if abs(p.pdgId()) in [11, 13] and p.statusFlags().isDirectPromptTauDecayProduct()]
        event.gentaus = [p for p in event.genParticles if abs(p.pdgId()) == 15 and p.statusFlags().isPrompt() and not any(abs(HTTGenAnalyzer.getFinalTau(p).daughter(i_d).pdgId()) in [11, 13] for i_d in xrange(HTTGenAnalyzer.getFinalTau(p).numberOfDaughters()))]

        def addInfo(tau, cands=None, maxDeltaR=None):
            HTTGenAnalyzer.genMatch(event, tau, event.gentauleps, event.genleps, [], 
                 dR=0.2, matchAll=True)
            HTTGenAnalyzer.attachGenStatusFlag(tau)
            self.tauIsoBreakdown(tau, cands, maxDeltaR=maxDeltaR)
            tau.nphotons = sum(1 for cand in TauHLTAnalyzer.tauFilteredPhotons(tau))

        pfCandidates = self.handles['pfCandidates'].product()
        hltPfCandidates = self.handles['hltPfCandidates'].product() if self.handles['hltPfCandidates'].isValid() else None
        hltSinglePfCandidates = self.handles['hltSinglePfCandidates'].product() if self.handles['hltSinglePfCandidates'].isValid() else None

        for tau in event.taus:
            addInfo(tau, [c for c in pfCandidates if abs(c.pdgId()) == 211], maxDeltaR=0.8)

        for tau in event.hlt_taus :
            addInfo(tau, [c for c in hltPfCandidates if abs(c.pdgId()) == 211], maxDeltaR=0.5)

        for tau in event.hlt_classic_taus:
            addInfo(tau, [c for c in hltPfCandidates if abs(c.pdgId()) == 211], maxDeltaR=0.5)

        for tau in event.hlt_classic_single_taus:
            addInfo(tau, [c for c in hltSinglePfCandidates if abs(c.pdgId()) == 211], maxDeltaR=0.5)

        for tau in event.hlt_single_taus:
            addInfo(tau, [c for c in hltSinglePfCandidates if abs(c.pdgId()) == 211], maxDeltaR=0.5)

        # Counts offline gen-matched tauh
        event.offline_35 = sum(1 for tau in event.taus if tau.pt() > 35. and tau.gen_match == 5)
        event.offline_30 = sum(1 for tau in event.taus if tau.pt() > 30. and tau.gen_match == 5)
        event.offline_20 = sum(1 for tau in event.taus if tau.pt() > 20. and tau.gen_match == 5)

        #
        if not hasattr(event, 'genTauJets'):
            HTTGenAnalyzer.getGenTauJets(event)
        event.gen_taus_35 = sum(1 for tau in event.genTauJets if tau.pt() > 35)

        # Counts offline tauh not matched to jet
        event.offline_nojet_35 = sum(1 for tau in event.taus if tau.pt() > 35. and tau.gen_match != 6)
        event.offline_nojet_30 = sum(1 for tau in event.taus if tau.pt() > 30. and tau.gen_match != 6)
        event.offline_nojet_20 = sum(1 for tau in event.taus if tau.pt() > 20. and tau.gen_match != 6)

        # event.trigger_infos = []

        triggerBits = self.handles['TriggerResults'].product()
        names = event.input.object().triggerNames(triggerBits)

        # # Get trigger names with:
        # print [n for n in names.triggerNames() if 'Tau' in n]

        for trigger_name in self.triggers:
            index = names.triggerIndex(trigger_name)
            if index == len(triggerBits):
                setattr(event, trigger_name, False)
                continue

            fired = triggerBits.accept(index)
            if fired:
                setattr(event, trigger_name, True)
            else:
                setattr(event, trigger_name, False)

            # event.trigger_infos.append(TriggerInfo(trigger_name, index, fired))

        iso_vals_25 = []
        iso_vals_30 = []
        iso_vals_35 = []
        iso_vals_dm_35 = []
        iso_vals_40 = []
        for tau in event.hlt_taus:
            iso = tau.chargedPtSumIso #+ max(0., tau.gammaPtSumIso - event.rho * 0.1752)
            pt = tau.pt()
            dm = tau.dm
            if dm and pt > 35.:
                iso_vals_dm_35.append(iso)
            if pt > 25.:
                iso_vals_25.append(iso)
            if pt > 30.:
                iso_vals_30.append(iso)
            if pt > 35.:
                iso_vals_35.append(iso)
            if pt > 40.:
                iso_vals_40.append(iso)

        event.min_max_iso_to_pass_25 = sorted(iso_vals_25)[1] if len(iso_vals_25) > 1 else 999.
        event.min_max_iso_to_pass_30 = sorted(iso_vals_30)[1] if len(iso_vals_30) > 1 else 999.
        event.min_max_iso_to_pass_35 = sorted(iso_vals_35)[1] if len(iso_vals_35) > 1 else 999.
        event.min_max_iso_to_pass_40 = sorted(iso_vals_40)[1] if len(iso_vals_40) > 1 else 999.

        event.min_max_iso_to_pass_dm_35 = sorted(iso_vals_dm_35)[1] if len(iso_vals_dm_35) > 1 else 999.

        # triggerObjects = self.handles['triggerObjects'].product()
        # for to in triggerObjects:
        #     to.unpackPathNames(names)
        #     for info in event.trigger_infos:
        #         if to.hasPathName(trigger_name):
        #             if to in info.objects:
        #                 continue
        #             print 'TO name', [n for n in to.filterLabels()], to.hasPathName(info.name, False)
        #             info.object_names.append('')
        #             info.objects.append(to)
        #             info.objIds.add(abs(to.pdgId()))
        # import pdb; pdb.set_trace()

        return True


    @staticmethod
    def tauChargedFilteredIso(tau, minDeltaZ=-1., maxDeltaZ=0.2, maxTrackChi2=100., maxTransverseImpactParameter=0.03, minTrackHits=3, minTrackPt=0.5, cands=None, maxDeltaR=None):
        
        if not cands:
            cands = [cand.get() for cand in tau.isolationPFChargedHadrCands()]
        pv = tau.vertex()
        filteredCands = []
        for cand in cands:
            if maxDeltaR:
                # Speed up
                if abs(cand.eta() - tau.eta()) > maxDeltaR or abs(cand.phi() - tau.phi()) > maxDeltaR:
                    continue
                if deltaR(tau, cand) > maxDeltaR:
                    continue

            # print 'deltaR:', deltaR(tau, cand)


            if not cand.trackRef().isAvailable():
                print 'Track not avaialble for PF candidate with ID', cand.pdgId()
                continue
            track = cand.trackRef().get()

            if TauHLTAnalyzer.filterTrack(track, pv, minDeltaZ, maxDeltaZ, maxTrackChi2, maxTransverseImpactParameter, minTrackHits, minTrackPt):
                continue

            filteredCands.append(cand)
        return filteredCands

    @staticmethod
    def filterTrack(track, pv, minDeltaZ=-1., maxDeltaZ=0.2, maxTrackChi2=100., maxTransverseImpactParameter=0.03, minTrackHits=3, minTrackPt=0.5,):
        return (track.pt() < minTrackPt
                or track.normalizedChi2() > maxTrackChi2
                or track.hitPattern().numberOfValidHits() < minTrackHits
                or abs(track.dz(pv)) > maxDeltaZ
                or abs(track.dz(pv)) < minDeltaZ
                or abs(track.dxy(pv)) > maxTransverseImpactParameter)

    @staticmethod
    def tauPhotonsOutsideSignalCone(tau):
        filteredCands = []
        signalConeSize = tau.signalConeSize()
        for c in tau.signalPFGammaCands():
            if deltaR(tau, c) > signalConeSize:
                filteredCands.append(c)
        return filteredCands

    @staticmethod
    def tauFilteredPhotons(tau, minPt=0.5, maxDR=0.5):
        filteredCands = []
        for cand in tau.isolationPFGammaCands():
            # if abs(cand.pdgId()) == 11:
            #     track = None
            #     if cand.trackRef().isAvailable():
            #         track = cand.trackRef().get()
            #     elif cand.gsfTrackRef().isAvailable():
            #         track = cand.gsfTrackRef().get()
            #     else:
            #         print 'No electron track found'
            #         import pdb; pdb.set_trace()
            #     if TauHLTAnalyzer.filterTrack(track, tau.vertex()):
            #         continue
            # el
            if (cand.pt() < minPt
                or deltaR(cand, tau) > maxDR):
                continue
            filteredCands.append(cand)
        return filteredCands

    @staticmethod
    def tauIsoBreakdown(tau, pfCandidates=None, maxDeltaR=None):
        # calculate photon pT outside signal cone
        variables = {
            'ptSumIso': tau.isolationPFCands(),
            'chargedPtSumIso': TauHLTAnalyzer.tauChargedFilteredIso(tau),
            'chargedPUPtSumIso': TauHLTAnalyzer.tauChargedFilteredIso(tau, minDeltaZ=0.2, maxDeltaZ=99999., cands=pfCandidates, maxDeltaR=maxDeltaR),
            'gammaPtSumIso': TauHLTAnalyzer.tauFilteredPhotons(tau),
            'gammaPtSumOutsideSignalCone': TauHLTAnalyzer.tauPhotonsOutsideSignalCone(tau),
            'neutralPtSumIso': tau.isolationPFNeutrHadrCands(),
            'ptSumSignal': tau.signalPFCands(),
            'chargedCandsPtSumSignal': tau.signalPFChargedHadrCands(),
            'gammaCandsPtSumSignal': tau.signalPFGammaCands(),
            'neutralCandsPtSumSignal': tau.signalPFNeutrHadrCands(),
        }

        for k, v in variables.items():
            ptsum = 0.
            for i in v:
                ptsum += i.pt()
            setattr(tau, k, ptsum)
