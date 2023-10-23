from setuptools import setup, find_packages

setup(
    name='ccc007', # 包名
    version='0.1.6',   # 版本号
    description='ccc007的工具', # 描述   
    author='ccc007', # 作者    
    author_email='mengchao704653@gmail.com', # 邮箱
    url='https://github.com/1492949083/repo', # 项目主页 
    packages=find_packages(), # 需要打包的目录模块
    install_requires=[ # 依赖列表
        'pywin32',
    ],
    long_description=open('README.md').read()
)