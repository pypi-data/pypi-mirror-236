
# 文字列パターンマッチ [ezptn]
# 【動作確認 / 使用例】

import sys
from sout import sout
from ezpip import load_develop
# 文字列パターンマッチ [ezptn]
ezptn = load_develop("ezptn", "../", develop_flag = True)

# パターンマッチ
res = ezptn.match("lambda %s: %s", "lambda a: a ** 2")
print(res)	# -> [('a', 'a ** 2')]
res = ezptn.match("%s:%s", "13:12:24")
print(res)	# -> [('13', '12:24'), ('13:12', '24')]
res = ezptn.match("%s--%s", "hoge-fuga")
print(res)	# -> []
res = ezptn.match("%squid", "equid")
print(res)	# -> [('e',)]
res = ezptn.match("%s(%s)", "hoge(22)")
print(res)	# -> [('hoge', '22')]
res = ezptn.match("%s(%s)", "hoge()")
print(res)	# -> [('hoge', '')]
res = ezptn.match("%s(%s)", "hoge()", allow_empty = False)
print(res)	# -> []
res = ezptn.match("(%s,((%s,%s),%s))", '(23,(("s",44),44))')
print(res)	# -> [('23', '"s"', '44', '44')]
