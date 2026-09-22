"""Voice-specific preflight checks for Buzz."""
from __future__ import annotations
from pathlib import Path
from buzz.config.settings import Settings

def voice_check(settings:Settings|None=None)->dict:
    settings=settings or Settings.load()
    checks=[]
    checks.append({"name":"openai_key","ok":bool(settings.openai_api_key),"detail":"configured" if settings.openai_api_key else "missing"})
    checks.append({"name":"elevenlabs_key","ok":bool(settings.elevenlabs_api_key),"detail":"configured" if settings.elevenlabs_api_key else "missing"})
    checks.append({"name":"elevenlabs_voice","ok":bool(settings.elevenlabs_voice_id),"detail":"configured" if settings.elevenlabs_voice_id else "missing"})
    model=settings.wake_model
    model_ok=bool(model and Path(model).expanduser().is_file())
    checks.append({"name":"wake_model","ok":model_ok,"detail":str(Path(model).expanduser()) if model else "missing"})
    try:
        import sounddevice as sd
        devices=sd.query_devices()
        default=sd.default.device
        input_index=default[0] if isinstance(default,(tuple,list)) else default
        input_ok=isinstance(input_index,int) and input_index>=0 and len(devices)>input_index and int(devices[input_index]["max_input_channels"])>0
        detail=str(devices[input_index]["name"]) if input_ok else "no default microphone"
        checks.append({"name":"microphone","ok":input_ok,"detail":detail})
    except Exception as exc:
        checks.append({"name":"microphone","ok":False,"detail":f"{type(exc).__name__}: {exc}"})
    return {"ready_for_voice_test":all(c["ok"] for c in checks),"checks":checks}
