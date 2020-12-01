import boto3
import os
from dotenv import load_dotenv
from termcolor import colored


def terminateNorthVirginia():
    load_dotenv(verbose=True)

    session = boto3.session.Session(
        aws_access_key_id=os.getenv("ACCESS_KEY"),
        aws_secret_access_key=os.getenv("SECRET_KEY"),
    )

    client = session.client("ec2", region_name="us-east-1")

    ec2 = session.resource("ec2", region_name="us-east-1")

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

    idsToTerminate = [instance.id for instance in myInstances]

    try:
        print("Terminating North Virginia instances...")
        for instance_id in idsToTerminate:
            ec2.Instance(instance_id).terminate()
        for instance_id in idsToTerminate:
            ec2.Instance(instance_id).wait_until_terminated()
        if len(idsToTerminate) > 0:
            print(colored("Successfully terminated North Virginia instances!", "green"))
            print("Number of instances terminated: {0}".format(len(idsToTerminate)))
            for i in range(len(idsToTerminate)):
                print("{0}) id = {1}".format(i + 1, idsToTerminate[i]))

            enis = client.describe_network_interfaces(
                Filters=[
                    {
                        "Name": "group-name",
                        "Values": [
                            "Application-SG",
                        ],
                    },
                ],
            )

            enis_ids = [eni["NetworkInterfaceId"] for eni in enis["NetworkInterfaces"]]

            for eni_id in enis_ids:
                try:
                    client.delete_network_interface(NetworkInterfaceId=eni_id)
                except:
                    pass

            try:
                client.delete_security_group(GroupName="Application-SG")
                print(
                    colored("Successfully deleted application security group.", "green")
                )
            except:
                print(colored("Couldn't delete application security group.", "red"))
        else:
            enis = client.describe_network_interfaces(
                Filters=[
                    {
                        "Name": "group-name",
                        "Values": [
                            "Application-SG",
                        ],
                    },
                ],
            )

            enis_ids = [eni["NetworkInterfaceId"] for eni in enis["NetworkInterfaces"]]

            for eni_id in enis_ids:
                try:
                    client.delete_network_interface(NetworkInterfaceId=eni_id)
                except:
                    pass

            print(colored("No instances to terminate right now.", "yellow"))

            deleteSG = False
            security_groups = client.describe_security_groups()
            for security_group in security_groups["SecurityGroups"]:
                if security_group["GroupName"] == "Application-SG":
                    deleteSG = True
                    sg_id = security_group["GroupId"]

            if deleteSG:
                client.delete_security_group(GroupId=sg_id)
                print(
                    colored("Successfully deleted application security group.", "green")
                )

    except Exception as e:
        print("\n")
        print(e)
        print(colored("Couldn't terminate instances. Try again!", "red"))

    print(colored("North Virigina termination complete. Continuing...\n", "green"))
