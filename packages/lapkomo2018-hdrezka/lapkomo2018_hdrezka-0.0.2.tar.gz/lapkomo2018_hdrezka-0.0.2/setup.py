from setuptools import setup, find_packages

setup(
    name="lapkomo2018_hdrezka",
    version="0.0.2",
    description="Package that help to get a direct film url from hdrezka.ag",
    long_description=open('README.txt').read(),
    author='lapkomo2018',
    author_email='lapkomo2018@gmail.com',
    packages=find_packages(),
    install_requires=[
        'selenium~=4.14.0',
        'requests~=2.31.0',
        'tqdm~=4.66.1',
        'webdriver-manager>=4.0.1'
    ],
    python_requires='~=3.10',
)
