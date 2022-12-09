import smartpy as sp

# TODO: update_ep variant layout?


# Mixins required: Administrable
class Upgradeable:
    """IMPORTANT: Must be initialised after any mixins that add lazy
    entrypoints, in order to work correctly."""
    def __init__(self):
        default_lazy = ["lazy-entry-points"] in self.flags

        # get lazy entry points
        self.upgradeable_entrypoints = []
        for f in dir(self):
            attr = getattr(self, f)
            if isinstance(attr, sp.Entrypoint) and (attr.message.lazify == True or (attr.message.lazify == None and default_lazy)):
                self.upgradeable_entrypoints.append(attr.message.fname)

        # if there are any, add the update ep
        if self.upgradeable_entrypoints:
            #print(f'{self.__class__.__name__}: {self.upgradeable_entrypoints}')
            def update_ep(self, params):
                # Build a variant from upgradeable_entrypoints.
                sp.set_type(params.ep_name, sp.TVariant(
                    **{entrypoint: sp.TUnit for entrypoint in self.upgradeable_entrypoints}))
                self.onlyAdministrator()

                # Build a matcher for upgradeable_entrypoints
                with params.ep_name.match_cases() as arg:
                    for entrypoint in self.upgradeable_entrypoints:
                        with arg.match(entrypoint):
                            sp.set_entry_point(entrypoint, params.new_code)

            self.update_ep = sp.entry_point(update_ep, lazify=False)
        else: print(f"\x1b[33;20mWARNING: Upgradeable used in {self.__class__.__name__} but upgradeable_entrypoints is empty!\x1b[0m")
