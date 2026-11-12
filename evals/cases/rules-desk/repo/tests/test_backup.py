import os

import deskctl


def test_backup_writes_a_file(conn, tmp_path):
    path = deskctl.backup(conn, str(tmp_path / "backups"))
    assert os.path.getsize(path) > 0
