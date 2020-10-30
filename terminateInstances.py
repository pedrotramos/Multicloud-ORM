import boto3
from dotenv import load_dotenv
import os

load_dotenv(verbose=True)

session = boto3.session.Session(
    aws_access_key_id=os.getenv("ACCESS_KEY"),
    aws_secret_access_key=os.getenv("SECRET_KEY"),
)

ec2 = session.resource("ec2", region_name="us-east-1")

myInstances = ec2.instances.filter(
    Filters=[
        # {
        #     "Name": "tag:owner",
        #     "Values": ["Pedro Ramos"],
        # },
        {
            "Name": "instance-state-name",
            "Values": ["Running"],
        },
    ]
)

instanceList = [instance for instance in myInstances]

try:
    print(instanceList)
    myInstances.terminate()
    print("Number of instances terminated: {0}".format(len(instanceList)))
    for i in range(len(instanceList)):
        print("{0}) id = {1}".format(i + 1, instancesToTerminate[i]))
except:
    print("Couldn't terminate instances.")
