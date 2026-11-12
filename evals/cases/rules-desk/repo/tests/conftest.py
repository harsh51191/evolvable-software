import sqlite3

import pytest

import deskctl


@pytest.fixture
def conn(tmp_path):
    connection = sqlite3.connect(tmp_path / "desk.db")
    connection.row_factory = sqlite3.Row
    deskctl.migrate(connection)
    yield connection
    connection.close()
