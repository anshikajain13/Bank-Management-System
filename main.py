import json 
import random 
import string
from pathlib import Path

class Bank:
    database = "database.json"
    data = []      #damy data

    if Path(database).exists():
        with open(database) as fs:
            data = json.loads(fs.read())
    

    @classmethod
    def __update(cls):
        with open(cls.database,'w') as fs:
            fs.write(json.dumps(cls.data))

    
    @classmethod
    def __accountgenerate(cls):
        alpha = random.choices(string.ascii_letters,k = 8)
        num = random.choices(string.digits, k =4)

        acc = alpha + num
        random.shuffle(acc)
        return "".join(acc)
    
    def create_user(self):
        info = {
            "name":input("tell user name :- "),
            "age": int(input("tell user Age :- ")),
            "email":input("Tell user Email :- "),
            "account_no": Bank.__accountgenerate(),
            "pin": int(input("tell user pin :- ")),
            "balance": 0
        }

        if info['age'] < 12 or len(str(info["pin"])) != 4:
            print("sorry cannot create account")
        
        else:
            Bank.data.append(info)
            Bank.__update()
    
    def deposite_money(self):
        accno = input("Tell your account number :- ")
        pin = int(input("tell your pin :- "))

        userdata = [i for i in Bank.data if            #list comprehension
                    i['account_no'] == accno and 
                    i['pin']== pin]
        
        if not userdata:
            print("sorry no such user exist")
        else:
            amount = int(input("Money :- "))
            userdata[0]['balance'] += amount
            Bank.__update()
            print("balance added successfully")

    def withdraw_money(self):
        accno = input("Tell your account number :- ")
        pin = int(input("tell your pin :- "))

        userdata = [i for i in Bank.data if             #list comprehension
                    i['account_no'] == accno and 
                    i['pin']== pin]
        if not userdata:
            print("sorry no such user exist")
        else:
            amount = int(input("Money :- "))
            if amount > userdata[0]['balance']:
                print("insufficient balance")
            else:
                userdata[0]['balance'] -= amount
                Bank.__update()
                print("balance added successfully")
            
            
    def show_details(self):
        accno = input("tell your account number:- ")
        pin = int(input("tell your pin:- "))
        
        userdata = [i for i in Bank.data if
                    i['account_no'] == accno and
                    i['pin'] == pin]
        
        if not userdata:
            print('no data found!')
        else:
            for i in userdata[0]:
                print(f"{i} - {userdata[0][i]}")
                
                
    def update_details(self):
        accno = input("tell your account number:- ")
        pin = int(input("tell your pin:- "))
        
        userdata = [i for i in Bank.data if
                    i['account_no'] == accno and
                    i['pin'] == pin]
        
        if not userdata:
            print("no user found!")
        else:
            print("you cannot change bankbalance, account number and age")
        
        newdata = {
            "name" : input("tell your new name or press enter to skip :"),
            "email" : input("tell your mail or press enter to skip :"),
            "pin" : input('tell your pin or press enter to skip :')
        }
        if newdata["name"] == "":
            newdata["name"] = userdata[0]["name"]
        if newdata["email"] == "":
            newdata["email"] = userdata[0]["email"]
        if newdata["pin"] == "":
            newdata["pin"] = str(userdata[0]["pin"])
            
        for i in userdata[0]:
            if i in newdata and i != "pin":
                userdata[0][i] = newdata[i]
            if i == 'pin':
                userdata[0][i] = int(newdata[i])
                
        Bank.__update()
        
    def delete_account(self):
        accno = input("tell your account number:- ")
        pin = int(input("tell your pin:- "))
        
        userdata = [i for i in Bank.data if
                    i['account_no'] == accno and
                    i['pin'] == pin] 
        
        if not userdata:
            print("no such user")
            
        else:
            print("are you sure, you want to delete")
            check = input("press y (yes) or n(no) : ")
            if check == "y":
                index = Bank.data.index(userdata[0])
                Bank.data.pop(index)
                Bank._Bank__update()



bank = Bank()

while True:

    print("press 1 for creating an account")
    print("press 2 for depositing money ")
    print("press 3 for withdrawing money ")
    print("press 4 for details of a user ")
    print("press 5 updating users details ")
    print("press 6 for deleting user")
    print("press 0 for exit")

    res = int(input("tell your response :- "))

    if res == 1:
        bank.create_user()
    elif res == 2:
        bank.deposite_money()
    elif res == 3:
        bank.withdraw_money()
    elif res == 4:
        bank.show_details()
    elif res == 5:
        bank.update_details()
    elif res == 6:
        bank.delete_account()
    elif res == 0:
        break
    else:
        print('invalid input try again')