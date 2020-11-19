from termcolor import colored
import json
import requests
import datetime

appURL = "http://apploadbalancer-1258571141.us-east-1.elb.amazonaws.com/tasks"

run = True

print("\nDjango CLI\n")

while run:
    print("Select Action From List Below!")
    print("1 - List All Tasks")
    print("2 - Get Task")
    print("3 - Add New Task")
    print("4 - Alter Task")
    print("5 - Delete Task")
    print("0 - Exit CLI")

    action = int(input("Selected Action Number: "))

    if action == 0:
        run = False
    elif action == 1:
        r = requests.get(url=appURL + "/listAll")
        print("\n")
        print(json.dumps(r.json(), sort_keys=False, indent=4))
        print("\n")
    elif action == 2:
        task_id = input("ID of task to get: ")
        r = requests.get(url=appURL + "/{0}".format(task_id))
        print("\n")
        print(json.dumps(r.json(), sort_keys=False, indent=4))
        print("\n")
    elif action == 3:
        taskTitle = input("Taks title: ")
        taskDescription = input("Task description: ")
        r = requests.post(
            url=appURL + "/add",
            json={
                "title": taskTitle,
                "pub_date": str(datetime.datetime.now()),
                "description": taskDescription,
            },
        )
        if r.status_code == 201:
            print(colored("\nSuccessfully added task!\n", "green"))
        else:
            print(colored("\nSomething went wrong! Try Again.\n", "red"))
    elif action == 4:
        task_id = input("ID of task to alter: ")
        taskTitle = input("Taks title: ")
        taskDescription = input("Task description: ")
        r = requests.put(
            url=appURL + "/alter/{0}".format(task_id),
            json={
                "title": taskTitle,
                "pub_date": str(datetime.datetime.now()),
                "description": taskDescription,
            },
        )
        if r.status_code == 201:
            print(colored("\nSuccessfully altered task!\n", "green"))
        else:
            print(colored("\nSomething went wrong! Try Again.\n", "red"))
    elif action == 5:
        task_id = input("ID of task to remove: ")
        r = requests.delete(url=appURL + "/remove/{0}".format(task_id))
        if r.status_code == 200:
            print(colored("\nSuccessfully removed task!\n", "green"))
        else:
            print(colored("\nSomething went wrong! Try Again.\n", "red"))
    else:
        print(colored("\nAction number does not exist! Try again.\n", "red"))
