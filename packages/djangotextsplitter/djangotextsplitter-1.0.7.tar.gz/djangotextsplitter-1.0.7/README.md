# djangotextsplitter

This package is meant as a django-extension for the pdftextsplitter package. As such, the pdftextsplitter package
should be installed before this package. <br />
<br />
This django-extension provides an out-of-the-box django-app with database models for the python-classes in pdftextsplitter.
As such, it becomes possible to store the results of the pdftextsplitter package in the django database. <br />
<br />
The django-application in this package does not contain any views, urls, templates, static files or any
other functionality. Only database models (including admin-registration) and load/write functions.
These models and load/write functions can then be used in other django applications, together with
the pdftextsplitter engine. <br />
<br />
Installation works like: pip install djangopdftextsplitter <br />
<br />

## List of database models

The database models in this application are:
* textpart (corresponds to the textpart-class from the pdftextsplitter-package)
* fontregion (corresponds to the fonregion-class from the pdftextsplitter-package)
* lineregion (corresponds to the lineregion-class from the pdftextsplitter-package)
* readingline (needed to store certain information, but does not have an equivalent in the pdftextsplitter-package)
* readinghistogram (needed to store certain information, but does not have an equivalent in the pdftextsplitter-package)
* title (corresponds to the title-class from the pdftextsplitter-package)
* body (corresponds to the body-class from the pdftextsplitter-package)
* footer (corresponds to the footer-class from the pdftextsplitter-package)
* headlines (corresponds to the headlines-class from the pdftextsplitter-package)
* headlines_hierarchy (needed to store certain information, but does not have an equivalent in the pdftextsplitter-package)
* enumeration (corresponds to the enumeration-class from the pdftextsplitter-package)
* enumeration_hierarchy (needed to store certain information, but does not have an equivalent in the pdftextsplitter-package)
* textsplitter (corresponds to the textsplitter-class from the pdftextsplitter-package)
* native_toc_element (corresponds to the native_toc_element-class from the pdftextsplitter-package)
* breakdown_decision (needed to store certain information, but does not have an equivalent in the pdftextsplitter-package)
* textalinea (corresponds to the textalinea-class from the pdftextsplitter-package)

## Getting started

Within a django-environment (if the djangotextsplitter is installed in the virtual environment and registered in the django),
one can simpy have access to the model by calling <br />
from djangotextsplitter import textsplitter as db_textsplitter <br />
We recommend using the 'as db_' to distinguish django database models from base classes in the pdftextsplitter-package. <br />
Loading/writing operations can be accessed with: <br />
from djangotextsplitter import load_textsplitter <br />
Each model that has an associated class in pdftextsplitter, has a load-function, a newwrite-function, an overwrite-function and a delete-function. <br />
They can be called as: <br />
from pdftextsplitter import textsplitter <br />
from djangotextsplitter import textsplitter as db_textsplitter <br />
mysplitter = load_textsplitter(31) # 31 is database primary key; in django the pk <br />
db_splitter = newwrite_textsplitter(mysplitter) # No need for a key here, as it is appended to the list <br />
db_splitter = overwrite_textsplitter(31,mysplitter) # 31 is database primary key; in django the pk <br />
delete_textsplitter(31) # 31 is database primary key; in django the pk <br />
<br />
For further details, we refer the user to the documentation of the pdftextsplitter-package, or to the mode details documentation in the docs-folder of this package. <br />
djangotextsplitter is not very complicated. It just provides the database models and load/newwrite/overwrite/delete functions to the pdftextsplitter package, so the pdftextsplitter package can be efficiently used from within a django webapplication.
