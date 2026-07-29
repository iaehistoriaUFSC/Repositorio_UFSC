from app.taxonomy import LexicalPrototypeClassifier


def test_taxonomy_has_current_assignable_classes():
    classifier = LexicalPrototypeClassifier()
    assert len(classifier.classes) == 44
    assert "5.3" not in classifier.classes
    assert "5.3.6.1" in classifier.classes


def test_lexical_classifier_is_deterministic_and_ranked():
    classifier = LexicalPrototypeClassifier()
    first = classifier.classify("The river of time carries history forward.", top_k=5)
    second = classifier.classify("The river of time carries history forward.", top_k=5)
    assert first == second
    assert len(first) == 5
    assert first[0].similarity >= first[1].similarity
    assert first[0].method == "annotated-sample-word-char-tfidf-v1"

