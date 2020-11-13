import boto3
import os
from dotenv import load_dotenv
from termcolor import colored


def launchLoadBalancer():
    load_dotenv(verbose=True)

    session = boto3.session.Session(
        aws_access_key_id=os.getenv("ACCESS_KEY"),
        aws_secret_access_key=os.getenv("SECRET_KEY"),
    )

    client = session.client("ec2", region_name="us-east-1")

    clientLB = session.client("elb", region_name="us-east-1")

    ec2 = session.resource("ec2", region_name="us-east-1")

    create = True

    lbs = clientLB.describe_load_balancers()

    print("Checking whether Load Balancer already exists...")
    for lb in lbs["LoadBalancerDescriptions"]:
        if lb["LoadBalancerName"] == "AppLoadBalancer":
            create = False

    if create:
        print("Creating Load Balancer...")
        try:
            myInstances = ec2.instances.filter(
                Filters=[
                    {
                        "Name": "tag:Owner",
                        "Values": ["Pedro Ramos"],
                    },
                    {
                        "Name": "tag:Application",
                        "Values": ["Application"],
                    },
                    {
                        "Name": "instance-state-name",
                        "Values": ["running", "pending"],
                    },
                ]
            )

            subnets = []
            for instance in myInstances:
                if instance.subnet.id not in subnets:
                    subnets.append(instance.subnet.id)
        except:
            print(
                colored("Couldn't get appropriate subnet for the Load Balancer", "red")
            )

        try:
            security_groups = client.describe_security_groups(
                GroupNames=[
                    "Application-SG",
                ],
            )

            loadBalancer = clientLB.create_load_balancer(
                LoadBalancerName="AppLoadBalancer",
                Listeners=[
                    {
                        "Protocol": "tcp",
                        "LoadBalancerPort": 80,
                        "InstanceProtocol": "tcp",
                        "InstancePort": 8080,
                    },
                ],
                Subnets=subnets,
                SecurityGroups=[
                    security_groups["SecurityGroups"][0]["GroupId"],
                ],
                Tags=[
                    {"Key": "Name", "Value": "TestAppLB"},
                    {"Key": "Owner", "Value": "Pedro Ramos"},
                    {"Key": "Application", "Value": "Application"},
                ],
            )

            print(colored("Successfully created Load Balancer!", "green"))

        except:
            print(colored("Couldn't create Load Balancer. Try Again!", "red"))

    else:
        print("Load Balancer already exists. Getting it's DNS Name...")

    lb = clientLB.describe_load_balancers(
        LoadBalancerNames=[
            "AppLoadBalancer",
        ],
    )

    print("Load Balancer DNS Name: " + lb["LoadBalancerDescriptions"][0]["DNSName"])

    print(
        colored(
            "Load Balancer setup complete. Proceeding to Auto Scalling Group setup...\n",
            "green",
        )
    )
