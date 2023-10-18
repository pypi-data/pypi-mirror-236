# Import required functionality:
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import models
# Import required parts from pdftextsplitter package:
from pdftextsplitter import enum_type

# Define a default function to generate a user:
def get_default_user() -> User:
    """
    This function generates a user object in the DB
    so that it can be used for passing a default foreign key.
    # parameters: None, #Return: That user-object...
    """

    # First, query whether we already have this user:
    query_result = User.objects.filter(email="dataloket@minienw.nl")
    query_list = list(query_result)

    # Check if it exists:
    if len(query_list) == 0:
        # Then, create a new user:
        user = User.objects.create_user(
            username="datalake", email="dataloket@minienw.nl", password="nicelake"
        )
        # Ande save it:
        user.save()
        return user

    else:
        # Then, we can return this object:
        return query_list[0]

# Database model for textpart:
class textpart(models.Model):
    """
    Equivalent of the textpart-class in the engine.
    """

    # primary Key field:
    # id = models.IntegerField(unique=True, primary_key=True)

    # Normal model fields:
    labelname = models.TextField(default="Textpart")
    documentpath = models.TextField(default="./")
    documentname = models.TextField(default="")
    outputpath = models.TextField(default="./")
    histogramsize = models.IntegerField(default=100)
    headerboundary = models.FloatField(default=1000.0)
    footerboundary = models.FloatField(default=55.0)
    ruleverbosity = models.IntegerField(default=0)
    verbosetextline = models.TextField(default="")
    nr_bold_chars = models.IntegerField(default=0)
    nr_total_chars = models.IntegerField(default=0)
    boldchars_ratio = models.FloatField(default=0.0)
    boldratio_threshold = models.FloatField(default=0.05)
    max_vertpos = models.FloatField(default=0.0)
    min_vertpos = models.FloatField(default=0.0)

    # NOTE: fontregions, lineregions, arrays per textline & histograms:
    # taken care of by passing a foreign key from fontregion to textpart.

    # method for generating a default foreign key in case someone tries to create a fontregion object (or
    # someone else) without creating the appropriate textpart first:
    @staticmethod
    def get_default_foreignkey() -> int:
        """
        This function generates a textpart object in the DB
        so that it can be used for passing a default foreign key.
        # parameters: None, #Return: That foreign key.
        """

        # Attempt to find an object with -1 cascade level:
        query_result = textpart.objects.filter(labelname="default_foreign_key_object")
        query_list = list(query_result)

        # Make our key:
        if len(query_list) == 0:
            # We have to create an object:
            new_object = textpart()
            new_object.labelname = "default_foreign_key_object"
            new_object.save()
            return new_object.id
        else:
            # We can return this object:
            return query_list[0].id

    # Method for printing the instance:
    def __str__(self):
        return str(self.labelname) + " " + str(self.documentname)

    # Metadata definition:
    class Meta:
        app_label = "djangotextsplitter"


# Database model for fontregion:
class fontregion(models.Model):
    """
    Equivalent of the fontregion-class in the engine.
    """

    # Normal model fields:
    left = models.FloatField(default=0.001)
    right = models.FloatField(default=10000.0)
    value = models.FloatField(default=10.0)
    frequency = models.FloatField(default=1.0)
    cascadelevel = models.IntegerField(default=-1)
    isregular = models.BooleanField(default=False)

    # ManytoOne relationship: many fontregions correspond to a single textpart:
    textpart = models.ForeignKey(textpart, on_delete=models.CASCADE)

    # Method for printing the instance:
    def __str__(self):
        return "L=" + str(self.left) + " V=" + str(self.value) + " R=" + str(self.right)

    # Metadata definition:
    class Meta:
        app_label = "djangotextsplitter"


# Database model for lineregion:
class lineregion(models.Model):
    """
    Equivalent of the line-class in the engine.
    """

    # Normal model fields:
    left = models.FloatField(default=0.0)
    right = models.FloatField(default=0.0)
    value = models.FloatField(default=0.0)
    frequency = models.FloatField(default=0.0)
    isregular = models.BooleanField(default=False)
    issmall = models.BooleanField(default=False)
    isbig = models.BooleanField(default=False)
    iszero = models.BooleanField(default=False)
    isvalid = models.BooleanField(default=False)

    # ManytoOne relationship: many lineregions correspond to a single textpart:
    textpart = models.ForeignKey(textpart, on_delete=models.CASCADE)

    # Method for printing the instance:
    def __str__(self):
        return "L=" + str(self.left) + " V=" + str(self.value) + " R=" + str(self.right)

    # Metadata definition:
    class Meta:
        app_label = "djangotextsplitter"


