# -*- coding: utf-8 -*-

"""
Text class.
"""

from typing import List
from textarium.utils import pipeline
from textarium.extraction import extract_keywords
import textarium.preprocessing as tp

class Text:
    def __init__(self, text: str, lang: str = 'en'):
        self.lang = lang
        self.raw_text = text
        self.prepared_text = None
        self.keywords = None

    def __str__(self) -> str:
        if not self.prepared_text:
            return self.raw_text[:100]
        else:
            return self.prepared_text[:100]

    def prepare(
        self, 
        lemmatize: bool = True, 
        get_keywords: bool = True,
        keywords_method: str = 'yake',
        stopwords: List[str] = None
    ):
        """Prepares text for analysis and ML modeling:
            - Removes punctuation, digits and extra spaces
            - Removes stopwords, html-tags and urls
            - Lemmatizes all words
            - Extract keywords using various approaches

        Returns:
            str: A prepared string
        """
        text = pipeline(self.raw_text, 
            [
                tp.remove_html,
                tp.remove_urls,
                tp.remove_digits,
                tp.make_lowercase,
                tp.remove_punctuation,
            ]
        )
        if lemmatize:
            text = tp.lemmatize(text, lang=self.lang)
        if stopwords:
            text = tp.remove_words(text, words_to_exclude=stopwords)
        if get_keywords:
            self.keywords = extract_keywords(text, lang=self.lang, method=keywords_method)
        self.prepared_text = text

