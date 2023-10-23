from setuptools import setup, find_packages

long_description = '''
# Article Generation Framework

This is a framework for generating articles using OpenAI's GPT-3 API.
'''








setup(
    name='agf',
    version='0.1',
    description='Article Generation Framework',
    long_description=long_description,
    author='Fauzaan Gasim',
    author_email='hello@fauzaanu.com',
    packages=find_packages(),
    install_requires=[
        'openai==0.27.6',
        'python-dotenv==1.0.0',
    ]
)