# Database model for readingline:
class readingline(models.Model):
    """
    Use to store the arrays-per textline of the textpart-class in the engine.
    """

    # Normal model fields:
    textcontent = models.TextField(default="")
    pagenumbers = models.IntegerField(default=0)
    positioncontent = models.FloatField(default=0.0)
    horposcontent = models.FloatField(default=0.0)
    whitelinesize = models.FloatField(default=0.0)
    fontsize_perline = models.FloatField(default=0.0)
    is_italic = models.BooleanField(default=False)
    is_bold = models.BooleanField(default=False)
    is_highlighted = models.BooleanField(default=False)
    # NOTE: We do NOT store fontsize_percharacter; only the histogram. It would be a waste of memory...

    # ManytoOne relationship: many readinglines correspond to a single textpart (one for each line in the document):
    textpart = models.ForeignKey(textpart, on_delete=models.CASCADE)

    # Method for printing the instance:
    def __str__(self):
        return str(self.textcontent)

    # Metadata definition:
    class Meta:
        app_label = "djangotextsplitter"


# Database model for readinghistogram:
class readinghistogram(models.Model):
    """
    Used to store the histogram-objects of the textpart-class.
    """

    # Normal model fields:
    Histogram_Name = models.TextField(default="")
    Histogram_content = models.FloatField(default=0.0)
    Histogram_Boundary = models.FloatField(default=0.0)

    # ManytoOne relationship: many readinghistograms correspond to a single textpart (histogramsize+1) elements for each histogram.
    textpart = models.ForeignKey(textpart, on_delete=models.CASCADE)

    # Method for printing the instance:
    def __str__(self):
        return (
            str(self.Histogram_Name)
            + " "
            + str(self.Histogram_content)
            + " "
            + str(self.Histogram_Boundary)
        )

    # Metadata definition:
    class Meta:
        app_label = "djangotextsplitter"


# Database model for title:
class title(models.Model):
    """
    Equivalent of the title-class in the engine.
    """

    # Normal model fields:
    labelname = models.TextField(default="Title")

    # OnetoOne relationship: a title-object needs an associated textpart (that also needs to be deleted, when this one is deleted):
    textpart = models.OneToOneField(textpart, on_delete=models.CASCADE)

    # Method for printing the instance:
    def __str__(self):
        return str(self.textpart.labelname) + " " + str(self.textpart.documentname)

    # Metadata definition:
    class Meta:
        app_label = "djangotextsplitter"

    # Method for generating a default foreign key in case someone tries to create an object pointing here
    # without creating the appropriate textpart first:
    @staticmethod
    def get_default_foreignkey() -> int:
        """
        This function generates an title object in the DB
        so that it can be used for passing a default foreign key.
        # parameters: None, #Return: That foreign key.
        """

        # Attempt to find an object with -1 cascade level:
        query_result = title.objects.filter(labelname="default_foreign_key_object")
        query_list = list(query_result)

        # Make our key:
        if len(query_list) == 0:
            # We have to create an object:
            new_object = title()
            new_object.labelname = "default_foreign_key_object"

            # Now point to the default foreign key of textpart:
            textpart_default_key = textpart.get_default_foreignkey()
            textpart_query_result = textpart.objects.filter(pk=textpart_default_key)
            textpart_query_list = list(textpart_query_result)
            new_object.textpart = textpart_query_list[0]

            # Now, save:
            new_object.save()
            return new_object.id
        else:
            # We can return this object:
            return query_list[0].id


