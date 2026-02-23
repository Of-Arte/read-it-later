"""
test_main.py
pytest suite for main.py

Run: pytest test_main.py -v
"""
import pytest
import main as urlfeed


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def reset_state():
    """
    Reset module-level shared state before every test.
    feed is a deque, favorites is a list -- both are mutated in place.
    """
    urlfeed.feed.clear()
    urlfeed.favorites.clear()
    urlfeed.TRACE = False
    yield


# ---------------------------------------------------------------------------
# add_post
# ---------------------------------------------------------------------------

class TestAddPost:
    def test_appends_url_to_feed(self, monkeypatch, capsys):
        monkeypatch.setattr("builtins.input", lambda _: "https://example.com")
        urlfeed.add_post()
        assert list(urlfeed.feed) == ["https://example.com"]

    def test_multiple_posts_preserve_order(self, monkeypatch):
        urls = ["https://a.com", "https://b.com", "https://c.com"]
        monkeypatch.setattr("builtins.input", lambda _: urls.pop(0))
        urlfeed.add_post()
        urlfeed.add_post()
        urlfeed.add_post()
        assert list(urlfeed.feed) == ["https://a.com", "https://b.com", "https://c.com"]

    def test_prints_confirmation(self, monkeypatch, capsys):
        monkeypatch.setattr("builtins.input", lambda _: "https://example.com")
        urlfeed.add_post()
        out = capsys.readouterr().out
        assert "https://example.com" in out
        assert "added to feed" in out

    def test_empty_string_is_accepted(self, monkeypatch):
        """Edge: empty input is a valid string; deque should still accept it."""
        monkeypatch.setattr("builtins.input", lambda _: "")
        urlfeed.add_post()
        assert "" in urlfeed.feed


# ---------------------------------------------------------------------------
# skip_post
# ---------------------------------------------------------------------------

class TestSkipPost:
    def test_removes_front_of_feed(self):
        urlfeed.feed.extend(["https://first.com", "https://second.com"])
        urlfeed.skip_post()
        assert list(urlfeed.feed) == ["https://second.com"]

    def test_prints_removed_url(self, capsys):
        urlfeed.feed.append("https://removed.com")
        urlfeed.skip_post()
        out = capsys.readouterr().out
        assert "https://removed.com" in out

    def test_empty_feed_prints_warning(self, capsys):
        urlfeed.skip_post()
        out = capsys.readouterr().out
        assert "Feed empty" in out

    def test_feed_empty_after_single_skip(self):
        urlfeed.feed.append("https://only.com")
        urlfeed.skip_post()
        assert len(urlfeed.feed) == 0


# ---------------------------------------------------------------------------
# view_data
# ---------------------------------------------------------------------------

class TestViewData:
    def test_prints_each_item_numbered(self, capsys):
        urlfeed.view_data("Feed", ["https://a.com", "https://b.com"])
        out = capsys.readouterr().out
        assert "1. https://a.com" in out
        assert "2. https://b.com" in out

    def test_prints_label_header(self, capsys):
        urlfeed.view_data("MyLabel", ["item"])
        out = capsys.readouterr().out
        assert "MyLabel" in out

    def test_empty_struct_prints_empty_message(self, capsys):
        urlfeed.view_data("Feed", [])
        out = capsys.readouterr().out
        assert "empty" in out.lower()

    def test_works_with_deque(self, capsys):
        from collections import deque
        d = deque(["https://x.com"])
        urlfeed.view_data("Feed", d)
        out = capsys.readouterr().out
        assert "https://x.com" in out


# ---------------------------------------------------------------------------
# add_favorite
# ---------------------------------------------------------------------------

