import smartpy as sp

from tz1and_contracts_smartpy.mixins.MetaSettings import MetaSettings


def contractSetMetadata(contract, metadata_uri):
    """ContractMetadata set_metadata."""
    set_metadata_handle = sp.contract(
        sp.TBigMap(sp.TString, sp.TBytes),
        sp.set_type_expr(contract, sp.TAddress),
        entry_point='set_metadata').open_some()
    sp.transfer(sp.big_map({"": sp.set_type_expr(metadata_uri, sp.TBytes)}),
        sp.mutez(0), set_metadata_handle)


# Mixins required: Administrable
class ContractMetadata:
    """(Mixin) Provide an interface to update tzip 16 metadata.

    Requires the `Administrable` mixin.
    """
    def __init__(self, metadata):
        # Add metadata as top-level element, according to the tzip specs.
        if isinstance(self, MetaSettings):
            self.addMetaSettings([
                ("metadata", metadata, sp.TBigMap(sp.TString, sp.TBytes), None)
            ], True)
        else:
            self.update_initial_storage(
                metadata = sp.set_type_expr(metadata, sp.TBigMap(sp.TString, sp.TBytes))
            )

            def set_metadata(self, metadata):
                """(Admin only) Set the contract metadata."""
                self.onlyAdministrator()
                self.data.metadata = metadata
            
            self.set_metadata = sp.entry_point(set_metadata, parameter_type=sp.TBigMap(sp.TString, sp.TBytes))