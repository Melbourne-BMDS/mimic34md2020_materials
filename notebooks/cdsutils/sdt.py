import numpy as np
import numpy.random as ra
import matplotlib.pyplot as plt
import seaborn as sns
import ipywidgets as ipw
from IPython.display import display, HTML
from cdsutils.mutils import *
from cdsutils.sdt import *

def pop1(l1,l2,n):
    return ra.uniform(l1,l2,n)

def pop2(l1,l2,n):
    return ra.normal(l1,l2,n)

def pop3(p1, p2, n):
    return ra.rayleigh(p1,n)



def num_pos(data, threshold):
    return len([d for d in data if d >= threshold])
def num_neg(data, threshold):
    return len([d for d in data if d < threshold])
def pf(data, threshold):
    return num_pos(data, threshold)/len(data)
def pops_min(*ps):
    return np.min([np.min(p) for p in ps])
def pops_max(*ps):
    return np.max([np.max(p) for p in ps])

def trace_roc(pos, neg, num=100, delta=0.1):
    mint = pops_min(pos,neg)
    maxt = pops_max(pos,neg)
    
    return ([pf(neg,t) for t in np.linspace(maxt+delta, mint-delta, num=num)],
           [pf(pos,t) for t in np.linspace(maxt+delta, mint-delta, num=num)]
        )
    

def _auc(fpf, tpf):
    auc = 0.0
    for i in range(len(fpf)-1):
        dx = fpf[i+1]-fpf[i]
        y2 = tpf[i+1]
        y1 = tpf[i]
        auc = auc + dx*y1

    return auc
def auc(pos, neg):
    fs, ts = trace_roc(pos, neg)
    return _auc(fs,ts)


def ppv(pos,neg, t):
    try:
        np = num_pos(pos, t)
        return np/(np+num_pos(neg, t))
    except ZeroDivisionError:
        return 1.0
def npv(pos, neg, t):
    try:
        nn = num_neg(neg, t)
        return nn/(nn+num_neg(pos, t))
    except ZeroDivisionError:
        return 1.0

def compute_stats(pos, neg):
    
    rslts = ipw.HTML()
    out1 = ipw.Output()
    box = ipw.HBox([out1, rslts])

    prev = len(pos)/(len(pos)+len(neg))
    cprev= 1-prev
    mint = pops_min(pos,neg)
    maxt = pops_max(pos,neg)
    fs,ts = trace_roc(pos, neg)
    auc_value = _auc(fs,ts)
    
    @interact(t=ipw.FloatSlider(min=mint+0.5,max=maxt-0.5))
    def _compute_stats(t):
        out1.clear_output(wait=True)
        tpf = pf(pos,t)
        sens = tpf
        fpf = pf(neg,t)
        spec = 1-fpf
        ntp = num_pos(pos,t)
        nfn = len(pos)-ntp
        ntn = num_neg(neg,t)
        nfp = len(neg)-ntn
        acc = (ntp+ntn)/(len(pos)+len(neg))
        _rslts = {"t":"% 3.2f"%t}
        _rslts["ppv"] = "(%3.2f, %3.2f)"%(ppv(pos,neg,t),tpf*prev/(tpf*prev+fpf*(1-prev)))
        _rslts["npv"] = "(%3.2f, %3.2f)"%(npv(pos,neg,t), spec*cprev/((1-tpf)*prev+spec*(cprev)))
        _rslts["sens."] = "%3.2f"%tpf
        _rslts["spec."] = "%3.2f"%(1 -fpf)
        _rslts["acc."] = "%3.2f"%(acc)
        _rslts["AUC"] = "%3.2f"%(auc_value)
        rslts.value = ddict(_rslts, template=dt2)
        with out1:
            dot = plt.Circle((fpf,tpf), 0.05, color='red')
            f1,(a1,a2) = plt.subplots(nrows=1, ncols=2)
            a2.plot(fs,ts)
            sns.distplot(neg,ax=a1, kde=False)
            sns.distplot(pos,ax=a1, kde=False)
            a1.axvline(t, c='k')
            a2.set_aspect("equal")
            a2.add_artist(dot)
            plt.show(f1)
            
        display(box)


