from setuptools import find_packages, setup

with open("README.rst", mode="r", encoding="utf-8") as f:
    long_description = f.read()

author = "am230"
name = "iwashi"
py_modules = [name]

setup(
    name=name,
    version="1.1.3",
    keywords=("generator"),
    description="Link Tree Generator",
    long_description=long_description,
    install_requires=["requests", "bs4", "yt-dlp", "loguru", "typingdict", "click"],
    license="MIT Licence",
    long_description_content_type="text/x-rst",
    packages=find_packages(),
    url=f"https://github.com/{author}/{name}",
    author=author,
    author_email="am.230@outlook.jp",
    py_modules=py_modules,
    platforms="any",
)
