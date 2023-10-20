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

# import required functionality:
from .newwrites import newwrite_fontregion
from .newwrites import newwrite_lineregion
from .newwrites import newwrite_textpart
from .newwrites import newwrite_title
from .newwrites import newwrite_footer
from .newwrites import newwrite_body
from .newwrites import newwrite_headlines
from .newwrites import newwrite_enumeration
from .newwrites import newwrite_textalinea
from .newwrites import newwrite_Native_TOC_Element
from .newwrites import newwrite_textsplitter
from .deletes import delete_fontregion
from .deletes import delete_lineregion
from .deletes import delete_textpart
from .deletes import delete_title
from .deletes import delete_footer
from .deletes import delete_body
from .deletes import delete_headlines
from .deletes import delete_enumeration
from .deletes import delete_textalinea
from .deletes import delete_Native_TOC_Element
from .deletes import delete_textsplitter

# import textsplitter classes:
from pdftextsplitter import fontregion as textpart_fontregion
from pdftextsplitter import lineregion as textpart_lineregion
from pdftextsplitter import textpart as textpart_textpart
from pdftextsplitter import title as textpart_title
from pdftextsplitter import footer as textpart_footer
from pdftextsplitter import body as textpart_body
from pdftextsplitter import headlines as textpart_headlines
from pdftextsplitter import enumeration as textpart_enumeration
from pdftextsplitter import textalinea as textpart_textalinea
from pdftextsplitter import enum_type as textpart_enum_type
from pdftextsplitter import texttype as textpart_texttype
from pdftextsplitter import textsplitter as textpart_textsplitter
from pdftextsplitter import OpenAI_Keys as textpart_OpenAI_Keys
from pdftextsplitter import Native_TOC_Element as textpart_Native_TOC_Element


# overwrite function for fontregion:
def overwrite_fontregion(db_id: int, textpart_object: textpart_fontregion) -> db_fontregion:
    """
    This function will retrieve a Django-model object and then
    overwrite it with data of the python class of TextPart.
    # parameters: int: database id of the model you want to overwrite
    # parameters: textpart_fontregion: the Textpart-class you want to use for overwriting
    # Returns: db_fontregion: the object just written to the database. It is
    # returned, so you can manipulate entries like foreign key after calling this function.
    """

    # begin by retrieving the database object:
    queryset = db_fontregion.objects.filter(pk=db_id)
    mylist = list(queryset)

    # Check that we actually have an item:
    if len(mylist) > 0:
        # retrieve the object:
        db_object = mylist[0]

        # Transfer the data:
        db_object.left = textpart_object.left
        db_object.right = textpart_object.right
        db_object.value = textpart_object.value
        db_object.frequency = textpart_object.frequency
        db_object.cascadelevel = textpart_object.cascadelevel
        db_object.isregular = textpart_object.isregular

        # Overwrite the foreign key with the default value, as we now
        # put in a separate entity:
        default_key = db_textpart.get_default_foreignkey()
        query_result = db_textpart.objects.filter(pk=default_key)
        query_list = list(query_result)
        db_object.textpart = query_list[0]

        # Save the output:
        db_object.save()

        # Done.
        return db_object

    else:
        # We have to return something, but we will not save it and we clearly mark
        # that is is not a good object:
        db_object = db_fontregion()
        db_object.cascadelevel = -1

        # Generate default foreign key:
        default_key = db_textpart.get_default_foreignkey()
        query_result = db_textpart.objects.filter(pk=default_key)
        query_list = list(query_result)
        db_object.textpart = query_list[0]

        # Return the object:
        return db_object


# overwrite function for lineregion:
def overwrite_lineregion(db_id: int, textpart_object: textpart_lineregion) -> db_lineregion:
    """
    This function will retrieve a Django-model object and then
    overwrite it with data of the python class of TextPart.
    # parameters: int: database id of the model you want to overwrite
    # parameters: textpart_lineregion: the Textpart-class you want to use for overwriting
    # Returns: db_lineregion: the object just written to the database. It is
    # returned, so you can manipulate entries like foreign key after calling this function.
    """

    # begin by retrieving the database object:
    queryset = db_lineregion.objects.filter(pk=db_id)
    mylist = list(queryset)

    # Check that we actually have an item:
    if len(mylist) > 0:
        # retrieve the object:
        db_object = mylist[0]

        # Transfer the data:
        db_object.left = textpart_object.left
        db_object.right = textpart_object.right
        db_object.value = textpart_object.value
        db_object.frequency = textpart_object.frequency
        db_object.isregular = textpart_object.isregular
        db_object.issmall = textpart_object.issmall
        db_object.isbig = textpart_object.isbig
        db_object.iszero = textpart_object.iszero
        db_object.isvalid = textpart_object.isvalid

        # Overwrite the foreign key with the default value, as we now
        # put in a separate entity:
        default_key = db_textpart.get_default_foreignkey()
        query_result = db_textpart.objects.filter(pk=default_key)
        query_list = list(query_result)
        db_object.textpart = query_list[0]

        # Save the output:
        db_object.save()

        # Done.
        return db_object

    else:
        # We have to return something, but we will not save it and we clearly mark
        # that is is not a good object:
        db_object = db_lineregion()
        db_object.frequency = -1.0

        # Generate default foreign key:
        default_key = db_textpart.get_default_foreignkey()
        query_result = db_textpart.objects.filter(pk=default_key)
        query_list = list(query_result)
        db_object.textpart = query_list[0]

        # Return the object:
        return db_object


