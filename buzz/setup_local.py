"""Local first-run setup helpers. Never commits or prints generated secrets."""
from __future__ import annotations
from pathlib import Path
from secrets import token_urlsafe

def initialize_local_env(root:Path=Path("."))->dict:
    target=root/".env"
    created=not target.exists()
    if created:
        example=root/".env.example"
        text=example.read_text(encoding="utf-8") if example.exists() else ""
    else:
        text=target.read_text(encoding="utf-8")
    generated=False
    lines=text.splitlines()
    found=False
    for i,line in enumerate(lines):
        if line.startswith("BUZZ_API_TOKEN="):
            found=True
            if not line.partition("=")[2].strip():
                lines[i]="BUZZ_API_TOKEN="+token_urlsafe(32)
                generated=True
            break
    if not found:
        lines.append("BUZZ_API_TOKEN="+token_urlsafe(32))
        generated=True
    target.write_text("\n".join(lines).rstrip()+"\n",encoding="utf-8")
    return {"env_created":created,"api_token_generated":generated,"path":str(target)}
