import deskctl


def test_backup_runs_pg_dump(tmp_path, monkeypatch):
    calls = []
    monkeypatch.setattr(deskctl.subprocess, "run", lambda args, check: calls.append(args))
    path = deskctl.backup(None, str(tmp_path))
    assert calls[0][0] == "pg_dump" and path.endswith(".dump")
