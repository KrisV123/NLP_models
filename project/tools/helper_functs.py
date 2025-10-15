import spacy
from spacy.tokens import DocBin
from spacy.training import Example

def get_full_text(nlp: spacy.language.Language, train_doc: str, output: str) -> None:
    doc_bin = DocBin().from_disk(train_doc)
    docs = list(doc_bin.get_docs(vocab=nlp.vocab))

    sent_list = [doc.text.rstrip(' ') for doc in docs]
    sent_str = ' '.join(sent_list)

    with open(output, 'wb') as f:
        f.write(sent_str.encode('utf-8'))


def create_pretrain_json(nlp: spacy.language.Language, train_doc: str, output: str) -> None:

    doc_bin = DocBin().from_disk(train_doc)
    docs = list(doc_bin.get_docs(vocab=nlp.vocab))

    PRETRAIN_DATA_LIST = list()
    for doc in docs:
        text_buffer: list[str] = list()
        for char in doc.text:
            if char == '"':
                text_buffer.append("\\")
            text_buffer.append(char)
        format_text = ''.join(text_buffer)

        data = '{' + f'"text": "{format_text}"' + '}'
        PRETRAIN_DATA_LIST.append(data)

    PRETRAIN_DATA = '\n'.join(PRETRAIN_DATA_LIST).encode('utf-8')

    with open(output + '/pretrain.jsonl', 'wb') as f:
        f.write(PRETRAIN_DATA)


def get_exapmles_from_spacy(nlp: spacy.language.Language, train_doc: str) -> list[Example]:
    doc_bin = DocBin().from_disk(train_doc)
    docs = list(doc_bin.get_docs(vocab=nlp.vocab))

    print('Making examples list')

    examples = list()
    for doc in docs:
        examples.append(Example(nlp.make_doc(doc.text), doc))

    print('Examples list finished!')
    return examples


def make_custom_example(nlp: spacy.language.Language, train_doc: str) -> list[Example]:
    doc_bin = DocBin().from_disk(train_doc)
    docs = list(doc_bin.get_docs(vocab=nlp.vocab))

    print('Making examples list')

    examples = list()
    for doc in docs:
        example = Example.from_dict(
            nlp.make_doc(doc.text),
            {
                "words": [token.text for token in doc],
                "heads": [token.head.i for token in doc],
                "deps": [token.dep_ for token in doc],
                "sent_starts": [bool(token.is_sent_start) for token in doc]
            }
        )
        examples.append(example)

    print('Examples list finished!')
    return examples
