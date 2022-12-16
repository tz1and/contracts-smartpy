from typing import List, Tuple, Callable
import smartpy as sp


# Required mixins: Administrable
class MetaSettings:
    """IMPORTANT: Must be initialised after all eps using meta settings but
    before Upgradeable, in order to work correctly."""
    def __init__(self, include_views = False, lazy_ep = True):
        if not hasattr(self, '_available_settings'): self._available_settings = []
        if not hasattr(self, '_available_settings_top_level'): self._available_settings_top_level = []

        # storage for grouped settings
        if self._available_settings:
            self.update_initial_storage(
                settings = sp.record(**{setting[0]: sp.set_type_expr(setting[1], setting[2]) for setting in self._available_settings}),
            )

        # storage for top level settings
        if self._available_settings_top_level:
            self.update_initial_storage(
                **{setting[0]: sp.set_type_expr(setting[1], setting[2]) for setting in self._available_settings_top_level}
            )

        # TODO: make sure settings names are unique across both levels
        joined_settings = self._available_settings + self._available_settings_top_level
        if not joined_settings:
            raise Exception(f"MetaSettings used in {self.__class__.__name__} but no settings defined!")

        t_update_settings_params = sp.TList(sp.TVariant(**{setting[0]: setting[2] for setting in joined_settings}))

        # Add update_settings entrypoint.
        def update_settings(self, params):
            """Allows the administrator to update various settings.
            
            Parameters are metaprogrammed with self.addMetaSettings"""
            self.onlyAdministrator()

            # If grouped settings exist, make a local copy.
            # This results in fewer ops.
            if self._available_settings:
                settings_local = sp.local("settings_local", self.data.settings)
            
            # Update settings.
            with sp.for_("update", params) as update:
                with update.match_cases() as arg:
                    for setting in joined_settings:
                        with arg.match(setting[0]) as value:
                            if setting[3] != None:
                                setting[3](value)
                            if setting in self._available_settings:
                                setattr(settings_local.value, setting[0], value)
                            else:
                                setattr(self.data, setting[0], value)

            # If grouped settings exist, write back the local copy.
            if self._available_settings:
                self.data.settings = settings_local.value
        self.update_settings = sp.entry_point(update_settings, lazify=lazy_ep, parameter_type=t_update_settings_params)

        # Add get_settings view if top-level settings exist
        if include_views and self._available_settings_top_level:
            def get_settings(self):
                sp.result(self.data.settings)
            self.get_settings = sp.onchain_view(pure=True)(get_settings)

    def addMetaSettings(self, settings: List[Tuple[str, sp.Expr, sp.Expr, None | Callable[[sp.Expr], sp.Expr]]], top_level=False):
        """Add one of more settings in form of a list of tuples of:
        (setting_name, default, type, validation_lambda)."""
        if top_level:
            if hasattr(self, '_available_settings_top_level'):
                self._available_settings_top_level.extend(settings)
            else: self._available_settings_top_level = settings
        else:
            if hasattr(self, '_available_settings'):
                self._available_settings.extend(settings)
            else: self._available_settings = settings