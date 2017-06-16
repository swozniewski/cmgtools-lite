from CMGTools.H2TauTau.proto.plotter.PlotConfigs import HistogramCfg, VariableCfg, SampleCfg
from CMGTools.H2TauTau.proto.plotter.HistCreator import createHistogram
from CMGTools.H2TauTau.proto.plotter.HistDrawer import HistDrawer

from ROOT import gStyle, TCanvas

from CMGTools.H2TauTau.proto.plotter.officialStyle import officialStyle
officialStyle(gStyle)

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

tau_dm_string = '(tau_pt>30)*((tau_decayMode==0 || tau_decayMode==1 || tau_decayMode==2 || tau_decayMode==10 || tau_decayMode==11)*(tau_decayMode - 8*(tau_decayMode==10) - 8*(tau_decayMode==11) - 1*(tau_decayMode==2)) - 1 *(!(tau_decayMode==0 || tau_decayMode==1 || tau_decayMode==2|| tau_decayMode==10|| tau_decayMode==11) && tau_decayMode>0 && tau_decayMode<200) - 2 *(!(tau_decayMode==0 || tau_decayMode==1 || tau_decayMode==2 || tau_decayMode==10 || tau_decayMode==11) && (tau_decayMode<0 || tau_decayMode>=200))) - 2*(tau_pt<30)'

variables = [
    VariableCfg(name='dm_migration_rec_hlt', drawname=tau_dm_string.replace('tau', 'hlt_single_tau')+':'+tau_dm_string, binning={'nbinsx':6, 'xmin':-2, 'xmax':4, 'nbinsy':6, 'ymin':-2, 'ymax':4}, unit=None, xtitle='Offline DM', ytitle='HLT DM'),
    VariableCfg(name='dm_migration_hlt_rec', drawname=tau_dm_string+':'+tau_dm_string.replace('tau', 'hlt_single_tau'), binning={'nbinsx':6, 'xmin':-2, 'xmax':4, 'nbinsy':6, 'ymin':-2, 'ymax':4}, unit=None, xtitle='HLT DM', ytitle='Offline DM'),
    VariableCfg(name='dm_migration_gen_rec', drawname=tau_dm_string+':'+tau_dm_string.replace('tau', 'tau_gen'), binning={'nbinsx':6, 'xmin':-2, 'xmax':4, 'nbinsy':6, 'ymin':-2, 'ymax':4}, unit=None, xtitle='Gen DM', ytitle='Offline DM'),
    VariableCfg(name='dm_migration_gen_hlt', drawname=tau_dm_string.replace('tau', 'hlt_single_tau')+':'+tau_dm_string.replace('tau', 'tau_gen'), binning={'nbinsx':6, 'xmin':-2, 'xmax':4, 'nbinsy':6, 'ymin':-2, 'ymax':4}, unit=None, xtitle='Gen DM', ytitle='HLT DM'),
    VariableCfg(name='dm_migration_gen_shrinkinghlt', drawname='-(hlt_classic_single_tau_pt>20) - 2 *(hlt_classic_single_tau_pt<20) '+':'+tau_dm_string.replace('tau', 'tau_gen'), binning={'nbinsx':6, 'xmin':-2, 'xmax':4, 'nbinsy':6, 'ymin':-2, 'ymax':4}, unit=None, xtitle='Gen DM', ytitle='HLT DM'),
]

cut = 'tau_gen_pt>40 && abs(tau_gen_eta)<2.3'# && abs(tau_gen_pdgId)==15 && ((hlt_single_tau_pt>20 && abs(hlt_single_tau_eta)<2.3) || (tau_pt > 20 && abs(tau_eta) < 2.3))'

canvas = TCanvas('decay_mode_matrix')

for var in variables:
    cfg = HistogramCfg(name='dm_migration', var=var, cfgs=samples, cut=cut, lumi=int_lumi, weight=total_weight)

    plot = createHistogram(cfg, verbose=True)

    hist = plot.GetStack().totalHist.weighted

    label = ['None', 'Other', '#pi', '#pi#pi^{0}s', '#pi#pi#pi', '#pi#pi#pi#pi^{0}s']
    for xbin in range(1, hist.GetXaxis().GetNbins()+1):
        hist.GetXaxis().SetBinLabel(xbin, label[xbin-1])
        hist.GetYaxis().SetBinLabel(xbin, label[xbin-1])

    # if 'Gen' in var.xtitle:
    #     hist.GetXaxis().SetBinLabel(1, 'Other')

    hist.GetYaxis().SetTitle(var.ytitle)

    for xbin in xrange(1, hist.GetNbinsX()+1):
        int_y = sum(hist.GetBinContent(xbin, ybin) for ybin in xrange(1, hist.GetNbinsY()+1))
        if int_y == 0.:
            int_y = 1.
        for ybin in xrange(1, hist.GetNbinsY()+1):
            # cont = round(hist.GetBinContent(xbin, ybin)/int_y, 2)
            hist.SetBinContent(xbin, ybin, hist.GetBinContent(xbin, ybin)/int_y)

    hist.Draw('TEXT')
    hist.GetYaxis().SetTitleOffset(1.2)
    hist.GetXaxis().SetTitleOffset(1.0)
    hist.SetMarkerColor(1)
    hist.SetMarkerSize(2.2)
    gStyle.SetPaintTextFormat("1.2f")

    canvas.Print('dm_migration_'+var.name+'.pdf')
    


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