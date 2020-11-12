from termcolor import colored
from terminateInstancesNorthVirgina import terminateNorthVirginia
from terminateInstancesOhio import terminateOhio
from deleteLoadBalancer import shutDownLoadBalancer


def main():
    print("\n")
    shutDownLoadBalancer()
    terminateOhio()
    terminateNorthVirginia()
    print(colored("Cloud shut down complete!\n", "green"))


main()