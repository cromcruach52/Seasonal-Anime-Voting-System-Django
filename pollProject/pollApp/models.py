# models.py
from django.db import models
from accounts.models import CustomUser

class Season(models.Model):
    name = models.CharField(max_length=100)
    year = models.IntegerField()
    image = models.ImageField(upload_to='season_images/', null=True, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} {self.year}"

    class Meta:
        verbose_name_plural = "Seasons"


class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='category_images/', null=True, blank=True)

    def __str__(self):
        return self.name


class Question(models.Model):
    question_text = models.CharField(max_length=300)
    pub_date = models.DateTimeField('date published')
    seasons = models.ManyToManyField(Season)
    image = models.ImageField(upload_to='question_images/', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.question_text

    def is_any_season_active(self):
        return any(season.active for season in self.seasons.all())

    def get_choice_votes(self):
        return self.choice_set.annotate(votes=models.Sum('vote__votes')).values('choice_text', 'votes')
    
    def to_dict(self):
        return {
            'id': self.id,
            'question_text': self.question_text,
            'pub_date': self.pub_date.isoformat(),  
            'seasons': [str(season) for season in self.seasons.all()],  
            'image': self.image.url if self.image else None,  
            'category': str(self.category) if self.category else None,
            }

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    image = models.ImageField(upload_to='choice_images/', null=True, blank=True)

    def __str__(self):
        return self.choice_text


class Vote(models.Model):
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE, null=True)
    season = models.ForeignKey(Season, on_delete=models.CASCADE, null=True)
    year = models.IntegerField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.choice.choice_text} in {self.season.name} {self.year} for {self.question.question_text}"
