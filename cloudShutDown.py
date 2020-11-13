from termcolor import colored
from terminateInstancesNorthVirgina import terminateNorthVirginia
from terminateInstancesOhio import terminateOhio
from deleteLoadBalancer import shutDownLoadBalancer
from deleteAutoScalingGroup import shutDownASG


def main():
    print("\n")
    shutDownASG()
    shutDownLoadBalancer()
    terminateOhio()
    terminateNorthVirginia()
    print(colored("Cloud shut down complete!\n", "green"))


main()