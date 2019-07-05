from django.db import models
from django.utils import timezone
# from django.forms.models import ModelForm
# from django.forms.widgets import CheckboxSelectMultiple

class Trip(models.Model):
    BUDGETS_CHOICES = (
        ("10만원 미만", "10만원 미만"),
        ("10-20만원 미만","10-20만원 미만"),
        ("20-30만원 미만", "20-30만원 미만"),
        ("30만원 이상", "30만원 이상")
    )
    PLACES_CHOICES = (
        ("서울", "서울"),
        ("경기","경기"),
        ("강원", "강원"),
        ("충청", "충청"),
        ("전라", "전라"),
        ("부산", "부산"),
        ("제주", "제주"),
        ("경상", "경상"),
        ("대전", "대전"),
        ("대구", "대구"),
        ("인천", "인천")
    )
    TRANSPORTATIONS_CHOICES = (
        ("버스", "버스"),
        ("지하철","지하철"),
        ("자동차", "자동차")
    )
    title=models.CharField(max_length=50)
    body=models.TextField(null=False)
    image=models.ImageField(upload_to='images/')
    date=models.DateTimeField('date published', default = timezone.datetime.now())
    writer=models.CharField(max_length=50)
    place=models.CharField(choices=PLACES_CHOICES, max_length=50)
    transportation=models.CharField(choices=TRANSPORTATIONS_CHOICES, max_length=50)
    person=models.IntegerField()
    budget=models.CharField(choices=BUDGETS_CHOICES,max_length=50)
    def sum(self):
        return self.body[:20]

class Comment(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, null = True, related_name='comments')
    contents = models.CharField(max_length=500)
    com_writer=models.CharField(max_length=50, default = "default")

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.contents
