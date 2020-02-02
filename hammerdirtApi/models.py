from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify
import datetime
from django.db.models import Sum, Avg, Max, Min, F
from django_mysql.models import JSONField
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
PARTICIPATING = [
    ("stopp", "Stop Plastic"),
    ("hd", "hammerdirt!"),
    ("wwf", "World Wildlife Fund"),
    ("pp", "Precious Plastic Léman"),
    ("eg", "Ecole International Genève"),
    ("ha", "Hackuarium"),
    ("asl", "Association Sauvegarde du Léman"),
]
PROJECT = [
    ("SLR", "Swiss Litter Report"),
    ("MCBP", "Montreux Clean Beach"),
    ("GL", "Grand Lac"),
    ("2020", "Project 2020"),
]
class CustomUser(AbstractUser):
    def user_image_path(instance, filename):
        a = slugify(instance.username)
        return '{0}/{1}'.format(a, filename)

    roles = [("part-rel", "Partner relations"),
             ("dev-iot", "IoT developer"),
             ("dev-py", "Python developer"),
             ("dev-js", "JavaScript developer"),
             ("res-lit", "Literature review"),
             ("ed-cont", "Education and training"),
             ("ops-csr", "Environmental responsibility"),
             ("fin-accts", "Accounts payable/recievable"),
             ("ops-bus", "Business operations"),
             ("ops-dev", "Dev-ops"),
             ("spB","Beach-sponsor" ),
             ("inB", "Beach-litter inventory"),
             ("dev-quant", "Quant developer"),
             ("survey", "Environmental surveyor")
             ]
    status = [("hd-assoc", "Hammerdirt associate"),
              ("hd-staff", "Hammerdirt staff"),
              ("hd-part", "Hammerdirt partner"),
              ("hd-dir", "Hammerdirt director"),
              ("spon", "Beach sponsor")
              ]
    about = models.CharField(
        db_column='about',
        max_length=500,
        blank=True,
        default=""
        )
    why = models.CharField(
        db_column='why',
        max_length=500,
        blank=True,
        default="Provided no reason"
        )
    avatar = models.ImageField(
        upload_to=user_image_path,
        max_length=100,
        blank=True,
        null=True
        )
    image_url = models.URLField(
        max_length=100,
        blank=True
        )
    position = models.CharField(
        db_column='position',
        max_length=30,
        blank=True,
        default="hd-assoc",
        choices=roles
        )
    hd_status = models.CharField(
        db_column='status',
        max_length=30,
        blank=True,
        default="hd-assoc",
        choices=status
        )
    user_twitter = models.CharField(
        max_length=50,
        blank=True,
        null=False,
        )
    def userKeys():
        a = list(get_user_model().objects.all().values('username', 'id'))
        return a
    def __str__(self):
        return u"username:%s"%(self.username)
class OwnedModel(models.Model):
    """
    Used to assign user to a created or updated record.
    """
    owner = models.ForeignKey(CustomUser, on_delete="DO_NOTHING")

    class Meta:
        abstract=True
class SwissLocations(models.Manager):
    print("calling swiss locations")
    def get_queryset(self):
        return super().get_queryset().filter(country="CH")
