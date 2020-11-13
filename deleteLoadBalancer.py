import boto3
import os
from dotenv import load_dotenv
from termcolor import colored


def shutDownLoadBalancer():
    load_dotenv(verbose=True)

    session = boto3.session.Session(
        aws_access_key_id=os.getenv("ACCESS_KEY"),
        aws_secret_access_key=os.getenv("SECRET_KEY"),
    )

    clientLB = session.client("elb", region_name="us-east-1")

    client = session.client("ec2", region_name="us-east-1")

    lbs = clientLB.describe_load_balancers()

    delete = False

    print("Checking whether there is a Load Balancer to delete...")
    for lb in lbs["LoadBalancerDescriptions"]:
        if lb["LoadBalancerName"] == "AppLoadBalancer":
            delete = True

    if delete:
        print("Deleting Load Balancers...")
        try:
            clientLB.delete_load_balancer(LoadBalancerName="AppLoadBalancer")
            print(colored("Successfully deleted Load Balancer.", "green"))
        except Exception as e:
            print("\n")
            print(e)
            print(colored("Couldn't delete Load Balancer. Try again!", "red"))

        print(colored("Load Balancer deletion complete. Continuing...\n", "green"))

    else:
        print(colored("No Load Balancers to delete. Continuing...\n", "green"))