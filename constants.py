AGE_GROUP_NAMES = ['young','mid','old','veryold']
STATES = ['s','i','r','v']


class IGroup:
    def __init__(self, name,age_group_names):
        self.name = name
        self.age_group_names = age_group_names
        self.sub_groups = self.generate_sub_groups()
        # initial vector
        # beta
        # gamma
    def generate_sub_groups(self):
        age_groups = []
        for age_group_name in self.age_group_names:
            age_groups.append(AgeGroup(self, age_group_name))
        groups = []
        for age_group in age_groups:
            for state in STATES:
                groups.append(State(age_group,state))
        return groups


    def __str__(self):
        return self.name

class AgeGroup():
    def __init__(self, igroup,age_group_name):
        self.group = igroup
        self.age_group = age_group_name
    def __str__(self):
        return str(self.group)+"_"+str(self.age_group)

class State():
    def __init__(self, age_group, state_name):
        self.group = str(age_group.group)
        self.age_group = str(age_group)
        self.state = state_name

    def __str__(self):
        return str(self.group) + "_" + str(self.age_group) + "_" + self.state

# class StateGroup(AgeGroup):
#     def __init__(self, name,age_group_name):
#         IGroup.__init__(self)
#         self.name = name
#         self.age_group_name = age_group_name
#     def __str__(self):
#         return self.name+"_"+self.age_group_name


igroups = [IGroup('g1',AGE_GROUP_NAMES),IGroup('g2',AGE_GROUP_NAMES)]

groups = []

for group in igroups:
    for g in group.sub_groups:
        groups.append(g)
        #print(str(g))

