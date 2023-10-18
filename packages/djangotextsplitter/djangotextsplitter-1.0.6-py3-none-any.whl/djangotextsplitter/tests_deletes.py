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

# Import Django functionality
from django.test import TestCase, tag
from django.contrib.auth.models import User

# Import required functionality:
from .loads import load_fontregion
from .loads import load_lineregion
from .loads import load_textpart
from .loads import load_title
from .loads import load_body
from .loads import load_footer
from .loads import load_headlines
from .loads import load_enumeration
from .loads import load_textalinea
from .loads import load_textsplitter
from .loads import load_Native_TOC_Element
from .newwrites import newwrite_fontregion
from .newwrites import newwrite_lineregion
from .newwrites import newwrite_textpart
from .newwrites import newwrite_title
from .newwrites import newwrite_body
from .newwrites import newwrite_footer
from .newwrites import newwrite_headlines
from .newwrites import newwrite_enumeration
from .newwrites import newwrite_textalinea
from .newwrites import newwrite_textsplitter
from .newwrites import newwrite_Native_TOC_Element
from .deletes import delete_fontregion
from .deletes import delete_lineregion
from .deletes import delete_textpart
from .deletes import delete_title
from .deletes import delete_footer
from .deletes import delete_body
from .deletes import delete_headlines
from .deletes import delete_enumeration
from .deletes import delete_textalinea
from .deletes import delete_textsplitter
from .deletes import delete_Native_TOC_Element

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


# Creation of the test classes:
@tag("database", "unit", "delete")
class fontregion_delete_tests(TestCase):
    def test_delete(self):
        """
        Unit test for a write-read operation that ovverwrites an existing DB-item.
        # Parameters: none; # Returns (bool): succes of the text.
        # Author: Christiaan Douma
        """

        # Create some nice examples of a textpart fontregion:
        textpart_object_1 = textpart_fontregion()
        textpart_object_1.left = 2.21
        textpart_object_1.right = 4.41
        textpart_object_1.value = 3.31
        textpart_object_1.frequency = 0.89
        textpart_object_1.cascadelevel = 2
        textpart_object_1.isregular = True

        textpart_object_2 = textpart_fontregion()
        textpart_object_2.left = 1.21
        textpart_object_2.right = 5.41
        textpart_object_2.value = 7.31
        textpart_object_2.frequency = 0.79
        textpart_object_2.cascadelevel = 3
        textpart_object_2.isregular = False

        # Write both objects to the database:
        db_object_1 = newwrite_fontregion(textpart_object_1)
        db_object_2 = newwrite_fontregion(textpart_object_2)

        # Now, delete one of them:
        delete_fontregion(db_object_1.id)

        # Next, attempt to delete something that we know does not exist:
        delete_fontregion(db_object_1.id + db_object_2.id + 1)

        # Next, test that we indeed have precisely one object left:

        # Next, retrieve the ID's. We test that, indeed nothing else is in the test-DB,
        # by testing that the length has to be exactly 1:
        id_list = list(db_fontregion.objects.values_list("id", flat=True).order_by("id"))
        id_length = len(id_list)

        # Test if there is actually something in the DB now:
        if not (id_length == 1):
            print(
                "\n ==> RAPPORT <fontregion test_delete>: The number of DB-entries was not as we expected!\n"
            )
            print(id_list)
            self.assertIs(True, False)
        else:
            # Then, we are fine:
            self.assertIs(True, True)

        # Done.


@tag("database", "unit", "delete")
class lineregion_delete_tests(TestCase):
    def test_delete(self):
        """
        Unit test for a write-read operation that ovverwrites an existing DB-item.
        # Parameters: none; # Returns (bool): succes of the text.
        # Author: Christiaan Douma
        """

        # Create some nice examples of a textpart lineregion:
        textpart_object_1 = textpart_lineregion()
        textpart_object_1.left = 2.21
        textpart_object_1.right = 4.41
        textpart_object_1.value = 3.31
        textpart_object_1.frequency = 0.89
        textpart_object_1.isregular = True
        textpart_object_1.issmall = True
        textpart_object_1.isbig = True
        textpart_object_1.iszero = True
        textpart_object_1.isvalid = True

        textpart_object_2 = textpart_lineregion()
        textpart_object_2.left = 1.21
        textpart_object_2.right = 5.41
        textpart_object_2.value = 7.31
        textpart_object_2.frequency = 0.79
        textpart_object_2.isregular = False
        textpart_object_2.issmall = True
        textpart_object_2.isbig = False
        textpart_object_2.iszero = True
        textpart_object_2.isvalid = False

        # Write both objects to the database:
        db_object_1 = newwrite_lineregion(textpart_object_1)
        db_object_2 = newwrite_lineregion(textpart_object_2)

        # Now, delete one of them:
        delete_lineregion(db_object_1.id)

        # Next, attempt to delete something that we know does not exist:
        delete_lineregion(db_object_1.id + db_object_2.id + 1)

        # Next, test that we indeed have precisely one object left:

        # Next, retrieve the ID's. We test that, indeed nothing else is in the test-DB,
        # by testing that the length has to be exactly 1:
        id_list = list(db_lineregion.objects.values_list("id", flat=True).order_by("id"))
        id_length = len(id_list)

        # Test if there is actually something in the DB now:
        if not (id_length == 1):
            print(
                "\n ==> RAPPORT <lineregion test_delete>: The number of DB-entries was not as we expected!\n"
            )
            print(id_list)
            self.assertIs(True, False)
        else:
            # then, we are fine:
            self.assertIs(True, True)

        # Done.


