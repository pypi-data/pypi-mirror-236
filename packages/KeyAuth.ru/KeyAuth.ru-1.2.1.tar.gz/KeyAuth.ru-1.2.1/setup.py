from setuptools import setup, find_packages

def README():
    with open("README.md", "r") as file:
        return file.read()

setup(
    name = "KeyAuth.ru",
    version = "1.2.1",
    author = "ttwiz_z",
    author_email = "moderkascriptsltd@gmail.com",
    description = "KeyAuth.ru API Wrapper for Python",
    long_description = README(),
    long_description_content_type = "text/markdown",
    url = "https://gist.github.com/ttwizz/88ded5b95c6b52c65e50196f555b51cd",
    packages = find_packages(),
    install_requires = ["requests>=2.31.0", "pywin32>=306"],
    classifiers = [
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    keywords = "KeyAuth.ru",
    project_urls = {
        "Author" : "https://github.com/ttwizz",
        "Organization" : "https://github.com/ModerkaScripts"
    },
    python_requires = ">=3.8"
)