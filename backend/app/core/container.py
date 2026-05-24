from app.core.settings import Settings, get_settings

class Container:
    # ============================================================
    # CORE CONFIG (SINGLE SOURCE OF TRUTH)
    # ============================================================
    settings: Settings = get_settings()