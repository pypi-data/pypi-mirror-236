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
from .newwrites import newwrite_textsplitter
from .deletes import delete_textsplitter
from .overwrites import overwrite_textsplitter

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

# Import testing tools:
from pdftextsplitter import AlineasPresent


# Creation of the test classes:
@tag("database", "integration")
class story_docs_inDB_tests(TestCase):
    def test_SplitDoc(self):
        # Perform the SplitDoc test:
        thetest = textpart_textsplitter()
        thetest.set_documentpath("./djangotextsplitter/Source/")
        thetest.set_documentname("SplitDoc")
        thetest.set_outputpath("./djangotextsplitter/Source/")
        thetest.standard_params()
        thetest.set_UseDummySummary(True)
        thetest.process(-1)  # NOTE: This is Django-mode, as it should be in these tests!

        # Now, store it in the DB:
        db_object = newwrite_textsplitter(thetest)

        # Next, obtain a search:
        id_list = list(
            db_textsplitter.objects.filter(documentname="SplitDoc")
            .values_list("id", flat=True)
            .order_by("id")
        )
        if not (len(id_list) == 1):
            print(
                " ==> SplitDoc integration write/load test --> We wrote an object, but we could not find it back"
            )
            self.assertIs(False, True)
        else:
            # Then, load it back:
            retrieved_object = load_textsplitter(id_list[0])

            # Next, test if all alineas exist:
            Answer = AlineasPresent(thetest.textalineas, retrieved_object.textalineas)

            # Test if the html-visualization works:
            html_comparison = thetest.html_visualization == retrieved_object.html_visualization
            if not html_comparison:
                Answer = False
                print(
                    " ==> SplitDoc integration write/load test --> SplitDoc HTML Comparison failed."
                )

            # Next, attempt to overwrite our object:
            thetest.set_MaxSummaryLength(3)
            thetest.process(-1)
            db_object_2 = overwrite_textsplitter(id_list[0], thetest)

            # Then, delete our object:
            delete_textsplitter(id_list[0])

            # Then, check if we actually are left with a clean database:
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
            id_list_headlines = list(
                db_headlines.objects.values_list("id", flat=True).order_by("id")
            )
            id_length_headlines = len(id_list_headlines)

            # Eliminate presence of default foreign key object:
            for k in range(0, id_length_headlines):
                Index = id_length_headlines - k - 1
                if (
                    load_headlines(id_list_headlines[Index]).labelname
                    == "default_foreign_key_object"
                ):
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
            id_list_textalinea = list(
                db_textalinea.objects.values_list("id", flat=True).order_by("id")
            )
            id_length_textalinea = len(id_list_textalinea)

            # Eliminate presence of default foreign key object:
            for k in range(0, id_length_textalinea):
                Index = id_length_textalinea - k - 1
                if (
                    load_textalinea(id_list_textalinea[Index]).labelname
                    == "default_foreign_key_object"
                ):
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

            # Also test for fontregions:
            id_list_fontregion = list(
                db_fontregion.objects.values_list("id", flat=True).order_by("id")
            )
            id_length_fontregion = len(id_list_fontregion)

            # Also test for lineregions:
            id_list_lineregion = list(
                db_lineregion.objects.values_list("id", flat=True).order_by("id")
            )
            id_length_lineregion = len(id_list_lineregion)

            # Also test for lineregions:
            id_list_readingline = list(
                db_readingline.objects.values_list("id", flat=True).order_by("id")
            )
            id_length_readingline = len(id_list_readingline)

            # Also test for lineregions:
            id_list_readinghistogram = list(
                db_readinghistogram.objects.values_list("id", flat=True).order_by("id")
            )
            id_length_readinghistogram = len(id_list_readinghistogram)

            # Also test for headlines_hierarchy:
            id_list_headlines_hierarchy = list(
                db_headlines_hierarchy.objects.values_list("id", flat=True).order_by("id")
            )
            id_length_headlines_hierarchy = len(id_list_headlines_hierarchy)

            # Also test for enumeration_hierarchy:
            id_list_enumeration_hierarchy = list(
                db_enumeration_hierarchy.objects.values_list("id", flat=True).order_by("id")
            )
            id_length_enumeration_hierarchy = len(id_list_enumeration_hierarchy)

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
                and (id_length_fontregion == 0)
                and (id_length_lineregion == 0)
                and (id_length_readingline == 0)
                and (id_length_readinghistogram == 0)
                and (id_length_headlines_hierarchy == 0)
                and (id_length_enumeration_hierarchy == 0)
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
                print(id_list_fontregion)
                print(id_list_lineregion)
                print(id_list_readingline)
                print(id_list_readinghistogram)
                print(id_list_headlines_hierarchy)
                print(id_list_enumeration_hierarchy)
                self.assertIs(True, False)
            else:
                # then, we are good:
                self.assertIs(True, Answer)

    def test_LineTest2(self):
        # Perform the LineTest2 test:
        thetest = textpart_textsplitter()
        thetest.set_documentpath("./djangotextsplitter/Source/")
        thetest.set_documentname("LineTest2")
        thetest.set_outputpath("./djangotextsplitter/Source/")
        thetest.standard_params()
        thetest.set_UseDummySummary(True)
        thetest.process(-1)  # NOTE: This is Django-mode, as it should be in these tests!

        # Now, store it in the DB:
        db_object = newwrite_textsplitter(thetest)

        # Next, obtain a search:
        id_list = list(
            db_textsplitter.objects.filter(documentname="LineTest2")
            .values_list("id", flat=True)
            .order_by("id")
        )
        if not (len(id_list) == 1):
            print(
                " ==> LineTest2 integration write/load test --> We wrote an object, but we could not find it back"
            )
            self.assertIs(False, True)
        else:
            # Then, load it back:
            retrieved_object = load_textsplitter(id_list[0])

            # Next, test if all alineas exist:
            Answer = AlineasPresent(thetest.textalineas, retrieved_object.textalineas)

            # Test if the html-visualization works:
            html_comparison = thetest.html_visualization == retrieved_object.html_visualization
            if not html_comparison:
                Answer = False
                print(
                    " ==> LineTest2 integration write/load test --> LineTest2 HTML Comparison failed."
                )

            # Next, attempt to overwrite our object:
            thetest.set_MaxSummaryLength(3)
            thetest.process(-1)
            db_object_2 = overwrite_textsplitter(id_list[0], thetest)

            # Then, delete our object:
            delete_textsplitter(id_list[0])

            # Then, check if we actually are left with a clean database:
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
            id_list_headlines = list(
                db_headlines.objects.values_list("id", flat=True).order_by("id")
            )
            id_length_headlines = len(id_list_headlines)

            # Eliminate presence of default foreign key object:
            for k in range(0, id_length_headlines):
                Index = id_length_headlines - k - 1
                if (
                    load_headlines(id_list_headlines[Index]).labelname
                    == "default_foreign_key_object"
                ):
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
            id_list_textalinea = list(
                db_textalinea.objects.values_list("id", flat=True).order_by("id")
            )
            id_length_textalinea = len(id_list_textalinea)

            # Eliminate presence of default foreign key object:
            for k in range(0, id_length_textalinea):
                Index = id_length_textalinea - k - 1
                if (
                    load_textalinea(id_list_textalinea[Index]).labelname
                    == "default_foreign_key_object"
                ):
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

            # Also test for fontregions:
            id_list_fontregion = list(
                db_fontregion.objects.values_list("id", flat=True).order_by("id")
            )
            id_length_fontregion = len(id_list_fontregion)

            # Also test for lineregions:
            id_list_lineregion = list(
                db_lineregion.objects.values_list("id", flat=True).order_by("id")
            )
            id_length_lineregion = len(id_list_lineregion)

            # Also test for lineregions:
            id_list_readingline = list(
                db_readingline.objects.values_list("id", flat=True).order_by("id")
            )
            id_length_readingline = len(id_list_readingline)

            # Also test for lineregions:
            id_list_readinghistogram = list(
                db_readinghistogram.objects.values_list("id", flat=True).order_by("id")
            )
            id_length_readinghistogram = len(id_list_readinghistogram)

            # Also test for headlines_hierarchy:
            id_list_headlines_hierarchy = list(
                db_headlines_hierarchy.objects.values_list("id", flat=True).order_by("id")
            )
            id_length_headlines_hierarchy = len(id_list_headlines_hierarchy)

            # Also test for enumeration_hierarchy:
            id_list_enumeration_hierarchy = list(
                db_enumeration_hierarchy.objects.values_list("id", flat=True).order_by("id")
            )
            id_length_enumeration_hierarchy = len(id_list_enumeration_hierarchy)

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
                and (id_length_fontregion == 0)
                and (id_length_lineregion == 0)
                and (id_length_readingline == 0)
                and (id_length_readinghistogram == 0)
                and (id_length_headlines_hierarchy == 0)
                and (id_length_enumeration_hierarchy == 0)
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
                print(id_list_fontregion)
                print(id_list_lineregion)
                print(id_list_readingline)
                print(id_list_readinghistogram)
                print(id_list_headlines_hierarchy)
                print(id_list_enumeration_hierarchy)
                self.assertIs(True, False)
            else:
                # then, we are good:
                self.assertIs(True, Answer)
