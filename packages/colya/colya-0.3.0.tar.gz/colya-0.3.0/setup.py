from setuptools import setup, find_packages

with open("./README.md", "r") as fh:
    long_description = fh.read()

setup(  
    name = 'colya',  
    version = '0.3.0',
    description = 'A Satori QQBot Scripyt',  
    license = 'MIT License',  
    install_requires = [],  
    packages=find_packages(where='.', exclude=(), include=('*',)),
    # packages_data = {
    #     "Manager/":["*.py","*.js","*.css","*.vue","*.png"],
    # },
    include_package_data=True,   # 自动打包文件夹内所有数据
    author = 'Ysasm',  
    long_description=long_description,
    long_description_content_type="text/markdown",
    author_email = '1613921123@qq.com',
    url = 'https://gitee.com/YSASM/ColyaBot.git',
    # packages=setuptools.find_packages(), 
    classifiers=[
        "Programming Language :: Python :: 3"
    ],
)  