# Database model for footer:
class footer(models.Model):
    """
    Equivalent of the footer-class in the engine.
    """

    # Normal model fields:
    labelname = models.TextField(default="Footer")

    # OnetoOne relationship: a footer-object needs an associated textpart (that also needs to be deleted, when this one is deleted):
    textpart = models.OneToOneField(textpart, on_delete=models.CASCADE)

    # Method for printing the instance:
    def __str__(self):
        return str(self.textpart.labelname) + " " + str(self.textpart.documentname)

    # Metadata definition:
    class Meta:
        app_label = "djangotextsplitter"

    # Method for generating a default foreign key in case someone tries to create an object pointing here
    # without creating the appropriate textpart first:
    @staticmethod
    def get_default_foreignkey() -> int:
        """
        This function generates an footer object in the DB
        so that it can be used for passing a default foreign key.
        # parameters: None, #Return: That foreign key.
        """

        # Attempt to find an object with -1 cascade level:
        query_result = footer.objects.filter(labelname="default_foreign_key_object")
        query_list = list(query_result)

        # Make our key:
        if len(query_list) == 0:
            # We have to create an object:
            new_object = footer()
            new_object.labelname = "default_foreign_key_object"

            # Now point to the default foreign key of textpart:
            textpart_default_key = textpart.get_default_foreignkey()
            textpart_query_result = textpart.objects.filter(pk=textpart_default_key)
            textpart_query_list = list(textpart_query_result)
            new_object.textpart = textpart_query_list[0]

            # Now, save:
            new_object.save()
            return new_object.id
        else:
            # We can return this object:
            return query_list[0].id


# Database model for body:
class body(models.Model):
    """
    Equivalent of the body-class in the engine.
    """

    # Normal model fields:
    labelname = models.TextField(default="Body")

    # OnetoOne relationship: a body-object needs an associated textpart (that also needs to be deleted, when this one is deleted):
    textpart = models.OneToOneField(textpart, on_delete=models.CASCADE)

    # Method for printing the instance:
    def __str__(self):
        return str(self.textpart.labelname) + " " + str(self.textpart.documentname)

    # Metadata definition:
    class Meta:
        app_label = "djangotextsplitter"

    # Method for generating a default foreign key in case someone tries to create an object pointing here
    # without creating the appropriate textpart first:
    @staticmethod
    def get_default_foreignkey() -> int:
        """
        This function generates an body object in the DB
        so that it can be used for passing a default foreign key.
        # parameters: None, #Return: That foreign key.
        """

        # Attempt to find an object with -1 cascade level:
        query_result = body.objects.filter(labelname="default_foreign_key_object")
        query_list = list(query_result)

        # Make our key:
        if len(query_list) == 0:
            # We have to create an object:
            new_object = body()
            new_object.labelname = "default_foreign_key_object"

            # Now point to the default foreign key of textpart:
            textpart_default_key = textpart.get_default_foreignkey()
            textpart_query_result = textpart.objects.filter(pk=textpart_default_key)
            textpart_query_list = list(textpart_query_result)
            new_object.textpart = textpart_query_list[0]

            # Now, save:
            new_object.save()
            return new_object.id
        else:
            # We can return this object:
            return query_list[0].id


# Database model for headlines:
class headlines(models.Model):
    """
    Equivalent of the headlines-class in the engine.
    """

    # Normal model fields:
    labelname = models.TextField(default="Headlines")

    # OnetoOne relationship: a headlines-object needs an associated textpart (that also needs to be deleted, when this one is deleted):
    textpart = models.OneToOneField(textpart, on_delete=models.CASCADE)

    # Method for printing the instance:
    def __str__(self):
        return str(self.labelname) + " " + str(self.textpart.documentname)

    # Metadata definition:
    class Meta:
        app_label = "djangotextsplitter"

    # Method for generating a default foreign key in case someone tries to create an object pointing here
    # without creating the appropriate textpart first:
    @staticmethod
    def get_default_foreignkey() -> int:
        """
        This function generates a headlines object in the DB
        so that it can be used for passing a default foreign key.
        # parameters: None, #Return: That foreign key.
        """

        # Attempt to find an object with -1 cascade level:
        query_result = headlines.objects.filter(labelname="default_foreign_key_object")
        query_list = list(query_result)

        # Make our key:
        if len(query_list) == 0:
            # We have to create an object:
            new_object = headlines()
            new_object.labelname = "default_foreign_key_object"

            # Now point to the default foreign key of textpart:
            textpart_default_key = textpart.get_default_foreignkey()
            textpart_query_result = textpart.objects.filter(pk=textpart_default_key)
            textpart_query_list = list(textpart_query_result)
            new_object.textpart = textpart_query_list[0]

            # Now, save:
            new_object.save()
            return new_object.id
        else:
            # We can return this object:
            return query_list[0].id


