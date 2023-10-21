
# 文字列パターンマッチ [ezptn]

import sys
from sout import sout

# 区切りリストによるパターンマッチ
def list_match(sep_ls, target_str):
	# セパレータが空の場合 (再帰終了条件)
	if len(sep_ls) == 0: return [(target_str,)]
	# 冒頭のセパレータ
	head_sep = sep_ls[0]
	# セパレータを順に見ていく
	div_ls = target_str.split(head_sep)
	if len(div_ls) == 1: return []	# セパレータが入っていない場合は「マッチしない」
	ret_ls = []
	for i in range(len(div_ls) - 1):
		left = head_sep.join(div_ls[:i+1])
		right = head_sep.join(div_ls[i+1:])
		# 再帰呼び出しして追記
		for e in list_match(sep_ls[1:], right):
			ret_ls.append((left,) + e)
	return ret_ls

# head_fix, tail_fixの処理
def fix_filter(raw_res, head_fix, tail_fix):
	ret_ls = []
	for e in raw_res:
		if head_fix is True:
			if e[0] != "": continue
			e = e[1:]
		if tail_fix is True:
			if e[-1] != "": continue
			e = e[:-1]
		ret_ls.append(e)
	return ret_ls

# パターンマッチ
def match(
	pattern,	# マッチパターン (文字列指定; %sでワイルドカードを指定)
	target_str,	# 解析対象の文字列
	allow_empty = True,	# ワイルドカードとして空文字列を許す
):
	# pattern == "" の場合
	if pattern == "": return ([tuple([])] if target_str == "" else [])
	# 区切りシーケンスのリスト
	sep_ls = pattern.split("%s")
	# 冒頭が%sではない場合
	head_fix = (sep_ls[0] != "")
	if head_fix is False: sep_ls = sep_ls[1:]
	# 末尾が%sではない場合
	tail_fix = (sep_ls[-1] != "")
	if tail_fix is False: sep_ls = sep_ls[:-1]
	# %sが連続していないことを確かめる
	if "" in sep_ls: raise Exception('[ezptn error] "%s" must not be consecutive.')
	# 区切りリストによるパターンマッチ
	raw_res = list_match(sep_ls, target_str)
	# head_fix, tail_fixの処理
	res = fix_filter(raw_res, head_fix, tail_fix)
	# ワイルドカードとして空文字を許さない場合
	if allow_empty is False:
		res = [e for e in res if "" not in e]
	return res
