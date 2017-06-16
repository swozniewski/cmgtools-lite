from copy import deepcopy as copy

from CMGTools.H2TauTau.proto.plotter.PlotConfigs import HistogramCfg, VariableCfg, SampleCfg
from CMGTools.H2TauTau.proto.plotter.HistCreator import createHistogram
from CMGTools.H2TauTau.proto.plotter.HistDrawer import HistDrawer

from CMGTools.H2TauTau.proto.plotter.helper_methods import plotDataOverMCEff
from CMGTools.H2TauTau.proto.plotter.ROCPlotter import histsToRoc, makeROCPlot

from ROOT import gStyle, TFile, TH2F, TChain

from CMGTools.H2TauTau.proto.plotter.officialStyle import officialStyle
officialStyle(gStyle)

# total_weight = 'weight * ' + getPUWeight()

only_stack = False

total_weight = '1'
tree_prod_name = 'HLTTauTreeProducer'
analysis_dir = '/afs/cern.ch/user/s/steggema/work/trigger/CMSSW_9_1_0_pre3/src/CMGTools/H2TauTau/cfgPython/generic/HPSatHLT_relax1p2p'
int_lumi = 1.

samples = [
    SampleCfg(name='ggH135', dir_name='ggH135_rawaod', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, xsec=1., sumweights=1.),
    SampleCfg(name='ggH135_1', dir_name='ggH135_rawaod_1', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, xsec=1., sumweights=1.),
    SampleCfg(name='ggH135_2', dir_name='ggH135_rawaod_2', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, xsec=1., sumweights=1.),
    SampleCfg(name='ggH135_3', dir_name='ggH135_rawaod_3', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, xsec=1., sumweights=1.),
]

g_cuts = {}
# g_cuts['any_hlt_tau'] = '((hlt_single_tau_pt>20 || hlt_tau_pt > 20 || hlt_classic_tau_pt > 20 || hlt_classic_single_tau_pt > 20) && (abs(hlt_single_tau_eta)<2.3 || abs(hlt_tau_eta) < 2.3 || abs(hlt_classic_tau_eta) <2.3 || abs(hlt_classic_single_tau_eta) < 2.3))'
# g_cuts['any_tau'] = '((hlt_single_tau_pt>20 || hlt_tau_pt > 20 || hlt_classic_tau_pt > 20 || hlt_classic_single_tau_pt > 20 || tau_pt > 20) && (abs(hlt_single_tau_eta)<2.3 || abs(hlt_tau_eta) < 2.3 || abs(hlt_classic_tau_eta) <2.3 || abs(hlt_classic_single_tau_eta) < 2.3 || abs(tau_eta) < 2.3))'
g_cuts['inclusive'] = '(((hlt_single_tau_pt>20 || hlt_tau_pt > 20 || hlt_classic_tau_pt > 20 || hlt_classic_single_tau_pt > 20 || tau_pt > 20) && (abs(hlt_single_tau_eta)<2.3 || abs(hlt_tau_eta) < 2.3 || abs(hlt_classic_tau_eta) <2.3 || abs(hlt_classic_single_tau_eta) < 2.3 || abs(tau_eta) < 2.3)) || tau_gen_pt>15)'
# g_cuts['offline_tau'] = '(tau_pt > 20)'


tau_names = ['tau_dm', 'hlt_single_tau_dm', 'tau', 'hlt_single_tau', 'hlt_single_tau_neutral', 'hlt_single_tau_outside', 'hlt_classic_single_tau'] # 'hlt_tau', 'hlt_classic_tau', 
tau_names = ['tau_dm', 'hlt_single_tau_dm', 'hlt_single_tau_newDM', 'tau', 'hlt_single_tau', 'hlt_single_tau_neutral', 'hlt_single_tau_outside', 'hlt_classic_single_tau'] # 'hlt_tau', 'hlt_classic_tau', 

