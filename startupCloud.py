from launchOhio import launchOhioInstances
from launchNorthVirginia import launchNorthVirginiaInstances
from createLoadBalancer import launchLoadBalancer


def main():
    print("\n")
    ipOhio = launchOhioInstances()
    launchNorthVirginiaInstances(ipOhio)
    launchLoadBalancer()


main()