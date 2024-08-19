from django.contrib import admin
from django.db import models
from datetime import datetime

from .models import Question, Choice, Season, Vote, Category  # Added import for Category

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['question_text', 'image']}),
        ('Date Information', {'fields': ['pub_date'], 'classes': ['collapse']}),
        ('Seasons', {'fields': ['seasons']}),  # Updated field name
        ('Category', {'fields': ['category']}),  # Added field for Category
    ]

    inlines = [ChoiceInline]
    filter_horizontal = ('seasons',)  # Updated field name
    list_filter = ('seasons__year', 'category__name')  # Updated field name
    search_fields = ['question_text', 'category__name']  # Added search field for Category

    def get_votes(self, obj):
        return '\n'.join([f"{choice.choice_text}: {Vote.objects.filter(choice=choice).aggregate(models.Sum('votes'))['votes__sum']}" for choice in obj.choice_set.all()])
    get_votes.short_description = 'Votes'

    def get_season(self, obj):  # Updated method name
        return ', '.join([season.name for season in obj.seasons.all()])  # Updated field name
    get_season.short_description = 'Season'  # Updated field name

    list_display = ('question_text', 'get_votes', 'get_season', 'category')  # Updated method name

class SeasonAdmin(admin.ModelAdmin):  # Updated class name
    list_display = ('name', 'year')
    list_filter = ('year',)  
    search_fields = ['name']

    def changelist_view(self, request, extra_context=None):
        if not request.GET.get('year__exact'):
            q = request.GET.copy()
            request.GET = q
            request.META['QUERY_STRING'] = request.GET.urlencode()

        return super().changelist_view(request, extra_context=extra_context)

admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Season, SeasonAdmin)  # Updated class name
admin.site.register(Vote)
admin.site.register(Category)  # Added registration for Category
