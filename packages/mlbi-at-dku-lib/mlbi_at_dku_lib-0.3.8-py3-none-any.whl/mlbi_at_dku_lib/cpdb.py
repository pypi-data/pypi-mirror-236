import copy, os, time, warnings, math
import numpy as np
import pandas as pd
import scanpy as sc
from matplotlib.pyplot import figure
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib
from subprocess import Popen, PIPE
import shlex, anndata

def run_command(cmd, verbose = True):
    cnt = 0
    with Popen(shlex.split(cmd), stdout=PIPE, bufsize=1, \
               universal_newlines=True ) as p:
        for line in p.stdout:
            if (line[:14] == 'Tool returned:'):                    
                cnt += 1
            elif cnt > 0:
                pass
            else: 
                if verbose:
                    print(line, end='')
                    
        exit_code = p.poll()
    return exit_code


def cpdb_run( df_cell_by_gene, cell_types, out_dir,
              gene_id_type = 'gene_name', db = None, 
              n_iter = None, pval_th = None, threshold = None):
    
    start = time.time()
    print('Running CellPhoneDB .. ')    
    X = df_cell_by_gene.astype(int) 
    ## X = (X.div(X.sum(axis = 1), axis=0)*1e6).astype(int)
    
    if out_dir[-1] == '/':
        out_dir = out_dir[:-1]
    
    if not os.path.isdir(out_dir):
        os.mkdir(out_dir)
        
    file_meta = '%s/meta_tmp.tsv' % out_dir
    file_cpm = '%s/exp_mat_tmp.tsv' % out_dir
    
    X.transpose().to_csv(file_cpm, sep = '\t')
    df_celltype = pd.DataFrame({'cell_type': cell_types}, 
                               index = X.index.values)    
    df_celltype.to_csv(file_meta, sep = '\t')
    
    cmd = 'cellphonedb method statistical_analysis '
    cmd = cmd + '%s %s ' % (file_meta, file_cpm)
    cmd = cmd + '--counts-data=%s ' % gene_id_type
    if pval_th is not None: cmd = cmd + '--pvalue=%f ' % pval_th
    if threshold is not None: cmd = cmd + '--threshold=%f ' % threshold
    if n_iter is not None: cmd = cmd + '--iterations=%i ' % n_iter
    if db is not None: '--database %s ' % db
    cmd = cmd + '--output-path %s ' % out_dir

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        run_command(cmd) 
    
    elapsed = time.time() - start
    print('Running CellPhoneDB .. done. %i' % elapsed )    
    
    if os.path.exists(file_cpm):
        os.remove(file_cpm)
    if os.path.exists(file_meta):
        os.remove(file_meta)
    
    return cmd
    
    
def split_cellphonedb_out(df):
    cols = df.columns.values
    items = cols[:10]
    pairs = cols[10:]
    df_items = df[items]
    df_pairs = df[pairs]    
    return df_items, df_pairs    
    
def cpdb_get_res( out_dir ):
    
    ## Load p_values
    df_pval = pd.read_csv('%s/pvalues.txt' % out_dir, sep = '\t', 
                          index_col = 0)    
    df_pval_items, df_pval_pairs = split_cellphonedb_out(df_pval)
    
    ## Load means
    df_mean = pd.read_csv('%s/means.txt' % out_dir, sep = '\t', 
                          index_col = 0)    
    df_mean_items, df_mean_pairs = split_cellphonedb_out(df_mean)
    
    ## Check integrity
    idxp = list(df_pval_items.index.values)
    idxm = list(df_mean_items.index.values)
    idxc = set(idxp).intersection(idxm)
    cnt = 0
    for p, m in zip(idxp, idxm):
        if p != m:
            cnt += 1
    if cnt > 0:
        print( len(idxc), len(df_pval_items.index.values), 
               len(df_mean_items.index.values), cnt )
    
    return df_mean_items, df_mean_pairs, df_pval_items, df_pval_pairs   


def to_vector(df, rows, cname):    
    cols = df.columns.values
    idxs, gps, cps, vals = [], [], [], []
    ga, gb, ca, cb = [], [], [], []
    
    for c in list(cols):
        vt = list(df[c])
        ct = [c]*len(vt)
        gt = list(rows)
        it = []
        for r in gt:
            idx = '%s--%s' % (r,c)
            it.append(idx)            
        idxs = idxs + it
        gps = gps + gt
        cps = cps + ct
        vals = vals + vt
        ga = ga + [g.split('_')[0] for g in gt]
        gb = gb + [g.split('_')[1] for g in gt]
        ca = ca + [g.split('|')[0] for g in ct]
        cb = cb + [g.split('|')[1] for g in ct]
        
    dfo = pd.DataFrame({'gene_pair': gps, 'cell_pair': cps, 
                        'gene_A': ga, 'gene_B': gb,
                        'cell_A': ca, 'cell_B': cb,
                         cname: vals}, index = idxs)    
    return dfo