# overwrite function for textpart:
def overwrite_textpart(db_id: int, textpart_object: textpart_textpart) -> db_textpart:
    """
    This function will retrieve a Django-model object and then
    overwrite it with data of the python class of TextPart.
    # parameters: int: database id of the model you want to overwrite
    # parameters: textpart_textpart: the Textpart-class you want to use for overwriting
    # Returns: db_textpart: the object just written to the database. It is
    # returned, so you can manipulate entries like foreign key after calling this function.
    """

    # begin by retrieving the database object:
    queryset = db_textpart.objects.filter(pk=db_id)
    mylist = list(queryset)

    # Check that we actually have an item:
    if len(mylist) > 0:
        # retrieve the object:
        db_object = mylist[0]

        # Transfer the data:
        db_object.labelname = textpart_object.labelname
        db_object.documentpath = textpart_object.documentpath
        db_object.documentname = textpart_object.documentname
        db_object.outputpath = textpart_object.outputpath
        db_object.histogramsize = textpart_object.histogramsize
        db_object.headerboundary = textpart_object.headerboundary
        db_object.footerboundary = textpart_object.footerboundary
        db_object.ruleverbosity = textpart_object.ruleverbosity
        db_object.verbosetextline = textpart_object.verbosetextline
        db_object.nr_bold_chars = textpart_object.nr_bold_chars
        db_object.nr_total_chars = textpart_object.nr_total_chars
        db_object.boldchars_ratio = textpart_object.boldchars_ratio
        db_object.boldratio_threshold = textpart_object.boldratio_threshold
        db_object.max_vertpos = textpart_object.max_vertpos
        db_object.min_vertpos = textpart_object.min_vertpos

        # Then, save the textpart object:
        db_object.save()

        # Deleting the fontregions requires a recursive approach:
        id_list_fontregion = list(
            db_fontregion.objects.filter(textpart=db_object)
            .values_list("id", flat=True)
            .order_by("id")
        )
        for this_id in id_list_fontregion:
            delete_fontregion(this_id)

        # Then, save the newly-associated fontregions:
        for region in textpart_object.fontregions:
            # Create a new db-object using the data from region:
            db_child = newwrite_fontregion(region)

            # Appoint foreign key:
            db_child.textpart = db_object

            # Now, save the child again, with the foreign key appointed to it:
            db_child.save()

        # Deleting the lineregions requires a recursive approach:
        id_list_lineregion = list(
            db_lineregion.objects.filter(textpart=db_object)
            .values_list("id", flat=True)
            .order_by("id")
        )
        for this_id in id_list_lineregion:
            delete_lineregion(this_id)

        # Next, save the associated lineregions:
        for region in textpart_object.lineregions:
            # Create a new db-object using the data from region:
            db_child = newwrite_lineregion(region)

            # Appoint foreign key:
            db_child.textpart = db_object

            # Now, save the child again, with the foreign key appointed to it:
            db_child.save()

        # Next, delete all readingline objects that point to this textpart-object:
        db_readingline.objects.filter(textpart=db_object).delete()

        # Next, save the associated content per textline:
        Index = 0
        for textline in textpart_object.textcontent:
            # Create a new db-object:
            db_child = db_readingline()

            # Transfer the data manually, as we do not have a seperate newwrite for this databse model.
            # the reason for that is that we do not have an associated python class for it in textpart.
            db_child.textcontent = textline
            if Index < len(textpart_object.pagenumbers):
                db_child.pagenumbers = textpart_object.pagenumbers[Index]
            if Index < len(textpart_object.positioncontent):
                db_child.positioncontent = textpart_object.positioncontent[Index]
            if Index < len(textpart_object.horposcontent):
                db_child.horposcontent = textpart_object.horposcontent[Index]
            if Index < len(textpart_object.whitelinesize):
                db_child.whitelinesize = textpart_object.whitelinesize[Index]
            if Index < len(textpart_object.fontsize_perline):
                db_child.fontsize_perline = textpart_object.fontsize_perline[Index]
            if Index < len(textpart_object.is_italic):
                db_child.is_italic = textpart_object.is_italic[Index]
            if Index < len(textpart_object.is_bold):
                db_child.is_bold = textpart_object.is_bold[Index]
            if Index < len(textpart_object.is_highlighted):
                db_child.is_highlighted = textpart_object.is_highlighted[Index]

            # Appoint foreign key:
            db_child.textpart = db_object

            # Now, save the child as well:
            db_child.save()

            # Update the index:
            Index = Index + 1

        # Next, delete all readinghistogram objects that point to this textpart-object:
        db_readinghistogram.objects.filter(textpart=db_object).delete()

        # Next, save the new histogram content.
        # We also transfer the data manually, as we do not have a seperate newwrite for this databse model.
        # the reason for that is that we do not have an associated python class for it in textpart.
        for k in range(0, textpart_object.histogramsize + 1):
            # Create histogram fontsize per character:
            if len(textpart_object.fontsizeHist_percharacter) == 3:
                if (
                    len(textpart_object.fontsizeHist_percharacter[0])
                    == textpart_object.histogramsize
                ) and (
                    len(textpart_object.fontsizeHist_percharacter[1])
                    == textpart_object.histogramsize + 1
                ):
                    db_histogram_fontsize_character = db_readinghistogram()
                    db_histogram_fontsize_character.Histogram_Name = "Fontsize_Character"
                    if k < textpart_object.histogramsize:
                        db_histogram_fontsize_character.Histogram_content = (
                            textpart_object.fontsizeHist_percharacter[0][k]
                        )
                    else:
                        db_histogram_fontsize_character.Histogram_content = 0.0
                    db_histogram_fontsize_character.Histogram_Boundary = (
                        textpart_object.fontsizeHist_percharacter[1][k]
                    )
                    db_histogram_fontsize_character.textpart = db_object
                    db_histogram_fontsize_character.save()

            # Create histogram fontsize per line:
            if len(textpart_object.fontsizeHist_perline) == 3:
                if (
                    len(textpart_object.fontsizeHist_perline[0]) == textpart_object.histogramsize
                ) and (
                    len(textpart_object.fontsizeHist_perline[1])
                    == textpart_object.histogramsize + 1
                ):
                    db_histogram_fontsize_line = db_readinghistogram()
                    db_histogram_fontsize_line.Histogram_Name = "Fontsize_Textline"
                    if k < textpart_object.histogramsize:
                        db_histogram_fontsize_line.Histogram_content = (
                            textpart_object.fontsizeHist_perline[0][k]
                        )
                    else:
                        db_histogram_fontsize_line.Histogram_content = 0.0
                    db_histogram_fontsize_line.Histogram_Boundary = (
                        textpart_object.fontsizeHist_perline[1][k]
                    )
                    db_histogram_fontsize_line.textpart = db_object
                    db_histogram_fontsize_line.save()

            # Create histogram fontsize per character:
            if len(textpart_object.whitespaceHist_perline) == 3:
                if (
                    len(textpart_object.whitespaceHist_perline[0]) == textpart_object.histogramsize
                ) and (
                    len(textpart_object.whitespaceHist_perline[1])
                    == textpart_object.histogramsize + 1
                ):
                    db_histogram_whiteline = db_readinghistogram()
                    db_histogram_whiteline.Histogram_Name = "Whiteline_Textline"
                    if k < textpart_object.histogramsize:
                        db_histogram_whiteline.Histogram_content = (
                            textpart_object.whitespaceHist_perline[0][k]
                        )
                    else:
                        db_histogram_whiteline.Histogram_content = 0.0
                    db_histogram_whiteline.Histogram_Boundary = (
                        textpart_object.whitespaceHist_perline[1][k]
                    )
                    db_histogram_whiteline.textpart = db_object
                    db_histogram_whiteline.save()

        # Done, so return the object:
        return db_object

    else:
        # We do have to return something:
        db_object = db_textpart
        db_object.labelname = "WRONG_OBJECT overwrite textpart"
        return db_object


