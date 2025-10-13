from pathlib import Path
from spacy.util import load_model_from_init_py, get_model_meta

from . import syntax_iterators

__version__ = get_model_meta(Path(__file__).parent)['version']


def load(**overrides):
    noun_chunks = getattr(syntax_iterators, 'noun_chunks')
    nlp = load_model_from_init_py(__file__, **overrides)
    nlp.vocab.get_noun_chunks = noun_chunks
    return nlp
