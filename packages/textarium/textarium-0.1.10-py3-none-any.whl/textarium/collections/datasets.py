# -*- coding: utf-8 -*-

"""
Datasets.
"""

import os
from typing import List
from textarium import Corpus

def load_bbc_dataset() -> Corpus:
    dataset = []
    data_folder_path = os.path.join(os.path.dirname(__file__), 'datasets/bbc/')
    category_folders = [f for f in os.listdir(data_folder_path) if os.path.isdir(os.path.join(data_folder_path, f))]
    for category in category_folders:
        article_folder_path = os.path.join(data_folder_path, category)
        for file in os.listdir(article_folder_path):
            try:
                article_file_path = os.path.join(article_folder_path, file)
                with open(article_file_path, 'r') as article_file:
                    article_text = ' '.join([line.rstrip() for line in article_file.readlines()])
                    dataset.append(article_text)
            except Exception as e:
                raise Exception(
                    f"Error processing {article_file_path}: {e}"
                )
    return Corpus(dataset, lang='en')