from backend.models.legal import Legal


def test_legal_model_create():
    entry = Legal(
        contract="Contract-001",
        partner="Partner Ltd",
        status="Active",
    )

    assert entry.contract == "Contract-001"


def test_legal_partner_type():
    entry = Legal(
        partner="Partner Ltd"
    )

    assert isinstance(entry.partner, str)


def test_legal_status_type():
    entry = Legal(
        status="Active"
    )

    assert isinstance(entry.status, str)