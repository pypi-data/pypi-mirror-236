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
from .overwrites import overwrite_fontregion
from .overwrites import overwrite_lineregion
from .overwrites import overwrite_textpart
from .overwrites import overwrite_title
from .overwrites import overwrite_body
from .overwrites import overwrite_footer
from .overwrites import overwrite_headlines
from .overwrites import overwrite_enumeration
from .overwrites import overwrite_textalinea
from .overwrites import overwrite_textsplitter
from .overwrites import overwrite_Native_TOC_Element

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
@tag("database", "unit", "unhappy")
class fontregion_unhappy_tests(TestCase):
    def test_load_nonexistent(self):
        """
        Unit test trying to look up a model that does not exist:
        # Parameters: none; # Returns (bool): succes of the text.
        # Author: Christiaan Douma
        """

        # Begin by finding all id's:
        id_list = list(db_fontregion.objects.values_list("id", flat=True).order_by("id"))
        id_length = len(id_list)

        # Check that we have indeed zero length:
        if not (id_length == 0):
            print(
                "\n ==> RAPPORT <fontregion test_overwrite_nonexistent>: At the start of the test, the test-DB should always be empty!\n"
            )
            self.assertIs(True, False)
        else:
            # Attempt to load something that we now know is impossible:
            textpart_object = load_fontregion(1)

            # Check if we indeed get a negative cascade back:
            Answer = textpart_object.cascadelevel == -1

            # perform the test:
            if not Answer:
                print(
                    "\n ==> RAPPORT <fontregion test_load_nonexistent>: We did not obtain a -1 cascadelevel, as we should for looking up a nonexistent item.\n"
                )
            self.assertIs(Answer, True)

        # Done.

    def test_overwrite_nonexistent(self):
        """
        Unit test trying to overwrite a model that does not exist:
        # Parameters: none; # Returns (bool): succes of the text.
        # Author: Christiaan Douma
        """

        # Begin by finding all id's:
        id_list = list(db_fontregion.objects.values_list("id", flat=True).order_by("id"))
        id_length = len(id_list)

        # Check that we have indeed zero length:
        if not (id_length == 0):
            print(
                "\n ==> RAPPORT <fontregion test_overwrite_nonexistent>: At the start of the test, the test-DB should always be empty!\n"
            )
            self.assertIs(True, False)
        else:
            # Create a nice example of a textpart fontregion:
            textpart_object = textpart_fontregion()
            textpart_object.left = 2.21
            textpart_object.right = 4.41
            textpart_object.value = 3.31
            textpart_object.frequency = 0.89
            textpart_object.cascadelevel = 2
            textpart_object.isregular = True

            # Attempt to overwrite something that we know does not exist:
            db_object = overwrite_fontregion(1, textpart_object)

            # Check that we still have an empty DB:
            new_id_list = list(db_fontregion.objects.values_list("id", flat=True).order_by("id"))
            new_id_length = len(new_id_list)

            # Check that we go a bad object returned:
            if not (db_object.cascadelevel == -1):
                Answer = False

            if not (new_id_length == 0):
                print(
                    "\n ==> RAPPORT <fontregion test_overwrite_nonexistent>: overwriting a nonexistent item should not do anything!\n"
                )
                print(new_id_list)
                self.assertIs(True, False)
            else:
                self.assertIs(True, True)

        # Done.


@tag("database", "unit", "unhappy")
class lineregion_unhappy_tests(TestCase):
    def test_load_nonexistent(self):
        """
        Unit test trying to look up a model that does not exist:
        # Parameters: none; # Returns (bool): succes of the text.
        # Author: Christiaan Douma
        """

        # Begin by finding all id's:
        id_list = list(db_lineregion.objects.values_list("id", flat=True).order_by("id"))
        id_length = len(id_list)

        # Check that we have indeed zero length:
        if not (id_length == 0):
            print(
                "\n ==> RAPPORT <lineregion test_overwrite_nonexistent>: At the start of the test, the test-DB should always be empty!\n"
            )
            self.assertIs(True, False)
        else:
            # Attempt to load something that we now know is impossible:
            textpart_object = load_lineregion(1)

            # Check if we indeed get a negative cascade back:
            Answer = textpart_object.frequency < -0.5

            # perform the test:
            if not Answer:
                print(
                    "\n ==> RAPPORT <lineregion test_load_nonexistent>: We did not obtain a negative frequency, as we should for looking up a nonexistent item.\n"
                )
            self.assertIs(Answer, True)

        # Done.

    def test_overwrite_nonexistent(self):
        """
        Unit test trying to overwrite a model that does not exist:
        # Parameters: none; # Returns (bool): succes of the text.
        # Author: Christiaan Douma
        """

        # Begin by finding all id's:
        id_list = list(db_lineregion.objects.values_list("id", flat=True).order_by("id"))
        id_length = len(id_list)

        # Check that we have indeed zero length:
        if not (id_length == 0):
            print(
                "\n ==> RAPPORT <lineregion test_overwrite_nonexistent>: At the start of the test, the test-DB should always be empty!\n"
            )
            self.assertIs(True, False)
        else:
            # Create a nice example of a textpart lineregion:
            textpart_object = textpart_lineregion()
            textpart_object.left = 2.21
            textpart_object.right = 4.41
            textpart_object.value = 3.31
            textpart_object.frequency = 0.89
            textpart_object.isregular = True
            textpart_object.issmall = True
            textpart_object.isbig = True
            textpart_object.iszero = True
            textpart_object.isvalid = True

            # Attempt to overwrite something that we know does not exist:
            db_object = overwrite_lineregion(1, textpart_object)

            # Check that we still have an empty DB:
            new_id_list = list(db_lineregion.objects.values_list("id", flat=True).order_by("id"))
            new_id_length = len(new_id_list)

            # Check that we go a bad object returned:
            if not (db_object.frequency < -0.5):
                Answer = False

            if not (new_id_length == 0):
                print(
                    "\n ==> RAPPORT <lineregion test_overwrite_nonexistent>: overwriting a nonexistent item should not do anything!\n"
                )
                print(new_id_list)
                self.assertIs(True, False)
            else:
                self.assertIs(True, True)

        # Done.


