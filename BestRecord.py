import os
import json

# 记录文件路径
RECORD_FILE = "best_records.json"

def init_record_file():
    """初始化记录文件，如果文件不存在则创建并写入初始数据"""
    if not os.path.exists(RECORD_FILE):
        initial_data = {
            "2*2": {"time": float('inf'), "steps": float('inf')},
            "3*3": {"time": float('inf'), "steps": float('inf')},
            "4*4": {"time": float('inf'), "steps": float('inf')},
            "4*6": {"time": float('inf'), "steps": float('inf')}
        }
        with open(RECORD_FILE, 'w', encoding='utf-8') as f:
            json.dump(initial_data, f, ensure_ascii=False, indent=2)

def get_best_record(difficulty):
    """获取指定难度的最佳记录（时间和步数）"""
    init_record_file()  # 确保文件存在
    with open(RECORD_FILE, 'r', encoding='utf-8') as f:
        records = json.load(f)
    return records.get(difficulty, {"time": float('inf'), "steps": float('inf')})

def update_best_record(difficulty, time, steps):
    """更新最佳记录，只有当新记录更好时才更新"""
    init_record_file()  # 确保文件存在
    with open(RECORD_FILE, 'r+', encoding='utf-8') as f:
        records = json.load(f)
        current_best = records[difficulty]
        
        # 同时比较时间和步数，只有当两者都更优时才更新
        if time < current_best["time"] and steps < current_best["steps"]:
            records[difficulty] = {"time": time, "steps": steps}
            f.seek(0)
            f.truncate()
            json.dump(records, f, ensure_ascii=False, indent=2)
            return True
    return False

def get_best_records(difficulty):
    init_record_file()
    if difficulty == "3*3":
        with open(RECORD_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)["3*3"]
    elif difficulty == "4*4":
        with open(RECORD_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)["4*4"]
    elif difficulty == "4*6":
        with open(RECORD_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)["4*6"]
    elif difficulty == "2*2":
        with open(RECORD_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)["2*2"]
    else:
        return None