# overwrite function for title:
def overwrite_title(db_id: int, textpart_object: textpart_title) -> db_title:
    """
    This function will retrieve a Django-model object and then
    overwrite it with data of the python class of TextPart.
    # parameters: int: database id of the model you want to overwrite
    # parameters: textpart_textpart: the Textpart-class you want to use for overwriting
    # Returns: db_textpart: the object just written to the database. It is
    # returned, so you can manipulate entries like foreign key after calling this function.
    """

    # begin by retrieving the database object:
    queryset = db_title.objects.filter(pk=db_id)
    mylist = list(queryset)

    # Check that we actually have an item:
    if len(mylist) > 0:
        # retrieve the object:
        db_object = mylist[0]

        # Next, retrieve the associated textpart_id:
        textpart_id = db_object.textpart.id

        # Cast our object to a textpart:
        textpart_object.__class__ = textpart_textpart

        # Overwrite the textpart:
        db_textpart_object = overwrite_textpart(textpart_id, textpart_object)

        # Undo the casting:
        textpart_object.__class__ = textpart_title

        # Pass the new db-textpart to the 1-1 relationship:
        db_object.textpart = db_textpart_object

        # Next, transfer additional data from textpart_object to db_object.
        db_object.labelname = textpart_object.labelname

        # Then, save the new title-object:
        db_object.save()

        # return the object:
        return db_object

    else:
        # We have to return something:
        db_object = db_title()
        db_object.labelname = "WRONG_OBJECT overwrite title"

        # Generate default foreign key:
        default_key = db_textpart.get_default_foreignkey()
        query_result = db_textpart.objects.filter(pk=default_key)
        query_list = list(query_result)
        db_object.textpart = query_list[0]

        # Return the object:
        return db_object


