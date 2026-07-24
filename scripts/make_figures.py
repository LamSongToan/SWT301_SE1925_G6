"""Regenerate score-level figures for both datasets (Raw and Improved).

Outputs to paper/figures/:
  {raw,improved}_score_distribution.png
  {raw,improved}_score_confusion_matrix.png
  {raw,improved}_dimension_kappa.png
  comparison_dimension_kappa.png
Run from repo root.
"""
import pandas as pd, numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.metrics import cohen_kappa_score, confusion_matrix
from pathlib import Path

FIG = Path('paper/figures'); FIG.mkdir(parents=True, exist_ok=True)

def score_row(s2r, irr, ob, obl, eb, ebl):
    s2r=str(s2r).strip().lower(); irr=str(irr).strip().lower()
    ob=str(ob).strip().lower(); obl=str(obl).strip().lower()
    eb=str(eb).strip().lower(); ebl=str(ebl).strip().lower()
    if s2r=='executable':
        return 5 if (ob=='present' and obl=='sufficient' and eb=='present' and ebl=='accurate') else 4
    if irr=='wrong information': return 1
    if ob=='present' and eb=='present': return 3
    if ob=='present' or eb=='present': return 2
    return 1
def s2r_bin(a): return 1 if str(a).strip().lower()=='executable' else 0
def ob3(a,b):
    a=str(a).strip().lower(); b=str(b).strip().lower()
    return 3 if (a=='present' and b=='sufficient') else (2 if a=='present' else 1)
def eb3(a,b):
    a=str(a).strip().lower(); b=str(b).strip().lower()
    return 3 if (a=='present' and b=='accurate') else (2 if a=='present' else 1)

def load(gt_path, llm_path, suffix):
    gt=pd.read_csv(gt_path, encoding='utf-8-sig'); lm=pd.read_csv(llm_path, encoding='utf-8-sig')
    gt['issue_key']=gt['BUG-ID'].astype(str).str.replace(f' {suffix}','',regex=False).str.strip()
    lm['issue_key']=lm['issue_key'].astype(str).str.strip()
    d=gt.merge(lm,on='issue_key',how='inner')
    d['gt']=d.apply(lambda r:score_row(r['S2R Label'],r['S2R Irrep Category'],r['OB Category'],r['OB Label'],r['EB Category'],r['EB Label']),axis=1)
    d['lm']=d.apply(lambda r:score_row(r['s2r_label'],r['s2r_failure_type'],r['observed_behavior_presence'],r['observed_behavior_quality'],r['expected_behavior_presence'],r['expected_behavior_quality']),axis=1)
    return d

def dim_kappas(d):
    ks2r=cohen_kappa_score(d['S2R Label'].apply(s2r_bin), d['s2r_label'].apply(s2r_bin))
    kob=cohen_kappa_score(d.apply(lambda r:ob3(r['OB Category'],r['OB Label']),axis=1), d.apply(lambda r:ob3(r['observed_behavior_presence'],r['observed_behavior_quality']),axis=1))
    keb=cohen_kappa_score(d.apply(lambda r:eb3(r['EB Category'],r['EB Label']),axis=1), d.apply(lambda r:eb3(r['expected_behavior_presence'],r['expected_behavior_quality']),axis=1))
    kc=cohen_kappa_score(d['gt'],d['lm'])
    return {'S2R':ks2r,'EB':keb,'OB':kob,'Composite':kc}

def figs(d, tag, title):
    x=np.arange(1,6); w=0.38
    # distribution
    fig,ax=plt.subplots(figsize=(7,4.2))
    ax.bar(x-w/2,[(d['gt']==s).sum() for s in x],w,label='Human ground truth',color='#4C72B0')
    ax.bar(x+w/2,[(d['lm']==s).sum() for s in x],w,label='LLM',color='#DD8452')
    ax.set_xlabel('Reproducibility score'); ax.set_ylabel('Number of reports')
    ax.set_title(f'{title}: score distribution (N={len(d)})'); ax.set_xticks(x); ax.legend()
    plt.tight_layout(); plt.savefig(FIG/f'{tag}_score_distribution.png',dpi=150); plt.close()
    # confusion
    cm=confusion_matrix(d['gt'],d['lm'],labels=x)
    fig,ax=plt.subplots(figsize=(5.2,4.6)); im=ax.imshow(cm,cmap='Blues')
    ax.set_xticks(range(5)); ax.set_xticklabels(x); ax.set_yticks(range(5)); ax.set_yticklabels(x)
    ax.set_xlabel('LLM score'); ax.set_ylabel('Human score'); ax.set_title(f'{title}: human vs LLM (N={len(d)})')
    for i in range(5):
        for j in range(5):
            ax.text(j,i,cm[i,j],ha='center',va='center',color='black' if cm[i,j]<cm.max()/2 else 'white')
    plt.colorbar(im,ax=ax,fraction=0.046); plt.tight_layout(); plt.savefig(FIG/f'{tag}_score_confusion_matrix.png',dpi=150); plt.close()
    # dimension kappa
    k=dim_kappas(d); names=['S2R','EB','OB','Composite']; vals=[k[n] for n in names]
    fig,ax=plt.subplots(figsize=(7,4.2))
    bars=ax.bar(names,vals,color=['#55A868','#4C72B0','#C44E52','#8172B3'])
    ax.axhline(0.70,ls='--',color='red',label='Pre-registered threshold (0.70)')
    ax.set_ylabel("Cohen's kappa"); ax.set_ylim(0,1); ax.set_title(f'{title}: agreement by dimension (N={len(d)})'); ax.legend()
    for b,v in zip(bars,vals): ax.text(b.get_x()+b.get_width()/2,v+0.02,f'{v:.3f}',ha='center')
    plt.tight_layout(); plt.savefig(FIG/f'{tag}_dimension_kappa.png',dpi=150); plt.close()
    return k

raw=load('data/raw/full_ground_truth_raw.csv','results/full/full_llm_output_raw.csv','Raw')
imp=load('data/improved/full_ground_truth_improved.csv','results/full/full_llm_output_improved.csv','Improved')
kr=figs(raw,'raw','Raw dataset'); ki=figs(imp,'improved','Improved dataset')

# comparison figure
names=['S2R','EB','OB','Composite']; xi=np.arange(len(names)); w=0.38
fig,ax=plt.subplots(figsize=(7.5,4.4))
ax.bar(xi-w/2,[kr[n] for n in names],w,label='Raw',color='#4C72B0')
ax.bar(xi+w/2,[ki[n] for n in names],w,label='Improved',color='#DD8452')
ax.axhline(0.70,ls='--',color='red',label='Threshold (0.70)')
ax.set_xticks(xi); ax.set_xticklabels(names); ax.set_ylabel("Cohen's kappa"); ax.set_ylim(0,1)
ax.set_title('LLM–human agreement by dimension: Raw vs Improved (N=139 each)'); ax.legend()
for i,n in enumerate(names):
    ax.text(i-w/2,kr[n]+0.02,f'{kr[n]:.2f}',ha='center',fontsize=8)
    ax.text(i+w/2,ki[n]+0.02,f'{ki[n]:.2f}',ha='center',fontsize=8)
plt.tight_layout(); plt.savefig(FIG/'comparison_dimension_kappa.png',dpi=150); plt.close()

print('RAW dims:', {k:round(v,4) for k,v in kr.items()})
print('IMPROVED dims:', {k:round(v,4) for k,v in ki.items()})
print('Figures written to', FIG)
