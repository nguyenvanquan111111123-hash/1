from deta import Deta
from fastapi import FastAPI
from pydantic import BaseModel
import json

# Khởi tạo Deta
deta = Deta()
db = deta.Base("anime_spirits")

app = FastAPI()

class AttackCommand(BaseModel):
    command: str  # "start", "stop", "change_mode", "speed_up", "speed_down"
    mode: str = None  # "normal", "atiban", "combo", "jumpAttack", "rangeAttack"
    speed: float = None

class GameStatus(BaseModel):
    running: bool
    mode: str
    speed: float

# Trạng thái mặc định
STATUS_KEY = "game_status"

def get_status():
    result = db.get(STATUS_KEY)
    if result:
        return result
    else:
        # Tạo status mặc định
        default_status = {
            "key": STATUS_KEY,
            "running": False,
            "mode": "normal",
            "speed": 0.1
        }
        db.put(default_status)
        return default_status

@app.get("/")
async def root():
    return {"message": "Anime Spirits Auto Attack API on Deta"}

@app.get("/status")
async def get_game_status():
    """Lấy trạng thái game hiện tại"""
    status = get_status()
    return {
        "running": status.get("running", False),
        "mode": status.get("mode", "normal"),
        "speed": status.get("speed", 0.1)
    }

@app.post("/start")
async def start_attack():
    """Bắt đầu đánh"""
    status = get_status()
    status["running"] = True
    db.put(status)
    return {"status": "Started", "data": status}

@app.post("/stop")
async def stop_attack():
    """Dừng đánh"""
    status = get_status()
    status["running"] = False
    db.put(status)
    return {"status": "Stopped", "data": status}

@app.post("/mode/{mode_name}")
async def change_mode(mode_name: str):
    """Thay đổi chế độ tấn công"""
    valid_modes = ["normal", "atiban", "combo", "jumpAttack", "rangeAttack"]
    
    if mode_name not in valid_modes:
        return {"error": f"Invalid mode. Valid modes: {valid_modes}"}
    
    status = get_status()
    status["mode"] = mode_name
    db.put(status)
    return {"status": f"Changed to {mode_name}", "data": status}

@app.post("/speed/up")
async def speed_up():
    """Tăng tốc độ"""
    status = get_status()
    status["speed"] = max(0.01, status.get("speed", 0.1) - 0.01)
    db.put(status)
    return {"status": f"Speed: {status['speed']:.2f}s", "data": status}

@app.post("/speed/down")
async def speed_down():
    """Giảm tốc độ"""
    status = get_status()
    status["speed"] = min(10, status.get("speed", 0.1) + 0.01)
    db.put(status)
    return {"status": f"Speed: {status['speed']:.2f}s", "data": status}

@app.post("/speed/reset")
async def speed_reset():
    """Reset tốc độ"""
    status = get_status()
    status["speed"] = 0.1
    db.put(status)
    return {"status": "Speed reset to 0.1s", "data": status}

@app.post("/speed/{new_speed}")
async def set_speed(new_speed: float):
    """Đặt tốc độ cụ thể"""
    if new_speed < 0.01 or new_speed > 10:
        return {"error": "Speed must be between 0.01 and 10"}
    
    status = get_status()
    status["speed"] = new_speed
    db.put(status)
    return {"status": f"Speed set to {new_speed:.2f}s", "data": status}

@app.get("/modes")
async def get_modes():
    """Lấy danh sách chế độ có sẵn"""
    return {
        "modes": [
            "normal",
            "atiban", 
            "combo",
            "jumpAttack",
            "rangeAttack"
        ]
    }

@app.post("/reset")
async def reset_all():
    """Reset tất cả về mặc định"""
    default_status = {
        "key": STATUS_KEY,
        "running": False,
        "mode": "normal",
        "speed": 0.1
    }
    db.put(default_status)
    return {"status": "Reset to default", "data": default_status}
