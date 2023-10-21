# ezptn

## Overview
- String pattern matching with placeholders.
- プレースホルダーを使った文字列パターンマッチ

## Usage
```python
import ezptn

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
```