# Database model for headlines-hierarchy:
class headlines_hierarchy(models.Model):
    """
    Equivalent of the hierarchy under headlines in the engine.
    """

    # Normal model fields:
    enum_field = models.IntegerField(default=0)

    # ManytoOne relationship: many headlines_hierarchy correspond to a single headlines:
    headlines = models.ForeignKey(headlines, on_delete=models.CASCADE)

    # Method for printing the instance:
    def __str__(self):
        return str(enum_type(self.enum_field))

    # Metadata definition:
    class Meta:
        app_label = "djangotextsplitter"


# Database model for enumeration:
class enumeration(models.Model):
    """
    Equivalent of the enumeration-class in the engine.
    """

    # Normal model fields:
    labelname = models.TextField(default="Enumeration")
    last_enumtype_index = models.IntegerField(default=0)
    this_enumtype_index = models.IntegerField(default=0)
    last_textline_bigroman = models.TextField(default="")
    last_textline_smallroman = models.TextField(default="")
    last_textline_bigletter = models.TextField(default="")
    last_textline_smallletter = models.TextField(default="")
    last_textline_digit = models.TextField(default="")
    last_textline_signmark = models.TextField(default="")

    # OnetoOne relationship: a enumeration-object needs an associated textpart (that also needs to be deleted, when this one is deleted):
    textpart = models.OneToOneField(textpart, on_delete=models.CASCADE)

    # Method for printing the instance:
    def __str__(self):
        return str(self.labelname) + " " + str(self.textpart.documentname)

    # Metadata definition:
    class Meta:
        app_label = "djangotextsplitter"

    # Method for generating a default foreign key in case someone tries to create an object pointing here
    # without creating the appropriate textpart first:
    @staticmethod
    def get_default_foreignkey() -> int:
        """
        This function generates an enumeration object in the DB
        so that it can be used for passing a default foreign key.
        # parameters: None, #Return: That foreign key.
        """

        # Attempt to find an object with -1 cascade level:
        query_result = enumeration.objects.filter(labelname="default_foreign_key_object")
        query_list = list(query_result)

        # Make our key:
        if len(query_list) == 0:
            # We have to create an object:
            new_object = enumeration()
            new_object.labelname = "default_foreign_key_object"

            # Now point to the default foreign key of textpart:
            textpart_default_key = textpart.get_default_foreignkey()
            textpart_query_result = textpart.objects.filter(pk=textpart_default_key)
            textpart_query_list = list(textpart_query_result)
            new_object.textpart = textpart_query_list[0]

            # Now, save:
            new_object.save()
            return new_object.id
        else:
            # We can return this object:
            return query_list[0].id


# Database model for enumeration-hierarchy:
class enumeration_hierarchy(models.Model):
    """
    Equivalent of the hierarchy under enumeration in the engine.
    """

    # Normal model fields:
    enum_field = models.IntegerField(default=0)

    # ManytoOne relationship: many enumeration_hierarchy correspond to a single enumeration:
    enumeration = models.ForeignKey(enumeration, on_delete=models.CASCADE)

    # Method for printing the instance:
    def __str__(self):
        return str(enum_type(self.enum_field))

    # Metadata definition:
    class Meta:
        app_label = "djangotextsplitter"


# NOTE: Add new textparts here! After the model of title, footer, body, headlines, enumeration.