class Beaches(OwnedModel):
    """
    Beach names and gps data.
    """
    REGION_CHOICES = (("CH", "Switzerland"),
                      ("FR", "France"),
                      ("USA", "United States"),
                      )
    WATER_CHOICES = (('r', 'river'),
                     ('l', 'lake'),
                     ('o', 'ocean'),
                     ('no', 'no shore-line')
                     )
    location = models.CharField(
        db_column='location',
        max_length=100,
        blank=False,
        null=False,
        default='location required'
        )
    latitude = models.DecimalField(
        db_column='latitude',
        max_digits=11,
        decimal_places=8,
        blank=False,
        null=False,
        default=111.11111
        )
    longitude = models.DecimalField(
        db_column='longitude',
        max_digits=11,
        decimal_places=8,
        blank=False,
        null=False,
        default=11.11111
        )
    city = models.CharField(
        db_column='city',
        max_length=100,
        blank=False,
        null=False,
        default='City required'
        )
    post = models.CharField(
        db_column='post',
        max_length=12,
        blank=False,
        null=False,
        default='Postal-code'
        )
    country = models.CharField(
        db_column='country',
        max_length=30,
        choices=REGION_CHOICES
        )
    water = models.CharField(
        db_column='water',
        max_length=12,
        blank=False,
        null=False,
        choices=WATER_CHOICES, default='l'
        )
    water_name = models.CharField(
        db_column='water_name',
        max_length=100,
        blank=False,
        null=False,
        default='if not a river, lake or ocean use name of park or location'
        )
    slug = models.SlugField(
        unique=True,
        primary_key=True,
        blank=False,
        default=''
        )
    city_slug = models.SlugField(
        blank=False,
        default=''
        )
    water_name_slug = models.SlugField(
        blank=False,
        default=''
        )
    is_2020 = models.BooleanField(db_column='is_2020', default=False)
    objects = models.Manager()
    swiss_beaches = SwissLocations()
    def swiss_categories():
        return Beaches.swiss_beaches.values_list('water_name','city','post','country','slug')
    def swiss_lakes():
        return Beaches.swiss_beaches.filter(water='l').order_by("water_name").values_list("water_name", flat=True).distinct()
    def swiss_rivers():
        return Beaches.swiss_beaches.filter(water='r').order_by("water_name").values_list("water_name", flat=True).distinct()
    def swiss_cities():
        return Beaches.swiss_beaches.order_by("city").values_list('city', flat=True).distinct()
    def swiss_post():
        return Beaches.swiss_beaches.order_by("post").values_list('post', flat=True).distinct()
    def save(self, *args, **kwargs):
        self.slug = slugify(self.location)
        self.city_slug = slugify(self.city)
        self.water_name_slug=slugify(self.water_name)
        super().save(*args, **kwargs)
    def getBeachesOwner(self, user):
        return Beaches.objects.filter(owner__username=user).values('slug')
    def __str__(self):
        return u'location:%s, location_slug:%s, water_name:%s, water_name_slug:%s, country:%s'%(self.location, self.slug, self.water_name, self.water_name_slug, self.country)
    class Meta:
        managed = True
        db_table = 'beaches'
        ordering = ['location']
        verbose_name_plural = 'Beaches'
class Codes(OwnedModel):
    """
    MLW codes and decriptions
    """
    code = models.CharField(db_column='code', max_length=5, primary_key=True, blank=False, null=False, default='Code')
    material = models.CharField(db_column='material', max_length=30, blank=False, null=False, default='An MLW material type')
    description = models.CharField(db_column='description', max_length=100, blank=False, null=False, default='Describe the item')
    source = models.CharField(db_column='source', max_length=30, blank=False, null=False, default='Where does it come from')
    source_two = models.CharField(db_column='source_two', max_length=30, blank=False, null=False, default='Where does it come from')
    single_use = models.BooleanField(db_column='single_use', default=False)
    micro = models.BooleanField(db_column='micro', default=False)

    def __str__(self):
        return u'%s, %s' %(self.description, self.code)
    class Meta:
        managed = True
        db_table = 'codes'
        ordering = ['material']
        verbose_name_plural = 'MLW codes'
