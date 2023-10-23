from setuptools import setup, find_packages

setup(
    name='bahila_extractor',
    version='0.2.3',
    packages=find_packages(),
    install_requires=[
        # 'theguardian',
        # 'theguardian-api-python',
        'requests',
        'openai',
        'bs4',
        'langchain',
        # any other dependencies
    ],
)