@tag("database", "unit", "unhappy")
class textpart_unhappy_tests(TestCase):
    def test_load_nonexistent(self):
        """
        Unit test trying to look up a model that does not exist:
        # Parameters: none; # Returns (bool): succes of the text.
        # Author: Christiaan Douma
        """

        # Begin by finding all id's:
        id_list = list(db_textpart.objects.values_list("id", flat=True).order_by("id"))
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

        # Check that we have indeed zero length:
        if (
            not (id_length == 0)
            and (id_length_fontregion == 0)
            and (id_length_lineregion == 0)
            and (id_length_readingline == 0)
            and (id_length_readinghistogram == 0)
        ):
            print(
                "\n ==> RAPPORT <textpart test_load_nonexistent>: At the start of the test, the test-DB should always be empty!\n"
            )
            self.assertIs(True, False)
        else:
            # Attempt to load something that we now know is impossible:
            textpart_object = load_textpart(1)

            # Check if we indeed get a negative cascade back:
            Answer = "WRONG_OBJECT" in textpart_object.labelname

            # perform the test:
            if not Answer:
                print(
                    "\n ==> RAPPORT <textpart test_load_nonexistent>: We did not obtain a <WRONG_OBJECT> labelname, as we should for looking up a nonexistent item.\n"
                )
            self.assertIs(Answer, True)

        # Done.

    def test_overwrite_nonexistent(self):
        """
        Unit test trying to overwrite a model that does not exist:
        # Parameters: none; # Returns (bool): succes of the text.
        # Author: Christiaan Douma
        """

        # Begin by finding all id's:
        id_list = list(db_textpart.objects.values_list("id", flat=True).order_by("id"))
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

        # Check that we have indeed zero length:
        if (
            not (id_length == 0)
            and (id_length_fontregion == 0)
            and (id_length_lineregion == 0)
            and (id_length_readingline == 0)
            and (id_length_readinghistogram == 0)
        ):
            print(
                "\n ==> RAPPORT <textpart test_overwrite_nonexistent>: At the start of the test, the test-DB should always be empty!\n"
            )
            self.assertIs(True, False)
        else:
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
            textpart_object_1.textcontent = [
                "my fisrt textline",
                "another textline",
                "Now I get bored",
            ]
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
            textpart_object_1.fontsizeHist_perline = [
                [11.0, 21.0],
                [1.1, 2.1, 3.1],
                [1.1, 2.1, 3.1],
            ]
            textpart_object_1.whitespaceHist_perline = [
                [12.0, 22.0],
                [1.2, 2.2, 3.1],
                [1.2, 2.2, 3.2],
            ]

            # Attempt to overwrite something that we know does not exist:
            db_object = overwrite_textpart(1, textpart_object_1)

            # Check that we still have an empty DB:
            new_id_list = list(db_textpart.objects.values_list("id", flat=True).order_by("id"))
            new_id_length = len(new_id_list)

            # Eliminate presence of default foreign key object:
            for k in range(0, new_id_length):
                Index = new_id_length - k - 1
                if load_textpart(new_id_list[Index]).labelname == "default_foreign_key_object":
                    new_id_list.pop(Index)
            new_id_length = len(new_id_list)

            # Also check fontregions:
            new_id_list_fontregion = list(
                db_fontregion.objects.values_list("id", flat=True).order_by("id")
            )
            new_id_length_fontregion = len(new_id_list_fontregion)

            # Also test for lineregions:
            new_id_list_lineregion = list(
                db_lineregion.objects.values_list("id", flat=True).order_by("id")
            )
            new_id_length_lineregion = len(new_id_list_lineregion)

            # Also test for readinglines:
            new_id_list_readingline = list(
                db_readingline.objects.values_list("id", flat=True).order_by("id")
            )
            new_id_length_readingline = len(new_id_list_readingline)

            # Also test for readinghistograms:
            new_id_list_readinghistogram = list(
                db_readinghistogram.objects.values_list("id", flat=True).order_by("id")
            )
            new_id_length_readinghistogram = len(new_id_list_readinghistogram)

            # Check that we got a bad object returned:
            if not ("WRONG_OBJECT" in db_object.labelname):
                Answer = False

            if (
                not (new_id_length == 0)
                and (new_id_length_fontregion == 0)
                and (new_id_length_lineregion == 0)
                and (new_id_length_readingline == 0)
                and (new_id_length_readinghistogram == 0)
            ):
                print(
                    "\n ==> RAPPORT <textpart test_overwrite_nonexistent>: overwriting a nonexistent item should not do anything!\n"
                )
                print(new_id_list)
                print(new_id_length_fontregion)
                print(new_id_length_lineregion)
                print(new_id_length_readingline)
                print(new_id_length_readinghistogram)
                self.assertIs(True, False)
            else:
                self.assertIs(True, True)

        # Done.


@tag("database", "unit", "unhappy")
class title_unhappy_tests(TestCase):
    def test_load_nonexistent(self):
        """
        Unit test trying to look up a model that does not exist:
        # Parameters: none; # Returns (bool): succes of the text.
        # Author: Christiaan Douma
        """

        # Begin by finding all id's:
        id_list = list(db_title.objects.values_list("id", flat=True).order_by("id"))
        id_length = len(id_list)

        # Also test for textparts:
        id_list_textpart = list(db_textpart.objects.values_list("id", flat=True).order_by("id"))
        id_length_textpart = len(id_list_textpart)

        # Check that we have indeed zero length:
        if not (id_length == 0) and (id_length_textpart == 0):
            print(
                "\n ==> RAPPORT <title test_load_nonexistent>: At the start of the test, the test-DB should always be empty!\n"
            )
            self.assertIs(True, False)
        else:
            # Attempt to load something that we now know is impossible:
            textpart_object = load_title(1)

            # Check if we indeed get a negative cascade back:
            Answer = "WRONG_OBJECT" in textpart_object.labelname

            # perform the test:
            if not Answer:
                print(
                    "\n ==> RAPPORT <title test_load_nonexistent>: We did not obtain a <WRONG_OBJECT> labelname, as we should for looking up a nonexistent item.\n"
                )
            self.assertIs(Answer, True)

        # Done.

    def test_overwrite_nonexistent(self):
        """
        Unit test trying to overwrite a model that does not exist:
        # Parameters: none; # Returns (bool): succes of the text.
        # Author: Christiaan Douma
        """

        # Begin by finding all id's:
        id_list = list(db_title.objects.values_list("id", flat=True).order_by("id"))
        id_length = len(id_list)

        # Also test for textparts:
        id_list_textpart = list(db_textpart.objects.values_list("id", flat=True).order_by("id"))
        id_length_textpart = len(id_list_textpart)

        # Check that we have indeed zero length:
        if not (id_length == 0) and (id_length_textpart == 0):
            print(
                "\n ==> RAPPORT <title test_overwrite_nonexistent>: At the start of the test, the test-DB should always be empty!\n"
            )
            self.assertIs(True, False)
        else:
            # Create a nice example of a title class. Only pass in just enough information
            # to see if the parent-class textpart gets handled. Do not use labelname, as
            # that one is supposed to be automatically set in the title-object.
            textpart_object = textpart_title()
            textpart_object.documentname = "This is a test-object for a title-class"  # ATTENTION: This is to prove that we indeed can dig one level deeper.

            # Attempt to overwrite something that we know does not exist:
            db_object = overwrite_title(1, textpart_object)

            # Check that we still have an empty DB:
            new_id_list = list(db_title.objects.values_list("id", flat=True).order_by("id"))
            new_id_length = len(new_id_list)

            # Eliminate presence of default foreign key object:
            for k in range(0, new_id_length):
                Index = new_id_length - k - 1
                if load_title(new_id_list[Index]).labelname == "default_foreign_key_object":
                    new_id_list.pop(Index)
            new_id_length = len(new_id_list)

            # Also check textparts:
            new_id_list_textpart = list(
                db_textpart.objects.values_list("id", flat=True).order_by("id")
            )
            new_id_length_textpart = len(new_id_list_textpart)

            # Eliminate presence of default foreign key object:
            for k in range(0, new_id_length_textpart):
                Index = new_id_length_textpart - k - 1
                if (
                    load_textpart(new_id_list_textpart[Index]).labelname
                    == "default_foreign_key_object"
                ):
                    new_id_list_textpart.pop(Index)
            new_id_length_textpart = len(new_id_list_textpart)

            # Check that we did not write anything:
            if not (new_id_length == 0) and (new_id_length_textpart == 0):
                print(
                    "\n ==> RAPPORT <textpart test_overwrite_nonexistent>: overwriting a nonexistent item should not do anything!\n"
                )
                print(new_id_list)
                print(new_id_length_textpart)
                self.assertIs(True, False)
            else:
                self.assertIs(True, True)

        # Done.