@tag("database", "unit", "delete")
class textpart_delete_tests(TestCase):
    def test_delete(self):
        """
        Unit test for a write-read operation that ovverwrites an existing DB-item.
        # Parameters: none; # Returns (bool): succes of the text.
        # Author: Christiaan Douma
        """

        # Create a nice example of a textpart class:
        textpart_object_1 = textpart_textpart()
        textpart_object_1.labelname = "Test for newwrite"
        textpart_object_1.documentpath = "/some/path/"
        textpart_object_1.outputpath = "/another/path/"
        textpart_object_1.documentname = "Hope for success"
        textpart_object_1.histogramsize = 2
        textpart_object_1.headerboundary = 700.0
        textpart_object_1.footerboundary = 20.0
        textpart_object_1.ruleverbosity = 2
        textpart_object_1.verbosetextline = "some nice line"
        textpart_object_1.nr_bold_chars = 102
        textpart_object_1.nr_total_chars = 1020
        textpart_object_1.boldchars_ratio = 0.02
        textpart_object_1.boldratio_threshold = 0.06
        textpart_object_1.max_vertpos = 695.0
        textpart_object_1.min_vertpos = 15.0
        fontregion_1 = textpart_fontregion()
        fontregion_1.left = 2.21
        fontregion_1.right = 4.41
        fontregion_1.value = 3.31
        fontregion_1.frequency = 0.89
        fontregion_1.cascadelevel = 2
        fontregion_1.isregular = True
        fontregion_2 = textpart_fontregion()
        fontregion_2.left = 4.41
        fontregion_2.right = 6.61
        fontregion_2.value = 5.51
        fontregion_2.frequency = 0.08
        fontregion_2.cascadelevel = 1
        fontregion_2.isregular = False
        lineregion_1 = textpart_lineregion()
        lineregion_1.left = 2.21
        lineregion_1.right = 4.41
        lineregion_1.value = 3.31
        lineregion_1.frequency = 0.89
        lineregion_1.isregular = True
        lineregion_1.issmall = True
        lineregion_1.isbig = True
        lineregion_1.iszero = True
        lineregion_1.isvalid = True
        lineregion_2 = textpart_lineregion()
        lineregion_2.left = 1.21
        lineregion_2.right = 5.41
        lineregion_2.value = 7.31
        lineregion_2.frequency = 0.79
        lineregion_2.isregular = False
        lineregion_2.issmall = True
        lineregion_2.isbig = False
        lineregion_2.iszero = True
        lineregion_2.isvalid = False
        textpart_object_1.fontregions = [fontregion_1, fontregion_2]
        textpart_object_1.lineregions = [lineregion_1, lineregion_2]
        textpart_object_1.textcontent = ["my fisrt textline", "another textline", "Now I get bored"]
        textpart_object_1.pagenumbers = [1, 2, 3]
        textpart_object_1.positioncontent = [5.0, 10.0, 20.0]
        textpart_object_1.horposcontent = [1.0, 2.0, 3.0]
        textpart_object_1.whitelinesize = [-2.0, 5.0, 10.0]
        textpart_object_1.fontsize_perline = [12.0, 13.0, 14.0]
        textpart_object_1.is_italic = [True, False, False]
        textpart_object_1.is_bold = [False, True, False]
        textpart_object_1.is_highlighted = [False, False, True]
        textpart_object_1.fontsizeHist_percharacter = [
            [10.0, 20.0],
            [1.0, 2.0, 3.0],
            [1.0, 2.0, 3.0],
        ]
        textpart_object_1.fontsizeHist_perline = [[11.0, 21.0], [1.1, 2.1, 3.1], [1.1, 2.1, 3.1]]
        textpart_object_1.whitespaceHist_perline = [[12.0, 22.0], [1.2, 2.2, 3.1], [1.2, 2.2, 3.2]]

        # Create a second nice example of a textpart class:
        textpart_object_2 = textpart_textpart()
        textpart_object_2.labelname = "Test for overwrite"
        textpart_object_2.documentpath = "/some/other/path/"
        textpart_object_2.outputpath = "/another/stupid/path/"
        textpart_object_2.documentname = "Hope for double success"
        textpart_object_2.histogramsize = 1
        textpart_object_2.headerboundary = 710.0
        textpart_object_2.footerboundary = 21.0
        textpart_object_2.ruleverbosity = 3
        textpart_object_2.verbosetextline = "some supernice line"
        textpart_object_2.nr_bold_chars = 103
        textpart_object_2.nr_total_chars = 1120
        textpart_object_2.boldchars_ratio = 0.021
        textpart_object_2.boldratio_threshold = 0.07
        textpart_object_2.max_vertpos = 696.0
        textpart_object_2.min_vertpos = 12.0
        fontregion_3 = textpart_fontregion()
        fontregion_3.left = 2.22
        fontregion_3.right = 4.43
        fontregion_3.value = 3.34
        fontregion_3.frequency = 0.85
        fontregion_3.cascadelevel = 1
        fontregion_3.isregular = False
        fontregion_4 = textpart_fontregion()
        fontregion_4.left = 4.49
        fontregion_4.right = 6.68
        fontregion_4.value = 5.57
        fontregion_4.frequency = 0.06
        fontregion_4.cascadelevel = 2
        fontregion_4.isregular = True
        fontregion_5 = textpart_fontregion()
        fontregion_5.left = 6.68
        fontregion_5.right = 7.31
        fontregion_5.value = 10.2
        fontregion_5.frequency = 0.02
        fontregion_5.cascadelevel = 3
        fontregion_5.isregular = False
        lineregion_3 = textpart_lineregion()
        lineregion_3.left = 2.21
        lineregion_3.right = 4.41
        lineregion_3.value = 3.31
        lineregion_3.frequency = 0.89
        lineregion_3.isregular = True
        lineregion_3.issmall = True
        lineregion_3.isbig = True
        lineregion_3.iszero = True
        lineregion_3.isvalid = True
        textpart_object_2.fontregions = [fontregion_3, fontregion_4, fontregion_5]
        textpart_object_2.lineregions = [lineregion_3]
        textpart_object_2.textcontent = ["my second textline", "another amazing textline"]
        textpart_object_2.pagenumbers = [4, 5]
        textpart_object_2.positioncontent = [6.0, 12.0]
        textpart_object_2.horposcontent = [1.1, 2.1]
        textpart_object_2.whitelinesize = [-2.0, 6.0]
        textpart_object_2.fontsize_perline = [11.0, 15.0]
        textpart_object_2.is_italic = [False, True]
        textpart_object_2.is_bold = [True, False]
        textpart_object_2.is_highlighted = [True, True]
        textpart_object_2.fontsizeHist_percharacter = [[7.0], [1.5, 2.5], [1.5, 2.5]]
        textpart_object_2.fontsizeHist_perline = [[8.0], [1.6, 2.6], [1.6, 2.6]]
        textpart_object_2.whitespaceHist_perline = [[9.0], [1.7, 2.7], [1.7, 2.7]]

        # Write both objects to the database:
        db_object_1 = newwrite_textpart(textpart_object_1)
        db_object_2 = newwrite_textpart(textpart_object_2)

        # Now, delete one of them:
        delete_textpart(db_object_1.id)

        # Next, attempt to delete something that we know does not exist:
        delete_textpart(db_object_1.id + db_object_2.id + 1)

        # Next, test that we indeed have precisely one object left:

        # Next, retrieve the ID's. We test that, indeed nothing else is in the test-DB,
        # by testing that the length has to be exactly 1:
        id_list = list(db_textpart.objects.values_list("id", flat=True).order_by("id"))
        id_length = len(id_list)

        # Eliminate presence of default foreign key object:
        for k in range(0, id_length):
            Index = id_length - k - 1
            if load_textpart(id_list[Index]).labelname == "default_foreign_key_object":
                id_list.pop(Index)
        id_length = len(id_list)

        # Also test for fontregions:
        id_list_fontregion = list(db_fontregion.objects.values_list("id", flat=True).order_by("id"))
        id_length_fontregion = len(id_list_fontregion)

        # Also test for lineregions:
        id_list_lineregion = list(db_lineregion.objects.values_list("id", flat=True).order_by("id"))
        id_length_lineregion = len(id_list_lineregion)

        # Also test for readinglines:
        id_list_readingline = list(
            db_readingline.objects.values_list("id", flat=True).order_by("id")
        )
        id_length_readingline = len(id_list_readingline)

        # Also test for readinghistograms:
        id_list_readinghistogram = list(
            db_readinghistogram.objects.values_list("id", flat=True).order_by("id")
        )
        id_length_readinghistogram = len(id_list_readinghistogram)

        # Test if there is actually something in the DB now:
        if not (
            (id_length == 1)
            and (id_length_fontregion == 3)
            and (id_length_lineregion == 1)
            and (id_length_readingline == 2)
            and (id_length_readinghistogram == 6)
        ):
            print(
                "\n ==> RAPPORT <textpart test_delete>: The number of DB-entries was not as we expected!\n"
            )
            print(id_list)
            print(id_list_fontregion)
            print(id_list_lineregion)
            print(id_list_readingline)
            print(id_list_readinghistogram)
            self.assertIs(True, False)
        else:
            # then, we are fine:
            self.assertIs(True, True)

        # Done.


