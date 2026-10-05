#!/usr/bin/env python3
"""anagram —— 终端变位词小工具。

在内置词表里找某个单词的变位词（anagram），或找出能用给定字母拼出的所有单词
（Scrabble / 拼字游戏帮手）。纯标准库，纯本地运行。
"""
import argparse
import json
import sys
from collections import Counter

VERSION = "0.1.0"

_WORDS_TEXT = """
listen silent enlist inlets tinsel
lines sent nest nets inset
sit tin line lens lent
evil vile live veil
stop pots tops spot post opts
dear read dare
angel angle glean
dusty study
night thing
inch chin
earth heart hater
brake break baker
elbow below bowel
arc car
state taste teats
master stream tamers
least slate stale steal tales
care race
loop pool polo
stressed desserts
drawer reward warder
lemon melon
anger range
cinema iceman anemic
diet tide tied
flow wolf
sheet heist
parse spare spear rapes reaps
alert later alter
meat mate team tame
part trap rapt
ate eat tea
now won
god dog
act cat
tap pat apt
war raw
top pot opt
lap pal alp
gnat tang
item time mite emit
save vase
snap naps pans
regal large glare lager
notes stone tones onset
stare rates tears aster taser
crate trace cater react caret
danger garden ranged gander
fined fiend
haste heats hates
apple banana cherry grape kiwi mango peach pear plum
bread butter cheese egg milk honey sugar salt pepper
house home room door window wall roof floor garden
water fire air stone wood metal gold silver
sun moon star sky cloud rain snow wind storm
tree flower grass leaf root branch seed fruit
river lake sea ocean beach wave sand island
mountain hill valley field farm road bridge street city town village
bus train plane ship bike
bird fish horse cow pig sheep mouse
book pen paper word page write story poem song music dance
love hate happy sad angry calm brave kind
mother father sister brother child baby man woman boy girl friend
day week month year morning evening spring summer autumn winter
red blue green yellow black white pink brown gray orange purple
one two three four five six seven eight nine ten
head hand foot eye ear nose mouth blood bone skin
king queen prince knight sword shield battle peace
school teacher student learn class test
work job money rich poor buy sell price shop
food drink cook sweet sour bitter fresh
shirt pants shoes hat coat dress
phone computer radio clock watch key light
smile laugh cry sing run jump swim fly walk climb
table chair lamp mirror knife fork spoon plate cup bowl
"""

# 去重并保序
WORDS = list(dict.fromkeys(_WORDS_TEXT.split()))


def signature(word):
    """变位签名：字母排序后相同的单词互为变位词。"""
    return "".join(sorted(word))


def find_anagrams(word, words):
    """找 word 的全部变位词（不含自身），按字母序返回。"""
    sig = signature(word)
    return sorted(w for w in words if w != word and signature(w) == sig)


def find_subwords(letters, words, min_len):
    """找出能用 letters 拼出的全部单词（每个字母至多用出现次数那么多）。"""
    pool = Counter(letters)
    out = []
    for w in words:
        if len(w) < min_len or len(w) > len(letters):
            continue
        c = Counter(w)
        if all(pool[ch] >= n for ch, n in c.items()):
            out.append(w)
    # 长的在前，同长度按字母序
    return sorted(out, key=lambda w: (-len(w), w))


def main(argv=None):
    p = argparse.ArgumentParser(
        prog="anagram",
        description="在终端里找变位词，或当拼字游戏帮手。纯本地，无网络。",
    )
    p.add_argument("word", nargs="?", help="要找变位词的单词")
    p.add_argument("--contains", metavar="LETTERS",
                   help="找出能用这些字母拼出的单词（Scrabble 帮手）")
    p.add_argument("--min", type=int, default=3, metavar="N",
                   help="--contains 模式下最短词长（默认 3）")
    p.add_argument("--json", action="store_true", help="JSON 输出")
    p.add_argument("--version", action="version", version="%(prog)s " + VERSION)
    args = p.parse_args(argv)

    if args.contains and args.word:
        print("error: --contains 和单词不能同时指定。", file=sys.stderr)
        return 2

    if args.contains:
        letters = args.contains.lower()
        if not letters.isalpha():
            print("error: --contains 只接受字母。", file=sys.stderr)
            return 2
        if args.min < 1:
            print("error: --min 必须大于等于 1。", file=sys.stderr)
            return 2
        found = find_subwords(letters, WORDS, args.min)
        if args.json:
            print(json.dumps({"letters": letters, "min_len": args.min,
                              "words": found}, ensure_ascii=False))
        elif found:
            print(f"用「{letters}」能拼出 {len(found)} 个单词（词长 >= {args.min}）：")
            for w in found:
                print(f"  {w}")
        else:
            print(f"用「{letters}」拼不出词长 >= {args.min} 的单词。")
        return 0

    if not args.word:
        p.print_usage(sys.stderr)
        print("error: 请给出一个单词，或用 --contains 指定字母。", file=sys.stderr)
        return 2
    word = args.word.lower()
    if not word.isalpha():
        print("error: 单词只接受字母。", file=sys.stderr)
        return 2
    found = find_anagrams(word, WORDS)
    if args.json:
        print(json.dumps({"word": word, "anagrams": found}, ensure_ascii=False))
    elif found:
        print(f"「{word}」的变位词（{len(found)} 个）：")
        for w in found:
            print(f"  {w}")
    else:
        print(f"词表里没有「{word}」的变位词。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
