# coding=utf-8
from seirv_generic_groups import run_model
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from load_configuration import Model
from jinja2 import Template

def get_averted(base,changed):
    '''
    
    :param base: the original state
    :param changed: the alternative
    :return: list of lists for 
    '''
    baseline_d = run_model(model=base,r_dict=True)
    changed_d = run_model(model=changed,r_dict=True)
    age_group = [x.split('_')[1] for x in list(baseline_d.keys())]
    group = [x.split('_')[0] for x in list(baseline_d.keys())]
    doses = [model.doses[x] for x in list(baseline_d.keys())]
    changed_doses = np.array([changed_model.doses[x] for x in list(baseline_d.keys())])
    baseline_values = np.array(list(baseline_d.values()))
    changed_values = np.array(list(changed_d.values()))
    averted = (baseline_values - changed_values) / sum(changed_doses-doses)
    df = pd.DataFrame([age_group,list(averted),group])
    df = df.transpose()
    df.columns = ['age_group', 'cases_averted_per_dose','group']
    return df

def generate_conf(conf_tmpl,context={}):
    return conf_tmpl.render(context)

def capd_plot(df):
    '''
    create visualization
    :param df: dataframe with results of get_averted
    :return: 
    '''
    g = sns.factorplot(x="age_group", y="cases_averted_per_dose", col="group",data=df, saturation=.5,kind="bar", ci=None, aspect=.6,order=["infants", "children", "adults","matures"],col_order=['ij','ia','ib','pb','p'])
    (g.set_axis_labels("", "cases averted per dose").set_xticklabels(rotation=45).set_titles("{col_name}").despine(left=True))

    for ax in g.axes[0]:
        for p in ax.patches:
            if not np.isnan(p.get_height()):
                ax.text(p.get_x() + p.get_width()/2., p.get_height(), '%0.3f' % p.get_height(),
                fontsize=12, color='blue', ha='center', va='bottom')
        plt.show()

if __name__ == "__main__":
    # run this code when this module is being run directly
    with open('popmodel-seirv.yaml') as file_:
        conf_tmpl = Template(file_.read())


    model = Model(generate_conf(conf_tmpl))
    d ={}
    d['p_coverage'] = 0.2
    d['infants_beta'] = 0.01
    changed_model = Model(generate_conf(conf_tmpl,d))
    capd_plot(get_averted(model,changed_model))