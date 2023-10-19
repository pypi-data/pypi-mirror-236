# import sys path:
# import sys

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


@tag("database", "unit")
class user_object_tests(TestCase):
    @tag("user")
    def test_newuser(self):
        """
        Unit test for get_default_user() in models.
        # Parameters: none; # Returns (bool): succes of the text.
        # Author: Christiaan Douma
        """

        # Collect the default user twice:
        user1 = get_default_user()
        user2 = get_default_user()

        # See that there is indeed an entry in the DB:
        test_queryset = User.objects.all()
        test_querylist = list(test_queryset)

        # Compare:
        Answer = False
        if len(test_querylist) == 1:
            if user1.email == user2.email:
                Answer = True

        # Perform the test:
        self.assertIs(Answer, True)

        # Done.


@tag("database", "unit", "print")
class models_print_tests(TestCase):
    def test_print_models(self):
        """
        Unit test for the str-function of the textsplitter-models.
        # Parameters: none; # Returns (bool): succes of the text.
        # Author: Christiaan Douma
        """

        db_textpart_inst = db_textpart()
        db_fontregion_inst = db_fontregion()
        db_fontregion_inst.textpart = db_textpart_inst
        db_lineregion_inst = db_lineregion()
        db_lineregion_inst.textpart = db_textpart_inst
        db_readingline_inst = db_readingline()
        db_readingline_inst.textpart = db_textpart_inst
        db_readinghistogram_inst = db_readinghistogram()
        db_readinghistogram_inst.textpart = db_textpart_inst

        db_title_inst = db_title()
        db_title_inst.textpart = db_textpart_inst
        db_body_inst = db_body()
        db_body_inst.textpart = db_textpart_inst
        db_footer_inst = db_footer()
        db_footer_inst.textpart = db_textpart_inst
        db_headlines_inst = db_headlines()
        db_headlines_inst.textpart = db_textpart_inst
        db_enumeration_inst = db_enumeration()
        db_enumeration_inst.textpart = db_textpart_inst
        db_headlines_hierarchy_inst = db_headlines_hierarchy()
        db_headlines_hierarchy_inst.headlines = db_headlines_inst
        db_enumeration_hierarchy_inst = db_enumeration_hierarchy()
        db_enumeration_hierarchy_inst.enumeration = db_enumeration_inst

        db_textsplitter_inst = db_textsplitter()
        db_textsplitter_inst.title = db_title_inst
        db_textsplitter_inst.body = db_body_inst
        db_textsplitter_inst.footer = db_footer_inst
        db_textsplitter_inst.headlines = db_headlines_inst
        db_textsplitter_inst.enumeration = db_enumeration_inst
        db_textsplitter_inst.textpart = db_textpart_inst

        db_Native_TOC_Element_inst = db_Native_TOC_Element()
        db_Native_TOC_Element_inst.textsplitter = db_textsplitter_inst
        db_breakdown_decisions_inst = db_breakdown_decisions()
        db_breakdown_decisions_inst.textsplitter = db_textsplitter_inst

        db_textalinea_inst = db_textalinea()
        db_textalinea_inst.textsplitter = db_textsplitter_inst
        db_textalinea_inst.textpart = db_textpart_inst

        Mystr = ""
        Mystr = Mystr + str(db_textpart_inst)
        Mystr = Mystr + str(db_fontregion_inst)
        Mystr = Mystr + str(db_lineregion_inst)
        Mystr = Mystr + str(db_readingline_inst)
        Mystr = Mystr + str(db_readinghistogram_inst)
        Mystr = Mystr + str(db_title_inst)
        Mystr = Mystr + str(db_body_inst)
        Mystr = Mystr + str(db_footer_inst)
        Mystr = Mystr + str(db_headlines_inst)
        Mystr = Mystr + str(db_enumeration_inst)
        Mystr = Mystr + str(db_headlines_hierarchy_inst)
        Mystr = Mystr + str(db_enumeration_hierarchy_inst)
        Mystr = Mystr + str(db_textsplitter_inst)
        Mystr = Mystr + str(db_Native_TOC_Element_inst)
        Mystr = Mystr + str(db_breakdown_decisions_inst)
        Mystr = Mystr + str(db_textalinea_inst)

        # Now, make a nice test:
        Answer = False
        if "Textpart" in Mystr:
            Answer = True
        self.assertEqual(Answer, True)

        # Done.


# Creation of the test classes:
@tag("database", "unit")
class fontregion_newwrite_tests(TestCase):
    @tag("newwrite")
    def test_newwrite(self):
        """
        Unit test for a write-read operation that writes a new object to the DB:
        # Parameters: none; # Returns (bool): succes of the text.
        # Author: Christiaan Douma
        """

        # Create a nice example of a textpart fontregion:
        textpart_object = textpart_fontregion()
        textpart_object.left = 2.21
        textpart_object.right = 4.41
        textpart_object.value = 3.31
        textpart_object.frequency = 0.89
        textpart_object.cascadelevel = 2
        textpart_object.isregular = True

        # write it to the database:
        db_object = newwrite_fontregion(textpart_object)

        # Next, retrieve the ID's. We test that, indeed nothing else is in the test-DB,
        # by testing that the length has to be exactly 1:
        id_list = list(db_fontregion.objects.values_list("id", flat=True).order_by("id"))
        id_length = len(id_list)

        # Test if there is actually something in the DB now:
        if not (id_length == 1):
            print(
                "\n ==> RAPPORT <fontregion test_newwrite>: The number of DB-entries was not as we expected!\n"
            )
            print(id_list)
            self.assertIs(True, False)
        else:
            # Then, obtain what should be the proper ID:
            properID = id_list[0]

            # retrieve the object from the database:
            retrieved_object = load_fontregion(properID)

            # Compare outputs:
            Answer = textpart_object.compare(retrieved_object)

            # print reports:
            if Answer == False:
                print("\n ==> RAPPORT <fontregion test_newwrite>: comparison failed!\n")
                textpart_object.printregion()
                retrieved_object.printregion()

            # perform the test:
            self.assertIs(Answer, True)

        # Done.


