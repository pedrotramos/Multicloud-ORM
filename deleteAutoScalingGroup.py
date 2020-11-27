import boto3
import os
from dotenv import load_dotenv
from termcolor import colored


def shutDownASG():
    load_dotenv(verbose=True)

    session = boto3.session.Session(
        aws_access_key_id=os.getenv("ACCESS_KEY"),
        aws_secret_access_key=os.getenv("SECRET_KEY"),
    )

    clientASG = session.client("autoscaling", region_name="us-east-1")

    asgs = clientASG.describe_auto_scaling_groups()

    delete = False

    print("Checking whether there is an Auto Scaling Group to delete...")
    for asg in asgs["AutoScalingGroups"]:
        if asg["AutoScalingGroupName"] == "DjangoApp":
            delete = True

    if delete:
        print("Deleting Auto Scaling Group...")
        try:
            clientASG.delete_auto_scaling_group(
                AutoScalingGroupName="DjangoApp", ForceDelete=True
            )
            print(colored("Successfully deleted Auto Scaling Group.", "green"))
        except Exception as e:
            print(e)
            print(colored("Couldn't delete Auto Scaling Group. Try Again!", "red"))

        print(colored("Auto Scaling Group deletion complete. Continuing...\n", "green"))
    else:
        print(colored("No Auto Scaling Groups to delete. Continuing...\n", "green"))

    delete = False

    lcs = clientASG.describe_launch_configurations()

    print("Checking whether there is a Launch Configuration to delete...")
    for lc in lcs["LaunchConfigurations"]:
        if lc["LaunchConfigurationName"] == "DjangoApp":
            delete = True

    if delete:
        print("Deleting Launch Configuration...")
        try:
            clientASG.delete_launch_configuration(LaunchConfigurationName="DjangoApp")
            print(colored("Successfully deleted Launch Configuration.", "green"))
        except Exception as e:
            print(e)
            print(colored("Couldn't delete Launch Configuration. Try Again!", "red"))

        print(
            colored("Launch Configuration deletion complete. Continuing...\n", "green")
        )
    else:
        print(colored("No Launch Configuration to delete. Continuing...\n", "green"))