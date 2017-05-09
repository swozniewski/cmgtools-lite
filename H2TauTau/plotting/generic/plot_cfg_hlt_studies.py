from copy import deepcopy as copy

from CMGTools.H2TauTau.proto.plotter.PlotConfigs import HistogramCfg, VariableCfg, SampleCfg
from CMGTools.H2TauTau.proto.plotter.HistCreator import createHistogram
from CMGTools.H2TauTau.proto.plotter.HistDrawer import HistDrawer

from CMGTools.H2TauTau.proto.plotter.helper_methods import plotDataOverMCEff
from CMGTools.H2TauTau.proto.plotter.ROCPlotter import histsToRoc, makeROCPlot

from ROOT import gStyle

from CMGTools.H2TauTau.proto.plotter.officialStyle import officialStyle
officialStyle(gStyle)

# total_weight = 'weight * ' + getPUWeight()

only_stack = False

total_weight = '1'
tree_prod_name = 'HLTTauTreeProducer'
analysis_dir = '/afs/cern.ch/user/s/steggema/work/80/CMSSW_8_0_21/src/CMGTools/H2TauTau/cfgPython/generic/HPSRecoverMoreInfo'
int_lumi = 1.

samples = [
    SampleCfg(name='ggH135', dir_name='ggH135_rawaod', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, xsec=1., sumweights=1.),
    SampleCfg(name='ggH135_2', dir_name='ggH135_rawaod_2', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, xsec=1., sumweights=1.),
]

cuts = {}
# cuts['any_hlt_tau'] = '((hlt_single_tau_pt>20 || hlt_tau_pt > 20 || hlt_classic_tau_pt > 20 || hlt_classic_single_tau_pt > 20) && (abs(hlt_single_tau_eta)<2.3 || abs(hlt_tau_eta) < 2.3 || abs(hlt_classic_tau_eta) <2.3 || abs(hlt_classic_single_tau_eta) < 2.3))'
cuts['any_tau'] = '((hlt_single_tau_pt>20 || hlt_tau_pt > 20 || hlt_classic_tau_pt > 20 || hlt_classic_single_tau_pt > 20 || tau_pt > 20) && (abs(hlt_single_tau_eta)<2.3 || abs(hlt_tau_eta) < 2.3 || abs(hlt_classic_tau_eta) <2.3 || abs(hlt_classic_single_tau_eta) < 2.3 || abs(tau_eta) < 2.3))'
# cuts['offline_tau'] = '(tau_pt > 20)'


# for tau_name in ['tau', 'hlt_tau', 'hlt_single_tau']:
tau_name = 'TAU'
variables = [
    # VariableCfg(name='jet_pt', binning=array([20., 30., 40., 50., 60., 80., 100., 120., 140., 160., 180., 200., 250., 300., 350.]), unit='GeV', xtitle='jet p_{T}'),
    # VariableCfg(name='rho', binning={'nbinsx':80, 'xmin':0, 'xmax':80}, unit='GeV', xtitle='#rho'),
    VariableCfg(name=tau_name+'_pt', binning={'nbinsx':30, 'xmin':0., 'xmax':150.}, unit='GeV', xtitle='p_{T}'),
    VariableCfg(name=tau_name+'_eta', binning={'nbinsx':48, 'xmin':-2.4, 'xmax':2.4}, unit=None, xtitle='#eta'),
    # # VariableCfg(name=tau_name+'_decayMode', binning={'nbinsx':15, 'xmin':-0., 'xmax':14.5}, unit=None, xtitle='decay mode'),
    # VariableCfg(name=tau_name+'_dm', binning={'nbinsx':2, 'xmin':-0.5, 'xmax':1.5}, unit=None, xtitle='decay mode finding'),
    VariableCfg(name=tau_name+'_chargedPtSumIso', drawname='abs('+tau_name+'_chargedPtSumIso)', binning={'nbinsx':10000, 'xmin':0., 'xmax':1000.}, unit='GeV', xtitle='iso charged pT sum'),
    VariableCfg(name=tau_name+'_chargedPtSumIso04', drawname='abs('+tau_name+'_chargedPtSumIso04)', binning={'nbinsx':10000, 'xmin':0., 'xmax':1000.}, unit='GeV', xtitle='iso charged pT sum (cone 0.4)'),
    VariableCfg(name=tau_name+'_chargedPtSumIso03', drawname='abs('+tau_name+'_chargedPtSumIso03)', binning={'nbinsx':10000, 'xmin':0., 'xmax':1000.}, unit='GeV', xtitle='iso charged pT sum (cone 0.3)'),
    VariableCfg(name=tau_name+'_gammaPtSumIso', drawname='abs('+tau_name+'_gammaPtSumIso)', binning={'nbinsx':40, 'xmin':0., 'xmax':70.}, unit=None, xtitle='iso photon pT sum'),
    VariableCfg(name=tau_name+'_gammaPtSumIso04', drawname='abs('+tau_name+'_gammaPtSumIso04)', binning={'nbinsx':40, 'xmin':0., 'xmax':70.}, unit=None, xtitle='iso photon pT sum (cone 0.4)'),
    VariableCfg(name=tau_name+'_gammaPtSumIso04Pt1', drawname='abs('+tau_name+'_gammaPtSumIso04Pt1)', binning={'nbinsx':40, 'xmin':0., 'xmax':70.}, unit=None, xtitle='iso photon pT sum (cone 0.4, p+{T} > 1 GeV)'),
    # # VariableCfg(name=tau_name+'_neutralPtSumIso', binning={'nbinsx':40, 'xmin':0., 'xmax':50.}, unit=None, xtitle='iso neutral pT sum'),
    VariableCfg(name=tau_name+'_gammaPtSumIso_rhocorr', drawname='abs('+tau_name+'_gammaPtSumIso) - rho*0.1752', binning={'nbinsx':40, 'xmin':-10., 'xmax':60.}, unit=None, xtitle='rho-corr iso photon pT sum'),
    VariableCfg(name=tau_name+'_combIso_rhocorr', drawname='abs('+tau_name+'_chargedPtSumIso) + max('+tau_name+'_gammaPtSumIso - rho*0.1752, 0)', binning={'nbinsx':40, 'xmin':-10., 'xmax':60.}, unit=None, xtitle='rho-corr combined isolation'),
    VariableCfg(name=tau_name+'_combIso_dbetacorr', drawname='abs('+tau_name+'_chargedPtSumIso) + max('+tau_name+'_gammaPtSumIso - '+tau_name+'_chargedPUPtSumIso*0.2, 0)', binning={'nbinsx':40, 'xmin':-10., 'xmax':60.}, unit=None, xtitle='rho-corr combined isolation'),
    VariableCfg(name=tau_name+'_gammaPtSumOutsideSignalCone', binning={'nbinsx':40, 'xmin':0., 'xmax':40.}, unit=None, xtitle='photon pT sum outside signal cone'),
    # VariableCfg(name=tau_name+'_dm_plus_pt30', drawname=tau_name+'_dm == 1 && '+tau_name+'_pt>30', binning={'nbinsx':2, 'xmin':-0.5, 'xmax':1.5}, unit=None, xtitle='decay mode finding'),
    # VariableCfg(name=tau_name+'_dm_plus_pt40', drawname=tau_name+'_dm == 1 && '+tau_name+'_pt>40', binning={'nbinsx':2, 'xmin':-0.5, 'xmax':1.5}, unit=None, xtitle='decay mode finding'),
]



