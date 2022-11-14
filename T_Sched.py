from datetime import timedelta

import bcrypt
from bcrypt import gensalt, hashpw, checkpw
import sql_init_login
import DB_User
import time
import datetime
import sqlite3

connection = sqlite3.connect('trains.db')
cursor = connection.cursor()
# user_actions[i] = (username, action)
# if not logged in, don't track this (or just use 'guest')
user_actions = []


class Schedules:
    def train_schedules(self):
        SCHED = connection.cursor()
        SCHED.execute("SELECT Distinct SName FROM STATION")
        Station = SCHED.fetchall()
        i = 0
        print("\nTo see a Schedule Select a Station")
        for row in Station:
            i += 1
            if i % 2 == 0:
                print("%1d)" % (i), row[0]),
            else:
                print("%1d)" % (i), row[0].ljust(20), end=' ')
        choice = input("\nInput Selection:")
        choice = int(choice)
        if choice > 8 or choice < 1:
            self.train_schedules()
            return
        Stat_Pick = str(Station[choice - 1][0])
        Qry = "SELECT TrainNumber, TDate, PlannedArrivalTime " \
              "FROM TRAIN_SCHEDULE WHERE SName=?"
        print(Stat_Pick)
        SCHED.execute(Qry, (Stat_Pick,))
        T_Schedule = SCHED.fetchall()
        print("Train #    Arrival Time   Departure Time     Date")

        for lines in T_Schedule:
            D_Time = datetime.datetime.strptime(lines[2], '%H:%M:%S') + datetime.timedelta(minutes=2)
            print(str(lines[0]).ljust(10), str(lines[2]).ljust(20), D_Time.strftime('%H:%M:%S').ljust(20))

        if Input() is True:
            print("FLAG")
            self.train_schedules()
        return


def Input():
    choice = input("\n - Press 1 to choose a different Station\n "
                   "- Press any key to return to main menu\n")
    if choice.upper == '1':
        return True
    else:
        return False
