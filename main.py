from datetime import date
from pathlib import Path
import sys
from PIL import Image
import numpy as np
from paddleocr import PaddleOCR, TextDetection, TextRecognition

import processing_function.date_segment_processing as dsp
import processing_function.file_processing as fp
import processing_function.ocr_processing as op
import processing_function.datapack_processing as dpp

if __name__ == "__main__":
    date_segments_json_path = Path(r".\processing_function\date_segments.json")
    date_segments, date_segments_checking = dsp.date_segments_import(date_segments_json_path)

    root_path = Path(r"C:\Users\tianxianghuhtx\Desktop\Railway\北京地铁\北京轨指中心客流量\work")
    include_subdirs = True
    files, files_readerror = fp.files_import(root_path, include_subdirs)
    if not ".png" in files:
        print(f"没有png文件 程序结束")
        sys.exit(0)
    
    png_valid, png_invalid = fp.png_filter(files[".png"])
    if not len(png_valid):
        print(f"没有文件名符合日期要求的png文件 程序结束")
        sys.exit(0)
    
    datapack = []
    for i, png_path in enumerate(png_valid, 1):
        png = Image.open(png_path).convert("RGB")
        png_width, png_height = png.size
        print(f"[{i}] {png_path.name}")
        print(f"    文件路径: {png_path.resolve()}")
        print(f"    分辨率: {png_width} x {png_height}")
        print("    -----")

        png_date = date.fromisoformat(png_path.stem)
        find = False
        name, begin, end, width, height, function, description, enabled = "", date(1970, 1, 1), date(1970, 1, 1), 0, 0, "", "", True
        for date_segment in date_segments:
            if date_segment.begin <= png_date <= date_segment.end:
                name = date_segment.name
                begin, end = date_segment.begin, date_segment.end
                width, height = date_segment.width, date_segment.height
                function = date_segment.function
                description = date_segment.description
                enabled = date_segment.enabled
                print(f"    匹配到日期段 {name}")
                print(f"        起始日期: {begin}")
                print(f"        结束日期: {end}")
                print(f"        分辨率: {width} x {height}")
                if function != "":
                    print(f"        处理函数: {function}")
                else:
                    print(f"        未指定处理函数")
                if description != "":
                    print(f"        描述: {description}")
                else:
                    print(f"        未填写描述")
                if enabled:
                    print(f"        日期段状态: 启用")
                else:
                    print(f"        日期段状态: 禁用")
                print("    -----")
                find = True
                break
        if find:
            errors = []
            if png_width != width: errors.append("[分辨率] 宽 不匹配")
            if png_height != height: errors.append("[分辨率] 高 不匹配")
            if function == "": errors.append("[处理函数] 未指定")
            elif not (hasattr(op, function) and callable(getattr(op, function))): errors.append("[处理函数] 不存在")
            if not enabled: errors.append("[日期段状态] 禁用")
            if len(errors):
                for e in errors:
                    print(f"        {e}")
                    print("        跳过")
                    print("    -----")
                print()
                continue
        else:
            print(f"        未匹配到日期段 跳过")
            print("    -----")
            print()
            continue

        ocr_function = getattr(op, function)
        ocrrespack = ocr_function(png)
        print("    OCR完成")
        print("    -----")

        # 数据包添加
        datapack.append((png_path.stem, ocrrespack))

        print()
    
    # 数据包后处理
    dpp.datapack_output_to_htxsheet(datapack, Path("htxsheet.csv"))