class TestAddFavorite:
    def test_adds_selected_item_to_favorites(self, monkeypatch):
        urlfeed.feed.extend(["https://a.com", "https://b.com"])
        monkeypatch.setattr("builtins.input", lambda _: "2")
        urlfeed.add_favorite()
        assert urlfeed.favorites == ["https://b.com"]

    def test_does_not_remove_from_feed(self, monkeypatch):
        urlfeed.feed.extend(["https://a.com", "https://b.com"])
        monkeypatch.setattr("builtins.input", lambda _: "1")
        urlfeed.add_favorite()
        assert len(urlfeed.feed) == 2

    def test_invalid_number_input_prints_error(self, monkeypatch, capsys):
        urlfeed.feed.append("https://a.com")
        monkeypatch.setattr("builtins.input", lambda _: "99")
        urlfeed.add_favorite()
        out = capsys.readouterr().out
        assert "Invalid" in out
        assert urlfeed.favorites == []

    def test_non_numeric_input_prints_error(self, monkeypatch, capsys):
        urlfeed.feed.append("https://a.com")
        monkeypatch.setattr("builtins.input", lambda _: "abc")
        urlfeed.add_favorite()
        out = capsys.readouterr().out
        assert "Invalid" in out

    def test_empty_feed_prints_warning(self, monkeypatch, capsys):
        # input won't be reached because feed is empty
        urlfeed.add_favorite()
        out = capsys.readouterr().out
        assert "Feed empty" in out

    def test_first_item_index_one(self, monkeypatch):
        """User picks '1' which maps to index 0."""
        urlfeed.feed.append("https://first.com")
        monkeypatch.setattr("builtins.input", lambda _: "1")
        urlfeed.add_favorite()
        assert urlfeed.favorites == ["https://first.com"]


# ---------------------------------------------------------------------------
# remove_last_favorite
# ---------------------------------------------------------------------------

class TestRemoveLastFavorite:
    def test_removes_last_item(self, capsys):
        urlfeed.favorites.extend(["https://a.com", "https://b.com"])
        urlfeed.remove_last_favorite()
        assert urlfeed.favorites == ["https://a.com"]

    def test_prints_removed_url(self, capsys):
        urlfeed.favorites.append("https://removed.com")
        urlfeed.remove_last_favorite()
        out = capsys.readouterr().out
        assert "https://removed.com" in out

    def test_empty_favorites_prints_warning(self, capsys):
        urlfeed.remove_last_favorite()
        out = capsys.readouterr().out
        assert "Favorites empty" in out

    def test_stack_lifo_order(self, capsys):
        """Last added should be first removed."""
        urlfeed.favorites.extend(["https://a.com", "https://b.com", "https://c.com"])
        urlfeed.remove_last_favorite()
        assert urlfeed.favorites[-1] == "https://b.com"


# ---------------------------------------------------------------------------
# shutdown
# ---------------------------------------------------------------------------

class TestShutdown:
    def test_returns_false(self, capsys):
        result = urlfeed.shutdown()
        assert result is False

    def test_prints_message(self, capsys):
        urlfeed.shutdown()
        out = capsys.readouterr().out
        assert "Shutting Down" in out


# ---------------------------------------------------------------------------
# toggle_trace
# ---------------------------------------------------------------------------

class TestToggleTrace:
    def test_toggles_on(self, capsys):
        urlfeed.TRACE = False
        urlfeed.toggle_trace()
        assert urlfeed.TRACE is True

    def test_toggles_off(self, capsys):
        urlfeed.TRACE = True
        urlfeed.toggle_trace()
        assert urlfeed.TRACE is False

    def test_double_toggle_returns_to_original(self):
        original = urlfeed.TRACE
        urlfeed.toggle_trace()
        urlfeed.toggle_trace()
        assert urlfeed.TRACE == original

    def test_prints_state_on(self, capsys):
        urlfeed.TRACE = False
        urlfeed.toggle_trace()
        out = capsys.readouterr().out
        assert "ON" in out

    def test_prints_state_off(self, capsys):
        urlfeed.TRACE = True
        urlfeed.toggle_trace()
        out = capsys.readouterr().out
        assert "OFF" in out


# ---------------------------------------------------------------------------
# print_menu
# ---------------------------------------------------------------------------

class TestPrintMenu:
    def test_prints_all_menu_keys(self, capsys):
        urlfeed.print_menu()
        out = capsys.readouterr().out
        for key, label, _ in urlfeed.menu:
            assert key in out
            assert label in out

    def test_menu_has_expected_options(self):
        keys = [key for key, _, _ in urlfeed.menu]
        assert "0" in keys   # shutdown
        assert "1" in keys   # add post
        assert "2" in keys   # skip post
        assert "3" in keys   # add favorite
        assert "4" in keys   # remove last favorite
        assert "5" in keys   # view feed
        assert "6" in keys   # view favorites
