# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import random


class MyClass:
    def __init__(self, value):
        self.value = value

    def get_value(self):
        return self.value

    def set_value(self, value):
        self.value = value

    def increment(self):
        self.value += 1

    def decrement(self):
        self.value -= 1

    def reset(self):
        self.value = 0

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self.value)

    def __add__(self, other):
        return self.value + other.value

    def __sub__(self, other):
        return self.value - other.value

    def __mul__(self, other):
        return self.value * other.value


class Person:
    __lastId = 1

    def __init__(self):
        self.id = Person.__lastId
        Person.__lastId += 1

    def get_id(self):
        return self.id


class Family:
    __familyId = 1

    def __init__(self):
        self.id = Family.__familyId
        Family.__familyId += 1

        self.members = []

    def get_members(self):
        return self.members

    def add_member(self, member):
        self.members.append(member)

    def remove_member(self, member):
        self.members.remove(member)

    def get_member_count(self):
        return len(self.members)

    def get_member_age(self, member):
        return member.age

    def get_member_id(self, member):
        return member.id

    # family id
    def get_family_id(self):
        return self.id

    # return members list
    def get_members_list(self):
        return self.members

    # return members list
    #def get_members_list_by_age(self):
     #   return sorted(self.members, key=lambda x: x.age)



def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


if __name__ == '__main__':
    print_hi('PyCharm')

    # person = Person()
    # print(person.get_id())

    personList = []

    for i in range(100000):
        personList.append(Person())

    for person in personList:
        print(person.get_id())

    family = Family()

    familyList = []

    familyCount = 0

    # create Families with 100 members from personlist

    # while familyCount = 100000
    while familyCount < 100000:
        # create a new Family
        family = Family()

        # Generate number between 2 and 7
        familySize = random.randint(2, 7)

        # if familyCount + familySize > 100000
        if familyCount + familySize > 100000:
            # set familySize to 100000 - familyCount
            familySize = 100000 - familyCount

        # TODO: Fix this
        if familySize < 2:
            # add another person to previous family
            family.add_member(personList[familyCount])
            familyCount += 1
            continue

        # add 100 members to the Family
        for i in range(familySize):
            family.add_member(personList[familyCount])
            familyCount += 1
        # add the Family to the FamilyList
        familyList.append(family)

    # print the FamilyList
    for family in familyList:
        print(family.get_family_id())
        #print(family.get_members_list())
        print(family.get_member_count())
        # Person id of first member in family
        print(family.get_member_id(family.get_members_list()[0]))
        # Person id of last member in family
        print(family.get_member_id(family.get_members_list()[-1]))
        print()

    print("Family count: " + str(len(familyList)))




"""
    # print the number of members in each Family
    for family in familyList:
        print(family.get_family_id())
        print(family.get_member_count())
"""

"""


    for i in range(100):
        familyList.append(Family())
        print("Done")
        # for j in range(50000):
        #   familyList[i].add_member(personList[j])
        #  print("Person id " + str(personList[j].get_id()), end= " ")

    print(familyList)
    print()
    # print(familyList[1].get_members_list())
    print("\nosjdosdjosd\n")
    # print(familyList[0].get_members_list())

    # add 2 persons to the family list
"""

"""
    print(family.get_member_count())

    # add 2 person to family from personList
    for i in range(2):
        family.add_member(personList[i])

    print(family.get_member_count())
    print(family.get_member_id(personList[0]))
    print(family.get_members_list())
    print("IDs:")

    # for each person in family, print id
    for person in family.get_members_list():
        print(person.get_id())

    print("IDs:")

    # add 2 person to family from personList
    for i in range(2, 4):
        family.add_member(personList[i])

    print(family.get_member_count())
    print(family.get_member_id(personList[0]))
    print(family.get_members_list())
    print("IDs:")

    # for each person in family, print id
    for person in family.get_members_list():
        print(person.get_id())

    print("IDs:")
"""

# 100,000 families
# 1 family have 2 - 7  memebers
# 30% > are senoir citizens (65 y > age)
# 20% is children (18 y < age)
#
# 40,000 - essential services
#
# Chance of getting infected:
# 	10-20% - Childrens
# 	15-40% - adults
# 	35-60% - senior
#
# Wearning facemask reduce risk by 5-10%
# If 1 fam member get infected, all fam mems 40 - 80%
#
# Sysmptems show after 5th day
# From 11th day not infection from person
# Hospitalized for 10 days
#
# fatality rate 0.1%
# immune for 6-7 months
#
# day 1 - one person get positive
#
# wear facemask | enforce/lift travel restriction
#
# Daily number of infected persons
# Total hospitalized patient count
# total fatalities
# number of recovered up to 50 days
