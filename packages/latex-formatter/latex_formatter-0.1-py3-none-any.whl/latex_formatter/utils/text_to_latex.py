from typing import Dict, Optional, Union
from .transfer import transfer_to_dict


all  = [
    "to_latex",
    "to_string",
    "to_arc",
    "to_arrow",
    "to_arrow_down",
    "to_equation",
    "to_fraction",
    "to_latexarray",
    "to_latexwrap",
    "to_limit",
    "to_average",
    "to_repeater",
    "to_repeating",
    "to_root",
    "to_script",
    "to_sum",
    "to_underbrace",
    "to_underline",
    "to_valence",
    "to_vector",
    "to_font",
    "to_img",
    "to_list",
    "to_matrix",
    "to_richtext",
    "to_select",
    "to_multiselect",
    "to_table",
    "to_text",
    "to_bold",
    "to_italic",
    "to_unit",
]


def lls():
    print("lls")

def to_latex(data: Dict[str, Union[str, Dict]]) -> str:
    return str(data)


def to_string(data):
    return data["value"]


def to_arc(data: Dict[str, str]) -> str:
    data = transfer_to_dict(data)
    print(f"data is {data}, {type(data)}")
    return "\\overset{\\LARGE{\\frown}}{%s}" % data["value"]


def to_arrow(data: Dict[str, Dict[str, str]]) -> str:
    data = transfer_to_dict(data)
    top = data["value"]["top"]
    bottom = data["value"]["bottom"]
    return f"\\xrightarrow[{bottom}]{{{top}}}"


def to_arrow_down(data: Dict[str, Dict[str, str]]) -> str:
    data = transfer_to_dict(data)
    left_lines = data["value"]["left"].split("[br]")
    right_lines = data["value"]["right"].split("[br]")

    total_lines = max(len(left_lines), len(right_lines))
    middle_row = total_lines // 2

    rows = []
    for i in range(total_lines):
        l = left_lines[i] if i < len(left_lines) else ""
        r = right_lines[i] if i < len(right_lines) else ""
        arrow = "\\downarrow" if i == middle_row else ""
        rows.append(f"{l} & {arrow} & {r} \\\\")

    return f"""
    \\begin{{array}}{{lcl}}
    {''.join(rows)}
    \\end{{array}}
    """


def to_equation(data):
    data = transfer_to_dict(data)
    equations = "\\\\".join(data["value"])  # 将方程式使用双反斜杠连接

    left_brace = ""
    right_brace = ""

    # 根据 "direction" 来决定添加哪种括号
    direction = data.get("direction", "left")
    if direction == "left":
        left_brace = "\\left\\{"
        right_brace = "\\right."
    elif direction == "right":
        left_brace = "\\left."
        right_brace = "\\right\\}"
    elif direction == "both":
        left_brace = "\\left\\{"
        right_brace = "\\right\\}"
    elif direction == "parentheses_left":
        left_brace = "\\left("
        right_brace = "\\right."
    elif direction == "parentheses_right":
        left_brace = "\\left."
        right_brace = "\\right)"
    elif direction == "parentheses_both":
        left_brace = "\\left("
        right_brace = "\\right)"

    return f"{left_brace} \\begin{{aligned}} {equations} \\end{{aligned}} {right_brace}"


def to_fraction(data):
    data = transfer_to_dict(data)
    numerator = data["value"]["numerator"]
    denominator = data["value"]["denominator"]
    return f"\\frac{{{numerator}}}{{{denominator}}}"


def to_latexarray(data):
    data = transfer_to_dict(data)
    rows = []
    left_brace = "\\left\\{"
    right_brace = "\\right."
    if data["type"] == "latexarray":
        value_list = data["value"]
        for value in value_list:
            if len(value) == 1:
                converted_row = value
                rows.append(" & ".join(converted_row))
            else:
                temp_str = ""
                for v in value:
                    if isinstance(v, str):
                        temp_str += v
                    # Todo: recursion
                    else:
                        if v["type"] == "fraction":
                            numerator = v["value"]["numerator"]
                            denominator = v["value"]["denominator"]
                            temp_str += f"\\frac{{{numerator}}}{{{denominator}}}"
                converted_row = temp_str

                rows.append(temp_str)
        s = "\\begin{{array}}{{c}} {} \\end{{array}}".format(" \\\\ ".join(rows))
        return f"{left_brace} \\begin{{aligned}} {s}\\end{{aligned}} {right_brace}"