@tag("database", "unit", "delete")
class title_delete_tests(TestCase):
    def test_delete(self):
        """
        Unit test for a write-read operation that ovverwrites an existing DB-item.
        # Parameters: none; # Returns (bool): succes of the text.
        # Author: Christiaan Douma
        """

        # Create a nice example of a title class. Only pass in just enough information
        # to see if the parent-class textpart gets handled. Do not use labelname, as
        # that one is supposed to be automatically set in the title-object.
        textpart_object_1 = textpart_title()
        textpart_object_1.documentname = "This is a test-object for a title-class"  # ATTENTION: This is to prove that we indeed can dig one level deeper.

        textpart_object_2 = textpart_title()
        textpart_object_2.documentname = "This is the second test-object for a title-class"

        # Write both objects to the database:
        db_object_1 = newwrite_title(textpart_object_1)
        db_object_2 = newwrite_title(textpart_object_2)

        # Now, delete one of them:
        delete_title(db_object_1.id)

        # Next, attempt to delete something that we know does not exist:
        delete_title(db_object_1.id + db_object_2.id + 1)

        # Next, test that we indeed have precisely one object left:

        # Next, retrieve the ID's. We test that, indeed nothing else is in the test-DB,
        # by testing that the length has to be exactly 1:
        id_list = list(db_title.objects.values_list("id", flat=True).order_by("id"))
        id_length = len(id_list)

        # Eliminate presence of default foreign key object:
        for k in range(0, id_length):
            Index = id_length - k - 1
            if load_title(id_list[Index]).labelname == "default_foreign_key_object":
                id_list.pop(Index)
        id_length = len(id_list)

        # Also test for textparts:
        id_list_textpart = list(db_textpart.objects.values_list("id", flat=True).order_by("id"))
        id_length_textpart = len(id_list_textpart)

        # Eliminate presence of default foreign key object:
        for k in range(0, id_length_textpart):
            Index = id_length_textpart - k - 1
            if load_textpart(id_list_textpart[Index]).labelname == "default_foreign_key_object":
                id_list_textpart.pop(Index)
        id_length_textpart = len(id_list_textpart)

        # Test if there is actually something in the DB now:
        if not ((id_length == 1) and (id_length_textpart == 1)):
            print(
                "\n ==> RAPPORT <title test_delete>: The number of DB-entries was not as we expected!\n"
            )
            print(id_list)
            print(id_list_textpart)
            self.assertIs(True, False)
        else:
            # then, we are fine:
            self.assertIs(True, True)

            # Done.


@tag("database", "unit", "delete")
class body_delete_tests(TestCase):
    def test_delete(self):
        """
        Unit test for a write-read operation that ovverwrites an existing DB-item.
        # Parameters: none; # Returns (bool): succes of the text.
        # Author: Christiaan Douma
        """

        # Create a nice example of a body class. Only pass in just enough information
        # to see if the parent-class textpart gets handled. Do not use labelname, as
        # that one is supposed to be automatically set in the body-object.
        textpart_object_1 = textpart_body()
        textpart_object_1.documentname = "This is a test-object for a body-class"  # ATTENTION: This is to prove that we indeed can dig one level deeper.

        textpart_object_2 = textpart_body()
        textpart_object_2.documentname = "This is the second test-object for a body-class"

        # Write both objects to the database:
        db_object_1 = newwrite_body(textpart_object_1)
        db_object_2 = newwrite_body(textpart_object_2)

        # Now, delete one of them:
        delete_body(db_object_1.id)

        # Next, attempt to delete something that we know does not exist:
        delete_body(db_object_1.id + db_object_2.id + 1)

        # Next, test that we indeed have precisely one object left:

        # Next, retrieve the ID's. We test that, indeed nothing else is in the test-DB,
        # by testing that the length has to be exactly 1:
        id_list = list(db_body.objects.values_list("id", flat=True).order_by("id"))
        id_length = len(id_list)

        # Eliminate presence of default foreign key object:
        for k in range(0, id_length):
            Index = id_length - k - 1
            if load_body(id_list[Index]).labelname == "default_foreign_key_object":
                id_list.pop(Index)
        id_length = len(id_list)

        # Also test for textparts:
        id_list_textpart = list(db_textpart.objects.values_list("id", flat=True).order_by("id"))
        id_length_textpart = len(id_list_textpart)

        # Eliminate presence of default foreign key object:
        for k in range(0, id_length_textpart):
            Index = id_length_textpart - k - 1
            if load_textpart(id_list_textpart[Index]).labelname == "default_foreign_key_object":
                id_list_textpart.pop(Index)
        id_length_textpart = len(id_list_textpart)

        # Test if there is actually something in the DB now:
        if not ((id_length == 1) and (id_length_textpart == 1)):
            print(
                "\n ==> RAPPORT <body test_delete>: The number of DB-entries was not as we expected!\n"
            )
            print(id_list)
            print(id_list_textpart)
            self.assertIs(True, False)
        else:
            # Then, we are fine.
            self.assertIs(True, True)

            # Done.


