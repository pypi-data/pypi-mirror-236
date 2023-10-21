
from setuptools import setup
# 公開用パッケージの作成 [ezpip]
import ezpip

# 公開用パッケージの作成 [ezpip]
with ezpip.packager(develop_dir = "./_develop_ezptn/") as p:
	setup(
		name = "ezptn",
		version = "0.0.1",
		description = "String pattern matching with placeholders.",
		author = "le_lattelle",
		author_email = "g.tiger.ml@gmail.com",
		url = "https://github.co.jp/",
		packages = p.packages,
		install_requires = ["relpath", "ezpip", "sout"],
		long_description = p.long_description,
		long_description_content_type = "text/markdown",
		license = "CC0 v1.0",
		classifiers = [
			"Programming Language :: Python :: 3",
			"Topic :: Software Development :: Libraries",
			"License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication"
		],
	)
