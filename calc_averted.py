# coding=utf-8
from seirv_generic_groups import run_model
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from load_configuration import Model

model = Model("popmodel-seirv.yaml")
changed_model = Model("popmodel-seirv-changed.yaml")




def get_averted():
    baseline_d = run_model(path="popmodel-seirv.yaml",r_dict=True)
    changed_d = run_model(path="popmodel-seirv-changed.yaml",r_dict=True)
    age_group = [x.split('_')[1] for x in list(baseline_d.keys())]
    group = [x.split('_')[0] for x in list(baseline_d.keys())]
    doses = [model.doses[x] for x in list(baseline_d.keys())]
    changed_doses = [changed_model.doses[x] for x in list(baseline_d.keys())]
    baseline_values = np.array(list(baseline_d.values()))
    changed_values = np.array(list(changed_d.values()))
    averted = (baseline_values / doses) - (changed_values/changed_doses)
    return [age_group,list(averted),group]



df = pd.DataFrame(get_averted())
df = df.transpose()
df.columns = ['age_group', 'cases_averted_per_dose','group']
g = sns.factorplot(x="age_group", y="cases_averted_per_dose", col="group",data=df, saturation=.5,kind="bar", ci=None, aspect=.6,order=["infants", "children", "adults","matures"],col_order=['ij','ia','ib','pb','p'])
(g.set_axis_labels("", "cases averted per dose").set_xticklabels(rotation=45).set_titles("{col_name}").despine(left=True))

for ax in g.axes[0]:
    for p in ax.patches:
        if not np.isnan(p.get_height()):
            ax.text(p.get_x() + p.get_width()/2., p.get_height(), '%0.2f' % p.get_height(),
                fontsize=12, color='blue', ha='center', va='bottom')
plt.show()
