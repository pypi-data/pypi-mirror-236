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


# load function for fontregion:
def load_fontregion(db_id: int) -> textpart_fontregion:
    """
    This function will retrieve a Django-model object and then
    convert it to the python class of TextPart.
    # parameters: int: database id of the model you want to retrieve
    # Returns: the Textpart-class you want to have.
    """

    # begin by retrieving the database object:
    queryset = db_fontregion.objects.filter(pk=db_id)
    mylist = list(queryset)

    # Check if we asked for a valid ID:
    if len(mylist) == 0:
        wrong_object = textpart_fontregion()
        wrong_object.left = 0.1
        wrong_object.right = 10.0
        wrong_object.value = 10.0
        wrong_object.frequency = 1.0
        wrong_object.cascadelevel = -1
        wrong_object.isregular = False
        return wrong_object
    else:
        # retrieve the db_object:
        db_object = mylist[0]

        # Create the new object:
        textpart_object = textpart_fontregion()

        # Transfer the data:
        textpart_object.left = db_object.left
        textpart_object.right = db_object.right
        textpart_object.value = db_object.value
        textpart_object.frequency = db_object.frequency
        textpart_object.cascadelevel = db_object.cascadelevel
        textpart_object.isregular = db_object.isregular

        # Return the output:
        return textpart_object


# load function for lineregion:
def load_lineregion(db_id: int) -> textpart_lineregion:
    """
    This function will retrieve a Django-model object and then
    convert it to the python class of TextPart.
    # parameters: int: database id of the model you want to retrieve
    # Returns: the Textpart-class you want to have.
    """

    # begin by retrieving the database object:
    queryset = db_lineregion.objects.filter(pk=db_id)
    mylist = list(queryset)

    # Check if we asked for a valid ID:
    if len(mylist) == 0:
        wrong_object = textpart_lineregion()
        wrong_object.left = 0.001
        wrong_object.right = 10000.0
        wrong_object.value = 10.0
        wrong_object.frequency = -1.0
        wrong_object.isregular = False
        wrong_object.issmall = False
        wrong_object.isbig = False
        wrong_object.iszero = False
        wrong_object.isvalid = False
        return wrong_object
    else:
        # retrieve the db_object:
        db_object = mylist[0]

        # Create the new object:
        textpart_object = textpart_lineregion()

        # Transfer the data:
        textpart_object.left = db_object.left
        textpart_object.right = db_object.right
        textpart_object.value = db_object.value
        textpart_object.frequency = db_object.frequency
        textpart_object.isregular = db_object.isregular
        textpart_object.issmall = db_object.issmall
        textpart_object.isbig = db_object.isbig
        textpart_object.iszero = db_object.iszero
        textpart_object.isvalid = db_object.isvalid

        # Return the output:
        return textpart_object