@tag("database", "unit", "unhappy")
class body_unhappy_tests(TestCase):
    def test_load_nonexistent(self):
        """
        Unit test trying to look up a model that does not exist:
        # Parameters: none; # Returns (bool): succes of the text.
        # Author: Christiaan Douma
        """

        # Begin by finding all id's:
        id_list = list(db_body.objects.values_list("id", flat=True).order_by("id"))
        id_length = len(id_list)

        # Also test for textparts:
        id_list_textpart = list(db_textpart.objects.values_list("id", flat=True).order_by("id"))
        id_length_textpart = len(id_list_textpart)

        # Check that we have indeed zero length:
        if not (id_length == 0) and (id_length_textpart == 0):
            print(
                "\n ==> RAPPORT <body test_load_nonexistent>: At the start of the test, the test-DB should always be empty!\n"
            )
            self.assertIs(True, False)
        else:
            # Attempt to load something that we now know is impossible:
            textpart_object = load_body(1)

            # Check if we indeed get a negative cascade back:
            Answer = "WRONG_OBJECT" in textpart_object.labelname

            # perform the test:
            if not Answer:
                print(
                    "\n ==> RAPPORT <body test_load_nonexistent>: We did not obtain a <WRONG_OBJECT> labelname, as we should for looking up a nonexistent item.\n"
                )
            self.assertIs(Answer, True)

        # Done.

    def test_overwrite_nonexistent(self):
        """
        Unit test trying to overwrite a model that does not exist:
        # Parameters: none; # Returns (bool): succes of the text.
        # Author: Christiaan Douma
        """

        # Begin by finding all id's:
        id_list = list(db_body.objects.values_list("id", flat=True).order_by("id"))
        id_length = len(id_list)

        # Also test for textparts:
        id_list_textpart = list(db_textpart.objects.values_list("id", flat=True).order_by("id"))
        id_length_textpart = len(id_list_textpart)

        # Check that we have indeed zero length:
        if not (id_length == 0) and (id_length_textpart == 0):
            print(
                "\n ==> RAPPORT <body test_overwrite_nonexistent>: At the start of the test, the test-DB should always be empty!\n"
            )
            self.assertIs(True, False)
        else:
            # Create a nice example of a body class. Only pass in just enough information
            # to see if the parent-class textpart gets handled. Do not use labelname, as
            # that one is supposed to be automatically set in the body-object.
            textpart_object = textpart_body()
            textpart_object.documentname = "This is a test-object for a body-class"  # ATTENTION: This is to prove that we indeed can dig one level deeper.

            # Attempt to overwrite something that we know does not exist:
            db_object = overwrite_body(1, textpart_object)

            # Check that we still have an empty DB:
            new_id_list = list(db_body.objects.values_list("id", flat=True).order_by("id"))
            new_id_length = len(new_id_list)

            # Eliminate presence of default foreign key object:
            for k in range(0, new_id_length):
                Index = new_id_length - k - 1
                if load_body(new_id_list[Index]).labelname == "default_foreign_key_object":
                    new_id_list.pop(Index)
            new_id_length = len(new_id_list)

            # Also check textparts:
            new_id_list_textpart = list(
                db_textpart.objects.values_list("id", flat=True).order_by("id")
            )
            new_id_length_textpart = len(new_id_list_textpart)

            # Eliminate presence of default foreign key object:
            for k in range(0, new_id_length_textpart):
                Index = new_id_length_textpart - k - 1
                if (
                    load_textpart(new_id_list_textpart[Index]).labelname
                    == "default_foreign_key_object"
                ):
                    new_id_list_textpart.pop(Index)
            new_id_length_textpart = len(new_id_list_textpart)

            # Check that we did not write anything:
            if not (new_id_length == 0) and (new_id_length_textpart == 0):
                print(
                    "\n ==> RAPPORT <textpart test_overwrite_nonexistent>: overwriting a nonexistent item should not do anything!\n"
                )
                print(new_id_list)
                print(new_id_length_textpart)
                self.assertIs(True, False)
            else:
                self.assertIs(True, True)

        # Done.


