# Copyright 2022 Thinh Vu @ GitHub
# See LICENSE for details.

from .Document_Classifier import DocumentClassifier

def classify(data_path):
    classifier = DocumentClassifier()
    classifier(data_path)