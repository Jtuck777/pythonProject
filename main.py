"""
SJSU CMPE138 Team5 Project
"""
import traceback, sys

import bcrypt
from bcrypt import gensalt, hashpw, checkpw
import sql_init_login
import DB_User
import sqlite3
import T_Sched
import Employees

connection = sqlite3.connect('trains.db')
cursor = connection.cursor()
# user_actions[i] = (username, action)
# if not logged in, don't track this (or just use 'guest')
user_actions = []



def main():
    # Initializes the DB and registration system
    # sql_init_login.init_db()
    schedule = T_Sched.Schedules()
    while True:
        print('\n-----Welcome to the CMPE 138 Train App-----')
        print('1) Create account   2) Passenger login '
              '\n3) Employee login   4) View Train Schedule'
              '\n5) Exit ')
        choice = input('Selection Input: ')
        if choice.upper() == '1':
            user = DB_User.NewUser()
            user.create_user()
            continue
        elif choice.upper() == '2':
            user = DB_User.Passenger()
            user.Pass_Login()
            user.Pass_Menu()
            continue
        elif choice.upper() == '3':
            user = DB_User.Employee()
            if user.EMP_Login():
                user.EMPLOYEE_MENU()
            continue
        elif choice.upper() == '4':
            schedule.schedule_menu()
            continue
        elif choice.upper() == '5':
            print("Good bye!!")
            break
        else:
            print('Invalid option!')


if __name__ == '__main__':
    main()
