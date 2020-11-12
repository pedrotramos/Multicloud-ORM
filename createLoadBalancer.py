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

    try:
        security_groups = client.describe_security_groups(
            GroupNames=[
                "Application-SG",
            ],
        )

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
        instance_ids = []
        for instance in myInstances:
            if instance.subnet.id not in subnets:
                subnets.append(instance.subnet.id)
            instance_ids.append(instance.id)

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

        print("Successfully created Load Balancer. Continuing...")

        # try:
        #     for instance_id in instance_ids:
        #         clientLB.register_instances_with_load_balancer(
        #             LoadBalancerName="AppLoadBalancer",
        #             Instances=[
        #                 {"InstanceId": instance_id},
        #             ],
        #         )
        #     print("Successfully registered instances with Load Balancer. Continuing...")
        print(
            colored(
                "Load Balancer setup complete. Proceeding to Auto Scalling Group setup...\n",
                "green",
            )
        )
        except:
            print("Couldn't register all instances with Load Balancer. Try Again!")
    except Exception as e:
        print(e)
        print(colored("Couldn't create Load Balancer. Try Again!", "red"))