# Database model for textsplitter
class textsplitter(models.Model):
    """
    Equivalent of the master textsplitter-class in the engine.
    """

    # Unique marker: document filename:
    documentname = models.TextField(default="", unique=True)

    # Normal model fields:
    labelname = models.TextField(default="TextSplitter")
    VERSION = models.TextField(default="")
    ratelimit_timeunit = models.FloatField(default=0.0)
    ratelimit_calls = models.IntegerField(default=0)
    ratelimit_tokens = models.IntegerField(default=0)
    Costs_price = models.FloatField(default=0.0)
    Costs_tokenportion = models.IntegerField(default=0)
    api_rate_starttime = models.FloatField(default=0.0)
    api_rate_currenttime = models.FloatField(default=0.0)
    api_rate_currenttokens = models.IntegerField(default=0)
    api_rate_currentcalls = models.IntegerField(default=0)
    callcounter = models.IntegerField(default=0)
    api_totalprice = models.FloatField(default=0.0)
    api_wrongcalls_duetomaxwhile = models.IntegerField(default=0)
    html_visualization = models.TextField(default="")
    MaxSummaryLength = models.IntegerField(default=50)
    summarization_threshold = models.IntegerField(default=50)
    UseDummySummary = models.BooleanField(default=False)
    LanguageModel = models.TextField(default="gpt-3.5-turbo")
    BackendChoice = models.TextField(default="openai")
    LanguageChoice = models.TextField(default="Default")
    LanguageTemperature = models.FloatField(default=0.1)
    MaxCallRepeat = models.IntegerField(default=20)
    doc_metadata_author = models.TextField(default="None")
    doc_metadata_creator = models.TextField(default="None")
    doc_metadata_producer = models.TextField(default="None")
    doc_metadata_subject = models.TextField(default="None")
    doc_metadata_title = models.TextField(default="None")
    doc_metadata_fullstring = models.TextField(default="")

    # Textpart fields:
    body = models.OneToOneField(body, on_delete=models.CASCADE)
    footer = models.OneToOneField(footer, on_delete=models.CASCADE)
    title = models.OneToOneField(title, on_delete=models.CASCADE)
    headlines = models.OneToOneField(headlines, on_delete=models.CASCADE)
    enumeration = models.OneToOneField(enumeration, on_delete=models.CASCADE)

    # Direct inherticance from textpart: OnetoOne relationship:
    # a textsplitter-object needs an associated textpart (that also needs to be deleted, when this one is deleted):
    textpart = models.OneToOneField(textpart, on_delete=models.CASCADE)

    # User of the text Ik w(if the user or doc is deleted, we want to keep the other one! so SET_DEFAULT)
    owner = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, verbose_name="owner", null=True)

    # Textalinea array: NOTE: taken care of by foreign key from textalinea to here.
    # logfile: That is a textfile-object, not data in the class. We will not save that one.

    # Method for printing the instance:
    def __str__(self):
        return str(self.labelname) + " " + str(self.documentname)

    # Metadata definition:
    class Meta:
        app_label = "djangotextsplitter"

    # method for generating a default foreign key in case someone tries to create a textalinea object
    # without creating the appropriate textsplitter first:
    @staticmethod
    def get_default_foreignkey() -> int:
        """
        This function generates a textsplitter object in the DB
        so that it can be used for passing a default foreign key.
        # parameters: None, #Return: That foreign key.
        """

        # Attempt to find an object with the default labelname:
        query_result = textsplitter.objects.filter(labelname="default_foreign_key_object")
        query_list = list(query_result)

        # Make our key:
        if len(query_list) == 0:
            # We have to create an object:
            new_object = textsplitter()
            new_object.labelname = "default_foreign_key_object"
            new_object.documentname = "default_foreign_key_document"

            # Now point to the default foreign key of title:
            title_default_key = title.get_default_foreignkey()
            title_query_result = title.objects.filter(pk=title_default_key)
            title_query_list = list(title_query_result)
            new_object.title = title_query_list[0]

            # Now point to the default foreign key of body:
            body_default_key = body.get_default_foreignkey()
            body_query_result = body.objects.filter(pk=body_default_key)
            body_query_list = list(body_query_result)
            new_object.body = body_query_list[0]

            # Now point to the default foreign key of footer:
            footer_default_key = footer.get_default_foreignkey()
            footer_query_result = footer.objects.filter(pk=footer_default_key)
            footer_query_list = list(footer_query_result)
            new_object.footer = footer_query_list[0]

            # Now point to the default foreign key of headlines:
            headlines_default_key = headlines.get_default_foreignkey()
            headlines_query_result = headlines.objects.filter(pk=headlines_default_key)
            headlines_query_list = list(headlines_query_result)
            new_object.headlines = headlines_query_list[0]

            # Now point to the default foreign key of enumeration:
            enumeration_default_key = enumeration.get_default_foreignkey()
            enumeration_query_result = enumeration.objects.filter(pk=enumeration_default_key)
            enumeration_query_list = list(enumeration_query_result)
            new_object.enumeration = enumeration_query_list[0]

            # Now point to the default foreign key of textpart:
            textpart_default_key = textpart.get_default_foreignkey()
            textpart_query_result = textpart.objects.filter(pk=textpart_default_key)
            textpart_query_list = list(textpart_query_result)
            new_object.textpart = textpart_query_list[0]

            new_object.save()
            return new_object.id
        else:
            # We can return this object:
            return query_list[0].id


