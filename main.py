#from sir_generic_groups import run_model, export_to_csv
from seirv_generic_groups import run_model
from pylab import *
size = 75

sir = run_model()
#export_to_csv()
for i in range(size):
    Sa = (sir[:, i])
    plot(range(len(Sa)), Sa)

plt.show()