@tag("database", "unit", "delete")
class footer_delete_tests(TestCase):
    def test_delete(self):
        """
        Unit test for a write-read operation that ovverwrites an existing DB-item.
        # Parameters: none; # Returns (bool): succes of the text.
        # Author: Christiaan Douma
        """

        # Create a nice example of a footer class. Only pass in just enough information
        # to see if the parent-class textpart gets handled. Do not use labelname, as
        # that one is supposed to be automatically set in the footer-object.
        textpart_object_1 = textpart_footer()
        textpart_object_1.documentname = "This is a test-object for a footer-class"  # ATTENTION: This is to prove that we indeed can dig one level deeper.

        textpart_object_2 = textpart_footer()
        textpart_object_2.documentname = "This is the second test-object for a footer-class"

        # Write both objects to the database:
        db_object_1 = newwrite_footer(textpart_object_1)
        db_object_2 = newwrite_footer(textpart_object_2)

        # Now, delete one of them:
        delete_footer(db_object_1.id)

        # Next, attempt to delete something that we know does not exist:
        delete_footer(db_object_1.id + db_object_2.id + 1)

        # Next, test that we indeed have precisely one object left:

        # Next, retrieve the ID's. We test that, indeed nothing else is in the test-DB,
        # by testing that the length has to be exactly 1:
        id_list = list(db_footer.objects.values_list("id", flat=True).order_by("id"))
        id_length = len(id_list)

        # Eliminate presence of default foreign key object:
        for k in range(0, id_length):
            Index = id_length - k - 1
            if load_footer(id_list[Index]).labelname == "default_foreign_key_object":
                id_list.pop(Index)
        id_length = len(id_list)

        # Also test for textparts:
        id_list_textpart = list(db_textpart.objects.values_list("id", flat=True).order_by("id"))
        id_length_textpart = len(id_list_textpart)

        # Eliminate presence of default foreign key object:
        for k in range(0, id_length_textpart):
            Index = id_length_textpart - k - 1
            if load_textpart(id_list_textpart[Index]).labelname == "default_foreign_key_object":
                id_list_textpart.pop(Index)
        id_length_textpart = len(id_list_textpart)

        # Test if there is actually something in the DB now:
        if not ((id_length == 1) and (id_length_textpart == 1)):
            print(
                "\n ==> RAPPORT <footer test_delete>: The number of DB-entries was not as we expected!\n"
            )
            print(id_list)
            print(id_list_textpart)
            self.assertIs(True, False)
        else:
            # Then, we are fine.
            self.assertIs(True, True)

            # Done.


@tag("database", "unit", "delete")
class headlines_delete_tests(TestCase):
    def test_delete(self):
        """
        Unit test for a write-read operation that ovverwrites an existing DB-item.
        # Parameters: none; # Returns (bool): succes of the text.
        # Author: Christiaan Douma
        """

        # Create a nice example of a headlines class. Only pass in just enough information
        # to see if the parent-class textpart gets handled. Do not use labelname, as
        # that one is supposed to be automatically set in the headlines-object.
        textpart_object_1 = textpart_headlines()
        textpart_object_1.documentname = "This is a test-object for a headlines-class"  # ATTENTION: This is to prove that we indeed can dig one level deeper.
        textpart_object_1.hierarchy = [
            textpart_enum_type.BIGROMAN,
            textpart_enum_type.DIGIT,
            textpart_enum_type.SMALLLETTER,
        ]

        textpart_object_2 = textpart_headlines()
        textpart_object_2.documentname = "This is the second test-object for a headlines-class"
        textpart_object_2.hierarchy = [textpart_enum_type.SIGNMARK, textpart_enum_type.SMALLROMAN]

        # Write both objects to the database:
        db_object_1 = newwrite_headlines(textpart_object_1)
        db_object_2 = newwrite_headlines(textpart_object_2)

        # Now, delete one of them:
        delete_headlines(db_object_1.id)

        # Next, attempt to delete something that we know does not exist:
        delete_headlines(db_object_1.id + db_object_2.id + 1)

        # Next, test that we indeed have precisely one object left:

        # Next, retrieve the ID's. We test that, indeed nothing else is in the test-DB,
        # by testing that the length has to be exactly 1:
        id_list = list(db_headlines.objects.values_list("id", flat=True).order_by("id"))
        id_length = len(id_list)

        # Eliminate presence of default foreign key object:
        for k in range(0, id_length):
            Index = id_length - k - 1
            if load_headlines(id_list[Index]).labelname == "default_foreign_key_object":
                id_list.pop(Index)
        id_length = len(id_list)

        # Also test for textparts:
        id_list_textpart = list(db_textpart.objects.values_list("id", flat=True).order_by("id"))
        id_length_textpart = len(id_list_textpart)

        # Eliminate presence of default foreign key object:
        for k in range(0, id_length_textpart):
            Index = id_length_textpart - k - 1
            if load_textpart(id_list_textpart[Index]).labelname == "default_foreign_key_object":
                id_list_textpart.pop(Index)
        id_length_textpart = len(id_list_textpart)

        # Also for the hierarchy:
        id_list_hierarchy = list(
            db_headlines_hierarchy.objects.values_list("id", flat=True).order_by("id")
        )
        id_length_hierarchy = len(id_list_hierarchy)

        # Test if there is actually something in the DB now:
        if not ((id_length == 1) and (id_length_textpart == 1) and (id_length_hierarchy == 2)):
            print(
                "\n ==> RAPPORT <headlines test_delete>: The number of DB-entries was not as we expected!\n"
            )
            print(id_list)
            print(id_list_textpart)
            print(id_list_hierarchy)
            self.assertIs(True, False)
        else:
            # Then, we are fine:
            self.assertIs(True, True)

            # Done.