# overwrite function for body:
def overwrite_body(db_id: int, textpart_object: textpart_body) -> db_body:
    """
    This function will retrieve a Django-model object and then
    overwrite it with data of the python class of TextPart.
    # parameters: int: database id of the model you want to overwrite
    # parameters: textpart_textpart: the Textpart-class you want to use for overwriting
    # Returns: db_textpart: the object just written to the database. It is
    # returned, so you can manipulate entries like foreign key after calling this function.
    """

    # begin by retrieving the database object:
    queryset = db_body.objects.filter(pk=db_id)
    mylist = list(queryset)

    # Check that we actually have an item:
    if len(mylist) > 0:
        # retrieve the object:
        db_object = mylist[0]

        # Next, retrieve the associated textpart_id:
        textpart_id = db_object.textpart.id

        # Cast our object to a textpart:
        textpart_object.__class__ = textpart_textpart

        # Overwrite the textpart:
        db_textpart_object = overwrite_textpart(textpart_id, textpart_object)

        # Undo the casting:
        textpart_object.__class__ = textpart_body

        # Pass the new db-textpart to the 1-1 relationship:
        db_object.textpart = db_textpart_object

        # Next, transfer additional data from textpart_object to db_object.
        db_object.labelname = textpart_object.labelname

        # Then, save the new body-object:
        db_object.save()

        # return the object:
        return db_object

    else:
        # We have to return something:
        db_object = db_body()
        db_object.labelname = "WRONG_OBJECT overwrite body"

        # Generate default foreign key:
        default_key = db_textpart.get_default_foreignkey()
        query_result = db_textpart.objects.filter(pk=default_key)
        query_list = list(query_result)
        db_object.textpart = query_list[0]

        # Return the object:
        return db_object


# overwrite function for footer:
def overwrite_footer(db_id: int, textpart_object: textpart_footer) -> db_footer:
    """
    This function will retrieve a Django-model object and then
    overwrite it with data of the python class of TextPart.
    # parameters: int: database id of the model you want to overwrite
    # parameters: textpart_textpart: the Textpart-class you want to use for overwriting
    # Returns: db_textpart: the object just written to the database. It is
    # returned, so you can manipulate entries like foreign key after calling this function.
    """

    # begin by retrieving the database object:
    queryset = db_footer.objects.filter(pk=db_id)
    mylist = list(queryset)

    # Check that we actually have an item:
    if len(mylist) > 0:
        # retrieve the object:
        db_object = mylist[0]

        # Next, retrieve the associated textpart_id:
        textpart_id = db_object.textpart.id

        # Cast our object to a textpart:
        textpart_object.__class__ = textpart_textpart

        # Overwrite the textpart:
        db_textpart_object = overwrite_textpart(textpart_id, textpart_object)

        # Undo the casting:
        textpart_object.__class__ = textpart_footer

        # Pass the new db-textpart to the 1-1 relationship:
        db_object.textpart = db_textpart_object

        # Next, transfer additional data from textpart_object to db_object.
        db_object.labelname = textpart_object.labelname

        # Then, save the new footer-object:
        db_object.save()

        # return the object:
        return db_object

    else:
        # We have to return something:
        db_object = db_footer()
        db_object.labelname = "WRONG_OBJECT overwrite footer"

        # Generate default foreign key:
        default_key = db_textpart.get_default_foreignkey()
        query_result = db_textpart.objects.filter(pk=default_key)
        query_list = list(query_result)
        db_object.textpart = query_list[0]

        # Return the object:
        return db_object