@tag("database", "unit")
class lineregion_newwrite_tests(TestCase):
    @tag("newwrite")
    def test_newwrite(self):
        """
        Unit test for a write-read operation that writes a new object to the DB:
        # Parameters: none; # Returns (bool): succes of the text.
        # Author: Christiaan Douma
        """

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

        # write it to the database:
        db_object = newwrite_lineregion(textpart_object)

        # Next, retrieve the ID's. We test that, indeed nothing else is in the test-DB,
        # by testing that the length has to be exactly 1:
        id_list = list(db_lineregion.objects.values_list("id", flat=True).order_by("id"))
        id_length = len(id_list)

        # Test if there is actually something in the DB now:
        if not (id_length == 1):
            print(
                "\n ==> RAPPORT <lineregion test_newwrite>: The number of DB-entries was not as we expected!\n"
            )
            print(id_list)
            self.assertIs(True, False)
        else:
            # Then, obtain what should be the proper ID:
            properID = id_list[0]

            # retrieve the object from the database:
            retrieved_object = load_lineregion(properID)

            # Compare outputs:
            Answer = textpart_object.compare(retrieved_object)

            # print reports:
            if Answer == False:
                print("\n ==> RAPPORT <lineregion test_newwrite>: comparison failed!\n")
                textpart_object.printregion()
                retrieved_object.printregion()

            # perform the test:
            self.assertIs(Answer, True)

        # Done.