# load function for textpart:
def load_textpart(db_id: int) -> textpart_textpart:
    """
    This function will retrieve a Django-model object and then
    convert it to the python class of TextPart.
    # parameters: int: database id of the model you want to retrieve
    # Returns: the Textpart-class you want to have.
    """

    # begin by retrieving the database object:
    queryset = db_textpart.objects.filter(pk=db_id)
    mylist = list(queryset)

    # Check if we asked for a valid ID:
    if len(mylist) == 0:
        wrong_object = textpart_textpart()
        wrong_object.labelname = "WRONG_OBJECT load textpart"
        return wrong_object
    else:
        # retrieve the db_object:
        db_object = mylist[0]

        # Create the new object:
        textpart_object = textpart_textpart()

        # Transfer the data:
        textpart_object.labelname = db_object.labelname
        textpart_object.documentpath = db_object.documentpath
        textpart_object.documentname = db_object.documentname
        textpart_object.outputpath = db_object.outputpath
        textpart_object.histogramsize = db_object.histogramsize
        textpart_object.headerboundary = db_object.headerboundary
        textpart_object.footerboundary = db_object.footerboundary
        textpart_object.ruleverbosity = db_object.ruleverbosity
        textpart_object.verbosetextline = db_object.verbosetextline
        textpart_object.nr_bold_chars = db_object.nr_bold_chars
        textpart_object.nr_total_chars = db_object.nr_total_chars
        textpart_object.boldchars_ratio = db_object.boldchars_ratio
        textpart_object.boldratio_threshold = db_object.boldratio_threshold
        textpart_object.max_vertpos = db_object.max_vertpos
        textpart_object.min_vertpos = db_object.min_vertpos

        # Collect foreign-key objects. Using a recursive strategy may be a little
        # ineffective here, but we still do it for consistency. If fontregion
        # would have classes depending on it as well, recursive is needed.
        id_queryset_fontregion = (
            db_fontregion.objects.filter(textpart=db_object)
            .values_list("id", flat=True)
            .order_by("id")
        )
        id_list_fontregion = list(id_queryset_fontregion)
        textpart_object.fontregions.clear()

        # Loop over the id's:
        for this_id in id_list_fontregion:
            # Get the fontregion:
            this_fontregion = load_fontregion(this_id)

            # Test if it is valid:
            if not (this_fontregion.cascadelevel == -1):
                # Add it to the class:
                textpart_object.fontregions.append(this_fontregion)

        # line regions too:
        id_queryset_lineregion = (
            db_lineregion.objects.filter(textpart=db_object)
            .values_list("id", flat=True)
            .order_by("id")
        )
        id_list_lineregion = list(id_queryset_lineregion)
        textpart_object.lineregions.clear()

        # Loop over the id's:
        for this_id in id_list_lineregion:
            # Get the fontregion:
            this_lineregion = load_lineregion(this_id)

            # Test if it is valid:
            if not (this_lineregion.frequency < -0.5):
                # Add it to the class:
                textpart_object.lineregions.append(this_lineregion)

        # Quantities per textline. We do not use a recursive strategy here, as textpart has no subclasses
        # involved here. So we just take the easiest approach:
        textpart_object.textcontent.clear()
        textpart_object.pagenumbers.clear()
        textpart_object.positioncontent.clear()
        textpart_object.horposcontent.clear()
        textpart_object.whitelinesize.clear()
        textpart_object.fontsize_perline.clear()
        textpart_object.is_italic.clear()
        textpart_object.is_bold.clear()
        textpart_object.is_highlighted.clear()

        queryset_readingline = db_readingline.objects.filter(textpart=db_object)
        list_readingline = list(queryset_readingline)

        for thisline in list_readingline:
            textpart_object.textcontent.append(thisline.textcontent)
            textpart_object.pagenumbers.append(thisline.pagenumbers)
            textpart_object.positioncontent.append(thisline.positioncontent)
            textpart_object.horposcontent.append(thisline.horposcontent)
            textpart_object.whitelinesize.append(thisline.whitelinesize)
            textpart_object.fontsize_perline.append(thisline.fontsize_perline)
            textpart_object.is_italic.append(thisline.is_italic)
            textpart_object.is_bold.append(thisline.is_bold)
            textpart_object.is_highlighted.append(thisline.is_highlighted)

        # NOTE: We do not load any information per character:
        textpart_object.fontsize_percharacter.clear()

        # Histograms (also no recursive strategy needed):
        queryset_readinghistogram = db_readinghistogram.objects.filter(textpart=db_object)
        list_readinghistogram = list(queryset_readinghistogram)

        # We need at least length 2 to allow for reasonable histograms:
        if len(list_readinghistogram) > 1:
            # Collect arrays for the histogram
            content_array_perchar = []
            boundary_array_perchar = []
            content_array_perline = []
            boundary_array_perline = []
            content_array_whiteline = []
            boundary_array_whiteline = []

            # loop over the histogram values:
            for onehist in list_readinghistogram:
                # Select first histogram:
                if onehist.Histogram_Name == "Fontsize_Character":
                    content_array_perchar.append(onehist.Histogram_content)
                    boundary_array_perchar.append(onehist.Histogram_Boundary)

                # Select second histogram:
                if onehist.Histogram_Name == "Fontsize_Textline":
                    content_array_perline.append(onehist.Histogram_content)
                    boundary_array_perline.append(onehist.Histogram_Boundary)

                # Select third histogram:
                if onehist.Histogram_Name == "Whiteline_Textline":
                    content_array_whiteline.append(onehist.Histogram_content)
                    boundary_array_whiteline.append(onehist.Histogram_Boundary)

            # Next, pop the last content-item, as those are n values and the boundaries are n+1:
            if len(content_array_perchar) > 1:
                content_array_perchar.pop()
            if len(content_array_perline) > 1:
                content_array_perline.pop()
            if len(content_array_whiteline) > 1:
                content_array_whiteline.pop()

            # Configure histogramsize:
            textpart_object.histogramsize = len(content_array_perchar)

            # Pass on histograms:
            textpart_object.fontsizeHist_percharacter = [
                content_array_perchar,
                boundary_array_perchar,
                boundary_array_perchar,
            ]
            textpart_object.fontsizeHist_perline = [
                content_array_perline,
                boundary_array_perline,
                boundary_array_perline,
            ]
            textpart_object.whitespaceHist_perline = [
                content_array_whiteline,
                boundary_array_whiteline,
                boundary_array_whiteline,
            ]

        else:
            # Then, there will be no histograms:
            textpart_object.fontsizeHist_percharacter.clear()
            textpart_object.fontsizeHist_perline.clear()
            textpart_object.whitespaceHist_perline.clear()

        # Return the output:
        return textpart_object


