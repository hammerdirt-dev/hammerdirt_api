"""
Views for the hammerdirt API:

These views are for the hammerdirt web app and api.


"""
from django.shortcuts import render
from django.contrib.auth import get_user_model
from .serializers import (
    CodesSerializer,
    BeachesSerializer,
    SurveySerializer,
    ViewCustomUserSerializer,
    LocationCodesTotalSerializer,
    CityCodesTotalSerializer,
    PostCodesTotalSerializer,
    BeachPcsMeterSerializer,
    DraftArticleSerializer,
    ArticleCommentSerializer,
    DimDataSerializer
)
import json
from .models import (
    Codes,
    Beaches,
    LitterDataPieces,
    PiecesPerMeterLocation,
    BeachesByCategory,
    # ReferencesOutput,
    DraftArticles,
    ArticleSearchCriteria,
    ArticleComment,
    SurveyAdminData,
    SurveyAdminViews
)
from rest_framework.renderers import JSONRenderer
from rest_framework import (
    generics
)
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import (
    APIView
)
from rest_framework.response import Response
from rest_framework.permissions import (
    BasePermission,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
    SAFE_METHODS
)
def api_home(request):
     return render(request,'api-home.html')
class AreWeHere(APIView):
    def get(self, request, *args, **kwargs):
        on_or_not =  [{"status":"true", "reply":"You can proceed"}]
        return Response(on_or_not)


# Generic api views from drf
class CodeCreate(generics.CreateAPIView):
    """
    Accepts a post method to create new MLW code objects.

    react variable = None
    """
    permission_classes = [IsAuthenticated]
    queryset = Codes.objects.all()
    serializer_class = CodesSerializer
class DimDataCreate(generics.CreateAPIView):
    """
    Accepts a post method to create dimensional data for a survey.

    """
    permission_classes = [IsAuthenticated]
    queryset = SurveyAdminData.objects.all()
    serializer_class = DimDataSerializer
class ArticleCreate(generics.CreateAPIView):
    """
    Accepts a post method to create new articles.
    """
    permission_classes = [IsAuthenticated]
    queryset = DraftArticles.objects.all()
    serializer_class = DraftArticleSerializer
class ArticleUpdate(generics.RetrieveUpdateAPIView):
    """
    Accepts a put method to update existing articles.
    """
    permission_classes = [IsAuthenticated]
    queryset = DraftArticles.objects.all()
    lookup_field = "slug"
    serializer_class = DraftArticleSerializer

class ArticleListView(generics.ListAPIView):
    """
    Returns an array of article objects:

    {
        "title": "The article title",
        "subject": "The article subject",
        "article": "The actual article contents",
        "image": "title image"
        "summary": "summary for article cards and intro",
        "references": "Data science par la pratique",
        "slug": "the-article-title"
    }...{"For all articles in the database"}
    """
    queryset = DraftArticles.objects.all().order_by('-date_created')
    serializer_class = DraftArticleSerializer
class ArticleCommentView(APIView):
    """
    Returns an array of article-comment objects:

    """
    def get(self, request, *args, **kwargs):
        comments = list(ArticleComment.objects.values('owner', 'doc_title', 'disposition', 'comment', 'subject', 'comment_date'))
        return Response(comments)


    queryset = ArticleComment.objects.all()
    serializer_class = ArticleCommentSerializer
class ArticleCommentCreate(generics.CreateAPIView):
    """
    Accepts a put method to create comments.
    """
    permission_classes = [IsAuthenticated]
    queryset = ArticleComment.objects.all()
    serializer_class = ArticleCommentSerializer

class CodeList(generics.ListAPIView):
    """
    Returns an array of MLW code objects:

    {
        "code": "G213",
        "material": "Chemicals",
        "description": "Paraffin wax",
        "source": "Recreation"
    },...{"For every code in the library"}
    """
    queryset = Codes.objects.all()
    serializer_class = CodesSerializer
class CodeDetail(generics.RetrieveAPIView):
    """
    Returns the detail for one MLW code object:

    {
    "code": "G213",
    "material": "Chemicals",
    "description": "Paraffin wax",
    "source": "Recreation"
    }
    """
    queryset = Codes.objects.all()
    lookup_field = "code"
    serializer_class = CodesSerializer
