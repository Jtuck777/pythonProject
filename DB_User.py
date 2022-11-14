"""
SJSU CMPE138 Team5 Project
"""
import sys

import bcrypt
from bcrypt import gensalt, hashpw, checkpw
import sqlite3
import datetime
import Employees

connection = sqlite3.connect('trains.db')


class NewUser:
    def create_user(self):
        Flag = True
        UN_Flag = False
        while Flag:
            user_info = []  # username, password, first name, last name, card info
            while UN_Flag is False:
                username, password = prompt()
                UN_Flag = NewPass_Username_DB_Check(username)
            user_info.append(username)
            password = hash_pw(password)
            user_info.append(password)
            user_info = self.New_Passenger_info(user_info)
            self.insert_user(user_info)
            Flag = False
        print('Account successfully created! Please login now.')
        return

    def New_Passenger_info(self, user_info):
        while True:
            # len(first_name), len(last_name) == 15
            first_name = input('Enter your first name: ')
            last_name = input('Enter your last name: ')
            user_info.append(first_name)
            user_info.append(last_name)
            cc_number = str(input('Enter your credit card number: '))
            if len(cc_number) == 16 and cc_number.isnumeric():
                user_info.append(cc_number)
                print('Expiration dates are in the form "MMYY".')
                exp_date = str(input('Enter your card\'s expiration date: '))
                if len(exp_date) == 4 and exp_date.isnumeric():
                    user_info.append(exp_date)
                    cvc = str(input('Enter the CCV: '))
                    if len(cvc) == 3 and cvc.isnumeric():
                        user_info.append(cvc)
                        break
                    else:
                        print('Bad CVC!')
                        continue
                # cvc (int), expdate (date, need to format this somehow)
                else:
                    print('Bad expiration date!')
                    continue
            else:
                print('Bad card info!')
                continue
        return user_info

    def insert_user(self, user_info):
        cursor = connection.cursor()
        cursor.execute("INSERT INTO PASSENGER (Username, HashPass, Fname, Lname, CardNum, ExpData, CVC)"
                       "VALUES (?,?,?,?,?,?,?)",
                       (
                           user_info[0], user_info[1], user_info[2], user_info[3], user_info[4], user_info[5],
                           user_info[6])
                       )
        connection.commit()
        return


##############################################################################################################

class Passenger:
    P_Username = ""

    def Pass_Login(self):

        username, password = prompt()
        if self.Pass_Credential_Check(username, password) is not True:
            if Invalid_Input():
                self.Pass_Login()
            else:
                return
        self.P_Username = username
        print("Passenger Username: ", self.P_Username)
        return

    def Pass_Menu(self):
        while True:
            print("\n-----Welcome to the Passenger Menu------")
            choice = input("1) Buy a Ticket       2) View Purchased Tickets "
                           "\n3) View Personal Info 4) Edit Personal Info "
                           "\n5) Logout\nSelection Input:")
            if choice.upper() == "1":
                print("BUY TICKET\n")
                continue
            if choice.upper() == "2":
                self.ViewTickets()
                continue
            if choice.upper() == "3":
                print("VIEW PERSONAL INFO\n")
                self.Print_UserInfo()
                continue
            if choice.upper() == "4":
                while True:
                    if self.Edit_Info() is True:
                        break

                print("EDIT PERSONAL INFO")
                continue
            if choice.upper() == "5":
                print("LOG OUT")
                break
        return

    def Pass_Credential_Check(self, Username, password):
        cursor = connection.cursor()
        Qry = "SELECT Username from PASSENGER  WHERE Username =?"
        cursor.execute(Qry, (Username,))
        Result = cursor.fetchall()
        if len(Result) <= 0:
            print("This Username does not Exist\n")
            return False
        Qry = "SELECT HashPass, Fname from PASSENGER  WHERE Username =?"
        cursor.execute(Qry, (Username,))
        rows = cursor.fetchall()
        H_password = bytes(password, encoding='utf-8')
        for row in rows:
            if checkpw(H_password, row[0]):
                print("\nLog in Successful, Hello ", row[1])
                return True
        return False

    def Print_UserInfo(self):
        cursor = connection.cursor()
        Qry = "SELECT * FROM PASSENGER WHERE Username =?"
        cursor.execute(Qry, (self.P_Username,))
        Result = cursor.fetchall()
        print("------------------------Current User Info------------------------------")
        print('1) Username'.ljust(20), '2) First Name'.ljust(20), '3) Last Name'.ljust(20))
        print(Result[0][0].ljust(20), Result[0][2].ljust(20), Result[0][3].ljust(20))
        print('\n4) CreditCard #'.ljust(20), '5) Exp. Date'.ljust(20), '6) CVC'.ljust(20))
        print(Result[0][4].ljust(20), Result[0][5].ljust(20), Result[0][6].ljust(20))
        print("--------------------------------------------------------------------------")
        return

    def ViewTickets(self):
        cursor = connection.cursor()
        Qry = "SELECT * FROM TICKET WHERE OwnerUser =?"
        cursor.execute(Qry, (self.P_Username,))
        Results = cursor.fetchall()
        i = 0
        print('\nTicket #'.ljust(10), 'Departure Station'.ljust(20), 'Arrival Station'.ljust(20),
              'Purchase Date'.ljust(20))
        print("------------------------------------------------------------------")
        for Lines in Results:
            print(str(Lines[0]).ljust(10), Lines[3].ljust(20), Lines[2].ljust(20), Lines[1].ljust(20))


    def Edit_Info(self):
        cursor = connection.cursor()
        Qry = "SELECT * FROM PASSENGER WHERE Username =?"
        cursor.execute(Qry, (self.P_Username,))
        Result = cursor.fetchall()
        user_info = []
        print(self.P_Username)
        for item in Result[0]:
            user_info.append(item)
        print("-------Edit User Info Menu--------")
        self.Print_UserInfo()
        print('1) Edit Username'.ljust(25), '2) Edit First Name'.ljust(25), '3) Edit Last Name'.ljust(25))
        print('4) Edit CreditCard #'.ljust(25), '5) Edit Exp. Date'.ljust(25), '6) Edit CVC'.ljust(25))
        print("7) Create New Password")
        choice = input("Selection Input:")
        if choice.upper() == 1:
            while True:
                username = input('Enter a New Username: ')
                if len(username) >= 4 and len(username) <= 15:
                    break
                else:
                    print("Invalid Username, try again")
                    continue
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
                CC = input('Enter a New Credit Card Number: ')
                if len(CC) == 16:
                    break
                else:
                    print("Invalid CC length, try again")
                    continue
            user_info[4] = CC
        if choice.upper() == '5':
            while True:
                E_Date = input('Enter a New Exp Date Number: ')
                if len(E_Date) == 4:
                    break
                else:
                    print("Invalid Exp Date length, try again")
                    continue
            user_info[5] = E_Date
        if choice.upper() == '6':
            while True:
                CVC = input('Enter a New CVC Number: ')
                if len(CVC) == 3:
                    break
                else:
                    print("Invalid CVC length, try again")
                    continue
            user_info[6] = CVC
        if choice.upper() == '7':
            while True:
                PW = input('Enter a New Password: ')
                if len(PW) >= 4:
                    PW = hash_pw(PW)
                    break
                else:
                    print("Invalid Password length, try again")
                    continue
            user_info[1] = PW
        if choice.upper() == '8':
            return True
        for x in user_info:
            print(x)
        self.insert_Edited_user(user_info)
        self.Print_UserInfo()
        return False

    def insert_Edited_user(self, user_info):
        cursor = connection.cursor()
        cursor.execute("UPDATE PASSENGER SET Username=?, HashPass=?, Fname=?, Lname=?, CardNum=?, ExpData=?, CVC=?"
                       "WHERE Username =?",
                       (user_info[0], user_info[1], user_info[2], user_info[3], user_info[4], user_info[5],
                        user_info[6], self.P_Username)
                       )
        connection.commit()
        return


