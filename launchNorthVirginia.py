import boto3
import os
from dotenv import load_dotenv
from termcolor import colored
from deleteAutoScalingGroup import shutDownASG
from deleteLoadBalancer import shutDownLoadBalancer
from terminateInstancesNorthVirgina import terminateNorthVirginia


def launchNorthVirginiaInstances(ipOhio):
    load_dotenv(verbose=True)

    session = boto3.session.Session(
        aws_access_key_id=os.getenv("ACCESS_KEY"),
        aws_secret_access_key=os.getenv("SECRET_KEY"),
    )

    client = session.client("ec2", region_name="us-east-1")

    ec2 = session.resource("ec2", region_name="us-east-1")

    clientASG = session.client("autoscaling", region_name="us-east-1")

    key_name = "Pedro-NV-ProjetoCloud"

    try:
        keyPair = ec2.create_key_pair(KeyName=key_name)
        with open("./{0}.pem".format(key_name), "w") as file:
            file.write(keyPair.key_material)
        os.system("chmod 700 {0}.pem".format(key_name))
        print("Successfully created North Virginia Application key pair. Continuing...")
    except:
        print("North Virginia Application key pair already exists. Continuing...")

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

    myInstanceList = [instance for instance in myInstances]

    asgRunning = False

    asgs = clientASG.describe_auto_scaling_groups()
    for asg in asgs["AutoScalingGroups"]:
        if asg["AutoScalingGroupName"] == "DjangoApp":
            asgRunning = True

    if len(myInstanceList) > 0 or asgRunning:
        print("Application already configured.")
        resp = input("Terminate and rebuild Application? [Y/N] ")
        if resp == "Y" or resp == "y":
            shutDownASG()
            shutDownLoadBalancer()
            terminateNorthVirginia()
            try:
                security_group = client.create_security_group(
                    GroupName="Application-SG",
                    Description="Security group for the Application.",
                )
                client.authorize_security_group_ingress(
                    GroupId=security_group["GroupId"],
                    IpPermissions=[
                        {
                            "IpProtocol": "tcp",
                            "FromPort": 22,
                            "ToPort": 22,
                            "IpRanges": [{"CidrIp": "0.0.0.0/0"}],
                        },
                        {
                            "IpProtocol": "tcp",
                            "FromPort": 8080,
                            "ToPort": 8080,
                            "IpRanges": [{"CidrIp": "0.0.0.0/0"}],
                        },
                        {
                            "IpProtocol": "tcp",
                            "FromPort": 80,
                            "ToPort": 80,
                            "IpRanges": [{"CidrIp": "0.0.0.0/0"}],
                        },
                    ],
                )
                print("Application security group successfully created. Continuing...")
            except:
                print("Application security group already exists. Continuing...")
            try:
                print("Creating North Virginia template instance...")
                ec2_instances = ec2.create_instances(
                    TagSpecifications=[
                        {
                            "ResourceType": "instance",
                            "Tags": [
                                {"Key": "Name", "Value": "TemplateInstance"},
                                {"Key": "Owner", "Value": "Pedro Ramos"},
                                {"Key": "Application", "Value": "Application"},
                            ],
                        },
                    ],
                    ImageId="ami-0dba2cb6798deb6d8",
                    KeyName=key_name,
                    MinCount=1,
                    MaxCount=1,
                    InstanceType="t2.micro",
                    SecurityGroups=["Application-SG"],
                    UserData="""#!/bin/sh
sudo apt update
cd /home/ubuntu
git clone https://github.com/pedrotramos/DjangoSetup-Tasks.git
sudo sed -i "83 c \\\t'HOST': '{0}'," tasks/portfolio/settings.py
cd tasks
./install.sh
sudo reboot
""".format(
                        ipOhio
                    ),
                )

                for i in range(len(ec2_instances)):
                    # use the boto3 waiter
                    ec2_instances[i].wait_until_running()
                    # reload the instance object
                    ec2_instances[i].reload()
                print(colored("Successfully created template instance!", "green"))

            except:
                print(
                    colored(
                        "Failed to create North Virginia template instance. Try again!\n",
                        "red",
                    )
                )
        else:
            print("North Virgina instances unchanged. Continuing...")
        print(
            colored(
                "North Virginia setup complete. Proceeding to Load Balancer setup...\n",
                "green",
            )
        )
    else:
        try:
            security_group = client.create_security_group(
                GroupName="Application-SG",
                Description="Security group for the Application.",
            )
            client.authorize_security_group_ingress(
                GroupId=security_group["GroupId"],
                IpPermissions=[
                    {
                        "IpProtocol": "tcp",
                        "FromPort": 22,
                        "ToPort": 22,
                        "IpRanges": [{"CidrIp": "0.0.0.0/0"}],
                    },
                    {
                        "IpProtocol": "tcp",
                        "FromPort": 8080,
                        "ToPort": 8080,
                        "IpRanges": [{"CidrIp": "0.0.0.0/0"}],
                    },
                    {
                        "IpProtocol": "tcp",
                        "FromPort": 80,
                        "ToPort": 80,
                        "IpRanges": [{"CidrIp": "0.0.0.0/0"}],
                    },
                ],
            )
            print("Application security group successfully created. Continuing...")
        except:
            print("Application security group already exists. Continuing...")
        try:
            print("Creating North Virginia template instance...")
            ec2_instances = ec2.create_instances(
                TagSpecifications=[
                    {
                        "ResourceType": "instance",
                        "Tags": [
                            {"Key": "Name", "Value": "TemplateInstance"},
                            {"Key": "Owner", "Value": "Pedro Ramos"},
                            {"Key": "Application", "Value": "Application"},
                        ],
                    },
                ],
                ImageId="ami-0dba2cb6798deb6d8",
                KeyName=key_name,
                MinCount=1,
                MaxCount=1,
                InstanceType="t2.micro",
                SecurityGroups=["Application-SG"],
                UserData="""#!/bin/sh
sudo apt update
cd /home/ubuntu
git clone https://github.com/pedrotramos/DjangoSetup-Tasks.git
sudo sed -i "83 c \\\t'HOST': '{0}'," tasks/portfolio/settings.py
cd tasks
./install.sh
sudo reboot
""".format(
                    ipOhio
                ),
            )

            for i in range(len(ec2_instances)):
                # use the boto3 waiter
                ec2_instances[i].wait_until_running()
                # reload the instance object
                ec2_instances[i].reload()
            print(colored("Successfully created template instance!", "green"))
            print(
                colored(
                    "North Virginia setup complete. Proceeding to Load Balancer setup...\n",
                    "green",
                )
            )
        except Exception as e:
            print(e)
            print(
                colored(
                    "Failed to create North Virginia template instance. Try again!\n",
                    "red",
                )
            )
