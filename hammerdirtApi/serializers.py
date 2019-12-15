from rest_framework import serializers
from hammerdirtApi.models import (
    Codes,
    Beaches,
    LitterDataPieces,
    PiecesPerMeterLocation,
    DraftArticles,
    ArticleComment,
    SurveyAdminData
)
from django.contrib.auth import get_user_model


class ArticleCommentSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = ArticleComment
        fields = '__all__'
class CodesSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Codes
        fields = [
            'code',
            'material',
            'description',
            'source',
            'owner'
            ]
class DimDataSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = SurveyAdminData
        fields = '__all__'

class BeachesSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Beaches
        fields = [
            "location",
            "latitude",
            "longitude",
            "city",
            "post",
            "country",
            "water",
            "water_name",
            "slug",
            "city_slug",
            "water_name_slug",
            "owner"
            ]
class SurveySerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    print("called serializer")
    class Meta:
        model = LitterDataPieces
        fields = '__all__'
class GetUserData(serializers.ModelSerializer):
    lookup_field="username"
class ViewCustomUserSerializer(GetUserData):
    class Meta:
        model = get_user_model()
        exclude = ('password', 'is_superuser', 'is_active', 'is_staff')

class LocationCodesTotalSerializer(serializers.Serializer):
    location__water_name = serializers.CharField(max_length=200)
    code = serializers.CharField(max_length=20)
    total = serializers.IntegerField()
    class Meta:
        fields=["location__water_name", "code", "total"]
class CityCodesTotalSerializer(serializers.Serializer):
    location__city = serializers.CharField(max_length=200)
    code = serializers.CharField(max_length=20)
    total = serializers.IntegerField()
class PostCodesTotalSerializer(serializers.Serializer):
    location__post = serializers.CharField(max_length=200)
    code = serializers.CharField(max_length=20)
    total = serializers.IntegerField()
class BeachPcsMeterSerializer(serializers.Serializer):
    location = serializers.CharField(max_length=100)
    daily_pcsm = serializers.DecimalField(max_digits=6, decimal_places=2)
    date = serializers.DateField()
class DraftArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = DraftArticles
        fields = '__all__'