class LitterDataPieces(OwnedModel):
    """
    The survey results by item code.
    """
    location = models.ForeignKey(
        Beaches,
        db_column='location',
        null=True,
        to_field="slug",
        on_delete=models.DO_NOTHING
        )
    date = models.DateField(
        db_column='date',
        blank=False,
        null=False,
        default=datetime.date.today
        )
    length = models.IntegerField(
        db_column='length',
        blank=False,
        null=False,
        default=1
        )
    quantity = models.IntegerField(
        db_column='quantity',
        blank=False,
        null=False,
        default=1
        )
    pcs_m = models.DecimalField(
        db_column='pcs_m',
        max_digits=6,
        decimal_places=2,
        blank=True,
        null=True
        )
    # pcs_m_squared=models.DecimalField(
    #     db_column='pcs_m_squared',
    #     max_digits=6,
    #     decimal_places=2,
    #     blank=True,
    #     null=True
    #     )
    code = models.ForeignKey(
        Codes,
        db_column='code',
        null=True,
        on_delete=models.DO_NOTHING
        )
    def __str__(self):
        return u"date:%s, source:%s, location:%s, length:%s, quantity:%s, code:%s, " %(self.date, self.code.source, self.location, self.length, self.quantity, self.code  )
    def pcs_meter(self):
        pieces = self.quantity/self.length
        pieces_rounded = round(pieces,2)
        return pieces_rounded
    def save(self, *args, **kwargs):
        self.pcs_m = self.pcs_meter()
        super().save(*args, **kwargs)
    class Meta:
        get_latest_by = 'date'
        managed = True
        db_table = 'litter_data_pieces'
        verbose_name_plural = 'Litter pieces'
class CityCodeTotals(models.Manager):
    def get_queryset(self):
        return super().get_queryset().values("location__city", "code").annotate(total = Sum("quantity"))
class PostCodeTotals(models.Manager):
    def get_queryset(self):
        return super().get_queryset().values("location__post", "code").annotate(total = Sum("quantity"))
class GroupedLocationsCode(models.Manager):
    def get_queryset(self):
        return super().get_queryset().values_list("location", "date", "code", "pcs_m", "quantity").order_by('-date','location')
class LocationCodeTotals(models.Manager):
    def get_queryset(self):
        return super().get_queryset().values("location__water_name","code").annotate(total = Sum("quantity"))
class BeachDailyPcsM(models.Manager):
    def get_queryset(self):
        return super().get_queryset().values("location", "date").annotate(daily_pcsm=Sum("pcs_m")).order_by('date')
class BeachDailyQuanity(models.Manager):
    def get_queryset(self):
        return super().get_queryset().values("location", "date", "owner").annotate(daily_total=Sum("quantity")).order_by('-date')
class PiecesPerMeterLocation(LitterDataPieces):
    """
    Returns the sum of pieces per meter per location per survey
    """
    objects = models.Manager()
    city_code_totals = CityCodeTotals()
    post_code_totals = PostCodeTotals()
    code_data = GroupedLocationsCode()
    location_code_totals = LocationCodeTotals()
    beach_daily_pcsM = BeachDailyPcsM()
    beach_daily_quantity = BeachDailyQuanity()
    class Meta:
        proxy = True
class BeachesForGrouping(models.Manager):
    def get_queryset(self):
        return super().get_queryset().values_list('water_name','city','post','country','slug')
