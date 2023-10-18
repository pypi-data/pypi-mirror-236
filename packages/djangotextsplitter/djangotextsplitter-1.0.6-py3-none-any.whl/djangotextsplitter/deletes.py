# import Django models:
from .models import get_default_user
from .models import fontregion as db_fontregion
from .models import lineregion as db_lineregion
from .models import readingline as db_readingline
from .models import readinghistogram as db_readinghistogram
from .models import textpart as db_textpart
from .models import title as db_title
from .models import body as db_body
from .models import footer as db_footer
from .models import headlines as db_headlines
from .models import headlines_hierarchy as db_headlines_hierarchy
from .models import enumeration as db_enumeration
from .models import enumeration_hierarchy as db_enumeration_hierarchy
from .models import textalinea as db_textalinea
from .models import textsplitter as db_textsplitter
from .models import Native_TOC_Element as db_Native_TOC_Element
from .models import breakdown_decisions as db_breakdown_decisions

# import required Django functionality:
from django.contrib.auth.models import User


# delete function for fontregion:
def delete_fontregion(db_id: int):
    """
    This function will delete a Django-model object from the database.
    # parameters: int: database id of the model you want to delete.
    # Returns: None.
    """

    # As fontregion does not have any dependencies, this is easy:
    db_fontregion.objects.filter(pk=db_id).delete()


# delete function for fontregion:
def delete_lineregion(db_id: int):
    """
    This function will delete a Django-model object from the database.
    # parameters: int: database id of the model you want to delete.
    # Returns: None.
    """

    # As fontregion does not have any dependencies, this is easy:
    db_lineregion.objects.filter(pk=db_id).delete()


# delete function for textpart:
def delete_textpart(db_id: int):
    """
    This function will delete a Django-model object from the database.
    # parameters: int: database id of the model you want to delete.
    # Returns: None.
    """

    # Collect the db_object that belongs to db_id:
    queryset = db_textpart.objects.filter(pk=db_id)
    mylist = list(queryset)

    # Check that we actually have an item:
    if len(mylist) > 0:
        # Collect the item:
        db_object = mylist[0]

        # Deleting the fontregions requires a recursive approach:
        id_list_fontregion = list(
            db_fontregion.objects.filter(textpart=db_object)
            .values_list("id", flat=True)
            .order_by("id")
        )
        for this_id in id_list_fontregion:
            delete_fontregion(this_id)

        # Deleting the lineregions requires a recursive approach:
        id_list_lineregion = list(
            db_lineregion.objects.filter(textpart=db_object)
            .values_list("id", flat=True)
            .order_by("id")
        )
        for this_id in id_list_lineregion:
            delete_lineregion(this_id)

        # Next, we delete the readinglines:
        db_readingline.objects.filter(textpart=db_object).delete()

        # And the histograms:
        db_readinghistogram.objects.filter(textpart=db_object).delete()

    # Next, delete the actual textpart:
    db_textpart.objects.filter(pk=db_id).delete()


# delete function for title:
def delete_title(db_id: int):
    """
    This function will delete a Django-model object from the database.
    # parameters: int: database id of the model you want to delete.
    # Returns: None.
    """

    # Collect the db_object that belongs to db_id:
    queryset = db_title.objects.filter(pk=db_id)
    mylist = list(queryset)

    # Check that we actually have an item:
    if len(mylist) > 0:
        # Collect the item:
        db_object = mylist[0]

        # Now, first delete the textpart-object that belongs to this one:
        delete_textpart(db_object.textpart.id)

    # then, we can delete the title-object itself:
    db_title.objects.filter(pk=db_id).delete()


# delete function for body:
def delete_body(db_id: int):
    """
    This function will delete a Django-model object from the database.
    # parameters: int: database id of the model you want to delete.
    # Returns: None.
    """

    # Collect the db_object that belongs to db_id:
    queryset = db_body.objects.filter(pk=db_id)
    mylist = list(queryset)

    # Check that we actually have an item:
    if len(mylist) > 0:
        # Collect the item:
        db_object = mylist[0]

        # Now, first delete the textpart-object that belongs to this one:
        delete_textpart(db_object.textpart.id)

    # then, we can delete the body-object itself:
    db_body.objects.filter(pk=db_id).delete()


# delete function for footer:
def delete_footer(db_id: int):
    """
    This function will delete a Django-model object from the database.
    # parameters: int: database id of the model you want to delete.
    # Returns: None.
    """

    # Collect the db_object that belongs to db_id:
    queryset = db_footer.objects.filter(pk=db_id)
    mylist = list(queryset)

    # Check that we actually have an item:
    if len(mylist) > 0:
        # Collect the item:
        db_object = mylist[0]

        # Now, first delete the textpart-object that belongs to this one:
        delete_textpart(db_object.textpart.id)

    # then, we can delete the footer-object itself:
    db_footer.objects.filter(pk=db_id).delete()


