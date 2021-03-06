from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from goals.models import Goal
from goals.forms import GoalForm, LoginForm, SignUpForm
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q


@login_required
def index(request):
    # goals = Goal.objects.filter(user=request.user).order_by("modified")
    goals = Goal.objects.filter(user=request.user, created_at__gte=datetime.toaday())
    
    query = request.GET.get("q")
    if query:
        goals = goals.filter(
            Q(title__icontains=query)
            | Q(description__icontains=query)
            | Q(created__icontains=query)
        ).distinct()
    page = request.GET.get("page", 1)
    paginator = Paginator(goals, 5)
    try:
        goals = paginator.page(page)
    except PageNotAnInteger:
        goals = paginator.goals(1)
    except EmptyPage:
        goals = paginator.page(paginator.num_pages)

    context = {"goals": goals}
    return render(request, "goals/index.html", context)


@login_required
def add(request):
    if request.method == "POST":
        form = GoalForm(request.POST)
        # check whether form is valid
        if form.is_valid():
            # To create and save an object in a single step
            Goal.objects.create(
                user=request.user,
                title=form.cleaned_data["title"],
                description=form.cleaned_data["description"],
            )
            return redirect("/")
        else:
            return redirect("")
    else:
        # if a GET (or any other method) we'll create a blank form
        form = GoalForm()
        # it will create an empty form instance and place it in the template context/form to be rendered.
    return render(request, "goals/add.html", {"form": form})


#############pk required#################


@login_required
def edit(request, pk):
    goal = Goal.objects.get(pk=pk, user=request.user)
    if request.method == "POST":
        form = GoalForm(request.POST)
        # check whether form is valid
        if form.is_valid():
            # process the data in form.cleaned_data as required in is_valid()
            goal.title = form.cleaned_data["title"]
            goal.description = form.cleaned_data["description"]
            goal.save()
            return redirect("/")
    else:
        # specify initial data for forms by specifying an initial parameter when instantiating the form.
        form = GoalForm(initial={"title": goal.title, "description": goal.description})
    return render(request, "goals/add.html", {"form": form})


@login_required
def delete(request, pk):
    Goal.objects.get(pk=pk, user=request.user).delete()
    return redirect("/")
    # return redirect('/login')


#############Accounts#################


def login_user(request):
    if not request.user.is_authenticated:
        # If form is submitted
        if request.method == "POST":
            # create a form instance and populate it with data from the request
            form = LoginForm(request.POST)
            # check whether form is valid
            if form.is_valid():
                # process the data in form.cleaned_data as required
                email = form.cleaned_data["email"]
                password = form.cleaned_data["password"]
                user_obj = User.objects.get(email=email)
                # authenticate() to verify a set of credentials passed.
                user = authenticate(username=user_obj.username, password=password)
                if user is not None:
                    logout(request)
                    login(request, user)
                    # Redirect to a success page.
                    return redirect("/")
                else:
                    # Redirect to login page
                    return redirect("/login")
                    # return HttpResponse("Either your credentials are incorrect or the user does not exist.")
        else:
            # if a GET (or any other method) we'll create a blank form
            form = LoginForm()
        # it will create an empty form instance and place it in the template context/form to be rendered.
        return render(request, "registration/login.html", {"form": form})
    else:
        return redirect("/")


def logout_user(request):
    logout(request)
    return redirect("/login")


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            mail_subject = "Activate your account."
            message = render_to_string(
                "goals/acc_active_email.html",
                {
                    "user": user,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": account_activation_token.make_token(user),
                },
            )
            to_email = form.cleaned_data.get("email")
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return HttpResponse(
                "Please confirm your email address to complete the registration"
            )
    else:
        form = SignUpForm()
    return render(request, "registration/signup.html", {"form": form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return HttpResponse(
            "Thank you for your email confirmation. Now you can login your account."
        )
    else:
        return HttpResponse("Activation link is invalid!")
