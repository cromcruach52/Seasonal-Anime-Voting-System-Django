# views.py
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.http import Http404
from django.db.models import Sum 
from django.contrib.auth.decorators import login_required
from .models import Question, Choice, Season, Vote
from datetime import datetime
from django.contrib import messages
from accounts.models import CustomUser


def home(request):
    return render(request, 'polls/home.html')


@login_required
def index(request):
    selected_season_id = request.GET.get('season')
    selected_year = int(request.GET.get('year', datetime.now().year))

    current_year = datetime.now().year
    years_range = range(current_year, current_year - 5, -1)

    seasons = Season.objects.filter(year=selected_year)

    selected_season = None
    latest_question_list = []

    if selected_season_id:
        try:
            selected_season = Season.objects.get(pk=selected_season_id, year=selected_year)
            print("Selected Season:", selected_season.name)

            latest_question_list = Question.objects.filter(seasons=selected_season).order_by('-pub_date')[:6]
        except Season.DoesNotExist:
            print("Invalid Season ID or Season not associated with the selected year.")
    else:
        latest_question_list = Question.objects.filter(seasons__year=selected_year).order_by('-pub_date')[:6]

    print("Selected Year:", selected_year)
    print("Number of Questions:", len(latest_question_list))

    # Logic for showing the current season and year by default
    current_month = datetime.now().month
    season_months = {
        'Spring': (3, 4, 5),
        'Summer': (6, 7, 8),
        'Fall': (9, 10, 11),
        'Winter': (12, 1, 2)
    }

    current_season = None
    for season, months in season_months.items():
        if current_month in months:
            current_season = season
            break

    default_season = Season.objects.filter(name=current_season, year=datetime.now().year).first()
    default_year = datetime.now().year

    # If no season is selected, use the default season and year
    if not selected_season_id:
        selected_season = default_season
        selected_year = default_year
        latest_question_list = Question.objects.filter(seasons=selected_season).order_by('-pub_date')[:6]

    active_question_list = []
    for question in latest_question_list:
        if question.seasons.filter(active=True).exists():
            active_question_list.append(question)

    context = {
        'latest_question_list': latest_question_list,
        'seasons': seasons,  
        'selected_season': selected_season.name if selected_season else None,
        'selected_year': selected_year,
        'years_range': years_range
    }

    return render(request, 'polls/index.html', context)


@login_required
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

@login_required
def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    # Retrieve all choices for the current question, sorted by votes in descending order
    choices = question.choice_set.annotate(total_votes=Sum('vote__votes')).order_by('-total_votes')[:10]

    context = {
        'question': question,
        'choices': choices,
    }

    return render(request, 'polls/results.html', context)

@login_required
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    
   
    if Vote.objects.filter(question=question, user=request.user).exists():
        messages.error(request, "You've already voted for this question.")
        return render(request, 'polls/detail.html', {'question': question})
    
 
    selected_choice_id = request.POST.get('choice')
    
    try:
        selected_choice = question.choice_set.get(pk=selected_choice_id)
    except (KeyError, Choice.DoesNotExist):
      
        messages.error(request, 'You did not select a valid choice.')
        return render(request, 'polls/detail.html', {'question': question})
    else:
      
        vote_instance, created = Vote.objects.get_or_create(
            choice=selected_choice,
            season=question.seasons.first(),  
            year=question.pub_date.year,
            question=question,  
            user=request.user  
        )
     
        vote_instance.votes += 1
        vote_instance.save()

     
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))