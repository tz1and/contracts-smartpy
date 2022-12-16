import smartpy as sp

from tz1and_contracts_smartpy.mixins.Administrable import Administrable
from tz1and_contracts_smartpy.mixins.ContractMetadata import ContractMetadata
from tz1and_contracts_smartpy.mixins.MetaSettings import MetaSettings
from tz1and_contracts_smartpy.mixins.Pausable import Pausable
from tz1and_contracts_smartpy.mixins.Upgradeable import Upgradeable

from tz1and_contracts_smartpy.utils import Utils


# Let's create a new contract that can count.
class Counter(
    # Of course it needs to be a smartpy contract!
    sp.Contract,
    # The administrable mixin adds a transferrable owner to the contract,
    # as well as related entrypoints and some functions to check the owner.
    # Most other mixins require it.
    Administrable,
    # ContractMetadata adds standard compliant contract metadata to the
    # contract and provides and interface for updating it - either and entry
    # point or through MetaSettings, if used.
    ContractMetadata,
    # Pausable adds a paused state. You need to check it with the isPaused,
    # onlyUnpaused or onlyPaused functions it adds.
    Pausable,
    # If the MetaSettings mixin is used, all the other mixins that have
    # configurable settings combine their settings into a single entrypoint.
    # You can also add other settings to it.
    MetaSettings,
    # Upgradeable automatically adds an entrypoint to upgrade lazy entrypoints.
    Upgradeable
):
    def __init__(self, admin, metadata):
        # The order how things are inited matters. Frist, sp.Contract.
        sp.Contract.__init__(self)

        # Let's add our counter to storage.
        self.init_storage(
            counter = sp.nat(0)
        )

        # We can add more settings to the MetaSettings mixin.
        # Settings take a name (the variable name in storage), the default value,
        # the type and an optional lambda for validation (can be None).
        #
        # The settings added through MetaSettings don't need to be added to
        # storage manually.
        self.addMetaSettings([
            ("increment", 1, sp.TNat, lambda x : sp.verify(x >= sp.nat(1)))
        ])

        # Now we initialise the mixins. Order matters for some!
        Administrable.__init__(self, admin)
        # SmartPy unfortunately has a little cycle for generating metadata.
        # The contract metadata is generated on compile, but you already must know
        # the contract metadata at compile time to put it into storage.
        # Is OK, we just compile twice before deploy :>.
        # You can find the generated metadata in the compiler output.
        ContractMetadata.__init__(self, metadata)
        Pausable.__init__(self)
        # MetaSettings must be initialised after any mixin that might use it!
        MetaSettings.__init__(self)
        # Upgradeable should be last, as some mixins (optionally) add entrypoints
        # as lazy.
        Upgradeable.__init__(self)

        # Let's also generate some contract metadata here.
        # You can specify a lot more than just a name and description.
        # See the docstring for more options.
        self.generateContractMetadata(
            name="The little counter that could",
            description="Count, that is.")

    # Now, our glorious, metasetting using, pausable, upgradeable increment ep!
    @sp.entry_point(lazify=True, parameter_type=sp.TUnit)
    def increment(self):
        # This will fail the operation if sender is not the admin.
        self.onlyAdministrator()

        # This will fail the operation if the contract is paused.
        self.onlyUnpaused()

        # Add increment to counter.
        self.data.counter += self.data.settings.increment

        # All done! ^.~
        # Look at the tests as well!