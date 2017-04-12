from officialStyle import officialStyle

from CMGTools.H2TauTau.proto.plotter.PlotConfigs import HistogramCfg, VariableCfg, SampleCfg
from CMGTools.H2TauTau.proto.plotter.HistCreator import createHistogram
from CMGTools.H2TauTau.proto.plotter.HistDrawer import HistDrawer

from ROOT import gStyle

from CMGTools.H2TauTau.proto.plotter.officialStyle import officialStyle
officialStyle(gStyle)

total_weight = '1'
tree_prod_name = 'HLTTauTreeProducer'
analysis_dir = '/afs/cern.ch/user/s/steggema/work/80/CMSSW_8_0_21/src/CMGTools/H2TauTau/cfgPython/generic/HPSCollated'
int_lumi = 1.

samples = [
    SampleCfg(name='ggH135', dir_name='ggH135_rawaod', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, xsec=1., sumweights=1.),
    SampleCfg(name='ggH135_2', dir_name='ggH135_rawaod_2', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, xsec=1., sumweights=1.),
]

tau_dm_string = '(tau_decayMode==0 || tau_decayMode==1 || tau_decayMode==10)*(tau_decayMode - 8*(tau_decayMode==10)) - 1 *(!(tau_decayMode==0 || tau_decayMode==1 || tau_decayMode==10))'

variables = [
    VariableCfg(name='dm_migration', drawname=tau_dm_string+':'+tau_dm_string.replace('tau', 'hlt_single_tau'), binning={'nbinsx':4, 'xmin':-1, 'xmax':3, 'nbinsy':4, 'ymin':-1, 'ymax':3}, unit=None, xtitle='Offline DM', ytitle='HLT DM'),
]

cut = ' abs(tau_gen_pdgId)==15 && ((hlt_single_tau_pt>20 || tau_pt > 20) && (abs(hlt_single_tau_eta)<2.3 || abs(tau_eta) < 2.3))'


for var in variables:
    cfg = HistogramCfg(name='dm_migration', var=var, cfgs=samples, cut=cut, lumi=int_lumi, weight=total_weight)

    plot = createHistogram(cfg, verbose=True)

    hist = plot.GetStack().totalHist.weighted

    label = ['None', '#pi', '#pi#pi^{0}s', '#pi#pi#pi']
    for xbin in range(1, hist.GetXaxis().GetNbins()+1):
        hist.GetXaxis().SetBinLabel(xbin, label[xbin-1])
        hist.GetYaxis().SetBinLabel(xbin, label[xbin-1])
    hist.DrawNormalized()
    import pdb; pdb.set_trace()
'''
hdecay = TH2F('decay', 'decay', 4, 0, 4, 4, 0, 4)

for target in ['m_vis']:
    for dmid, dm in enumerate(['1p', '1pp0', '3p']):

        if target == 'm_2' and dm in ['1p']:
            continue

        for gendmid, gendm in enumerate(['1p', '1pp0', '3p']):

            filename = 'datacard/datacard_template_' + \
                dm + '_gen' + gendm + '_' + target + '.root'
            file = TFile(filename)
            hist = file.Get('mt_signal/ZTT')
            entry = int(hist.Integral(0, hist.GetNbinsX()+1))
# print 'reco = ', dm, 'gen = ', gendm, int(hist.Integral(0,
# hist.GetNbinsX()+1))

            hdecay.SetBinContent(gendmid+1, dmid+1, entry)


hdecay.GetXaxis().SetTitle('Generated #tau_{h} mode')
hdecay.GetYaxis().SetTitle('Reconstructed #tau_{h} mode')
hdecay.SetMarkerSize(2.3)

canvas = TCanvas('decay_mode_matrix')
label = ['#pi', '#pi#pi^{0}s', '#pi#pi#pi']
for xbin in range(1, hdecay.GetXaxis().GetNbins()+1):
    hdecay.GetXaxis().SetBinLabel(xbin, label[xbin-1])
    hdecay.GetYaxis().SetBinLabel(xbin, label[xbin-1])

hdecay.Draw('text')
canvas.SaveAs('decaymode_matrix_raw.gif')

canvas_norm = TCanvas('decay_mode_matrix_norm')
# normalize for each bin
for xbin in range(1, hdecay.GetXaxis().GetNbins()+1):
    total = 0.
    for ybin in range(1, hdecay.GetYaxis().GetNbins()+1):
        total += hdecay.GetBinContent(xbin, ybin)

    for ybin in range(1, hdecay.GetYaxis().GetNbins()+1):
        entry = hdecay.GetBinContent(xbin, ybin)
        frac = Double(entry/total)
        print xbin, ybin, frac

        hdecay.SetBinContent(xbin, ybin, frac)


hdecay.Draw("text")

canvas_norm.SaveAs('decaymode_matrix.gif')
'''