@tag("database", "unit", "unhappy")
class footer_unhappy_tests(TestCase):
    def test_load_nonexistent(self):
        """
        Unit test trying to look up a model that does not exist:
        # Parameters: none; # Returns (bool): succes of the text.
        # Author: Christiaan Douma
        """

        # Begin by finding all id's:
        id_list = list(db_footer.objects.values_list("id", flat=True).order_by("id"))
        id_length = len(id_list)

        # Also test for textparts:
        id_list_textpart = list(db_textpart.objects.values_list("id", flat=True).order_by("id"))
        id_length_textpart = len(id_list_textpart)

        # Check that we have indeed zero length:
        if not (id_length == 0) and (id_length_textpart == 0):
            print(
                "\n ==> RAPPORT <footer test_load_nonexistent>: At the start of the test, the test-DB should always be empty!\n"
            )
            self.assertIs(True, False)
        else:
            # Attempt to load something that we now know is impossible:
            textpart_object = load_footer(1)

            # Check if we indeed get a negative cascade back:
            Answer = "WRONG_OBJECT" in textpart_object.labelname

            # perform the test:
            if not Answer:
                print(
                    "\n ==> RAPPORT <footer test_load_nonexistent>: We did not obtain a <WRONG_OBJECT> labelname, as we should for looking up a nonexistent item.\n"
                )
            self.assertIs(Answer, True)

        # Done.

    def test_overwrite_nonexistent(self):
        """
        Unit test trying to overwrite a model that does not exist:
        # Parameters: none; # Returns (bool): succes of the text.
        # Author: Christiaan Douma
        """

        # Begin by finding all id's:
        id_list = list(db_footer.objects.values_list("id", flat=True).order_by("id"))
        id_length = len(id_list)

        # Also test for textparts:
        id_list_textpart = list(db_textpart.objects.values_list("id", flat=True).order_by("id"))
        id_length_textpart = len(id_list_textpart)

        # Check that we have indeed zero length:
        if not (id_length == 0) and (id_length_textpart == 0):
            print(
                "\n ==> RAPPORT <footer test_overwrite_nonexistent>: At the start of the test, the test-DB should always be empty!\n"
            )
            self.assertIs(True, False)
        else:
            # Create a nice example of a footer class. Only pass in just enough information
            # to see if the parent-class textpart gets handled. Do not use labelname, as
            # that one is supposed to be automatically set in the footer-object.
            textpart_object = textpart_footer()
            textpart_object.documentname = "This is a test-object for a footer-class"  # ATTENTION: This is to prove that we indeed can dig one level deeper.

            # Attempt to overwrite something that we know does not exist:
            db_object = overwrite_footer(1, textpart_object)

            # Check that we still have an empty DB:
            new_id_list = list(db_footer.objects.values_list("id", flat=True).order_by("id"))
            new_id_length = len(new_id_list)

            # Eliminate presence of default foreign key object:
            for k in range(0, new_id_length):
                Index = new_id_length - k - 1
                if load_footer(new_id_list[Index]).labelname == "default_foreign_key_object":
                    new_id_list.pop(Index)
            new_id_length = len(new_id_list)

            # Also check textparts:
            new_id_list_textpart = list(
                db_textpart.objects.values_list("id", flat=True).order_by("id")
            )
            new_id_length_textpart = len(new_id_list_textpart)

            # Eliminate presence of default foreign key object:
            for k in range(0, new_id_length_textpart):
                Index = new_id_length_textpart - k - 1
                if (
                    load_textpart(new_id_list_textpart[Index]).labelname
                    == "default_foreign_key_object"
                ):
                    new_id_list_textpart.pop(Index)
            new_id_length_textpart = len(new_id_list_textpart)

            # Check that we did not write anything:
            if not (new_id_length == 0) and (new_id_length_textpart == 0):
                print(
                    "\n ==> RAPPORT <textpart test_overwrite_nonexistent>: overwriting a nonexistent item should not do anything!\n"
                )
                print(new_id_list)
                print(new_id_length_textpart)
                self.assertIs(True, False)
            else:
                self.assertIs(True, True)

        # Done.


@tag("database", "unit", "unhappy")
class headlines_unhappy_tests(TestCase):
    def test_load_nonexistent(self):
        """
        Unit test trying to look up a model that does not exist:
        # Parameters: none; # Returns (bool): succes of the text.
        # Author: Christiaan Douma
        """

        # Begin by finding all id's:
        id_list = list(db_headlines.objects.values_list("id", flat=True).order_by("id"))
        id_length = len(id_list)

        # Also test for textparts:
        id_list_textpart = list(db_textpart.objects.values_list("id", flat=True).order_by("id"))
        id_length_textpart = len(id_list_textpart)

        # Also for the hierarchy:
        id_list_hierarchy = list(
            db_headlines_hierarchy.objects.values_list("id", flat=True).order_by("id")
        )
        id_length_hierarchy = len(id_list_hierarchy)

        # Check that we have indeed zero length:
        if not (id_length == 0) and (id_length_textpart == 0) and (id_length_hierarchy == 0):
            print(
                "\n ==> RAPPORT <headlines test_load_nonexistent>: At the start of the test, the test-DB should always be empty!\n"
            )
            self.assertIs(True, False)
        else:
            # Attempt to load something that we now know is impossible:
            textpart_object = load_headlines(1)

            # Check if we indeed get a negative cascade back:
            Answer = "WRONG_OBJECT" in textpart_object.labelname

            # perform the test:
            if not Answer:
                print(
                    "\n ==> RAPPORT <headlines test_load_nonexistent>: We did not obtain a <WRONG_OBJECT> labelname, as we should for looking up a nonexistent item.\n"
                )
            self.assertIs(Answer, True)

        # Done.

    def test_overwrite_nonexistent(self):
        """
        Unit test trying to overwrite a model that does not exist:
        # Parameters: none; # Returns (bool): succes of the text.
        # Author: Christiaan Douma
        """

        # Begin by finding all id's:
        id_list = list(db_headlines.objects.values_list("id", flat=True).order_by("id"))
        id_length = len(id_list)

        # Also test for textparts:
        id_list_textpart = list(db_textpart.objects.values_list("id", flat=True).order_by("id"))
        id_length_textpart = len(id_list_textpart)

        # Also for the hierarchy:
        id_list_hierarchy = list(
            db_headlines_hierarchy.objects.values_list("id", flat=True).order_by("id")
        )
        id_length_hierarchy = len(id_list_hierarchy)

        # Check that we have indeed zero length:
        if not (id_length == 0) and (id_length_textpart == 0) and (id_length_hierarchy == 0):
            print(
                "\n ==> RAPPORT <headlines test_overwrite_nonexistent>: At the start of the test, the test-DB should always be empty!\n"
            )
            self.assertIs(True, False)
        else:
            # Create a nice example of a headlines class. Only pass in just enough information
            # to see if the parent-class textpart gets handled. Do not use labelname, as
            # that one is supposed to be automatically set in the headlines-object.
            textpart_object = textpart_headlines()
            textpart_object.documentname = "This is a test-object for a headlines-class"  # ATTENTION: This is to prove that we indeed can dig one level deeper.
            textpart_object.hierarchy = [
                textpart_enum_type.BIGROMAN,
                textpart_enum_type.DIGIT,
                textpart_enum_type.SMALLLETTER,
            ]

            # Attempt to overwrite something that we know does not exist:
            db_object = overwrite_headlines(1, textpart_object)

            # Check that we still have an empty DB:
            new_id_list = list(db_headlines.objects.values_list("id", flat=True).order_by("id"))
            new_id_length = len(new_id_list)

            # Also check textparts:
            new_id_list_textpart = list(
                db_textpart.objects.values_list("id", flat=True).order_by("id")
            )
            new_id_length_textpart = len(new_id_list_textpart)

            # Eliminate presence of default foreign key object:
            for k in range(0, new_id_length):
                Index = new_id_length - k - 1
                if load_headlines(new_id_list[Index]).labelname == "default_foreign_key_object":
                    new_id_list.pop(Index)
            new_id_length = len(new_id_list)

            # Eliminate presence of default foreign key object:
            for k in range(0, new_id_length_textpart):
                Index = new_id_length_textpart - k - 1
                if (
                    load_textpart(new_id_list_textpart[Index]).labelname
                    == "default_foreign_key_object"
                ):
                    new_id_list_textpart.pop(Index)
            new_id_length_textpart = len(new_id_list_textpart)

            # Also for the hierarchy:
            new_id_list_hierarchy = list(
                db_headlines_hierarchy.objects.values_list("id", flat=True).order_by("id")
            )
            new_id_length_hierarchy = len(new_id_list_hierarchy)

            # Check that we did not write anything:
            if (
                not (new_id_length == 0)
                and (new_id_length_textpart == 0)
                and (new_id_length_hierarchy == 0)
            ):
                print(
                    "\n ==> RAPPORT <textpart test_overwrite_nonexistent>: overwriting a nonexistent item should not do anything!\n"
                )
                print(new_id_list)
                print(new_id_length_textpart)
                self.assertIs(True, False)
            else:
                self.assertIs(True, True)

        # Done.


