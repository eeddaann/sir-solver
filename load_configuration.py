import yaml
import numpy as np

STATES = ['s', 'e', 'i', 'r', 'v']


class IGroup:
    def __init__(self, name, subgroups, beta, gamma):
        self.name = name
        self.beta = beta
        self.gamma = gamma
        self.sub_groups = self.generate_sub_groups(subgroups)

    def generate_sub_groups(self, subgroups):
        sub_groups = []
        for sub_group in subgroups:
            sub_groups.append(SubGroup(self, sub_group))
        groups = []
        for sub_group in sub_groups:
            for state in STATES:
                groups.append(State(sub_group, state))
        return groups

    def __str__(self):
        return self.name


class SubGroup():
    def __init__(self, igroup, sub_group):
        self.group = igroup
        self.name = sub_group['name']
        self.size = sub_group['size']
        self.coverage = sub_group['coverage']
        self.doses = self.size * self.coverage
        if 'beta' in sub_group:
            self.beta = sub_group['beta']
        else:
            self.beta = self.group.beta
        if 'gamma' in sub_group:
            self.gamma = sub_group['gamma']
        else:
            self.gamma = self.group.gamma
        if 'contacts' in sub_group:
            self.contacts_raw = sub_group['contacts']
        else:
            self.contacts_raw = {}

    def __str__(self):
        return str(self.group) + "_" + str(self.name)


class State():
    def __init__(self, sub_group, state_name):
        self.group = str(sub_group.group)
        self.sub_group = sub_group
        self.state = state_name
        self.beta = self.sub_group.beta
        self.gamma = self.sub_group.gamma
        self._r0 = self.sub_group.size * 0.0
        self.initial_number = self._get_size()
        self.contacts_vector = None
        self.doses = self.sub_group.size * self.sub_group.coverage

    def _get_size(self):
        if self.state is 's':
            return (self.sub_group.size - (self.sub_group.size * 20.0 ** -4) - self._r0) * (1 - self.sub_group.coverage)
        elif self.state in ['e', 'i']:
            return self.sub_group.size * 10.0 ** -4
        elif self.state is 'r':
            return self._r0
        elif self.state is 'v':
            return (self.sub_group.size - (self.sub_group.size * 20.0 ** -4) - self._r0) * self.sub_group.coverage

    def __str__(self):
        return str(self.sub_group) + "_" + self.state

    def generate_contacts_vector(self, sub_groups_lst):
        # TODO: this function is ugly!
        if self.state == 's':  # should be more agnostic..
            contacts_vector = []
            for subgroup in sub_groups_lst:
                if (str(subgroup.sub_group) in self.sub_group.contacts_raw) and (subgroup.state is 's'):
                    contacts_vector.append(self.sub_group.contacts_raw[str(subgroup.sub_group)])
                else:
                    contacts_vector.append(0)
            self.contacts_vector = contacts_vector
        else:
            self.contacts_vector = None


class Model:
    def __init__(self, config_path):
        self.doses = {}
        self.dataMap = self.load_DataMap(config_path)
        self.global_params = self.load_global_params()
        self.groups = self.load_groups()
        for g in self.groups:
            g.generate_contacts_vector(self.groups)

        PopIn = np.array([g.initial_number for g in self.groups])
        self.total_pop = sum(PopIn)
        self.PopIn = PopIn / sum(PopIn)
        self.contacts = [g.contacts_vector for g in self.groups]  # TODO: normalize
        self.beta = [g.beta for g in self.groups]
        self.gamma = [g.gamma for g in self.groups]
        self.states = [g.state for g in self.groups]
        self.groups_num = len(self.groups)

    def load_DataMap(self, config_path):
        f = open(config_path)
        dataMap = yaml.load(f)
        f.close()
        return dataMap

    def load_global_params(self):
        return self.dataMap[0]['global'][0]

    def load_groups(self):
        default_beta = self.dataMap[0]['global'][-1]['beta']
        default_gamma = self.dataMap[0]['global'][-1]['gamma']


        groups = []
        for group in self.dataMap[1]['groups']:
            beta, gamma = default_beta, default_gamma
            if 'beta' in group:
                beta = group['beta']
            if 'gamma' in group:
                gamma = group['gamma']
            groups.append(IGroup(group['name'], group['subgroups'], beta, gamma))

        sub_groups = []

        for group in groups:
            for g in group.sub_groups:
                sub_groups.append(g)
                self.doses[str(g)] = g.doses
        return sub_groups

    def set_global_beta(self,val):
        self.beta = [val]*len(self.beta)

    def set_global_gamma(self,val):
        self.gamma = [val]*len(self.gamma)
