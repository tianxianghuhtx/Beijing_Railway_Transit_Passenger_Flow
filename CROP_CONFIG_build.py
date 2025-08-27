from decimal import Decimal, ROUND_HALF_UP
from typing import List

def _round_half_up(x: float) -> int:
    return int(Decimal(str(x)).quantize(Decimal('1'), rounding=ROUND_HALF_UP))

def split_into_27(a: int, b: int) -> List[int]:
    """
    给定两个整数 a、b，27 等分区间 [a, b]，
    返回包含边界在内的 28 个分界点（整数，四舍五入）。
    """
    step = (b - a) / 27
    return [_round_half_up(a + i * step) for i in range(28)]

def reorder_numbers(nums):
    if len(nums) != 28:
        raise ValueError("需要正好 28 个数！")

    # 原位置 → 新位置 的映射表
    position_map = {
        1: 1,  2: 2,  3: 3,  4: 4,  5: 5,
        6: 6,  7: 7,  8: 8,  9: 9,  10: 10,
        11: 11, 12: 12, 13: 13, 14: 14, 15: 15,
        16: 16, 17: 17, 18: 18, 19: 19,
        20: 22, 21: 21, 22: 23, 23: 24, 24: 20,
        25: 27, 26: 28, 27: 26, 28: 25
    }

    # 先建一个空列表，长度28
    result = [None] * 28

    # 按照映射表放置元素
    for old_pos, new_pos in position_map.items():
        result[new_pos - 1] = nums[old_pos - 1]

    return result


a = 900
b = 2484
CROP_CONFIG = {
        "M1BATONG": {
            "name": (111, 900, 169, 45),
            "flow": (633, 900, 865, 45)
        },
        "M2": {
            "name": (111, 960, 169, 45),
            "flow": (633, 960, 865, 45)
        },
        "M3": {
            "name": (111, 1019, 169, 45),
            "flow": (633, 1019, 865, 45)
        },
        "M4DAXING": {
            "name": (111, 1077, 169, 45),
            "flow": (633, 1077, 865, 45)
        },
        "M5": {
            "name": (111, 1136, 169, 45),
            "flow": (633, 1136, 865, 45)
        },
        "M6": {
            "name": (111, 1194, 169, 45),
            "flow": (633, 1194, 865, 45)
        },
        "M7": {
            "name": (111, 1252, 169, 45),
            "flow": (633, 1252, 865, 45)
        },
        "M8": {
            "name": (111, 1312, 169, 45),
            "flow": (633, 1312, 865, 45)
        },
        "M9": {
            "name": (111, 1369, 169, 45),
            "flow": (633, 1369, 865, 45)
        },
        "M10": {
            "name": (111, 1428, 169, 45),
            "flow": (633, 1428, 865, 45)
        },
        "M11": {
            "name": (111, 1487, 169, 45),
            "flow": (633, 1487, 865, 45)
        },
        "M12": {
            "name": (111, 1545, 169, 45),
            "flow": (633, 1545, 865, 45)
        },
        "M13": {
            "name": (111, 1604, 169, 45),
            "flow": (633, 1604, 865, 45)
        },
        "M14": {
            "name": (111, 1663, 169, 45),
            "flow": (633, 1663, 865, 45)
        },
        "M15": {
            "name": (111, 1721, 169, 45),
            "flow": (633, 1721, 865, 45)
        },
        "M16": {
            "name": (111, 1779, 169, 45),
            "flow": (633, 1779, 865, 45)
        },
        "M17S": {
            "name": (111, 1838, 169, 45),
            "flow": (633, 1838, 865, 45)
        },
        "M17N": {
            "name": (111, 1896, 169, 45),
            "flow": (633, 1896, 865, 45)
        },
        "M19": {
            "name": (111, 1956, 169, 45),
            "flow": (633, 1956, 865, 45)
        },
        "M24_YIZHUANG": {
            "name": (111, 2132, 169, 45),
            "flow": (633, 2132, 865, 45)
        },
        "M25_FANGSHAN": {
            "name": (111, 2073, 169, 45),
            "flow": (633, 2073, 865, 45)
        },
        "YANFANG": {
            "name": (111, 2191, 169, 45),
            "flow": (633, 2191, 865, 45)
        },
        "M26_S1": {
            "name": (111, 2248, 169, 45),
            "flow": (633, 2248, 865, 45)
        },
        "M27_CHANGPING": {
            "name": (111, 2014, 169, 45),
            "flow": (633, 2014, 865, 45)
        },
        "M34_SHOUDUJICHANG": {
            "name": (111, 2425, 169, 45),
            "flow": (633, 2425, 865, 45)
        },
        "M35_DAXINGJICHANG": {
            "name": (111, 2484, 169, 45),
            "flow": (633, 2484, 865, 45)
        },
        "XIJIAO": {
            "name": (111, 2366, 169, 45),
            "flow": (633, 2366, 865, 45)
        },
        "YIZHUANGT1": {
            "name": (111, 2308, 169, 45),
            "flow": (633, 2308, 865, 45)
        }
    }


nums = split_into_27(a, b)
new_nums = reorder_numbers(nums)
print("新顺序：", new_nums)

# 校验数量一致
if len(new_nums) != len(CROP_CONFIG):
    raise ValueError(f"new_nums数量({len(new_nums)})与条目数量({len(CROP_CONFIG)})不一致")

# 组装“原格式”文本
lines = []
lines.append("CROP_CONFIG = { ")  # 注意：与原文一致，{ 后保留一个空格然后换行

keys = list(CROP_CONFIG.keys())
for i, key in enumerate(keys):
    y = new_nums[i]
    n0, _, n2, n3 = CROP_CONFIG[key]["name"]
    f0, _, f2, f3 = CROP_CONFIG[key]["flow"]

    lines.append(f'        "{key}": {{')
    lines.append(f'            "name": ({n0}, {y}, {n2}, {n3}),')
    lines.append(f'            "flow": ({f0}, {y}, {f2}, {f3}),')
    # 最后一个条目不加逗号，其余加逗号，严格匹配原格式
    if i < len(keys) - 1:
        lines.append('        },')
    else:
        lines.append('        }')

lines.append('    }')

# 打印最终文本
print("\n".join(lines))