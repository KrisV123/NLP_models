from typing import Iterator, Union, Tuple

from spacy.tokens import Doc, Span
import spacy

def noun_chunks(doclike: Union[Doc, Span]) -> Iterator[Tuple[int, int, int]]:
    LEFT_MODIFIERS = (
        "det",          # determinátor (ten, každý, môj...)
        "det:predet",   # predeterminátor (napr. všetky tie domy)
        "det:poss",     # posesívny determinátor (môj, tvoj)
        "amod",         # adjektívny prívlastok (krásny dom)
        "nummod",       # číslovka (tri domy)
        "nummod:gov",   # riadená číslovka (napr. päť litrov)
        "neg",          # negátor (napr. „nie“ pri adj. alebo príslovke)
        "case",         # predložkový marker pre nmod
    )

    RIGHT_MODIFIERS = (
        "nmod",         # nominal modifier (genitív, PP, atď.)
        "flat",         # ploché štruktúry, napr. mená (Bratislava mesto)
        "fixed",        # pevné viacslovné výrazy (idiomy)
        "xcomp",        # doplnková fráza (napr. „túžba byť lepší“)
    )

    INDEPEND_MODIFIERS = (
        "compound",     # viacslovné substantívne výrazy (napr. názvy)
        "acl",          # adnominal clause (napr. „stojaci pri bráne“)
        "acl:relcl",    # relatívna veta („ktorý prišiel“)
        "appos",        # apozícia (Bratislava, hlavné mesto)
        "vocative",     # vokatív (v osloveniach)
    )

    doc = doclike.doc
    np_label = doc.vocab.strings.add('NP')
    length = len(doc)

    for i, word in enumerate(doc):
        if word.pos_ not in ('NOUN', 'PRON', 'PROPN'):
            continue
        idx = i
        chunk = [word]

        while idx - 1 >= 0 and\
              (doc[idx - 1].dep_ in LEFT_MODIFIERS + INDEPEND_MODIFIERS\
               and doc[idx - 1].head in chunk):
            idx -= 1
            chunk.insert(0, doc[idx])

        idx = i
        while idx + 1 < length and\
              (doc[idx + 1].dep_ in RIGHT_MODIFIERS + INDEPEND_MODIFIERS\
               and doc[idx + 1].head in chunk):
            idx += 1
            chunk.append(doc[idx])

        yield (chunk[0].left_edge.i, chunk[-1].right_edge.i + 1, np_label)


SYNTAX_ITERATORS = {'noun_chunks': noun_chunks}
