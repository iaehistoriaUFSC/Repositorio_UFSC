from app.pipeline import PipelineConfig, _ensemble, analyze, segment_sentences
from app.workers.melbert_worker import WORD_RE as MELBERT_WORD_RE


class FakeRuntime:
    def detect(self, model_id, sentences, threshold):
        sentence = sentences[0]
        word = "river"
        start = sentence["text"].index(word)
        return [
            {
                "model_id": model_id,
                "sentence_id": sentence["id"],
                "sentence_text": sentence["text"],
                "word_index": 2,
                "word": word,
                "char_start": sentence["char_start"] + start,
                "char_end": sentence["char_start"] + start + len(word),
                "score": 0.8 if model_id == "xlmr" else 1.0,
                "is_metaphor": True,
                "score_semantics": "test",
            }
        ]


def test_sentence_segmentation_preserves_offsets():
    text = "History flows. Time stops!\nA new layer appears."
    rows = segment_sentences(text)
    assert [row["text"] for row in rows] == [
        "History flows.",
        "Time stops!",
        "A new layer appears.",
    ]
    assert text[rows[1]["char_start"] : rows[1]["char_end"]] == "Time stops!"


def test_melbert_targets_follow_upstream_whitespace_indices():
    sentence = "Seeds, planted in reform."

    assert [match.group(0) for match in MELBERT_WORD_RE.finditer(sentence)] == [
        "Seeds,",
        "planted",
        "in",
        "reform.",
    ]


def test_two_model_majority_requires_two_positive_votes():
    positive = {
        "sentence_id": "sentence-00001",
        "sentence_text": "History flows.",
        "word_index": 1,
        "word": "flows",
        "char_start": 8,
        "char_end": 13,
        "score": 0.9,
        "is_metaphor": True,
    }
    negative = {**positive, "score": 0.1, "is_metaphor": False}

    rows = _ensemble(
        {"melbert": [positive], "xlmr": [negative]},
        ("melbert", "xlmr"),
        "majority",
        0.5,
    )

    assert rows == []


def test_pipeline_keeps_detection_taxonomy_and_period_separate():
    result = analyze(
        "The river of time carries history.",
        PipelineConfig(
            model_ids=("melbert", "xlmr"),
            ensemble_rule="majority",
            document_year=1830,
        ),
        runtime=FakeRuntime(),
    )
    assert result["manifest"]["period"]["id"] == "B"
    assert result["manifest"]["application_version"] == "0.1.1"
    assert result["manifest"]["models"] == ["melbert", "xlmr"]
    assert len(result["detections"]) == 1
    row = result["detections"][0]
    assert row["positive_votes"] == 2
    assert row["taxonomy"]["class_id"]
    assert row["review_status"] == "unreviewed_machine_prediction"
