# -*- coding: utf-8 -*-

"""
Term-document Matrix class.
"""

import numpy as np
from typing import Dict, Tuple
from textarium.corpus import Corpus
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from prettytable import PrettyTable

class TermDocMatrix:
    def __init__(self, vectorizer_type: str, ngram_range: Tuple = (1, 1), analyzer: str = 'word'):
        self.type = vectorizer_type
        self.ngram_range = ngram_range
        self.analyzer = analyzer
        self.matrix = None
        self.vectorizer = None
        self.tokens = None

    def from_corpus(self, corpus: Corpus, use_raw : bool = False):
        """Generate term-doc matrix from Corpus texts.

        Args:
            corpus (Corpus): Corpus class object.

        Raises:
            Exception: If provided TermDocMatrix 'type' parameter does not exist.
        """
        if self.type == 'count':
            self.vectorizer = CountVectorizer(ngram_range=self.ngram_range, analyzer=self.analyzer)
        elif self.type == 'tfidf':
            self.vectorizer = TfidfVectorizer(ngram_range=self.ngram_range, analyzer=self.analyzer)
        else:
            raise Exception("There is no such type")
        self.matrix = self.vectorizer.fit_transform(corpus.to_array(use_raw=use_raw))
        self.tokens = self.vectorizer.get_feature_names_out()

    def term_frequency(self, ascending=False, print_n: int = 10) -> Dict:
        """Calculate frequencies for each term.

        Args:
            ascending (bool, optional): Sorting order. Defaults to False.
            print_n (int, optional): Number of top elements to print. Defaults to 10.

        Returns:
            Dict: A sorted dictionary with term frequencies.
        """
        if self.type != 'count':
            raise Exception("Available only for TermDocMatrix generated with CountVectorizer")
        freqs = dict(zip(self.tokens, np.squeeze(np.asarray(self.matrix.sum(axis=0)))))
        sorted_freqs = dict(sorted(freqs.items(), key=lambda item: item[1], reverse=not ascending)[:print_n])
        tab = PrettyTable(["Term", "Count"])
        for k, v in sorted_freqs.items():
            tab.add_row([k, v])
        print(tab)
        return sorted_freqs

    def term_doc_frequency(self, ascending=False, print_n: int = 10) -> Dict:
        """Calculate term-doc frequencies for each term.

        Args:
            ascending (bool, optional): Sorting order. Defaults to False.
            print_n (int, optional): Number of top elements to print. Defaults to 10.

        Returns:
            Dict: A sorted dictionary with term-doc frequencies.
        """
        if self.type != 'count':
            raise Exception("Available only for TermDocMatrix generated with CountVectorizer")
        freqs = dict(zip(self.tokens, np.squeeze(np.asarray(self.matrix.astype(bool).sum(axis=0)))))
        sorted_freqs = dict(sorted(freqs.items(), key=lambda item: item[1], reverse=not ascending)[:print_n])
        tab = PrettyTable(["Term", "Count"])
        for k, v in sorted_freqs.items():
            tab.add_row([k, v])
        print(tab)
        return sorted_freqs



    

