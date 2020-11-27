import boto3
import os
from dotenv import load_dotenv
from termcolor import colored
from terminateInstancesOhio import terminateOhio


def launchOhioInstances():
    load_dotenv(verbose=True)

    session = boto3.session.Session(
        aws_access_key_id=os.getenv("ACCESS_KEY"),
        aws_secret_access_key=os.getenv("SECRET_KEY"),
    )

    client = session.client("ec2", region_name="us-east-2")

    ec2 = session.resource("ec2", region_name="us-east-2")

    key_name = "Pedro-O-ProjetoCloud"

    try:
        keyPair = ec2.create_key_pair(KeyName=key_name)
        with open("./{0}.pem".format(key_name), "w") as file:
            file.write(keyPair.key_material)
        os.system("chmod 700 {0}.pem".format(key_name))
        print("Successfully created Ohio Database key pair. Continuing...")
    except:
        print("Ohio Database key pair already exists. Continuing...")

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

    myInstanceList = [instance for instance in myInstances]

    if len(myInstanceList) > 0:
        print("Instances already running.")
        resp = input("Terminate and recreate instances? [Y/N] ")
        if resp == "Y" or resp == "y":
            terminateOhio()
            try:
                security_group = client.create_security_group(
                    GroupName="Database-SG",
                    Description="Security group for the Database.",
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
                            "FromPort": 5432,
                            "ToPort": 5432,
                            "IpRanges": [{"CidrIp": "0.0.0.0/0"}],
                        },
                    ],
                )
                print("Database security group successfully created. Continuing...")
            except:
                print("Database security group already exists. Continuing...")
            try:
                ec2_instances = ec2.create_instances(
                    TagSpecifications=[
                        {
                            "ResourceType": "instance",
                            "Tags": [
                                {"Key": "Name", "Value": "DB-Instance"},
                                {"Key": "Owner", "Value": "Pedro Ramos"},
                                {"Key": "Application", "Value": "Database Server"},
                            ],
                        },
                    ],
                    ImageId="ami-07efac79022b86107",
                    KeyName=key_name,
                    MinCount=1,
                    MaxCount=1,
                    InstanceType="t2.micro",
                    SecurityGroups=["Database-SG"],
                    UserData="""#!/bin/sh
sudo apt update
sudo apt install postgresql postgresql-contrib -y
sudo -u postgres psql -c "CREATE USER cloud WITH PASSWORD 'cloud';"
sudo -u postgres createdb -O cloud tasks
sed -i "59 c listen_addresses='*'" /etc/postgresql/12/main/postgresql.conf
sed -i "$ a host all all 0.0.0.0/0 trust" /etc/postgresql/12/main/pg_hba.conf
sudo ufw allow 5432/tcp
sudo systemctl restart postgresql
""",
                )

                print(colored("Successfully created instances!", "green"))
                print(
                    "Number of instances created in Ohio: {0}".format(
                        len(ec2_instances)
                    )
                )
                for i in range(len(ec2_instances)):
                    # use the boto3 waiter
                    ec2_instances[i].wait_until_running()
                    # reload the instance object
                    ec2_instances[i].reload()
                    public_ip = ec2_instances[i].public_ip_address
                    print("{0}) Public IPv4 Address: {1}".format(i + 1, public_ip))

            except:
                print(colored("Failed to create Ohio instances. Try again!\n", "red"))
        else:
            public_ip = myInstanceList[0].public_ip_address
            print("Running instances unchanged. Continuing...")
        print(
            colored(
                "Ohio setup complete. Proceeding to North Virginia setup...\n",
                "green",
            )
        )
        return public_ip
    else:
        try:
            security_group = client.create_security_group(
                GroupName="Database-SG", Description="Security group for the Database."
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
                        "FromPort": 5432,
                        "ToPort": 5432,
                        "IpRanges": [{"CidrIp": "0.0.0.0/0"}],
                    },
                ],
            )
            print("Database security group successfully created. Continuing...")
        except:
            print("Database security group already exists. Continuing...")
        try:
            ec2_instances = ec2.create_instances(
                TagSpecifications=[
                    {
                        "ResourceType": "instance",
                        "Tags": [
                            {"Key": "Name", "Value": "DB-Instance"},
                            {"Key": "Owner", "Value": "Pedro Ramos"},
                            {"Key": "Application", "Value": "Database Server"},
                        ],
                    },
                ],
                ImageId="ami-07efac79022b86107",
                KeyName=key_name,
                MinCount=1,
                MaxCount=1,
                InstanceType="t2.micro",
                SecurityGroups=["Database-SG"],
                UserData="""#!/bin/sh
sudo apt update
sudo apt install postgresql postgresql-contrib -y
sudo -u postgres psql -c "CREATE USER cloud WITH PASSWORD 'cloud';"
sudo -u postgres createdb -O cloud tasks
sudo sed -i "59 c listen_addresses='*'" /etc/postgresql/12/main/postgresql.conf
sudo sed -i "$ a host all all 0.0.0.0/0 trust" /etc/postgresql/12/main/pg_hba.conf
sudo ufw allow 5432/tcp
sudo systemctl restart postgresql
""",
            )

            print(colored("Successfully created instances!", "green"))
            print("Number of instances created in Ohio: {0}".format(len(ec2_instances)))
            for i in range(len(ec2_instances)):
                # use the boto3 waiter
                ec2_instances[i].wait_until_running()
                # reload the instance object
                ec2_instances[i].reload()
                public_ip = ec2_instances[i].public_ip_address
                print("{0}) Public IPv4 Address: {1}".format(i + 1, public_ip))
            print(
                colored(
                    "Ohio setup complete. Proceeding to North Virginia setup...\n",
                    "green",
                )
            )
            return public_ip
        except Exception as e:
            print(e)
            print(colored("Failed to create Ohio instances. Try again!\n", "red"))