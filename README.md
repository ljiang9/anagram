# anagram

终端变位词小工具：给一个英文单词，找出它的全部变位词（anagram）；
或给一把字母，找出能拼出的所有单词（Scrabble / 拼字游戏帮手）。

纯 Python 标准库，纯本地运行，无网络。

## 安装

无需安装，Python 3.10+ 直接运行：

```bash
cd anagram
python3 -m anagram listen
```

## 用法

```bash
# 找变位词
python3 -m anagram listen
# → silent / enlist / inlets / tinsel

# 大小写不敏感
python3 -m anagram LISTEN

# 拼字帮手：用这些字母能拼出哪些词
python3 -m anagram --contains listen
python3 -m anagram --contains listen --min 4   # 只看 4 个字母以上的

# JSON 输出（给脚本用）
python3 -m anagram listen --json
python3 -m anagram --contains abc --json
```

### 参数

| 参数 | 说明 |
|---|---|
| `word` | 要找变位词的单词（位置参数） |
| `--contains LETTERS` | 拼字模式：找出能用这些字母拼出的单词 |
| `--min N` | 拼字模式下最短词长，默认 3 |
| `--json` | JSON 输出 |
| `--version` | 版本号 |

`word` 和 `--contains` 不能同时给；都没给时报错并提示用法。

## 设计取舍

- **内置词表约 370 个常用英文单词**（人工精选，含多组经典变位词家族），不是完整词典。
  冷僻词可能找不到变位词——这是"小巧"的代价，不是 bug。
- 变位判定用"字母排序签名"，O(n) 建表，查询飞快。
- 拼字模式每个字母至多用它在输入里出现的次数那么多，结果按"长的在前、同长度按字母序"排列。
- 只支持英文字母；查不到时给一句中文提示，不抛 traceback。

## 已知局限

- 词表是人工精选快照：只有约 370 词，拼对但冷僻的词会被判"没有变位词"。
- 不含专有名词（如 Stein、Intel 这类）。
- 英文 only，没有中文变位（中文按字变位意义不大）。

## 许可证

MIT，Copyright (c) 2026 ljiang9。