# variables = all_vars

tau_names = ['tau', 'hlt_single_tau', 'hlt_classic_single_tau'] # 'hlt_tau', 'hlt_classic_tau', 

sb_cuts = {
    'gen_tau_45':{
        's':'&& (abs(tau_gen_pdgId)==15 && tau_gen_pt>45 && abs(tau_gen_eta)<2.3)',
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

from ROOT import TCanvas, TLegend
can = TCanvas('can', '', 800, 800)

for cut_name, cut in cuts.items():
    for signal_cut_name, cuts in sb_cuts.items():
        cut_s = cuts['s']
        cut_b = cuts['b']

        cfg_s = HistogramCfg(name=cut_name+'_'+signal_cut_name+'s', var=None, cfgs=samples, cut=cut + cut_s, lumi=int_lumi, weight=total_weight)
        cfg_b = HistogramCfg(name=cut_name+signal_cut_name+'b', var=None, cfgs=samples, cut=cut + cut_b, lumi=int_lumi, weight=total_weight)
        
        pt_cut = '45'
        if '25' in signal_cut_name:
            pt_cut = '20'
        if '40' in signal_cut_name:
            pt_cut = '35'

        for variable in variables:
            rocs = []
            for tau_name in tau_names:
                cfg_s.var = copy(variable)
                cfg_b.var = copy(variable)
                cfg_s.var.name = cfg_s.var.name.replace('TAU', tau_name)
                cfg_b.var.name = cfg_b.var.name.replace('TAU', tau_name)
                if cfg_s.var.drawname:
                    cfg_s.var.drawname = cfg_s.var.drawname.replace('TAU', tau_name)
                    cfg_b.var.drawname = cfg_b.var.drawname.replace('TAU', tau_name)
                
                # If we test isolation, we want a fixed pT cut
                if any('Iso' in name for name in [cfg_s.var.name, cfg_b.var.name, cfg_s.var.drawname, cfg_b.var.drawname]):
                    if tau_name in ['hlt_tau', 'hlt_single_tau']:
                        cfg_s.var.drawname += ' + 99.*({tau}_pt<{pt_cut} || abs({tau}_eta)>2.3)'.format(pt_cut=str(int(pt_cut)-10), tau=tau_name)
                        cfg_b.var.drawname += ' + 99.*({tau}_pt<{pt_cut} || abs({tau}_eta)>2.3)'.format(pt_cut=str(int(pt_cut)-10), tau=tau_name)
                    else:
                        cfg_s.var.drawname += ' + 99.*({tau}_pt<{pt_cut} || abs({tau}_eta)>2.3)'.format(pt_cut=pt_cut, tau=tau_name)
                        cfg_b.var.drawname += ' + 99.*({tau}_pt<{pt_cut} || abs({tau}_eta)>2.3)'.format(pt_cut=pt_cut, tau=tau_name)


                # If we test pT, we want a fixed isolation cut
                if cfg_s.var.name == tau_name+'_pt':
                    cfg_s.var.drawname += '- 99.*(abs({tau}_chargedPtSumIso)>2.)'.format(tau=tau_name)
                    cfg_b.var.drawname += '- 99.*(abs({tau}_chargedPtSumIso)>2.)'.format(tau=tau_name)
                    

                # # We always want to use DM finding, except for tests
                # if tau_name in ['tau', 'hlt_tau', 'hlt_single_tau'] and not 'dm_' in cfg_s.var.name:
                #     cfg_s.var.drawname += ' + 9999.*({tau}_dm<0.5)'.format(tau=tau_name)
                #     cfg_b.var.drawname += ' + 9999.*({tau}_dm<0.5)'.format(tau=tau_name)

                apply_dm = True

                if apply_dm:
                    if tau_name in ['tau', 'hlt_tau', 'hlt_single_tau'] and not 'dm_' in cfg_s.var.name:
                        if cfg_s.var.name == tau_name+'_pt':
                            cfg_s.var.drawname += ' -250.*(!({tau}_decayMode==0 || {tau}_decayMode==1 || {tau}_decayMode==10))'.format(tau=tau_name)
                            cfg_b.var.drawname += ' -250.*(!({tau}_decayMode==0 || {tau}_decayMode==1 || {tau}_decayMode==10))'.format(tau=tau_name)
                        else:
                            cfg_s.var.drawname += ' + 250.*(!({tau}_decayMode==0 || {tau}_decayMode==1 || {tau}_decayMode==10))'.format(tau=tau_name)
                            cfg_b.var.drawname += ' + 250.*(!({tau}_decayMode==0 || {tau}_decayMode==1 || {tau}_decayMode==10))'.format(tau=tau_name)

                print cfg_s.var
                print cfg_s.var.drawname

                plot_s = createHistogram(cfg_s, verbose=True)
                plot_b = createHistogram(cfg_b, verbose=True)

                hist_s = plot_s.GetStack().totalHist.weighted
                hist_b = plot_b.GetStack().totalHist.weighted

                # Keep overflow            
                nbins = hist_s.GetNbinsX()
                hist_s.SetBinContent(nbins, hist_s.GetBinContent(nbins)+hist_s.GetBinContent(nbins+1))
                hist_b.SetBinContent(nbins, hist_b.GetBinContent(nbins)+hist_b.GetBinContent(nbins+1))

                if hist_s.Integral() > 0:
                    hist_s.Scale(1./hist_s.Integral()*hist_b.Integral())
                else:
                    continue

                hist_s.SetLineColor(2)
                hist_s.SetLineStyle(1)
                hist_s.SetFillColor(0)
                hist_s.SetLineWidth(4)

                hist_b.SetLineStyle(2)
                hist_b.SetFillColor(0)
                hist_b.SetLineWidth(4)

                hist_s.Draw('HIST')
                hist_s.GetYaxis().SetRangeUser(0., 1.3*max(hist_s.GetMaximum(), hist_b.GetMaximum()))

                hist_b.Draw('SAME HIST')

                legend = TLegend(0.68, 0.68, 0.93, 0.91)
                legend.SetFillColor(0)
                legend.SetFillStyle(0)
                legend.SetLineColor(0)
                legend.SetLineWidth(0)
                legend.SetTextFont(42)
                legend.SetBorderSize(0)

                tau_type = 'Offline HPS'
                if cfg_s.var.name.startswith('hlt_tau'):
                    tau_type = 'HLT HPS'
                elif cfg_s.var.name.startswith('hlt_single_tau'):
                    tau_type = 'sHLT HPS'
                elif cfg_s.var.name.startswith('hlt_classic_tau'):
                    tau_type = 'HLT classic'
                elif cfg_s.var.name.startswith('hlt_classic_single_tau'):
                    tau_type = 'sHLT classic'

                legend.AddEntry(None, tau_type, '')
                legend.AddEntry(hist_s, 'taus', 'l')
                legend.AddEntry(hist_b, 'jets', 'l')
                legend.Draw()
                can.Print('plots/'+cfg_s.var.name+cfg_s.name+'.pdf')

                roc = histsToRoc(hist_s, hist_b)
                print '\n#### For tau', tau_name
                print 'Eff_s for cut 2 GeV', hist_s.Integral(0, hist_s.FindBin(2.))/hist_s.Integral(0, hist_s.GetNbinsX()+2)
                print 'Eff_b for cut 2 GeV', hist_b.Integral(0, hist_b.FindBin(2.))/hist_b.Integral(0, hist_b.GetNbinsX()+2)
                roc.name = tau_type
                roc.title = tau_type

                rocs.append(roc)

                if not 'TAU' in variable.name:
                    break

            if 'TAU' in variable.name:
                makeROCPlot(rocs, 'roc'+variable.name+cfg_s.name, xmin=0.)
