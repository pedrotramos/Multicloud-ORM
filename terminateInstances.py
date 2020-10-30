import boto3
import os
from dotenv import load_dotenv
from termcolor import colored

load_dotenv(verbose=True)

session = boto3.session.Session(
    aws_access_key_id=os.getenv("ACCESS_KEY"),
    aws_secret_access_key=os.getenv("SECRET_KEY"),
)

ec2 = session.resource("ec2", region_name="us-east-1")

myInstances = ec2.instances.filter(
    Filters=[
        {
            "Name": "tag:Owner",
            "Values": ["Pedro Ramos"],
        },
        {
            "Name": "instance-state-name",
            "Values": ["running", "pending"],
        },
    ]
)

idsToTerminate = [instance.id for instance in myInstances]

try:
    for instance_id in idsToTerminate:
        ec2.Instance(instance_id).terminate()
    print("\n")
    if len(idsToTerminate) > 0:
        print(colored("Successfully terminated instances!", "green"))
        print("Number of instances terminated: {0}".format(len(idsToTerminate)))
        for i in range(len(idsToTerminate)):
            print("{0}) id = {1}".format(i + 1, idsToTerminate[i]))
    else:
        print(colored("No instances to terminate right now", "yellow"))
except:
    print("\n")
    print(colored("Couldn't terminate instances", "red"))