@tag("database", "unit")
class textpart_newwrite_tests(TestCase):
    @tag("foreignkey")
    def test_default_foreignkey(self):
        """
        Unit test for get_default_foreignkey() of textpart.
        # Parameters: none; # Returns (bool): succes of the text.
        # Author: Christiaan Douma
        """

        # Create the default foreign key:
        test_pk = db_textpart.get_default_foreignkey()

        # Again; we are supposed to get the same answer then:
        test_pk2 = db_textpart.get_default_foreignkey()

        # See that there is indeed an entry in the DB:
        test_queryset = db_textpart.objects.filter(pk=test_pk)
        test_querylist = list(test_queryset)

        # Compare:
        Answer = False
        if len(test_querylist) == 1:
            retrieved_pk = test_querylist[0].id
            if retrieved_pk == test_pk:
                if test_pk == test_pk2:
                    Answer = True

        # Perform the test:
        self.assertIs(Answer, True)

        # Done.

    @tag("newwrite")
    def test_newwrite(self):
        """
        Unit test for a write-read operation that writes a new object to the DB:
        # Parameters: none; # Returns (bool): succes of the text.
        # Author: Christiaan Douma
        """

        # Create a nice example of a textpart class:
        textpart_object = textpart_textpart()
        textpart_object.labelname = "Test for newwrite"
        textpart_object.documentpath = "/some/path/"
        textpart_object.outputpath = "/another/path/"
        textpart_object.documentname = "Hope for success"
        textpart_object.histogramsize = 2
        textpart_object.headerboundary = 700.0
        textpart_object.footerboundary = 20.0
        textpart_object.ruleverbosity = 2
        textpart_object.verbosetextline = "some nice line"
        textpart_object.nr_bold_chars = 102
        textpart_object.nr_total_chars = 1020
        textpart_object.boldchars_ratio = 0.02
        textpart_object.boldratio_threshold = 0.06
        textpart_object.max_vertpos = 695.0
        textpart_object.min_vertpos = 15.0
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
        textpart_object.fontregions = [fontregion_1, fontregion_2]
        textpart_object.lineregions = [lineregion_1, lineregion_2]
        textpart_object.textcontent = ["my fisrt textline", "another textline", "Now I get bored"]
        textpart_object.pagenumbers = [1, 2, 3]
        textpart_object.positioncontent = [5.0, 10.0, 20.0]
        textpart_object.horposcontent = [1.0, 2.0, 3.0]
        textpart_object.whitelinesize = [-2.0, 5.0, 10.0]
        textpart_object.fontsize_perline = [12.0, 13.0, 14.0]
        textpart_object.is_italic = [True, False, False]
        textpart_object.is_bold = [False, True, False]
        textpart_object.is_highlighted = [False, False, True]
        textpart_object.fontsizeHist_percharacter = [[10.0, 20.0], [1.0, 2.0, 3.0], [1.0, 2.0, 3.0]]
        textpart_object.fontsizeHist_perline = [[11.0, 21.0], [1.1, 2.1, 3.1], [1.1, 2.1, 3.1]]
        textpart_object.whitespaceHist_perline = [[12.0, 22.0], [1.2, 2.2, 3.1], [1.2, 2.2, 3.2]]

        # write the object to the database:
        db_object = newwrite_textpart(textpart_object)

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
            and (id_length_fontregion == 2)
            and (id_length_lineregion == 2)
            and (id_length_readingline == 3)
            and (id_length_readinghistogram == 9)
        ):
            print(
                "\n ==> RAPPORT <textpart test_newwrite>: The number of DB-entries was not as we expected!\n"
            )
            print(id_list)
            print(id_list_fontregion)
            print(id_list_lineregion)
            print(id_list_readingline)
            print(id_list_readinghistogram)
            self.assertIs(True, False)
        else:
            # Then, obtain what should be the proper ID:
            properID = id_list[0]

            # retrieve the object from the database:
            retrieved_object = load_textpart(properID)

            # Compare outputs:
            Answer = True

            # Normal fields:
            if not (textpart_object.labelname == retrieved_object.labelname):
                Answer = False
            if not (textpart_object.documentpath == retrieved_object.documentpath):
                Answer = False
            if not (textpart_object.outputpath == retrieved_object.outputpath):
                Answer = False
            if not (textpart_object.documentname == retrieved_object.documentname):
                Answer = False
            if not (textpart_object.histogramsize == retrieved_object.histogramsize):
                Answer = False
            if not (textpart_object.headerboundary == retrieved_object.headerboundary):
                Answer = False
            if not (textpart_object.footerboundary == retrieved_object.footerboundary):
                Answer = False
            if not (textpart_object.ruleverbosity == retrieved_object.ruleverbosity):
                Answer = False
            if not (textpart_object.verbosetextline == retrieved_object.verbosetextline):
                Answer = False
            if not (textpart_object.nr_bold_chars == retrieved_object.nr_bold_chars):
                Answer = False
            if not (textpart_object.nr_total_chars == retrieved_object.nr_total_chars):
                Answer = False
            if not (textpart_object.boldchars_ratio == retrieved_object.boldchars_ratio):
                Answer = False
            if not (textpart_object.boldratio_threshold == retrieved_object.boldratio_threshold):
                Answer = False
            if not (textpart_object.max_vertpos == retrieved_object.max_vertpos):
                Answer = False
            if not (textpart_object.min_vertpos == retrieved_object.min_vertpos):
                Answer = False

            # fontregions:
            if not (len(retrieved_object.fontregions) == 2):
                Answer = False
            else:
                if not fontregion_1.compare(retrieved_object.fontregions[0]):
                    Answer = False
                if not fontregion_2.compare(retrieved_object.fontregions[1]):
                    Answer = False

            # lineregions:
            if not (len(retrieved_object.lineregions) == 2):
                Answer = False
            else:
                if not lineregion_1.compare(retrieved_object.lineregions[0]):
                    Answer = False
                if not lineregion_2.compare(retrieved_object.lineregions[1]):
                    Answer = False

            # Content per textline:
            for k in range(0, 3):
                if not (retrieved_object.textcontent[k] == textpart_object.textcontent[k]):
                    Answer = False
                if not (retrieved_object.pagenumbers[k] == textpart_object.pagenumbers[k]):
                    Answer = False
                if not (retrieved_object.positioncontent[k] == textpart_object.positioncontent[k]):
                    Answer = False
                if not (retrieved_object.horposcontent[k] == textpart_object.horposcontent[k]):
                    Answer = False
                if not (retrieved_object.whitelinesize[k] == textpart_object.whitelinesize[k]):
                    Answer = False
                if not (
                    retrieved_object.fontsize_perline[k] == textpart_object.fontsize_perline[k]
                ):
                    Answer = False
                if not (retrieved_object.is_italic[k] == textpart_object.is_italic[k]):
                    Answer = False
                if not (retrieved_object.is_bold[k] == textpart_object.is_bold[k]):
                    Answer = False
                if not (retrieved_object.is_highlighted[k] == textpart_object.is_highlighted[k]):
                    Answer = False

            # Content of fontsize per character histogram:
            if not (len(retrieved_object.fontsizeHist_percharacter) == 3):
                Answer = False
            else:
                if not (len(retrieved_object.fontsizeHist_percharacter[0]) == 2):
                    Answer = False
                else:
                    if not (
                        retrieved_object.fontsizeHist_percharacter[0][0]
                        == textpart_object.fontsizeHist_percharacter[0][0]
                    ):
                        Answer = False
                    if not (
                        retrieved_object.fontsizeHist_percharacter[0][1]
                        == textpart_object.fontsizeHist_percharacter[0][1]
                    ):
                        Answer = False

                if not (len(retrieved_object.fontsizeHist_percharacter[1]) == 3):
                    Answer = False
                else:
                    if not (
                        retrieved_object.fontsizeHist_percharacter[1][0]
                        == textpart_object.fontsizeHist_percharacter[1][0]
                    ):
                        Answer = False
                    if not (
                        retrieved_object.fontsizeHist_percharacter[1][1]
                        == textpart_object.fontsizeHist_percharacter[1][1]
                    ):
                        Answer = False
                    if not (
                        retrieved_object.fontsizeHist_percharacter[1][2]
                        == textpart_object.fontsizeHist_percharacter[1][2]
                    ):
                        Answer = False

            # Content of fontsize per line histogram:
            if not (len(retrieved_object.fontsizeHist_perline) == 3):
                Answer = False
            else:
                if not (len(retrieved_object.fontsizeHist_perline[0]) == 2):
                    Answer = False
                else:
                    if not (
                        retrieved_object.fontsizeHist_perline[0][0]
                        == textpart_object.fontsizeHist_perline[0][0]
                    ):
                        Answer = False
                    if not (
                        retrieved_object.fontsizeHist_perline[0][1]
                        == textpart_object.fontsizeHist_perline[0][1]
                    ):
                        Answer = False

                if not (len(retrieved_object.fontsizeHist_perline[1]) == 3):
                    Answer = False
                else:
                    if not (
                        retrieved_object.fontsizeHist_perline[1][0]
                        == textpart_object.fontsizeHist_perline[1][0]
                    ):
                        Answer = False
                    if not (
                        retrieved_object.fontsizeHist_perline[1][1]
                        == textpart_object.fontsizeHist_perline[1][1]
                    ):
                        Answer = False
                    if not (
                        retrieved_object.fontsizeHist_perline[1][2]
                        == textpart_object.fontsizeHist_perline[1][2]
                    ):
                        Answer = False

            # Content of whitelines histogram:
            if not (len(retrieved_object.whitespaceHist_perline) == 3):
                Answer = False
            else:
                if not (len(retrieved_object.whitespaceHist_perline[0]) == 2):
                    Answer = False
                else:
                    if not (
                        retrieved_object.whitespaceHist_perline[0][0]
                        == textpart_object.whitespaceHist_perline[0][0]
                    ):
                        Answer = False
                    if not (
                        retrieved_object.whitespaceHist_perline[0][1]
                        == textpart_object.whitespaceHist_perline[0][1]
                    ):
                        Answer = False

                if not (len(retrieved_object.whitespaceHist_perline[1]) == 3):
                    Answer = False
                else:
                    if not (
                        retrieved_object.whitespaceHist_perline[1][0]
                        == textpart_object.whitespaceHist_perline[1][0]
                    ):
                        Answer = False
                    if not (
                        retrieved_object.whitespaceHist_perline[1][1]
                        == textpart_object.whitespaceHist_perline[1][1]
                    ):
                        Answer = False
                    if not (
                        retrieved_object.whitespaceHist_perline[1][2]
                        == textpart_object.whitespaceHist_perline[1][2]
                    ):
                        Answer = False

            # print reports:
            if Answer == False:
                print("\n ==> RAPPORT <textpart test_newwrite>: comparison failed!\n")

            # perform the test:
            self.assertIs(Answer, True)

        # Done.

    @tag("newwrite")
    def test_newwrite_partially_empty(self):
        """
        Unit test for a write-read operation that writes a new object to the DB:
        # Parameters: none; # Returns (bool): succes of the text.
        # Author: Christiaan Douma
        """

        # Create a nice example of a textpart class:
        textpart_object = textpart_textpart()
        textpart_object.labelname = "Test for newwrite"
        textpart_object.documentpath = "/some/path/"
        textpart_object.outputpath = "/another/path/"
        textpart_object.documentname = "Hope for success"
        textpart_object.histogramsize = 2
        textpart_object.headerboundary = 700.0
        textpart_object.footerboundary = 20.0
        textpart_object.ruleverbosity = 2
        textpart_object.verbosetextline = "some nice line"
        textpart_object.nr_bold_chars = 102
        textpart_object.nr_total_chars = 1020
        textpart_object.boldchars_ratio = 0.02
        textpart_object.boldratio_threshold = 0.06
        textpart_object.max_vertpos = 695.0
        textpart_object.min_vertpos = 15.0

        # write the object to the database:
        db_object = newwrite_textpart(textpart_object)

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
            and (id_length_fontregion == 0)
            and (id_length_lineregion == 0)
            and (id_length_readingline == 0)
            and (id_length_readinghistogram == 0)
        ):
            print(
                "\n ==> RAPPORT <textpart test_newwrite_partially_empty>: The number of DB-entries was not as we expected!\n"
            )
            print(id_list)
            print(id_list_fontregion)
            print(id_list_lineregion)
            print(id_list_readingline)
            print(id_list_readinghistogram)
            self.assertIs(True, False)
        else:
            # Then, obtain what should be the proper ID:
            properID = id_list[0]

            # retrieve the object from the database:
            retrieved_object = load_textpart(properID)

            # Compare outputs:
            Answer = True

            # Normal fields:
            if not (textpart_object.labelname == retrieved_object.labelname):
                Answer = False
            if not (textpart_object.documentpath == retrieved_object.documentpath):
                Answer = False
            if not (textpart_object.outputpath == retrieved_object.outputpath):
                Answer = False
            if not (textpart_object.documentname == retrieved_object.documentname):
                Answer = False
            if not (textpart_object.histogramsize == retrieved_object.histogramsize):
                Answer = False
            if not (textpart_object.headerboundary == retrieved_object.headerboundary):
                Answer = False
            if not (textpart_object.footerboundary == retrieved_object.footerboundary):
                Answer = False
            if not (textpart_object.ruleverbosity == retrieved_object.ruleverbosity):
                Answer = False
            if not (textpart_object.verbosetextline == retrieved_object.verbosetextline):
                Answer = False
            if not (textpart_object.nr_bold_chars == retrieved_object.nr_bold_chars):
                Answer = False
            if not (textpart_object.nr_total_chars == retrieved_object.nr_total_chars):
                Answer = False
            if not (textpart_object.boldchars_ratio == retrieved_object.boldchars_ratio):
                Answer = False
            if not (textpart_object.boldratio_threshold == retrieved_object.boldratio_threshold):
                Answer = False
            if not (textpart_object.max_vertpos == retrieved_object.max_vertpos):
                Answer = False
            if not (textpart_object.min_vertpos == retrieved_object.min_vertpos):
                Answer = False

            # fontregions:
            if not (len(retrieved_object.fontregions) == 0):
                Answer = False

            # lineregions:
            if not (len(retrieved_object.lineregions) == 0):
                Answer = False

            # Content per textline:
            if not (len(retrieved_object.textcontent) == 0):
                Answer = False

            # Content of fontsize per character histogram:
            if not (len(retrieved_object.fontsizeHist_percharacter) == 0):
                Answer = False
            if not (len(retrieved_object.fontsizeHist_perline) == 0):
                Answer = False
            if not (len(retrieved_object.whitespaceHist_perline) == 0):
                Answer = False

            # print reports:
            if Answer == False:
                print(
                    "\n ==> RAPPORT <textpart test_newwrite_partially_empty>: comparison failed!\n"
                )

            # perform the test:
            self.assertIs(Answer, True)

        # Done.