def cpdb_get_vec( df_info, df_mean_pairs, df_pval_pairs, 
                  pval_max = 0.05, mean_min = 0.01 ):    
    dfp = to_vector(df_pval_pairs, 
                    df_info['interacting_pair'], 'pval')
    dfm = to_vector(df_mean_pairs, 
                    df_info['interacting_pair'], 'mean')
    b = (dfp['pval'] <= pval_max) & (dfm['mean'] >= mean_min) 
    b = b & (~dfp['pval'].isnull()) & (~dfm['mean'].isnull())
    dfp = dfp.loc[b,:].copy(deep=True)
    dfm = dfm.loc[b,:].copy(deep=True)   
    dfp['mean'] = dfm['mean']    
    return dfp    


def cpdb_get_results( out_dir, pval_max = 0.05, mean_min = 0.01 ):
    df_mean_info, df_mean_pairs, df_pval_info, df_pval_pairs = \
          cpdb_get_res( out_dir )
    dfv = cpdb_get_vec( df_pval_info, df_mean_pairs, df_pval_pairs, 
                        pval_max = pval_max, mean_min = mean_min )
    return df_pval_info, df_pval_pairs, df_mean_pairs, dfv

###################################
### Plot functions for CellPhoneDB

def cpdb_plot( dfp, mkr_sz = 6, tick_sz = 6, 
                             legend_fs = 11, title_fs = 14,
                             dpi = 120, title = None, swap_ax = False ):
    if swap_ax == False:
        a = 'gene_pair'
        b = 'cell_pair'
    else:
        b = 'gene_pair'
        a = 'cell_pair'
    
    y = len(set(dfp[a]))
    x = len(set(dfp[b]))
    
    print('%i %ss, %i %ss found' % (y, a, x, b))
    
    pv = -np.log10(dfp['pval']+1e-10).round()
    np.min(pv), np.max(pv)
    
    mn = np.log2((1+dfp['mean']))
    np.min(mn), np.max(mn)    
    
    w = x/6
    sc.settings.set_figure_params(figsize=(w, w*(y/x)), 
                                  dpi=dpi, facecolor='white')
    fig, ax = plt.subplots()

    mul = mkr_sz
    scatter = ax.scatter(dfp[b], dfp[a], s = pv*mul, c = mn, 
                         linewidth = 0, cmap = 'Reds')

    legend1 = ax.legend(*scatter.legend_elements(),
                        loc='upper left', 
                        bbox_to_anchor=(1+1/x, 0.5), 
                        title=' log2(m) ', 
                        fontsize = legend_fs)
    legend1.get_title().set_fontsize(legend_fs)
    ax.add_artist(legend1)

    # produce a legend with a cross section of sizes from the scatter
    handles, labels = scatter.legend_elements(prop='sizes', alpha=0.6)
    # print(labels)
    labels = [1, 2, 3, 4, 5]
    legend2 = ax.legend(handles, labels, loc='lower left', 
                        bbox_to_anchor=(1+1/x, 0.5), 
                        title='-log10(p)', 
                        fontsize = legend_fs)
    legend2.get_title().set_fontsize(legend_fs)

    if title is not None: plt.title(title, fontsize = title_fs)
    plt.yticks(fontsize = tick_sz)
    plt.xticks(rotation = 90, ha='center', fontsize = tick_sz)
    plt.margins(x=0.6/x, y=0.6/y)
    plt.show()   
    return 

def cpdb_get_gp_n_cp(idx):
    
    items = idx.split('--')
    gpt = items[0]
    cpt = items[1]
    gns = gpt.split('_')
    ga = gns[0]
    gb = gns[1]
    cts = cpt.split('|')
    ca = cts[0]
    cb = cts[1]
    
    return gpt, cpt, ga, gb, ca, cb
    
    
def cpdb_add_interaction( file_i, file_c = None, 
                          file_p = None, file_g = None, 
                          out_dir = 'cpdb_out'):
        
    if file_i is None:
        print('ERROR: provide file containing interaction info.')
        return None
    if not os.path.exists(file_i):
        print('ERROR: %s not found' % file_i)
    
    if file_c is not None:
        if not os.path.exists(file_c):
            print('ERROR: %s not found' % file_c)
            return None
    
    if file_p is not None:
        if not os.path.exists(file_p):
            print('ERROR: %s not found' % file_p)
            return None

    if file_g is not None:
        if not os.path.exists(file_g):
            print('ERROR: %s not found' % file_g)
            return None
    
    cmd = 'cellphonedb database generate '
    cmd = cmd + '--user-interactions %s ' % file_i
    if file_c is not None: cmd = cmd + '--user-complex %s ' % file_c
    if file_p is not None: cmd = cmd + '--user-protein %s ' % file_p
    if file_g is not None: cmd = cmd + '--user-gene %s ' % file_g
    cmd = cmd + '--result-path %s ' % out_dir

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        run_command(cmd) 
        pass
    
    print('Updated DB files saved to %s' % out_dir )    
    return out_dir


