#!/usr/bin/env python
# coding:utf-8

import json
from collections import OrderedDict
from variables import *
import requests
import owncloud

class Weeelab_users():
    """Class used to add, update, delete or print the list of users"""
    def __init__(self):
        """init function of weelab_users, read file of users"""
        # self.json_file = open("users.json", 'r')
        # self.user_file = json.loads(self.json_file.read(),
                                    # object_pairs_hook=OrderedDict)
        # self.json_file.close()
        oc = owncloud.Client(OC_URL)
        oc.login(OC_USER, OC_PWD)
        self.user_file = json.loads(oc.get_file_contents(USER_PATH), 
                                    object_pairs_hook=OrderedDict)

    def start(self):
        """Start function, select the function to do"""
        function = {
            'add': self.add,
            'update': self.update,
            'search': self.search,
            'delete': self.delete,
            'print': self.print_list,
            'help': self.help_user,
            'exit': self.exit
        }
        warning = """PLEASE BE CAREFUL, YOU COULD "SMINCHIARE" (ndr. damage)
THE USER LIST IF YOU DON'T PAY ATTENTION!!!! IF YOU ARE NOT AUTHORIZED LEAVE
EVERY HOPE YOU ENTER AND EXIT THE PROGRAM NOW. \n
If you are @quel_tale, Hi :) you owe me a beer every time you use this program.
So insert Y and I show you how deep the rabbit hole goes otherwise insert N.
(Y/N)
"""
        console = input(warning + "> ")
        command = console.split(' ', 1)
        if command[0] == "Y" or command[0] == "y":
            print("I solemnly swear that I am up to no good. Ok we can start! \
\n")        
        else:
            print("Oh ok, I'll be good here for the next time waiting for you \
<3.")
            exit()
        menu = """Which operation would you like to perform?
* 1) print: print the full list of users;
* 2) add: add a user to the list;
* 3) update: update the user info;
* 4) search: search a user in the list;
* 5) delete: delete a user from the list;
* 6) help: instructions on how to use this script;
* 7) exit: exit from the weee_users script.
"""
        console = input(menu + "> ")
        while True:
            command = console.split(' ', 1)
            # self.json_file = open("users.json", 'r')
            # self.user_file = json.loads(self.json_file.read(),
                                        #object_pairs_hook=OrderedDict)
            # self.json_file.close()
            self.user_file = json.loads(oc.get_file_contents(USER_PATH))
            try:
                function.get(str(command[0]))()
                console = input(menu + "> ")
            except (IndexError, ValueError, TypeError):
                print("ERROR. Check the input.")
                console = input("> ")
        

    def add(self):
        """Function used to set the user on the list"""
        user = OrderedDict()
        level = {1: "name",
        2: "surname",
        3: "username",
        4: "serial",
        5: "telegramID",
        6: "nicknames",
        7: "level"
        }
        msg = """You selected to add a user to the list, please be sure
to have all the information needed (name, surname, _username_, serial,
_telegramID_, nicknames, _level_), the _data_ must be correct to guarantee
the proper operation of the bot. The user is added to the list when the
last data (_level_) is inserted, you can exit everytime writing exit also
in the field to be compiled (I hope noone is called "exit", indeed is called
"noone" ah ah ah). \n
PRESS ENTER TO PROCEED.
"""
        input(msg)
        index = 1
        menu = """
You can return to the previous field/menu writing return.
Insert the %s of the user: 
"""
        while index < 8 and index > 0:
            if index == 6:
                user[level[index]] = str(input(menu % level[index] + "> ")).split(' ')
            else:
                user[level[index]] = str(input(menu % level[index] + "> "))
            if user[level[index]] == "return":
                index = index - 1 
            else:
                index = index + 1
            
            if index == 8:
                msg = """
The user is about to be listed, please check the info. To confirm insert Y 
otherwise insert N to return to previous field.
"""
                command = str(input(msg + json.dumps(user, indent=4)
                              + "\n (Y/N)\n> "))
                if command[0] == "Y" or command[0] == "y":
                    index = index + 1
                    self.user_file["users"].append(user)
                    # j_file = open("users.json", 'w')
                    # j_file.write(json.dumps(self.user_file, indent=4))
                    # j_file.close()
                    oc.put_file_contents(
                        USER_BOT_PATH, self.user_file.encode('utf-8'))
                    print("User listed. \n")
                else:
                    index = index -1

    def update(self):
        """Function to update a user in the list, WORK IN PROGRESS"""
        user_number = 0
        level = {1: "name",
        2: "surname",
        3: "username",
        4: "serial",
        5: "telegramID",
        6: "nicknames",
        7: "level"
        }
        menu = """
You selected to update a user in the list. You can search him/her by the name.
Please insert the name of the user to search. Insert -1 to return.\n
"""
        name = input(menu + "> ")
        if name == str(-1):
            user_number = -1
        else:
            user_list = self.search(name)
        while user_number != -1:
            if len(user_list) > 0:
                user_number = int(input("> "))
                if user_number != -1:
                    msg = "User to update: \n" + json.dumps(
                        user_list[user_number], indent=4) + "\nconfirm? (Y/N)"
                    command = input(msg + "> ")
                    if command[0] == "Y" or command[0] == "y":
                        msg = """
Which field you want to update? Insert -1 to exit.\n %s
"""
                        field = int(input(msg % json.dumps(level, indent=4) + "> "))
                        if field == -1:
                            user_number = -1
                        else:
                            msg = "Insert the new value"
                            value = str(input(msg + "> "))
                            user_list[user_number][level[field]] = value
                            msg = "User updated: \n" + json.dumps(
                            user_list[user_number], indent=4) + "\nconfirm? (Y/N)\n"
                            command = input(msg + "> ")
                            if command[0] == "Y" or command[0] == "y":
                                #j_file = open("users.json", 'w')
                                #j_file.write(json.dumps(self.user_file, indent=4))
                                #j_file.close()
                                oc.put_file_contents(
                                    USER_BOT_PATH, self.user_file.encode('utf-8'))
                                print("User updated.\n")
                                name = input(menu + "> ")
                                if name != str(-1):
                                    user_list = self.search(name)
                                else:
                                    user_number = -1
                            else:
                                user_number = -1
                    else:
                        user_number = -1
            else:
                menu = """Sorry no user with this name. Try again or insert -1
to exit.
"""
                user = input("> ")
                if int(user) == -1:
                    user_number == -1
                else: 
                    user_number = 0
                    user_list = self.search(user)
    
    def search(self, name=None):
        """Function to search a user in the list."""
        menu = """You are searching a user in the list. You can
sarch him/her by the name.
Please insert the name of the user to search.
"""     
        if name is None:
            name = input(menu + "> ")
        user_list = []
        for user in self.user_file["users"]:
            if str(user['name']) == name:
                user_list.append(user)
        print("These are the users found.\n")
        i = 0
        if len(user_list) > 0:
            for user in user_list:
                print(str(i) + ": " + json.dumps(user, indent=4))
                i = i +1
            print("\n")
        else:
            print("Sorry no user with this name.\n")
        return user_list

    def delete(self):
        """Function to delete a user in the list"""
        user_number = 0
        menu = """You selected to delete a user in the list. You can
sarch him/her by the name.
Please insert the name of the user to search or -1 to return.
"""
        name = input(menu + "> ")
        if name != str(-1):
            user_list = self.search(name)
            while user_number != -1:
                if len(user_list) > 0:
                    user_number = int(input("> "))
                    if user_number != -1:
                        msg = "User to delete: \n" + json.dumps(
                            user_list[user_number], indent=4) + "\nconfirm? (Y/N) \n"
                        command = input(msg + "> ")
                        if command[0] == "Y" or command[0] == "y":
                            self.user_file["users"].remove(user_list[user_number])
                            #j_file = open("users.json", 'w')
                            #j_file.write(json.dumps(self.user_file, indent=4))
                            #j_file.close()
                            oc.put_file_contents(
                                USER_BOT_PATH, self.user_file.encode('utf-8'))
                            print("User deleted.\n")
                            name = input(menu + "> ")
                            user_list = self.search(name)
                        else:
                            user_number = -1
                else:
                    msg = "Try again or insert -1 to exit.\n"
                    user = str(input(msg + "> "))
                    if user == str(-1):
                        user_number = -1
                    else: 
                        user_number = 0
                        user_list = self.search(user)
    
    def print_list(self):
        """print the list of the user"""
        # menu = """You selected to print the list of the users. Proceed? (Y/N)
