
from setuptools import setup, find_packages

setup(
    name='tiger_Age',
    version='0.1',
    author='Kaina',
    author_email='b10930027@gapps.ntust.edu.tw',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'scipy',
        'opencv-python',
        'nibabel',
        'pandas',
        'scikit-learn',
        'tensorflow',
        'keras',
    ],  # 依赖项列表
)
