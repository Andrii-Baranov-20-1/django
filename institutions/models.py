from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class Category(models.Model):
    """Category"""
    name = models.CharField("Category", max_length=150)
    description = models.TextField("Description")
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Category"


class Types(models.Model):
    """Types"""
    name = models.CharField("Name", max_length=100)
    description = models.TextField("Description")
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Types"
        verbose_name_plural = "Types"


class EducationalInstitution(models.Model):
    """Educational Institutions"""
    name = models.CharField("Name", max_length=150)
    street = models.CharField("Street", max_length=200, default='')
    #phone = models.CharField("Phone Number", max_length=13, default='+38')
    types = models.ManyToManyField(Types, verbose_name="types")
    category = models.ForeignKey(Category, verbose_name="category", on_delete=models.SET_NULL, null=True)

    # menu = models.CharField(WebSite, verbose_name="menu")

    mainPhoto = models.ImageField("Photo", upload_to="education_main_photo/")
    description = models.TextField("Description")

    url = models.SlugField(max_length=160, unique=True)
    draft = models.BooleanField("Draft Field", default=False)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("institution_detail", kwargs={"slug": self.url})

    def get_review(self):
        return self.reviews_set.filter(parent__isnull=True)

    def average_rating(self):
        ratings = self.rating_set.all()
        if ratings.exists():
            return round(sum(r.star.value for r in ratings) / ratings.count(), 1)
        return 0

    class Meta:
        verbose_name = "Education Institution"
        verbose_name_plural = "Education Institutions"


class EducationalInstitutionPhoto(models.Model):
    """Educational Institutions photos"""
    title = models.TextField("Title", max_length=120)
    description = models.TextField("Description")
    image = models.ImageField("Image", upload_to="education_photos/")
    restaurant = models.ForeignKey(EducationalInstitution, verbose_name="educational_institute", on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Institution Photo"
        verbose_name_plural = "Institution Photos"


class RatingStar(models.Model):
    """Rating"""
    value = models.PositiveSmallIntegerField("Value", default=0)

    def __str__(self):
        return f'{self.value}'

    class Meta:
        verbose_name = "Rating Star"
        verbose_name_plural = "Rating Star"
        ordering = ["-value"]


class Rating(models.Model):
    """Rating"""
    ip = models.CharField("IP address", max_length=15)
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE, verbose_name="star")
    institution  = models.ForeignKey(EducationalInstitution, on_delete=models.CASCADE, verbose_name="restaurant")

    def __str__(self):
        return f"{self.star} - {self.institution }"

    class Meta:
        verbose_name = "Rating"
        verbose_name_plural = "Rating"


class Reviews(models.Model):
    """Reviews"""
    name = models.CharField("Name", max_length=100)
    email = models.EmailField()
    text = models.TextField("Message", max_length=5000)
    parent = models.ForeignKey(
        'self', verbose_name="Parent", on_delete=models.SET_NULL, blank=True, null=True
    )
    institution  = models.ForeignKey(EducationalInstitution, verbose_name="Educational Institution", on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} for {self.institution .name}'

    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Review"


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username


class Record(models.Model):
    name = models.CharField("Name", max_length=150)
    street = models.CharField("Street", max_length=200, default='')
    #phone = models.CharField("Phone Number", max_length=13, default='+38')
    types = models.ManyToManyField(Types, verbose_name="types")
    category = models.ForeignKey(Category, verbose_name="category", on_delete=models.SET_NULL, null=True)

    mainPhoto = models.ImageField("Photo", upload_to="education_main_photo/")
    description = models.TextField("Description", default='No description available')

    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("crud_detail", args=[str(self.id)])
