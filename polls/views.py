from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
#from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth import logout

from .models import Choice, Question, UserProfile


@login_required
def IndexView(request):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'
    questions = Question.objects.order_by('-pub_date')[:5]
    values_from_session = request.session.pop('user_id', None)
    print "values_from_session",values_from_session
    # my_user = UserProfile.objects.all().first()
    my_user = UserProfile.objects.get(user_id = values_from_session)
    # print checking.name
    print my_user.name
    return render(request, template_name, {'questions' : questions, 'my_user' : my_user})
    # def get_queryset(self):
    #     """Return the last five published questions."""
    #     return Question.objects.order_by('-pub_date')[:5]

@login_required
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

# class DetailView(generic.DetailView):
#     model = Question
#     template_name = 'polls/detail.html'


@login_required
def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

# class ResultsView(generic.DetailView):
#     model = Question
#     template_name = 'polls/results.html'

@login_required
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))    

# class EmailBackend(ModelBackend):
#     def authenticate(self, username=None, password=None, **kwargs):
#         UserModel = get_user_model()
#         try:
#             user = UserModel.objects.get(email=username)
#         except UserModel.DoesNotExist:
#             return None
#         else:
#             if user.check_password(password):
#                 return user
#         return None

# class CustomBackend(ModelBackend):  # requires to define two functions authenticate and get_user
	
#     def authenticate(self, username=None, password=None, **kwargs):
#         UserModel = get_user_model()

#         try:
#             # below line gives query set,you can change the queryset as per your requirement
#             user = UserModel.objects.filter(
#                 Q(username__iexact=username) |
#                 Q(email__iexact=username)
#             ).distinct()

#         except UserModel.DoesNotExist:
#             return None

#         if user.exists():
#             ''' get the user object from the underlying query set,
#             there will only be one object since username and email
#             should be unique fields in your models.'''
#             user_obj = user.first()
#             if user_obj.check_password(password):
#                 return user_obj
#             return None
#         else:
#             return None

#     def get_user(self, user_id):
#         UserModel = get_user_model()
#         try:
#             return UserModel.objects.get(pk=user_id)
#         except UserModel.DoesNotExist:
#             return None

def get_user(email):
    try:
    	print "get_user"
        return User.objects.get(email=email.lower())
    except User.DoesNotExist:
        return None


def login_auth(request):
	if request.method == 'POST':

		email = request.POST.get('email')
		print email
		password = request.POST.get('password')
		print password
		username = get_user(email)
		user = authenticate(username=username, password=password)
		if user is not None:
			print "user is not none"
			if user.is_active:
				login(request, user)
				print "useriddd"
				print user.id
				request.session['user_id'] = user.id
				return HttpResponseRedirect(reverse('polls:index'))
			else:
				return render(request, 'polls/login.html')
		else:
			return render(request, 'polls/login.html')
	else:
		return render(request, 'polls/login.html')

def logoutView(request):
	logout(request)
	if request.method == 'POST':
		logout(request)
		print 'logout done'
	return render(request, 'polls/login.html')

	# return HttpResponseRedirect(reverse('polls:login'))
				
	# if request.method == 'POST':
	# 	username = request.POST['username']
	# 	password = request.POST['password']
	# 	#obj = EmailBackend() 
	# 	user = authenticate(request, username=username, password=password)
	# 	if user is not None:
	# 		login(request, user)
	# 		return HttpResponseRedirect(reverse('polls:index'))
	# 	else:
	# 		return render(request, 'polls/login.html')
	# else:
	# 	return render(request, 'polls/login.html')