@tag("database", "unit")
class title_newwrite_tests(TestCase):
    @tag("foreignkey")
    def test_default_foreignkey(self):
        """
        Unit test for get_default_foreignkey() of title.
        # Parameters: none; # Returns (bool): succes of the text.
        # Author: Christiaan Douma
        """

        # Create the default foreign key:
        test_pk = db_title.get_default_foreignkey()

        # Again; we are supposed to get the same answer then:
        test_pk2 = db_title.get_default_foreignkey()

        # See that there is indeed an entry in the DB:
        test_queryset = db_title.objects.filter(pk=test_pk)
        test_querylist = list(test_queryset)

        # Compare:
        Answer = False
        if len(test_querylist) == 1:
            retrieved_pk = test_querylist[0].id
            if retrieved_pk == test_pk:
                if test_pk == test_pk2:
                    Answer = True

        # Perform the test:
        self.assertIs(Answer, True)

        # Done.

    @tag("newwrite")
    def test_newwrite(self):
        """
        Unit test for a write-read operation that writes a new object to the DB:
        # Parameters: none; # Returns (bool): succes of the text.
        # Author: Christiaan Douma
        """

        # Create a nice example of a title class. Only pass in just enough information
        # to see if the parent-class textpart gets handled. Do not use labelname, as
        # that one is supposed to be automatically set in the title-object.
        textpart_object = textpart_title()
        textpart_object.documentname = "This is a test-object for a title-class"  # ATTENTION: This is to prove that we indeed can dig one level deeper.

        # write it to the database:
        db_object = newwrite_title(textpart_object)

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
                "\n ==> RAPPORT <title test_newwrite>: The number of DB-entries was not as we expected!\n"
            )
            print(id_list)
            print(id_list_textpart)
            self.assertIs(True, False)
        else:
            # Then, obtain what should be the proper ID:
            properID = id_list[0]

            # retrieve the object from the database:
            retrieved_object = load_title(properID)

            # Compare outputs:
            Answer = True

            # Check that we indeed have the correct object:
            if not (retrieved_object.labelname == "Title"):
                Answer = False
            if not (retrieved_object.documentname == textpart_object.documentname):
                Answer = False

            # print reports:
            if Answer == False:
                print("\n ==> RAPPORT <title test_newwrite>: comparison failed!\n")
                print(textpart_object.labelname + " " + textpart_object.documentname)
                print(retrieved_object.labelname + " " + retrieved_object.documentname)

            # perform the test:
            self.assertIs(Answer, True)

        # Done.


@tag("database", "unit")
class body_newwrite_tests(TestCase):
    @tag("foreignkey")
    def test_default_foreignkey(self):
        """
        Unit test for get_default_foreignkey() of body.
        # Parameters: none; # Returns (bool): succes of the text.
        # Author: Christiaan Douma
        """

        # Create the default foreign key:
        test_pk = db_body.get_default_foreignkey()

        # Again; we are supposed to get the same answer then:
        test_pk2 = db_body.get_default_foreignkey()

        # See that there is indeed an entry in the DB:
        test_queryset = db_body.objects.filter(pk=test_pk)
        test_querylist = list(test_queryset)

        # Compare:
        Answer = False
        if len(test_querylist) == 1:
            retrieved_pk = test_querylist[0].id
            if retrieved_pk == test_pk:
                if test_pk == test_pk2:
                    Answer = True

        # Perform the test:
        self.assertIs(Answer, True)

        # Done.

    @tag("newwrite")
    def test_newwrite(self):
        """
        Unit test for a write-read operation that writes a new object to the DB:
        # Parameters: none; # Returns (bool): succes of the text.
        # Author: Christiaan Douma
        """

        # Create a nice example of a body class. Only pass in just enough information
        # to see if the parent-class textpart gets handled. Do not use labelname, as
        # that one is supposed to be automatically set in the body-object.
        textpart_object = textpart_body()
        textpart_object.documentname = "This is a test-object for a body-class"  # ATTENTION: This is to prove that we indeed can dig one level deeper.

        # write it to the database:
        db_object = newwrite_body(textpart_object)

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
                "\n ==> RAPPORT <body test_newwrite>: The number of DB-entries was not as we expected!\n"
            )
            print(id_list)
            print(id_list_textpart)
            self.assertIs(True, False)
        else:
            # Then, obtain what should be the proper ID:
            properID = id_list[0]

            # retrieve the object from the database:
            retrieved_object = load_body(properID)

            # Compare outputs:
            Answer = True

            # Check that we indeed have the correct object:
            if not (retrieved_object.labelname == "Body"):
                Answer = False
            if not (retrieved_object.documentname == textpart_object.documentname):
                Answer = False

            # print reports:
            if Answer == False:
                print("\n ==> RAPPORT <body test_newwrite>: comparison failed!\n")
                print(textpart_object.labelname + " " + textpart_object.documentname)
                print(retrieved_object.labelname + " " + retrieved_object.documentname)

            # perform the test:
            self.assertIs(Answer, True)

        # Done.


