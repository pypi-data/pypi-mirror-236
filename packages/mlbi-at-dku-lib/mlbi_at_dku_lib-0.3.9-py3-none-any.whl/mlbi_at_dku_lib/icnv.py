import warnings, math, time, copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import cluster, mixture
from sklearn.neighbors import kneighbors_graph
from sknetwork.clustering import Louvain

import scanpy as sc
import infercnvpy as cnv

cell_cycle_genes_s = ['ATAD2', 'BLM', 'BRIP1', 'CASP8AP2', 'CCNE2',
         'CDC45', 'CDC6', 'CDCA7', 'CHAF1B', 'CLSPN', 'DSCC1',
         'DTL', 'E2F8', 'EXO1', 'FEN1', 'GINS2', 'GMNN', 'HELLS',
         'MCM2', 'MCM4', 'MCM5', 'MCM6', 'MLF1IP', 'MSH2', 'NASP',
         'PCNA', 'POLA1', 'POLD3', 'PRIM1', 'RAD51', 'RAD51AP1',
         'RFC2', 'RPA2', 'RRM1', 'RRM2', 'SLBP', 'TIPIN', 'TYMS',
         'UBR7', 'UHRF1', 'UNG', 'USP1', 'WDR76']

cell_cycle_genes_g2m = ['ANLN', 'ANP32E', 'AURKA', 'AURKB', 'BIRC5',
         'BUB1', 'CBX5', 'CCNB2', 'CDC20', 'CDC25C', 'CDCA2',
         'CDCA3', 'CDCA8', 'CDK1', 'CENPA', 'CENPE', 'CENPF',
         'CKAP2', 'CKAP2L', 'CKAP5', 'CKS1B', 'CKS2', 'CTCF',
         'DLGAP5', 'ECT2', 'FAM64A', 'G2E3', 'GAS2L3', 'GTSE1',
         'HJURP', 'HMGB2', 'HMMR', 'HN1', 'KIF11', 'KIF20B', 'KIF23',
         'KIF2C', 'LBR', 'MKI67', 'NCAPD2', 'NDC80', 'NEK2', 'NUF2',
         'NUSAP1', 'PSRC1', 'RANGAP1', 'SMC4', 'TACC3', 'TMPO', 'TOP2A',
         'TPX2', 'TTK', 'TUBB4B', 'UBE2C']

MIN_ABS_VALUE = 1e-8

def bimodal_fit( x ):
    
    df_param = pd.DataFrame( columns = ['value'], \
                          index = ['w0', 'm0', 'v0', 'w1', 'm1', 'v1'] )
    
    gmm = mixture.GaussianMixture(n_components = 2, random_state = 0)
    y = gmm.fit_predict(np.array(x).reshape(-1, 1))

    mns = [m[0] for m in gmm.means_]
    cvs = [cv[0,0] for cv in gmm.covariances_]

    wgs = gmm.weights_           
    if mns[0] < mns[1]:
        w0, w1 = wgs[0], wgs[1]
        m0, m1 = mns[0], mns[1]
        v0, v1 = cvs[0], cvs[1]
    else:
        w0, w1 = wgs[1], wgs[0]
        m0, m1 = mns[1], mns[0]
        v0, v1 = cvs[1], cvs[0]

    param = [w0, m0, v0, w1, m1, v1]
    df_param['value'] = param
            
    return df_param['value']
        
        
def get_normal_pdf( x, mu, var, nbins):
    
    y = np.array(x)
    mn_x = y.min()
    mx_x = y.max()
    dx = mx_x - mn_x
    mn_x -= dx/4
    mx_x += dx/4
    L = 100
    # dx = len(y)*(mx_x-mn_x)/L
    dx = (mx_x-mn_x)/nbins
    xs = np.arange(mn_x,mx_x, dx )
    pdf = (dx*len(y))*np.exp(-((xs-mu)**2)/(2*var+MIN_ABS_VALUE))/(np.sqrt(2*math.pi*var)+MIN_ABS_VALUE) + MIN_ABS_VALUE
    return pdf, xs


def get_malignancy_prob( xs, param ):
    
    w0, mu0, var0, w1, mu1, var1 = tuple(param)
    
    p0 = w0*np.exp(-((xs-mu0)**2)/(2*var0+MIN_ABS_VALUE))/(np.sqrt(2*math.pi*var0)+MIN_ABS_VALUE) + MIN_ABS_VALUE
    p1 = w1*np.exp(-((xs-mu1)**2)/(2*var1+MIN_ABS_VALUE))/(np.sqrt(2*math.pi*var1)+MIN_ABS_VALUE) + MIN_ABS_VALUE    
    pr = p1/(p0+p1)
    
    b = (xs < mu0)
    pr[b] = MIN_ABS_VALUE
    
    return pr


