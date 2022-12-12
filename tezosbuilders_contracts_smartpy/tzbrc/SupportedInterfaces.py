from enum import Enum
import smartpy as sp


t_interface_pair = sp.TPair(sp.TString, sp.TNat)
t_supported_interfaces = sp.TSet(t_interface_pair)

class StorageLevel(Enum):
    BigMap = 1
    TopLevel = 2
    Inline = 3

class SupportedInterfaces:
    def __init__(self, supported_interfaces_set, interface_storage = StorageLevel.Inline):
        self.interface_storage = interface_storage
        match self.interface_storage:
            case StorageLevel.BigMap:
                self.update_initial_storage(
                    supported_interfaces = sp.big_map({"": sp.set_type_expr(supported_interfaces_set, t_supported_interfaces)})
                )
            
            case StorageLevel.TopLevel:
                self.update_initial_storage(
                    supported_interfaces = sp.set_type_expr(supported_interfaces_set, t_supported_interfaces)
                )

            case StorageLevel.Inline:
                self.supported_interfaces_set = sp.set_type_expr(supported_interfaces_set, t_supported_interfaces)

        # TODO: Maybe MetaSettings or ep to update interfaces.
        #if (self.interface_storage is not StorageLevel.Inline):
        #    pass

    @sp.onchain_view(pure=True)
    def supported_interfaces(self):
        """Returns the contract's supported interfaces."""
        with sp.set_result_type(t_supported_interfaces):
            match self.interface_storage:
                case StorageLevel.BigMap:
                    sp.result(self.data.supported_interfaces.get("", message=sp.unit))
                
                case StorageLevel.TopLevel:
                    sp.result(self.data.supported_interfaces)

                case StorageLevel.Inline:
                    sp.result(self.supported_interfaces_set)