def center(p1, p2):
    return (p1[0]+p2[0])/2, (p1[1]+p2[1])/2

def norm( p ):
    n = np.sqrt(p[0]**2 + p[1]**2)
    return n

def vrot( p, s ):
    v = (np.array([[0, -1], [1, 0]]).dot(np.array(p)))
    v = ( v/norm(v) )
    return v #, v2
    
def vrot2( p, t ):
    v = (np.array([[np.cos(t), -np.sin(t)], [np.sin(t), np.cos(t)]]).dot(p))
    return v #, v2
    
def get_arc_pnts( cp, R, t1, t2, N):
    
    a = (t1 - t2)
    if a >= math.pi:
        t2 = t2 + 2*math.pi
    elif a <= -math.pi:
        t1 = t1 + 2*math.pi
    
    N1 = (N*np.abs(t1 - t2)/(2*math.pi))
    # print(N1)
    s = np.sign(t1 - t2)
    t = t2 + np.arange(N1+1)*(s*2*math.pi/N)
    # if t.max() > (math.pi*2): t = t - math.pi*2
    
    x = np.sin(t)*R + cp[0]
    y = np.cos(t)*R + cp[1]
    x[-1] = np.sin(t1)*R + cp[0]
    y[-1] = np.cos(t1)*R + cp[1]
        
    return x, y, a

def get_arc( p1, p2, R, N ):
    
    A = norm(p1 - p2)
    pc = center(p1, p2)
    
    a = np.sqrt((R*A)**2 - norm(p1 - pc)**2)
    c = pc + vrot(p1 - pc, +1)*a

    d1 = p1 - c
    t1 = np.arctan2(d1[0], d1[1])
    d2 = p2 - c
    t2 = np.arctan2(d2[0], d2[1])

    x, y, t1 = get_arc_pnts( c, R*A, t2, t1, N)
    
    return x, y, c


def get_circ( p1, R, N ):
    
    pp = np.arange(N)*(2*math.pi/N)
    px = np.sin(pp)*0.5
    py = np.cos(pp)
    pnts = np.array([px, py])
    
    t = -np.arctan2(p1[0], p1[1])
    pnts = vrot2( pnts, t+math.pi )*R
    pnts[0,:] = pnts[0,:] + p1[0]*(1+R)
    pnts[1,:] = pnts[1,:] + p1[1]*(1+R)
    x = pnts[0,:]
    y = pnts[1,:]
    c = np.array([0,0])
    
    return x, y, c


