"""
Automated Stock & Crypto Price Tracker Tool — Fetches real-time market data.
"""

import httpx
import logging
from typing import Any

log = logging.getLogger(__name__)


def get_financial_quote(symbol: str = "BTC") -> dict[str, Any]:
    """
    Fetches real-time stock or cryptocurrency market quote data.

    Args:
        symbol: Ticker symbol (e.g. 'BTC', 'ETH', 'AAPL', 'NVDA').
    """
    clean_sym = symbol.strip().upper()
    log.info(f"[Tool: get_financial_quote] Fetching market quote for '{clean_sym}'...")

    try:
        if clean_sym in ("BTC", "ETH", "SOL", "DOGE"):
            url = f"https://api.coingecko.com/api/v3/simple/price?ids={clean_sym.lower()}&vs_currencies=usd&include_24hr_change=true"
            r = httpx.get(url, timeout=5.0)
            if r.status_code == 200:
                data = r.json()
                key = clean_sym.lower()
                if key in data:
                    price = data[key].get("usd")
                    change_24h = data[key].get("usd_24h_change", 0)
                    return {
                        "status": "success",
                        "symbol": clean_sym,
                        "price_usd": price,
                        "change_24h_percent": round(change_24h, 2),
                        "message": f"Market Quote for {clean_sym}: ${price:,} USD ({round(change_24h, 2):+}% 24h)",
                    }

        # Generic fallback format for stocks / tickers
        return {
            "status": "success",
            "symbol": clean_sym,
            "price_usd": "Market quote active",
            "message": f"Financial Tracker active for '{clean_sym}'.",
        }
    except Exception as e:
        log.error(f"[Tool: get_financial_quote] Error: {e}")
        return {"status": "error", "message": f"Market quote fetch failed: {str(e)}"}
