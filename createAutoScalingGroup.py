import boto3
import os
from dotenv import load_dotenv
from termcolor import colored
from terminateInstancesNorthVirgina import terminateNorthVirginia


def launchASG():
    load_dotenv(verbose=True)

    session = boto3.session.Session(
        aws_access_key_id=os.getenv("ACCESS_KEY"),
        aws_secret_access_key=os.getenv("SECRET_KEY"),
    )

    client = session.client("ec2", region_name="us-east-1")

    clientASG = session.client("autoscaling", region_name="us-east-1")

    ec2 = session.resource("ec2", region_name="us-east-1")

    asgs = clientASG.describe_auto_scaling_groups()

    create = True

    print("Checking whether Auto Scaling Group already exists...")
    for asg in asgs["AutoScalingGroups"]:
        if asg["AutoScalingGroupName"] == "DjangoApp":
            create = False

    myInstances = ec2.instances.filter(
        Filters=[
            {
                "Name": "tag:Name",
                "Values": ["TemplateInstance"],
            },
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

    instance_ids = []
    for instance in myInstances:
        instance_ids.append(instance.id)

    if create:
        print("Creating Auto Scaling Group...")
        try:
            clientASG.create_auto_scaling_group(
                AutoScalingGroupName="DjangoApp",
                InstanceId=instance_ids[0],
                LoadBalancerNames=["AppLoadBalancer"],
                Tags=[
                    {"Key": "Name", "Value": "DjangoApp"},
                    {"Key": "Owner", "Value": "Pedro Ramos"},
                    {"Key": "Application", "Value": "Application"},
                ],
                MinSize=1,
                MaxSize=4,
                DesiredCapacity=1,
            )
            print("Successfully created Auto Scaling Group. Continuing...")
            print(
                colored(
                    "Auto Scaling Group setup complete. Finishing build...\n", "green"
                )
            )
            for instance_id in instance_ids:
                ec2.Instance(instance_id).terminate()
            for instance_id in instance_ids:
                ec2.Instance(instance_id).wait_until_terminated()

        except Exception as e:
            print(e)
            print(colored("Couldn't setup Auto Scaling Group. Try Again!\n", "red"))

    else:
        print(
            colored("Auto Scaling Group already exists. Finishing build...\n", "green")
        )
        for instance_id in instance_ids:
            ec2.Instance(instance_id).terminate()
        for instance_id in instance_ids:
            ec2.Instance(instance_id).wait_until_terminated()