class BeachList(generics.ListAPIView):
    """
    Returns an array of survey location objects:

    [{
        "location": "A l ombre",
        "latitude": "43.81119100",
        "longitude": "4.64817800",
        "city": "Beaucaire",
        "post": "30032",
        "country": "FR",
        "water": "r",
        "water_name": "Rhï¿½ne en aval",
        "slug": "a-l-ombre",
        "city_slug": "beaucaire",
        "water_name_slug": "rhone-en-aval"
        },...{"For every location with a survey"}]

    react variable: LIST_OF_BEACHES
    """
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Beaches.objects.all()
    serializer_class = BeachesSerializer
class BeachDetail(generics.RetrieveAPIView):
    """
    Returns one survey location object:

    {
        "location": "A l ombre",
        "latitude": "43.81119100",
        "longitude": "4.64817800",
        "city": "Beaucaire",
        "post": "30032",
        "country": "FR",
        "water": "r",
        "water_name": "Rhï¿½ne en aval",
        "slug": "a-l-ombre",
        "city_slug": "beaucaire",
        "water_name_slug": "rhone-en-aval"
        }

    react variable: None
    """
    queryset = Beaches.objects.all()
    serializer_class = BeachesSerializer
class BeachCreate(generics.CreateAPIView):
    """
    Accepts a post method to create a new survey location.
    """
    permission_classes = [IsAuthenticated]
    queryset = Beaches.objects.all()
    serializer_class = BeachesSerializer
class SurveyList(generics.CreateAPIView):
    """
    Accepts a post method that accepts an array of survey results.
    """
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = SurveySerializer
    print("called survey list")
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data)
class UserData(generics.ListAPIView):
    """
    Returns an array of user objects:

    [{
        "id": 1,
        "username": "AnonymousUser",
        "about": "",
        "why": "Provided no reason",
        "avatar": null,
        "image_url": "",
        "position": "hd-assoc",
        "hd_status": "hd-assoc",
        "user_twitter": "",
        "is_staff": false,
        "is_active": true,
        "groups": [],
        "user_permissions": []
    },...{"For every user in the group"}]

    """
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = get_user_model().objects.filter(is_active=True)
    serializer_class = ViewCustomUserSerializer


# Custom views for the app
# these views generate JSON objects for indexedDB
# the results are processed by the front end
# ther are not attached to a serializer

class ViewPostCodeTotals(APIView):
    """
    Returns an array of post-code code total objects. Each object contains the total count for the MLW
    codes indentified within a postal-code:

    [{
    "location": "1000", //Postal code
    "results": [
       {
           "code": "G100",
           "total": 185
       },
       {
           "code": "G11",
           "total": 11
       } .... {"for all MLW codes identified within the postal-code"},
    }...("For all postal codes")]

    """
    daily_totals = PiecesPerMeterLocation.post_code_totals.all()
    def get(self, request, *args, **kwargs):
        pieces = self.daily_totals
        def make_dict(self,a):
            new={}
            for element in a:
                if element['location__post'] in list(new.keys()):
                    new[element['location__post']].append({'code':element['code'], 'total':element['total']})
                else:
                    new.update({element['location__post']:[{'code':element['code'], 'total':element['total']}]})
            return new
        piecesX = make_dict(self, pieces)
        pieceKeys = list(piecesX.keys())
        theJson = [{'location':x, 'results':piecesX[x]} for x in pieceKeys]
        return Response(theJson)
class ViewCityCodeTotals(APIView):
    """
    Returns an array of city code total objects. Each object contains the total count for the MLW
    codes indentified within a city limit:

    [{
        "location": "Montreux", //name of the city
        "results": [
           {
               "code": "G100",
               "total": 185
           },
           {
               "code": "G11",
               "total": 11
           } .... {"for all MLW codes identified within city limits"},
        }..{"for all cities"}]

    """
    daily_totals = PiecesPerMeterLocation.city_code_totals.all()
    def get(self, request, *args, **kwargs):
        pieces = self.daily_totals
        def make_dict(self,a):
            new={}
            for element in a:
                if element['location__city'] in list(new.keys()):
                    new[element['location__city']].append({'code':element['code'], 'total':element['total']})
                else:
                    new.update({element['location__city']:[{'code':element['code'], 'total':element['total']}]})
            return new
        piecesX = make_dict(self, pieces)
        pieceKeys = list(piecesX.keys())
        theJson = [{'location':x, 'results':piecesX[x]} for x in pieceKeys]
        return Response(theJson)
