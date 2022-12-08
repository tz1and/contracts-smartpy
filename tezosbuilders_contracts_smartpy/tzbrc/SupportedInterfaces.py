import smartpy as sp


t_interface_pair = sp.TPair(sp.TString, sp.TNat)
t_supported_interfaces = sp.TSet(t_interface_pair)

# Required mixins: Administrable
class SupportedInterfaces:
    def __init__(self, supported_interfaces):
        self.update_initial_storage(
            supported_interfaces = sp.big_map({"": sp.set_type_expr(supported_interfaces, t_supported_interfaces)})
        )

    @sp.onchain_view(pure=True)
    def supported_interfaces(self):
        """Returns the contract's supported interfaces."""
        with sp.set_result_type(t_supported_interfaces):
            sp.result(self.data.supported_interfaces.get("", message=sp.unit))
