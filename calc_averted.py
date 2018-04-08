# coding=utf-8
from seirv_generic_groups import run_model
import numpy as np
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
def get_doses():
    pass


def get_averted():
    baseline = np.array(run_model(path="popmodel-seirv.yaml",r_lst=True))
    labels = np.array(run_model(path="popmodel-seirv.yaml",r_lst=True))#[1]
    print(baseline)
    #averted = np.array(baseline[0]) - np.array(run_model(path="popmodel-seirv-changed.yaml",r_lst=True)[0])
    #sns.barplot(labels, averted, palette="BuGn_d")
    #plt.show()



get_averted()