class ViewWaterBodyCodeTotals(APIView):
    """
    Returns an array of water body code total objects. Each object contains the total count for the MLW
    codes indentified on the shores of the requested body of water:

    [{
        "location": "Lac Léman",// name of water body
        "results": [
           {
               "code": "G100",
               "total": 375
           },
           {
               "code": "G11",
               "total": 10
           } .... {"for all MLW codes identified on a body of water"},
     }...{"for all water bodies"}]
    """
    daily_totals = PiecesPerMeterLocation.location_code_totals.all()
    def get(self, request, *args, **kwargs):
        pieces = self.daily_totals
        def make_dict(self,a):
            new={}
            for element in a:
                if element['location__water_name'] in list(new.keys()):
                    new[element['location__water_name']].append({'code':element['code'], 'total':element['total']})
                else:
                    new.update({element['location__water_name']:[{'code':element['code'], 'total':element['total']}]})
            return new
        piecesX = make_dict(self, pieces)
        pieceKeys = list(piecesX.keys())
        theJson = [{'location':x, 'results':piecesX[x]} for x in pieceKeys]
        return Response(theJson)
class ViewLitterDataPieces(APIView):
    """
    Returns an array of location daily total objects. Each object contains the total pcs_m per survey:

    [{
        "location": "baye-de-montreux-g",
        "results": [
             [
                 "2015-11-23", // day of survey
                 5.75 // pieces per meter
             ],
             [
                 "2015-12-04",
                 8.4
             ]
        ]
    },...{"For every location with a survey"}]
    """
    daily_totals = PiecesPerMeterLocation.beach_daily_pcsM.all()
    def get(self, request, *args, **kwargs):
        pieces = self.daily_totals
        def make_dict(self,a):
            new={}
            for element in a:
                if element['location'] in list(new.keys()):
                    new[element['location']].append([element['date'], element['daily_pcsm']])
                else:
                    new.update({element['location']:[[element['date'], element['daily_pcsm']]]})
            return new
        piecesX = make_dict(self, pieces)
        pieceKeys = list(piecesX.keys())
        theJson = [{'location':x, 'results':piecesX[x]} for x in pieceKeys]
        return Response(theJson)
class ViewBeachesByCategory(APIView):
    """Returns an array of grouped beach objects. The beaches are grouped according to different criteria:

    [{
        "location": "Rhône en aval", // the body of water
        "beaches": [ // the survey locations at that body of water
         "a-l-ombre",
         "a-lombre",
         "antimonie",
         "antinomie",
         "bonaparte",
         "des-fougeres",
         "herbes-1001",
         "la-cavalerie",
         "la-rampe",
         "les-bercails",
         "mad-max"
        ]
    },...{"For every city, postal-code and body of water"}]
    """
    beaches_and_categories = BeachesByCategory.beaches_and_categories.all()
    def get(self, request, *args, **kwargs):
        beaches = self.beaches_and_categories
        def make_dict(self,a,n):
            new={}
            for element in a:
             if element[n] in new.keys():
                 new[element[n]].append(element[4])
             else:
                 new.update({element[n]:[element[4]]})
            return new
        def combined(self):
            new = {}
            for i in [0,1,2,3]:
              a_dict = make_dict(self, beaches, i)
              new.update(a_dict)
            return new
        these_beaches = combined(self)
        location_keys = these_beaches.keys()
        places_beaches = [{'location':x, 'beaches':these_beaches[x]} for x in location_keys]
        return Response(places_beaches)
