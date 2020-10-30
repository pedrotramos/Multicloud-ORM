import boto3
from dotenv import load_dotenv
import os

load_dotenv(verbose=True)

session = boto3.session.Session(
    aws_access_key_id=os.getenv("ACCESS_KEY"),
    aws_secret_access_key=os.getenv("SECRET_KEY"),
)

ec2 = session.resource("ec2", region_name="us-east-1")

key_name = input("Insert the name of the key to be used: ")

try:
    keys = ec2.create_key_pair(KeyName=key_name)
    print("Key pair created succesfully!")
except:
    print("Could not create key pair...")
    pass

try:
    ec2_instances = ec2.create_instances(
        TagSpecifications=[
            {
                "ResourceType": "instance",
                "Tags": [
                    {"Key": "Name", "Value": "TestInstance2"},
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
    print("Number of instances created: {0}".format(len(ec2_instances)))
    for i in range(len(ec2_instances)):
        print("{0}) id = {1}".format(i + 1, ec2_instances[i].id))
except:
    print("Couldn't create instances...")