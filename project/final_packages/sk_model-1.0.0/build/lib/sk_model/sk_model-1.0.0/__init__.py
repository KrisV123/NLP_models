from spacy.language import Language, BaseDefaults
from ..syntax_iterators import SYNTAX_ITERATORS

class CustomDefaults(BaseDefaults):
    syntax_iterators = SYNTAX_ITERATORS


class CustomSlovakLanguage(Language):
    lang = 'sk'
    Defaults = CustomDefaults


__all__ = ['CustomSlovakLanguage']
