import json
import os
from datetime import datetime

# 记录文件路径
STEP_RECORD_FILE = "step_records.json"

def init_step_record_file():
    """初始化步骤记录文件"""
    if not os.path.exists(STEP_RECORD_FILE):
        with open(STEP_RECORD_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f, ensure_ascii=False, indent=2)

def save_step_record(difficulty, steps):
    """保存完整游戏步骤记录"""
    init_step_record_file()
    
    # 创建记录数据
    record = {
        "timestamp": datetime.now().isoformat(),
        "difficulty": difficulty,
        "total_steps": len(steps),
        "steps": steps
    }
    
    # 读取现有记录并添加新记录
    with open(STEP_RECORD_FILE, 'r+', encoding='utf-8') as f:
        records = json.load(f)
        records.append(record)
        f.seek(0)
        f.truncate()
        json.dump(records, f, ensure_ascii=False, indent=2)
    
    return record

def get_latest_step_record(difficulty=None):
    """获取最新的步骤记录，可指定难度"""
    init_step_record_file()
    
    with open(STEP_RECORD_FILE, 'r', encoding='utf-8') as f:
        records = json.load(f)
    
    if not records:
        return None
    
    # 如果指定了难度，筛选对应难度的最新记录
    if difficulty:
        filtered = [r for r in records if r["difficulty"] == difficulty]
        return filtered[-1] if filtered else None
    
    # 返回最新的记录
    return records[-1]