import random
import time

def generate_random_array(row, column):

    total_elements = row * column
    # 计算需要的不重复数字个数
    num_count = total_elements // 2
    
    random_nums = random.sample(range(1, num_count + 1), num_count)

    if total_elements % 2 != 0:
        # 每个数字重复2次，打乱顺序
        array_flat = random_nums * 2  # 每个数字出现2次
        array_flat.append(num_count + 1)  # 添加一个额外的数字
    else:
        array_flat = random_nums * 2  # 每个数字出现2次
    
    random.shuffle(array_flat)     # 随机打乱
    
    # 转换成 row×column 的二维数组
    result = [array_flat[i * column : (i + 1) * column] for i in range(row)]
    return result

def count_steps(step):
    step += 1
    return step

def time_start():
    return time.time()

def time_end(start_time):
    end_time = time.time()
    elapsed_time = end_time - start_time
    return elapsed_time

def format_time(seconds):
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes}分{seconds}秒"