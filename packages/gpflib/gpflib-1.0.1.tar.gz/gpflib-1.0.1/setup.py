import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name="gpflib",  # 模块名称
    version="1.0.1",  # 当前版本
    author="endongxun",  # 作者
    author_email="edxun@126.com",  # 作者邮箱
    description="Grid-based Parsing Framework",  # 模块简介
    long_description=long_description,  # 模块详细介绍
    long_description_content_type="text/markdown",  # 模块详细介绍格式
    packages=setuptools.find_packages(),  # 自动找到项目中导入的模块
    
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
    ],
    
    package_data={
        'gpflib': ['gpflib.dll', 'config.txt', 'gpflib.py'],
    },
    
    install_requires=[
        'pywin32'
    ],
    
    python_requires='>=3',
)
