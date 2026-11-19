import pytest

from backend.schemas.legal import (
    LegalCreate,
    LegalUpdate,
)


def test_legal_create_valid():

    entry = LegalCreate(
        contract="Contract-001",
        partner="Partner Ltd",
        status="Active",
    )

    assert entry.contract == "Contract-001"


def test_legal_update_valid():

    entry = LegalUpdate(
        status="Closed"
    )

    assert entry.status == "Closed"


def test_legal_missing_contract():

    with pytest.raises(Exception):

        LegalCreate(
            partner="Partner Ltd",
            status="Active",
        )