@tag("database", "unit", "delete")
class enumeration_delete_tests(TestCase):
    def test_delete(self):
        """
        Unit test for a write-read operation that ovverwrites an existing DB-item.
        # Parameters: none; # Returns (bool): succes of the text.
        # Author: Christiaan Douma
        """

        # Create a nice example of a enumeration class. Only pass in just enough information
        # to see if the parent-class textpart gets handled. Do not use labelname, as
        # that one is supposed to be automatically set in the enumeration-object.
        textpart_object_1 = textpart_enumeration()
        textpart_object_1.documentname = "This is a test-object for a enumeration-class"  # ATTENTION: This is to prove that we indeed can dig one level deeper.
        textpart_object_1.hierarchy = [
            textpart_enum_type.BIGROMAN,
            textpart_enum_type.DIGIT,
            textpart_enum_type.SMALLLETTER,
        ]
        textpart_object_1.last_enumtype_index = 1
        textpart_object_1.this_enumtype_index = 2
        textpart_object_1.last_textline_bigroman = "IX. en dan nog wat"
        textpart_object_1.last_textline_smallroman = "vii) komt er nog wat van?"
        textpart_object_1.last_textline_bigletter = "F) en nog iets"
        textpart_object_1.last_textline_smallletter = "(a) gaat zo nog even door"
        textpart_object_1.last_textline_digit = "3) en zo voort"
        textpart_object_1.last_textline_signmark = "– ta ta ta"

        textpart_object_2 = textpart_enumeration()
        textpart_object_2.documentname = "This is the second test-object for a enumeration-class"
        textpart_object_2.hierarchy = [textpart_enum_type.SIGNMARK, textpart_enum_type.SMALLROMAN]
        textpart_object_2.last_enumtype_index = 3
        textpart_object_2.this_enumtype_index = 4
        textpart_object_2.last_textline_bigroman = "XI. en dan dan nog wat"
        textpart_object_2.last_textline_smallroman = "vi) komt er ooit nog wat van?"
        textpart_object_2.last_textline_bigletter = "G) en dan nog iets"
        textpart_object_2.last_textline_smallletter = "(b) gaat zo nog door"
        textpart_object_2.last_textline_digit = "4) enzo voort"
        textpart_object_2.last_textline_signmark = "– ta ta"

        # Write both objects to the database:
        db_object_1 = newwrite_enumeration(textpart_object_1)
        db_object_2 = newwrite_enumeration(textpart_object_2)

        # Now, delete one of them:
        delete_enumeration(db_object_1.id)

        # Next, attempt to delete something that we know does not exist:
        delete_enumeration(db_object_1.id + db_object_2.id + 1)

        # Next, test that we indeed have precisely one object left:

        # Next, retrieve the ID's. We test that, indeed nothing else is in the test-DB,
        # by testing that the length has to be exactly 1:
        id_list = list(db_enumeration.objects.values_list("id", flat=True).order_by("id"))
        id_length = len(id_list)

        # Eliminate presence of default foreign key object:
        for k in range(0, id_length):
            Index = id_length - k - 1
            if load_enumeration(id_list[Index]).labelname == "default_foreign_key_object":
                id_list.pop(Index)
        id_length = len(id_list)

        # Also test for textparts:
        id_list_textpart = list(db_textpart.objects.values_list("id", flat=True).order_by("id"))
        id_length_textpart = len(id_list_textpart)

        # Eliminate presence of default foreign key object:
        for k in range(0, id_length_textpart):
            Index = id_length_textpart - k - 1
            if load_textpart(id_list_textpart[Index]).labelname == "default_foreign_key_object":
                id_list_textpart.pop(Index)
        id_length_textpart = len(id_list_textpart)

        # Also for the hierarchy:
        id_list_hierarchy = list(
            db_enumeration_hierarchy.objects.values_list("id", flat=True).order_by("id")
        )
        id_length_hierarchy = len(id_list_hierarchy)

        # Test if there is actually something in the DB now:
        if not ((id_length == 1) and (id_length_textpart == 1) and (id_length_hierarchy == 2)):
            print(
                "\n ==> RAPPORT <enumeration test_delete>: The number of DB-entries was not as we expected!\n"
            )
            print(id_list)
            print(id_list_textpart)
            print(id_list_hierarchy)
            self.assertIs(True, False)
        else:
            # Then, we are fine:
            self.assertIs(True, True)

            # Done.


