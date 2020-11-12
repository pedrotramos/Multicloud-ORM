import boto3
import os
from dotenv import load_dotenv
from termcolor import colored


def terminateOhio():
    load_dotenv(verbose=True)

    session = boto3.session.Session(
        aws_access_key_id=os.getenv("ACCESS_KEY"),
        aws_secret_access_key=os.getenv("SECRET_KEY"),
    )

    client = session.client("ec2", region_name="us-east-2")

    ec2 = session.resource("ec2", region_name="us-east-2")

    myInstances = ec2.instances.filter(
        Filters=[
            {
                "Name": "tag:Owner",
                "Values": ["Pedro Ramos"],
            },
            {
                "Name": "tag:Application",
                "Values": ["Database Server"],
            },
            {
                "Name": "instance-state-name",
                "Values": ["running", "pending"],
            },
        ]
    )

    idsToTerminate = [instance.id for instance in myInstances]

    try:
        print("Terminating Ohio instances...")
        for instance_id in idsToTerminate:
            ec2.Instance(instance_id).terminate()
        for instance_id in idsToTerminate:
            ec2.Instance(instance_id).wait_until_terminated()
        if len(idsToTerminate) > 0:
            print(colored("Successfully terminated instances!", "green"))
            print("Number of instances terminated: {0}".format(len(idsToTerminate)))
            for i in range(len(idsToTerminate)):
                print("{0}) id = {1}".format(i + 1, idsToTerminate[i]))
            try:
                client.delete_security_group(GroupName="Database-SG")
                print(colored("Successfully deleted database security group", "green"))
            except:
                print(colored("Couldn't delete database security group", "red"))
        else:
            print(colored("No instances to terminate right now.", "yellow"))
    except Exception as e:
        print("\n")
        print(e)
        print(colored("Couldn't terminate instances. Try again!", "red"))

    print(colored("Ohio termination complete. Continuing...\n", "green"))