def to_latexwrap(data):
    data = transfer_to_dict(data)
    rows = []
    left_symbol = data.get("left", "{")
    right_symbol = data.get("right", ".")

    # 根据 left_symbol 和 right_symbol 选择适当的 LaTeX 符号
    if left_symbol == "{":
        left_brace = "\\left\\{"
    elif left_symbol == "(":
        left_brace = "\\left("
    else:
        left_brace = "\\left."

    if right_symbol == "}":
        right_brace = "\\right\\}"
    elif right_symbol == "(":
        right_brace = "\\right("
    elif right_symbol == ")":
        right_brace = "\\right)"
    else:
        right_brace = "\\right."
    for value in data["value"]:
        if isinstance(value, str):
            rows.append(value)
        else:
            type = value["type"]
            if type == "latexarray":
                latex_col = (
                    " \\begin{array}{c} "
                    + " \\\\ ".join(v[0] for v in value["value"])
                    + " \\end{array} "
                )
                rows.append(latex_col)

    s = " & ".join(rows)
    return f"{left_brace} \\begin{{aligned}} {s}\\end{{aligned}} {right_brace}"


def to_limit(data):
    data = transfer_to_dict(data)
    lower = data["value"]["lower"]
    function = data["value"]["function"]
    return f"\\lim_{{{lower}}} {function}"


def to_average(data):
    data = transfer_to_dict(data)
    value = data["value"]
    return f"\\overline{{{value}}}"


def to_repeater(data):
    data = transfer_to_dict(data)
    value = data["value"]
    # 使用 \dot 来为数字添加点
    return f"\\dot{{{value}}}"


def to_repeating(data):
    data = transfer_to_dict(data)
    if data["type"] == "repeating":
        pre = data["value"]["pre"]
        repeater = data["value"]["repeater"]

        # 根据 repeater 的长度，决定如何为数字添加点
        if len(repeater) == 1:
            repeater_latex = f"\\dot{{{repeater}}}"
        elif len(repeater) == 2:
            repeater_latex = f"\\dot{{{repeater[0]}}}\\dot{{{repeater[1]}}}"
        else:
            repeater_latex = (
                f"\\dot{{{repeater[0]}}}{repeater[1:-1]}\\dot{{{repeater[-1]}}}"
            )

        return f"0.{pre}{repeater_latex}"


def fraction_to_latex(data):
    if not isinstance(data, dict):
        data = transfer_to_dict(data)
    numerator_content = []
    for item in data["value"]["numerator"]:
        if isinstance(item, str):
            numerator_content.append(item)
        elif item["type"] == "script":
            numerator_content.append(script_to_latex(item))
    numerator = "".join(numerator_content)
    denominator = data["value"]["denominator"]
    return f"\\displaystyle \\frac{{{numerator}}}{{{denominator}}}"


def script_to_latex(data):
    if not isinstance(data, dict):
        print("not dict")
        data = transfer_to_dict(data)
    front = data["value"]["front"]
    sub = data["value"]["sub"]
    return f"{front}_{{{sub}}}"


def to_root(data):
    data = transfer_to_dict(data)
    if data["type"] == "root":
        index = data["value"].get("index", "")
        if index:
            index_part = f"[{index}]"
        else:
            index_part = ""

        radicand = data["value"]["radicand"]
        if radicand["type"] == "fraction":
            radicand_latex = fraction_to_latex(radicand)
        else:
            radicand_latex = radicand  # 这里可能还需要根据不同的类型进行扩展

        return f"\\displaystyle \\sqrt{index_part}{{{radicand_latex}}}"


