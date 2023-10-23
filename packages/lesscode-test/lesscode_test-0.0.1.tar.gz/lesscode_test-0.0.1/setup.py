# -*- coding: utf-8 -*-

import setuptools
from lesscode_test.version import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="lesscode_test",
    version=__version__,
    author="navysummer",
    author_email="navysummer@yeah.net",
    description="lesscode_test是低代码测试框架",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitee.com/navysummer/lesscode_test",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        # "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    platforms='python',
    install_requires=[
        "APScheduler>=3.9.1",
        "PyYAML>=6.0.1",
        "gevent>=22.10.2",
        "httpx>=0.24.1",
        "lesscode_options>=0.0.0"
    ]

)

"""
1、打包流程
打包过程中也可以多增加一些额外的操作，减少上传中的错误

# 先升级打包工具
pip install --upgrade setuptools wheel twine

# 打包
python setup.py sdist bdist_wheel

# 检查
twine check dist/*

# 上传pypi
twine upload dist/*
twine upload dist/* --repository-url https://pypi.chanyeos.com/ -u admin -p shangqi
# 安装最新的版本测试
pip install -U lesscode_test -i https://pypi.org/simple
pip install -U lesscode_test -i https://pypi.chanyeos.com/simple
"""
