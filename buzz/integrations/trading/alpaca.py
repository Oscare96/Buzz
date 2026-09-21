"""Alpaca REST adapter for Buzz trading capabilities."""
from __future__ import annotations
from typing import Any
import requests
from buzz.integrations.trading.base import TradingProvider

class AlpacaTradingProvider(TradingProvider):
    def __init__(self, api_key: str, secret_key: str, base_url: str = "https://paper-api.alpaca.markets") -> None:
        self.base=base_url.rstrip("/")
        self.headers={"APCA-API-KEY-ID":api_key,"APCA-API-SECRET-KEY":secret_key,"Content-Type":"application/json"}
    def _get(self,path:str):
        r=requests.get(self.base+path,headers=self.headers,timeout=15); r.raise_for_status(); return r.json()
    def portfolio(self)->dict[str,Any]:
        account=self._get("/v2/account"); positions=self._get("/v2/positions")
        return {"equity":account.get("equity"),"cash":account.get("cash"),"buying_power":account.get("buying_power"),"positions":positions}
    def bot_status(self)->dict[str,Any]:
        return {"status":"external","message":"Bot lifecycle requires the Buzz bot-control adapter."}
    def preview_order(self,symbol:str,side:str,quantity:float)->dict[str,Any]:
        return {"symbol":symbol,"side":side,"quantity":quantity,"status":"preview","submitted":False}
    def place_order(self,symbol:str,side:str,quantity:float,idempotency_key:str)->dict[str,Any]:
        payload={"symbol":symbol,"side":side,"qty":str(quantity),"type":"market","time_in_force":"day","client_order_id":idempotency_key}
        r=requests.post(self.base+"/v2/orders",headers=self.headers,json=payload,timeout=15); r.raise_for_status(); return r.json()
    def set_bot_enabled(self,bot:str,enabled:bool)->dict[str,Any]:
        raise NotImplementedError("Trading bot control requires a configured bot-control adapter.")
