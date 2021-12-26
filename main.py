import random
from matplotlib import pyplot as plt, animation
import numpy as np
import pandas as pd
import plotly.express as px
from matplotlib.widgets import RadioButtons, Button

populationSize = 1000
familySizeMin = 2
familySizeMax = 7
wearFaceMask = False
travelRestrictions = False
fatalityRate = 0.1
daysToSimulate = 100

positiveDate = 5


class Person:
    __lastId = 1

    # TODO : Check on changing __lastId from 0 to 1

    def __init__(self, status):
        self.id = Person.__lastId
        Person.__lastId += 1
        self.age = None
        self.status = status
        self.infectedDate = None
        self.time_sick = 0
        self.family_id = 0
        self.essentialWorker = False

    def get_id(self):
        return self.id

    def set_age(self, age):
        self.age = age

    def get_age(self):
        return self.age

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

    def add_family_id(self, fam_id):
        self.family_id = fam_id

    def get_family_id(self):
        return self.family_id

    def set_essential_worker(self, is_essential):
        self.essentialWorker = is_essential

    def get_essential_worker(self):
        return self.essentialWorker


class Family:
    __familyId = 1

    def __init__(self):
        self.id = Family.__familyId
        Family.__familyId += 1

        self.members = []
        self.familyInfected = False

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

    def get_family_infected(self):
        return self.familyInfected

    def set_family_infected(self, infected):
        self.familyInfected = infected

    # return members list
    # def get_members_list_by_age(self):
    #   return sorted(self.members, key=lambda x: x.age)


