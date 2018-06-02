#from sir_generic_groups import run_model, export_to_csv
from seirv_generic_groups import run_model
from pylab import *
from calc_averted import generate_conf
from jinja2 import Template
from load_configuration import Model
import seirv_generic_groups
size = 75
with open('popmodel-seirv.yaml') as file_:
    conf_tmpl = Template(file_.read())
model = Model(generate_conf(conf_tmpl))
sir = seirv_generic_groups.run_model(model=model)
print(sir)
d = {0:np.zeros(51),1:np.zeros(51),2:np.zeros(51),3:np.zeros(51),4:np.zeros(51)}
l = {0:'suspected',1:'exposed',2:'infected',3:'recovered',4:'vaccinated'}
for i in range(len(sir)):
    d[i%5] += sir[:, i]
fig, ax = plt.subplots()
for key in d:
    ax.plot(range(len(d[key])), d[key],label=l[key])
legend = ax.legend(loc='best', shadow=True)

# The frame is matplotlib.patches.Rectangle instance surrounding the legend.
frame = legend.get_frame()
frame.set_facecolor('0.90')

# Set the fontsize
for label in legend.get_texts():
    label.set_fontsize('large')

for label in legend.get_lines():
    label.set_linewidth(1.5)  # the legend line width
plt.show()