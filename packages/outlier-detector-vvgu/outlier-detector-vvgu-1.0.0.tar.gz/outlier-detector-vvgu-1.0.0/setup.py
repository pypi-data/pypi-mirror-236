from setuptools import setup, find_packages


def readme():
    with open('README.md', 'r') as f:
        return f.read()


setup(
    name='outlier-detector-vvgu',
    version='1.0.0',
    author='Artorius',
    author_email='Artorius.81@yandex.ru',
    description='Small package for detecting outliers',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/Artorius81',
    packages=find_packages(),
    install_requires=['requests>=2.25.1'],
    classifiers=[
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    keywords='example python',
    project_urls={
        'GitHub': 'https://github.com/Artorius81'
    },
    python_requires='>=3.7'
)
