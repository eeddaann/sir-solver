# coding=utf-8
from seirv_generic_groups import run_model
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from load_configuration import Model

model = Model("popmodel-seirv.yaml")




def get_averted():
    baseline = run_model(path="popmodel-seirv.yaml",r_dict=True)
    age_group = [x.split('_')[1] for x in list(run_model(path="popmodel-seirv.yaml",r_dict=True).keys())]
    group = [x.split('_')[0] for x in list(run_model(path="popmodel-seirv.yaml",r_dict=True).keys())]
    doses = [model.doses[x] for x in list(run_model(path="popmodel-seirv.yaml",r_dict=True).keys())]
    baseline_values = np.array(list(baseline.values()))
    changed_values = np.array(list(run_model(path="popmodel-seirv-changed.yaml",r_lst=True)))
    print(changed_values)
    averted = (baseline_values - changed_values) / doses
    return [age_group,list(averted),group]



df = pd.DataFrame(get_averted())
df = df.transpose()
df.columns = ['who', 'survived','class']
print(df)
g = sns.factorplot(x="who", y="survived", col="class",data=df, saturation=.5,kind="bar", ci=None, aspect=.6)
#(g.set_axis_labels("", "cases averted per dose").set_xticklabels(["infants", "children", "adults","matures"],rotation=45).set_titles("{col_name}").despine(left=True))
(g.set_axis_labels("", "cases averted per dose").set_xticklabels(rotation=45).set_titles("{col_name}").despine(left=True)) # TODO: fix xticklabels order
plt.show()