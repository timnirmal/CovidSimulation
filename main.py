# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import random
from typing import List

populationSize = 100
familySizeMin = 2
familySizeMax = 7
wearFaceMask = False
fatalityRate = 0.1

positiveDate = 5



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
        self.age = None
        self.status = None
        self.infectedDate = 0

    def get_id(self):
        return self.id

    def set_age(self, age):
        self.age = age

    def get_age(self):
        return self.age

    def set_positive(self):
        self.status = "positive"

    def set_infected(self):
        self.status = "infected"

    def set_recovered(self):
        self.status = "recovered"

    def set_infected_date(self, date):
        self.infectedDate = date

    def get_infected_date(self):
        return self.infectedDate

    def get_status(self):
        return self.status

    def get_status_str(self):
        if self.status == "positive":
            return "infected"
        elif self.status == "infected":
            return "infected"
        elif self.status == "recovered":
            return "recovered"
        else:
            return "healthy"



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
    # def get_members_list_by_age(self):
    #   return sorted(self.members, key=lambda x: x.age)


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


if __name__ == '__main__':
    print_hi('PyCharm')

    # person = Person()
    # print(person.get_id())

    personList: list[Person] = []

    for i in range(populationSize):
        personList.append(Person())

    for person in personList:
        print(person.get_id())

    ######################################################################
    """ Setting Ages """

    seniorNumber = int(populationSize * 0.3)
    childrenNumber = int(populationSize * 0.2)
    adultNumber = populationSize - seniorNumber - childrenNumber

    # set first 30% of population to be seniors
    for i in range(seniorNumber):
        personList[i].set_age(random.randint(65, 85))

    # set next adultNumber of population to be adult
    for i in range(seniorNumber, seniorNumber + adultNumber):
        personList[i].set_age(random.randint(18, 65))

    # set Last 20% of population to be children
    for i in range(seniorNumber + adultNumber, populationSize):
        personList[i].set_age(random.randint(0, 18))

    ######################################################################
    """ Create family """
    familyList: list[Family] = []

    familyCount = 0
    memberCountList: list[int] = []
    # create list number population size
    for i in range(populationSize):
        memberCountList.append(i)

    while familyCount < populationSize:
        # create a new Family
        family = Family()

        # Generate number between 2 and 7
        familySize = random.randint(familySizeMin, familySizeMax)

        # if familyCount + familySize > populationSize
        if familyCount + familySize > populationSize:
            # set familySize to 100000 - familyCount
            familySize = populationSize - familyCount
        # TODO: Fix this
        if familySize < familySizeMin:
            # add another person to previous family
            family.add_member(personList[familyCount])
            familyCount += 1
            continue

        # add 100 members to the Family
        for i in range(familySize):
            # get random member from memberCountList
            randomMember = random.choice(memberCountList)
            # remove random member from memberCountList
            memberCountList.remove(randomMember)
            # add random member to family
            family.add_member(personList[randomMember])
            familyCount += 1
        # add the Family to the FamilyList
        familyList.append(family)

    # print the FamilyList
    for family in familyList:
        print(family.get_family_id())
        # print(family.get_members_list())
        print(family.get_member_count())
        # Person id of first member in family
        print(family.get_member_id(family.get_members_list()[0]))
        # Person id of last member in family
        print(family.get_member_id(family.get_members_list()[-1]))
        print()

    print("Family count: " + str(len(familyList)))










    ######################################################################
    """ Run while loop until 100 days """

    day = 1
    positiveCount = 0
    deathCount = 0
    infectedCount = 0

    while day < 10:
        ######################################################################
        """ Positive """
        if day == 1:
            print("Day " + str(day))
            print("Make 1 Random Person Positive")

            # get random person from personList
            randomPerson = random.choice(personList)
            # set person to be positive
            randomPerson.set_infected()
            randomPerson.set_infected_date(day)
            positiveCount += 1

            # print person id
            print(randomPerson.get_id())
            # print person age
            print(randomPerson.get_age())
            # print person is positive
            print(randomPerson.get_status())

            day += 1
            continue

        else:
            ######################################################################
            """ Infected """
            print("Day " + str(day))
            print("Infect 1 Random Person")

            # get random person from personList
            randomPerson = random.choice(personList)
            # set person to be infected
            randomPerson.set_infected()
            randomPerson.set_infected_date(day)
            positiveCount += 1

            # print person id
            print(randomPerson.get_id())
            # print person age
            print(randomPerson.get_age())
            # print person is infected
            print(randomPerson.get_status())

            day += 1

        ######################################################################
        """ Process Positive Details of Each Person """
        for person in personList:
            dateSinceInfected = day - person.get_infected_date()

            if dateSinceInfected == day:
                print("Person not Infected")
            elif dateSinceInfected < day:
                print("Person Infected")
            elif 5 <= dateSinceInfected <= 11:
                print("Person is Positive")


        ######################################################################
        """ Show Data of each day """

        print("Day " + str(day))
        print("Positive Count: " + str(positiveCount))
        print("Death Count: " + str(deathCount))
        print("Infected Count: " + str(infectedCount))


    print("END")








# 100,000 People (Created Person Classes)
# 30% > are senoir citizens (65 y > age) (Assign age to each person)
# 20% is children (18 y < age)
# 1 family have 2 - 7  memebers (Randomize member adding to family)
#
# 40,000 - essential services TODO
#
# Chance of getting infected:
# 	10-20% - Childrens
# 	15-40% - adults
# 	35-60% - senior
#
# Wearning facemask reduce risk by 5-10%
# If 1 fam member get infected, all fam mems 40 - 80%
#
# Symptoms show after 5th day
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


"""

class Person:
    __lastId = 1

    def __init__(self):
        self.id = Person.__lastId
        Person.__lastId += 1

    def get_id(self):
        return self.id

    def __str__(self):
        return str(self.id)

    def __repr__(self):
        return str(self.id)

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def __lt__(self, other):
        return self.id < other.id

    def __gt__(self, other):
        return self.id > other.id

    def __le__(self, other):
        return self.id <= other.id

"""

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
