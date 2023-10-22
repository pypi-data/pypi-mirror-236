

import enum
import typing

T_Result = typing.TypeVar("T_Result")


class ChunkSplitter(str, enum.Enum):
    """
    An enumeration.
    """

    CHARACTER_TEXT_SPLITTER = "CharacterTextSplitter"
    LANGUAGE = "Language"
    LATEX_TEXT_SPLITTER = "LatexTextSplitter"
    MARKDOWN_TEXT_SPLITTER = "MarkdownTextSplitter"
    NLTK_TEXT_SPLITTER = "NLTKTextSplitter"
    PYTHON_CODE_TEXT_SPLITTER = "PythonCodeTextSplitter"
    RECURSIVE_CHARACTER_TEXT_SPLITTER = "RecursiveCharacterTextSplitter"
    SENTENCE_TRANSFORMERS_TOKEN_TEXT_SPLITTER = "SentenceTransformersTokenTextSplitter"
    SPACY_TEXT_SPLITTER = "SpacyTextSplitter"
    TEXT_SPLITTER = "TextSplitter"
    TOKEN_TEXT_SPLITTER = "TokenTextSplitter"
    TOKENIZER = "Tokenizer"

    def visit(
        self,
        character_text_splitter: typing.Callable[[], T_Result],
        language: typing.Callable[[], T_Result],
        latex_text_splitter: typing.Callable[[], T_Result],
        markdown_text_splitter: typing.Callable[[], T_Result],
        nltk_text_splitter: typing.Callable[[], T_Result],
        python_code_text_splitter: typing.Callable[[], T_Result],
        recursive_character_text_splitter: typing.Callable[[], T_Result],
        sentence_transformers_token_text_splitter: typing.Callable[[], T_Result],
        spacy_text_splitter: typing.Callable[[], T_Result],
        text_splitter: typing.Callable[[], T_Result],
        token_text_splitter: typing.Callable[[], T_Result],
        tokenizer: typing.Callable[[], T_Result],
    ) -> T_Result:
        if self is ChunkSplitter.CHARACTER_TEXT_SPLITTER:
            return character_text_splitter()
        if self is ChunkSplitter.LANGUAGE:
            return language()
        if self is ChunkSplitter.LATEX_TEXT_SPLITTER:
            return latex_text_splitter()
        if self is ChunkSplitter.MARKDOWN_TEXT_SPLITTER:
            return markdown_text_splitter()
        if self is ChunkSplitter.NLTK_TEXT_SPLITTER:
            return nltk_text_splitter()
        if self is ChunkSplitter.PYTHON_CODE_TEXT_SPLITTER:
            return python_code_text_splitter()
        if self is ChunkSplitter.RECURSIVE_CHARACTER_TEXT_SPLITTER:
            return recursive_character_text_splitter()
        if self is ChunkSplitter.SENTENCE_TRANSFORMERS_TOKEN_TEXT_SPLITTER:
            return sentence_transformers_token_text_splitter()
        if self is ChunkSplitter.SPACY_TEXT_SPLITTER:
            return spacy_text_splitter()
        if self is ChunkSplitter.TEXT_SPLITTER:
            return text_splitter()
        if self is ChunkSplitter.TOKEN_TEXT_SPLITTER:
            return token_text_splitter()
        if self is ChunkSplitter.TOKENIZER:
            return tokenizer()