@tag("database", "unit", "unhappy")
class enumeration_unhappy_tests(TestCase):
    def test_load_nonexistent(self):
        """
        Unit test trying to look up a model that does not exist:
        # Parameters: none; # Returns (bool): succes of the text.
        # Author: Christiaan Douma
        """

        # Begin by finding all id's:
        id_list = list(db_enumeration.objects.values_list("id", flat=True).order_by("id"))
        id_length = len(id_list)

        # Also test for textparts:
        id_list_textpart = list(db_textpart.objects.values_list("id", flat=True).order_by("id"))
        id_length_textpart = len(id_list_textpart)

        # Also for the hierarchy:
        id_list_hierarchy = list(
            db_enumeration_hierarchy.objects.values_list("id", flat=True).order_by("id")
        )
        id_length_hierarchy = len(id_list_hierarchy)

        # Check that we have indeed zero length:
        if not (id_length == 0) and (id_length_textpart == 0) and (id_length_hierarchy == 0):
            print(
                "\n ==> RAPPORT <enumeration test_load_nonexistent>: At the start of the test, the test-DB should always be empty!\n"
            )
            self.assertIs(True, False)
        else:
            # Attempt to load something that we now know is impossible:
            textpart_object = load_enumeration(1)

            # Check if we indeed get a negative cascade back:
            Answer = "WRONG_OBJECT" in textpart_object.labelname

            # perform the test:
            if not Answer:
                print(
                    "\n ==> RAPPORT <enumeration test_load_nonexistent>: We did not obtain a <WRONG_OBJECT> labelname, as we should for looking up a nonexistent item.\n"
                )
            self.assertIs(Answer, True)

        # Done.

    def test_overwrite_nonexistent(self):
        """
        Unit test trying to overwrite a model that does not exist:
        # Parameters: none; # Returns (bool): succes of the text.
        # Author: Christiaan Douma
        """

        # Begin by finding all id's:
        id_list = list(db_enumeration.objects.values_list("id", flat=True).order_by("id"))
        id_length = len(id_list)

        # Also test for textparts:
        id_list_textpart = list(db_textpart.objects.values_list("id", flat=True).order_by("id"))
        id_length_textpart = len(id_list_textpart)

        # Also for the hierarchy:
        id_list_hierarchy = list(
            db_enumeration_hierarchy.objects.values_list("id", flat=True).order_by("id")
        )
        id_length_hierarchy = len(id_list_hierarchy)

        # Check that we have indeed zero length:
        if not (id_length == 0) and (id_length_textpart == 0) and (id_length_hierarchy == 0):
            print(
                "\n ==> RAPPORT <enumeration test_overwrite_nonexistent>: At the start of the test, the test-DB should always be empty!\n"
            )
            self.assertIs(True, False)
        else:
            # Create a nice example of a enumeration class. Only pass in just enough information
            # to see if the parent-class textpart gets handled. Do not use labelname, as
            # that one is supposed to be automatically set in the enumeration-object.
            textpart_object = textpart_enumeration()
            textpart_object.documentname = "This is a test-object for a enumeration-class"  # ATTENTION: This is to prove that we indeed can dig one level deeper.
            textpart_object.hierarchy = [
                textpart_enum_type.BIGROMAN,
                textpart_enum_type.DIGIT,
                textpart_enum_type.SMALLLETTER,
            ]
            textpart_object.last_enumtype_index = 1
            textpart_object.this_enumtype_index = 2
            textpart_object.last_textline_bigroman = "IX. en dan nog wat"
            textpart_object.last_textline_smallroman = "vii) komt er nog wat van?"
            textpart_object.last_textline_bigletter = "F) en nog iets"
            textpart_object.last_textline_smallletter = "(a) gaat zo nog even door"
            textpart_object.last_textline_digit = "3) en zo voort"
            textpart_object.last_textline_signmark = "– ta ta ta"

            # Attempt to overwrite something that we know does not exist:
            db_object = overwrite_enumeration(1, textpart_object)

            # Check that we still have an empty DB:
            new_id_list = list(db_enumeration.objects.values_list("id", flat=True).order_by("id"))
            new_id_length = len(new_id_list)

            # Eliminate presence of default foreign key object:
            for k in range(0, new_id_length):
                Index = new_id_length - k - 1
                if load_enumeration(new_id_list[Index]).labelname == "default_foreign_key_object":
                    new_id_list.pop(Index)
            new_id_length = len(new_id_list)

            # Also check textparts:
            new_id_list_textpart = list(
                db_textpart.objects.values_list("id", flat=True).order_by("id")
            )
            new_id_length_textpart = len(new_id_list_textpart)

            # Eliminate presence of default foreign key object:
            for k in range(0, new_id_length_textpart):
                Index = new_id_length_textpart - k - 1
                if (
                    load_textpart(new_id_list_textpart[Index]).labelname
                    == "default_foreign_key_object"
                ):
                    new_id_list_textpart.pop(Index)
            new_id_length_textpart = len(new_id_list_textpart)

            # Also for the hierarchy:
            new_id_list_hierarchy = list(
                db_enumeration_hierarchy.objects.values_list("id", flat=True).order_by("id")
            )
            new_id_length_hierarchy = len(new_id_list_hierarchy)

            # Check that we did not write anything:
            if (
                not (new_id_length == 0)
                and (new_id_length_textpart == 0)
                and (new_id_length_hierarchy == 0)
            ):
                print(
                    "\n ==> RAPPORT <textpart test_overwrite_nonexistent>: overwriting a nonexistent item should not do anything!\n"
                )
                print(new_id_list)
                print(new_id_length_textpart)
                self.assertIs(True, False)
            else:
                self.assertIs(True, True)

        # Done.


