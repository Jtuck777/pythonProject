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
            if choice.upper() == '3':
                return

    def ViewDriveSchedule(self):
        print("Hello ", self.Driv_Username)
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
                print("%1d)" % (i), row[0].ljust(20))
        choice = input("\nInput Selection:")
        choice = int(choice)
        if choice < 0 or choice > Driv.rowcount:
            self.Select_Date()
            return
        Date_Pick = str(Dates[choice - 1][0])
        Qry = "SELECT * " \
              "FROM (TRAIN_SCHEDULE AS TS LEFT JOIN TRAIN_LINE_INSTANCE AS TLI " \
              "ON TS.TrainNumber = TLI.TrainNumber AND TS.TDate = TLI.TDate) " \
              "WHERE OperatedBy = ? AND TDate = ?"
        Driv.execute(Qry, self.Driv_Username, Date_Pick)
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
                print('Edit Stations PLace Holder')
            if choice.upper() == '4':
                print('Edit Schedule PLace Holder')
            if choice.upper() == '5':
                print('Edit Train Line Instance PLace Holder')
            if choice.upper() == '6':
                print('Edit Employee Info PLace Holder')
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
                    user_info[5]=D
                if j == 2:
                    user_info[5]=C
                if j == 3:
                    user_info[5]=A
            if choice.upper() == '7':
                print("Delete Employee")
                Qry ="DELETE FROM EMPLOYEE WHERE Username=?"
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