def plot_circ( df_in, figsize = (10, 10), title = None, title_fs = 16, 
               text_fs = 14, num_fs = 12, margin = 0.12, alpha = 0.5, 
               N = 500, R = 4, Rs = 0.1, lw_max = 10, lw_scale = 0.1, 
               log_lw = False, node_size = 10, rot = True, 
               cmap = 'Spectral', ax = None, show = True):
              
    df = df_in.copy(deep = True)
    mxv = df_in.max().max()
    
    if ax is None: 
        plt.figure(figsize = figsize)
        ax = plt.gca()
        
    color_map = matplotlib.colormaps[cmap]
    color_lst = [color_map(i/(df.shape[0]-1)) for i in range(df.shape[0])]

    clst = list(df.index.values) 

    M = df.shape[0]
    pp = np.arange(M)*(2*math.pi/M)
    px = np.sin(pp)
    py = np.cos(pp)
    pnts = np.array([px, py])
    
    for j in range(pnts.shape[1]):
        p1 = pnts[:,j]
        for k in range(pnts.shape[1]):
            p2 = pnts[:,k]
            
            val = df.loc[clst[j], clst[k]]
            if lw_scale > 0:
                lw = val*lw_scale
            elif lw_max > 0:
                lw = val*lw_max/mxv
            else:
                lw = val
            if log_lw: lw = np.log2(lw)                    
                    
            if (df.loc[clst[j], clst[k]] != 0): # & (j!= k):

                if j == k:
                    x, y, c = get_circ( p1, 0.1, N )
                    K = int(len(x)*0.5)
                    d = vrot(p1, 1)
                    d = d*0.05/norm(d)
                elif (j != k) :
                    x, y, c = get_arc( p1, p2, R, N )

                    K = int(len(x)*0.5)
                    d = (p2 - p1)
                    d = d*0.05/norm(d)

                q2 = np.array([x[K], y[K]])
                q1 = np.array([x[K] - d[0], y[K] - d[1]])

                s = norm(q1 - q2)
                
                ha = 'center'
                if c[0] < -1:
                    ha = 'left'
                elif c[0] > 1:
                    ha = 'right'
                    
                va = 'center'
                if c[1] < -1:
                    va = 'bottom'
                elif c[1] > 1:
                    va = 'top'
                    
                if norm(q2) <= 0.7: # mnR*2:
                    ha = 'center'
                    va = 'center'
                    
                if ax is None: 
                    plt.plot(x, y, c = color_lst[j], linewidth = lw, alpha = alpha)
                    if j != k:
                        plt.arrow(q1[0], q1[1], q2[0]-q1[0], q2[1]-q1[1], linewidth = lw,
                              head_width=s/2, head_length=s, 
                              fc=color_lst[j], ec=color_lst[j])
                    plt.text( q2[0], q2[1], ' %i ' % val, fontsize = num_fs, 
                              va = va, ha = ha)
                else:
                    ax.plot(x, y, c = color_lst[j], linewidth = lw, alpha = alpha)
                    if j != k:
                        ax.arrow(q1[0], q1[1], q2[0]-q1[0], q2[1]-q1[1], linewidth = lw,
                              head_width=0.05*lw/lw_max, head_length=s, alpha = alpha, 
                              fc=color_lst[j], ec=color_lst[j])
                    ax.text( q2[0], q2[1], '%i' % val, fontsize = num_fs, 
                             va = va, ha = ha)

            elif (df.loc[clst[j], clst[k]] != 0) & (j== k):
                x, y, c = get_circ( p1, Rs, N )
                K = int(len(x)*0.5)
                d = vrot(p1, 1)
                d = d*0.05/norm(d)

                q2 = np.array([x[K], y[K]])
                q1 = np.array([x[K] - d[0], y[K] - d[1]])

                s = norm(q1 - q2)
                
                ha = 'center'
                if c[0] < -1:
                    ha = 'left'
                elif c[0] > 1:
                    ha = 'right'
                    
                va = 'center'
                if c[1] < -1:
                    va = 'bottom'
                elif c[1] > 1:
                    va = 'top'
                    
                if norm(q2) <= 0.7: # mnR*2:
                    ha = 'center'
                    va = 'center'
                    
                if ax is None: 
                    plt.plot(x, y, c = color_lst[j], linewidth = lw, alpha = alpha)
                    plt.arrow(q1[0], q1[1], q2[0]-q1[0], q2[1]-q1[1], linewidth = lw,
                              head_width=s/2, head_length=s, 
                              fc=color_lst[j], ec=color_lst[j])
                    plt.text( q2[0], q2[1], ' %i ' % val, fontsize = num_fs, 
                              va = va, ha = ha)
                else:
                    ax.plot(x, y, c = color_lst[j], linewidth = lw, alpha = alpha)
                    ax.arrow(q1[0], q1[1], q2[0]-q1[0], q2[1]-q1[1], linewidth = lw,
                              head_width=0.05*lw/lw_max, head_length=s, alpha = alpha, 
                              fc=color_lst[j], ec=color_lst[j])
                    ax.text( q2[0], q2[1], '%i' % val, fontsize = num_fs, 
                             va = va, ha = ha)
    if rot:
        rotation = 90 - 180*np.abs(pp)/math.pi
        b = rotation < -90
        rotation[b] = 180+rotation[b]
    else:
        rotation = np.zeros(M)
        
    for j in range(pnts.shape[1]):
        (x, y) = (pnts[0,j], pnts[1,j])
        
        ha = 'center'
        if x < 0:
            ha = 'right'
        else: 
            ha = 'left'
        va = 'center'
        if y == 0:
            pass
        elif y < 0:
            va = 'top'
        else: 
            va = 'bottom'
            
        a = (df.loc[clst[j], clst[j]] != 0)*(Rs*2)
        if ax is None: 
            plt.plot( x, y, 'o', ms = node_size, c = color_lst[j])
            plt.text( x, y, ' %s ' % clst[j], fontsize = text_fs, 
                      ha = ha, va = va, rotation = rotation[j])
        else:
            ax.plot( x, y, 'o', ms = node_size, c = color_lst[j])
            ax.text( x*(1+a), y*(1+a), '  %s  ' % clst[j], fontsize = text_fs, 
                     ha = ha, va = va, rotation = rotation[j])

    if ax is None: 
        plt.xticks([])
        plt.yticks([])
        plt.margins(x=margin, y=margin)
    else:
        ax.set_xticks([])
        ax.set_yticks([])
        ax.margins(x=margin, y=margin)
        
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False) 
        
    if title is not None: ax.set_title(title, fontsize = title_fs )
        
    if show: plt.show()
    return