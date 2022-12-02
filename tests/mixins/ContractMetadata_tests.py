import smartpy as sp

Administrable = sp.io.import_script_from_url("file:contracts/mixins/Administrable.py").Administrable
MetaSettings = sp.io.import_script_from_url("file:contracts/mixins/MetaSettings.py").MetaSettings
contract_metadata_mixin = sp.io.import_script_from_url("file:contracts/mixins/ContractMetadata.py")


class ContractMetadataTest(
    Administrable,
    contract_metadata_mixin.ContractMetadata,
    sp.Contract):
    def __init__(self, administrator, metadata):
        Administrable.__init__(self, administrator = administrator)
        contract_metadata_mixin.ContractMetadata.__init__(self, metadata = metadata)


class ContractMetadataTestMetaSettings(
    ContractMetadataTest,
    MetaSettings):
    def __init__(self, administrator, metadata):
        self.available_settings = []

        ContractMetadataTest.__init__(self, administrator = administrator, metadata = metadata)
        MetaSettings.__init__(self)


@sp.add_test(name = "ContractMetadata_tests", profile = True)
def test():
    admin = sp.test_account("Administrator")
    alice = sp.test_account("Alice")
    bob   = sp.test_account("Robert")
    scenario = sp.test_scenario()

    scenario.h1("ContractMetadata contract")
    scenario.table_of_contents()

    # Let's display the accounts:
    scenario.h2("Accounts")
    scenario.show([admin, alice, bob])

    scenario.h2("Test ContractMetadata")

    scenario.h3("Contract origination")
    initial_metadata = sp.utils.metadata_of_url("https://initial_meta.com")
    change_metadata = ContractMetadataTest(admin.address, initial_metadata)
    scenario += change_metadata

    # check default
    scenario.verify(change_metadata.data.metadata[""] == initial_metadata[""])

    #
    # set_metadata
    #
    scenario.h3("set_metadata")

    new_metadata = sp.utils.metadata_of_url("https://new_meta.com")

    # No permission for anyone but admin.
    for acc in [bob, alice, admin]:
        change_metadata.set_metadata(new_metadata).run(
            sender = acc,
            valid = (True if acc is admin else False),
            exception = (None if acc is admin else "ONLY_ADMIN"))

        if acc is admin: scenario.verify(change_metadata.data.metadata[""] == new_metadata[""])

    # Test meta settings.
    scenario.h2("Test ContractMetadata - MetaSettings")

    scenario.h3("Contract origination")
    initial_metadata = sp.utils.metadata_of_url("https://new_meta.com")
    change_metadata_meta = ContractMetadataTestMetaSettings(admin.address, initial_metadata)
    scenario += change_metadata_meta

    # check default
    scenario.verify(change_metadata_meta.data.metadata[""] == initial_metadata[""])

    #
    # update_settings
    #
    scenario.h3("update_settings")

    new_metadata = sp.utils.metadata_of_url("https://new_meta.com")

    # No permission for anyone but admin.
    for acc in [bob, alice, admin]:
        change_metadata_meta.update_settings([sp.variant("metadata", new_metadata)]).run(
            sender = acc,
            valid = (True if acc is admin else False),
            exception = (None if acc is admin else "ONLY_ADMIN"))

        if acc is admin: scenario.verify(change_metadata_meta.data.metadata[""] == new_metadata[""])