@tag("database", "unit")
class footer_newwrite_tests(TestCase):
    @tag("foreignkey")
    def test_default_foreignkey(self):
        """
        Unit test for get_default_foreignkey() of footer.
        # Parameters: none; # Returns (bool): succes of the text.
        # Author: Christiaan Douma
        """

        # Create the default foreign key:
        test_pk = db_footer.get_default_foreignkey()

        # Again; we are supposed to get the same answer then:
        test_pk2 = db_footer.get_default_foreignkey()

        # See that there is indeed an entry in the DB:
        test_queryset = db_footer.objects.filter(pk=test_pk)
        test_querylist = list(test_queryset)

        # Compare:
        Answer = False
        if len(test_querylist) == 1:
            retrieved_pk = test_querylist[0].id
            if retrieved_pk == test_pk:
                if test_pk == test_pk2:
                    Answer = True

        # Perform the test:
        self.assertIs(Answer, True)

        # Done.

    @tag("newwrite")
    def test_newwrite(self):
        """
        Unit test for a write-read operation that writes a new object to the DB:
        # Parameters: none; # Returns (bool): succes of the text.
        # Author: Christiaan Douma
        """

        # Create a nice example of a footer class. Only pass in just enough information
        # to see if the parent-class textpart gets handled. Do not use labelname, as
        # that one is supposed to be automatically set in the footer-object.
        textpart_object = textpart_footer()
        textpart_object.documentname = "This is a test-object for a footer-class"  # ATTENTION: This is to prove that we indeed can dig one level deeper.

        # write it to the database:
        db_object = newwrite_footer(textpart_object)

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
                "\n ==> RAPPORT <footer test_newwrite>: The number of DB-entries was not as we expected!\n"
            )
            print(id_list)
            print(id_list_textpart)
            self.assertIs(True, False)
        else:
            # Then, obtain what should be the proper ID:
            properID = id_list[0]

            # retrieve the object from the database:
            retrieved_object = load_footer(properID)

            # Compare outputs:
            Answer = True

            # Check that we indeed have the correct object:
            if not (retrieved_object.labelname == "Footer"):
                Answer = False
            if not (retrieved_object.documentname == textpart_object.documentname):
                Answer = False

            # print reports:
            if Answer == False:
                print("\n ==> RAPPORT <footer test_newwrite>: comparison failed!\n")
                print(textpart_object.labelname + " " + textpart_object.documentname)
                print(retrieved_object.labelname + " " + retrieved_object.documentname)

            # perform the test:
            self.assertIs(Answer, True)

        # Done.


@tag("database", "unit")
class headlines_newwrite_tests(TestCase):
    @tag("foreignkey")
    def test_default_foreignkey(self):
        """
        Unit test for get_default_foreignkey() of headlines.
        # Parameters: none; # Returns (bool): succes of the text.
        # Author: Christiaan Douma
        """

        # Create the default foreign key:
        test_pk = db_headlines.get_default_foreignkey()

        # Again; we are supposed to get the same answer then:
        test_pk2 = db_headlines.get_default_foreignkey()

        # See that there is indeed an entry in the DB:
        test_queryset = db_headlines.objects.filter(pk=test_pk)
        test_querylist = list(test_queryset)

        # Compare:
        Answer = False
        if len(test_querylist) == 1:
            retrieved_pk = test_querylist[0].id
            if retrieved_pk == test_pk:
                if test_pk == test_pk2:
                    Answer = True

        # Perform the test:
        self.assertIs(Answer, True)

        # Done.

    @tag("newwrite")
    def test_newwrite(self):
        """
        Unit test for a write-read operation that writes a new object to the DB:
        # Parameters: none; # Returns (bool): succes of the text.
        # Author: Christiaan Douma
        """

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

        # write it to the database:
        db_object = newwrite_headlines(textpart_object)

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
        if not ((id_length == 1) and (id_length_textpart == 1) and (id_length_hierarchy == 3)):
            print(
                "\n ==> RAPPORT <headlines test_newwrite>: The number of DB-entries was not as we expected!\n"
            )
            print(id_list)
            print(id_list_textpart)
            print(id_list_hierarchy)
            self.assertIs(True, False)
        else:
            # Then, obtain what should be the proper ID:
            properID = id_list[0]

            # retrieve the object from the database:
            retrieved_object = load_headlines(properID)

            # Compare outputs:
            Answer = True

            # Check that we indeed have the correct object:
            if not (retrieved_object.labelname == "Headlines"):
                Answer = False
            if not (retrieved_object.documentname == textpart_object.documentname):
                Answer = False

            # Check for the hierarchy:
            if not (len(retrieved_object.hierarchy) == len(textpart_object.hierarchy)):
                Answer = False
            else:
                for k in range(0, len(retrieved_object.hierarchy)):
                    if not (retrieved_object.hierarchy[k] == textpart_object.hierarchy[k]):
                        Answer = False

            # print reports:
            if Answer == False:
                print("\n ==> RAPPORT <headlines test_newwrite>: comparison failed!\n")
                print(textpart_object.labelname + " " + textpart_object.documentname)
                print(retrieved_object.labelname + " " + retrieved_object.documentname)

            # perform the test:
            self.assertIs(Answer, True)

        # Done.


