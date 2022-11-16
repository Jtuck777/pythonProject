import bcrypt
from bcrypt import gensalt, hashpw, checkpw
import sql_init_login
import DB_User
import time
import datetime
import sqlite3

connection = sqlite3.connect('trains.db')


class Driver:

    def __init__(self, Username):
        self.Driv_Username = Username

    def Driver_Menu(self):
        while True:
            print("------Welcome to the Driver Menu------")
            print('1) Edit Train Schedule'.ljust(30), '2) View Personal Train Schedule')
            print('3) Exit / Log Out')
            choice = input('Selection Input: ')
            if choice.upper() == '1':
                print('Edit Schedule PLace Holder\n')
            if choice.upper() == '2':
                print('View Personal Train Schedule PLace Holder\n')
                self.ViewDriveSchedule(self.Driv_Username)
            if choice.upper() == '3':
                return

    def ViewDriveSchedule(self, D_Username):
        print("Hello ", D_Username)
        print("Please Select Today's Date")
        Driv = connection.cursor()
        Qry = "SELECT DISTINCT TDate FROM TRAIN_SCHEDULE"
        Driv.execute(Qry)
        Dates = Driv.fetchall()
        i = 0
        for row in Dates:
            i += 1
            if i % 2 == 0:
                print("%1d)" % (i), row[0])
            else:
                print("%1d)" % (i), row[0].ljust(20), end="")
        while True:
            choice = input("\nInput Selection:")
            choice = int(choice) - 1
            if choice >= 0 and choice < len(Dates):
                break
            else:
                print("Invalid Input")
        Date_Pick = str(Dates[choice - 1][0])
        Qry = "SELECT * " \
              "FROM (TRAIN_SCHEDULE AS TS LEFT JOIN TRAIN_LINE_INSTANCE AS TLI " \
              "ON TS.TrainNumber = TLI.TrainNumber AND TS.TDate = TLI.TDate) " \
              "WHERE OperatedBy = ? AND TLI.TDate = ?"
        Driv.execute(Qry, (D_Username, Date_Pick))
        Driv_Sched = Driv.fetchall()
        for lines in Driv_Sched:
            print(lines)
        return


class Controller:

    def __init__(self, Username):
        self.Cntr_Username = Username

    def Cntr_Menu(self):
        while True:
            print("------Welcome to the Controller Menu------")
            print('1) Edit Train Schedule'.ljust(30), '2) Edit Train Line Instance')
            print('3) Edit Train Line '.ljust(30), '4) Exit / Log Out')
            choice = input('Selection Input: ')
            if choice.upper() == '1':
                print('Edit Schedule PLace Holder\n')
            if choice.upper() == '2':
                print('Edit Train Line Instance PLace Holder\n')
            if choice.upper() == '3':
                print('Edit Train Line PLace Holder\n')
            if choice.upper() == '4':
                return

    def C_edit_trainLine(self):
        print("Update Train Line Place Holder")

    def C_edit_schedule(self):
        print("UPdate schdule place holder")

    def C_edit_TL_Instance(self):
        print("Update TL Instance placeholder")


