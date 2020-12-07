from db.db import PhasmaConfig, PhasmaDB


def test_config():
    cfg = PhasmaConfig(logging_level="info")

    assert cfg.logging_level == "info"


def test_db_object_with_logging():
    db = PhasmaDB("info")
    assert db is not None


def test_db_object_without_logging():
    db = PhasmaDB()
    assert db is not None


def test_db_object_generates_config():
    db = PhasmaDB("info")

    cfg = db._generate_config()
    compare_cfg = PhasmaConfig(logging_level="info")

    assert cfg == compare_cfg


def test_db_object_generates_empty_config():
    db = PhasmaDB()

    cfg = db._generate_config()
    compare_cfg = PhasmaConfig(logging_level=None)

    assert cfg == compare_cfg
