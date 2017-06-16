import ROOT

from CMGTools.H2TauTau.proto.plotter.ROCPlotter import makeROCPlot

prefixes = [
    # 'effs_any_tau',
    # 'effs_chargedPtRel_any_tau',
    # 'effs_rhoCorr_any_tau'
    # 'effsnopu_chargedPt_any_tau'
    'effs_chargedPt_inclusive'
    # 'effsnopuno15_chargedPt04_inclusive'
]

sb_names = [
    ('gen_tau_45_reco_tau_40', 'p_{T}^{gen} > 45 GeV (rec 40)'),
    ('gen_tau_25_reco_tau_20', 'p_{T}^{gen} > 25 GeV (rec 20)'),
    ('gen_tau_25_dm0_reco_tau_20', 'p_{T}^{gen} > 25 GeV 1p (rec 20)'),
    ('gen_tau_25_dm1_reco_tau_20', 'p_{T}^{gen} > 25 GeV 1p+pi0 (rec 20)'),
    ('gen_tau_25_dm10_reco_tau_20', 'p_{T}^{gen} > 25 GeV 3p (rec 20)'),
    ('gen_tau_40_dm0_reco_tau_40', 'p_{T}^{gen} > 40 GeV 1p (rec 40)'),
    ('gen_tau_40_dm1_reco_tau_40', 'p_{T}^{gen} > 40 GeV 1p+pi0 (rec 40)'),
    ('gen_tau_40_dm10_reco_tau_40', 'p_{T}^{gen} > 40 GeV 3p (rec 40)'),
    ('gen_tau_45', 'p_{T}^{gen} > 45 GeV'),
    ('gen_tau_25', 'p_{T}^{gen} > 25 GeV'),
    ('gen_tau_25_dm0', 'p_{T}^{gen} > 25 GeV 1p'),
    ('gen_tau_25_dm1', 'p_{T}^{gen} > 25 GeV 1p+pi0'),
    ('gen_tau_25_dm10', 'p_{T}^{gen} > 25 GeV 3p'),
    ('gen_tau_40_dm0', 'p_{T}^{gen} > 40 GeV 1p'),
    ('gen_tau_40_dm1', 'p_{T}^{gen} > 40 GeV 1p+pi0'),
    ('gen_tau_40_dm10', 'p_{T}^{gen} > 40 GeV 3p'),
    ('gen_tau_35', 'p_{T}^{gen} > 35 GeV'),
    ('gen_tau_35_reco_tau_35', 'p_{T}^{gen} > 35 GeV (rec 35)'),
]

tau_names = ['hlt_single_tau_dm', 'hlt_single_tau',  'hlt_classic_single_tau', 'tau_dm', 'tau', 'hlt_single_tau_neutral', 'hlt_single_tau_outside']

tau_name_to_plot = {
    'tau_dm':'Offline HPS (DM)',
    'tau':'Offline HPS',
    'hlt_single_tau_dm':'HLT HPS (DM)',
    'hlt_single_tau':'HLT HPS',
    'hlt_single_tau_neutral':'HLT HPS plus neutral',
    'hlt_single_tau_outside':'HLT HPS outside',
    'hlt_classic_single_tau':'HLT Shrinking'
}

import pickle
for prefix in prefixes:
    for sb_name in sb_names:
        effs = pickle.load(open('{d}_{c}.pkl'.format(d=prefix, c=sb_name[0]), 'rb'))

        rocs = []

        for name in tau_names:
            effs_sb = effs[name]
            if name in ['tau_dm', 'tau'] and 'reco_tau' in sb_name[0]:
                continue

            roc = ROOT.TGraph(len(effs_sb))
            for i, eff_sb in enumerate(effs_sb):
                roc.SetPoint(i, eff_sb[1], eff_sb[0])

            roc.name = name
            roc.title = tau_name_to_plot[name]
            rocs.append(roc)

        makeROCPlot(rocs, sb_name[0]+prefix, outdir='rocs_nopu/', title=sb_name[1], xmin=0.4 if 'rec' in sb_name[0] else 0.2, ymin=0.004, logy=True)


