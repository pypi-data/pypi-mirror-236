from locallang.lang import LangInit

try:
    from locallang.lang import Localisation
except:
    pass

__version__ = "0.0.8"
__all__ = ["LangInit", "Localisation"]
