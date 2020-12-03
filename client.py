from termcolor import colored
import json
import requests
import argparse
import datetime
import sys

parser = argparse.ArgumentParser()
parser.add_argument(
    "verb",
    choices=["GET", "POST", "PUT", "DELETE"],
    help="HTTP verb of the request",
    type=str,
)
parser.add_argument(
    "--id", required="PUT" in sys.argv or "DELETE" in sys.argv, help="Task ID", type=int
)
parser.add_argument(
    "--title",
    required="PUT" in sys.argv or "POST" in sys.argv,
    help="Task title",
    type=str,
)
parser.add_argument(
    "--desc",
    required="PUT" in sys.argv or "POST" in sys.argv,
    help="Task description",
    type=str,
)
args = parser.parse_args()

appURL = "http://apploadbalancer-718275496.us-east-1.elb.amazonaws.com/tasks"

if args.verb == "GET" and args.id is None:
    r = requests.get(url=appURL + "/")
    print("\n")
    print(json.dumps(r.json(), sort_keys=False, indent=4))
    print("\n")
elif args.verb == "GET":
    r = requests.get(url=appURL + "/{0}".format(args.id))
    print("\n")
    print(json.dumps(r.json(), sort_keys=False, indent=4))
    print("\n")
elif args.verb == "POST":
    r = requests.post(
        url=appURL + "/",
        json={
            "title": args.title,
            "pub_date": str(datetime.datetime.now()),
            "description": args.desc,
        },
    )
    if r.status_code == 201:
        print(colored("\nSuccessfully added task!\n", "green"))
    else:
        print(colored("\nSomething went wrong! Try Again.\n", "red"))
        print(args.title, args.desc)
        print(r.status_code)
elif args.verb == "PUT":
    r = requests.put(
        url=appURL + "/{0}".format(args.id),
        json={
            "title": args.title,
            "pub_date": str(datetime.datetime.now()),
            "description": args.desc,
        },
    )
    if r.status_code == 201:
        print(colored("\nSuccessfully altered task!\n", "green"))
    else:
        print(colored("\nSomething went wrong! Try Again.\n", "red"))
        print(r.status_code)
elif args.verb == "DELETE":
    r = requests.delete(url=appURL + "/{0}".format(args.id))
    if r.status_code == 200:
        print(colored("\nSuccessfully removed task!\n", "green"))
    else:
        print(colored("\nSomething went wrong! Try Again.\n", "red"))
        print(r.status_code)
else:
    print(colored("\nBad Request! Try again.\n", "red"))
