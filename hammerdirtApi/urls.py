"""hammerdirt_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import include
from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from hammerdirtApi.views import (
    CodeList,
    CodeDetail,
    BeachList,
    SurveyList,
    UserData,
    ViewLitterDataPieces,
    ViewBeachesByCategory,
    ViewCodeTotalsByBeachAndDay,
    ViewCodeTotals,
    ViewBeachCategories,
    ViewWaterBodyCodeTotals,
    ViewCityCodeTotals,
    ViewPostCodeTotals,
    ArticleCreate,
    ArticleListView,
    ArticleUpdate,
    ArticleCommentView,
    ArticleCommentCreate,
    ViewArticleSearchCriteria,
    ViewLatestInventories,
    AreWeHere,
    DimDataView,
    DimDataCreate,
)
urlpatterns = [
    path('article-view/', ArticleListView.as_view(), name="list-articles"),
    path('article-search/',ViewArticleSearchCriteria.as_view(), name='article-search'),
    path('article-update/<slug>', ArticleUpdate.as_view()),
    path('article-comment/',ArticleCommentView.as_view(), name='article-comment'),
    path('article-comment/create/', ArticleCommentCreate.as_view(), name='article-comment-create' ),
    path('are-we-online/', AreWeHere.as_view(), name='are-we-here'),
    path('code-totals/water-bodies/', ViewWaterBodyCodeTotals.as_view(), name="water-body-code-totals"),
    path('code-totals/cities/', ViewCityCodeTotals.as_view(), name="city-code-totals"),
    path('code-totals/post-code/', ViewPostCodeTotals.as_view(), name="postal-code-totals"),
    path('create-article/', ArticleCreate.as_view(), name='comment-create'),
    path('hd-auth/', include("djoser.urls.base")),
    path('hd-auth/', include("djoser.urls.authtoken")),
    path('hd-auth/', include("djoser.urls.jwt")),
    path('list-of-beaches/', BeachList.as_view(), name='list_of_beaches'),
    path('list-of-beaches/by-category/', ViewBeachesByCategory.as_view(), name='beaches-by-location'),
    path('list-of-beaches/categories/', ViewBeachCategories.as_view(), name='category-groups'),
    path('mlw-codes/list/', CodeList.as_view(), name="mlw-code-list"),
    path('mlw-codes/detail/<code>', CodeDetail.as_view(), name='code-detail'),
    path('surveys/', SurveyList.as_view(), name='enter-survey'),
    path('surveys/dim-data/dim-data-create/', DimDataCreate.as_view(), name='dim-data-create'),
    path('surveys/daily-totals/', ViewLitterDataPieces.as_view(), name="pcs-m-day"),
    path('surveys/daily-totals/code-totals/', ViewCodeTotalsByBeachAndDay.as_view(), name="code-results"),
    path('surveys/daily-totals/code-totals/daily-totals/', ViewLatestInventories.as_view(), name="latest-daily-total"),
    path('users/', UserData.as_view()),
]
