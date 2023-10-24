from setuptools import setup, find_packages

setup(
    name='basex_ex',
    version='1.1',
    packages=find_packages(),
    install_requires=[
        'numpy~=1.24.3',
        'pandas~=2.0.2',
        'scipy~=1.10.1',
        'matplotlib~=3.7.1',
        'matplotlib_venn~=0.11.9'
        
    ],
    author='pin-people',
    author_email='rodrigo.toledo@pinpeople.com.br',
    description='Tools for EX Analysis',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
)