# load function for title:
def load_title(db_id: int) -> textpart_title:
    """
    This function will retrieve a Django-model object and then
    convert it to the python class of TextPart.
    # parameters: int: database id of the model you want to retrieve
    # Returns: the Textpart-class you want to have.
    """

    # begin by retrieving the database object:
    queryset = db_title.objects.filter(pk=db_id)
    mylist = list(queryset)

    # Check if we asked for a valid ID:
    if len(mylist) == 0:
        wrong_object = textpart_title()
        wrong_object.labelname = "WRONG_OBJECT load title"
        return wrong_object
    else:
        # retrieve the db_object:
        db_object = mylist[0]

        # retrieve the id of the associated textpart-object:
        textpart_id = db_object.textpart.id

        # Create a new title-object:
        textpart_object = textpart_title()

        # Next, load the textpart:
        textpart_object_textpart = load_textpart(textpart_id)

        # Then, add the information from the parent to the child:
        textpart_object.fill_from_other_textpart(textpart_object_textpart)

        # Next, transfer additional data from db_object to textpart_object.
        textpart_object.labelname = db_object.labelname

        # Then, return the object:
        return textpart_object


# load function for body:
def load_body(db_id: int) -> textpart_body:
    """
    This function will retrieve a Django-model object and then
    convert it to the python class of TextPart.
    # parameters: int: database id of the model you want to retrieve
    # Returns: the Textpart-class you want to have.
    """

    # begin by retrieving the database object:
    queryset = db_body.objects.filter(pk=db_id)
    mylist = list(queryset)

    # Check if we asked for a valid ID:
    if len(mylist) == 0:
        wrong_object = textpart_body()
        wrong_object.labelname = "WRONG_OBJECT load body"
        return wrong_object
    else:
        # retrieve the db_object:
        db_object = mylist[0]

        # retrieve the id of the associated textpart-object:
        textpart_id = db_object.textpart.id

        # Create a new body-object:
        textpart_object = textpart_body()

        # Next, load the textpart:
        textpart_object_textpart = load_textpart(textpart_id)

        # Then, add the information from the parent to the child:
        textpart_object.fill_from_other_textpart(textpart_object_textpart)

        # Next, transfer additional data from db_object to textpart_object.
        textpart_object.labelname = db_object.labelname

        # Then, return the object:
        return textpart_object


# load function for footer:
def load_footer(db_id: int) -> textpart_footer:
    """
    This function will retrieve a Django-model object and then
    convert it to the python class of TextPart.
    # parameters: int: database id of the model you want to retrieve
    # Returns: the Textpart-class you want to have.
    """

    # begin by retrieving the database object:
    queryset = db_footer.objects.filter(pk=db_id)
    mylist = list(queryset)

    # Check if we asked for a valid ID:
    if len(mylist) == 0:
        wrong_object = textpart_footer()
        wrong_object.labelname = "WRONG_OBJECT load footer"
        return wrong_object
    else:
        # retrieve the db_object:
        db_object = mylist[0]

        # retrieve the id of the associated textpart-object:
        textpart_id = db_object.textpart.id

        # Create a new footer-object:
        textpart_object = textpart_footer()

        # Next, load the textpart:
        textpart_object_textpart = load_textpart(textpart_id)

        # Then, add the information from the parent to the child:
        textpart_object.fill_from_other_textpart(textpart_object_textpart)

        # Next, transfer additional data from db_object to textpart_object.
        textpart_object.labelname = db_object.labelname

        # Then, return the object:
        return textpart_object


