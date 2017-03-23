from copy import copy

from CMGTools.H2TauTau.proto.plotter.PlotConfigs import HistogramCfg, VariableCfg, SampleCfg
from CMGTools.H2TauTau.proto.plotter.HistCreator import createHistogram
from CMGTools.H2TauTau.proto.plotter.HistDrawer import HistDrawer

from ROOT import gStyle

from CMGTools.H2TauTau.proto.plotter.officialStyle import officialStyle
officialStyle(gStyle)

# total_weight = 'weight * ' + getPUWeight()

only_stack = False

total_weight = '1'
tree_prod_name = 'HLTTauTreeProducer'
analysis_dir = '/afs/cern.ch/user/s/steggema/work/80/CMSSW_8_0_21/src/CMGTools/H2TauTau/cfgPython/generic/HPSReClassicDMFix'
int_lumi = 1.

samples = [
    SampleCfg(name='ggH135', dir_name='ggH135_rawaod', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, xsec=1., sumweights=1.),
    SampleCfg(name='ggH135_2', dir_name='ggH135_rawaod_2', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, xsec=1., sumweights=1.),
]

any_hlt_tau = '&& (hlt_tau_pt > 0 || hlt_classic_tau_pt > 0)'

cuts = {
    # 'any_gen_tau':'TAU_pt>0 && TAU_gen_pt>0 && abs(TAU_gen_pdgId)==15'+any_hlt_tau,
    # 'dm0_gen_tau':'TAU_pt>0 && TAU_gen_pt>0 && abs(TAU_gen_pdgId)==15 && TAU_gen_decayMode==0'+any_hlt_tau,
    # 'dm1_gen_tau':'TAU_pt>0 && TAU_gen_pt>0 && abs(TAU_gen_pdgId)==15 && TAU_gen_decayMode==1'+any_hlt_tau,
    # 'dm10_gen_tau':'TAU_pt>0 && TAU_gen_pt>0 && abs(TAU_gen_pdgId)==15 && TAU_gen_decayMode==10'+any_hlt_tau,
    'jets':'TAU_pt>0 && (abs(TAU_gen_pdgId)<6 || TAU_gen_pdgId>20)'+any_hlt_tau,
}

tau_name = 'TAU'

variables = [
    VariableCfg(name='rho', binning={'nbinsx':80, 'xmin':0, 'xmax':80}, unit='GeV', xtitle='#rho'),
    VariableCfg(name=tau_name+'_reso', drawname='TAU_pt-TAU_gen_pt', binning={'nbinsx':80, 'xmin':-50, 'xmax':50}, unit='GeV', xtitle='p_{T} - gen p_{T}'),
    VariableCfg(name=tau_name+'_pt', binning={'nbinsx':30, 'xmin':0., 'xmax':150.}, unit='GeV', xtitle='p_{T}'),
    VariableCfg(name=tau_name+'_isreco', drawname=tau_name+'_pt>0.', binning={'nbinsx':2, 'xmin':-0.5, 'xmax':1.5}, unit='', xtitle='is reconstructed (p_{T} > 0 GeV)'),
    VariableCfg(name=tau_name+'_isreco20', drawname=tau_name+'_pt>20.', binning={'nbinsx':2, 'xmin':-0.5, 'xmax':1.5}, unit='', xtitle='is reconstructed (p_{T} > 20 GeV)'),
    VariableCfg(name=tau_name+'_isreco35', drawname=tau_name+'_pt>35.', binning={'nbinsx':2, 'xmin':-0.5, 'xmax':1.5}, unit='', xtitle='is reconstructed (p_{T} > 35 GeV)'),
    VariableCfg(name=tau_name+'_decayMode', binning={'nbinsx':15, 'xmin':-0., 'xmax':14.5}, unit=None, xtitle='decay mode'),
    VariableCfg(name=tau_name+'_dm', binning={'nbinsx':2, 'xmin':-0.5, 'xmax':1.5}, unit=None, xtitle='decay mode finding'),
    VariableCfg(name=tau_name+'_chargedPtSumIso', binning={'nbinsx':50, 'xmin':0., 'xmax':50.}, unit='GeV', xtitle='iso charged pT sum'),
    VariableCfg(name=tau_name+'_gammaCandsPtSumSignal', binning={'nbinsx':40, 'xmin':0., 'xmax':50.}, unit=None, xtitle='signal photon pT sum'),
    VariableCfg(name=tau_name+'_neutralCandsPtSumSignal', binning={'nbinsx':40, 'xmin':0., 'xmax':50.}, unit=None, xtitle='signal neutral pT sum'),
    VariableCfg(name=tau_name+'_gammaPtSumIso', binning={'nbinsx':40, 'xmin':0., 'xmax':70.}, unit=None, xtitle='iso photon pT sum'),
    # VariableCfg(name=tau_name+'_neutralPtSumIso', binning={'nbinsx':40, 'xmin':0., 'xmax':50.}, unit=None, xtitle='iso neutral pT sum'),
    VariableCfg(name=tau_name+'_gammaPtSumIso_rhocorr', drawname=tau_name+'_gammaPtSumIso - rho*0.1752', binning={'nbinsx':40, 'xmin':-10., 'xmax':60.}, unit=None, xtitle='rho-corr iso photon pT sum'),
    VariableCfg(name=tau_name+'_combIso_rhocorr', drawname=tau_name+'_chargedPtSumIso + max('+tau_name+'_gammaPtSumIso - rho*0.1752, 0)', binning={'nbinsx':40, 'xmin':-10., 'xmax':60.}, unit=None, xtitle='rho-corr combined isolation'),
    VariableCfg(name=tau_name+'_combIso_dbetacorr', drawname=tau_name+'_chargedPtSumIso + max('+tau_name+'_gammaPtSumIso - '+tau_name+'_chargedPUPtSumIso*0.2, 0)', binning={'nbinsx':40, 'xmin':-10., 'xmax':60.}, unit=None, xtitle='rho-corr combined isolation'),
    VariableCfg(name=tau_name+'_dm_plus_pt30', drawname=tau_name+'_dm == 1 && '+tau_name+'_pt>30', binning={'nbinsx':2, 'xmin':-0.5, 'xmax':1.5}, unit=None, xtitle='decay mode finding'),
    VariableCfg(name=tau_name+'_dm_plus_pt40', drawname=tau_name+'_dm == 1 && '+tau_name+'_pt>40', binning={'nbinsx':2, 'xmin':-0.5, 'xmax':1.5}, unit=None, xtitle='decay mode finding'),
]