@tag("database", "unit")
class enumeration_newwrite_tests(TestCase):
    @tag("foreignkey")
    def test_default_foreignkey(self):
        """
        Unit test for get_default_foreignkey() of enumeration.
        # Parameters: none; # Returns (bool): succes of the text.
        # Author: Christiaan Douma
        """

        # Create the default foreign key:
        test_pk = db_enumeration.get_default_foreignkey()

        # Again; we are supposed to get the same answer then:
        test_pk2 = db_enumeration.get_default_foreignkey()

        # See that there is indeed an entry in the DB:
        test_queryset = db_enumeration.objects.filter(pk=test_pk)
        test_querylist = list(test_queryset)

        # Compare:
        Answer = False
        if len(test_querylist) == 1:
            retrieved_pk = test_querylist[0].id
            if retrieved_pk == test_pk:
                if test_pk == test_pk2:
                    Answer = True

        # Perform the test:
        self.assertIs(Answer, True)

        # Done.

    @tag("newwrite")
    def test_newwrite(self):
        """
        Unit test for a write-read operation that writes a new object to the DB:
        # Parameters: none; # Returns (bool): succes of the text.
        # Author: Christiaan Douma
        """

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

        # write it to the database:
        db_object = newwrite_enumeration(textpart_object)

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
        if not ((id_length == 1) and (id_length_textpart == 1) and (id_length_hierarchy == 3)):
            print(
                "\n ==> RAPPORT <enumeration test_newwrite>: The number of DB-entries was not as we expected!\n"
            )
            print(id_list)
            print(id_list_textpart)
            print(id_list_hierarchy)
            self.assertIs(True, False)
        else:
            # Then, obtain what should be the proper ID:
            properID = id_list[0]

            # retrieve the object from the database:
            retrieved_object = load_enumeration(properID)

            # Compare outputs:
            Answer = True

            # Check that we indeed have the correct object:
            if not (retrieved_object.labelname == "Enumeration"):
                Answer = False
            if not (retrieved_object.documentname == textpart_object.documentname):
                Answer = False

            # Check for the hierarchy:
            if not (len(retrieved_object.hierarchy) == len(textpart_object.hierarchy)):
                Answer = False
            else:
                for k in range(0, len(retrieved_object.hierarchy)):
                    if not (retrieved_object.hierarchy[k] == textpart_object.hierarchy[k]):
                        Answer = False

            # Check the values:
            if not (textpart_object.last_enumtype_index == retrieved_object.last_enumtype_index):
                Answer = False
            if not (textpart_object.this_enumtype_index == retrieved_object.this_enumtype_index):
                Answer = False
            if not (
                textpart_object.last_textline_bigroman == retrieved_object.last_textline_bigroman
            ):
                Answer = False
            if not (
                textpart_object.last_textline_smallroman
                == retrieved_object.last_textline_smallroman
            ):
                Answer = False
            if not (
                textpart_object.last_textline_bigletter == retrieved_object.last_textline_bigletter
            ):
                Answer = False
            if not (
                textpart_object.last_textline_smallletter
                == retrieved_object.last_textline_smallletter
            ):
                Answer = False
            if not (textpart_object.last_textline_digit == retrieved_object.last_textline_digit):
                Answer = False
            if not (
                textpart_object.last_textline_signmark == retrieved_object.last_textline_signmark
            ):
                Answer = False

            # print reports:
            if Answer == False:
                print("\n ==> RAPPORT <enumeration test_newwrite>: comparison failed!\n")
                print(textpart_object.labelname + " " + textpart_object.documentname)
                print(retrieved_object.labelname + " " + retrieved_object.documentname)

            # perform the test:
            self.assertIs(Answer, True)

        # Done.


@tag("database", "unit")
class textalinea_newwrite_tests(TestCase):
    @tag("foreignkey")
    def test_default_foreignkey(self):
        """
        Unit test for get_default_foreignkey() of textalinea.
        # Parameters: none; # Returns (bool): succes of the text.
        # Author: Christiaan Douma
        """

        # Create the default foreign key:
        test_pk = db_textalinea.get_default_foreignkey()

        # Again; we are supposed to get the same answer then:
        test_pk2 = db_textalinea.get_default_foreignkey()

        # See that there is indeed an entry in the DB:
        test_queryset = db_textalinea.objects.filter(pk=test_pk)
        test_querylist = list(test_queryset)

        # Compare:
        Answer = False
        if len(test_querylist) == 1:
            retrieved_pk = test_querylist[0].id
            if retrieved_pk == test_pk:
                if test_pk == test_pk2:
                    Answer = True

        # Perform the test:
        self.assertIs(Answer, True)

        # Done.

    @tag("newwrite")
    def test_newwrite(self):
        """
        Unit test for a write-read operation that writes a new object to the DB:
        # Parameters: none; # Returns (bool): succes of the text.
        # Author: Christiaan Douma
        """

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

        # write it to the database:
        db_object = newwrite_textalinea(textpart_object)

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
                "\n ==> RAPPORT <textalinea test_newwrite>: The number of DB-entries was not as we expected!\n"
            )
            print(id_list)
            print(id_list_textpart)
            self.assertIs(True, False)
        else:
            # Then, obtain what should be the proper ID:
            properID = id_list[0]

            # retrieve the object from the database:
            retrieved_object = load_textalinea(properID)

            # Compare outputs:
            Answer = True

            # Check that we indeed have the correct object:
            if not (retrieved_object.labelname == "Alinea"):
                Answer = False
            if not (retrieved_object.documentname == textpart_object.documentname):
                Answer = False

            # Check the other values:
            if not (textpart_object.textlevel == retrieved_object.textlevel):
                Answer = False
            if not (textpart_object.typelevel == retrieved_object.typelevel):
                Answer = False
            if not (textpart_object.texttitle == retrieved_object.texttitle):
                Answer = False
            if not (textpart_object.nativeID == retrieved_object.nativeID):
                Answer = False
            if not (textpart_object.parentID == retrieved_object.parentID):
                Answer = False
            if not (textpart_object.horizontal_ordering == retrieved_object.horizontal_ordering):
                Answer = False
            if not (textpart_object.summary == retrieved_object.summary):
                Answer = False
            if not (textpart_object.sum_CanbeEmpty == retrieved_object.sum_CanbeEmpty):
                Answer = False
            if not (textpart_object.alineatype == retrieved_object.alineatype):
                Answer = False
            if not (textpart_object.enumtype == retrieved_object.enumtype):
                Answer = False
            if not (textpart_object.html_visualization == retrieved_object.html_visualization):
                Answer = False
            if not (textpart_object.summarized_wordcount == retrieved_object.summarized_wordcount):
                Answer = False
            if not (textpart_object.total_wordcount == retrieved_object.total_wordcount):
                Answer = False
            if not (textpart_object.nr_decendants == retrieved_object.nr_decendants):
                Answer = False
            if not (textpart_object.nr_children == retrieved_object.nr_children):
                Answer = False
            if not (textpart_object.nr_depths == retrieved_object.nr_depths):
                Answer = False
            if not (textpart_object.nr_pages == retrieved_object.nr_pages):
                Answer = False

            # print reports:
            if Answer == False:
                print("\n ==> RAPPORT <textalinea test_newwrite>: comparison failed!\n")
                print(textpart_object.labelname + " " + textpart_object.documentname)
                print(retrieved_object.labelname + " " + retrieved_object.documentname)

            # perform the test:
            self.assertIs(Answer, True)

        # Done.


