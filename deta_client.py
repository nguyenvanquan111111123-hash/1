import pyautogui
import time
import requests
from pynput import keyboard
import threading

# Cấu hình Deta API
DETA_URL = "https://your-deta-url.deta.dev"  # Thay bằng URL Deta của bạn
CHECK_INTERVAL = 0.5  # Kiểm tra lệnh từ server mỗi 0.5 giây

# Biến toàn cục
current_speed = 0.1
current_mode = "normal"
running = False

def get_status_from_server():
    """Lấy trạng thái từ Deta"""
    try:
        response = requests.get(f"{DETA_URL}/status", timeout=5)
        if response.status_code == 200:
            return response.json()
    except:
        pass
    return None

def normal_attack():
    """Đánh thường"""
    pyautogui.press('space')

def atiban_attack():
    """Đánh nhanh liên tục (3 cái)"""
    for _ in range(3):
        pyautogui.press('space')
        time.sleep(current_speed * 0.3)

def combo_attack():
    """Combo đánh"""
    for _ in range(2):
        pyautogui.press('space')
        time.sleep(current_speed * 0.2)
    time.sleep(current_speed * 0.5)
    pyautogui.press('space')

def jump_attack():
    """Bay lên đầu boss"""
    pyautogui.press('space')
    time.sleep(current_speed * 0.5)
    pyautogui.press('space')
    time.sleep(current_speed * 0.2)
    pyautogui.press('space')
    time.sleep(current_speed * 0.2)
    pyautogui.press('space')

def range_attack():
    """Đánh xa"""
    pyautogui.press('e')
    time.sleep(current_speed * 0.3)
    pyautogui.press('space')
    time.sleep(current_speed * 0.2)
    pyautogui.press('space')

def execute_attack():
    """Thực thi tấn công dựa trên chế độ"""
    if current_mode == "normal":
        normal_attack()
    elif current_mode == "atiban":
        atiban_attack()
    elif current_mode == "combo":
        combo_attack()
    elif current_mode == "jumpAttack":
        jump_attack()
    elif current_mode == "rangeAttack":
        range_attack()

def on_press(key):
    """Xử lý input từ bàn phím (local)"""
    try:
        if key == keyboard.Key.esc:
            print("\n[ESC] Thoát chương trình!")
            return False
    except:
        pass

def poll_server():
    """Kiểm tra trạng thái từ server liên tục"""
    global current_speed, current_mode, running
    
    print("\n[INFO] Đang kết nối tới Deta server...")
    print(f"[INFO] URL: {DETA_URL}")
    print("[INFO] Bấm ESC để thoát\n")
    
    while True:
        try:
            status = get_status_from_server()
            
            if status:
                current_speed = status.get("speed", 0.1)
                current_mode = status.get("mode", "normal")
                running = status.get("running", False)
                
                if running:
                    execute_attack()
                    time.sleep(current_speed)
                else:
                    time.sleep(0.1)
            else:
                print("[ERROR] Không kết nối được tới server. Đang thử lại...")
                time.sleep(2)
                
        except KeyboardInterrupt:
            print("\n[INFO] Dừng chương trình!")
            break
        except Exception as e:
            print(f"[ERROR] {str(e)}")
            time.sleep(1)

if __name__ == "__main__":
    print("=" * 60)
    print("Anime Spirits - Client (Nhận lệnh từ Deta)")
    print("=" * 60)
    print(f"\n📌 Deta URL: {DETA_URL}")
    print("📍 Trạng thái: Chờ lệnh từ server")
    print("\n💻 Điều khiển qua API Deta:")
    print("  POST /start - Bắt đầu")
    print("  POST /stop - Dừng")
    print("  POST /mode/{mode} - Thay chế độ")
    print("  POST /speed/up - Tăng tốc độ")
    print("  POST /speed/down - Giảm tốc độ")
    print("\n📱 Điều khiển Local:")
    print("  ESC - Thoát")
    print("\n" + "=" * 60 + "\n")
    
    # Bắt đầu keyboard listener
    listener_thread = threading.Thread(target=lambda: keyboard.Listener(on_press=on_press).start(), daemon=True)
    listener_thread.start()
    
    # Bắt đầu polling server
    poll_server()