# overwrite function for headlines:
def overwrite_headlines(db_id: int, textpart_object: textpart_headlines) -> db_headlines:
    """
    This function will retrieve a Django-model object and then
    overwrite it with data of the python class of TextPart.
    # parameters: int: database id of the model you want to overwrite
    # parameters: textpart_textpart: the Textpart-class you want to use for overwriting
    # Returns: db_textpart: the object just written to the database. It is
    # returned, so you can manipulate entries like foreign key after calling this function.
    """

    # begin by retrieving the database object:
    queryset = db_headlines.objects.filter(pk=db_id)
    mylist = list(queryset)

    # Check that we actually have an item:
    if len(mylist) > 0:
        # retrieve the object:
        db_object = mylist[0]

        # Next, retrieve the associated textpart_id:
        textpart_id = db_object.textpart.id

        # Cast our object to a textpart:
        textpart_object.__class__ = textpart_textpart

        # Overwrite the textpart:
        db_textpart_object = overwrite_textpart(textpart_id, textpart_object)

        # Undo the casting:
        textpart_object.__class__ = textpart_headlines

        # Pass the new db-textpart to the 1-1 relationship:
        db_object.textpart = db_textpart_object

        # Next, transfer additional data from textpart_object to db_object.
        db_object.labelname = textpart_object.labelname

        # Then, save the new headlines-object:
        db_object.save()

        # Next, delete all hierarchy-objects associated to this item:
        db_headlines_hierarchy.objects.filter(headlines=db_object).delete()

        # Next, save the new associated hierarchy:
        Index = 0
        for this_enum in textpart_object.hierarchy:
            # Create a new db-object:
            db_child = db_headlines_hierarchy()

            # Transfer the data manually, as we do not have a seperate newwrite for this database model.
            db_child.enum_field = this_enum.value

            # Appoint foreign key:
            db_child.headlines = db_object

            # Now, save the child as well:
            db_child.save()

            # Update the index:
            Index = Index + 1

        # return the object:
        return db_object

    else:
        # We have to return something:
        db_object = db_headlines()
        db_object.labelname = "WRONG_OBJECT overwrite headlines"

        # Generate default foreign key:
        default_key = db_textpart.get_default_foreignkey()
        query_result = db_textpart.objects.filter(pk=default_key)
        query_list = list(query_result)
        db_object.textpart = query_list[0]

        # Return the object:
        return db_object


# overwrite function for enumeration:
def overwrite_enumeration(db_id: int, textpart_object: textpart_enumeration) -> db_enumeration:
    """
    This function will retrieve a Django-model object and then
    overwrite it with data of the python class of TextPart.
    # parameters: int: database id of the model you want to overwrite
    # parameters: textpart_textpart: the Textpart-class you want to use for overwriting
    # Returns: db_textpart: the object just written to the database. It is
    # returned, so you can manipulate entries like foreign key after calling this function.
    """

    # begin by retrieving the database object:
    queryset = db_enumeration.objects.filter(pk=db_id)
    mylist = list(queryset)

    # Check that we actually have an item:
    if len(mylist) > 0:
        # retrieve the object:
        db_object = mylist[0]

        # Next, retrieve the associated textpart_id:
        textpart_id = db_object.textpart.id

        # Cast our object to a textpart:
        textpart_object.__class__ = textpart_textpart

        # Overwrite the textpart:
        db_textpart_object = overwrite_textpart(textpart_id, textpart_object)

        # Undo the casting:
        textpart_object.__class__ = textpart_enumeration

        # Pass the new db-textpart to the 1-1 relationship:
        db_object.textpart = db_textpart_object

        # Next, transfer additional data from textpart_object to db_object.
        db_object.labelname = textpart_object.labelname
        db_object.last_enumtype_index = textpart_object.last_enumtype_index
        db_object.this_enumtype_index = textpart_object.this_enumtype_index
        db_object.last_textline_bigroman = textpart_object.last_textline_bigroman
        db_object.last_textline_smallroman = textpart_object.last_textline_smallroman
        db_object.last_textline_bigletter = textpart_object.last_textline_bigletter
        db_object.last_textline_smallletter = textpart_object.last_textline_smallletter
        db_object.last_textline_digit = textpart_object.last_textline_digit
        db_object.last_textline_signmark = textpart_object.last_textline_signmark

        # Then, save the new enumeration-object:
        db_object.save()

        # Next, delete all hierarchy-objects associated to this item:
        db_enumeration_hierarchy.objects.filter(enumeration=db_object).delete()

        # Next, save the new associated hierarchy:
        Index = 0
        for this_enum in textpart_object.hierarchy:
            # Create a new db-object:
            db_child = db_enumeration_hierarchy()

            # Transfer the data manually, as we do not have a seperate newwrite for this database model.
            db_child.enum_field = this_enum.value

            # Appoint foreign key:
            db_child.enumeration = db_object

            # Now, save the child as well:
            db_child.save()

            # Update the index:
            Index = Index + 1

        # return the object:
        return db_object

    else:
        # We have to return something:
        db_object = db_enumeration()
        db_object.labelname = "WRONG_OBJECT overwrite enumeration"

        # Generate default foreign key:
        default_key = db_textpart.get_default_foreignkey()
        query_result = db_textpart.objects.filter(pk=default_key)
        query_list = list(query_result)
        db_object.textpart = query_list[0]

        # Return the object:
        return db_object


