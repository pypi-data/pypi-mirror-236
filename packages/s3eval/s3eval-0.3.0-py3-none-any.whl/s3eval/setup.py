from setuptools import setup, find_packages

setup(
    name='S3Eval',  # 包的名称
    version='0.1.1',  # 包的版本号
    author='Fangyu Lei',  # 作者名称
    author_email='leifangyu@qq.com',  # 作者邮箱
    description='S3Eval: A Synthetic, Scalable and Systematic Evaluation Suite for Language Models',  # 包的描述信息
    url='https://github.com/lfy79001/S3Eval',  # 包的项目主页或相关链接
    packages=find_packages(),  # 包含的包列表
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],  # 包的分类标签
    install_requires=[
        'pandas'
    ],  
)