class Admin:

    def __init__(self, Username):
        self.Admin_Username = Username

    def Admin_Menu(self):
        while True:
            print("------Welcome to the Admin Menu------")
            print('1) Create New Employee'.ljust(30), '2) Edit Employee Info ')
            print('3) Edit Stations'.ljust(30), '4) Edit Schedule')
            print('5) Edit Train Line Instance'.ljust(30), '6) Edit Train Line')
            print('7) Edit Train Types '.ljust(30), '8) Exit')
            choice = input('Selection Input: ')
            if choice.upper() == '1':
                self.CreateNewEmployee()
            if choice.upper() == '2':
                self.Edit_Employee()
            if choice.upper() == '3':
                editStation()
                print('Edit Stations PLace Holder')
            if choice.upper() == '4':
                print('Edit Schedule PLace Holder')
            if choice.upper() == '5':

                print('Edit Train Line Instance PLace Holder')
            if choice.upper() == '6':
                print('Edit Train Line Place Holder')
                editTrainLines()
            if choice.upper() == '7':
                print('Edit Train Types PLace Holder')
            if choice.upper() == '8':
                print('Exit PLace Holder')
                return

    def CreateNewEmployee(self):
        print("Create New Employee placeholder")
        Flag = True
        UN_Flag = False
        while Flag:
            user_info = []  # username, password, first name, last name, card info
            while UN_Flag is False:
                username, password = prompt()
                UN_Flag = Employee_DB_Check(username)
            user_info.append(username)
            password = hash_pw(password)
            user_info.append(password)
            first_name = input('Enter your first name: ')
            last_name = input('Enter your last name: ')
            user_info.append(first_name)
            user_info.append(last_name)
            print("Enter the Employees Start Date")
            d = GetDate()
            user_info.append(d)
            D = 'Driver'
            C = 'Controller'
            A = 'Admin'
            print("Select Employee Position")
            print("1) Driver 2) Controller 3) Admin")
            choice = int(input("Input Select:"))
            if choice == 1:
                user_info.append(D)
            if choice == 2:
                user_info.append(C)
            if choice == 3:
                user_info.append(A)
            self.insert_Employee(user_info)
            Flag = False

    #####################################################################################3

    def insert_Employee(self, user_info):
        print(user_info)
        cursor = connection.cursor()
        cursor.execute("INSERT INTO EMPLOYEE (Username, HashPass, Fname, Lname, StartDate, JobType)"
                       "VALUES (?,?,?,?,?,?)",
                       (user_info[0], user_info[1], user_info[2], user_info[3], user_info[4], user_info[5])
                       )
        connection.commit()
        return

    def Print_UserInfo(self, EmpUserName):
        cursor = connection.cursor()
        Qry = "SELECT * FROM EMPLOYEE WHERE Username =?"
        cursor.execute(Qry, (EmpUserName,))
        Results = cursor.fetchall()
        print('\nUsername'.ljust(21), 'First Name'.ljust(20), 'Last Name'.ljust(20),
              'StartDate'.ljust(20), 'JobType'.ljust(20))
        print("-----------------------------------------------------------------------------------------")
        print(Results[0][0].ljust(20), Results[0][2].ljust(20), Results[0][3].ljust(20),
              Results[0][4].ljust(20), Results[0][5].ljust(20))

    def Edit_Employee(self):
        print("-------Edit Employee Info Menu--------")
        cursor = connection.cursor()
        Qry = "SELECT * FROM EMPLOYEE"
        cursor.execute(Qry)
        Results = cursor.fetchall()
        i = 0
        print('   Username'.ljust(23), 'First Name'.ljust(20), 'Last Name'.ljust(20),
              'StartDate'.ljust(20), 'JobType'.ljust(20))
        print("-----------------------------------------------------------------------------------------")
        for Result in Results:
            i += 1
            print("%1d)" % (i), Result[0].ljust(20), Result[2].ljust(20), Result[3].ljust(20),
                  Result[4].ljust(20), Result[5].ljust(20))
        print("------------------------------------------------------------------------------------------")
        while True:
            choice = int(input("Enter Number of Employee to Edit: ")) - 1
            if choice < len(Results) and choice >= 0:
                break
            else:
                print(cursor.rowcount)
                continue
        EmpUserName = Results[choice][0]
        user_info = []
        for x in Results[choice]:
            user_info.append(x)

        while True:
            self.Print_UserInfo(EmpUserName)
            print('1) Edit Username'.ljust(25), '2) Edit First Name'.ljust(25), '3) Edit Last Name'.ljust(25))
            print("4) Create New Password".ljust(25), "5) New StartDate".ljust(25), "6) Change Jobtype".ljust(25))
            print("7) Delete Employee".ljust(25), "8) Exit")
            choice = input("Input Selection: ")
            if choice.upper() == '1':
                while True:
                    username = input('Enter a New Username: ')
                    if len(username) >= 4 and len(username) <= 15:
                        break
                    else:
                        print("Invalid Username, try again")
                        continue
                if Employee_DB_Check(EmpUserName):
                    user_info[0] = username

            if choice.upper() == '2':
                while True:
                    F_name = input('Enter a New First Name: ')
                    if len(F_name) >= 1 and len(F_name) <= 15:
                        break
                    else:
                        print("Invalid First name, try again")
                        continue
                user_info[2] = F_name
            if choice.upper() == '3':
                while True:
                    L_name = input('Enter a New Last Name: ')
                    if len(L_name) >= 1 and len(L_name) <= 15:
                        break
                    else:
                        print("Invalid Last name, try again")
                        continue
                user_info[3] = L_name
            if choice.upper() == '4':
                while True:
                    PW = input('Enter a New Password: ')
                    if len(PW) >= 4:
                        PW = hash_pw(PW)
                        break
                    else:
                        print("Invalid Password length, try again")
                        continue
                user_info[1] = PW
            if choice.upper() == '5':
                d = GetDate()
                user_info[4] = d
            if choice.upper() == '6':
                D = 'Driver'
                C = 'Controller'
                A = 'Admin'
                print("1) Driver 2) Controller 3) Admin")
                j = int(input("Select JobType:"))
                if j == 1:
                    user_info[5] = D
                if j == 2:
                    user_info[5] = C
                if j == 3:
                    user_info[5] = A
            if choice.upper() == '7':
                print("Delete Employee")
                Qry = "DELETE FROM EMPLOYEE WHERE Username=?"
                cursor.execute(Qry, (EmpUserName,))
                connection.commit()
                return
            if choice.upper() == '8':
                return
            self.insert_Edited_Emp(user_info, EmpUserName)
            EmpUserName = user_info[0]

    def insert_Edited_Emp(self, user_info, U_Name):
        cursor = connection.cursor()
        cursor.execute("UPDATE EMPLOYEE SET Username=?, HashPass=?, Fname=?, Lname=?, StartDate=?, JobType=?"
                       "WHERE Username =?",
                       (user_info[0], user_info[1], user_info[2], user_info[3], user_info[4], user_info[5],
                        U_Name)
                       )
        connection.commit()
        return

    def edit_trainLine(self):
        print("Update Train Line Place Holder")

    def edit_schedule(self):
        print("UPdate schdule place holder")

    def edit_TL_Instance(self):
        print("Update TL Instance placeholder")