def get_cnv_threshold_bimodal( obs, ref_ind, score_key = 'cnv_score', 
                               cluster_key = 'cnv_leiden', th_min = 0, refp_min = 0.9, 
                               ucr = 0.1, plot_stat = True, suffix = '', Data = None ):
    
    ## obs must contain columns 'cnv_cluster', 'cnv_score'
    
    df = obs.groupby([cluster_key])[score_key].agg(**{'cmean':'mean'})
    idx_lst = list(df.index.values)
    
    ps = bimodal_fit( df['cmean'] )
    w0, m0, v0, w1, m1, v1 = tuple(ps)

    mxv = df['cmean'].max()
    mnv = df['cmean'].min()
    Dv = mxv - mnv
    dv = Dv/200
    n_bins = 50

    x = np.arange(mnv,mxv,dv)
    pdf0, xs0 = get_normal_pdf( x, m0, v0, 100)
    pdf1, xs1 = get_normal_pdf( x, m1, v1, 100)

    th = -1
    for k in range(len(xs0)):
        if (pdf1[k] >= pdf0[k]) & (xs0[k] > m0):
            th = xs0[k]
            break
            
    ss_div_dm = (np.sqrt(v1)+np.sqrt(v0))/(m1-m0)
    if ss_div_dm > 1:
        print('INFO: Std_sum/Mean_diff: %f > 1' % (ss_div_dm))
        print('INFO: indicating that no tumor cells might be present in this sample.' % (ss_div_dm))
        th = m0 + np.sqrt(v0)
            
    s = obs[score_key]
    tpr = get_malignancy_prob( s, list(ps) )
    obs['tumor_score'+ suffix] = tpr
    
    # print('threshold: ', th )
    th = max(th, th_min)
    
    dec = pd.Series(['Normal']*len(s), index = obs.index)
    
    lt = th - (th - m0)*ucr # p_exc 
    ut = th + (m1 - th)*ucr #p_exc
    
    bs = (s > th)
    df['dec'] = 'Normal'
    for idx in idx_lst:
        b1 = obs[cluster_key] == idx
        if df.loc[idx, 'cmean'] > ut:            
            dec[b1] = 'Tumor'
            df.loc[idx, 'dec'] = 'Tumor'
        elif df.loc[idx, 'cmean'] < lt:
            pass
        else:
            dec[b1] = 'unclear'
            df.loc[idx, 'dec'] = 'unclear'
                
    
    # b = (obs[ref_key].isin(ref_types)) | (s <= th)
    # dec[b] = 'Normal'    
    obs['tumor_dec'+ suffix] = dec
    
    tclust = dec.copy(deep = True)
    tclust[:] = None
    cnt = 1
    for c in idx_lst:
        b = obs[cluster_key] == c
        b1 = dec == 'Tumor'
        if np.sum(b&b1) > 0:
            tclust[b&b1] = 'Tumor_c%i' % cnt
            cnt += 1        
    obs['tumor_cluster'+ suffix] = tclust

    ss_div_dm = (np.sqrt(v1)+np.sqrt(v0))/(m1-m0)
    if ss_div_dm > 1:
        print('INFO: Std_sum/Mean_diff: %f > 1' % (ss_div_dm))
        print('INFO: indicating that no tumor cells might be present in this sample.' % (ss_div_dm))
    
    params = {}
    params['th'] = th
    params['m0'] = m0
    params['v0'] = v0
    params['w0'] = w0
    params['m1'] = m1
    params['v1'] = v1
    params['w1'] = w1
    params['df'] = df
    
    if plot_stat:
        plot_stats( params, n_bins = 30, title = None, title_fs = 14,
                    label_fs = 12, tick_fs = 11, legend_fs = 11, 
                    legend_loc = 'upper left', bbox_to_anchor = (1, 1),
                    figsize = (4,3), log = False, alpha = 0.8 )
        
    return obs[['tumor_dec'+ suffix, 'tumor_score'+ suffix]], params


