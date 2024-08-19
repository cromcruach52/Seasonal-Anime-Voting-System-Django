from django.shortcuts import render
from django.db.models import Sum, F
from accounts.models import CustomUser
from pollApp.models import Vote, Question, Season, Category
import json
from django.contrib.auth.decorators import login_required, user_passes_test
from pollApp.models import Choice

def is_admin(user):
    return user.is_superuser

@login_required
@user_passes_test(is_admin)
def vote_statistics(request):
    selected_year = request.GET.get('year')
    selected_season_id = request.GET.get('season')
    selected_question_id = request.GET.get('question')

    years = Season.objects.values_list('year', flat=True).distinct()
    seasons = Season.objects.all()
    all_questions = Question.objects.all().distinct()
    age_ranges = [(0, 12), (13, 17), (18, 25), (26, 35), (36, 45), (46, 55), (56, 65), (66, 100)]
    if selected_year:
        seasons = seasons.filter(year=selected_year)
        all_questions = all_questions.filter(vote__year=selected_year)

    if selected_season_id:
        all_questions = all_questions.filter(vote__season__id=selected_season_id)

    questions = all_questions

    if selected_question_id:
        questions = questions.filter(id=selected_question_id)

    question_votes = []

    for question in questions:
        top_votes_qs = Vote.objects.filter(question=question)

        if selected_year:
            top_votes_qs = top_votes_qs.filter(year=selected_year)

        if selected_season_id:
            top_votes_qs = top_votes_qs.filter(season__id=selected_season_id)

        top_votes_qs = top_votes_qs.values('choice__choice_text').annotate(total_votes=Sum('votes')).order_by('-total_votes')[:10]

        for vote in top_votes_qs:
            voters = CustomUser.objects.filter(vote__choice__choice_text=vote['choice__choice_text'])
            vote['voters'] = list(voters.values('username', 'region', 'gender', 'age'))

            total_voters = voters.count()
            vote['gender_percentage'] = {gender[1]: voters.filter(gender=gender[0]).count() / total_voters * 100 for gender in CustomUser.GENDERS if gender[0]}
            vote['region_percentage'] = {region[1]: voters.filter(region=region[0]).count() / total_voters * 100 for region in CustomUser.REGIONS if region[0]}
            vote['age_percentage'] = {f'{age_range[0]}-{age_range[1]}': voters.filter(age__range=age_range).count() / total_voters * 100 for age_range in age_ranges}

        question_votes.append({'question': question.to_dict(), 'top_votes': list(top_votes_qs)})

    question_votes_json = json.dumps(question_votes)

    context = {
        'question_votes_json': question_votes_json,
        'question_votes': question_votes,
        'years': years,
        'seasons': seasons,
        'all_questions': all_questions,
        'selected_year': selected_year,
        'selected_season': int(selected_season_id) if selected_season_id else None,
        'selected_question': int(selected_question_id) if selected_question_id else None,
    }

    return render(request, 'voteStatistics/vote_statistics.html', context)

@login_required
@user_passes_test(is_admin)
def category_statistics(request):
    all_categories = Category.objects.all()
    selected_category_name = request.GET.get('category')

    questions = Question.objects.all()
    if selected_category_name:
        questions = questions.filter(category__name=selected_category_name)

    categories = {}
    season_votes = {}

    # Count the number of votes for each season within the selected category
    for question in questions:
        for season in question.seasons.all():
            if season not in season_votes:
                season_votes[season] = 0
            season_votes[season] += Vote.objects.filter(question=question, season=season).count()

    total_votes = sum(season_votes.values())

    for question in questions:
        if question.category not in categories:
            categories[question.category] = {}

        for season in question.seasons.all():
            if season not in categories[question.category]:
                categories[question.category][season] = {
                    'questions': []
                }

            choice_votes = Vote.objects.filter(question=question, season=season).values('choice__choice_text').annotate(total_votes=Sum('votes'))
            total_question_votes = sum(vote['total_votes'] for vote in choice_votes)

            question_data = {
                'question': question,
                'choice_votes': choice_votes,
                'total_votes': total_question_votes,
                'weighted_scores': {}  # Placeholder for weighted scores
            }
            categories[question.category][season]['questions'].append(question_data)

    # Calculate weights and weighted scores
    for category, seasons in categories.items():
        for season, data in seasons.items():
            # Calculate the weight for the current season
            weight = season_votes[season] / total_votes
            for question_data in data['questions']:
                total_question_votes = question_data['total_votes']
                for vote in question_data['choice_votes']:
                    # Calculate the percentage of votes for the current choice
                    percentage = vote['total_votes'] / total_question_votes
                    # Calculate the weighted score for the current choice
                    weighted_score = percentage * weight
                    # Store the weight and weighted score in the vote dictionary
                    vote['season_weight'] = weight
                    vote['weighted_score'] = weighted_score
    
    top_shows_by_category = {}
    for category, seasons in categories.items():
        top_shows = []
        for season, data in seasons.items():
            for question_data in data['questions']:
                for vote in question_data['choice_votes']:
                    # Assuming 'choice' is the foreign key to the Choice model
                    choices = Choice.objects.filter(choice_text=vote['choice__choice_text'])

                    if choices.exists():
                        # Use the first choice or handle the situation as needed
                        choice = choices.first()
                        image_path = choice.image.url  # Adjust the field name accordingly
                    else:
                        # Handle the case where no choices are found
                        image_path = "path/to/default/image.jpg"  # Adjust with the default image path

                    top_shows.append({
                        'show': vote['choice__choice_text'],
                        'weighted_score': vote['weighted_score'],
                        'choice_image': image_path,  # Include the image path
                    })
        # Sort the shows by weighted score in descending order and select the top 5
        top_shows.sort(key=lambda x: x['weighted_score'], reverse=True)
        top_shows_by_category[category] = top_shows[:5]

    return render(request, 'voteStatistics/category_statistics.html', {
        'categories': categories,
        'all_categories': all_categories,
        'season_votes': season_votes,
        'top_shows_by_category': top_shows_by_category
    })
