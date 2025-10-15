
import os, json
try:
    import redis
except Exception:
    redis = None

FALLBACK_FILE = os.path.join(os.path.dirname(__file__), "assets", "preferences.json")

def _read_fallback():
    try:
        with open(FALLBACK_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def _write_fallback(data):
    # Ensure directory exists
    os.makedirs(os.path.dirname(FALLBACK_FILE), exist_ok=True)
    with open(FALLBACK_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def get_redis_client():
    url = os.environ.get("REDIS_URL")
    if url and redis is not None:
        return redis.Redis.from_url(url)
    return None

def get_pref(key, default=None):
    client = get_redis_client()
    if client:
        try:
            v = client.get(key)
            if v is None:
                return default
            return json.loads(v)
        except Exception:
            return default
    else:
        data = _read_fallback()
        return data.get(key, default)

def set_pref(key, value):
    client = get_redis_client()
    if client:
        try:
            client.set(key, json.dumps(value))
            return True
        except Exception:
            return False
    else:
        data = _read_fallback()
        data[key] = value
        _write_fallback(data)
        return True