def get_cnv_threshold_useref( obs, ref_ind, score_key = 'tumor_score', 
                              cluster_key = 'cnv_leiden', th_min = 0, refp_min = 0.9, 
                              p_exc = 0.1, ucr = 0.1, plot_stat = True, 
                              suffix = '', Data = None ):
    
    ## obs must contain columns 'cnv_cluster', 'cnv_score'
    start_time = time.time()
    
    # df = obs.groupby([cluster_key])[score_key].agg(**{'cmean':'median'})
    df = obs.groupby([cluster_key])[score_key].agg(**{'cmean':'mean'})
    idx_lst = list(df.index.values)
    
    ns = 0
    # while(ns == 0):
        
    b_inc = []
    df['Ref_percent'] = 0
    for idx in idx_lst:
        b = obs[cluster_key] == idx
        # cts = obs.loc[b, ref_key]
        '''
        ct_vc = cts.value_counts()
        cnt = 0
        for ct in list(ct_vc.index.values):
            if ct in ref_types:
                cnt += ct_vc[ct]
        '''
        cnt = np.sum(np.array(ref_ind)[b])
        ref_percent = cnt/np.sum(b)
        df.loc[idx, 'Ref_percent'] = ref_percent
        if (ref_percent >= refp_min):
            b_inc.append(True)
        else:
            b_inc.append(False)

    df['b_inc'] = b_inc
    b = np.array(b_inc)
    # print(df)

    ns = np.sum(b)
    # if ns == 0: refp_min *= 0.95
    if ns == 0:
        print('ERROR: no reference type clusters found.')
        obs['tumor_prob'+ suffix] = 0
        obs['tumor_dec'+ suffix] = 'NA'
        obs['tumor_cluster'+ suffix] = ''
        return None
    elif ns == 1:
        print('WARNING: Only one reference type cluster found.')
        cmeans = np.array(df.loc[b,'cmean'])
        th2 = cmeans[0]
        b2 = df['cmean'] <= th2
    else:        
        cmeans = np.array(df.loc[b,'cmean'])
        odr = cmeans.argsort()
        m = int(round(ns*(1-p_exc)))
        if m == len(odr):
            m = m-1
        if m < 0: m = 0
        # print(' ns = %i -> m = %i' % (ns, m))
        th2 = cmeans[odr[m]]
        # th2 = cmeans.max()
        b2 = df['cmean'] <= th2
        # b = b & b2
    
    ns = np.sum(~b)
    if ns > 0:
        cmeans = np.array(df.loc[~b,'cmean'])
        odr = cmeans.argsort()

        m = int(round(ns*(p_exc)))
        if m == len(odr):
            m = m-1
        # print(' ns = %i -> m = %i' % (ns, m))
        th3 = cmeans[odr[m]]
        b3 = df['cmean'] >= max(th3, th2) 
    else:
        th3 = df['cmean'].max()
        b3 = False

    # print(' th2 = %5.2f, th3 = %5.2f' % (th2, th3))
    
    # print(th2, th3)
    
    w0 = np.sum(b&b2)/(len(b)*p_exc)
    m0 = df.loc[b&b2,'cmean'].mean()
    if np.sum(b&b2) > 1:
        v0 = df.loc[b&b2,'cmean'].var()
    else:
        idx = df.index.values[b&b2][0]
        bt = obs[cluster_key] == idx
        v0 = obs.loc[bt, score_key].var()
        

    for k, idx in enumerate(idx_lst):
        if df.loc[idx, 'cmean'] <= (m0 + np.sqrt(v0)):
            b[k] = True
                    
    if np.sum((~b)&b3) > 0:
        w1 = np.sum((~b)&b3)/(len(b)*p_exc)
        m1 = df.loc[(~b)&b3,'cmean'].mean()
        if np.sum((~b)&b3) > 1:
            v1 = df.loc[(~b)&b3,'cmean'].var()
        else:
            idx = df.index.values[(~b)&b3][0]
            bt = obs[cluster_key] == idx
            v1 = obs.loc[bt, score_key].var()
    else:
        w1 = 0
        m1 = np.abs(th3 - m0)*2 + m0 # m0*10
        v1 = v0

    mxv = df['cmean'].max()
    mnv = df['cmean'].min()
    Dv = mxv - mnv
    dv = Dv/200
    n_bins = 20

    x = np.arange(mnv,mxv,dv)
    pdf0, xs0 = get_normal_pdf( x, m0, v0, 100)
    pdf1, xs1 = get_normal_pdf( x, m1, v1, 100)

    pdf0 = pdf0 #*w0
    pdf1 = pdf1 #*w1
    
    th = -1
    for k in range(len(xs0)):
        if (pdf1[k] >= pdf0[k]) & (xs0[k] > m0):
            th = xs0[k]
            break
            
    ss_div_dm = (np.sqrt(v1)+np.sqrt(v0))/(m1-m0)
    if ss_div_dm > 1:
        print('INFO: Std_sum/Mean_diff: %f > 1' % (ss_div_dm))
        print('INFO: indicating that no tumor cells might be present in this sample.' % (ss_div_dm))
        # th = m0 + np.sqrt(v0)
        
    # print('threshold: ', th )
    th = max(th, th_min)
            
    s = obs[score_key]
    tpr = get_malignancy_prob( s, [w0, m0, v0, w1, m1, v1] )
    
    obs['tumor_prob'+ suffix] = tpr
    
    dec = pd.Series(['Normal']*len(s), index = obs.index)
    '''
    b = s >= th
    dec[b] = 'Tumor'
    dec[~b] = 'Normal'
    '''
    br = np.array(ref_ind)
    bs = (s > th)
    
    #'''
    lt = th - (th - m0)*ucr # p_exc 
    ut = th + (m1 - th)*ucr #p_exc
#     b = (s > lt) & (s < ut) & (~br)
#     print(lt, ut, np.sum(~br), np.sum(b))
#     dec[b] = 'unclear'
    #'''
    
    df['dec'] = 'Normal'
    for idx in idx_lst:
        b1 = obs[cluster_key] == idx
        if df.loc[idx, 'cmean'] > ut:            
            dec[b1&(~br)] = 'Tumor'
            df.loc[idx, 'dec'] = 'Tumor'
        elif df.loc[idx, 'cmean'] < lt:
            pass
        else:
            dec[b1&(~br)] = 'unclear'
            df.loc[idx, 'dec'] = 'unclear'
            
        # obs.loc[b1&(~br), score_key] = df.loc[idx, 'cmean']
            
#             if np.sum(b1&br) == 0:
#                 dec[b1] = 'Tumor'
#             elif (np.sum(b1&br)/np.sum(b1)) >= refp_min:
#                 pass
#             else:
#                 dec[b1&bs&(~br)] = 'Tumor'

#                 # if np.sum(b1&(~br)&bs)/np.sum(b1) < 0.4:
#                 if np.sum(b1&bs&(~br)/np.sum(b1) < 0.3:
#                     pass
#                 else:
#                     # dec[b1&(~br)&bs] = 'Tumor'
#                     dec[b1&bs&(~br)] = 'Tumor'
    '''
    lt = th - (th - m0)*p_exc 
    ut = th + (m1 - th)*p_exc
    b = (s > lt) & (s < ut) & (~br)
    print(lt, ut, np.sum(~br), np.sum(b))
    dec[b] = 'unclear'
    #'''
    if ss_div_dm > 1:
        b = dec == 'Tumor'
        print('INFO: %i among %i were identified as tumor cells, which, however, might be normal cells.' \
              % (np.sum(b), len(b)))
    
    # b = (obs[ref_key].isin(ref_types)) | (s <= th)
    # dec[b] = 'Normal'    
    obs['tumor_dec'+ suffix] = dec

    tclust = dec.copy(deep = True)
    tclust[:] = None
    cnt = 1
    for c in idx_lst:
        b = obs[cluster_key] == c
        b1 = dec == 'Tumor'
        if np.sum(b&b1) > 0:
            tclust[b&b1] = 'Tumor_c%i' % cnt
            cnt += 1        
    obs['tumor_cluster'+ suffix] = tclust
    
    etime = round(time.time() - start_time) 
    # print('CNVth(%i) ' % etime, end = '', flush = True)
    
    params = {}
    params['th'] = th
    params['m0'] = m0
    params['v0'] = v0
    params['w0'] = w0
    params['m1'] = m1
    params['v1'] = v1
    params['w1'] = w1
    params['df'] = df
    
    if plot_stat:
        plot_stats( params, n_bins = 30, title = None, title_fs = 14,
                    label_fs = 12, tick_fs = 11, legend_fs = 11, 
                    legend_loc = 'upper left', bbox_to_anchor = (1, 1),
                    figsize = (4,3), log = False, alpha = 0.8 )
        
    return obs[['tumor_dec'+ suffix, 'tumor_prob'+ suffix, 'tumor_cluster'+ suffix]], params