@tag("database", "unit", "unhappy")
class textalinea_unhappy_tests(TestCase):
    def test_load_nonexistent(self):
        """
        Unit test trying to look up a model that does not exist:
        # Parameters: none; # Returns (bool): succes of the text.
        # Author: Christiaan Douma
        """

        # Begin by finding all id's:
        id_list = list(db_textalinea.objects.values_list("id", flat=True).order_by("id"))
        id_length = len(id_list)

        # Also test for textparts:
        id_list_textpart = list(db_textpart.objects.values_list("id", flat=True).order_by("id"))
        id_length_textpart = len(id_list_textpart)

        # Check that we have indeed zero length:
        if not (id_length == 0) and (id_length_textpart == 0):
            print(
                "\n ==> RAPPORT <textalinea test_load_nonexistent>: At the start of the test, the test-DB should always be empty!\n"
            )
            self.assertIs(True, False)
        else:
            # Attempt to load something that we now know is impossible:
            textpart_object = load_textalinea(1)

            # Check if we indeed get a negative cascade back:
            Answer = "WRONG_OBJECT" in textpart_object.labelname

            # perform the test:
            if not Answer:
                print(
                    "\n ==> RAPPORT <textalinea test_load_nonexistent>: We did not obtain a <WRONG_OBJECT> labelname, as we should for looking up a nonexistent item.\n"
                )
            self.assertIs(Answer, True)

        # Done.

    def test_overwrite_nonexistent(self):
        """
        Unit test trying to overwrite a model that does not exist:
        # Parameters: none; # Returns (bool): succes of the text.
        # Author: Christiaan Douma
        """

        # Begin by finding all id's:
        id_list = list(db_textalinea.objects.values_list("id", flat=True).order_by("id"))
        id_length = len(id_list)

        # Also test for textparts:
        id_list_textpart = list(db_textpart.objects.values_list("id", flat=True).order_by("id"))
        id_length_textpart = len(id_list_textpart)

        # Check that we have indeed zero length:
        if not (id_length == 0) and (id_length_textpart == 0):
            print(
                "\n ==> RAPPORT <textalinea test_overwrite_nonexistent>: At the start of the test, the test-DB should always be empty!\n"
            )
            self.assertIs(True, False)
        else:
            # Create a nice example of a textalinea class. Only pass in just enough information
            # to see if the parent-class textpart gets handled. Do not use labelname, as
            # that one is supposed to be automatically set in the textalinea-object.
            textpart_object = textpart_textalinea()
            textpart_object.documentname = "This is a test-object for a textalinea-class"  # ATTENTION: This is to prove that we indeed can dig one level deeper.
            textpart_object.textlevel = 1
            textpart_object.typelevel = 2
            textpart_object.texttitle = "Stomme titel"
            textpart_object.nativeID = 3
            textpart_object.parentID = 4
            textpart_object.horizontal_ordering = 5
            textpart_object.summary = "Moet ik die nou ook nog allemaal typen?"
            textpart_object.sum_CanbeEmpty = True
            textpart_object.alineatype = textpart_texttype.HEADLINES
            textpart_object.enumtype = textpart_enum_type.UNKNOWN
            textpart_object.html_visualization = "<html>"
            textpart_object.summarized_wordcount = 6
            textpart_object.total_wordcount = 7
            textpart_object.nr_decendants = 8
            textpart_object.nr_children = 9
            textpart_object.nr_depths = 10
            textpart_object.nr_pages = 11

            # Attempt to overwrite something that we know does not exist:
            db_object = overwrite_textalinea(1, textpart_object)

            # Check that we still have an empty DB:
            new_id_list = list(db_textalinea.objects.values_list("id", flat=True).order_by("id"))
            new_id_length = len(new_id_list)

            # Eliminate presence of default foreign key object:
            for k in range(0, new_id_length):
                Index = new_id_length - k - 1
                if load_textalinea(new_id_list[Index]).labelname == "default_foreign_key_object":
                    new_id_list.pop(Index)
            new_id_length = len(new_id_list)

            # Also check textparts:
            new_id_list_textpart = list(
                db_textpart.objects.values_list("id", flat=True).order_by("id")
            )
            new_id_length_textpart = len(new_id_list_textpart)

            # Eliminate presence of default foreign key object:
            for k in range(0, new_id_length_textpart):
                Index = new_id_length_textpart - k - 1
                if (
                    load_textpart(new_id_list_textpart[Index]).labelname
                    == "default_foreign_key_object"
                ):
                    new_id_list_textpart.pop(Index)
            new_id_length_textpart = len(new_id_list_textpart)

            # Check that we did not write anything:
            if not (new_id_length == 0) and (new_id_length_textpart == 0):
                print(
                    "\n ==> RAPPORT <textpart test_overwrite_nonexistent>: overwriting a nonexistent item should not do anything!\n"
                )
                print(new_id_list)
                print(new_id_length_textpart)
                self.assertIs(True, False)
            else:
                self.assertIs(True, True)

        # Done.


@tag("database", "unit", "unhappy")
class Native_TOC_Element_unhappy_tests(TestCase):
    def test_load_nonexistent(self):
        """
        Unit test trying to look up a model that does not exist:
        # Parameters: none; # Returns (bool): succes of the text.
        # Author: Christiaan Douma
        """

        # Begin by finding all id's:
        id_list = list(db_Native_TOC_Element.objects.values_list("id", flat=True).order_by("id"))
        id_length = len(id_list)

        # Check that we have indeed zero length:
        if not (id_length == 0):
            print(
                "\n ==> RAPPORT <Native_TOC_Element test_overwrite_nonexistent>: At the start of the test, the test-DB should always be empty!\n"
            )
            self.assertIs(True, False)
        else:
            # Attempt to load something that we now know is impossible:
            textpart_object = load_Native_TOC_Element(1)

            # Check if we indeed get a negative cascade back:
            Answer = textpart_object.cascadelevel == -1

            # perform the test:
            if not Answer:
                print(
                    "\n ==> RAPPORT <Native_TOC_Element test_load_nonexistent>: We did not obtain a -1 cascadelevel, as we should for looking up a nonexistent item.\n"
                )
            self.assertIs(Answer, True)

        # Done.

    def test_overwrite_nonexistent(self):
        """
        Unit test trying to overwrite a model that does not exist:
        # Parameters: none; # Returns (bool): succes of the text.
        # Author: Christiaan Douma
        """

        # Begin by finding all id's:
        id_list = list(db_Native_TOC_Element.objects.values_list("id", flat=True).order_by("id"))
        id_length = len(id_list)

        # Check that we have indeed zero length:
        if not (id_length == 0):
            print(
                "\n ==> RAPPORT <Native_TOC_Element test_overwrite_nonexistent>: At the start of the test, the test-DB should always be empty!\n"
            )
            self.assertIs(True, False)
        else:
            # Create a nice example of a textpart fontregion:
            textpart_object = textpart_Native_TOC_Element()
            textpart_object.cascadelevel = 1
            textpart_object.title = "Wat een leuk hoofdstuk"
            textpart_object.page = 2
            textpart_object.Xpos = 10.0
            textpart_object.Ypos = 11.0
            textpart_object.Zpos = 12.0

            # Attempt to overwrite something that we know does not exist:
            db_object = overwrite_Native_TOC_Element(1, textpart_object)

            # Check that we still have an empty DB:
            new_id_list = list(
                db_Native_TOC_Element.objects.values_list("id", flat=True).order_by("id")
            )
            new_id_length = len(new_id_list)

            # Check that we go a bad object returned:
            if not (db_object.cascadelevel == -1):
                Answer = False

            if not (new_id_length == 0):
                print(
                    "\n ==> RAPPORT <Native_TOC_Element test_overwrite_nonexistent>: overwriting a nonexistent item should not do anything!\n"
                )
                print(new_id_list)
                self.assertIs(True, False)
            else:
                self.assertIs(True, True)

        # Done.