# Database model for a native TOC element:
class Native_TOC_Element(models.Model):
    """
    Equivalent of the Native_TOC_Element-class in the engine.
    """

    # Normal model fields:
    cascadelevel = models.IntegerField(default=0)
    title = models.TextField(default="")
    page = models.IntegerField(default=0)
    Xpos = models.FloatField(default=0.0)
    Ypos = models.FloatField(default=0.0)
    Zpos = models.FloatField(default=0.0)

    # ManytoOne relationship: many fontregions correspond to a single textpart:
    textsplitter = models.ForeignKey(textsplitter, on_delete=models.CASCADE)

    # Method for printing the instance:
    def __str__(self):
        return str(self.title)

    # Metadata definition:
    class Meta:
        app_label = "djangotextsplitter"


# Database model for a native TOC element:
class breakdown_decisions(models.Model):
    """
    Used to store the breakdown decisions per textline of the textsplitter.
    """

    # Normal model fields:
    textline = models.TextField(default="")

    # ManytoOne relationship: many fontregions correspond to a single textpart:
    textsplitter = models.ForeignKey(textsplitter, on_delete=models.CASCADE)

    # Method for printing the instance:
    def __str__(self):
        return str(self.textline)

    # Metadata definition:
    class Meta:
        app_label = "djangotextsplitter"


# Database model for textalinea:
class textalinea(models.Model):
    """
    Equivalent of the textalinea-class in the engine.
    """

    # Normal model fields:
    labelname = models.TextField(default="Alinea")
    textlevel = models.IntegerField(default=0)
    typelevel = models.IntegerField(default=0)
    texttitle = models.TextField(default="")
    nativeID = models.IntegerField(default=-1)
    parentID = models.IntegerField(default=-1)
    horizontal_ordering = models.IntegerField(default=-1)
    summary = models.TextField(default="")
    sum_CanbeEmpty = models.BooleanField(default=False)
    alineatype = models.IntegerField(default=0)  # NOTE: enum_type
    enumtype = models.IntegerField(default=0)  # NOTE: enum_type
    html_visualization = models.TextField(default="")
    summarized_wordcount = models.IntegerField(default=0)
    total_wordcount = models.IntegerField(default=0)
    nr_decendants = models.IntegerField(default=0)
    nr_children = models.IntegerField(default=0)
    nr_depths = models.IntegerField(default=0)
    nr_pages = models.IntegerField(default=0)

    # OnetoOne relationship: a textalinea-object needs an associated textpart (that also needs to be deleted, when this one is deleted):
    textpart = models.OneToOneField(textpart, on_delete=models.CASCADE)

    # ManytoOne relationship: many textalineas correspond to a single textsplitter:
    textsplitter = models.ForeignKey(textsplitter, on_delete=models.CASCADE)

    # Method for printing the instance:
    def __str__(self):
        return str(self.textpart.documentname) + " " + str(self.texttitle)

    # Metadata definition:
    class Meta:
        app_label = "djangotextsplitter"

    # Method for generating a default foreign key in case someone tries to create an object pointing here
    # without creating the appropriate textpart first:
    @staticmethod
    def get_default_foreignkey() -> int:
        """
        This function generates an textalinea object in the DB
        so that it can be used for passing a default foreign key.
        # parameters: None, #Return: That foreign key.
        """

        # Attempt to find an object with -1 cascade level:
        query_result = textalinea.objects.filter(labelname="default_foreign_key_object")
        query_list = list(query_result)

        # Make our key:
        if len(query_list) == 0:
            # We have to create an object:
            new_object = textalinea()
            new_object.labelname = "default_foreign_key_object"

            # Now point to the default foreign key of textpart:
            textpart_default_key = textpart.get_default_foreignkey()
            textpart_query_result = textpart.objects.filter(pk=textpart_default_key)
            textpart_query_list = list(textpart_query_result)
            new_object.textpart = textpart_query_list[0]

            # Now point to the default foreign key of textsplitter:
            textsplitter_default_key = textsplitter.get_default_foreignkey()
            textsplitter_query_result = textsplitter.objects.filter(pk=textsplitter_default_key)
            textsplitter_query_list = list(textsplitter_query_result)
            new_object.textsplitter = textsplitter_query_list[0]

            # Now, save:
            new_object.save()
            return new_object.id
        else:
            # We can return this object:
            return query_list[0].id
