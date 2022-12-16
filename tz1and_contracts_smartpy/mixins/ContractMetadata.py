from typing import List
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
    """(Mixin) Provide an interface to include and update tzip 16 metadata.

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

    def generateContractMetadata(self, name: str, description: str, interfaces: List[str] = [],
        authors: List[str] = [], homepage: str = "", source_location: str = "",
        license: str = "", version: str = "1.0.0", include_offchain_views: bool = True):
        """Generate a metadata json file, optionally with all the contract's
        views as offchain views.
        
        `name`: the name of the contract.
        `description`: the contracts description.
        `interfaces`: interfaces implemented. TZIP-016 is added by defualt.
        `authors`: list of authors. Omitted if empty.
        `homepage`: Url of homepage. Omitted if empty.
        `source_location`: Url of source code. Omitted if empty.
        `license`: The SPDX license identifier. Omitted if empty.
        `version`: The version of the contract. 1.0.0 by default.
        `include_offchain_views`: Whether to include offchain views in the metadata."""
        # Generate the basic metadata.
        metadata_base = {
            "name": name,
            "description": description,
            "version": version,
            "interfaces": ["TZIP-016"] + interfaces,
            "source": {
                "tools": ["SmartPy", "tz1and-smart-contracts"]
            }
        }

        # Add optional fields.
        if authors: metadata_base["authors"] = authors
        if homepage: metadata_base["homepage"] = homepage
        if source_location: metadata_base["source"]["location"] = source_location
        if license:  metadata_base["license"] = { "name": license }

        # Add offchain views.
        if include_offchain_views:
            offchain_views = []
            for f in dir(self):
                attr = getattr(self, f)
                if isinstance(attr, sp.OnOffchainView):
                    # Include onchain views as tip 16 offchain views
                    offchain_views.append(attr)
        metadata_base["views"] = offchain_views
        self.init_metadata("metadata_base", metadata_base)