# delete function for headlines:
def delete_headlines(db_id: int):
    """
    This function will delete a Django-model object from the database.
    # parameters: int: database id of the model you want to delete.
    # Returns: None.
    """

    # Collect the db_object that belongs to db_id:
    queryset = db_headlines.objects.filter(pk=db_id)
    mylist = list(queryset)

    # Check that we actually have an item:
    if len(mylist) > 0:
        # Collect the item:
        db_object = mylist[0]

        # Now, first delete the textpart-object that belongs to this one:
        delete_textpart(db_object.textpart.id)

        # Also, delete the hierarchy that belongs to this one:
        db_headlines_hierarchy.objects.filter(headlines=db_object).delete()

    # then, we can delete the headlines-object itself:
    db_headlines.objects.filter(pk=db_id).delete()


# delete function for enumeration:
def delete_enumeration(db_id: int):
    """
    This function will delete a Django-model object from the database.
    # parameters: int: database id of the model you want to delete.
    # Returns: None.
    """

    # Collect the db_object that belongs to db_id:
    queryset = db_enumeration.objects.filter(pk=db_id)
    mylist = list(queryset)

    # Check that we actually have an item:
    if len(mylist) > 0:
        # Collect the item:
        db_object = mylist[0]

        # Now, first delete the textpart-object that belongs to this one:
        delete_textpart(db_object.textpart.id)

        # Also, delete the hierarchy that belongs to this one:
        db_enumeration_hierarchy.objects.filter(enumeration=db_object).delete()

    # then, we can delete the enumeration-object itself:
    db_enumeration.objects.filter(pk=db_id).delete()


# delete function for textalinea:
def delete_textalinea(db_id: int):
    """
    This function will delete a Django-model object from the database.
    # parameters: int: database id of the model you want to delete.
    # Returns: None.
    """

    # Collect the db_object that belongs to db_id:
    queryset = db_textalinea.objects.filter(pk=db_id)
    mylist = list(queryset)

    # Check that we actually have an item:
    if len(mylist) > 0:
        # Collect the item:
        db_object = mylist[0]

        # Now, first delete the textpart-object that belongs to this one:
        delete_textpart(db_object.textpart.id)

    # then, we can delete the textalinea-object itself:
    db_textalinea.objects.filter(pk=db_id).delete()


# delete function for Native_TOC_Element:
def delete_Native_TOC_Element(db_id: int):
    """
    This function will delete a Django-model object from the database.
    # parameters: int: database id of the model you want to delete.
    # Returns: None.
    """

    # As fontregion does not have any dependencies, this is easy:
    db_Native_TOC_Element.objects.filter(pk=db_id).delete()


# delete function for textsplitter:
def delete_textsplitter(db_id: int):
    """
    This function will delete a Django-model object from the database.
    # parameters: int: database id of the model you want to delete.
    # Returns: None.
    """

    # Collect the db_object that belongs to db_id:
    queryset = db_textsplitter.objects.filter(pk=db_id)
    mylist = list(queryset)

    # Check that we actually have an item:
    if len(mylist) > 0:
        # Collect the item:
        db_object = mylist[0]

        # Deleting the textalineas requires a recursive approach.
        # NOTE: This needs to be done before deleting the rest, otherwise; somehow the links are lost.
        id_list_textalinea = list(
            db_textalinea.objects.filter(textsplitter=db_object)
            .values_list("id", flat=True)
            .order_by("id")
        )
        for this_id in id_list_textalinea:
            delete_textalinea(this_id)

        # Deleting the Native_TOC_Elements requires a recursive approach.
        # This should also be done at this point, before we loose links:
        id_list_Native_TOC_Element = list(
            db_Native_TOC_Element.objects.filter(textsplitter=db_object)
            .values_list("id", flat=True)
            .order_by("id")
        )
        for this_id in id_list_Native_TOC_Element:
            delete_Native_TOC_Element(this_id)

        # Next, we execute this one at the correct points:
        db_breakdown_decisions.objects.filter(textsplitter=db_object).delete()

        # Now, first delete the textpart-object that belongs to this one:
        delete_textpart(db_object.textpart.id)

        # then, delete the 1-1 relations:
        delete_title(db_object.title.id)
        delete_footer(db_object.footer.id)
        delete_body(db_object.body.id)
        delete_headlines(db_object.headlines.id)
        delete_enumeration(db_object.enumeration.id)

    # then, we can delete the textsplitter-object itself:
    db_textsplitter.objects.filter(pk=db_id).delete()