# load function for headlines:
def load_headlines(db_id: int) -> textpart_headlines:
    """
    This function will retrieve a Django-model object and then
    convert it to the python class of TextPart.
    # parameters: int: database id of the model you want to retrieve
    # Returns: the Textpart-class you want to have.
    """

    # begin by retrieving the database object:
    queryset = db_headlines.objects.filter(pk=db_id)
    mylist = list(queryset)

    # Check if we asked for a valid ID:
    if len(mylist) == 0:
        wrong_object = textpart_headlines()
        wrong_object.labelname = "WRONG_OBJECT load headlines"
        return wrong_object
    else:
        # retrieve the db_object:
        db_object = mylist[0]

        # retrieve the id of the associated textpart-object:
        textpart_id = db_object.textpart.id

        # Create a new headlines-object:
        textpart_object = textpart_headlines()

        # Next, load the textpart:
        textpart_object_textpart = load_textpart(textpart_id)

        # Then, add the information from the parent to the child:
        textpart_object.fill_from_other_textpart(textpart_object_textpart)

        # Next, transfer additional data from db_object to textpart_object.
        textpart_object.labelname = db_object.labelname

        # Next, collect the hierarchy:
        queryset_hierarchy = db_headlines_hierarchy.objects.filter(headlines=db_object)
        list_hierarchy = list(queryset_hierarchy)
        textpart_object.hierarchy.clear()

        # Loop over the hierarchy to append:
        for element in list_hierarchy:
            textpart_object.hierarchy.append(textpart_enum_type(element.enum_field))

        # Then, return the object:
        return textpart_object


# load function for enumeration:
def load_enumeration(db_id: int) -> textpart_enumeration:
    """
    This function will retrieve a Django-model object and then
    convert it to the python class of TextPart.
    # parameters: int: database id of the model you want to retrieve
    # Returns: the Textpart-class you want to have.
    """

    # begin by retrieving the database object:
    queryset = db_enumeration.objects.filter(pk=db_id)
    mylist = list(queryset)

    # Check if we asked for a valid ID:
    if len(mylist) == 0:
        wrong_object = textpart_enumeration()
        wrong_object.labelname = "WRONG_OBJECT load enumeration"
        return wrong_object
    else:
        # retrieve the db_object:
        db_object = mylist[0]

        # retrieve the id of the associated textpart-object:
        textpart_id = db_object.textpart.id

        # Create a new enumeration-object:
        textpart_object = textpart_enumeration()

        # Next, load the textpart:
        textpart_object_textpart = load_textpart(textpart_id)

        # Then, add the information from the parent to the child:
        textpart_object.fill_from_other_textpart(textpart_object_textpart)

        # Next, transfer additional data from db_object to textpart_object.
        textpart_object.labelname = db_object.labelname
        textpart_object.last_enumtype_index = db_object.last_enumtype_index
        textpart_object.this_enumtype_index = db_object.this_enumtype_index
        textpart_object.last_textline_bigroman = db_object.last_textline_bigroman
        textpart_object.last_textline_smallroman = db_object.last_textline_smallroman
        textpart_object.last_textline_bigletter = db_object.last_textline_bigletter
        textpart_object.last_textline_smallletter = db_object.last_textline_smallletter
        textpart_object.last_textline_digit = db_object.last_textline_digit
        textpart_object.last_textline_signmark = db_object.last_textline_signmark

        # Next, collect the hierarchy:
        queryset_hierarchy = db_enumeration_hierarchy.objects.filter(enumeration=db_object)
        list_hierarchy = list(queryset_hierarchy)
        textpart_object.hierarchy.clear()

        # Loop over the hierarchy to append:
        for element in list_hierarchy:
            textpart_object.hierarchy.append(textpart_enum_type(element.enum_field))

        # Then, return the object:
        return textpart_object


