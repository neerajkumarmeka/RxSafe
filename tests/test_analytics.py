from core.analytics import (
    get_database_stats,
    get_severity_distribution,
    get_top_interacting_drugs,
)


EXPECTED_DRUG_COUNT = 1798
EXPECTED_INTERACTION_COUNT = 48930


def test_database_stats():
    stats = get_database_stats()

    assert stats["total_drugs"] == EXPECTED_DRUG_COUNT
    assert stats["total_interactions"] == EXPECTED_INTERACTION_COUNT


def test_severity_distribution():
    distribution = get_severity_distribution()

    assert isinstance(distribution, list)
    assert len(distribution) > 0

    total = sum(
        item["count"]
        for item in distribution
    )

    assert total == EXPECTED_INTERACTION_COUNT


def test_top_interacting_drugs():
    results = get_top_interacting_drugs(5)

    assert len(results) == 5

    for result in results:
        assert "drug" in result
        assert "interaction_count" in result
        assert result["interaction_count"] > 0


def test_top_interacting_drugs_limit():
    results = get_top_interacting_drugs(3)

    assert len(results) == 3