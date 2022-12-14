from typing import Any, List, Tuple, Callable
import smartpy as sp


# Required mixins: Administrable
class MetaSettings:
    """IMPORTANT: Must be initialised after all eps using meta settings but
    before Upgradeable, in order to work correctly."""
    def __init__(self, lazy_ep = True):
        if self.available_settings:
            t_update_settings_params = sp.TList(sp.TVariant(**{setting[0]: setting[1] for setting in self.available_settings}))

            def update_settings(self, params):
                """Allows the administrator to update various settings.
                
                Parameters are metaprogrammed with self.available_settings"""
                self.onlyAdministrator()

                with sp.for_("update", params) as update:
                    with update.match_cases() as arg:
                        for setting in self.available_settings:
                            with arg.match(setting[0]) as value:
                                if setting[2] != None:
                                    setting[2](value)
                                setattr(self.data, setting[0], value)

            self.update_settings = sp.entry_point(update_settings, lazify=lazy_ep, parameter_type=t_update_settings_params)
        else: print(f"\x1b[33;20mWARNING: MetaSettings used in {self.__class__.__name__} but available_settings is empty!\x1b[0m")

    def addMetaSettings(self, settings: List[Tuple[str, sp.Expr, None | Callable[[sp.Expr], sp.Expr]]]):
        """Add one of more settings in form of a list of tuples."""
        if hasattr(self, 'available_settings'):
            self.available_settings.extend(settings)
        else: self.available_settings = settings