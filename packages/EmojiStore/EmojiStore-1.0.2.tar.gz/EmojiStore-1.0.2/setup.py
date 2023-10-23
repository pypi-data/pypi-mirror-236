# This file uses the following encoding : utf-8

from setuptools import setup

with open("README.md", "r") as file:
    long_description = file.read()

setup(
    name='EmojiStore',
    packages=['EmojiStore'],
    version='1.0.2',
    license='MIT',
    description='Free unicode emojis ready to use !',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Antares Mugisho',
    author_email='antaresmugisho@gmail.com',
    url='https://antaresmugisho.vercel.app/',
    download_url='https://github.com/AntaresMugisho/EmojiStore/archive/refs/tags/v1.0-beta.tar.gz',
    keywords=['python', 'emoji', 'sticker', 'mood'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)