@tag("database", "unit", "unhappy")
class textsplitter_unhappy_tests(TestCase):
    def test_load_nonexistent(self):
        """
        Unit test trying to look up a model that does not exist:
        # Parameters: none; # Returns (bool): succes of the text.
        # Author: Christiaan Douma
        """

        # Begin by finding all id's:
        id_list = list(db_textsplitter.objects.values_list("id", flat=True).order_by("id"))
        id_length = len(id_list)

        # Also test for textparts:
        id_list_textpart = list(db_textpart.objects.values_list("id", flat=True).order_by("id"))
        id_length_textpart = len(id_list_textpart)

        # Also test for titles:
        id_list_title = list(db_title.objects.values_list("id", flat=True).order_by("id"))
        id_length_title = len(id_list_title)

        # Also test for footers:
        id_list_footer = list(db_footer.objects.values_list("id", flat=True).order_by("id"))
        id_length_footer = len(id_list_footer)

        # Also test for bodys:
        id_list_body = list(db_body.objects.values_list("id", flat=True).order_by("id"))
        id_length_body = len(id_list_body)

        # Also test for headliness:
        id_list_headlines = list(db_headlines.objects.values_list("id", flat=True).order_by("id"))
        id_length_headlines = len(id_list_headlines)

        # Also test for enumerations:
        id_list_enumeration = list(
            db_enumeration.objects.values_list("id", flat=True).order_by("id")
        )
        id_length_enumeration = len(id_list_enumeration)

        # Also test for textalineas:
        id_list_textalinea = list(db_textalinea.objects.values_list("id", flat=True).order_by("id"))
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
            (id_length == 0)
            and (id_length_textpart == 0)
            and (id_length_title == 0)
            and (id_length_footer == 0)
            and (id_length_body == 0)
            and (id_length_headlines == 0)
            and (id_length_enumeration == 0)
            and (id_length_textalinea == 0)
            and (id_length_Native_TOC_Element == 0)
            and (id_length_breakdown_decisions == 0)
        ):
            print(
                "\n ==> RAPPORT <textsplitter test_load_nonexistent>: At the start of the test, the test-DB should always be empty!\n"
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
            # Attempt to load something that we now know is impossible:
            textpart_object = load_textsplitter(1)

            # Check if we indeed get a negative cascade back:
            Answer = "WRONG_OBJECT" in textpart_object.labelname

            # perform the test:
            if not Answer:
                print(
                    "\n ==> RAPPORT <textsplitter test_load_nonexistent>: We did not obtain a <WRONG_OBJECT> labelname, as we should for looking up a nonexistent item.\n"
                )
            self.assertIs(Answer, True)

        # Done.

    def test_overwrite_nonexistent(self):
        """
        Unit test trying to overwrite a model that does not exist:
        # Parameters: none; # Returns (bool): succes of the text.
        # Author: Christiaan Douma
        """

        # Begin by finding all id's:
        id_list = list(db_textsplitter.objects.values_list("id", flat=True).order_by("id"))
        id_length = len(id_list)

        # Also test for textparts:
        id_list_textpart = list(db_textpart.objects.values_list("id", flat=True).order_by("id"))
        id_length_textpart = len(id_list_textpart)

        # Also test for titles:
        id_list_title = list(db_title.objects.values_list("id", flat=True).order_by("id"))
        id_length_title = len(id_list_title)

        # Also test for footers:
        id_list_footer = list(db_footer.objects.values_list("id", flat=True).order_by("id"))
        id_length_footer = len(id_list_footer)

        # Also test for bodys:
        id_list_body = list(db_body.objects.values_list("id", flat=True).order_by("id"))
        id_length_body = len(id_list_body)

        # Also test for headliness:
        id_list_headlines = list(db_headlines.objects.values_list("id", flat=True).order_by("id"))
        id_length_headlines = len(id_list_headlines)

        # Also test for enumerations:
        id_list_enumeration = list(
            db_enumeration.objects.values_list("id", flat=True).order_by("id")
        )
        id_length_enumeration = len(id_list_enumeration)

        # Also test for textalineas:
        id_list_textalinea = list(db_textalinea.objects.values_list("id", flat=True).order_by("id"))
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
            (id_length == 0)
            and (id_length_textpart == 0)
            and (id_length_title == 0)
            and (id_length_footer == 0)
            and (id_length_body == 0)
            and (id_length_headlines == 0)
            and (id_length_enumeration == 0)
            and (id_length_textalinea == 0)
            and (id_length_Native_TOC_Element == 0)
            and (id_length_breakdown_decisions == 0)
        ):
            print(
                "\n ==> RAPPORT <textsplitter test_overwrite_nonexistent>: At the start of the test, the test-DB should always be empty!\n"
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
            # Create a nice example of a textsplitter class. Only pass in just enough information
            # to see if all its children get handled. Do not use labelname, as
            # that one is supposed to be automatically set in the textsplitter-object.
            textpart_object = textpart_textsplitter()
            textpart_object.documentname = "Dit is een coole PDF"
            textalinea_1 = textpart_textalinea()
            textalinea_1.summary = "Wat een leuke samenvatting."
            textalinea_1.documentname = "Die komt van een dom document"
            textalinea_2 = textpart_textalinea()
            textalinea_2.summary = "En nog een leuke samenvatting."
            textalinea_2.documentname = "Die komt van een ander dom document"
            textalinea_3 = textpart_textalinea()
            textalinea_3.summary = "En dan een langdradig verhaal"
            textalinea_3.documentname = "Die komt van een kort document"
            textpart_object.textalineas = [textalinea_1, textalinea_2, textalinea_3]
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
            textpart_object.native_TOC = [TOC_1, TOC_2]
            textpart_object.title = textpart_title()
            textpart_object.title.documentname = "Title van die coole PDF"
            textpart_object.footer = textpart_footer()
            textpart_object.footer.documentname = "Footer van die coole PDF"
            textpart_object.body = textpart_body()
            textpart_object.body.documentname = "Body van die coole PDF"
            textpart_object.headlines = textpart_headlines()
            textpart_object.headlines.documentname = "Headlines van die coole PDF"
            textpart_object.enumeration = textpart_enumeration()
            textpart_object.enumeration.documentname = "Enumeration van die coole PDF"
            textpart_object.enumeration.last_textline_bigroman = "VII) en dan nog wat"
            textpart_object.VERSION = "1.2.3"
            textpart_object.ratelimit_timeunit = 0.1
            textpart_object.ratelimit_calls = 1
            textpart_object.ratelimit_tokens = 2
            textpart_object.Costs_price = 0.2
            textpart_object.Costs_tokenportion = 3
            textpart_object.api_rate_starttime = 0.3
            textpart_object.api_rate_currenttime = 0.4
            textpart_object.api_rate_currenttokens = 4
            textpart_object.api_rate_currentcalls = 5
            textpart_object.callcounter = 6
            textpart_object.api_totalprice = 0.5
            textpart_object.api_wrongcalls_duetomaxwhile = 7
            textpart_object.html_visualization = '<html class = "nice">'
            textpart_object.MaxSummaryLength = 8
            textpart_object.summarization_threshold = 9
            textpart_object.UseDummySummary = True
            textpart_object.LanguageModel = "gpt-zoveel"
            textpart_object.BackendChoice = "Sesamstraat"
            textpart_object.LanguageChoice = "Latin"
            textpart_object.LanguageTemperature = 0.6
            textpart_object.MaxCallRepeat = 10
            textpart_object.doc_metadata_author = "Pietje Bell"
            textpart_object.doc_metadata_creator = "Drogist Geelman"
            textpart_object.doc_metadata_producer = "Paul Velinga"
            textpart_object.doc_metadata_subject = "Kattenkwaad"
            textpart_object.doc_metadata_title = "Wandelende ramp"
            textpart_object.doc_metadata_fullstring = "lees het boek zelf maar"
            textpart_object.textclassification = [
                "some stupid classification",
                "another dum classification",
                "a third decision we are not interested in",
            ]

            # Attempt to overwrite something that we know does not exist:
            db_object = overwrite_textsplitter(1, textpart_object)

            # Check that we still have an empty DB:
            new_id_list = list(db_textsplitter.objects.values_list("id", flat=True).order_by("id"))
            new_id_length = len(new_id_list)

            # Eliminate presence of default foreign key object:
            for k in range(0, new_id_length):
                Index = new_id_length - k - 1
                if load_textsplitter(new_id_list[Index]).labelname == "default_foreign_key_object":
                    new_id_list.pop(Index)
            new_id_length = len(new_id_list)

            # Also test for textparts:
            new_id_list_textpart = list(
                db_textpart.objects.values_list("id", flat=True).order_by("id")
            )
            new_id_length_textpart = len(new_id_list_textpart)

            # Eliminate presence of default foreign key object:
            for k in range(0, new_id_length_textpart):
                Index = new_id_length_textpart - k - 1
                if (
                    load_textpart(new_id_list_textpart[Index]).labelname
                    == "default_foreign_key_object"
                ):
                    new_id_list_textpart.pop(Index)
            new_id_length_textpart = len(new_id_list_textpart)

            # Also test for titles:
            new_id_list_title = list(db_title.objects.values_list("id", flat=True).order_by("id"))
            new_id_length_title = len(new_id_list_title)

            # Eliminate presence of default foreign key object:
            for k in range(0, new_id_length_title):
                Index = new_id_length_title - k - 1
                if load_title(new_id_list_title[Index]).labelname == "default_foreign_key_object":
                    new_id_list_title.pop(Index)
            new_id_length_title = len(new_id_list_title)

            # Also test for footers:
            new_id_list_footer = list(db_footer.objects.values_list("id", flat=True).order_by("id"))
            new_id_length_footer = len(new_id_list_footer)

            # Eliminate presence of default foreign key object:
            for k in range(0, new_id_length_footer):
                Index = new_id_length_footer - k - 1
                if load_footer(new_id_list_footer[Index]).labelname == "default_foreign_key_object":
                    new_id_list_footer.pop(Index)
            new_id_length_footer = len(new_id_list_footer)

            # Also test for bodys:
            new_id_list_body = list(db_body.objects.values_list("id", flat=True).order_by("id"))
            new_id_length_body = len(new_id_list_body)

            # Eliminate presence of default foreign key object:
            for k in range(0, new_id_length_body):
                Index = new_id_length_body - k - 1
                if load_body(new_id_list_body[Index]).labelname == "default_foreign_key_object":
                    new_id_list_body.pop(Index)
            new_id_length_body = len(new_id_list_body)

            # Also test for headliness:
            new_id_list_headlines = list(
                db_headlines.objects.values_list("id", flat=True).order_by("id")
            )
            new_id_length_headlines = len(new_id_list_headlines)

            # Eliminate presence of default foreign key object:
            for k in range(0, new_id_length_headlines):
                Index = new_id_length_headlines - k - 1
                if (
                    load_headlines(new_id_list_headlines[Index]).labelname
                    == "default_foreign_key_object"
                ):
                    new_id_list_headlines.pop(Index)
            new_id_length_headlines = len(new_id_list_headlines)

            # Also test for enumerations:
            new_id_list_enumeration = list(
                db_enumeration.objects.values_list("id", flat=True).order_by("id")
            )
            new_id_length_enumeration = len(new_id_list_enumeration)

            # Eliminate presence of default foreign key object:
            for k in range(0, new_id_length_enumeration):
                Index = new_id_length_enumeration - k - 1
                if (
                    load_enumeration(new_id_list_enumeration[Index]).labelname
                    == "default_foreign_key_object"
                ):
                    new_id_list_enumeration.pop(Index)
            new_id_length_enumeration = len(new_id_list_enumeration)

            # Also test for textalineas:
            new_id_list_textalinea = list(
                db_textalinea.objects.values_list("id", flat=True).order_by("id")
            )
            new_id_length_textalinea = len(new_id_list_textalinea)

            # Eliminate presence of default foreign key object:
            for k in range(0, new_id_length_textalinea):
                Index = new_id_length_textalinea - k - 1
                if (
                    load_textalinea(new_id_list_textalinea[Index]).labelname
                    == "default_foreign_key_object"
                ):
                    new_id_list_textalinea.pop(Index)
            new_id_length_textalinea = len(new_id_list_textalinea)

            # Also test for Native_TOC_Elements:
            new_id_list_Native_TOC_Element = list(
                db_Native_TOC_Element.objects.values_list("id", flat=True).order_by("id")
            )
            new_id_length_Native_TOC_Element = len(new_id_list_Native_TOC_Element)

            # Also test for breakdown_decisions:
            new_id_list_breakdown_decisions = list(
                db_breakdown_decisions.objects.values_list("id", flat=True).order_by("id")
            )
            new_id_length_breakdown_decisions = len(new_id_list_breakdown_decisions)

            if not (
                (new_id_length == 0)
                and (new_id_length_textpart == 0)
                and (new_id_length_title == 0)
                and (new_id_length_footer == 0)
                and (new_id_length_body == 0)
                and (new_id_length_headlines == 0)
                and (new_id_length_enumeration == 0)
                and (new_id_length_textalinea == 0)
                and (new_id_length_Native_TOC_Element == 0)
                and (new_id_length_breakdown_decisions == 0)
            ):
                print(
                    "\n ==> RAPPORT <textsplitter test_overwrite_nonexistent>: overwriting a nonexistent item should not do anything!\n"
                )
                print(id_list)
                print(new_id_list)
                print(id_list_textpart)
                print(new_id_list_textpart)
                print(id_list_title)
                print(new_id_list_title)
                print(id_list_footer)
                print(new_id_list_footer)
                print(id_list_body)
                print(new_id_list_body)
                print(id_list_headlines)
                print(new_id_list_headlines)
                print(id_list_enumeration)
                print(new_id_list_enumeration)
                print(id_list_textalinea)
                print(new_id_list_textalinea)
                print(id_list_Native_TOC_Element)
                print(new_id_list_Native_TOC_Element)
                print(id_list_breakdown_decisions)
                print(new_id_list_breakdown_decisions)
                self.assertIs(True, False)
            else:
                self.assertIs(True, True)

        # Done.
