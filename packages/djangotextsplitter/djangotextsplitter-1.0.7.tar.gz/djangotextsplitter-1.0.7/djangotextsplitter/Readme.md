# Analyze app

This is a Django application meant to execute and store the results of document analysis into a database.
Django is configured (see settings.py in the main folder) with a postgress SQL database. the goal
of this storage is to save all results calculated by the textsplitter (see TextPart-folder), so that
one can continue the analysis at a later time without having to recalculate everything. this saves
CPU-time and costs for paying ChatGPT.

## Models

The file models.py contains the required database models to save an entire textsplitter-object
(this is the main class that handles a single document analysis) to teh database. It contains
the following models: <br />
<br />

models.py
* textpart
* fontregion
* lineregion
* readingline
* readinghistogram
* title
* body
* footer
* headlines
* headlines_hierarchy
* enumeration
* enumeration_hierarchy
* textsplitter
* native_toc_element
* breakdown_decision
* textalinea

<br />

How these models are connected to each other, is shown in the class inheritance diagram included in this folder.
Both the SQL-relations and the python relations (from TextPart-folder) are shown.

## Database operations

This app contains 4 important files: loads.py, newwrites.py, overwrites.py, deletes.py <br />
<br />

These files contain the functions for database operations of the classes in models.py. The naming convertion
is newwrite_textpart (or overwrite/load/delete; textpart can be any model). The models readingline, readinghistogram,
headlines_hierarchy, enumeration_hierarchy and breakdown_decision do not have such functions of their own,
as they do not have an associated python class in textpart. <br />
<br />

The purpose of these functions is to provide so-called deep-loads, deep-deletes and deep-writes (meaning
that all children of the class are also stored in full detail). they are implemented recursively, meaning
that load_textsplitter utilizes load_title, which utilizes load_textpart, and so on. <br />

<br />
A newwrite is called as db_object = newwrite_textpart(textpart_input) where textpart_input is an instance of the python textpart-class. <br />
An overwrite is called as db_object = newwrite_textpart(id: int, textpart_input) where textpart_input is an instance of the python textpart-class and id is the database id that you want to overwrite <br />
A load is called as textpart_object = load_textpart(id: int) where id is the database id you wish to load and textpart_object is an instance of the python class containing the information from the specific database istance (and all its children). <br />
A delete is called as delete_textpart(id: int) where id is the database id you wish to delete. <br />
<br />

This makes it possible to simply execute and store an instance of the textsplitter as: <br />
mysplitter = textsplitter() <br />
mysplitter.set_documenpath("/path/to/my/document/")
mysplitter.set_outputpath("/path/to/where/you/want/to/save/your/results/") <br />
mysplitter.set_documentname("mydocument")
mysplitter.standard_params() # to set all configurable parameters to their default values <br />
mysplitter.process() # actually execute the analysis <br />
db_object = newwrite_textsplitter(mysplitter) # To store the results to the database <br />
<br />

## Tests

All database operations are unit-tested and integration tested with full code coverage. each unit-test
is designed in such a way that it does not only test the model, but also all of its direct children.
It checks whether the amount of DB-entries is as expected and whether the content is as expected. We test
newwrite-load combination, newwrite-overwrite-load combination, newwrite-newwrite-delete(existent)-delete(nonexistent) combination,
load(non-existent) and overwrite(non-existent). Hence, all possible combinations are covered. For integration
tests, we use some of the Toy-docs (integration tests) from pdftextsplitter.

## Setting up

Install your own postgres SQL server. Then, define the following environmental variables on your system:
MY_PSQL_DBNAME: The name of the database you would like to connect to.
MY_PSQL_USER: The postgres user that should be used for this connection.
MY_PSQL_PASSWORD': The password needed to connect through this user.
MY_PSQL_HOST: The host of the connection (for a local server, the value should equal 'localhost')
MY_PSQL_PORT: The port the connection runs through.
After that, execute migrations and then you can run the database tests. You also have access to a basic django application where the models are registered.