@tag("database", "unit", "delete")
class textalinea_delete_tests(TestCase):
    def test_delete(self):
        """
        Unit test for a write-read operation that ovverwrites an existing DB-item.
        # Parameters: none; # Returns (bool): succes of the text.
        # Author: Christiaan Douma
        """

        # Create a nice example of a textalinea class. Only pass in just enough information
        # to see if the parent-class textpart gets handled. Do not use labelname, as
        # that one is supposed to be automatically set in the textalinea-object.
        textpart_object_1 = textpart_textalinea()
        textpart_object_1.documentname = "This is a test-object for a textalinea-class"  # ATTENTION: This is to prove that we indeed can dig one level deeper.
        textpart_object_1.textlevel = 1
        textpart_object_1.typelevel = 2
        textpart_object_1.texttitle = "Stomme titel"
        textpart_object_1.nativeID = 3
        textpart_object_1.parentID = 4
        textpart_object_1.horizontal_ordering = 5
        textpart_object_1.summary = "Moet ik die nou ook nog allemaal typen?"
        textpart_object_1.sum_CanbeEmpty = True
        textpart_object_1.alineatype = textpart_texttype.HEADLINES
        textpart_object_1.enumtype = textpart_enum_type.UNKNOWN
        textpart_object_1.html_visualization = "<html>"
        textpart_object_1.summarized_wordcount = 6
        textpart_object_1.total_wordcount = 7
        textpart_object_1.nr_decendants = 8
        textpart_object_1.nr_children = 9
        textpart_object_1.nr_depths = 10
        textpart_object_1.nr_pages = 11

        textpart_object_2 = textpart_textalinea()
        textpart_object_2.documentname = "This is the second test-object for a textalinea-class"
        textpart_object_2.textlevel = 11
        textpart_object_2.typelevel = 10
        textpart_object_2.texttitle = "Stomme en lange titel"
        textpart_object_2.nativeID = 9
        textpart_object_2.parentID = 8
        textpart_object_2.horizontal_ordering = 7
        textpart_object_2.summary = "Moet ik die ook nog allemaal typen?"
        textpart_object_2.sum_CanbeEmpty = False
        textpart_object_2.alineatype = textpart_texttype.ENUMERATION
        textpart_object_2.enumtype = textpart_enum_type.BIGLETTER
        textpart_object_2.html_visualization = "<html></html>"
        textpart_object_2.summarized_wordcount = 6
        textpart_object_2.total_wordcount = 5
        textpart_object_2.nr_decendants = 4
        textpart_object_2.nr_children = 3
        textpart_object_2.nr_depths = 2
        textpart_object_2.nr_pages = 1

        # Write both objects to the database:
        db_object_1 = newwrite_textalinea(textpart_object_1)
        db_object_2 = newwrite_textalinea(textpart_object_2)

        # Now, delete one of them:
        delete_textalinea(db_object_1.id)

        # Next, attempt to delete something that we know does not exist:
        delete_textalinea(db_object_1.id + db_object_2.id + 1)

        # Next, test that we indeed have precisely one object left:

        # Next, retrieve the ID's. We test that, indeed nothing else is in the test-DB,
        # by testing that the length has to be exactly 1:
        id_list = list(db_textalinea.objects.values_list("id", flat=True).order_by("id"))
        id_length = len(id_list)

        # Eliminate presence of default foreign key object:
        for k in range(0, id_length):
            Index = id_length - k - 1
            if load_textalinea(id_list[Index]).labelname == "default_foreign_key_object":
                id_list.pop(Index)
        id_length = len(id_list)

        # Also test for textparts:
        id_list_textpart = list(db_textpart.objects.values_list("id", flat=True).order_by("id"))
        id_length_textpart = len(id_list_textpart)

        # Eliminate presence of default foreign key object:
        for k in range(0, id_length_textpart):
            Index = id_length_textpart - k - 1
            if load_textpart(id_list_textpart[Index]).labelname == "default_foreign_key_object":
                id_list_textpart.pop(Index)
        id_length_textpart = len(id_list_textpart)

        # Test if there is actually something in the DB now:
        if not ((id_length == 1) and (id_length_textpart == 1)):
            print(
                "\n ==> RAPPORT <textalinea test_delete>: The number of DB-entries was not as we expected!\n"
            )
            print(id_list)
            print(id_list_textpart)
            self.assertIs(True, False)
        else:
            # Then, we are fine:
            self.assertIs(True, True)

            # Done.


@tag("database", "unit", "delete")
class Native_TOC_Element_delete_tests(TestCase):
    def test_delete(self):
        """
        Unit test for a write-read operation that ovverwrites an existing DB-item.
        # Parameters: none; # Returns (bool): succes of the text.
        # Author: Christiaan Douma
        """

        # Create some nice examples of a textpart fontregion:
        textpart_object_1 = textpart_Native_TOC_Element()
        textpart_object_1.cascadelevel = 1
        textpart_object_1.title = "Wat een leuk hoofdstuk"
        textpart_object_1.page = 2
        textpart_object_1.Xpos = 10.0
        textpart_object_1.Ypos = 11.0
        textpart_object_1.Zpos = 12.0

        textpart_object_2 = textpart_Native_TOC_Element()
        textpart_object_2.cascadelevel = 3
        textpart_object_2.title = "Wat een dom hoofdstuk"
        textpart_object_2.page = 4
        textpart_object_2.Xpos = 20.0
        textpart_object_2.Ypos = 21.0
        textpart_object_2.Zpos = 22.0

        # Write both objects to the database:
        db_object_1 = newwrite_Native_TOC_Element(textpart_object_1)
        db_object_2 = newwrite_Native_TOC_Element(textpart_object_2)

        # Now, delete one of them:
        delete_Native_TOC_Element(db_object_1.id)

        # Next, attempt to delete something that we know does not exist:
        delete_Native_TOC_Element(db_object_1.id + db_object_2.id + 1)

        # Next, test that we indeed have precisely one object left:

        # Next, retrieve the ID's. We test that, indeed nothing else is in the test-DB,
        # by testing that the length has to be exactly 1:
        id_list = list(db_Native_TOC_Element.objects.values_list("id", flat=True).order_by("id"))
        id_length = len(id_list)

        # Test if there is actually something in the DB now:
        if not (id_length == 1):
            print(
                "\n ==> RAPPORT <Native_TOC_Element test_delete>: The number of DB-entries was not as we expected!\n"
            )
            print(id_list)
            self.assertIs(True, False)
        else:
            # Then, we are fine:
            self.assertIs(True, True)

        # Done.


