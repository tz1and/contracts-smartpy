import smartpy as sp


# Mixins required: Administrable
class Pausable:
    def __init__(self, paused = False, include_views = True):
        self.update_initial_storage(
            paused = paused
        )

        if hasattr(self, 'available_settings'):
            self.available_settings.append(
                ("paused", sp.TBool, None)
            )
        else:
            def set_paused(self, new_paused):
                self.onlyAdministrator()
                self.data.paused = new_paused
            
            self.set_paused = sp.entry_point(set_paused)

        if include_views:
            def is_paused(self):
                sp.result(self.isPaused())

            self.is_paused = sp.onchain_view(pure=True)(is_paused)

    def isPaused(self):
        return self.data.paused

    def onlyUnpaused(self):
        sp.verify(self.isPaused() == False, 'ONLY_UNPAUSED')

    def onlyPaused(self):
        sp.verify(self.isPaused() == True, 'ONLY_PAUSED')
