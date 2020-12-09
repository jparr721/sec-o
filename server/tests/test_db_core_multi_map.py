from db.core.multi_map import MultiMap


def test_creates_with_config():
    mm = MultiMap()

    assert mm is not None


def test_map_length():
    mm = MultiMap()

    assert len(mm) == 0
    assert mm.empty() is True


def test_map_length_nonzero():
    mm = MultiMap()
    mm.add_edge("1", "2")

    assert len(mm) == 1


def test_map_contains_key():
    mm = MultiMap()
    mm.add_edge("1", "2")

    assert mm.contains_key("1") is True
    assert mm.contains_key("2") is False


def test_map_contains_value():
    mm = MultiMap()
    mm.add_edge("1", "2")

    assert mm.contains_value("1", "2") is True
    assert mm.contains_value("1", "1") is False


def test_map_contains_value_if_value_None():
    mm = MultiMap()

    assert mm.contains_value("1", "1") is False


def test_map_removes_key():
    mm = MultiMap()
    mm.add_edge("1", "2")

    assert mm.contains_key("1") is True
    assert mm.contains_value("1", "2") is True

    assert mm.remove_key("1") is True

    assert mm.contains_key("1") is False
    assert mm.contains_value("1", "2") is False


def test_map_removes_value():
    mm = MultiMap()
    mm.add_edge("1", "2")

    assert mm.contains_key("1") is True
    assert mm.contains_value("1", "2") is True

    mm.remove_edge("1", "2")

    assert mm.contains_key("1") is True
    assert mm.contains_value("1", "2") is False


def test_map_clears_key():
    mm = MultiMap()
    mm.add_edge("1", "2")

    assert mm.contains_key("1") is True
    assert mm.contains_value("1", "2") is True

    mm.clear_key("1")

    assert mm.contains_key("1") is True
    assert mm.contains_value("1", "2") is False


def test_map_safe_get():
    mm = MultiMap()
    mm.add_edge("1", "2")

    assert mm.get("1") == ["2"]
    assert mm.get("2") is None


def test_map_clear():
    mm = MultiMap()
    mm.add_edge("1", "2")
    mm.add_edge("1", "3")
    mm.add_edge("2", "4")

    assert mm.get("1") == ["2", "3"]
    assert mm.contains_key("1") is True
    assert mm.contains_key("2") is True
    assert mm.contains_value("1", "2") is True
    assert mm.contains_value("1", "3") is True
    assert mm.contains_value("2", "4") is True
    assert len(mm) == 2

    mm.clear()

    assert len(mm) == 0
