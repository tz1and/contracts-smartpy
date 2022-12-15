from typing import Any, Dict
import smartpy as sp


def getPrevSettingsFields(contract) -> Dict[str, Any]:
    if hasattr(contract.storage, "settings"):
        return contract.storage.settings.fields
    return {}