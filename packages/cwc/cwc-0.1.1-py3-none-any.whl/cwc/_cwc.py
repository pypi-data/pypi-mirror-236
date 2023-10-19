# -*- coding: utf-8 -*-

# Install Require
# pip install mecab-python3
# pip install janome
# pip install wordcloud
# pip install pyperclip

import os
import re
import sys
from os.path import join as pathjoin
from wordcloud import WordCloud

font_path = "C:/Windows/Fonts/meiryo.ttc"
out_tmp = pathjoin(os.environ.get('TMP'), "tmp_wordcloud.png")

try:
    import MeCab
    t = MeCab.Tagger('-d Y:/usr/local/mecab/dic/ipadic/')

    def cwc(text, hinshi={"名詞"}, excludes=[]):

        node = t.parseToNode(text)
        ret = ""

        if hinshi and excludes:
            def chk(ns, wt):
                return wt in hinshi and all(e not in ns for e in excludes)
        elif hinshi:
            def chk(ns, wt):
                return wt in hinshi
        elif excludes:
            def chk(ns, wt):
                return all(e not in ns for e in excludes)

        while node:
            ns = node.surface
            if ns != "":
                wt = node.feature.split(",")[0]
                if chk(ns, wt):
                    ret += " " + ns
            node = node.next
            if node is None:
                break
        return ret
except Exception:
    from janome.tokenizer import Tokenizer

    def cwc(text, hinshi={"名詞"}, excludes=[]):
        t = Tokenizer()
        tokens = t.tokenize(text)
        ret = ""

        if not hinshi:
            def hfilter(s):
                return True
        elif len(hinshi) == 1:
            hinshi = list(hinshi)[0]

            def hfilter(s):
                return hinshi in s
        else:
            def hfilter(L):
                return L.split(",")[0] in hinshi

        if excludes:
            for token in tokens:
                s = token.surface
                if hfilter(token.part_of_speech) and all(x not in s for x in excludes):
                    ret += " " + s
        else:
            for token in tokens:
                if hfilter(token.part_of_speech):
                    ret += " " + token.surface

        return ret

def create_parser():
    from argparse import ArgumentParser

    parser = ArgumentParser(description="create wordcloud")
    padd = parser.add_argument

    padd('-o', '--outfile',
         help='outputfile path',
         default=out_tmp,
         )

    padd('-E', '--excludes', nargs='+',
         help='exclude files',
         default=[],
         )

    padd('-e', '--encoding',
         help='input file encoding',
         default="cp932",
         )

    padd('-H', '--hinshi', nargs='+',
         help='hinshi',
         default=["名詞"],
         )

    padd('-n', '--no_open', action='store_true',
         help='if finish when png file do not open '
         )

    padd('filename',
         metavar='<filename>',
         nargs="*",
         help='Text Source Files (default: clipboad text data)',
         )

    return parser.parse_args()

def main():
    import codecs
    import pyperclip
    try:
        import tkinter as tk
        from tkinter import messagebox

        def cerr(msg):
            tk.Tk().withdraw()
            messagebox.showinfo("エラーメッセージ", msg)
    except (ModuleNotFoundError, ImportError):
        def cerr(msg):
            sys.stderr.write(msg)

    args = create_parser()
    hinshi = set(args.hinshi)
    excludes = args.excludes

    if args.filename:
        text = ""
        for f in args.filename:
            try:
                with codecs.open(os.path.normpath(f), encoding=args.encoding) as fp:
                    text += fp.read()
            except UnicodeEncodeError:
                with codecs.open(os.path.normpath(f), encoding="utf-8") as fp:
                    text += fp.read()
    else:
        text = re.sub("\s", "", pyperclip.paste())

    if text:
        wc = WordCloud(font_path=font_path, collocations=False, width=1920, height=1080, background_color="white", colormap="winter")
        wc.generate(cwc(text, hinshi, excludes))
        wc.to_file(out_tmp)
        if not args.no_open:
            os.startfile(args.outfile)

    else:
        cerr("クリップボードが空っぽまたは、空白、タブ、改行のみで文章がないため処理を中止しました。\nワードクラウド化したい文章をコピーして再度実行してください。")


def test():
    test_text = """インストールされている Tkinter のバージョンを確認するには、Python シェルから次を実行します。"""
    wc = WordCloud(font_path=font_path, collocations=False, width=1920, height=1080, background_color="white", colormap="winter")
    wc.generate(cwc(test_text.replace("\r", "").replace("\n", "")))
    wc.to_file(out_tmp)
    os.startfile(out_tmp)


if __name__ == "__main__":
    test()
    # main()
