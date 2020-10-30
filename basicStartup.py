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

myInstanceList = [instance for instance in myInstances]

if len(myInstanceList) > 0:
    print(colored("Couldn't create instances. Instances already running.", "red"))
else:
    print("\n")
    print(colored("Type the name of the key to be used.", "cyan"))
    print(colored("Make sure you have access to the selected private key file!", "red"))
    key_name = input("Key name: ")
    print("\n")

    try:
        ec2_instances = ec2.create_instances(
            TagSpecifications=[
                {
                    "ResourceType": "instance",
                    "Tags": [
                        {"Key": "Name", "Value": "TestInstance"},
                        {"Key": "Owner", "Value": "Pedro Ramos"},
                        {"Key": "Application", "Value": "Test"},
                    ],
                },
            ],
            ImageId="ami-0dba2cb6798deb6d8",
            KeyName=key_name,
            MinCount=1,
            MaxCount=2,
            InstanceType="t2.micro",
        )
        print(colored("Successfully created instances!", "green"))
        print("Number of instances created: {0}".format(len(ec2_instances)))
        for i in range(len(ec2_instances)):
            print("{0}) id = {1}".format(i + 1, ec2_instances[i].id))
    except:
        prin("\n")
        print(colored("Failed to create instances. Check key name!", "red"))