@tag("database", "unit")
class Native_TOC_Element_newwrite_tests(TestCase):
    @tag("newwrite")
    def test_newwrite(self):
        """
        Unit test for a write-read operation that writes a new object to the DB:
        # Parameters: none; # Returns (bool): succes of the text.
        # Author: Christiaan Douma
        """

        # Create a nice example of a textpart Native_TOC_Element:
        textpart_object = textpart_Native_TOC_Element()
        textpart_object.cascadelevel = 1
        textpart_object.title = "Wat een leuk hoofdstuk"
        textpart_object.page = 2
        textpart_object.Xpos = 10.0
        textpart_object.Ypos = 11.0
        textpart_object.Zpos = 12.0

        # write it to the database:
        db_object = newwrite_Native_TOC_Element(textpart_object)

        # Next, retrieve the ID's. We test that, indeed nothing else is in the test-DB,
        # by testing that the length has to be exactly 1:
        id_list = list(db_Native_TOC_Element.objects.values_list("id", flat=True).order_by("id"))
        id_length = len(id_list)

        # Test if there is actually something in the DB now:
        if not (id_length == 1):
            print(
                "\n ==> RAPPORT <Native_TOC_Element test_newwrite>: The number of DB-entries was not as we expected!\n"
            )
            print(id_list)
            self.assertIs(True, False)
        else:
            # Then, obtain what should be the proper ID:
            properID = id_list[0]

            # retrieve the object from the database:
            retrieved_object = load_Native_TOC_Element(properID)

            # Compare outputs:
            Answer = True
            if not (textpart_object.cascadelevel == retrieved_object.cascadelevel):
                Answer = False
            if not (textpart_object.title == retrieved_object.title):
                Answer = False
            if not (textpart_object.page == retrieved_object.page):
                Answer = False
            if not (textpart_object.Xpos == retrieved_object.Xpos):
                Answer = False
            if not (textpart_object.Ypos == retrieved_object.Ypos):
                Answer = False
            if not (textpart_object.Zpos == retrieved_object.Zpos):
                Answer = False

            # print reports:
            if Answer == False:
                print("\n ==> RAPPORT <Native_TOC_Element test_newwrite>: comparison failed!\n")
                textpart_object.print_TOC_element()
                retrieved_object.print_TOC_element()

            # perform the test:
            self.assertIs(Answer, True)

        # Done.


