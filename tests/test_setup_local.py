from buzz.setup_local import initialize_local_env

def test_initialize_local_env_generates_token_without_returning_secret(tmp_path):
    (tmp_path/".env.example").write_text("OPENAI_API_KEY=\nBUZZ_API_TOKEN=\n")
    result=initialize_local_env(tmp_path)
    text=(tmp_path/".env").read_text()
    assert result["api_token_generated"] is True
    assert "BUZZ_API_TOKEN=" in text and len(text.split("BUZZ_API_TOKEN=",1)[1].strip())>20
    assert "token" not in result