def Employee_DB_Check(Username):
    cursor = connection.cursor()
    rows = cursor.execute("SELECT Username from EMPLOYEE")
    for user in rows:
        if user == Username:
            print("Username is already in use")
            return False
    return True


def Station_DB_Check(StatName):# Returns False if StatName already in DB
    cursor = connection.cursor()
    rows = cursor.execute("SELECT Sname from STATION")
    for stat in rows:
        if stat[0] == StatName:
            print("Station name is already in use")
            return False
    return True

def TL_DB_Check(TL_Name):# Returns False if StatName already in DB
    cursor = connection.cursor()
    rows = cursor.execute("SELECT Sname from STATION")
    for stat in rows:
        if stat[0] == StatName:
            print("Station name is already in use")
            return False
    return True
def Print_StationInfo(StatName):
    cursor = connection.cursor()
    Qry = "SELECT * FROM STATION WHERE Sname =?"
    cursor.execute(Qry, (StatName,))
    Results = cursor.fetchall()
    Qry = "SELECT Distinct LineName FROM STATION natural join Visits WHERE Sname = ?"
    cursor.execute(Qry, (StatName,))
    Results2 = cursor.fetchall()
    print('\nStation Name'.ljust(21), 'Address'.ljust(20), "Visiting Trainlines")
    print("-----------------------------------------------------------------------------------------")
    print(Results[0][0].ljust(20), Results[0][1].ljust(20), end="")
    for result in Results2:
        print("-",result[0], end=" ")
    print("\n")

def insert_Station(Stat_info):
    print(Stat_info)
    cursor = connection.cursor()
    cursor.execute("INSERT INTO STATION (Sname, location)"
                   "VALUES (?,?)",
                   (Stat_info[0], Stat_info[1])
                   )
    connection.commit()
    return

def Update_Station(Stat_info, StatName):
    print(Stat_info)
    cursor = connection.cursor()
    cursor.execute("UPDATE STATION SET Sname=?, location=? WHERE Sname =?",
                    (Stat_info[0], Stat_info[1], StatName)
                   )

    connection.commit()
    return

def prompt():
    while True:
        username = input('Enter a username: ')
        password = input('Enter a password: ')
        if len(username) >= 4 and len(username) <= 15 and len(password) >= 4:
            break
        else:
            continue
    return username, password


def hash_pw(password):
    print(password)
    Byte_PW = bytes(password, 'utf-8')
    return bcrypt.hashpw(Byte_PW, bcrypt.gensalt())


def GetDate():
    year = int(input('Enter a year: '))
    month = int(input('Enter a month: '))
    day = int(input('Enter a day: '))
    if year < 2000 or year > 9999:
        print("Invalid year")
        return GetDate()
    if month < 1 or month > 12:
        print("Invalid month")
        return GetDate()
    if day < 1 or day > 31:
        print("Invalid Day")
        return GetDate()
    testeddate = str(year) + '-' + str(month) + '-' + str(day)
    dt_obj = datetime.datetime.strptime(testeddate, '%Y-%m-%d')
    return datetime.datetime.strftime(dt_obj, '%Y-%m-%d')


def Invalid_Input():
    choice = input("Press 1 to try again or 2 to return to main menu\n")
    if choice.upper == '1':
        return True
    else:
        return False


def editStation():
    print("-------Edit Station Info Menu--------")
    cursor = connection.cursor()
    Qry = "SELECT * FROM STATION"
    cursor.execute(Qry)
    Results = cursor.fetchall()
    i = 1
    print('   Station'.ljust(23), 'Location'.ljust(20))
    print("-----------------------------------------------------------------------------------------")

    for Result in Results:
        print("%1d)" % (i), Result[0].ljust(20), Result[1].ljust(20))
        i += 1
    print("------------------------------------------------------------------------------------------")
    print("%1d)" % (i), "Create a New Station")
    print("%1d)" % (i+1), "Exit")
    print("------------------------------------------------------------------------------------------")
    while True:
        choice = int(input("Select Station or Operation number: ")) - 1
        if choice <= len(Results)+1 and choice >= 0:
            break
        else:
            print(cursor.rowcount)
            continue