@tag("database", "unit", "delete")
class textsplitter_delete_tests(TestCase):
    def test_delete(self):
        """
        Unit test for a write-read operation that ovverwrites an existing DB-item.
        # Parameters: none; # Returns (bool): succes of the text.
        # Author: Christiaan Douma
        """

        # Create a nice example of a textsplitter class. Only pass in just enough information
        # to see if all its children get handled. Do not use labelname, as
        # that one is supposed to be automatically set in the textsplitter-object.
        textpart_object_1 = textpart_textsplitter()
        textpart_object_1.documentname = "Dit is een coole PDF"
        textalinea_1 = textpart_textalinea()
        textalinea_1.summary = "Wat een leuke samenvatting."
        textalinea_1.documentname = "Die komt van een dom document"
        textalinea_2 = textpart_textalinea()
        textalinea_2.summary = "En nog een leuke samenvatting."
        textalinea_2.documentname = "Die komt van een ander dom document"
        textalinea_3 = textpart_textalinea()
        textalinea_3.summary = "En dan een langdradig verhaal"
        textalinea_3.documentname = "Die komt van een kort document"
        textpart_object_1.textalineas = [textalinea_1, textalinea_2, textalinea_3]
        TOC_1 = textpart_Native_TOC_Element()
        TOC_1.cascadelevel = 1
        TOC_1.title = "Wat een leuk hoofdstuk"
        TOC_1.page = 2
        TOC_1.Xpos = 10.0
        TOC_1.Ypos = 11.0
        TOC_1.Zpos = 12.0
        TOC_2 = textpart_Native_TOC_Element()
        TOC_2.cascadelevel = 3
        TOC_2.title = "Wat een dom hoofdstuk"
        TOC_2.page = 4
        TOC_2.Xpos = 20.0
        TOC_2.Ypos = 21.0
        TOC_2.Zpos = 22.0
        textpart_object_1.native_TOC = [TOC_1, TOC_2]
        textpart_object_1.title = textpart_title()
        textpart_object_1.title.documentname = "Title van die coole PDF"
        textpart_object_1.footer = textpart_footer()
        textpart_object_1.footer.documentname = "Footer van die coole PDF"
        textpart_object_1.body = textpart_body()
        textpart_object_1.body.documentname = "Body van die coole PDF"
        textpart_object_1.headlines = textpart_headlines()
        textpart_object_1.headlines.documentname = "Headlines van die coole PDF"
        textpart_object_1.enumeration = textpart_enumeration()
        textpart_object_1.enumeration.documentname = "Enumeration van die coole PDF"
        textpart_object_1.enumeration.last_textline_bigroman = "VII) en dan nog wat"
        textpart_object_1.VERSION = "1.2.3"
        textpart_object_1.ratelimit_timeunit = 0.1
        textpart_object_1.ratelimit_calls = 1
        textpart_object_1.ratelimit_tokens = 2
        textpart_object_1.Costs_price = 0.2
        textpart_object_1.Costs_tokenportion = 3
        textpart_object_1.api_rate_starttime = 0.3
        textpart_object_1.api_rate_currenttime = 0.4
        textpart_object_1.api_rate_currenttokens = 4
        textpart_object_1.api_rate_currentcalls = 5
        textpart_object_1.callcounter = 6
        textpart_object_1.api_totalprice = 0.5
        textpart_object_1.api_wrongcalls_duetomaxwhile = 7
        textpart_object_1.html_visualization = '<html class = "nice">'
        textpart_object_1.MaxSummaryLength = 8
        textpart_object_1.summarization_threshold = 9
        textpart_object_1.UseDummySummary = True
        textpart_object_1.LanguageModel = "gpt-zoveel"
        textpart_object_1.BackendChoice = "Sesamstraat"
        textpart_object_1.LanguageChoice = "Latin"
        textpart_object_1.LanguageTemperature = 0.6
        textpart_object_1.MaxCallRepeat = 10
        textpart_object_1.doc_metadata_author = "Pietje Bell"
        textpart_object_1.doc_metadata_creator = "Drogist Geelman"
        textpart_object_1.doc_metadata_producer = "Paul Velinga"
        textpart_object_1.doc_metadata_subject = "Kattenkwaad"
        textpart_object_1.doc_metadata_title = "Wandelende ramp"
        textpart_object_1.doc_metadata_fullstring = "lees het boek zelf maar"
        textpart_object_1.textclassification = [
            "some stupid classification",
            "another dum classification",
            "a third decision we are not interested in",
        ]

        # Create one more:
        textpart_object_2 = textpart_textsplitter()
        textpart_object_2.documentname = "Dit is een super-irritante PDF"
        textalinea_1 = textpart_textalinea()
        textalinea_1.summary = "Wat een leuke zin."
        textalinea_1.documentname = "Die komt van een leuk document"
        textalinea_2 = textpart_textalinea()
        textalinea_2.summary = "En nog een leuke zooi."
        textalinea_2.documentname = "Die komt van een ander leuk document"
        TOC_1 = textpart_Native_TOC_Element()
        TOC_1.cascadelevel = 5
        TOC_1.title = "Wat een extra leuk hoofdstuk"
        TOC_1.page = 6
        TOC_1.Xpos = 30.0
        TOC_1.Ypos = 31.0
        TOC_1.Zpos = 32.0
        TOC_2 = textpart_Native_TOC_Element()
        TOC_2.cascadelevel = 7
        TOC_2.title = "Wat een extra dom hoofdstuk"
        TOC_2.page = 8
        TOC_2.Xpos = 40.0
        TOC_2.Ypos = 41.0
        TOC_2.Zpos = 42.0
        TOC_3 = textpart_Native_TOC_Element()
        TOC_3.cascadelevel = 9
        TOC_3.title = "Wat een gigantisch dom hoofdstuk"
        TOC_3.page = 10
        TOC_3.Xpos = 50.0
        TOC_3.Ypos = 51.0
        TOC_3.Zpos = 52.0
        textpart_object_2.native_TOC = [TOC_1, TOC_2, TOC_3]
        textpart_object_2.textalineas = [textalinea_1, textalinea_2]
        textpart_object_2.title = textpart_title()
        textpart_object_2.title.documentname = "Title van die irritante PDF"
        textpart_object_2.footer = textpart_footer()
        textpart_object_2.footer.documentname = "Footer van die irritante PDF"
        textpart_object_2.body = textpart_body()
        textpart_object_2.body.documentname = "Body van die irritante PDF"
        textpart_object_2.headlines = textpart_headlines()
        textpart_object_2.headlines.documentname = "Headlines van die irritante PDF"
        textpart_object_2.enumeration = textpart_enumeration()
        textpart_object_2.enumeration.documentname = "Enumeration van die irritante PDF"
        textpart_object_2.enumeration.last_textline_bigroman = "VII) en dan nog wat"
        textpart_object_2.VERSION = "3.4.1"
        textpart_object_2.ratelimit_timeunit = 2.1
        textpart_object_2.ratelimit_calls = 11
        textpart_object_2.ratelimit_tokens = 12
        textpart_object_2.Costs_price = 2.2
        textpart_object_2.Costs_tokenportion = 13
        textpart_object_2.api_rate_starttime = 2.3
        textpart_object_2.api_rate_currenttime = 2.4
        textpart_object_2.api_rate_currenttokens = 14
        textpart_object_2.api_rate_currentcalls = 15
        textpart_object_2.callcounter = 16
        textpart_object_2.api_totalprice = 2.5
        textpart_object_2.api_wrongcalls_duetomaxwhile = 17
        textpart_object_2.html_visualization = '<html class = "stupid">'
        textpart_object_2.MaxSummaryLength = 18
        textpart_object_2.summarization_threshold = 19
        textpart_object_2.UseDummySummary = False
        textpart_object_2.LanguageModel = "gpt-zozo"
        textpart_object_2.BackendChoice = "Pino"
        textpart_object_2.LanguageChoice = "Greek"
        textpart_object_2.LanguageTemperature = 2.6
        textpart_object_2.MaxCallRepeat = 20
        textpart_object_2.doc_metadata_author = "Will Verdrag"
        textpart_object_2.doc_metadata_creator = "Halt Arratay"
        textpart_object_2.doc_metadata_producer = "Baron Arald"
        textpart_object_2.doc_metadata_subject = "Avonturen"
        textpart_object_2.doc_metadata_title = "The Ranger's apprentice"
        textpart_object_2.doc_metadata_fullstring = "Koop het boek. Supergoed!!!"
        textpart_object_2.textclassification = [
            "some stupid idiotic classification",
            "another idiotic dum classification",
        ]

        # Write both objects to the database:
        db_object_1 = newwrite_textsplitter(textpart_object_1)
        db_object_2 = newwrite_textsplitter(textpart_object_2)

        # Now, delete one of them:
        delete_textsplitter(db_object_1.id)

        # Next, attempt to delete something that we know does not exist:
        delete_textsplitter(db_object_1.id + db_object_2.id + 1)

        # Next, test that we indeed have precisely one object left:

        # Next, retrieve the ID's. We test that, indeed nothing else is in the test-DB,
        # by testing that the length has to be exactly 1:
        id_list = list(db_textsplitter.objects.values_list("id", flat=True).order_by("id"))
        id_length = len(id_list)

        # Eliminate presence of default foreign key object:
        for k in range(0, id_length):
            Index = id_length - k - 1
            if load_textsplitter(id_list[Index]).labelname == "default_foreign_key_object":
                id_list.pop(Index)
        id_length = len(id_list)

        # Also test for textparts:
        id_list_textpart = list(db_textpart.objects.values_list("id", flat=True).order_by("id"))
        id_length_textpart = len(id_list_textpart)

        # Eliminate presence of default foreign key object:
        for k in range(0, id_length_textpart):
            Index = id_length_textpart - k - 1
            if load_textpart(id_list_textpart[Index]).labelname == "default_foreign_key_object":
                id_list_textpart.pop(Index)
        id_length_textpart = len(id_list_textpart)

        # Also test for titles:
        id_list_title = list(db_title.objects.values_list("id", flat=True).order_by("id"))
        id_length_title = len(id_list_title)

        # Eliminate presence of default foreign key object:
        for k in range(0, id_length_title):
            Index = id_length_title - k - 1
            if load_title(id_list_title[Index]).labelname == "default_foreign_key_object":
                id_list_title.pop(Index)
        id_length_title = len(id_list_title)

        # Also test for footers:
        id_list_footer = list(db_footer.objects.values_list("id", flat=True).order_by("id"))
        id_length_footer = len(id_list_footer)

        # Eliminate presence of default foreign key object:
        for k in range(0, id_length_footer):
            Index = id_length_footer - k - 1
            if load_footer(id_list_footer[Index]).labelname == "default_foreign_key_object":
                id_list_footer.pop(Index)
        id_length_footer = len(id_list_footer)

        # Also test for bodys:
        id_list_body = list(db_body.objects.values_list("id", flat=True).order_by("id"))
        id_length_body = len(id_list_body)

        # Eliminate presence of default foreign key object:
        for k in range(0, id_length_body):
            Index = id_length_body - k - 1
            if load_body(id_list_body[Index]).labelname == "default_foreign_key_object":
                id_list_body.pop(Index)
        id_length_body = len(id_list_body)

        # Also test for headliness:
        id_list_headlines = list(db_headlines.objects.values_list("id", flat=True).order_by("id"))
        id_length_headlines = len(id_list_headlines)

        # Eliminate presence of default foreign key object:
        for k in range(0, id_length_headlines):
            Index = id_length_headlines - k - 1
            if load_headlines(id_list_headlines[Index]).labelname == "default_foreign_key_object":
                id_list_headlines.pop(Index)
        id_length_headlines = len(id_list_headlines)

        # Also test for enumerations:
        id_list_enumeration = list(
            db_enumeration.objects.values_list("id", flat=True).order_by("id")
        )
        id_length_enumeration = len(id_list_enumeration)

        # Eliminate presence of default foreign key object:
        for k in range(0, id_length_enumeration):
            Index = id_length_enumeration - k - 1
            if (
                load_enumeration(id_list_enumeration[Index]).labelname
                == "default_foreign_key_object"
            ):
                id_list_enumeration.pop(Index)
        id_length_enumeration = len(id_list_enumeration)

        # Also test for textalineas:
        id_list_textalinea = list(db_textalinea.objects.values_list("id", flat=True).order_by("id"))
        id_length_textalinea = len(id_list_textalinea)

        # Eliminate presence of default foreign key object:
        for k in range(0, id_length_textalinea):
            Index = id_length_textalinea - k - 1
            if load_textalinea(id_list_textalinea[Index]).labelname == "default_foreign_key_object":
                id_list_textalinea.pop(Index)
        id_length_textalinea = len(id_list_textalinea)

        # Also test for Native_TOC_Elements:
        id_list_Native_TOC_Element = list(
            db_Native_TOC_Element.objects.values_list("id", flat=True).order_by("id")
        )
        id_length_Native_TOC_Element = len(id_list_Native_TOC_Element)

        # Also test for breakdown_decisions:
        id_list_breakdown_decisions = list(
            db_breakdown_decisions.objects.values_list("id", flat=True).order_by("id")
        )
        id_length_breakdown_decisions = len(id_list_breakdown_decisions)

        # Test if there is actually something in the DB now:
        if not (
            (id_length == 1)
            and (id_length_textpart == 8)
            and (id_length_title == 1)
            and (id_length_footer == 1)
            and (id_length_body == 1)
            and (id_length_headlines == 1)
            and (id_length_enumeration == 1)
            and (id_length_textalinea == 2)
            and (id_length_Native_TOC_Element == 3)
            and (id_length_breakdown_decisions == 2)
        ):
            print(
                "\n ==> RAPPORT <textsplitter test_delete>: The number of DB-entries was not as we expected!\n"
            )
            print(id_list)
            print(id_list_textpart)
            print(id_list_title)
            print(id_list_footer)
            print(id_list_body)
            print(id_list_headlines)
            print(id_list_enumeration)
            print(id_list_textalinea)
            print(id_list_Native_TOC_Element)
            print(id_list_breakdown_decisions)
            self.assertIs(True, False)
        else:
            # Then, we are fine:
            self.assertIs(True, True)

            # Done