def to_script(data):
    data = transfer_to_dict(data)
    front = data["value"]["front"]
    sup = data["value"].get("sup", "")
    sub = data["value"].get("sub", "")

    if sup and sub:  # 同时存在上标和下标
        return f"\\displaystyle {front}^{{{sup}}}_{{{sub}}}"
    elif sup:  # 只存在上标
        return f"\\displaystyle {front}^{{{sup}}}"
    elif sub:  # 只存在下标
        return f"\\displaystyle {front}_{{{sub}}}"
    else:  # 不应该出现既没有上标也没有下标的情况
        return front


def to_sum(data):
    data = transfer_to_dict(data)
    upper_bound = data["value"]["upper"]["value"]
    lower_bound = data["value"]["lower"]["value"]
    variable = data["value"]["variable"]

    return f"\\displaystyle \\sum_{{{lower_bound}}}^{{{upper_bound}}} {variable}"


def to_underbrace(data):
    data = transfer_to_dict(data)
    top_data = data["value"]["top"]["value"]
    top_elements = []
    for item in top_data:
        if item["type"] == "string":
            top_elements.append(item["value"])
        elif item["type"] == "script":
            front = item["value"]["front"]
            sup = item["value"].get("sup", "")
            sub = item["value"].get("sub", "")
            if sup:
                top_elements.append(f"{front}^{{{sup}}}")
            if sub:
                top_elements.append(f"{front}_{{{sub}}}")
    top_string = "".join(top_elements)

    # 获取bottom部分的值
    bottom = data["value"]["bottom"]

    return f"\\displaystyle \\underbrace{{{top_string}}}_{{\\text{{{bottom}}}}}"


def to_underline(data):
    data = transfer_to_dict(data)
    value = data["value"]
    return f"\\displaystyle \\underline{{{value}}}"


def to_valence(data):
    data = transfer_to_dict(data)
    top_value = data["value"]["top"]["value"]
    bottom_value = data["value"]["bottom"]["value"]

    return f"\\displaystyle \\stackrel{{{top_value}}}{{{bottom_value}}}"


def to_vector(data):
    data = transfer_to_dict(data)
    value = data["value"]
    return f"\\displaystyle \\vec{{{value}}}"


def to_font(data):
    data = transfer_to_dict(data)
    color = data["color"]
    value = data["value"]
    return f"\\displaystyle \\textcolor{{{color}}}{{{value}}}"


def to_img(data):
    data = transfer_to_dict(data)
    # 检查是否有svg路径
    src = data["value"]["svg_src"] if data["value"]["svg_src"] else data["value"]["src"]
    width = data["value"]["width"]
    height = data["value"]["height"]

    # 在实际LaTeX文档中，您可能需要提前设置图片的路径
    # \graphicspath{{<path to your images>}}
    return f"\\includegraphics[width={width}px,height={height}px]{{{src}}}"


def to_list(data):
    data = transfer_to_dict(data)
    items = data["value"]
    latex_lines = []

    for item in items:
        tag = item["tag"]
        content = item["content"]
        # 连接标签和内容
        latex_lines.append(f"{tag}{content}")

    return "\\\\".join(latex_lines)


def to_matrix(data):
    data = transfer_to_dict(data)
    matrix = data["value"]
    latex_rows = []

    for row in matrix:
        latex_rows.append(" & ".join(row))

    return "\\begin{bmatrix} " + " \\\\ ".join(latex_rows) + " \\end{bmatrix}"


def to_richtext(data):
    data = transfer_to_dict(data)
    value = data["value"]
    if value["type"] == "merge":
        merged_items = value["value"]
        latex_parts = []
        for item in merged_items:
            if item["type"] == "string":
                latex_parts.append(to_string(item))
            elif item["type"] == "script":
                latex_parts.append(script_to_latex(item))
            # 这里可以添加其他数据类型的处理
        return "".join(latex_parts)
    else:
        # 对于其他可能的rich text内容，可以在这里添加处理方法
        pass