if __name__ == '__main__':
    # person = Person()
    # print(person.get_id())

    personList: list[Person] = []

    for i in range(populationSize):
        personList.append(Person('healthy'))

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
    """ Setting Essential Workers """
    # 40,000 people from 18 to 65 years old are essential workers
    # 50,000 people are adults
    essentialWorkerNumber = 0

    while essentialWorkerNumber < 40000:
        personList[random.randint(seniorNumber, seniorNumber + adultNumber)].set_essential_worker(True)
        essentialWorkerNumber += 1

    print("Number of Essential Workers: ", essentialWorkerNumber)

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

        # add members to the Family
        for i in range(familySize):
            # get random member from memberCountList
            randomMember = random.choice(memberCountList)
            # remove random member from memberCountList
            memberCountList.remove(randomMember)
            # add random member to family
            family.add_member(personList[randomMember])
            # add family id to random member PersonList
            personList[randomMember].add_family_id(family.get_family_id())
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
    """ Simulation """
    print("Day, Healthy, Sick, Recovered, Dead")

    n_healthy = populationSize - 1
    n_sick = 1

    healthy_history: list[int] = [n_healthy]
    sick_history: list[int] = [n_sick]
    recovered_history = [0]
    dead_history = [0]
    dateList: list[int] = [0]
    # days = [day for day in range(daysToSimulate)]

    # First day 1 random person is sick

    for day in range(daysToSimulate):
        healthy = 0
        sick = 0
        recovered = 0
        dead = 0

        dateList.append(dateList[-1] + 1)

        # First day 1 random person is sick
        if day == 0:
            person1 = random.randint(0, populationSize - 1)
            personList[person1].status = "Sick"
            sick += 1
            # person family
            familyList[personList[person1].get_family_id() - 1].set_family_infected(True)
            healthy = populationSize -sick
            healthy_history.append(healthy)
            sick_history.append(sick)
            recovered_history.append(recovered)
            dead_history.append(dead)
            continue

        for person in personList:
            # get persons family id and get family from familyList
            family_id = person.get_family_id()
            # print("family_id: " + str(family_id))
            family = familyList[person.get_family_id() - 1]

            if person.status == 'sick' and person.time_sick < 15:
                person.time_sick += 1
                family.set_family_infected(True)
            elif person.status == 'sick' and person.time_sick == 15:
                family.set_family_infected(False)
                # Dead or Alive
                if random.randint(0, 9) == 4:
                    person.status = 'dead'
                else:
                    person.status = 'recovered'
                    # set family infected to False

            if person.status == 'healthy':
                # Define chance of getting infected
                chance_of_infection = 0

                # if family is infected
                if family.get_family_infected():
                    if person.get_age() < 18:
                        chance_of_infection = random.uniform(0.050, 0.100)
                    elif 18 <= person.get_age() < 65:
                        chance_of_infection = random.uniform(0.055, 0.120)
                    elif person.get_age() >= 65:
                        chance_of_infection = random.uniform(0.075, 0.140)
                    if travelRestrictions:
                        chance_of_infection += 0.1
                    print("family infected" + str(family))
                else:
                    # if family is not infected
                    if person.get_age() < 18:
                        chance_of_infection = random.uniform(0.010, 0.020)
                    elif 18 <= person.get_age() < 65:
                        chance_of_infection = random.uniform(0.015, 0.040)
                    elif person.get_age() >= 65:
                        chance_of_infection = random.uniform(0.035, 0.060)
                    if travelRestrictions:
                        chance_of_infection = 0

                # Face Mask
                if wearFaceMask:
                    chance_of_infection = random.uniform(0.005, 0.010)

                # Essential Worker
                if person.get_essential_worker():
                    chance_of_infection += random.uniform(0.020, 0.040)

                if random.random() < chance_of_infection:
                    person.status = 'sick'
                    family.set_family_infected(True)

        for person in personList:
            if person.status == 'healthy':
                healthy += 1
            elif person.status == 'sick':
                sick += 1
            elif person.status == 'recovered':
                recovered += 1
            else:
                dead += 1

        healthy_history.append(healthy)
        sick_history.append(sick)
        recovered_history.append(recovered)
        dead_history.append(dead)

        print(day, healthy, sick, recovered, dead)

    ######################################################################
    """ Clear Data Set """

    # remove first element from list
    dateList.pop(0)
    healthy_history.pop(0)
    sick_history.pop(0)
    recovered_history.pop(0)
    dead_history.pop(0)
    print()
    print(dateList)
    print(healthy_history)
    print(sick_history)
    print(recovered_history)
    print(dead_history)

    print()
    print(len(dateList))
    print(len(healthy_history))
    print(len(sick_history))
    print(len(recovered_history))
    print(len(dead_history))


    ######################################################################
    """ Graph """

    # Plot the data
    plt.plot(dateList, healthy_history, label='Healthy')
    plt.plot(dateList, sick_history, label='Sick')
    plt.plot(dateList, recovered_history, label='Recovered')
    plt.plot(dateList, dead_history, label='Dead')
    plt.xlabel('Days')
    plt.ylabel('People')
    plt.title('COVID-19 Simulation')
    plt.legend()
    plt.show()

    ######################################################################
    """ Animated Graph """
    # Animate the graph
    # Comment this for fast execution
    """"
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_xlim(0, daysToSimulate)
    ax.set_ylim(0, populationSize)
    ax.set_xlabel('Days')
    ax.set_ylabel('People')
    ax.set_title('COVID-19 Simulation')
    line1, = ax.plot([], [], label='Healthy')
    line2, = ax.plot([], [], label='Sick')
    line3, = ax.plot([], [], label='Recovered')
    line4, = ax.plot([], [], label='Dead')
    ax.legend()

    # radio button for pause/play matplotlib animation
    faceMaskButton_ax = fig.add_axes([0.8, 0.025, 0.1, 0.04])
    # Add a button for resetting the parameters
    reset_button_ax = fig.add_axes([0.8, 0.025, 0.1, 0.04])
    reset_button = Button(reset_button_ax, 'Reset', hovercolor='0.975')


    def reset_button_on_clicked(mouse_event):
        print("Value Changed")
        wearFaceMask = True
        print(wearFaceMask)


    reset_button.on_clicked(reset_button_on_clicked)

    # Add a set of radio buttons for changing color
    axis_color = 'lightgoldenrodyellow'
    color_radios_ax = fig.add_axes([0.025, 0.5, 0.15, 0.15], facecolor=axis_color)
    color_radios = RadioButtons(color_radios_ax, ('red', 'blue', 'green'), active=0)


    def color_radios_on_clicked(label):
        line1.set_color(label)
        fig.canvas.draw_idle()


    color_radios.on_clicked(color_radios_on_clicked)


    def animate(i):
        line1.set_data(dateList[:i], healthy_history[:i])
        line2.set_data(dateList[:i], sick_history[:i])
        line3.set_data(dateList[:i], recovered_history[:i])
        line4.set_data(dateList[:i], dead_history[:i])
        return line1, line2, line3, line4


    ani = animation.FuncAnimation(fig, animate, frames=populationSize, interval=30, blit=True)
    plt.show()

    # export the animation
    ani.save('covid192.gif', writer='ffmpeg', fps=3)
    """

# 100,000 People (Created Person Classes)
# 30% > are senior citizens (65 y > age) (Assign age to each person)
# 20% is children (18 y < age)
# 1 family have 2 - 7  members (Randomize member adding to family)
#
# 40,000 - essential services TODO
#
# Chance of getting infected:
# 	10-20% - Children
# 	15-40% - adults
# 	35-60% - senior
#
# Warning facemask reduce risk by 5-10%
# If 1 fam member get infected, all fam members 40 - 80%
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
"""

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