def get_cnv_threshold( obs, cluster_sel, score_key = 'cnv_score', 
                       cluster_key = 'cnv_leiden', th_min = 0, refp_min = 0.9, 
                       p_exc = 0.1, plot_stat = True, suffix = '', Data = None ):
    
    ## obs must contain columns 'cnv_cluster', 'cnv_score'
    start_time = time.time()
    
    df = obs.groupby([cluster_key])[score_key].agg(**{'cmean':'median'})
    idx_lst = list(df.index.values)
    
    ns = 0
    # while(ns == 0):
        
    b_inc = []
    for idx in idx_lst:
        if idx in cluster_sel:
            b_inc.append(True)
        else:
            b_inc.append(False)

    df['b_inc'] = b_inc
    b = np.array(b_inc)
    # print(df)

    ns = np.sum(b)
    # if ns == 0: refp_min *= 0.95
    if ns == 0:
        print('ERROR: no reference type clusters found.')
        obs['tumor_score'+ suffix] = 0
        obs['tumor_dec'+ suffix] = 'NA'
        obs['tumor_cluster'+ suffix] = ''
        return None
    elif ns == 1:
        print('WARNING: Only one reference type cluster found.')
        cmeans = np.array(df.loc[b,'cmean'])
        th2 = cmeans[0]
        b2 = df['cmean'] <= th2
    else:        
        cmeans = np.array(df.loc[b,'cmean'])
        odr = cmeans.argsort()
        m = int(round(ns*(1-p_exc)))
        if m == len(odr):
            m = m-1
        if m < 0: m = 0
        # th2 = cmeans[odr[m]]
        th2 = cmeans.max()
        b2 = df['cmean'] <= th2
        # b = b & b2
    
    ns = np.sum(~b)
    if ns > 0:
        cmeans = np.array(df.loc[~b,'cmean'])
        odr = cmeans.argsort()

        m = int(round(ns*(p_exc)))
        if m == len(odr):
            m = m-1
        th3 = cmeans[odr[m]]
        b3 = df['cmean'] >= max(th3, th2) 
    else:
        th3 = df['cmean'].max()
        b3 = False

    
    # print(th2, th3)
    
    w0 = np.sum(b&b2)/(len(b)*p_exc)
    m0 = df.loc[b&b2,'cmean'].mean()
    if np.sum(b&b2) > 1:
        v0 = df.loc[b&b2,'cmean'].var()
    else:
        idx = df.index.values[b&b2][0]
        bt = obs[cluster_key] == idx
        v0 = obs.loc[bt, score_key].var()
        

    for k, idx in enumerate(idx_lst):
        if df.loc[idx, 'cmean'] <= (m0 + np.sqrt(v0)):
            b[k] = True
                    
    if np.sum((~b)&b3) > 0:
        w1 = np.sum((~b)&b3)/(len(b)*p_exc)
        m1 = df.loc[(~b)&b3,'cmean'].mean()
        if np.sum((~b)&b3) > 1:
            v1 = df.loc[(~b)&b3,'cmean'].var()
        else:
            idx = df.index.values[(~b)&b3][0]
            bt = obs[cluster_key] == idx
            v1 = obs.loc[bt, score_key].var()
    else:
        w1 = 0
        m1 = np.abs(th3 - m0)*2 + m0 # m0*10
        v1 = v0

    mxv = df['cmean'].max()
    mnv = df['cmean'].min()
    Dv = mxv - mnv
    dv = Dv/200
    n_bins = 30

    x = np.arange(mnv,mxv,dv)
    pdf0, xs0 = get_normal_pdf( x, m0, v0, 100)
    pdf1, xs1 = get_normal_pdf( x, m1, v1, 100)

    pdf0 = pdf0 #*w0
    pdf1 = pdf1 #*w1
    
    th = -1
    for k in range(len(xs0)):
        if (pdf1[k] >= pdf0[k]) & (xs0[k] > m0):
            th = xs0[k]
            break
            
    ss_div_dm = (np.sqrt(v1)+np.sqrt(v0))/(m1-m0)
    if ss_div_dm > 1:
        print('INFO: Std_sum/Mean_diff: %f > 1' % (ss_div_dm))
        print('INFO: indicating that no tumor cells might be present in this sample.' % (ss_div_dm))
        # th = m0 + np.sqrt(v0)
        
    # print('threshold: ', th )
    th = max(th, th_min)
            
    s = obs[score_key]
    tpr = get_malignancy_prob( s, [w0, m0, v0, w1, m1, v1] )
    
    obs['tumor_score'+ suffix] = tpr
    
    dec = pd.Series(['Normal']*len(s), index = obs.index)
    '''
    b = s >= th
    dec[b] = 'Tumor'
    dec[~b] = 'Normal'
    '''
    bs = (s > th)
    for idx in idx_lst:
        if df.loc[idx, 'cmean'] > th:
            b1 = obs[cluster_key] == idx
            dec[b1] = 'Tumor'
            
    '''
    lt = th - (th - m0)*0.05 
    ut = th + (m1 - th)*0.05
    b = (s > lt) & (s < ut) & (~br)
    print(lt, ut, np.sum(~br), np.sum(b))
    dec[b] = 'unclear'
    '''
    if ss_div_dm > 1:
        b = dec == 'Tumor'
        print('INFO: %i among %i were identified as tumor cells, which, however, might be normal cells.' \
              % (np.sum(b), len(b)))
    
    # b = (obs[ref_key].isin(ref_types)) | (s <= th)
    # dec[b] = 'Normal'    
    obs['tumor_dec'+ suffix] = dec

    tclust = dec.copy(deep = True)
    tclust[:] = None
    cnt = 1
    for c in idx_lst:
        b = obs[cluster_key] == c
        b1 = dec == 'Tumor'
        if np.sum(b&b1) > 0:
            tclust[b&b1] = 'Tumor_c%i' % cnt
            cnt += 1        
    obs['tumor_cluster'+ suffix] = tclust
    
    etime = round(time.time() - start_time) 
    # print('CNVth(%i) ' % etime, end = '', flush = True)
    
    params = {}
    params['th'] = th
    params['m0'] = m0
    params['v0'] = v0
    params['w0'] = w0
    params['m1'] = m1
    params['v1'] = v1
    params['w1'] = w1
    params['df'] = df
    
    if plot_stat:
        plot_stats( params, n_bins = 30, title = None, title_fs = 14,
                    label_fs = 12, tick_fs = 11, legend_fs = 11, 
                    legend_loc = 'upper left', bbox_to_anchor = (1, 1),
                    figsize = (4,3), log = False, alpha = 0.8 )

    return obs[['tumor_dec'+ suffix, 'tumor_score'+ suffix, 'tumor_cluster'+ suffix]], params