# Insert Y to proceed or N to return.
# """
        # command = input(menu + "> ")
        #if command[0] == "Y" or command[0] == "y":
        print(json.dumps(self.user_file, indent=4))
        input("PRESS ENTER TO PROCEED")

    def help_user(self):
        """help for user, WORK IN PROGRESS"""
        msg = """
The function available are the following:

* 1) print: print the full list of users;
* 2) add: add a user to the list;
* 3) update: update the user info;
* 4) search: search a user in the list;
* 5) delete: delete a user from the list;
* 6) help: instructions on how to use this script;
* 7) exit: exit from the weee_users script.

1) print: you can print all the user list, no input required.
2) add: you can add a new user you are driven ste(p) by ste(p) to complete all the field.
3) update: you can update a user in the list, first you search it by name and then
you select it from the list, you have also to select the field you want to update from a list
and then insert the new value, you are driven in every ste(p).
4) search: you can search a user in the list by name.
5) delete: you can search a user by name and delete it from the list.
6) help: this "usefull" help.
7) exit: simple exit from the program.

In every moment you can return to main menu or a step back writing -1 or in some case return.
"""
        print(msg)

    def exit(self):
        exit()

if __name__ == '__main__':
    Weee_Users = Weeelab_users()
    Weee_Users.start()