class Lakes(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(water='l').order_by("water_name").values_list("water_name", flat=True).distinct()
class Rivers(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(water='r').order_by("water_name").values_list("water_name", flat=True).distinct()
class Cities(models.Manager):
    def get_queryset(self):
        return super().get_queryset().order_by("city").values_list('city', flat=True).distinct()
class PostalCodes(models.Manager):
    def get_queryset(self):
        return super().get_queryset().order_by("post").values_list('post', flat=True).distinct()
class BeachesByCategory(Beaches):
    class Meta:
        proxy = True
    beaches_and_categories = BeachesForGrouping()
    objects = models.Manager()
    lakes = Lakes()
    rivers = Rivers()
    cities = Cities()
    postal_codes = PostalCodes()
# begin Switzerland only
class SwissCityCodeTotals(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(location__country='CH').values("location__city", "code").annotate(total = Sum("quantity"))
class SwissPostCodeTotals(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(location__country='CH').values("location__post", "code").annotate(total = Sum("quantity"))
class SwissGroupedLocationsCode(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(location__country='CH').values_list("location", "date", "code", "pcs_m", "quantity").order_by('-date','location')
class SwissLocationCodeTotals(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(location__country='CH').values("location__water_name","code").annotate(total = Sum("quantity"))
class SwissBeachDailyPcsM(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(location__country='CH').values("location", "date").annotate(daily_pcsm=Sum("pcs_m")).order_by('date')
class SwissBeachDailyQuanity(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(location__country='CH').values("location", "date", "owner").annotate(daily_total=Sum("quantity")).order_by('-date')
class SwissPiecesPerMeterLocation(LitterDataPieces):
    """
    Returns the sum of pieces per meter per location per survey
    """
    objects = models.Manager()
    city_code_totals = SwissCityCodeTotals()
    post_code_totals = SwissPostCodeTotals()
    code_data = SwissGroupedLocationsCode()
    location_code_totals = SwissLocationCodeTotals()
    beach_daily_pcsM = SwissBeachDailyPcsM()
    beach_daily_quantity = SwissBeachDailyQuanity()
    class Meta:
        proxy = True
#
class References(OwnedModel):
    """
    The library or reading list for hammerdirt projects and articles.
    """
    title = models.CharField(db_column='title', max_length=240, blank=False, null=False, default='Titles are required')
    slug = models.SlugField(unique=True, blank=True, null=False)
    author = models.CharField(db_column='author', max_length=120, blank=False, null=False, default='Authors deserve credit')
    abstract = models.CharField(db_column='abstract', max_length=200,  blank=False, null=False, default='What is this about')
    url = models.URLField(db_column='ref_url', blank=True, max_length=200)
    date = models.DateField(db_column='date', blank=False, null=False, default=datetime.date.today)
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    def getReferenceOwner(self, user):
        return References.objects.filter(owner__username=user).values('slug')
    def __str__(self):
        return u"slug:%s" %(self.slug)
    class Meta:
        managed = True
        get_latest_by = 'date'
        db_table = 'library'
        verbose_name_plural = 'References'
class ReferenceTitles(models.Manager):
    def get_queryset(self):
        return super().get_queryset().order_by("title").values('title', 'slug')
class ReferencesOutput(References):
    class Meta:
        proxy = True
    select_references = ReferenceTitles()
class DraftArticles(OwnedModel):
    """
    Tiny MCE editor
    """
    def article_image_path(instance, filename):
        a = instance.slug
        return '{0}/{1}'.format(a, filename)
    title = models.CharField(
        db_column="title",
        max_length=40,
        null=False,
        blank=False,
        unique=True,
        default="Article name"
        )
    date_created =  models.DateField(
        db_column='date_created',
        blank=False,
        null=False,
        default=datetime.date.today
        )
    last_edit = models.DateTimeField(
        auto_now_add=False,
        auto_now=True,
        db_column='last_edit'
        )
    subject = models.CharField(
        db_column='subject',
        max_length=30,
        )
    slug = models.SlugField(
        unique=True,
        blank=False,
        default='',
        primary_key=True
        )
    article = JSONField()
    image = JSONField()
    summary =  models.CharField(
        db_column='summary',
        max_length=200,
        default="This needs a summary"
        )
    # references = JSONField()
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    def getArticleOwner(self, user):
        return DraftArticles.objects.filter(owner__username=user).values('slug')
    def __str__(self):
        return u"slug:%s, title:%s"%(self.slug, self.title)
    class Meta:
        db_table = "article_drafts"
        managed = True
        verbose_name_plural = 'Article drafts'
class ArticleSearchList(models.Manager):
    def get_queryset(self):
        return super().get_queryset().order_by("title").values('title', 'subject', 'owner','slug')
class ArticleSearchCriteria(DraftArticles):
    class Meta:
        proxy = True
    article_search_criteria = ArticleSearchList()

class ArticleComment(OwnedModel):
    DISPOSITION = [
        ("op", "opened"),
        ("ack","Acknowledged"),
        ("inr","In Review"),
        ("p","Priority"),
        ("see","See repo"),
        ("c","Closed"),
        ("cln","Clarification needed" )
    ]
    SUBJECT = [
        ("ui","User interface"),
        ("dis","Display"),
        ("ed", "Edit requested"),
        ("rf", "Check references"),
        ("mi", "More information"),
        ("ms", "Missing section"),
        ("d", "Data incomplete"),
        ("g", "This looks good"),
        ("fr","Feature request"),
        ("pi","Performance issue")
    ]
    doc_title =  models.ForeignKey(
        DraftArticles,
        to_field="title",
        db_column='doc_title',
        null=True,
        on_delete=models.DO_NOTHING
        )
    subject = models.CharField(
        db_column='subject',
        max_length=30,
        choices=SUBJECT
        )
    disposition = models.CharField(
        db_column='disposition',
        max_length=30,
        choices=DISPOSITION
        )
    comment_date = models.DateTimeField(
        auto_now_add=True,
        auto_now=False,
        db_column='date_created'
        )
    comment = models.CharField(
        db_column='summary',
        max_length=500,
        default="This needs a summary"
        )
    def __str__(self):
        return u"doc_title:%s, subject:%s, disposition:%s, comment_date:%s, comment:%s, owner:%s" %(self.doc_title, self.subject, self.disposition, self.comment_date, self.comment, self.owner)
    class Meta:
        db_table = "article_comments"
        managed = True
        verbose_name_plural = 'Article comments'
class SurveyAdminData(OwnedModel):
    """
    Dimensional and participation data for a survey.
    """
    location = models.ForeignKey(
        Beaches,
        db_column='location',
        null=True,
        # to_field="slug",
        on_delete=models.DO_NOTHING
        )
    date = models.DateField(
        db_column='date',
        blank=False,
        null=False,
        default=datetime.date.today
        )

    length = models.IntegerField(
        db_column='length',
        blank=False,
        null=False,
        default=1
        )
    area = models.DecimalField(
        db_column='area',
        max_digits=6,
        decimal_places=2,
        blank=True,
        null=True
        )
    mac_plast_w = models.DecimalField(
        db_column='mac_plast_w',
        max_digits=5,
        decimal_places=3,
        blank=True,
        null=True
        )
    mic_plas_w = models.DecimalField(
        db_column='mic_plas_w',
        max_digits=7,
        decimal_places=5,
        blank=True,
        null=True
        )
    total_w = models.DecimalField(
        db_column='non_plas_w',
        max_digits=5,
        decimal_places=3,
        blank=True,
        null=True
        )
    est_weight = models.DecimalField(
        db_column='est_weight',
        max_digits=4,
        decimal_places=1,
        blank=True,
        null=True
        )
    num_parts_staff = models.IntegerField(
        db_column='num_parts_staff',
        blank=False,
        null=False,
        default=1
        )
    num_parts_other = models.IntegerField(
        db_column='num_parts_other',
        blank=False,
        null=False,
        default=0
        )
    time_minutes = models.IntegerField(
        db_column='time_minutes',
        blank=False,
        null=False,
        default=0
        )
    participants = JSONField()
    project=models.CharField(
        db_column='project',
        max_length=30,
        blank=True,
        default="2020",
        choices=PROJECT
        )
    is_2020 = models.BooleanField(db_column='is_2020', default=False)
    def __str__(self):
        return u"location:%s, date:%s, length:%s"%(self.location, self.date,self.length)
    class Meta:
        get_latest_by = 'date'
        managed = True
        db_table = 'survey_dim_data'
        verbose_name_plural = 'Survey dimensions'
class SurveyAdminValues(models.Manager):
    def get_queryset(self):
        return super().get_queryset().order_by("date").values('location', 'date', 'length','owner', 'total_w', 'time_minutes', 'mac_plast_w','mic_plas_w', 'area')
class SurveyAdminViews(SurveyAdminData):
    class Meta:
        proxy = True
    basic_data = SurveyAdminValues()
