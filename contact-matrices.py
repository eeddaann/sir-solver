# coding=utf-8
import numpy as np
# population structures 0-4,5-9..

I_STRUCT = [878200,806900,730500,669200,616000,596000,584600,558700,532900,454100,404100,386600,369400,335400,206300,416900]
I_STRUCT_R = [ 878200, 2206700, 3342400, 2119000]

#IA_STRUCT =
IA_STRUCT_R =[201700,592200,725600,258300]

#IJ_STRUCT =
IJ_STRUCT_R =[676500,1614500,2616800,1860700]

P_STRUCT = [724031,619066,564274,532297,499859,423717,328891,269645,228529,191227,158553,120364,81366,56146,38615,47756]
P_STRUCT_R = [724031,1715637,1941868,502800]

ROW_MASK = np.array([np.concatenate([[1],[2]*3,[3]*6,[4]*6]),]) # cells by age group (extra , for 2d array)
COL_MASK = np.array([np.concatenate([[7],[8]*3,[9]*6,[10]*6]),])
# load csv to numpy array
I_raw_contacts = np.loadtxt(open("data/I-contacts.csv", "rb"), delimiter=",", skiprows=1)
J_raw_contacts = np.loadtxt(open("data/J-contacts.csv", "rb"), delimiter=",", skiprows=1)

# Dor
JJ = 0.5489150242
JM = 0.02461634309
MJ = 0.2282321494
MM = 0.1982364834

def create_mask(row_mask = ROW_MASK,col_mask = COL_MASK):
    return np.dot(row_mask.T,col_mask)

def normalize(arr):
    return arr / sum(arr)

def per_week(arr):
    return arr * 7

def transform(struct, raw_contacts):
    mask = create_mask()
    d = dict(zip([7,8,9,10,14,16,18,20,21,24,27,30,28,32,36,40], len([7,8,9,10,14,16,18,20,21,24,27,30,28,32,36,40])*[0]))
    struct = np.array(struct)
    total_contacts = raw_contacts * struct # multiply by weight
    for (x, y), value in np.ndenumerate(mask):
          #d[value] += value # for demo
          d[value] += total_contacts[(x, y)]
    arr = np.array(sorted(list(d.values()))).reshape(4,4)
    # arr = normalize(arr)
    return per_week(arr)

#print(create_mask())


def main():
    print("###_P_###")
    print(transform(P_STRUCT, J_raw_contacts)/P_STRUCT_R)

    print("###_I_###")
    print(transform(I_STRUCT, I_raw_contacts)/I_STRUCT_R)


main()