reco_tau_20 = 'tau_pt>20 && (tau_decayMode==0 || tau_decayMode==1 || tau_decayMode==10 || tau_decayMode==11) && tau_loose_db_iso>0.5'
reco_tau_40 = 'tau_pt>40 && (tau_decayMode==0 || tau_decayMode==1 || tau_decayMode==10 || tau_decayMode==11) && tau_loose_db_iso>0.5'
reco_tau_35 = 'tau_pt>35 && (tau_decayMode==0 || tau_decayMode==1 || tau_decayMode==10 || tau_decayMode==11) && tau_loose_db_iso>0.5'

sb_cuts = {
    'gen_tau_45_reco_tau_40':{
        's':'&& (abs(tau_gen_pdgId)==15 && tau_gen_pt>45 && abs(tau_gen_eta)<2.3) && ' + reco_tau_40,
        'b':'&& ((abs(tau_gen_eta)<2.3) && (tau_gen_pdgId>20 || abs(tau_gen_pdgId)<6))'
    },
    'gen_tau_35_reco_tau_35':{
        's':'&& (abs(tau_gen_pdgId)==15 && tau_gen_pt>35 && abs(tau_gen_eta)<2.3) && ' + reco_tau_40,
        'b':'&& ((abs(tau_gen_eta)<2.3) && (tau_gen_pdgId>20 || abs(tau_gen_pdgId)<6))'
    },
    'gen_tau_25_reco_tau_20':{
        's':'&& (abs(tau_gen_pdgId)==15 && tau_gen_pt>25 && abs(tau_gen_eta)<2.3) && ' + reco_tau_20,
        'b':'&& ((abs(tau_gen_eta)<2.3) && (tau_gen_pdgId>20 || abs(tau_gen_pdgId)<6))'
    },
    'gen_tau_25_dm0_reco_tau_20':{
        's':'&& (abs(tau_gen_pdgId)==15 && tau_gen_pt>25 && abs(tau_gen_eta)<2.3 && tau_gen_decayMode==0) && ' + reco_tau_20,
        'b':'&& ((abs(tau_gen_eta)<2.3) && (tau_gen_pdgId>20 || abs(tau_gen_pdgId)<6))'
    },
    'gen_tau_25_dm1_reco_tau_20':{
        's':'&& (abs(tau_gen_pdgId)==15 && tau_gen_pt>25 && abs(tau_gen_eta)<2.3 && tau_gen_decayMode==1) && ' + reco_tau_20,
        'b':'&& ((abs(tau_gen_eta)<2.3) && (tau_gen_pdgId>20 || abs(tau_gen_pdgId)<6))'
    },
    'gen_tau_25_dm10_reco_tau_20':{
        's':'&& (abs(tau_gen_pdgId)==15 && tau_gen_pt>25 && abs(tau_gen_eta)<2.3 && tau_gen_decayMode==10) && ' + reco_tau_20,
        'b':'&& ((abs(tau_gen_eta)<2.3) && (tau_gen_pdgId>20 || abs(tau_gen_pdgId)<6))'
    },
    'gen_tau_40_dm0_reco_tau_40':{
        's':'&& (abs(tau_gen_pdgId)==15 && tau_gen_pt>40 && abs(tau_gen_eta)<2.3 && tau_gen_decayMode==0) && ' + reco_tau_40,
        'b':'&& ((abs(tau_gen_eta)<2.3) && (tau_gen_pdgId>20 || abs(tau_gen_pdgId)<6))'
    },
    'gen_tau_40_dm1_reco_tau_40':{
        's':'&& (abs(tau_gen_pdgId)==15 && tau_gen_pt>40 && abs(tau_gen_eta)<2.3 && tau_gen_decayMode==1) && ' + reco_tau_40,
        'b':'&& ((abs(tau_gen_eta)<2.3) && (tau_gen_pdgId>20 || abs(tau_gen_pdgId)<6))'
    },
    'gen_tau_40_dm10_reco_tau_40':{
        's':'&& (abs(tau_gen_pdgId)==15 && tau_gen_pt>40 && abs(tau_gen_eta)<2.3 && tau_gen_decayMode==10) && ' + reco_tau_40,
        'b':'&& ((abs(tau_gen_eta)<2.3) && (tau_gen_pdgId>20 || abs(tau_gen_pdgId)<6))'
    },
    'gen_tau_45':{
        's':'&& (abs(tau_gen_pdgId)==15 && tau_gen_pt>45 && abs(tau_gen_eta)<2.3)',
        'b':'&& ((abs(tau_gen_eta)<2.3) && (tau_gen_pdgId>20 || abs(tau_gen_pdgId)<6))'
    },
    'gen_tau_35':{
        's':'&& (abs(tau_gen_pdgId)==15 && tau_gen_pt>35 && abs(tau_gen_eta)<2.3)',
        'b':'&& ((abs(tau_gen_eta)<2.3) && (tau_gen_pdgId>20 || abs(tau_gen_pdgId)<6))'
    },
    'gen_tau_25':{
        's':'&& (abs(tau_gen_pdgId)==15 && tau_gen_pt>25 && abs(tau_gen_eta)<2.3)',
        'b':'&& ((abs(tau_gen_eta)<2.3) && (tau_gen_pdgId>20 || abs(tau_gen_pdgId)<6))'
    },
    'gen_tau_25_dm0':{
        's':'&& (abs(tau_gen_pdgId)==15 && tau_gen_pt>25 && abs(tau_gen_eta)<2.3 && tau_gen_decayMode==0)',
        'b':'&& ((abs(tau_gen_eta)<2.3) && (tau_gen_pdgId>20 || abs(tau_gen_pdgId)<6))'
    },
    'gen_tau_25_dm1':{
        's':'&& (abs(tau_gen_pdgId)==15 && tau_gen_pt>25 && abs(tau_gen_eta)<2.3 && tau_gen_decayMode==1)',
        'b':'&& ((abs(tau_gen_eta)<2.3) && (tau_gen_pdgId>20 || abs(tau_gen_pdgId)<6))'
    },
    'gen_tau_25_dm10':{
        's':'&& (abs(tau_gen_pdgId)==15 && tau_gen_pt>25 && abs(tau_gen_eta)<2.3 && tau_gen_decayMode==10)',
        'b':'&& ((abs(tau_gen_eta)<2.3) && (tau_gen_pdgId>20 || abs(tau_gen_pdgId)<6))'
    },
    'gen_tau_40_dm0':{
        's':'&& (abs(tau_gen_pdgId)==15 && tau_gen_pt>40 && abs(tau_gen_eta)<2.3 && tau_gen_decayMode==0)',
        'b':'&& ((abs(tau_gen_eta)<2.3) && (tau_gen_pdgId>20 || abs(tau_gen_pdgId)<6))'
    },
    'gen_tau_40_dm1':{
        's':'&& (abs(tau_gen_pdgId)==15 && tau_gen_pt>40 && abs(tau_gen_eta)<2.3 && tau_gen_decayMode==1)',
        'b':'&& ((abs(tau_gen_eta)<2.3) && (tau_gen_pdgId>20 || abs(tau_gen_pdgId)<6))'
    },
    'gen_tau_40_dm10':{
        's':'&& (abs(tau_gen_pdgId)==15 && tau_gen_pt>40 && abs(tau_gen_eta)<2.3 && tau_gen_decayMode==10)',
        'b':'&& ((abs(tau_gen_eta)<2.3) && (tau_gen_pdgId>20 || abs(tau_gen_pdgId)<6))'
    }
}


