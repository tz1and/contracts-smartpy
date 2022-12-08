import smartpy as sp

from tezosbuilders_contracts_smartpy.tzbrc import SupportedInterfaces


class SupportedInterfacesTest(
    SupportedInterfaces.SupportedInterfaces,
    sp.Contract):
    def __init__(self, supported_interaces):
        sp.Contract.__init__(self)
        SupportedInterfaces.SupportedInterfaces.__init__(self, supported_interaces)


@sp.add_test(name = "SupportedInterfaces_tests", profile = True)
def test():
    admin = sp.test_account("Administrator")
    alice = sp.test_account("Alice")
    bob   = sp.test_account("Robert")
    scenario = sp.test_scenario()

    scenario.h1("SupportedInterfaces contract")
    scenario.table_of_contents()

    # Let's display the accounts:
    scenario.h2("Accounts")
    scenario.show([admin, alice, bob])

    scenario.h2("Test SupportedInterfaces")

    test_interfaces = sp.set([
        sp.pair("TZBRC", sp.nat(1)),
        sp.pair("TZ1", sp.nat(666)),
        sp.pair("VIP", sp.nat(1337))]
    )

    scenario.h3("Contract origination")
    supported_interaces = SupportedInterfacesTest(test_interfaces)
    scenario += supported_interaces

    #
    # view: supported_interfaces
    #
    scenario.h3("view: supported_interfaces")

    res = scenario.compute(supported_interaces.supported_interfaces())
    scenario.show(res)
    scenario.verify_equal(res, test_interfaces)