"""
This script is related to phrase generator a text summarization and clean_sents.
Functions don't work all the time perfectly. In this case, there are few params
inside an input to fine-tune final output.
"""

import spacy
from spacy.tokens import Span
from spacy.util import registry
from spacy.language import Language
import pytextrank #type:ignore

from operator import itemgetter
from math import sqrt

def phrase_generator(model_name: str,
                     text: str,
                     phrase_ammount: int,
                     min_tok_ammount: int,
                     max_tok_ammount: int) -> list[tuple[float, str]]:
    """
    Returns cleaned phrases generated from noun phrase generator
    """

    @registry.misc("prefix_scrubber")
    def prefix_scrubber():
        def scrubber_func(span: Span) -> str:
            while len(span) > 1 and span[0].text in nlp.Defaults.stop_words:
                span = span[1:]

            for token in span:
                if token.pos_ not in ["DET", "PRON"]:
                    break
                else:
                    span = span[1:]

            return span.text
        return scrubber_func

    nlp = spacy.load(model_name)
    nlp.add_pipe('topicrank', config={"scrubber": {"@misc": "prefix_scrubber"}}, last=True)
    doc = nlp(text)

    phrases = [
        (phrase.rank, phrase.text.count(' ') + 1, phrase.text)
        for phrase in doc._.phrases
    ]
    phrases.sort(key=itemgetter(0))

    rel_phrases = list()
    count = 0
    for _, txt_len, txt in phrases:
        if txt_len >= min_tok_ammount and txt_len <= max_tok_ammount:
            rel_phrases.append(txt)
            count += 1
        if count == phrase_ammount:
            break

    return rel_phrases


def text_summarization(model_name: str,
                       text: str,
                       sents_ammount: int,
                       limit_phrases: int= 4) -> list[str]:
    """
    Returns most relevant sentences from article.

    sents_ammount: Returns most n rated sentenses from article\n
    limit_phrases: sets ammount of phrases, which will be used to count ranking (default 4)
    """

    nlp = spacy.load(model_name)
    nlp.add_pipe('textrank', last=True)

    doc = nlp(text)
    sent_bound = [[sent.start, sent.end, set()] for sent in doc.sents]
    unit_vector = list()

    for phrase_id, phrase in enumerate(doc._.phrases):
        unit_vector.append(phrase.rank)

        for chunk in phrase.chunks:
            for sent_start, sent_end, phrases_idx_set in sent_bound:
                assert isinstance(phrases_idx_set, set)

                if chunk.start >= sent_start and chunk.end <= sent_end:
                    phrases_idx_set.add(phrase_id)
                    break

        if phrase_id == limit_phrases:
            break

    def normalize_vector(vector) -> list[float]:
        summ = sum(vector)
        return [rank/summ for rank in vector]

    norm_unit_vect = normalize_vector(unit_vector)
    sent_rank: list[tuple[int, float]] = list()

    for sent_id, (_, _, phrases_idx_set) in enumerate(sent_bound):
        assert isinstance(phrases_idx_set, set)
        summ = 0.0
        for phrase_id in phrases_idx_set:
            summ += norm_unit_vect[phrase_id] ** 2.0

        sent_rank.append((sent_id, sqrt(summ)))

    sent_rank.sort(key=itemgetter(1), reverse=True)
    final_sents = sent_rank[:sents_ammount]

    sents_id = dict()
    sent_id = 0
    for sent in doc.sents:
        sents_id[sent_id] = sent.text
        sent_id += 1

    summary = [
        sents_id[id]
        for id, _ in sorted(final_sents, key=itemgetter(0))
        if id in sents_id
    ]

    return summary


def clean_sents(sents: list[str]) -> list[str]:
    """
    cleans sentenses into cleaner state.
    Meant to be used with text_summarization function.
    Potentially will be extended in future
    """

    cleaned_sents = list()
    for sent in sents:
        while sent[0] == ' ':
            sent = sent[1:]
        while sent[-1] == ' ':
            sent = sent[:-1]

        if sent[-1] != '.':
            if sent[-1] == ':':
                sent = sent[0:-1] + '.'
            else:
                sent = sent + '.'
        cleaned_sents.append(sent)
    return cleaned_sents
