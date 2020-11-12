import boto3
import os
from dotenv import load_dotenv
from termcolor import colored


def launchASG():
    load_dotenv(verbose=True)

    session = boto3.session.Session(
        aws_access_key_id=os.getenv("ACCESS_KEY"),
        aws_secret_access_key=os.getenv("SECRET_KEY"),
    )

    client = session.client("ec2", region_name="us-east-1")

    clientASG = session.client("autoscaling", region_name="us-east-1")

    ec2 = session.resource("ec2", region_name="us-east-1")

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

        clientASG.create_auto_scaling_group(
            AutoScalingGroupName="AppASG",
            InstanceId=[myInstances[0].id],
            LoadBalancerNames=["AppLoadBalancer"],
            Tags=[
                {"Key": "Name", "Value": "TestAppASG"},
                {"Key": "Owner", "Value": "Pedro Ramos"},
                {"Key": "Application", "Value": "Application"},
            ],
            MinSize=1,
            MaxSize=2,
            DesiredCapacity=1,
        )

        print("Successfully created Auto Scaling Group. Continuing...")

        instance_ids = []
        for instance in myInstances:
            instance_ids.append(instance.id)

        response = clientASG.attach_instances(
            InstanceIds=instance_ids,
            AutoScalingGroupName="AppASG",
        )

        print("Successfully attached instances to Auto Scaling Group. Continuing...")
        print(colored("Auto Scaling Group setup complete.", "green"))

    except Exception as e:
        print(e)
        print(colored("Couldn't setup Auto Scaling Group. Try Again!", "red"))