@tag("database", "unit")
class textsplitter_newwrite_tests(TestCase):
    @tag("foreignkey")
    def test_default_foreignkey(self):
        """
        Unit test for get_default_foreignkey() of textsplitter.
        # Parameters: none; # Returns (bool): succes of the text.
        # Author: Christiaan Douma
        """

        # Create the default foreign key:
        test_pk = db_textsplitter.get_default_foreignkey()

        # Again; we are supposed to get the same answer then:
        test_pk2 = db_textsplitter.get_default_foreignkey()

        # See that there is indeed an entry in the DB:
        test_queryset = db_textsplitter.objects.filter(pk=test_pk)
        test_querylist = list(test_queryset)

        # Compare:
        Answer = False
        if len(test_querylist) == 1:
            retrieved_pk = test_querylist[0].id
            if retrieved_pk == test_pk:
                if test_pk == test_pk2:
                    Answer = True

        # Perform the test:
        self.assertIs(Answer, True)

        # Done.

    @tag("newwrite")
    def test_newwrite(self):
        """
        Unit test for a write-read operation that writes a new object to the DB:
        # Parameters: none; # Returns (bool): succes of the text.
        # Author: Christiaan Douma
        """

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

        # write it to the database:
        db_object = newwrite_textsplitter(textpart_object)
        db_object.owner = get_default_user()
        db_object.save()

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
            and (id_length_textpart == 9)
            and (id_length_title == 1)
            and (id_length_footer == 1)
            and (id_length_body == 1)
            and (id_length_headlines == 1)
            and (id_length_enumeration == 1)
            and (id_length_textalinea == 3)
            and (id_length_Native_TOC_Element == 2)
            and (id_length_breakdown_decisions == 3)
        ):
            print(
                "\n ==> RAPPORT <textsplitter test_newwrite>: The number of DB-entries was not as we expected!\n"
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
            # Then, obtain what should be the proper ID:
            properID = id_list[0]

            # retrieve the object from the database:
            retrieved_object = load_textsplitter(properID)

            # retrieve the object from the database, including the user
            retrieved_db_object = db_textsplitter.objects.get(pk=properID)
            # Compare outputs:
            Answer = True

            # Check that we have the correct user attached to the db object
            if not retrieved_db_object.owner.username == 'datalake':
                Answer = False
            if not retrieved_db_object.owner.email == 'dataloket@minienw.nl':
                Answer = False
            # a password is stored as a pbkdf2_sha256 hash, so we cannot compare string values
            if not retrieved_db_object.owner.check_password('nicelake'):
                Answer = False

            # Check that we indeed have the correct object:
            if not (retrieved_object.labelname == "TextSplitter"):
                Answer = False
            if not (retrieved_object.documentname == textpart_object.documentname):
                Answer = False

            # Textalineas:
            if not (len(retrieved_object.textalineas) == len(textpart_object.textalineas)):
                Answer = False
            else:
                for k in range(0, len(textpart_object.textalineas)):
                    if not textpart_object.textalineas[k].compare(retrieved_object.textalineas[k]):
                        Answer = False

            # breakdown_decisions:
            if not (
                len(retrieved_object.textclassification) == len(textpart_object.textclassification)
            ):
                Answer = False
            else:
                for k in range(0, len(textpart_object.textclassification)):
                    if not (
                        textpart_object.textclassification[k]
                        == retrieved_object.textclassification[k]
                    ):
                        Answer = False

            # Native_TOC_Elements:
            if not (len(retrieved_object.native_TOC) == len(textpart_object.native_TOC)):
                Answer = False
            else:
                for k in range(0, len(textpart_object.native_TOC)):
                    if not (
                        textpart_object.native_TOC[k].cascadelevel
                        == retrieved_object.native_TOC[k].cascadelevel
                    ):
                        Answer = False
                    if not (
                        textpart_object.native_TOC[k].title == retrieved_object.native_TOC[k].title
                    ):
                        Answer = False
                    if not (
                        textpart_object.native_TOC[k].page == retrieved_object.native_TOC[k].page
                    ):
                        Answer = False
                    if not (
                        textpart_object.native_TOC[k].Xpos == retrieved_object.native_TOC[k].Xpos
                    ):
                        Answer = False
                    if not (
                        textpart_object.native_TOC[k].Ypos == retrieved_object.native_TOC[k].Ypos
                    ):
                        Answer = False
                    if not (
                        textpart_object.native_TOC[k].Zpos == retrieved_object.native_TOC[k].Zpos
                    ):
                        Answer = False

            # 1-1 relations:
            if not (retrieved_object.title.labelname == "Title"):
                Answer = False
            if not (retrieved_object.title.documentname == textpart_object.title.documentname):
                Answer = False
            if not (retrieved_object.footer.labelname == "Footer"):
                Answer = False
            if not (retrieved_object.footer.documentname == textpart_object.footer.documentname):
                Answer = False
            if not (retrieved_object.body.labelname == "Body"):
                Answer = False
            if not (retrieved_object.body.documentname == textpart_object.body.documentname):
                Answer = False
            if not (retrieved_object.headlines.labelname == "Headlines"):
                Answer = False
            if not (
                retrieved_object.headlines.documentname == textpart_object.headlines.documentname
            ):
                Answer = False
            if not (retrieved_object.enumeration.labelname == "Enumeration"):
                Answer = False
            if not (
                retrieved_object.enumeration.documentname
                == textpart_object.enumeration.documentname
            ):
                Answer = False

            # Other data fields:
            if not (retrieved_object.VERSION == textpart_object.VERSION):
                Answer = False
            if not (retrieved_object.ratelimit_timeunit == textpart_object.ratelimit_timeunit):
                Answer = False
            if not (retrieved_object.ratelimit_calls == textpart_object.ratelimit_calls):
                Answer = False
            if not (retrieved_object.ratelimit_tokens == textpart_object.ratelimit_tokens):
                Answer = False
            if not (retrieved_object.Costs_price == textpart_object.Costs_price):
                Answer = False
            if not (retrieved_object.Costs_tokenportion == textpart_object.Costs_tokenportion):
                Answer = False
            if not (retrieved_object.api_rate_starttime == textpart_object.api_rate_starttime):
                Answer = False
            if not (retrieved_object.api_rate_currenttime == textpart_object.api_rate_currenttime):
                Answer = False
            if not (
                retrieved_object.api_rate_currenttokens == textpart_object.api_rate_currenttokens
            ):
                Answer = False
            if not (
                retrieved_object.api_rate_currentcalls == textpart_object.api_rate_currentcalls
            ):
                Answer = False
            if not (retrieved_object.callcounter == textpart_object.callcounter):
                Answer = False
            if not (retrieved_object.api_totalprice == textpart_object.api_totalprice):
                Answer = False
            if not (
                retrieved_object.api_wrongcalls_duetomaxwhile
                == textpart_object.api_wrongcalls_duetomaxwhile
            ):
                Answer = False
            if not (retrieved_object.html_visualization == textpart_object.html_visualization):
                Answer = False
            if not (retrieved_object.MaxSummaryLength == textpart_object.MaxSummaryLength):
                Answer = False
            if not (
                retrieved_object.summarization_threshold == textpart_object.summarization_threshold
            ):
                Answer = False
            if not (retrieved_object.UseDummySummary == textpart_object.UseDummySummary):
                Answer = False
            if not (retrieved_object.LanguageModel == textpart_object.LanguageModel):
                Answer = False
            if not (retrieved_object.BackendChoice == textpart_object.BackendChoice):
                Answer = False
            if not (retrieved_object.LanguageChoice == textpart_object.LanguageChoice):
                Answer = False
            if not (retrieved_object.LanguageTemperature == textpart_object.LanguageTemperature):
                Answer = False
            if not (retrieved_object.MaxCallRepeat == textpart_object.MaxCallRepeat):
                Answer = False
            if not (retrieved_object.doc_metadata_author == textpart_object.doc_metadata_author):
                Answer = False
            if not (retrieved_object.doc_metadata_creator == textpart_object.doc_metadata_creator):
                Answer = False
            if not (
                retrieved_object.doc_metadata_producer == textpart_object.doc_metadata_producer
            ):
                Answer = False
            if not (retrieved_object.doc_metadata_subject == textpart_object.doc_metadata_subject):
                Answer = False
            if not (retrieved_object.doc_metadata_title == textpart_object.doc_metadata_title):
                Answer = False
            if not (
                retrieved_object.doc_metadata_fullstring == textpart_object.doc_metadata_fullstring
            ):
                Answer = False

            # Print reports:
            if not Answer:
                print("\n ==> RAPPORT <textsplitter test_newwrite>: comparison failed!\n")
                print(textpart_object.labelname + " " + textpart_object.documentname)
                print(retrieved_object.labelname + " " + retrieved_object.documentname)

            # Perform the test:
            self.assertIs(True, Answer)

            # Done

    @tag("newwrite")
    def test_newwrite_nonunique(self):
        """
        Unit test for a write-read operation that writes a new object to the DB:
        # Parameters: none; # Returns (bool): succes of the text.
        # Author: Christiaan Douma
        """

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

        # write it to the database:
        db_object_1 = newwrite_textsplitter(textpart_object)

        # Write it to the database again:
        db_object_2 = newwrite_textsplitter(textpart_object)

        # Check that the first one is succesful:
        if "WRONG_OBJECT" in db_object_1.documentname:
            print(
                "textsplitter uniqueness newwrite test: We failed to write an object to the database that was not yet there!"
            )
            self.assertIs(True, False)

        # Check that the second one is NOT succesful:
        if not ("WRONG_OBJECT" in db_object_2.documentname):
            print(
                "textsplitter uniqueness newwrite test: We did not get an error message when writing an object to the database that was already there!"
            )
            self.assertIs(True, False)

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

        # Test if there is exactly one quantity of textsplitter in the DB:
        if not (
            (id_length == 1)
            and (id_length_textpart == 9)
            and (id_length_title == 1)
            and (id_length_footer == 1)
            and (id_length_body == 1)
            and (id_length_headlines == 1)
            and (id_length_enumeration == 1)
            and (id_length_textalinea == 3)
            and (id_length_Native_TOC_Element == 2)
            and (id_length_breakdown_decisions == 3)
        ):
            print(
                "\n ==> RAPPORT <textsplitter test_newwrite>: The number of DB-entries was not as we expected!\n"
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
            # then, we are good:
            self.assertIs(True, True)

            # Done
