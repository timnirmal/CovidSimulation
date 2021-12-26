import random
from matplotlib import pyplot as plt, animation

populationSize = 1000
daysToSimulate = 100
familySizeMin = 2
familySizeMax = 7
fatalityRate = 0.1
wearFaceMask = False
travelRestrictions = False
factor = 1.2


class Person:
    __lastId = 1

    def __init__(self, status):
        self.id = Person.__lastId
        Person.__lastId += 1

        self.age = None
        self.status = status
        self.infectedDate = None
        self.time_sick = 0
        self.family_id = 0
        self.essentialWorker = False
        self.time_immune = 0
        self.time_immune_left = 0

    def get_id(self):
        return self.id

    def set_age(self, age):
        self.age = age

    def get_age(self):
        return self.age

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

    def add_member(self, member):
        self.members.append(member)

    def get_member_count(self):
        return len(self.members)

    def get_family_id(self):
        return self.id

    def get_family_infected(self):
        return self.familyInfected

    def set_family_infected(self, infected):
        self.familyInfected = infected


def person_simulation():
    # int variables for count
    healthy = 0
    sick = 0
    recovered = 0
    hospitalized = 0
    dead = 0
    personNumber = 0  # For 1st date

    dateList.append(dateList[-1] + 1)

    # Number of Deaths for that day = 0.001 * Number of Positive for that day
    # get last data from infected history
    n = (populationSize - healthy_history[-1]) * fatalityRate
    total_deaths = dead_history[-1]

    if n > 0 and total_deaths > 0 and day > 12:
        total_deaths = int(n - total_deaths)
        if total_deaths < 0:
            total_deaths = 0
    else:
        total_deaths = 0

    for person in personList:
        # get persons family id and get family from familyList
        family = familyList[person.get_family_id() - 1]

        if person.status == 'infected' and person.time_sick < 5:
            person.time_sick += 1
            family.set_family_infected(True)
        elif person.status == 'infected' and person.time_sick == 5:
            family.set_family_infected(False)
            person.status = 'hospitalized'
            person.time_sick += 1
        elif person.status == 'hospitalized' and person.time_sick < 15:
            family.set_family_infected(False)
            person.status = 'hospitalized'
            person.time_sick += 1
        elif person.status == 'hospitalized' and person.time_sick == 15:
            family.set_family_infected(False)
            # Dead or Alive
            if total_deaths > 0 and random.random() < 0.09:
                person.status = 'dead'
                total_deaths -= 1
            elif total_deaths <= 0 and random.random() < 0.05:
                person.status = 'dead'
                total_deaths -= 1
            else:
                person.status = 'recovered'
                person.time_immune = random.randint(180, 210)

        if person.status == 'recovered' and person.time_immune > 0:
            person.time_immune_left -= 1
        if person.status == 'recovered' and person.time_immune <= 0:
            person.status = 'healthy'

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

            # Update person as infected
            if random.random() * factor < chance_of_infection:
                person.status = 'infected'
                family.set_family_infected(True)
                personNumber += 1

            if day == 0 and personNumber == 1:
                return update(dead, healthy, personList, recovered, sick, hospitalized)

    return update(dead, healthy, personList, recovered, sick, hospitalized)


def update(dead, healthy, personList, recovered, sick, hospitalized):
    for person in personList:
        if person.status == 'healthy':
            healthy += 1
        elif person.status == 'infected':
            sick += 1
        elif person.status == 'recovered':
            recovered += 1
        elif person.status == 'hospitalized':
            hospitalized += 1
        else:
            dead += 1

    healthy_history.append(healthy)
    sick_history.append(sick)
    recovered_history.append(recovered)
    dead_history.append(dead)
    hospitalized_history.append(hospitalized)
    return dead, healthy, recovered, sick, hospitalized


if __name__ == '__main__':
    print("\nCovid-19 Simulation\n")

    # inputs
    print("Fill these values to do the simulation. \n"
          "If you dont need to add do changes enter number of days you do the simulations as the input\n")
    wearFaceMaskAt = int(input("\tEnforce Facemask Wear at day : "))
    enforceTravelRestrictionsAt = int(input("\tEnforce Travel Restrictions At : "))
    liftTravelRestrictionsAt = int(input("\tLift Travel Restrictions At : "))

    personList: list[Person] = []

    for i in range(populationSize):
        personList.append(Person('healthy'))

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

    ######################################################################
    """ Simulation """
    print("\nDay   Healthy   Sick  Recovered   Dead Hospitalized")

    n_healthy = populationSize - 1
    n_sick = 1

    # Daily History
    healthy_history: list[int] = [n_healthy]
    sick_history: list[int] = [n_sick]
    hospitalized_history: list[int] = [0]
    recovered_history = [0]
    dead_history = [0]
    dateList: list[int] = [0]

    for day in range(daysToSimulate):
        if wearFaceMaskAt < day:
            wearFaceMask = True
        else:
            wearFaceMask = False

        if enforceTravelRestrictionsAt <= day <= liftTravelRestrictionsAt:
            travelRestrictions = True
        else:
            travelRestrictions = False

        dead, healthy, recovered, sick, hospitalized = person_simulation()

        print(
            " " + str(day + 1) + "\t\t" + str(healthy) + "\t\t" + str(sick) + "\t\t" + str(recovered) + "\t\t\t" + str(
                dead) + "\t\t" + str(hospitalized))

    ######################################################################
    """ Clear Data Set """

    # remove first element from list
    dateList.pop(0)
    healthy_history.pop(0)
    sick_history.pop(0)
    recovered_history.pop(0)
    dead_history.pop(0)
    hospitalized_history.pop(0)

    ######################################################################
    """ Graph """

    # Plot the data
    plt.plot(dateList, healthy_history, label='Healthy')
    plt.plot(dateList, sick_history, label='infected')
    plt.plot(dateList, recovered_history, label='Recovered')
    plt.plot(dateList, dead_history, label='Dead')
    plt.plot(dateList, hospitalized_history, label='Hospitalized')
    plt.xlabel('Days')
    plt.ylabel('People')
    plt.title('COVID-19 Simulation')
    plt.legend()
    plt.show()

    ######################################################################
    """ Animated Graph """
    # Animate the graph
    # Comment this for fast execution

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_xlim(0, daysToSimulate)
    ax.set_ylim(0, populationSize)
    ax.set_xlabel('Days')
    ax.set_ylabel('People')
    ax.set_title('COVID-19 Simulation')
    line1, = ax.plot([], [], label='Healthy')
    line2, = ax.plot([], [], label='infected')
    line3, = ax.plot([], [], label='Recovered')
    line4, = ax.plot([], [], label='Dead')
    line5, = ax.plot([], [], label='Hospitalized')
    ax.legend()


    def animate(i):
        line1.set_data(dateList[:i], healthy_history[:i])
        line2.set_data(dateList[:i], sick_history[:i])
        line3.set_data(dateList[:i], recovered_history[:i])
        line4.set_data(dateList[:i], dead_history[:i])
        line5.set_data(dateList[:i], hospitalized_history[:i])
        return line1, line2, line3, line4, line5


    # Show Animation
    ani = animation.FuncAnimation(fig, animate, frames=populationSize, interval=30, blit=True)
    plt.show()

    # Export the Animation
    ani.save('covid19.gif', writer='ffmpeg', fps=30)

# https://github.com/timnirmal/CovidSimulation/
# 100,000 People (Created Person Classes)
# 30% > are senior citizens (65 y > age) (Assign age to each person)
# 20% is children (18 y < age)
# 1 family have 2 - 7  members (Randomize member adding to family)
#
# 40,000 - essential services
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
