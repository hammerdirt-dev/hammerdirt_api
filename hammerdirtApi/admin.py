from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import (
    CustomUser,
    Beaches,
    Codes,
    LitterDataPieces,
    References,
    DraftArticles,
    ArticleComment,
    SurveyAdminData
)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    filter_horizontal = ('groups', 'user_permissions')
    fieldsets = (
        ('User', {'fields':
                    ('username',
                     'first_name',
                     'last_name',
                     'email',
                     'about',
                     'why',
                     'avatar',
                     'position',
                     'hd_status',
                     'user_twitter',
                     'date_joined'),
                     }),
         ('Permissions',{'fields':('groups','is_staff','is_active', 'is_superuser', 'user_permissions')})
        )
admin.site.register(CustomUser, CustomUserAdmin)
class LocationFilter(SimpleListFilter):
    title = 'Location of interest' # a label for our filter
    parameter_name = 'pages' # you can put anything here
    list_of_lakes = Beaches.objects.order_by().values_list('water_name', flat=True).distinct()
    print(len(list_of_lakes))
    print(list_of_lakes)
    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        my_list = [(x, (x)) for x in self.list_of_lakes]
        my_list_sorted = sorted(my_list)
        return my_list_sorted

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        return queryset.filter(water_name=self.value())

class BeachesAdmin(admin.ModelAdmin):
    list_filter = ('water_name',)
    search_fields = ['city','water_name']
    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        super().save_model(request, obj, form, change)
    readonly_fields = ('owner', 'slug', 'water_name_slug', 'city_slug')
admin.site.register(Beaches, BeachesAdmin)

class CodesAdmin(admin.ModelAdmin):
    search_fields = ['code', 'material', 'source','description']
    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        super().save_model(request, obj, form, change)
    readonly_fields = ('owner',)
admin.site.register(Codes, CodesAdmin)

class LitterDataPiecesAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "code":
            kwargs["queryset"] = Codes.objects.order_by('code')
        return super(LitterDataPiecesAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
    search_fields = ['date','location__water_name_slug','location__city_slug', 'location__location']
    list_filter = ('owner','location__water_name')
    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        super().save_model(request, obj, form, change)
    readonly_fields = ('owner',)
admin.site.register(LitterDataPieces, LitterDataPiecesAdmin)

class ReferencesAdmin(admin.ModelAdmin):
    search_fields = ('title', )
    list_filter = ('owner',  )
    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        super().save_model(request, obj, form, change)
    readonly_fields = ('owner','slug')
admin.site.register(References, ReferencesAdmin)

class DraftArticlesAdmin(admin.ModelAdmin):
    search_fields = ('subject', )
    list_filter =('owner','subject' )
    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        super().save_model(request, obj, form, change)
    readonly_fields = ('owner','slug')
admin.site.register(DraftArticles, DraftArticlesAdmin)
class SurveyAdminDataAdmin(admin.ModelAdmin):
    search_fields = ('location', )
    list_filter =('owner','location' )
    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        super().save_model(request, obj, form, change)
    readonly_fields = ('owner','survey_key')
admin.site.register(SurveyAdminData, SurveyAdminDataAdmin)

class ArticleCommentAdmin(admin.ModelAdmin):
    search_fields = ('subject', 'disposition')
    list_filter=('owner','disposition')
    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        super().save_model(request, obj, form, change)
    readonly_fields = ('owner',)
admin.site.register(ArticleComment, ArticleCommentAdmin)
