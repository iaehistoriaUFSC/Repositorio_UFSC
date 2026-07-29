from app.models import load_registry, reference_fingerprint, registry_by_id


def test_registry_contains_requested_models():
    registry = registry_by_id()
    assert set(registry) == {"melbert", "xlmr", "cl_roberta", "framebert"}
    assert registry["melbert"]["recommended"] is True
    assert registry["xlmr"]["training_data"] == "VU Amsterdam Metaphor Corpus"
    assert registry["framebert"]["experimental"] is True


def test_reference_dataset_has_stable_fingerprint():
    assert len(reference_fingerprint()) == 64
    assert reference_fingerprint() == reference_fingerprint()