# overwrite function for textalinea:
def overwrite_textalinea(db_id: int, textpart_object: textpart_textalinea) -> db_textalinea:
    """
    This function will retrieve a Django-model object and then
    overwrite it with data of the python class of TextPart.
    # parameters: int: database id of the model you want to overwrite
    # parameters: textpart_textpart: the Textpart-class you want to use for overwriting
    # Returns: db_textpart: the object just written to the database. It is
    # returned, so you can manipulate entries like foreign key after calling this function.
    """

    # begin by retrieving the database object:
    queryset = db_textalinea.objects.filter(pk=db_id)
    mylist = list(queryset)

    # Check that we actually have an item:
    if len(mylist) > 0:
        # retrieve the object:
        db_object = mylist[0]

        # Next, retrieve the associated textpart_id:
        textpart_id = db_object.textpart.id

        # Cast our object to a textpart:
        textpart_object.__class__ = textpart_textpart

        # Overwrite the textpart:
        db_textpart_object = overwrite_textpart(textpart_id, textpart_object)

        # Undo the casting:
        textpart_object.__class__ = textpart_textalinea

        # Pass the new db-textpart to the 1-1 relationship:
        db_object.textpart = db_textpart_object

        # Next, transfer additional data from textpart_object to db_object.
        db_object.labelname = textpart_object.labelname
        db_object.textlevel = textpart_object.textlevel
        db_object.typelevel = textpart_object.typelevel
        db_object.texttitle = textpart_object.texttitle
        db_object.nativeID = textpart_object.nativeID
        db_object.parentID = textpart_object.parentID
        db_object.horizontal_ordering = textpart_object.horizontal_ordering
        db_object.summary = textpart_object.summary
        db_object.sum_CanbeEmpty = textpart_object.sum_CanbeEmpty
        db_object.alineatype = textpart_object.alineatype.value
        db_object.enumtype = textpart_object.enumtype.value
        db_object.html_visualization = textpart_object.html_visualization
        db_object.summarized_wordcount = textpart_object.summarized_wordcount
        db_object.total_wordcount = textpart_object.total_wordcount
        db_object.nr_decendants = textpart_object.nr_decendants
        db_object.nr_children = textpart_object.nr_children
        db_object.nr_depths = textpart_object.nr_depths
        db_object.nr_pages = textpart_object.nr_pages

        # Now point to the default foreign key:
        default_key = db_textsplitter.get_default_foreignkey()
        query_result = db_textsplitter.objects.filter(pk=default_key)
        query_list = list(query_result)
        db_object.textsplitter = query_list[0]

        # Then, save the new textalinea-object:
        db_object.save()

        # return the object:
        return db_object

    else:
        # We have to return something:
        db_object = db_textalinea()
        db_object.labelname = "WRONG_OBJECT overwrite textalinea"

        # Generate default foreign key:
        default_key = db_textpart.get_default_foreignkey()
        query_result = db_textpart.objects.filter(pk=default_key)
        query_list = list(query_result)
        db_object.textpart = query_list[0]

        # Return the object:
        return db_object


