from datetime import date
from pathlib import Path
import json
from jsonschema import Draft202012Validator, ValidationError

class DateSegment:
    '''
    日期段 类

    name (str) 日期段名称
    begin (datetime.date) 开始日期
    end (datetime.date) 结束日期
    width (int) 分辨率-宽
    height (int) 分辨率-高
    function (str) 处理函数名称
    description (str) 日期段描述
    enabled (bool) 日期段启用标识
    '''
    name: str = ""
    begin: date = date(1970, 1, 1)
    end: date = date(1970, 1, 1)
    width: int = 0
    height: int = 0
    function: str = ""
    description:str = ""
    enabled: bool = False


    def __init__(self, name: str, begin: date, end: date,width: int, height: int, function: str, description:str, enabled: bool):
        '''
        初始化
        '''
        self.name = name
        self.begin = begin
        self.end = end
        self.width = width
        self.height = height
        self.function = function
        self.description = description
        self.enabled = enabled

def date_segments_import(json_path: Path = Path(r".\processing_function\date_segments.json")):
    # 读取 日期段-json-schema
    schema_path = Path(r".\processing_function\date_segments_schema.json")
    try:
        try:
            with schema_path.open("r", encoding="utf-8") as f:
                date_segments_schema = json.load(f)
        except UnicodeDecodeError:
            with schema_path.open("r", encoding="utf-8-sig") as f:
                date_segments_schema = json.load(f)
    except FileNotFoundError as e:
        raise RuntimeError(f"[读取 日期段-json-schema 发生错误] 文件 {schema_path} 不存在") from e
    except IsADirectoryError as e:
        raise RuntimeError(f"[读取 日期段-json-schema 发生错误] {schema_path} 是目录而非文件") from e
    except PermissionError as e:
        raise RuntimeError(f"[读取 日期段-json-schema 发生错误] 文件 {schema_path} 被占用 或 无访问权限") from e
    except json.JSONDecodeError as e:
        raise RuntimeError(
            f"[读取 日期段-json-schema 发生错误] 文件 {schema_path} 第 {e.lineno} 行 第 {e.colno} 列 有语法错误 {e.msg}"
        ) from e
    except OSError as e:
        err = getattr(e, "strerror", str(e))
        no  = getattr(e, "errno", None)
        raise RuntimeError(f"[读取 日期段-json-schema 发生错误] 文件 {schema_path} 读取失败 系统错误 {'' if no is None else f' errno={no}'} {err}") from e
    
    # 读取 日期段-json
    try:
        try:
            with json_path.open("r", encoding="utf-8") as f:
                date_segments_json = json.load(f)
        except UnicodeDecodeError:
            with json_path.open("r", encoding="utf-8-sig") as f:
                date_segments_json = json.load(f)
    except FileNotFoundError as e:
        raise RuntimeError(f"[读取 日期段-json 发生错误] 文件 {json_path} 不存在") from e
    except IsADirectoryError as e:
        raise RuntimeError(f"[读取 日期段-json 发生错误] {json_path} 是目录而非文件") from e
    except PermissionError as e:
        raise RuntimeError(f"[读取 日期段-json 发生错误] 文件 {json_path} 被占用 或 无访问权限") from e
    except json.JSONDecodeError as e:
        raise RuntimeError(f"[读取 日期段-json 发生错误] 文件 {json_path} 第 {e.lineno} 行 第 {e.colno} 列 有语法错误 {e.msg}") from e
    except OSError as e:
        err = getattr(e, "strerror", str(e))
        no  = getattr(e, "errno", None)
        raise RuntimeError(f"[读取 日期段-json 发生错误] 文件 {json_path} 读取失败 系统错误 {'' if no is None else f' errno={no}'} {err}") from e

    # 使用 日期段-json-schema 校验 日期段-json
    def _path_str(err: ValidationError) -> str:
        return "/".join(map(str, err.absolute_path)) or "<root>"
    validator = Draft202012Validator(date_segments_schema)
    errors = sorted(validator.iter_errors(date_segments_json), key=lambda e: tuple(e.absolute_path))
    if errors:
        print(f"[验证 日期段-json 发现错误] {json_path} 不符合格式要求")
        print(f"日期段-json-schema 文件 {schema_path}")
        print(f"以下为全部错误信息（共 {len(errors)} 条）：")
        for i, e in enumerate(errors, 1):
            print(f"{i:>3}. → {_path_str(e)} - {e.message}")
        detail = "\n".join(f"{i}. {_path_str(e)} - {e.message}" 
                           for i, e in enumerate(errors, 1))
        raise RuntimeError(
            f"[验证 日期段-json 发现错误] 使用 {schema_path} 验证 {json_path} 时发现 {len(errors)} 个错误：\n{detail}"
        )
    
    # 导入全部日期段 同时查找日期顺序错误
    date_segments_checking = [] # [日期段内容, 日期顺序检查, 重复检查] True为无问题 False为有问题
    for ds_json_element in date_segments_json:
        ds_element = DateSegment(
            ds_json_element["name"],
            date(ds_json_element["date"]["begin"]["year"], ds_json_element["date"]["begin"]["month"], ds_json_element["date"]["begin"]["day"]),
            date(ds_json_element["date"]["end"]["year"], ds_json_element["date"]["end"]["month"], ds_json_element["date"]["end"]["day"]),
            ds_json_element["resolution"]["width"],
            ds_json_element["resolution"]["height"],
            ds_json_element["function"],
            ds_json_element["description"],
            ds_json_element["enabled"]
        )
        if ds_element.begin <= ds_element.end:
            date_segments_checking.append([ds_element, True, True])
        else:
            date_segments_checking.append([ds_element, False, True])
        
    # 查找日期顺序错误
    cnt = len(date_segments_checking)
    for i in range(cnt):
        if date_segments_checking[i][1]:
            for j in range(i+1, cnt):
                ibegin, iend = date_segments_checking[i][0].begin, date_segments_checking[i][0].end
                jbegin, jend = date_segments_checking[j][0].begin, date_segments_checking[j][0].end
                if not (iend < jbegin or ibegin > jend):
                    date_segments_checking[i][2] = False
                    date_segments_checking[j][2] = False
    
    date_segments = []
    for dsc_element in date_segments_checking:
        if dsc_element[1] and dsc_element[2]:
            date_segments.append(dsc_element[0])
    
    return date_segments, date_segments_checking
            
