import pandas as pd
import random as ran
import os

cat1 = [None]*1500001
cat2 = [None]*1500001
cat3 = [None]*1500001
cat4 = [None]*1500001
cat5 = [None]*1500001
cat6 = [None]*1500001
cat7 = [None]*1500001
cat8 = [None]*1500001
cat9 = [None]*1500001
cat10 = [None]*1500001

# KWh discharge per 5 mins
rate = 5 / 60


class car():

    def __init__(self, id, capacity, soc, percent):
        self.id = id
        # capacity/soc in kwh
        self.capacity = capacity
        self.soc = soc
        self.percent = percent
        self.cat = 0
        self.recat()

    def recat(self):
        if self.percent < 0.1:
            self.cat = 0.1
        elif self.percent < 0.2:
            self.cat = 0.2
        elif self.percent < 0.3:
            self.cat = 0.3
        elif self.percent < 0.4:
            self.cat = 0.4
        elif self.percent < 0.5:
            self.cat = 0.5
        elif self.percent < 0.6:
            self.cat = 0.6
        elif self.percent < 0.7:
            self.cat = 0.7
        elif self.percent < 0.8:
            self.cat = 0.8
        elif self.percent < 0.9:
            self.cat = 0.9
        else:
            self.cat = 1

    def charge(self):
        self.soc += 250 * rate
        self.percent = self.soc / self.capacity
        if self.percent > self.cat:
            self.recat()

    def discharge(self):
        self.soc -= 25 * rate
        self.percent = self.soc / self.capacity
        if self.percent > self.cat:
            self.recat()

    def checkState(self):
        return self.percent

    def setPercent(self, p):
        self.percent = p


def createCars():
    i = 0

    while (i < 1500000):

        r = ran.random()

        if r < 0.5:
            capacity = 60
        elif r < 0.85:
            capacity = 70
        else:
            capacity = 100

        r = ran.random()

        soc = capacity * r

        c = car(i, capacity, soc, r)

        if r < 0.1:
            cat1[i] = c
        elif r < 0.2:
            cat2[i] = c
        elif r < 0.3:
            cat3[i] = c
        elif r < 0.4:
            cat4[i] = c
        elif r < 0.5:
            cat5[i] = c
        elif r < 0.6:
            cat6[i] = c
        elif r < 0.7:
            cat7[i] = c
        elif r < 0.8:
            cat8[i] = c
        elif r < 0.9:
            cat9[i] = c
        else:
            cat10[i] = c

        i += 1


def average_soc():
    total = 0
    for bat in cat1:
        if bat != None:
            total += bat.percent
    for bat in cat2:
        if bat != None:
            total += bat.percent
    for bat in cat3:
        if bat != None:
            total += bat.percent
    for bat in cat4:
        if bat != None:
            total += bat.percent
    for bat in cat5:
        if bat != None:
            total += bat.percent
    for bat in cat6:
        if bat != None:
            total += bat.percent
    for bat in cat7:
        if bat != None:
            total += bat.percent
    for bat in cat8:
        if bat != None:
            total += bat.percent
    for bat in cat9:
        if bat != None:
            total += bat.percent
    for bat in cat10:
        if bat != None:
            total += bat.percent
    return total/1500000

# del cat1[1]
def over(by_how_much):
    excess = by_how_much * 1000

    print("Excess: " + str(excess))

    while excess > 0:
        #print("Excess: " + str(excess))

        for bat in cat6:
            #print("battery")
            if bat == None:
                continue
            battery = bat
            battery.charge()
            excess = excess - (50*rate)
            #print("Excess: " + str(excess))
            if battery.cat != 0.6:
                #print(battery.id)
                cat6[battery.id] = None
                cat7[battery.id] = battery
        break


def under(by_how_much):
    shortage = by_how_much * 1000

    print("Shortage: " + str(shortage))

    while shortage > 0:
        print("Shortage: "+str(shortage))
        for bat in cat10:
            if bat == None:
                continue
            battery = bat
            battery.discharge()
            shortage -= (25*rate)
            if battery.cat != 1:
                cat10[battery.id] = None
                cat9[battery.id] = battery
            if shortage <= 0:
                break
        for bat in cat9:
            if bat == None:
                continue
            battery = bat
            battery.discharge()
            shortage -= (25 * rate)
            if battery.cat != 0.9:
                cat9[battery.id] = None
                cat8[battery.id] = battery
            if shortage <= 0:
                break
        for bat in cat8:
            if bat == None:
                continue
            battery = bat
            battery.discharge()
            shortage -= (25 * rate)
            if battery.cat != 0.8:
                cat8[battery.id] = None
                cat7[battery.id] = battery
            if shortage <= 0:
                break
        for bat in cat7:
            if bat == None:
                continue
            battery = bat
            battery.discharge()
            shortage -= (25 * rate)
            if battery.cat != 0.7:
                cat7[battery.id] = None
                cat6[battery.id] = battery
            if shortage <= 0:
                break
        for bat in cat6:
            if bat == None:
                continue
            battery = bat
            battery.discharge()
            shortage -= (25 * rate)
            if battery.cat != 0.6:
                cat6[battery.id] = None
                cat5[battery.id] = battery
            if shortage <= 0:
                break


if __name__ == '__main__':

    createCars()

    print(average_soc())

    # , index_col = "Time"

    # print("PYTHONPATH:", os.environ.get('PYTHONPATH'))

    df = pd.read_csv('CAISO-demand-20230403.csv')
    # print(type(df))
    # print(df.to_string)
    # print(df.loc[:,"Time"])

    for row in df.iterrows():
        # supply/demand are in MW. 1 MW = 1000 KW
        # assuming supply is 25,000 and constant
        # print(row[1]["Time"])
        difference = 25000 - row[1]["Demand"]
        print(row[1]["Time"])
        if difference > 10:
            over(difference)
        elif difference < 100:
            under(difference)

    print(average_soc())

    quit()