# overwrite function for Native_TOC_Element:
def overwrite_Native_TOC_Element(
    db_id: int, textpart_object: textpart_Native_TOC_Element
) -> db_Native_TOC_Element:
    """
    This function will retrieve a Django-model object and then
    overwrite it with data of the python class of TextPart.
    # parameters: int: database id of the model you want to overwrite
    # parameters: textpart_Native_TOC_Element: the Textpart-class you want to use for overwriting
    # Returns: db_Native_TOC_Element: the object just written to the database. It is
    # returned, so you can manipulate entries like foreign key after calling this function.
    """

    # begin by retrieving the database object:
    queryset = db_Native_TOC_Element.objects.filter(pk=db_id)
    mylist = list(queryset)

    # Check that we actually have an item:
    if len(mylist) > 0:
        # retrieve the object:
        db_object = mylist[0]

        # Transfer the data:
        db_object.cascadelevel = textpart_object.cascadelevel
        db_object.title = textpart_object.title
        db_object.page = textpart_object.page
        db_object.Xpos = textpart_object.Xpos
        db_object.Ypos = textpart_object.Ypos
        db_object.Zpos = textpart_object.Zpos

        # Overwrite the foreign key with the default value, as we now
        # put in a separate entity:
        default_key = db_textsplitter.get_default_foreignkey()
        query_result = db_textsplitter.objects.filter(pk=default_key)
        query_list = list(query_result)
        db_object.textsplitter = query_list[0]

        # Save the output:
        db_object.save()

        # Done.
        return db_object

    else:
        # We have to return something, but we will not save it and we clearly mark
        # that is is not a good object:
        db_object = db_Native_TOC_Element()
        db_object.cascadelevel = -1
        db_object.title = "WRONG_OBJECT load Native_TOC_Element"
        db_object.page = -1
        db_object.Xpos = -1.0
        db_object.Ypos = -1.0
        db_object.Zpos = -1.0

        # Generate default foreign key:
        default_key = db_textsplitter.get_default_foreignkey()
        query_result = db_textsplitter.objects.filter(pk=default_key)
        query_list = list(query_result)
        db_object.textsplitter = query_list[0]

        # Return the object:
        return db_object