vars = {
    'chargedPt':'abs({tau}_chargedPtSumIso)',
    # 'chargedPt04':'abs({tau}_chargedPtSumIso04)',
    # 'chargedPtRel':'abs({tau}_chargedPtSumIso/{tau}_pt)',
    # 'rhoCorr':'abs({tau}_chargedPtSumIso) + max({tau}_gammaPtSumIso - rho*0.1752, 0)'
}

from ROOT import TCanvas, TLegend
can = TCanvas('can', '', 800, 800)

for var_name, var in vars.items():
    for cut_name, cut in g_cuts.items():
        print '\n\n#### Investigating general cut', cut_name
        for signal_cut_name, cuts in sb_cuts.items():
            print '\n## Specific cut', signal_cut_name

            cut_s = cut + cuts['s']
            cut_b = cut + cuts['b']

            tree = TChain('tree')
            for sample in samples:
                tree.Add('/'.join([sample.ana_dir, sample.dir_name, sample.tree_prod_name, sample.tree_name + '.root']))
            
            effs_b = [0.001, 0.002, 0.005, 0.007, 0.009, 0.01, 0.012, 0.015, 0.02, 0.025, 0.03, 0.035, 0.04, 0.045, 0.05, 0.0625, 0.075, 0.1, 0.15, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]

            effs = {}

            for tau_name in tau_names:
                print '\n# Tau', tau_name

                effs[tau_name] = []
                dict_tau_name = tau_name[:]

                hist_s_name = 's'+tau_name
                hist_b_name = 'b'+tau_name

                n_bins_x = 160
                n_bins_y = 200

                xmin = 20.
                xmax = 100.
                ymin = 0.
                ymax = 20.

                hist_s = TH2F(hist_s_name, '', n_bins_x, xmin, xmax, n_bins_y, ymin, ymax)
                hist_b = TH2F(hist_b_name, '', n_bins_x, xmin, xmax, n_bins_y, ymin, ymax)

                extra_draw_var = ''
                if 'dm' in tau_name:
                    tau_name = tau_name[:-3]
                    extra_draw_var = ' + 200.*(!({tau}_decayMode==0 || {tau}_decayMode==1 || {tau}_decayMode==10 || {tau}_decayMode==11))'.format(tau=tau_name)
                if 'newDM' in tau_name:
                    tau_name = tau_name[:-6]
                    extra_draw_var = ' + 200.*(!({tau}_decayMode>=0 && {tau}_decayMode<=12))'.format(tau=tau_name)

                addNeutral = False
                if tau_name == 'hlt_single_tau_neutral':
                    tau_name = 'hlt_single_tau'
                    addNeutral = True

                draw_var = var
                if tau_name == 'hlt_single_tau_outside':
                    draw_var = var.replace('_chargedPtSumIso', '_chargedPtSumIsoOutsideSignalCone')
                    tau_name = 'hlt_single_tau'

                tau_pt_name = tau_name+'_pt'
                if addNeutral:
                    tau_pt_name += '+ ((hlt_classic_single_tau_pt>0)*hlt_classic_single_tau_neutralCandsPtSumSignal)'

                tree.Draw((draw_var+'{e}:{tau_pt}>>{h}').format(e=extra_draw_var, tau=tau_name, tau_pt=tau_pt_name, h=hist_s_name), cut_s)
                tree.Draw((draw_var+'{e}:{tau_pt}>>{h}').format(e=extra_draw_var, tau=tau_name, tau_pt=tau_pt_name, h=hist_b_name), cut_b)

                # Find max eff_s for given eff_b

                for target_eff_b in effs_b:
                    print 'Target eff b', target_eff_b

                    best_eff_b = -1.
                    best_eff_s = -1.
                    best_i_x = -1
                    best_i_y = -1

                    int_s = hist_s.Integral(0, n_bins_x+1, 0, n_bins_y+1)
                    int_b = hist_b.Integral(0, n_bins_x+1, 0, n_bins_y+1)

                    for i_x in xrange(n_bins_x+1):
                        for i_y in xrange(n_bins_y+1):
                            eff_s = hist_s.Integral(i_x, n_bins_x+1, 0, i_y)/int_s
                            eff_b = hist_b.Integral(i_x, n_bins_x+1, 0, i_y)/int_b

                            if eff_b < target_eff_b and eff_s > best_eff_s:
                                best_eff_s = eff_s
                                best_eff_b = eff_b
                                best_i_x = i_x
                                best_i_y = i_y

                    print 'Obtained best eff_s', best_eff_s
                    print ' for eff_b', best_eff_b, 'while target was', target_eff_b
                    print ' cut x', xmin + best_i_x*(xmax-xmin)/n_bins_x, 'cut y', ymin + best_i_y*(ymax-ymin)/n_bins_y

                    effs[dict_tau_name].append((best_eff_b, best_eff_s, hist_s.GetXaxis().GetBinCenter(best_i_x), hist_s.GetYaxis().GetBinCenter(best_i_y)))

            import pickle
            pickle.dump(effs, open('effs_{v}_{d}_{c}.pkl'.format(v=var_name, d=cut_name, c=signal_cut_name), 'wb'))
