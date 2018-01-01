#from sir_generic_groups import run_model, export_to_csv
from seirv_generic_groups import run_model, export_to_csv
from pylab import *
size = 75
# no vaccination policy:
p = [1]*100

sir = run_model(p)
export_to_csv(p)
for i in range(size):
    Sa = (sir[:, i])
    plot(range(len(Sa)), Sa)

plt.show()