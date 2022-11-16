from bcrypt import gensalt, hashpw, checkpw
import sql_init_login
import DB_User
import datetime
import sqlite3

connection = sqlite3.connect('trains.db')
cursor = connection.cursor()
# user_actions[i] = (username, action)
# if not logged in, don't track this (or just use 'guest')
user_actions = []


class Schedules:
    def schedule_menu(self):
        while True:
            print('\n-----Select A Schedule Type-----')
            print('1) Station Schedule       2) Train Schedule '
                  '\n3) Train Line Information 4) Exit')
            choice = input('Selection Input: ')

            if choice.upper() == '1':
                self.station_schedule()
                continue
            elif choice.upper() == '2':
                self.train_schedule()
                continue
            elif choice.upper() == '3':
                self.train_line_info()
                continue
            elif choice.upper() == '4':
                break
            else:
                print('Invalid option!')
        return

    def station_schedule(self):
        # Select Station
        SCHED = connection.cursor()
        SCHED.execute("SELECT Distinct SName FROM STATION")
        T_Station = SCHED.fetchall()
        print("\n-----Select a Station-----")
        if self.list_options(T_Station, 20) is False:
            return
        choice = self.get_option_selection(len(T_Station))
        Stat_Pick = str(T_Station[choice - 1][0])

        # Get Selected Station Information
        Qry = "SELECT distinct TDate FROM TRAIN_SCHEDULE WHERE SName=? ORDER BY TDate ASC"
        SCHED.execute(Qry, (Stat_Pick,))
        T_Dates = SCHED.fetchall()

        # Get Date
        print("\n-----Select a Date-----")
        if len(T_Dates)==0:
            print("No Available Dates for this Station")
            return
        self.list_options(T_Dates, 12)
        choice = self.get_option_selection(len(T_Dates))
        Date_Pick = str(T_Dates[choice - 1][0])

        # Get Station Schedule
        Qry = "SELECT S.TrainNumber, I.LineName, S.PlannedArrivalTime " \
              "FROM TRAIN_SCHEDULE S NATURAL JOIN TRAIN_LINE_INSTANCE I " \
              "WHERE S.SName=? AND S.TDate=? " \
              "ORDER BY S.TrainNumber ASC"
        SCHED.execute(Qry, (Stat_Pick, Date_Pick))
        T_Schedule = SCHED.fetchall()

        # Print Schedule
        print("\n-----", Stat_Pick, "Schedule On", Date_Pick, "-----")
        print("Train #   Train Line   Arrival Time   Departure Time")
        for lines in T_Schedule:
            # D_Time is the planned arrival time, but 2 minutes later
            D_Time = datetime.datetime.strptime(lines[2], '%H:%M:%S') + datetime.timedelta(minutes=2)
            print(str(lines[0]).ljust(9), str(lines[1]).ljust(12), str(lines[2]).ljust(14),
                  D_Time.strftime('%H:%M:%S').ljust(14))

        # Ask if user wants to see a new station schedule
        print("\nWould you like to choose a different station?")
        while True:
            choice = input("Y or N: ")
            if choice.upper() == 'Y':
                self.station_schedule()
                return
            elif choice.upper() == 'N':
                return

    def train_schedule(self):
        # Query train lines
        SCHED = connection.cursor()
        SCHED.execute("SELECT distinct LineName FROM TRAIN_LINE")
        T_Train_Lines = SCHED.fetchall()

        # Get train line from user
        print("\n-----Select a Train Line-----")
        if len(T_Train_Lines)==0:
            print("No Available Stations for this Train Line")
            return
        self.list_options(T_Train_Lines, 15)
        choice = self.get_option_selection(len(T_Train_Lines))
        Line_Pick = str(T_Train_Lines[choice - 1][0])

        # Query train numbers
        Qry = "SELECT distinct TrainNumber FROM TRAIN_LINE_INSTANCE WHERE LineName=?"
        SCHED.execute(Qry, (Line_Pick,))
        T_Train_Nums = SCHED.fetchall()

        # Get train number from user
        print("\n-----Select a Train Number-----")
        if len(T_Train_Nums)==0:
            print("No Available Dates for this Train Line ")
            return
        self.list_options(T_Train_Nums, 15)
        choice = self.get_option_selection(len(T_Train_Nums))
        Num_Pick = str(T_Train_Nums[choice - 1][0])

        # Query dates
        Qry = "SELECT distinct TDate FROM TRAIN_LINE_INSTANCE WHERE LineName=? AND TrainNumber=?"
        SCHED.execute(Qry, (Line_Pick, Num_Pick))
        T_Dates = SCHED.fetchall()

        # Get date from user
        print("\n-----Select a Date-----")
        self.list_options(T_Dates, 12)
        choice = self.get_option_selection(len(T_Dates))
        Date_Pick = str(T_Dates[choice - 1][0])

        # Get Train Schedule
        Qry = "SELECT S.SName, S.PlannedArrivalTime " \
              "FROM TRAIN_SCHEDULE S NATURAL JOIN TRAIN_LINE_INSTANCE I " \
              "WHERE I.LineName=? AND S.TrainNumber=? AND S.TDate=? " \
              "ORDER BY S.PlannedArrivalTime ASC"
        SCHED.execute(Qry, (Line_Pick, Num_Pick, Date_Pick))
        T_Schedule = SCHED.fetchall()

        # Print Schedule
        print("\n-----", Line_Pick, Num_Pick, "On", Date_Pick, "-----")
        print("Station             Arrival Time   Departure Time")
        for lines in T_Schedule:
            # D_Time is the planned arrival time, but 2 minutes later
            D_Time = datetime.datetime.strptime(lines[1], '%H:%M:%S') + datetime.timedelta(minutes=2)
            print(str(lines[0]).ljust(19), str(lines[1]).ljust(14), D_Time.strftime('%H:%M:%S').ljust(14))

        # Ask if user wants to see a new train schedule
        print("\nWould you like to choose a different train?")
        while True:
            choice = input("Y or N: ")
            if choice.upper() == 'Y':
                self.train_schedule()
                return
            elif choice.upper() == 'N':
                return

    def train_line_info(self):
        # Query train lines
        SCHED = connection.cursor()
        SCHED.execute("SELECT distinct LineName FROM TRAIN_LINE")
        T_Train_Lines = SCHED.fetchall()

        # Get train line from user
        print("\n-----Select a Train Line-----")
        self.list_options(T_Train_Lines, 15)
        choice = self.get_option_selection(len(T_Train_Lines))
        Line_Pick = str(T_Train_Lines[choice - 1][0])

        # Print basic information
        Qry = "SELECT LineColor, StartStation, EndStation FROM TRAIN_LINE WHERE LineName=?"
        SCHED.execute(Qry, (Line_Pick,))
        T_Line = SCHED.fetchall()
        print("\n-----Line Information-----")
        print("         Line:", Line_Pick)
        print("        Color:", T_Line[0][0])
        print("Start Station:", T_Line[0][1])
        print("  End Station:", T_Line[0][2])

        # Print stations visited
        Qry = "SELECT SName FROM VISITS WHERE LineName=?"
        SCHED.execute(Qry, (Line_Pick,))
        T_Stats = SCHED.fetchall()
        print("\n-----Station Visited-----")
        for i, row in enumerate(T_Stats, start=1):
            if i % 2 == 0:
                print(row[0]),
            else:
                print(str(row[0]).ljust(20), end=' ')
        if i % 2 == 1:
            print()

        # Print line numbers
        Qry = "SELECT distinct TrainNumber FROM TRAIN_LINE_INSTANCE WHERE LineName=?"
        SCHED.execute(Qry, (Line_Pick,))
        T_Line_Nums = SCHED.fetchall()
        print("\n-----Train Numbers-----")
        for i, row in enumerate(T_Line_Nums, start=1):
            if i % 2 == 0:
                print(row[0]),
            else:
                print(str(row[0]).ljust(15), end=' ')
        if i % 2 == 1:
            print()

        # Ask if user wants to see a new train line
        print("\nWould you like to choose a different train line?")
        while True:
            choice = input("Y or N: ")
            if choice.upper() == 'Y':
                self.train_line_info()
                return
            elif choice.upper() == 'N':
                return

    def list_options(self, list, just):

        for i, row in enumerate(list, start=1):
            if i % 2 == 0:
                print("%1d)" % (i), row[0]),
            else:
                print("%1d)" % (i), str(row[0]).ljust(just), end=' ')
        if i % 2 == 1:
            print()
    def get_option_selection(self, list_len):
        while True:
            choice = input("Input Selection: ")
            choice = int(choice)
            if choice <= list_len and choice > 0:
                return choice


if __name__ == "__main__":
    schedule_obj = Schedules()
    schedule_obj.schedule_menu()