from ROOT import TCanvas, TLegend
can = TCanvas('can', '', 800, 800)

for cut_name, cut in cuts.items():
    cfgs = {}
    tau_names = ['tau', 'hlt_tau', 'hlt_classic_tau']
    for tau_name in tau_names:
        cfgs[tau_name] = HistogramCfg(name=cut_name+tau_name, var=None, cfgs=samples, cut=cut, lumi=int_lumi, weight=total_weight)

    for variable in variables:
        colours = [1, 2, 4]
        styles = [2, 1, 3]

        legend = TLegend(0.68, 0.68, 0.93, 0.91)
        legend.SetFillColor(0)
        legend.SetFillStyle(0)
        legend.SetLineColor(0)
        legend.SetLineWidth(0)
        legend.SetTextFont(42)
        legend.SetBorderSize(0)

        hists = []
        titles = ['Offline', 'HLT HPS', 'HLT standard']

        for i_cfg, (cfg, tau_name) in enumerate(zip(cfgs.values(), tau_names)):
            cfg.var = copy(variable)
            cfg.var.name = cfg.var.name.replace('TAU', tau_name)
            if cfg.var.drawname:
                cfg.var.drawname = cfg.var.drawname.replace('TAU', tau_name)
            cfg.cut = cfg.cut.replace('TAU', tau_name)
            print cfg.var

            plot = createHistogram(cfg, verbose=True)
        
            hist = plot.GetStack().totalHist.weighted

            # Keep overflow            
            nbins = hist.GetNbinsX()
            hist.SetBinContent(nbins, hist.GetBinContent(nbins)+hist.GetBinContent(nbins+1))

            # hist_s.Scale(1./hist_s.Integral())

            hist.SetLineColor(colours[i_cfg])
            hist.SetLineStyle(styles[i_cfg])
            hist.SetFillColor(0)
            hist.SetLineWidth(4)
            hist.plot = plot

            legend.AddEntry(hist, titles[i_cfg], 'l')

            hists.append(hist)

        for i, hist in enumerate(hists):
            hist.GetYaxis().SetRangeUser(0., 1.3*max(h.GetMaximum() for h in hists))
            hist.Draw('HIST' if i == 0 else 'SAME HIST')

        legend.Draw()
        can.Print('plots_reco/'+variable.name+'_'+cut_name+'.pdf')