class ViewCodeTotalsByBeachAndDay(APIView):
    """
    Returns an array of nested dicts of survey results grouped by location, date and code:
    [
    {
        "location": "baye-de-montreux-g",
        "dailyTotals": [
            {
                "date": "2015-11-23",
                "code": "G100",
                "pcs_m": 0.02,
                "quantity": 1
            },
            {
                "date": "2015-11-23",
                "code": "G11",
                "pcs_m": 0.02,
                "quantity": 1
            },... {"For each code"}
        ]
    },...{"For each beach"}
    """
    daily_totals = PiecesPerMeterLocation.code_data.all()
    def get(self, request, *args, **kwargs):
        pieces = self.daily_totals
        def make_dict(self,a):
            new={}
            location ={}
            for element in a:
                if element[0] in new.keys():
                    new[element[0]].append({"date":element[1], "code":element[2], "pcs_m":element[3], "quantity":element[4]})
                else:
                    new.update({element[0]:[{"date":element[1], "code":element[2], "pcs_m":element[3], "quantity":element[4]}]})
            the_new_keys = list(new.keys())
            out = [{"location":x, "dailyTotals":new[x]} for x in the_new_keys]
            # out = [new]
            return out
        pieces = make_dict(self, pieces)
        serializer = pieces
        return Response(serializer)
class ViewBeachCategories(APIView):
    """
    Returns  a list of dicts [{lakes:[list of all the lakes by name]},...{cities:[list of all...]}]

    [{
        "category": "lakes", // grouping level
        "results": [ // objects that correspond
        "Bielersee",
        "Bodensee",
        "Greifensee",
        "Katzensee",
        "Lac Lï¿½man",
        "Neuenburgersee",
        "not official",
        "Quatre Cantons",
        "Schiffenensee",
        "Sempachsee",
        "Sihlsee",
        "Thunersee",
        "Untersee",
        "Walensee",
        "Zugersee",
        "Zurichsee"
        ]
    },...{"For each:postal-code, rivers, lakes, cities"}]

    """
    rivers = list(BeachesByCategory.rivers.all())
    lakes = list(BeachesByCategory.lakes.all())
    cities = list(BeachesByCategory.cities.all())
    postal = list(BeachesByCategory.postal_codes.all())
    def get(self, request, *args, **kwargs):
        def make_dict(self):
            the_dict = [{
                'category':'lakes',
                'results':self.lakes
                },
                {
                'category':'cities',
                'results':self.cities
                },
                {
                'category':'post',
                'results':self.postal
                },
                {
                'category':'rivers',
                'results':self.rivers
                }]
            return the_dict
        data = make_dict(self)
        return Response(data)
class ViewArticleSearchCriteria(APIView):
    """
    Returns a nested dict a list of dicts =
    [
        {article_title:"a title", article_subject:"subject", article_slug:"slug", article_owner:"owner"}

    ]

    """
    articles = list(ArticleSearchCriteria.article_search_criteria.all())
    def get(self, request, *args, **kwargs):
        the_list = self.articles
        return Response(the_list)
class ViewCodeTotals(APIView):
    """
    Returns a nested dict {{"beach-name":{"code":total, "code":total}}...}
    """
    code_totals = list(PiecesPerMeterLocation.location_code_totals.all())
    def get(self, request, *args, **kwargs):
        def group_codes(self, a):
            new = []
            for el in a:
                new.append({
                    "location":el['location'],
                    "waterName":el["location__water_name"],
                    "cityName":el["location__city"],
                    "postCode":el["location__post"],
                    "code":el['code'],
                    "total":el['total'],
                    "date":el['date']
                    })

            return new
        grouped_totals = group_codes(self, self.code_totals)
        json_ed = json.dumps(grouped_totals)
        return Response(grouped_totals)
class ViewLatestInventories(APIView):
    """
    Returns a nested dict returns the last three survey totals.
    """
    daily_total = list(PiecesPerMeterLocation.beach_daily_quantity.all())
    def get(self, request, *args, **kwargs):
        last_three = self.daily_total[:3]
        return Response(last_three)
class DimDataView(APIView):

    def get(self, request, *args, **kwargs):
        dim_data = list(SurveyAdminViews.basic_data.all())
        # grouped_totals = group_codes(self, self.code_totals)
        # json_ed = json.dumps(grouped_totals)
        return Response(dim_data)
