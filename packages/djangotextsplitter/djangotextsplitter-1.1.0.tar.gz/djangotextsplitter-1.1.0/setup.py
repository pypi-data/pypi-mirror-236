from distutils.core import setup

setup(
    name="djangotextsplitter",  # Name of the package
    packages=["djangotextsplitter"],  # Best to keep this the same as the name of the package.
    version="1.1.0",  # Speaks for itself, keep in sync with the textsplitter-class!
    license="MIT",  # Most commonly used licenses: https://help.github.com/articles/licensing-a-repository
    description="This package allows the pdftextsplitter engine to communicate with a Django-database",
    author="Unit Data en Innovatie, Ministerie van Infrastructuur en Waterstaat, Netherlands",
    author_email="dataloket@minienw.nl",  # Contact email address
    url="https://gitlab.com/datainnovatielab/public/djangotextsplitter/dist/",
    download_url="https://gitlab.com/datainnovatielab/public/djangotextsplitter/dist/",
    keywords=["NLP", "PDF", "Text recognition", "Structure recognition", "ChatGPT"],
    install_requires=[  # the list of dependencies: other packages that your package needs to function.
        "setuptools>=59.6.0",
        "wheel>=0.41.1",
        "build>=0.10.0",
        "numpy>=1.25.2",
        "pandas>=2.0.3",
        "coverage>=7.3.0",
        "django>=4.2.4",
        "pylint>=2.17.5",
        "pdftextsplitter>=1.2.3",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",  # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        "Intended Audience :: Developers",  # The intended audience for the package
        "Topic :: Software Development :: Build Tools",  # Better to keep this as it is.
        "License :: OSI Approved :: MIT License",  # Should be the same as the previous license choice.
        "Programming Language :: Python :: 3.10",  # Specification of which python versions are supported.
    ],
)