def plot_stats( params, n_bins = 30, title = None, title_fs = 14,
                label_fs = 12, tick_fs = 11, legend_fs = 11, 
                legend_loc = 'upper left', bbox_to_anchor = (1, 1),
                figsize = (4,3), log = True, alpha = 0.8 ):
    
    th = params['th']
    m0 = params['m0']
    v0 = params['v0']
    w0 = params['w0']
    m1 = params['m1']
    v1 = params['v1']
    w1 = params['w1']
    df = params['df']
        
    mxv = df['cmean'].max()
    mnv = df['cmean'].min()
    Dv = mxv - mnv
    dv = Dv/200

    x = np.arange(mnv,mxv,dv)
    pdf0, xs0 = get_normal_pdf( x, m0, v0, 100)
    pdf1, xs1 = get_normal_pdf( x, m1, v1, 100)
    
    pr = pdf1/(pdf1 + pdf0) # get_malignancy_prob( xs0, [w0, m0, v0, w1, m1, v1] )
    bx = (xs0 >= m0) & ((xs1 <= m1))

    nn = len(df['cmean'])
    pdf0 = pdf0*(w0*nn*(200/n_bins)/pdf0.sum())
    pdf1 = pdf1*(w1*nn*(200/n_bins)/(pdf1.sum())) 

    max_pdf = max(pdf0.max(), pdf1.max())
    
    plt.figure(figsize = figsize)
    ax = plt.gca()
    
    counts, bins = np.histogram(df['cmean'], bins = n_bins)
    # max_cnt = np.max(counts)

    legend_labels = []
    
    max_cnt = 0
    b = df['dec'] == 'Normal'
    if np.sum(b) > 0:
        legend_labels.append('Normal')
        counts, bins_t, bar_t = plt.hist(df.loc[b, 'cmean'], bins = bins, alpha = alpha)
        max_cnt = max(max_cnt, np.max(counts))
    b = df['dec'] == 'Tumor'
    if np.sum(b) > 0:
        legend_labels.append('Tumor')
        counts, bins_t, bar_t = plt.hist(df.loc[b, 'cmean'], bins = bins, alpha = alpha)
        max_cnt = max(max_cnt, np.max(counts))
    b = df['dec'] == 'unclear'
    if np.sum(b) > 0:
        legend_labels.append('unclear')
        counts, bins_t, bar_t = plt.hist(df.loc[b, 'cmean'], bins = bins, alpha = alpha)
        max_cnt = max(max_cnt, np.max(counts))
    
    sf = 0.9*max_cnt/max_pdf
    plt.plot(xs0, pdf0*sf)
    plt.plot(xs1, pdf1*sf)
    plt.plot([th, th], [0, max_cnt]) # max(pdf0.max()*sf, pdf1.max()*sf)])
    plt.plot(xs0[bx], pr[bx]*max_cnt)

    if title is not None: plt.title(title, fontsize = title_fs)
    plt.xlabel('CNV_score', fontsize = label_fs)
    plt.ylabel('Number of clusters', fontsize = label_fs)
    plt.legend(['Normal distr.', 'Tumor distr.', 'Threshold', 'Tumor Prob.'], #, 'Score hist.'], 
               loc = legend_loc, bbox_to_anchor = bbox_to_anchor, fontsize = legend_fs)
    if log: plt.yscale('log')
    ax.tick_params(axis='x', labelsize=tick_fs)
    ax.tick_params(axis='y', labelsize=tick_fs)
    plt.grid()
    plt.show()
        
    return 
    