# overwrite function for textsplitter:
def overwrite_textsplitter(db_id: int, textpart_object: textpart_textsplitter) -> db_textsplitter:
    """
    This function will retrieve a Django-model object and then
    overwrite it with data of the python class of TextPart.
    # parameters: int: database id of the model you want to overwrite
    # parameters: textpart_textsplitter: the Textpart-class you want to use for overwriting
    # Returns: db_textsplitter: the object just written to the database. It is
    # returned, so you can manipulate entries like foreign key after calling this function.
    """

    # begin by retrieving the database object:
    queryset = db_textsplitter.objects.filter(pk=db_id)
    mylist = list(queryset)

    # Check uniqueness constrain:
    queryset_name = db_textsplitter.objects.filter(documentname=textpart_object.documentname)
    checklist = list(queryset_name)

    # Adapt so we can overwrite an existing element with the same name:
    checklist_uniqueness = False
    if len(checklist) == 0:
        checklist_uniqueness = True
    if len(checklist) == 1:
        if checklist[0].documentname == textpart_object.documentname:
            checklist_uniqueness = True

    # Check that we actually have an item:
    if (len(mylist) > 0) and (checklist_uniqueness == True):
        # retrieve the object:
        db_object = mylist[0]

        # Next, transfer additional data from textpart_object to db_object.
        db_object.labelname = textpart_object.labelname
        db_object.VERSION = textpart_object.VERSION
        db_object.ratelimit_timeunit = textpart_object.ratelimit_timeunit
        db_object.ratelimit_calls = textpart_object.ratelimit_calls
        db_object.ratelimit_tokens = textpart_object.ratelimit_tokens
        db_object.Costs_price = textpart_object.Costs_price
        db_object.Costs_tokenportion = textpart_object.Costs_tokenportion
        db_object.api_rate_starttime = textpart_object.api_rate_starttime
        db_object.api_rate_currenttime = textpart_object.api_rate_currenttime
        db_object.api_rate_currenttokens = textpart_object.api_rate_currenttokens
        db_object.api_rate_currentcalls = textpart_object.api_rate_currentcalls
        db_object.callcounter = textpart_object.callcounter
        db_object.api_totalprice = textpart_object.api_totalprice
        db_object.api_wrongcalls_duetomaxwhile = textpart_object.api_wrongcalls_duetomaxwhile
        db_object.html_visualization = textpart_object.html_visualization
        db_object.MaxSummaryLength = textpart_object.MaxSummaryLength
        db_object.summarization_threshold = textpart_object.summarization_threshold
        db_object.UseDummySummary = textpart_object.UseDummySummary
        db_object.LanguageModel = textpart_object.LanguageModel
        db_object.BackendChoice = textpart_object.BackendChoice
        db_object.LanguageChoice = textpart_object.LanguageChoice
        db_object.LanguageTemperature = textpart_object.LanguageTemperature
        db_object.MaxCallRepeat = textpart_object.MaxCallRepeat
        db_object.doc_metadata_author = textpart_object.doc_metadata_author
        db_object.doc_metadata_creator = textpart_object.doc_metadata_creator
        db_object.doc_metadata_producer = textpart_object.doc_metadata_producer
        db_object.doc_metadata_subject = textpart_object.doc_metadata_subject
        db_object.doc_metadata_title = textpart_object.doc_metadata_title
        db_object.doc_metadata_fullstring = textpart_object.doc_metadata_fullstring

        # NOTE: We do NOT write the security token in the class to the database.
        # Instead, when loading we recollect it from the one storage place.

        # Then, collect the id's from the 1-1 relationships:
        title_id = db_object.title.id
        footer_id = db_object.footer.id
        body_id = db_object.body.id
        headlines_id = db_object.headlines.id
        enumeration_id = db_object.enumeration.id

        # Next, write the 1-1 relationships to the database:
        db_object_title = overwrite_title(title_id, textpart_object.title)
        db_object_footer = overwrite_footer(footer_id, textpart_object.footer)
        db_object_body = overwrite_body(body_id, textpart_object.body)
        db_object_headlines = overwrite_headlines(headlines_id, textpart_object.headlines)
        db_object_enumeration = overwrite_enumeration(enumeration_id, textpart_object.enumeration)

        # And connect them to db_object:
        db_object.title = db_object_title
        db_object.footer = db_object_footer
        db_object.body = db_object_body
        db_object.headlines = db_object_headlines
        db_object.enumeration = db_object_enumeration

        # Next, handle the direct inheritance from textpart:
        textpart_id = db_object.textpart.id
        textpart_object.__class__ = textpart_textpart
        db_textpart_object = overwrite_textpart(textpart_id, textpart_object)
        textpart_object.__class__ = textpart_textsplitter
        db_object.textpart = db_textpart_object

        # Next, write the uniqueness-field to the DB:
        db_object.documentname = textpart_object.documentname

        # Then, save the new textalinea-object:
        db_object.save()

        # Next, delete all breakdown_decisions objects that point to this textpart-object:
        db_breakdown_decisions.objects.filter(textsplitter=db_object).delete()

        # Next, save the associated content per textline:
        for thisline in textpart_object.textclassification:
            # Create a new db-object:
            db_child = db_breakdown_decisions()

            # Transfer the data manually, as we do not have a seperate newwrite for this databse model.
            # the reason for that is that we do not have an associated python class for it in textpart.
            db_child.textline = thisline

            # Appoint foreign key:
            db_child.textsplitter = db_object

            # Now, save the child as well:
            db_child.save()

        # delete all textalinea objects that point to this textsplitter-object.
        # This requires a so-called deep delete:
        id_list_textalinea = list(
            db_textalinea.objects.filter(textsplitter=db_object)
            .values_list("id", flat=True)
            .order_by("id")
        )
        for this_id in id_list_textalinea:
            delete_textalinea(this_id)

        # Then, save the newly-associated textalineas:
        for alinea in textpart_object.textalineas:
            # Create a new db-object using the data from alinea:
            db_child = newwrite_textalinea(alinea)

            # Appoint foreign key:
            db_child.textsplitter = db_object

            # Now, save the child again, with the foreign key appointed to it:
            db_child.save()

        # delete all Native_TOC_Element objects that point to this textsplitter-object.
        # This requires a so-called deep delete:
        id_list_Native_TOC_Element = list(
            db_Native_TOC_Element.objects.filter(textsplitter=db_object)
            .values_list("id", flat=True)
            .order_by("id")
        )
        for this_id in id_list_Native_TOC_Element:
            delete_Native_TOC_Element(this_id)

        # Then, save the newly-associated textalineas:
        for This_TOC_Element in textpart_object.native_TOC:
            # Create a new db-object using the data from alinea:
            db_child = newwrite_Native_TOC_Element(This_TOC_Element)

            # Appoint foreign key:
            db_child.textsplitter = db_object

            # Now, save the child again, with the foreign key appointed to it:
            db_child.save()

        # return the object:
        return db_object

    else:
        # We have to return something:
        db_object = db_textsplitter()
        db_object.labelname = "WRONG_OBJECT overwrite textsplitter"
        db_object.documentname = "WRONG_OBJECT overwrite textsplitter"

        # Return the object:
        return db_object