def to_select(data):
    data = transfer_to_dict(data)
    # 获取必要的数据
    options = data["options"]
    solution = data["solution"]
    no = data["no"]

    # 开始组装题目文本
    output = []

    # 添加题号
    output.append(f"**{no}.** (多选)")

    # 循环遍历所有选项，并添加到输出中
    for opt in options:
        tag = opt["tag"]
        option_text = opt["option"]
        output.append(f"{tag}. {option_text}")

    # 添加答案
    output.append(f"\n**答案**: {solution}")

    return "\n".join(output)


def to_multiselect(data):
    data = transfer_to_dict(data)
    # 获取必要的数据
    options = data["options"]
    solution = data["solution"]
    no = data.get("no", "")

    # 开始组装题目文本
    output = []

    # 添加题号（如果有）
    if no:
        output.append(f"**{no}.**")

    # 循环遍历所有选项，并添加到输出中
    for opt in options:
        tag = opt["tag"]
        option_text = opt["option"]
        output.append(f"{tag}. {option_text}")

    # 添加答案
    solution_str = "、".join(solution)
    output.append(f"\n**答案**: {solution_str}")

    return "\n".join(output)


def to_table(data):
    data = transfer_to_dict(data)
    rows = data["value"]

    # 开始组装LaTeX表格
    output = ["\\begin{tabular}{|c|c|}"]
    output.append("\\hline")

    for row in rows:
        row_content = []
        for cell in row:
            value = cell["value"]
            # 如果值是一个列表，则处理列表内容
            if isinstance(value, list):
                value = process_cell_content(value)
            # 根据colspan和rowspan添加相应的指令
            cell_content = f"\\multicolumn{{{cell['colspan']}}}{{|c|}}{{\\multirow{{{cell['rowspan']}}}{{*}}{{{value}}}}}"
            row_content.append(cell_content)
        output.append(" & ".join(row_content) + " \\\\ \\hline")

    output.append("\\end{tabular}")

    return "\n".join(output)


def process_cell_content(cell_content):
    data = transfer_to_dict(data)
    processed = []
    for item in cell_content:
        if "type" in item:
            if item["type"] == "colorpink":
                processed.append(f"\\textcolor{{pink}}{{{item['value']}}}")
            elif item["type"] == "script":
                front = item["value"]["front"]
                sup = item["value"]["sup"]
                processed.append(f"{front}$^{{{sup}}}$")
        else:
            processed.append(item)
    return "".join(processed)


def to_text(data, solution_content):
    data = transfer_to_dict(data)
    # 获取填空内容
    value = (
        solution_content[data["index"]] if data["index"] < len(solution_content) else ""
    )

    # 如果value为空，使用blank代替
    if not value:
        value = data["blank"]

    # 判断是否支持换行
    if data["wordwrap"]:
        value = "\\newline ".join(value.split("\n"))

    # 判断是否适配填空长度
    if not data["noautowidth"]:
        value = "\\underline{\\hspace{" + str(len(value) * 0.8) + "cm}}"
    else:
        value = "\\underline{" + value + "}"

    return value


def to_bold(data):
    data = transfer_to_dict(data)
    return f"\\textbf{{{data['value']}}}"


def to_italic(data):
    data = transfer_to_dict(data)
    return f"\\textit{{{data['value']}}}"


def to_unit(data):
    data = transfer_to_dict(data)
    return f"\\mathrm{{{data['value']}}}"

functions_list  = [
    to_latex,
    to_string,
    to_arc,
    to_arrow,
    to_arrow_down,
    to_equation,
    to_fraction,
    to_latexarray,
    to_latexwrap,
    to_limit,
    to_average,
    to_repeater,
    to_repeating,
    to_root,
    to_script,
    to_sum,
    to_underbrace,
    to_underline,
    to_valence,
    to_vector,
    to_font,
    to_img,
    to_list,
    to_matrix,
    to_richtext,
    to_select,
    to_multiselect,
    to_table,
    to_text,
    to_bold,
    to_italic,
    to_unit,
]

conversion_functions = {func.__name__[3:]: func for func in functions_list}