def get_cnv_dec(adata, ref_key, ref_types, cluster_key = 'cnv_leiden', 
                       score_key = 'cnv_score', th_min = 0, use_ref = True, suffix = ''):
    
    if use_ref:
        df = get_cnv_threshold_useref( adata.obs, ref_key, ref_types, 
                                       score_key = score_key, cluster_key = cluster_key, th_min = th_min,
                                       plot_stat = True, suffix = suffix )
    else:
        df = get_cnv_threshold_bimodal( adata.obs, ref_key, ref_types, score_key = score_key, 
                                        cluster_key = cluster_key, th_min = th_min, 
                                        plot_stat = True, suffix = suffix )
    
    return adata.obs[[cluster_key, score_key, 'tumor_dec'+suffix, 'tumor_score'+suffix]]


def detect_communities(X_pca, y_clust, cobj, pmaj = 0.7, 
                             cutoff = 0.01, verbose = False ):
    
    adj_agg = cobj.aggregate_
    adj_agg_mat = adj_agg.todense().astype(int) 
    labels_unique, counts = np.unique(y_clust, return_counts=True)

    ## Get neighbor clusters
    # cutoff = 0.01
    aj = {}
    for j in range(len(labels_unique)):
        a = []
        b = []
        for k in range(len(labels_unique)):
            if (adj_agg_mat[j,k] >= adj_agg_mat[j,j]*cutoff) & (adj_agg_mat[j,k] >= adj_agg_mat[k,k]*cutoff):
                a.append(k)
                b.append(adj_agg_mat[j,k])
        if len(a) > 0:
            odr = (-np.array(b)).argsort()
            a1 = []
            b1 = []
            bn = []
            for o in odr:
                a1.append(a[o])
                b1.append(b[o])
                nv = int(10*np.log10(b[o]/adj_agg_mat[j,j] + 1e-10))
                bn.append(nv)
            d = dict(zip(a1,bn))
            bn.sort(reverse = True)
            aj[j] = d

    ## Get community list
    communities = []
    for key in aj.keys():
        d = aj[key]
        nodes = list(d.keys())
        if len(nodes) > 1:
            common = nodes
            for n in nodes:
                common = list(set(common).intersection(list(aj[n].keys())))
            if len(common) > 1:
                communities.append(common)
                # print(key, ': ', common)

    to_del = []
    for k, c in enumerate(communities):
        b = False
        for k2, c2 in enumerate(communities):
            if (k2 != k) & (k not in to_del) & (k2 not in to_del):
                if (len(list(set(c) - set(c2))) == 0):
                    to_del.append(k)

    for k in reversed(to_del):
        del communities[k]
    
    return communities


def merge_communities( communities ):
    
    cm = copy.deepcopy(communities)
    to_del = []
    for j in reversed(range(len(cm))):
        if j > 0:
            for k in range(j):
                c = list(set(cm[k]).intersection(cm[j]))
                if len(c) > 0:
                    cm[k] = list(set(cm[k]).union(cm[j]))
                    to_del.append(j)
                    break
                    
    for j in to_del:
        del cm[j]
        
    ss = []
    for j, c in enumerate(cm):
        c.sort()
        cm[j] = c
        ss.append(-len(c))
    
    ss = np.array(ss)
    odr = ss.argsort()
    
    return cm[odr[0]]