################################################################################################

class Employee:
    E_Username = ''

    def EMP_Login(self):
        username, password = prompt()
        self.E_Username = username
        if self.Emp_Credential_Check(username, password) is not True:
            if Invalid_Input() is True:
                self.EMP_Login()
            else:
                return False
        return True

    def Emp_Credential_Check(self, Username, password):
        cursor = connection.cursor()
        Qry = "SELECT Username from EMPLOYEE  WHERE Username =?"
        cursor.execute(Qry, (Username,))
        Result = cursor.fetchall()
        if len(Result) <= 0:
            print("\nThis Username does not Exist")
            return False
        Qry = "SELECT HashPass, FName from EMPLOYEE WHERE Username =?"
        cursor.execute(Qry, (Username,))
        rows = cursor.fetchall()
        H_password = bytes(password, encoding='utf-8')
        for row in rows:
            if checkpw(H_password, row[0]):
                print("\nLog in Successful, Hello ", row[1])
                return True
        return False

    def EMPLOYEE_MENU(self):
        cursor = connection.cursor()
        Qry = "SELECT JobType FROM EMPLOYEE WHERE Username=?"
        print("\nAdmin Username:", self.E_Username)
        cursor.execute(Qry, (self.E_Username,))
        Job = cursor.fetchall()
        print()
        if Job[0][0] == 'Driver':
            Emp_Driv = Employees.Driver(self.E_Username)
            Emp_Driv.Driver_Menu()
            return
        if Job[0][0] == 'Controller':
            Emp_Cntr = Employees.Controller(self.E_Username)
            Emp_Cntr.Cntr_Menu()
            return
        if Job[0][0] == 'Admin':
            Emp_Admin = Employees.Admin(self.E_Username)
            Emp_Admin.Admin_Menu()
            return
        else:
            print("Please see admin to fix your Employee Profile")


# user_info = [username, hashpass, firstname, lastname, cardnum, expdate, cvc]
def NewPass_Username_DB_Check(Username):
    cursor = connection.cursor()
    rows = cursor.execute("SELECT Username from PASSENGER")
    for user in rows:
        if user == Username:
            print("\nThat Username already Exist, please choose another")
            return False
    return True


def hash_pw(password):
    Byte_PW = bytes(password, 'utf-8')
    return bcrypt.hashpw(Byte_PW, bcrypt.gensalt())


def prompt():
    while True:
        username = input('Enter a username: ')
        password = input('Enter a password: ')
        if len(username) >= 4 and len(username) <= 15 and len(password) >= 4:
            break
        else:
            continue
    return username, password


def Invalid_Input():
    choice = input("Press 1 to try again or any button to return to Prev Menu\n")
    if choice == '1':
        return True
    else:
        return False
