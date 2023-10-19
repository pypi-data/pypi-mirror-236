# hxz_pandora-Cloud

![Python version](https://img.shields.io/badge/python-%3E%3D3.7-green)
[![Issues](https://img.shields.io/github/issues-raw/zhile-io/hxz_pandora-cloud)](https://github.com/shoot82003/hxz_pandora-cloud/issues)
[![Commits](https://img.shields.io/github/last-commit/zhile-io/hxz_pandora-cloud/master)](https://github.com/shoot82003/hxz_pandora-cloud/commits/master)
[![PyPi](https://img.shields.io/pypi/v/hxz_pandora-cloud.svg)](https://pypi.python.org/pypi/hxz_pandora-cloud)
[![Downloads](https://static.pepy.tech/badge/hxz_pandora-cloud)](https://pypi.python.org/pypi/hxz_pandora-cloud)

[![PyPi workflow](https://github.com/shoot82003/hxz_pandora-cloud/actions/workflows/python-publish.yml/badge.svg)](https://github.com/shoot82003/hxz_pandora-cloud/actions/workflows/python-publish.yml)

### A package for hxz_pandora-ChatGPT



1.先打包,注意版本号__init__.py修改版本号
注意修改src的文件夹名
python setup.py sdist bdist_wheel

2.再上传pypi命令
twine upload --skip-existing --verbose -u __token__ -p pypi-AgEIcHlwaS5vcmcCJDg3YTQ3NzNlLWU3YjctNDFkOS04ZTQyLWFkNWQ2NzYwMDAxYgACKlszLCJiYWE5ZGY0ZS01OGRhLTQzMWMtOWJmYS1kMjIxNDNlNTg1MjAiXQAABiDR_mO7SkLd_caYiQkhYu68mAo5wd7KjpthKRO4AO3wsA dist/*

3.安装,注意版本号,因为刚上传的原因无法安装时,需-i进行安装

pip install shootpandora-ChatGPT~=20230725.1.2


pip install -i https://pypi.org/simple/ shootpandora-ChatGPT~=20230725.1.4


pip install -i https://pypi.org/simple/ shootpandora-Cloud~=20230725.1.4

4.若存在多个版本时会出错,可卸载后再pip install安装
pip uninstall shootpandora-chatgpt