def compute_cnv_scores(adata, ref_ind, use_cnv_score = False,
                       cluster_key = 'cnv_leiden', score_key = 'tumor_score', 
                       gmm_N_comp = 20, th_min = 0, refp_min = 0.9, p_exc = 0.1, 
                       dec_margin = 0.05, clustering_res = 4, n_neighbors = 10, gcm = 0.05,
                       plot_stat = False, use_cnv_cluster = True, use_ref = True, suffix = '', Data = None):
    
    score_key = score_key + suffix
    ## Get X_pca for ref_type cells

    X_pca = adata.obsm['X_cnv_pca']
    
    start_time = time.time()
    print('Running iCNV addon .. ', end = '', flush = True)
    
    if use_cnv_cluster:      
        y_clust = adata.obs[cluster_key].copy(deep = True)
        cnv_clust_lst = list(set(y_clust))
    else:
        # y_clust, cobj = clustering_alg(X_pca, clust_algo = 'lv', 
        #                                resolution = clustering_res, N_neighbors = n_neighbors)         
        adj = kneighbors_graph(X_pca, int(n_neighbors), mode='connectivity', include_self=True)
        etime = round(time.time() - start_time) 
        print('N(%i).' % etime, end = '', flush = True)
            
        cobj = Louvain(resolution = clustering_res)
        y_clust = cobj.fit_transform(adj)        
        
        adata.obs[cluster_key] = y_clust
        adata.obs[cluster_key] = adata.obs[cluster_key].astype(str)
        y_clust = pd.Series(y_clust, index = adata.obs.index)
        cnv_clust_lst = list(set(y_clust))
        
    if use_cnv_score:
        adata.obs[score_key] = adata.obs['cnv_score']
    else:
        if use_ref:
            cnv_clust_lst.sort()
            b_inc = []
            for idx in cnv_clust_lst:
                b = y_clust == idx
                bt = ref_ind
                cnt = np.sum(b&bt)

                if (cnt >= refp_min*np.sum(b)):
                    b_inc.append(True)
                else:
                    b_inc.append(False)

            if np.sum(b_inc) > 0:
                cluster_sel = list(np.array(cnv_clust_lst)[b_inc]) 
                b = y_clust == cluster_sel[0]
                for c in cluster_sel[1:]:
                    b = b | (y_clust == c)
            else:
                print('ERROR: No reference cell types found.')
                adata.obs[score_key] = 0
                adata.obs['tumor_prob'+ suffix] = 0
                adata.obs['tumor_dec'+ suffix] = 'NA'
                adata.obs['tumor_cluster'+ suffix] = ''
                return adata.obs[[cluster_key, score_key, 'tumor_dec'+suffix, 
                          'tumor_prob'+suffix, 'tumor_cluster'+ suffix]]
            X_pca_sel = X_pca[b,:]
        else:
            X_pca_sel = X_pca


        etime = round(time.time() - start_time) 
        # print('C(%i).' % etime, end = '', flush = True)

        ## Get GMM model parameters
        gmm = mixture.GaussianMixture(n_components = int(gmm_N_comp), random_state = 0)
        gmm.fit(X_pca_sel)
        y_conf_gmm = -gmm.score_samples(X_pca)
        #'''
        X_cnv = pd.DataFrame(adata.obsm['X_cnv'].todense(), index = adata.obs.index.values)
        y_conf = np.sqrt((X_cnv**2).mean(axis = 1))*100  

        yc = np.array(y_conf)
        odr = yc.argsort()
        n = int(len(yc)*0.975)
        ymax = yc[odr[n]]
        b = y_conf > ymax
        y_conf[b] = ymax

        adata.obs[score_key] = y_conf*(1/(1+np.exp(-y_conf_gmm*gcm)))

        etime = round(time.time() - start_time) 
        print('G(%i)' % etime, end = '', flush = True)
    
    ## Replace GMM scores with their cluster mean
    '''
    cnv_clust_lst = list(set(adata.obs[cluster_key]))
    for c in cnv_clust_lst:
        b = adata.obs[cluster_key] == c
        adata.obs.loc[b, score_key] = adata.obs.loc[b, score_key].mean()
    '''
    if use_ref:
        df, params = get_cnv_threshold_useref( adata.obs, ref_ind, 
                                       score_key = score_key, cluster_key = cluster_key,
                                       th_min = th_min, refp_min = refp_min, p_exc = p_exc, ucr = dec_margin,
                                       plot_stat = plot_stat, suffix = suffix, Data = Data )
    else:
        df, params = get_cnv_threshold_bimodal( adata.obs, ref_ind, 
                                        score_key = score_key, cluster_key = cluster_key, 
                                        th_min = th_min, refp_min = refp_min, ucr = dec_margin,
                                        plot_stat = plot_stat, suffix = suffix, Data = Data )
    
    etime = round(time.time() - start_time) 
    print(' .. done (%i) ' % etime) #, end = '', flush = True)
    
    return adata.obs[[cluster_key, score_key, 'tumor_dec'+suffix, 
                      'tumor_prob'+suffix, 'tumor_cluster'+ suffix]], params


import warnings

def run_icnv(adata, ref_key, ref_types, gtf_file, cluster_key = 'cnv_leiden', 
             resolution = 2, N_pca = 15, n_neighbors = 10, pca_umap = True, n_cores = 4 ):
    
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
    
        ## Normalize and log-transform
        sc.pp.normalize_total(adata, target_sum=1e4)
        sc.pp.log1p(adata)

        sc.pp.highly_variable_genes(adata, n_top_genes = 2000) # , flavor = 'seurat_v3')
        # sc.tl.score_genes_cell_cycle(adata, cell_cycle_genes_s, cell_cycle_genes_g2m)

        cnv.io.genomic_position_from_gtf(gtf_file, adata, gtf_gene_id='gene_name', adata_gene_id=None, inplace=True)
        cnv.tl.infercnv(adata, reference_key = ref_key, reference_cat=ref_types, 
                        window_size=100, n_jobs = n_cores)

        if pca_umap:
            print('PCA .. ', end = '')
            cnv.tl.pca(adata, svd_solver='arpack', n_comps = N_pca) 
            print('Finding neighbors .. ', end = '')
            cnv.pp.neighbors(adata, key_added = 'cnv_neighbors', n_neighbors=n_neighbors, n_pcs=N_pca)
            print('Clustering .. ', end = '')
            cnv.tl.leiden(adata, neighbors_key='cnv_neighbors', key_added=cluster_key, resolution = resolution)
            print('UMAP .. ', end = '')
            cnv.tl.umap(adata)
            
        print('Scoring .. ', end = '')
        cnv.tl.cnv_score(adata, groupby = cluster_key, key_added = 'cnv_score')
        print('done.')

    return adata



from sklearn.decomposition import PCA
from sklearn import cluster, mixture
from sklearn.neighbors import KNeighborsRegressor
from sklearn.neighbors import kneighbors_graph
from sklearn.neighbors import NearestNeighbors

CLUSTERING_AGO = 'lv'
SKNETWORK = True
try:
    from sknetwork.clustering import Louvain
except ImportError:
    print('WARNING: sknetwork not installed. Will used GMM for clustering.')
    CLUSTERING_AGO = 'gmm'
    SKNETWORK = False

from sklearn.decomposition import PCA
from sklearn import cluster, mixture
from sklearn.neighbors import KNeighborsRegressor
from sklearn.neighbors import kneighbors_graph
from sklearn.neighbors import NearestNeighbors

CLUSTERING_AGO = 'lv'
SKNETWORK = True
try:
    from sknetwork.clustering import Louvain
except ImportError:
    print('WARNING: sknetwork not installed. Will used GMM for clustering.')
    CLUSTERING_AGO = 'gmm'
    SKNETWORK = False

    
