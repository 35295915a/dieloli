from types import FunctionType
from wcwidth import wcswidth
from Script.Core import rich_text, constant
from Script.Config import game_config


def align(text: str, just="left", only_fix=False, columns=1, text_width=None) -> str:
    """
    文本对齐处理函数
    Keyword arguments:
    text -- 需要进行对齐处理的文本
    just -- 文本的对齐方式(right/center/left) (default 'left')
    only_fix -- 只返回对齐所需要的补全文本 (default False)
    columns -- 将行宽平分指定列后，再进行对齐补全 (default 1)
    text_width -- 指定行宽，为None时将使用game_config中的配置 (default None)
    Return arguments:
    str -- 对齐后的文本
    """
    count_index = get_text_index(text)
    if text_width is None:
        width = game_config.config_normal.text_width
        width = int(width / columns)
    else:
        width = int(text_width)
    if just == "right":
        if only_fix:
            return " " * (width - count_index)
        else:
            return " " * (width - count_index) + text
    elif just == "left":
        if only_fix:
            return " " * (width - count_index)
        else:
            return text + " " * (width - count_index)
    elif just == "center":
        width_i = width / 2
        count_i = count_index / 2
        if only_fix:
            return " " * int(width_i - count_i)
        else:
            return " " * int(width_i - count_i) + text + " " * int(width_i - count_i)


def get_text_index(text: str) -> int:
    """
    计算文本最终显示的真实长度
    Keyword arguments:
    text -- 要进行长度计算的文本
    """
    text_style_list = rich_text.get_rich_text_print(text, "standard")
    text_index = 0
    style_width = 0
    style_name_list = list(game_config.config_font_data.keys())
    for i in range(0, len(style_name_list)):
        style_text_head = "<" + style_name_list[i] + ">"
        style_text_tail = "</" + style_name_list[i] + ">"
        if style_text_head in text:
            if style_name_list[i] in bar_list:
                text = text.replace(style_text_head, "")
                text = text.replace(style_text_tail, "")
            else:
                text = text.replace(style_text_head, "")
                text = text.replace(style_text_tail, "")
    for i in range(len(text)):
        text_index += wcswidth(text[i])
    return text_index + style_width


def full_to_half_text(ustring: str) -> str:
    """
    将全角字符串转换为半角
    Keyword arguments:
    ustring -- 要转换的全角字符串
    """
    rstring = ""
    for uchar in ustring:
        inside_code = ord(uchar)
        if inside_code == 12288:
            inside_code = 32
        elif inside_code >= 65281 and inside_code <= 65374:
            inside_code -= 65248
        aaa = chr(inside_code)
        rstring += aaa
    return rstring


def id_index(now_id: int) -> str:
    """
    生成命令id文本
    Keyword arguments:
    now_id -- 命令id
    Return arguments:
    str -- id文本
    """
    if now_id >= 100:
        return f"[{now_id}]"
    elif now_id >= 10:
        if now_id:
            return f"[0{now_id}]"
        return "[000]"
    return f"[00{now_id}]"
