# XML to SRT Converter

一个基于 PyQt5 的图形界面工具，用于将特定格式的 XML 字幕文件批量转换为标准 SRT 字幕文件。

## 功能特性

- 批量转换指定文件夹内的所有 `.xml` 字幕文件
- 自动从 XML 中读取帧率（`timebase`）并将帧号转换为时间码
- 生成标准的 SRT 格式（含序号、时间轴、字幕文本）
- 简单易用的图形界面，无需命令行操作
- 支持选择输入目录和输出目录

## 依赖安装

### 1. Python 环境
确保已安装 Python 3.6 及以上版本。

### 2. 安装依赖库
本工具依赖 PyQt5，可以使用 pip 安装：

```bash
pip install PyQt5
```

或使用国内镜像加速：

```bash
pip install PyQt5 -i https://pypi.tuna.tsinghua.edu.cn/simple
```

## 使用方法

### 运行程序

```bash
python xmlToSrt.py
```

### 操作步骤

1. 点击 **选择导入 XML 目录**，选中存放 `.xml` 字幕文件的文件夹
2. 点击 **选择导出 SRT 目录**，选中转换后 `.srt` 文件的输出文件夹
3. 点击 **开始转换**，程序将自动处理文件夹中所有 `.xml` 文件
4. 转换完成后弹出提示，显示成功转换的文件数量

## XML 输入格式说明

程序要求 XML 文件遵循以下结构：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<root>
    <timebase>25</timebase>
    <generatoritem>
        <start>100</start>
        <end>250</end>
        <parameter>
            <parameterid>str</parameterid>
            <value>这是第一句字幕</value>
        </parameter>
    </generatoritem>
    <generatoritem>
        <start>300</start>
        <end>450</end>
        <parameter>
            <parameterid>str</parameterid>
            <value>第二句字幕</value>
        </parameter>
    </generatoritem>
</root>
```

**字段说明：**

| 字段 | 说明 |
|------|------|
| `timebase` | 视频帧率（fps），用于将帧号转换为时间 |
| `generatoritem` | 每一条字幕的容器 |
| `start` / `end` | 字幕开始和结束的**帧号**（整数） |
| `parameterid` 为 `'str'` 的 `value` | 字幕文本内容 |

> ⚠️ 注意：若某条字幕的 `start`、`end` 或 `value` 缺失或为空，该条字幕将被自动跳过。

## 输出 SRT 格式示例

假设帧率为 `25`，帧号 `100` 到 `250` 的字幕将转换为：

```
1
00:00:04,000 --> 00:00:10,000
这是第一句字幕

2
...
```

时间计算公式：`秒 = 帧号 / 帧率`，毫秒部分精确到三位。

## 界面预览

- 两个按钮用于选择目录（按钮文字会显示选中的文件夹名称）
- 一个“开始转换”按钮
- 转换过程无进度条，完成后弹出消息框提示

## 常见问题

**Q：为什么转换后的 SRT 文件是空的？**  
A：请检查 XML 文件是否包含有效的 `<generatoritem>` 条目，且每个条目都有非空的 `start`、`end` 和 `value`。

**Q：程序报错 “No module named 'PyQt5'”？**  
A：请先执行 `pip install PyQt5` 安装依赖。

**Q：能否支持单个文件而不是文件夹？**  
A：当前版本仅支持按文件夹批量转换。如需单文件功能，可自行修改或提交 Issue。

## 许可证

MIT License
