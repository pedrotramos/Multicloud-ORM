from termcolor import colored
from launchOhio import launchOhioInstances
from launchNorthVirginia import launchNorthVirginiaInstances
from createLoadBalancer import launchLoadBalancer
from createAutoScalingGroup import launchASG


def main():
    print("\n")
    ipOhio = launchOhioInstances()
    launchNorthVirginiaInstances(ipOhio)
    launchLoadBalancer()
    launchASG()
    print(colored("Build complete!\n", "green"))
    print("In a couple of minutes the service should be available for access.\n")


main()