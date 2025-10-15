# Slovak NLP models for Spacy framework

A collection of 3 fully-trained CNN models for Slovak Language designed for lightweight usage.
Every model include morphologizer, parser, tagger and trainable lemmatizer.
The package also contains algorithm for phrase generation and text summarization and simple noun phrases extraction.
Requires Spacy 3.x

##### disclamer

It is recomended to test the models, if accuracy is sufficient before using in production. More detailed informations about models is in their own README documents. Similary with all other algorithms

### 1. sk_regular_model

- trained on sentences from newspaper articles
- best for common texts with basic sentence structures

### 2. sk_specified_model

- trained on legal documents
- best on texts without typical sentence structure with bullet points, paragraphs, ect. and simillar documents

### 3. sk_model

- combination of two previous models
- best for situation, where structure of text isn't known
- with smaller accuracy


## Usage (recomended)

1. create virtual enviroment
2. install spacy framework and pytextrank module `pip install spacy pytextrank`
3. install model via `pip install project/final_packages/"model_name"`

next can be used with tools from project/tools/text_rank.py

#### Example

```python
from project.tools.text_rank import phrase_generator, text_summarization
from project.tools.test_texts import real_article

summary = text_summarization('sk_model', real_article, 4)
phrases = phrase_generator('sk_model', real_article, 5, 2, 5)
```

in case of using and modifying whole repository, better option will be using all dependencies in requirements.txt `pip install -r requirements.txt`

## Credits

Sources for training:

- [UD Slovak-SNK Treebank](https://github.com/UniversalDependencies/UD_Slovak-SNK) — Part of Speech and Dependency relations (CC BY-SA 4.0)
- [Jazykovedný ústav Ľudovíta Štúra](https://www.juls.savba.sk/data.html?) — Morphological and syntactic annotations (CC BY-SA 4.0)