# load function for textalinea:
def load_textalinea(db_id: int) -> textpart_textalinea:
    """
    This function will retrieve a Django-model object and then
    convert it to the python class of TextPart.
    # parameters: int: database id of the model you want to retrieve
    # Returns: the Textpart-class you want to have.
    """

    # begin by retrieving the database object:
    queryset = db_textalinea.objects.filter(pk=db_id)
    mylist = list(queryset)

    # Check if we asked for a valid ID:
    if len(mylist) == 0:
        wrong_object = textpart_textalinea()
        wrong_object.labelname = "WRONG_OBJECT load textalinea"
        return wrong_object
    else:
        # retrieve the db_object:
        db_object = mylist[0]

        # retrieve the id of the associated textpart-object:
        textpart_id = db_object.textpart.id

        # Create a new textalinea-object:
        textpart_object = textpart_textalinea()

        # Next, load the textpart:
        textpart_object_textpart = load_textpart(textpart_id)

        # Then, add the information from the parent to the child:
        textpart_object.fill_from_other_textpart(textpart_object_textpart)

        # Next, transfer additional data from db_object to textpart_object.
        textpart_object.labelname = db_object.labelname
        textpart_object.textlevel = db_object.textlevel
        textpart_object.typelevel = db_object.typelevel
        textpart_object.texttitle = db_object.texttitle
        textpart_object.nativeID = db_object.nativeID
        textpart_object.parentID = db_object.parentID
        textpart_object.horizontal_ordering = db_object.horizontal_ordering
        textpart_object.summary = db_object.summary
        textpart_object.sum_CanbeEmpty = db_object.sum_CanbeEmpty
        textpart_object.alineatype = textpart_texttype(db_object.alineatype)
        textpart_object.enumtype = textpart_enum_type(db_object.enumtype)
        textpart_object.html_visualization = db_object.html_visualization
        textpart_object.summarized_wordcount = db_object.summarized_wordcount
        textpart_object.total_wordcount = db_object.total_wordcount
        textpart_object.nr_decendants = db_object.nr_decendants
        textpart_object.nr_children = db_object.nr_children
        textpart_object.nr_depths = db_object.nr_depths
        textpart_object.nr_pages = db_object.nr_pages

        # Then, return the object:
        return textpart_object


# load function for Native_TOC_Element:
def load_Native_TOC_Element(db_id: int) -> textpart_Native_TOC_Element:
    """
    This function will retrieve a Django-model object and then
    convert it to the python class of TextPart.
    # parameters: int: database id of the model you want to retrieve
    # Returns: the Textpart-class you want to have.
    """

    # begin by retrieving the database object:
    queryset = db_Native_TOC_Element.objects.filter(pk=db_id)
    mylist = list(queryset)

    # Check if we asked for a valid ID:
    if len(mylist) == 0:
        wrong_object = textpart_Native_TOC_Element()
        wrong_object.cascadelevel = -1
        wrong_object.title = "WRONG_OBJECT load Native_TOC_Element"
        wrong_object.page = -1
        wrong_object.Xpos = -1.0
        wrong_object.Ypos = -1.0
        wrong_object.Zpos = -1.0
        return wrong_object
    else:
        # retrieve the db_object:
        db_object = mylist[0]

        # Create the new object:
        textpart_object = textpart_Native_TOC_Element()

        # Transfer the data:
        textpart_object.cascadelevel = db_object.cascadelevel
        textpart_object.title = db_object.title
        textpart_object.page = db_object.page
        textpart_object.Xpos = db_object.Xpos
        textpart_object.Ypos = db_object.Ypos
        textpart_object.Zpos = db_object.Zpos

        # Return the output:
        return textpart_object