########################Create NEW STATION###############################
    if choice >= len(Results):
        if choice == len(Results)+1:
            return
        NewStation = []
        while True:
            StatName = input('Enter a New Station Name: ')
            if len(StatName) >= 4 and len(StatName) <= 15 and Station_DB_Check(StatName):
                NewStation.append(StatName)
                break
            else:
                print("Invalid Station name, try again")
                continue

        while True:
            StatAddr = input('Enter a New Station Address: ')
            if len(StatAddr) >= 4:
                break
            else:
                print("Invalid Station Addr, try again")
                continue
        NewStation.append(StatAddr)
        Qry = "SELECT DISTINCT LineName FROM TRAIN_LINE"
        cursor.execute(Qry)
        Results = cursor.fetchall()
        for Result in Results:
            while True:
                MSG ="Is this station visited by "+ Result[0]+ " (Y/N):"
                YN = input(MSG)
                if YN == "y" or YN == "Y":
                    cursor.execute("INSERT INTO Visits (LineName, Sname) VALUES (?,?)"
                   , (Result[0], StatName))
                    break
                elif YN == 'N' or YN == "n":
                    break
                else:
                    print("Invalid Input please enter Y or N")
                    continue

        insert_Station(NewStation)
        return
    else:
        Stat_info = []
        for x in Results[choice]:
            Stat_info.append(x)
        StatName = Stat_info[0]
        while True:
            Print_StationInfo(StatName)
            print('1) Edit Station Name'.ljust(25), '2) Edit Address'.ljust(25), '3) Delete Station'.ljust(25))
            print("4) Exit")
            choice = input("Input Selection: ")
            if choice.upper() == '1':
                while True:
                    NewStatName = input('Enter a New Station Name: ')
                    if len(StatName) >= 4 and len(StatName) <= 15 and Station_DB_Check(NewStatName):
                        Stat_info[0] = NewStatName
                        break
                    else:
                        print("Invalid Station name, try again")
                        continue
            if choice.upper() == '2':
                while True:
                    StatAddr = input('Enter a New Station Address: ')
                    if len(StatAddr) >= 4:
                        break
                    else:
                        print("Invalid Station Addr, try again")
                        continue
                Stat_info[1] = StatAddr
            if choice.upper() == '3':
                print("Delete Station")
                Qry = "DELETE FROM STATION WHERE Sname=?"
                cursor.execute(Qry, (StatName,))
                connection.commit()
                return
            if choice.upper() =='4':
                return
            Update_Station(Stat_info, StatName)
            StatName = Stat_info[0]


def editTrainLines():
    print("-------Edit Train Lines Info Menu--------")
    cursor = connection.cursor()
    Qry = "SELECT LineName FROM TRAIN_LINE"
    cursor.execute(Qry)
    Results = cursor.fetchall()
    i = 1
    print('   Train Lines'.ljust(23))
    for Result in Results:

        if i % 2 == 0:
            print("%1d)" % (i), Result[0]),
        else:
            print("%1d)" % (i), Result[0].ljust(20), end=' ')
        i += 1
    print("------------------------------------------------------------------------------------------")
    print("%1d)" % (i), "Create a New Station")
    print("%1d)" % (i + 1), "Exit")
    print("------------------------------------------------------------------------------------------")
    while True:
        choice = int(input("Select TrainLine or Operation number: ")) - 1
        if choice <= len(Results) + 1 and choice >= 0:
            break
        else:
            print("Invalid Input Please try again")
            continue
    if choice >= len(Results):
        if choice == len(Results) + 1:
            return
        NewTrainLine = []
        while True:
            TL_Name = input('Enter a New Train Line Name: ')
            if len(TL_Name) >= 4 and len(TL_Name) <= 15 and TL_DB_Check(TL_Name):
                NewTrainLine.append(TL_Name)
                break
            else:
                print("Invalid Train Line name, try again")
                continue

        while True:
            StatAddr = input('Enter a New Station Address: ')
            if len(StatAddr) >= 4:
                break
            else:
                print("Invalid Station Addr, try again")
                continue
        NewTrainLine.append(StatAddr)
        Qry = "SELECT DISTINCT LineName FROM TRAIN_LINE"
        cursor.execute(Qry)
        Results = cursor.fetchall()
        for Result in Results:
            while True:
                MSG = "Is this station visited by " + Result[0] + " (Y/N):"
                YN = input(MSG)
                if YN == "y" or YN == "Y":
                    cursor.execute("INSERT INTO Visits (LineName, Sname) VALUES (?,?)"
                                   , (Result[0], StatName))
                    break
                elif YN == 'N' or YN == "n":
                    break
                else:
                    print("Invalid Input please enter Y or N")
                    continue

        insert_Station(NewTrainLine)
        return
    else: