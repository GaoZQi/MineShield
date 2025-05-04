import chardet


def detect_encoding(file_path):
    with open(file_path, "rb") as f:
        result = chardet.detect(f.read())
    return result["encoding"]


def try_read_file(input_file, encodings):
    for enc in encodings:
        try:
            with open(input_file, "r", encoding=enc, errors="strict") as f:
                return f.read(), enc
        except Exception as e:
            print(f"用 {enc} 读取失败：{e}")
    raise Exception("所有编码都读取失败！")


def convert_to_utf8(input_file, output_file):
    detected_encoding = detect_encoding(input_file)
    print(f"chardet 检测到编码：{detected_encoding}")

    encodings_to_try = [detected_encoding, "windows-1251", "utf-8", "latin1"]
    try:
        content, used_encoding = try_read_file(input_file, encodings_to_try)
        print(f"成功使用编码：{used_encoding}")
    except Exception as e:
        print(f"严格读取失败，尝试宽容模式：{e}")
        with open(input_file, "r", encoding=detected_encoding, errors="replace") as f:
            content = f.read()
        print(f"使用 {detected_encoding} 严格失败，但在 replace 模式下成功读取。")

    with open(output_file, "w", encoding="utf-8") as f_out:
        f_out.write(content)
    print(f"已将 {input_file} 转换为 UTF-8 并保存为 {output_file}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        print("用法: python convert_encoding.py <输入文件> <输出文件>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    try:
        convert_to_utf8(input_file, output_file)
    except Exception as e:
        print(f"转换出错：{e}")