# load function for textalinea:
def load_textsplitter(db_id: int) -> textpart_textsplitter:
    """
    This function will retrieve a Django-model object and then
    convert it to the python class of TextPart.
    # parameters: int: database id of the model you want to retrieve
    # Returns: the Textpart-class you want to have.
    """

    # begin by retrieving the database object:
    queryset = db_textsplitter.objects.filter(pk=db_id)
    mylist = list(queryset)

    # Check if we asked for a valid ID:
    if len(mylist) == 0:
        wrong_object = textpart_textsplitter()
        wrong_object.labelname = "WRONG_OBJECT load textsplitter"
        return wrong_object
    else:
        # retrieve the db_object:
        db_object = mylist[0]

        # retrieve the id of the associated 1-1 objects:
        textpart_id = db_object.textpart.id
        title_id = db_object.title.id
        footer_id = db_object.footer.id
        body_id = db_object.body.id
        headlines_id = db_object.headlines.id
        enumeration_id = db_object.enumeration.id

        # Create a new textsplitter-object:
        textpart_object = textpart_textsplitter()

        # Next, load the associated 1-1 objects:
        textpart_object.title = load_title(title_id)
        textpart_object.footer = load_footer(footer_id)
        textpart_object.body = load_body(body_id)
        textpart_object.headlines = load_headlines(headlines_id)
        textpart_object.enumeration = load_enumeration(enumeration_id)

        # Then, add the information from the parent to the child:
        textpart_object_textpart = load_textpart(textpart_id)
        textpart_object.fill_from_other_textpart(textpart_object_textpart)

        # Next, transfer additional data from db_object to textpart_object.
        textpart_object.labelname = db_object.labelname
        textpart_object.VERSION = db_object.VERSION
        textpart_object.ratelimit_timeunit = db_object.ratelimit_timeunit
        textpart_object.ratelimit_calls = db_object.ratelimit_calls
        textpart_object.ratelimit_tokens = db_object.ratelimit_tokens
        textpart_object.Costs_price = db_object.Costs_price
        textpart_object.Costs_tokenportion = db_object.Costs_tokenportion
        textpart_object.api_rate_starttime = db_object.api_rate_starttime
        textpart_object.api_rate_currenttime = db_object.api_rate_currenttime
        textpart_object.api_rate_currenttokens = db_object.api_rate_currenttokens
        textpart_object.api_rate_currentcalls = db_object.api_rate_currentcalls
        textpart_object.callcounter = db_object.callcounter
        textpart_object.api_totalprice = db_object.api_totalprice
        textpart_object.api_wrongcalls_duetomaxwhile = db_object.api_wrongcalls_duetomaxwhile
        textpart_object.html_visualization = db_object.html_visualization
        textpart_object.MaxSummaryLength = db_object.MaxSummaryLength
        textpart_object.summarization_threshold = db_object.summarization_threshold
        textpart_object.UseDummySummary = db_object.UseDummySummary
        textpart_object.LanguageModel = db_object.LanguageModel
        textpart_object.BackendChoice = db_object.BackendChoice
        textpart_object.LanguageChoice = db_object.LanguageChoice
        textpart_object.LanguageTemperature = db_object.LanguageTemperature
        textpart_object.MaxCallRepeat = db_object.MaxCallRepeat
        textpart_object.doc_metadata_author = db_object.doc_metadata_author
        textpart_object.doc_metadata_creator = db_object.doc_metadata_creator
        textpart_object.doc_metadata_producer = db_object.doc_metadata_producer
        textpart_object.doc_metadata_subject = db_object.doc_metadata_subject
        textpart_object.doc_metadata_title = db_object.doc_metadata_title
        textpart_object.doc_metadata_fullstring = db_object.doc_metadata_fullstring

        # Add security token:
        textpart_object.thekeys = textpart_OpenAI_Keys()
        textpart_object.ChatGPT_Key = textpart_object.thekeys.standard_key

        # Add the unique documentname field:
        textpart_object.documentname = db_object.documentname

        # Decisions per textline:
        textpart_object.textclassification.clear()
        queryset_textclassification = db_breakdown_decisions.objects.filter(textsplitter=db_object)
        list_textclassification = list(queryset_textclassification)

        for thisline in list_textclassification:
            textpart_object.textclassification.append(thisline.textline)

        # Add the textalinea-parts:
        id_queryset_textalinea = (
            db_textalinea.objects.filter(textsplitter=db_object)
            .values_list("id", flat=True)
            .order_by("id")
        )
        id_list_textalinea = list(id_queryset_textalinea)
        textpart_object.textalineas.clear()

        # Loop over the id's:
        for this_id in id_list_textalinea:
            # Get the textalinea:
            this_alinea = load_textalinea(this_id)

            # Test if it is valid:
            if not ("WRONG_OBJECT" in this_alinea.labelname):
                # Add it to the class:
                textpart_object.textalineas.append(this_alinea)

        # Add the Native_TOC_Element-parts:
        id_queryset_Native_TOC_Element = (
            db_Native_TOC_Element.objects.filter(textsplitter=db_object)
            .values_list("id", flat=True)
            .order_by("id")
        )
        id_list_Native_TOC_Element = list(id_queryset_Native_TOC_Element)
        textpart_object.native_TOC.clear()

        # Loop over the id's:
        for this_id in id_list_Native_TOC_Element:
            # Get the Native_TOC_Element:
            this_TOC_Element = load_Native_TOC_Element(this_id)

            # Test if it is valid:
            if not ("WRONG_OBJECT" in this_TOC_Element.title):
                # Add it to the class:
                textpart_object.native_TOC.append(this_TOC_Element)

        # Then, return the object:
        return textpart_object