def clustering_alg(X_pca, clust_algo = 'lv', N_clusters = 25, resolution = 1, N_neighbors = 10):
    
    if clust_algo[:2] == 'gm':
        gmm = mixture.GaussianMixture(n_components = int(N_clusters), random_state = 0)
        cluster_label = gmm.fit_predict(np.array(X_pca))
        return cluster_label, gmm
    elif clust_algo[:2] == 'km':
        km = cluster.KMeans(n_clusters = int(N_clusters), random_state = 0)
        km.fit(X_pca)
        cluster_label = km.labels_
        return cluster_label, km
    else:
        adj = kneighbors_graph(X_pca, int(N_neighbors), mode='connectivity', include_self=True)
        louvain = Louvain(resolution = resolution)
        if hasattr(louvain, 'fit_predict'):
            cluster_label = louvain.fit_predict(adj)        
        else:
            cluster_label = louvain.fit_transform(adj)        
        return cluster_label, louvain
    '''
    elif clust_algo[:2] == 'ld':
        leiden = LeidenClustering()
        leiden.fit(X)
        cluster_label = leiden.labels_
        return cluster_label, km
    '''

def detect_tumor_cells(X_cnv, ref_ind, pca = False, use_cnv_score = False, 
                       clust = None, Clustering_resolution = 1, N_clusters = 30,
                       # cluster_key = 'cnv_leiden', score_key = 'tumor_score', 
                       gmm_N_comp = 20, th_min = 0, refp_min = 0.9, p_exc = 0.1, 
                       dec_margin = 0.05, n_neighbors = 10, gcm = 0.05,
                       plot_stat = False, use_ref = True, 
                       suffix = '', Data = None):
    
    score_key = 'tumor_score' + suffix
    cluster_key = 'cnv_cluster' 
    ## Get X_pca for ref_type cells

    start_time = time.time()
    print('Running iCNV addon .. ', end = '', flush = True)
    
    if isinstance(X_cnv, pd.DataFrame):
        df = pd.DataFrame(index = X_cnv.index.values)
    else:
        df = pd.DataFrame()
        X_cnv = pd.DataFrame(X_cnv)
    
    N_components_pca = 15
    pca_obj = PCA(n_components = int(N_components_pca), copy = True, random_state = 0)

    if not pca: 
        X_pca = pca_obj.fit_transform(X_cnv)
    else: 
        X_pca = np.array(X_cnv.copy(deep = True)) #.copy(deep = True)
            
    if clust:      
        y_clust = list(clust)
    else:
        y_clust, cobj = clustering_alg(X_pca, clust_algo = CLUSTERING_AGO, N_clusters = N_clusters, 
                                resolution = Clustering_resolution, N_neighbors = n_neighbors)
        
    cnv_clust_lst = list(set(y_clust))
    df[cluster_key] = y_clust
        
    if use_ref:
        cnv_clust_lst.sort()
        b_inc = []
        for idx in cnv_clust_lst:
            b = y_clust == idx
            bt = b & ref_ind
            cnt = np.sum(bt)

            if (cnt >= refp_min*np.sum(b)):
                b_inc.append(True)
            else:
                b_inc.append(False)

        if np.sum(b_inc) > 0:
            cluster_sel = list(np.array(cnv_clust_lst)[b_inc]) 
            b = y_clust == cluster_sel[0]
            for c in cluster_sel[1:]:
                b = b | (y_clust == c)
        else:
            print('ERROR: No reference cell types found.')
            df[score_key] = 0
            df['tumor_prob'+ suffix] = 0
            df['tumor_dec'+ suffix] = 'NA'
            df['tumor_cluster'+ suffix] = ''
            return df[[cluster_key, score_key, 'tumor_dec'+suffix, 
                      'tumor_prob'+suffix, 'tumor_cluster'+ suffix]]
        X_pca_sel = X_pca[b,:]
    else:
        X_pca_sel = X_pca


    etime = round(time.time() - start_time) 
    # print('C(%i).' % etime, end = '', flush = True)

    ## Get GMM model parameters
    gmm = mixture.GaussianMixture(n_components = int(gmm_N_comp), random_state = 0)
    gmm.fit(X_pca_sel)
    y_conf_gmm = -gmm.score_samples(X_pca)
    #'''
    y_conf = np.sqrt((X_cnv**2).mean(axis = 1))*100  

    yc = np.array(y_conf)
    odr = yc.argsort()
    n = int(len(yc)*0.975)
    ymax = yc[odr[n]]
    b = y_conf > ymax
    y_conf[b] = ymax

    df[score_key] = y_conf*(1/(1+np.exp(-y_conf_gmm*gcm)))

    etime = round(time.time() - start_time) 
    print('G(%i)' % etime, end = '', flush = True)
    
    ## Replace GMM scores with their cluster mean
    if ref_ind is not None:
        dft, params = get_cnv_threshold_useref( df, ref_ind, 
                                       score_key = score_key, cluster_key = cluster_key,
                                       th_min = th_min, refp_min = refp_min, p_exc = p_exc, ucr = dec_margin,
                                       plot_stat = plot_stat, suffix = suffix, Data = Data )
    else:
        dft, params = get_cnv_threshold_bimodal( df, ref_ind, 
                                        score_key = score_key, cluster_key = cluster_key, 
                                        th_min = th_min, refp_min = refp_min, ucr = dec_margin,
                                        plot_stat = plot_stat, suffix = suffix, Data = Data )
    
    etime = round(time.time() - start_time) 
    print(' .. done (%i) ' % etime) #, end = '', flush = True)
    
    return df, params

