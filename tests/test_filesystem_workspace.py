from buzz.skills.filesystem import ReadFileSkill, WriteFileSkill


def test_workspace_write_and_read(monkeypatch, tmp_path):
    monkeypatch.setenv("BUZZ_WORKSPACE", str(tmp_path))
    written = WriteFileSkill().execute(path="hello.txt", content="buzz")
    assert written.success
    read = ReadFileSkill().execute(path="hello.txt")
    assert read.success and read.data == "buzz"


def test_workspace_blocks_escape(monkeypatch, tmp_path):
    monkeypatch.setenv("BUZZ_WORKSPACE", str(tmp_path))
    result = WriteFileSkill().execute(path="../outside.txt", content="no")
    assert not result.success
