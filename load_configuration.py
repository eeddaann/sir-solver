
import yaml
STATES = ['s','i','r','id','v']
class IGroup:
    def __init__(self, name,subgroups,beta,gamma,initial_ratio):
        self.name = name
        self.beta = beta
        self.gamma = gamma
        self.initial_ratio = initial_ratio
        self.sub_groups = self.generate_sub_groups(subgroups)
    def generate_sub_groups(self,subgroups):
        sub_groups = []
        for sub_group in subgroups:
            sub_groups.append(SubGroup(self, sub_group))
        groups = []
        for sub_group in sub_groups:
            for state in STATES:
                groups.append(State(sub_group,state))
        return groups


    def __str__(self):
        return self.name

class SubGroup():
    def __init__(self, igroup,sub_group):
        self.group = igroup
        self.name = sub_group['name']
        self.size = sub_group['size']
        if 'beta' in sub_group:
            self.beta = sub_group['beta']
        else:
            self.beta = self.group.beta
        if 'gamma' in sub_group:
            self.gamma = sub_group['gamma']
        else:
            self.gamma = self.group.gamma
        if 'initial ratio' in sub_group:
            self.initial_ratio = sub_group['initial ratio']
        else:
            self.initial_ratio = self.group.initial_ratio
    def __str__(self):
        return str(self.group)+"_"+str(self.name)

class State():
    def __init__(self, sub_group, state_name):
        self.group = str(sub_group.group)
        self.sub_group = str(sub_group)
        self.state = state_name
        self.beta = sub_group.beta
        self.gamma = sub_group.gamma
        self.initial_number = sub_group.size * sub_group.initial_ratio[self.state]

    def __str__(self):
        return str(self.sub_group) + "_" + self.state

class Model:
    def __init__(self, config_path='config.yaml'):
        self.dataMap = self.load_DataMap(config_path)
        self.global_params = self.load_global_params()
        self.groups = self.load_groups()
    def load_DataMap(self,config_path):
        f = open(config_path)
        dataMap = yaml.load(f)
        f.close()
        return dataMap
    def load_global_params(self):
        return self.dataMap[0]['global'][0]
    def load_groups(self):
        default_beta = self.dataMap[0]['global'][-1]['beta']
        default_gamma = self.dataMap[0]['global'][-1]['gamma']
        default_initial_ratio = self.dataMap[0]['global'][-1]['initial ratio']

        groups = []
        for group in self.dataMap[1]['groups']:
            print(group)
            beta,gamma,initial_ratio = default_beta,default_gamma,default_initial_ratio
            if 'beta' in group:
                beta = group['beta']
            if 'gamma' in group:
                gamma = group['gamma']
            if 'initial ratio' in group:
                initial_ratio = group['initial ratio']
            groups.append(IGroup(group['name'],group['subgroups'],beta,gamma,initial_ratio))

        sub_groups = []

        for group in groups:
            for g in group.sub_groups:
                sub_groups.append(g)
        return sub_groups
