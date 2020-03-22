from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse

# Create your views here.
from django.urls import reverse

from rango import models
from rango.forms import CategoryForm, DishForm
from rango.models import Category, Dish, UserComment
from rango.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from datetime import datetime

# this is our homepage views. It will send the categories and dishes to the HTML
def homepage(request):
    category_list = Category.objects.order_by('-category')
    dish_list = Dish.objects.order_by('-likes')[:5]

    context_dict = {}
    context_dict['categories'] = category_list
    context_dict['dishes'] = dish_list

    # This is the visitor data:
    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']

    response = render(request, 'rango/homepage.html', context=context_dict)
    return response

# This is the views of category pages:
def show_category(request, category_name_slug):
    context_dict = {}
    category_list = Category.objects.order_by('-category')
    context_dict['categories'] = category_list
    try:
        category = Category.objects.get(slug=category_name_slug)

        dishes = Dish.objects.filter(category=category)
        # dishes here means all the dishes of this category
        context_dict['dishes'] = dishes

        context_dict['category'] = category

    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['dishes'] = None

    return render(request, 'rango/category.html', context_dict)

# this is for add one category
def add_category(request):
    form = CategoryForm
    category_list = Category.objects.order_by('-category')
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return homepage(request)
        else:
            print(form.errors)
    return render(request, 'rango/add_category.html', {'form': form,
                                                       'categories': category_list})


# this method is to add a new dish:
    # Beacause our dish pages are created by our own therefore this time the dishes url MUST be a outside webpage
def add_dish(request, category_name_slug):
    category_list = Category.objects.order_by('-category')
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    if category is None:
        return redirect('/rango/')

    form = DishForm()
    if request.method == 'POST':

        form = DishForm(request.POST)
        if form.is_valid():
            success = 'You added a need dish!'
            if category:
                dish = form.save(commit=False)
                dish.category = category
                dish.save()
                return redirect(reverse('rango:show_category', kwargs={'category_name_slug': category_name_slug}))
            else:
                print(form.errors)

    context_dict = {'form': form, 'category': category, 'categories': category_list,}
    return render(request, 'rango/add_dish.html', context=context_dict)

# This is the old registration method. But we applied django-registration-redux now so it is no longer used
def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'rango/register.html',
                  context={'user_form': user_form, 'profile_form': profile_form, 'registered': registered})

# Same to above
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('rango:homepage'))
            else:
                return HttpResponse("Your Rango account is disabled.")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'rango/login.html')


@login_required
def user_logout(request):
    logout(request)
    return render(request, 'rango/logout.html')


def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val


def visitor_cookie_handler(request):
    visits = int(request.COOKIES.get('visits', '1'))
    last_visit_cookie = request.COOKIES.get('last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')

    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        request.session['last_visit'] = str(datetime.now())
    else:
        request.session['last_visit'] = last_visit_cookie
    request.session['visits'] = visits

# From main_course1 to dessert three, we used the similar method:
    # because we want to recieve the users comments and output all users comments
    # therefore we need to create a form to connect users comment and users like/dislike to the dishes
    # then we collect users informations by get user objects and get the dish using dish names:
def main_course1(request):
    category_list = Category.objects.order_by('-category')

    d2 = "Oil spilled noodles"
    # get dish name
    dish = Dish.objects.get(dish=d2)
    form = DishForm()
    if request.method == "POST":
        # user name
        u = User.objects.get(username=request.user.username)
        # comment
        c = request.POST.get("comment_input", None)
        # like
        like = request.POST.get("like", None)
        isl = False
        # if like let isl(islike) to be true, and let the dish.likes ++
        if like == "like":
            isl = True
            dish.likes = dish.likes + 1
            dish.save()
            # create the comment and save it
        models.UserComment.objects.create(
            username=u,
            comment=c,
            dish=d2,
            islike=isl,
        )

        info_list = UserComment.objects.filter(dish=d2)
        return render(request, "rango/main_course1.html", {"info_list": info_list,
                                                           "categories": category_list,
                                                           "form": form,
                                                           "dish": dish,
                                                           })
    info_list = UserComment.objects.filter(dish=d2)
    return render(request, "rango/main_course1.html", {"info_list": info_list,
                                                       "categories": category_list,
                                                       "form": form,
                                                       "dish": dish, })

# All dish views below are similar to main_course1!
def main_course2(request):
    category_list = Category.objects.order_by('-category')
    d2 = "Sambo Rice"
    dish = Dish.objects.get(dish=d2)
    form = DishForm()
    if request.method == "POST":
        u = User.objects.get(username=request.user.username)
        c = request.POST.get("comment_input", None)
        like = request.POST.get("like", None)
        isl = False
        if like == "like":
            isl = True
            dish.likes = dish.likes + 1
            dish.save()
        models.UserComment.objects.create(
            username=u,
            comment=c,
            dish=d2,
            islike=isl,
        )

        info_list = UserComment.objects.filter(dish=d2)
        return render(request, "rango/main_course2.html", {"info_list": info_list,
                                                           "categories": category_list,
                                                           "form": form,
                                                           "dish": dish,
                                                           })
    info_list = UserComment.objects.filter(dish=d2)
    return render(request, "rango/main_course2.html", {"info_list": info_list,
                                                       "categories": category_list,
                                                       "form": form,
                                                       "dish": dish, })


def main_course3(request):
    category_list = Category.objects.order_by('-category')
    d2 = "Sesame catsup baked wheat cake"
    dish = Dish.objects.get(dish=d2)
    form = DishForm()
    if request.method == "POST":
        u = User.objects.get(username=request.user.username)
        c = request.POST.get("comment_input", None)
        like = request.POST.get("like", None)
        isl = False
        if like == "like":
            isl = True
            dish.likes = dish.likes + 1
            dish.save()
        models.UserComment.objects.create(
            username=u,
            comment=c,
            dish=d2,
            islike=isl,
        )

        info_list = UserComment.objects.filter(dish=d2)
        return render(request, "rango/main_course3.html", {"info_list": info_list,
                                                           "categories": category_list,
                                                           "form": form,
                                                           "dish": dish,
                                                           })
    info_list = UserComment.objects.filter(dish=d2)
    return render(request, "rango/main_course3.html", {"info_list": info_list,
                                                       "categories": category_list,
                                                       "form": form,
                                                       "dish": dish, })


def soup1(request):
    category_list = Category.objects.order_by('-category')
    d2 = "Hot and Sour Soup"
    dish = Dish.objects.get(dish=d2)
    form = DishForm()
    if request.method == "POST":
        u = User.objects.get(username=request.user.username)
        c = request.POST.get("comment_input", None)
        like = request.POST.get("like", None)
        isl = False
        if like == "like":
            isl = True
            dish.likes = dish.likes + 1
            dish.save()
        models.UserComment.objects.create(
            username=u,
            comment=c,
            dish=d2,
            islike=isl,
        )

        info_list = UserComment.objects.filter(dish=d2)
        return render(request, "rango/soup1.html", {"info_list": info_list,
                                                    "categories": category_list,
                                                    "form": form,
                                                    "dish": dish,
                                                    })
    info_list = UserComment.objects.filter(dish=d2)
    return render(request, "rango/soup1.html", {"info_list": info_list,
                                                "categories": category_list,
                                                "form": form,
                                                "dish": dish, })


def soup2(request):
    category_list = Category.objects.order_by('-category')
    d2 = "Duck Bone Soup"
    dish = Dish.objects.get(dish=d2)
    form = DishForm()
    if request.method == "POST":
        u = User.objects.get(username=request.user.username)
        c = request.POST.get("comment_input", None)
        like = request.POST.get("like", None)
        isl = False
        if like == "like":
            isl = True
            dish.likes = dish.likes + 1
            dish.save()
        models.UserComment.objects.create(
            username=u,
            comment=c,
            dish=d2,
            islike=isl,
        )

        info_list = UserComment.objects.filter(dish=d2)
        return render(request, "rango/soup2.html", {"info_list": info_list,
                                                    "categories": category_list,
                                                    "form": form,
                                                    "dish": dish,
                                                    })
    info_list = UserComment.objects.filter(dish=d2)
    return render(request, "rango/soup2.html", {"info_list": info_list,
                                                "categories": category_list,
                                                "form": form,
                                                "dish": dish, })


def soup3(request):
    category_list = Category.objects.order_by('-category')
    d2 = "White Gourd and Pork Ribs Soup"
    dish = Dish.objects.get(dish=d2)
    form = DishForm()
    if request.method == "POST":
        u = User.objects.get(username=request.user.username)
        c = request.POST.get("comment_input", None)
        like = request.POST.get("like", None)
        isl = False
        if like == "like":
            isl = True
            dish.likes = dish.likes + 1
            dish.save()
        models.UserComment.objects.create(
            username=u,
            comment=c,
            dish=d2,
            islike=isl,
        )

        info_list = UserComment.objects.filter(dish=d2)
        return render(request, "rango/soup3.html", {"info_list": info_list,
                                                    "categories": category_list,
                                                    "form": form,
                                                    "dish": dish,
                                                    })
    info_list = UserComment.objects.filter(dish=d2)
    return render(request, "rango/soup3.html", {"info_list": info_list,
                                                "categories": category_list,
                                                "form": form,
                                                "dish": dish, })


def dessert1(request):
    category_list = Category.objects.order_by('-category')
    d2 = "Green Bean Soup"
    dish = Dish.objects.get(dish=d2)
    form = DishForm()
    if request.method == "POST":
        u = User.objects.get(username=request.user.username)
        c = request.POST.get("comment_input", None)
        like = request.POST.get("like", None)
        isl = False
        if like == "like":
            isl = True
            dish.likes = dish.likes + 1
            dish.save()
        models.UserComment.objects.create(
            username=u,
            comment=c,
            dish=d2,
            islike=isl,
        )

        info_list = UserComment.objects.filter(dish=d2)
        return render(request, "rango/dessert1.html", {"info_list": info_list,
                                                       "categories": category_list,
                                                       "form": form,
                                                       "dish": dish,
                                                       })
    info_list = UserComment.objects.filter(dish=d2)
    return render(request, "rango/dessert1.html", {"info_list": info_list,
                                                   "categories": category_list,
                                                   "form": form,
                                                   "dish": dish, })


def dessert2(request):
    category_list = Category.objects.order_by('-category')
    d2 = "Black Rice Cake"
    dish = Dish.objects.get(dish=d2)
    form = DishForm()
    if request.method == "POST":
        u = User.objects.get(username=request.user.username)
        c = request.POST.get("comment_input", None)
        like = request.POST.get("like", None)
        isl = False
        if like == "like":
            isl = True
            dish.likes = dish.likes + 1
            dish.save()
        models.UserComment.objects.create(
            username=u,
            comment=c,
            dish=d2,
            islike=isl,
        )

        info_list = UserComment.objects.filter(dish=d2)
        return render(request, "rango/dessert2.html", {"info_list": info_list,
                                                       "categories": category_list,
                                                       "form": form,
                                                       "dish": dish,
                                                       })
    info_list = UserComment.objects.filter(dish=d2)
    return render(request, "rango/dessert2.html", {"info_list": info_list,
                                                   "categories": category_list,
                                                   "form": form,
                                                   "dish": dish, })


def dessert3(request):
    category_list = Category.objects.order_by('-category')
    d2 = "Mung Bean Pastry"
    dish = Dish.objects.get(dish=d2)
    form = DishForm()
    if request.method == "POST":
        u = User.objects.get(username=request.user.username)
        c = request.POST.get("comment_input", None)
        like = request.POST.get("like", None)
        isl = False
        if like == "like":
            isl = True
            dish.likes = dish.likes + 1
            dish.save()
        models.UserComment.objects.create(
            username=u,
            comment=c,
            dish=d2,
            islike=isl,
        )

        info_list = UserComment.objects.filter(dish=d2)
        return render(request, "rango/dessert3.html", {"info_list": info_list,
                                                       "categories": category_list,
                                                       "form": form,
                                                       "dish": dish,
                                                       })
    info_list = UserComment.objects.filter(dish=d2)
    return render(request, "rango/dessert3.html", {"info_list": info_list,
                                                   "categories": category_list,
                                                   "form": form,
                                                   "dish": dish, })


def starter1(request):
    category_list = Category.objects.order_by('-category')
    d2 = "Water steamed buns"
    dish = Dish.objects.get(dish=d2)
    form = DishForm()
    if request.method == "POST":
        u = User.objects.get(username=request.user.username)
        c = request.POST.get("comment_input", None)
        like = request.POST.get("like", None)
        isl = False
        if like == "like":
            isl = True
            dish.likes = dish.likes + 1
            dish.save()
        models.UserComment.objects.create(
            username=u,
            comment=c,
            dish=d2,
            islike=isl,
        )

        info_list = UserComment.objects.filter(dish=d2)
        return render(request, "rango/starter1.html", {"info_list": info_list,
                                                       "categories": category_list,
                                                       "form": form,
                                                       "dish": dish,
                                                       })
    info_list = UserComment.objects.filter(dish=d2)
    return render(request, "rango/starter1.html", {"info_list": info_list,
                                                   "categories": category_list,
                                                   "form": form,
                                                   "dish": dish, })


def starter2(request):
    category_list = Category.objects.order_by('-category')
    d2 = "Hot and sour chicken feet"
    dish = Dish.objects.get(dish=d2)
    form = DishForm()
    if request.method == "POST":
        u = User.objects.get(username=request.user.username)
        c = request.POST.get("comment_input", None)
        like = request.POST.get("like", None)
        isl = False
        if like == "like":
            isl = True
            dish.likes = dish.likes + 1
            dish.save()
        models.UserComment.objects.create(
            username=u,
            comment=c,
            dish=d2,
            islike=isl,
        )

        info_list = UserComment.objects.filter(dish=d2)
        return render(request, "rango/starter2.html", {"info_list": info_list,
                                                       "categories": category_list,
                                                       "form": form,
                                                       "dish": dish,
                                                       })
    info_list = UserComment.objects.filter(dish=d2)
    return render(request, "rango/starter2.html", {"info_list": info_list,
                                                   "categories": category_list,
                                                   "form": form,
                                                   "dish": dish, })


def starter3(request):
    category_list = Category.objects.order_by('-category')

    d2 = "Honey Pork Jerky"
    dish = Dish.objects.get(dish=d2)
    form = DishForm()
    if request.method == "POST":
        u = User.objects.get(username=request.user.username)
        c = request.POST.get("comment_input", None)
        like = request.POST.get("like", None)
        isl = False
        if like == "like":
            isl = True
            dish.likes = dish.likes + 1
            dish.save()
        models.UserComment.objects.create(
            username=u,
            comment=c,
            dish=d2,
            islike=isl,
        )

        info_list = UserComment.objects.filter(dish=d2)
        return render(request, "rango/starter3.html", {"info_list": info_list,
                                                       "categories": category_list,
                                                       "form": form,
                                                       "dish": dish,
                                                       })
    info_list = UserComment.objects.filter(dish=d2)
    return render(request, "rango/starter3.html", {"info_list": info_list,
                                                   "categories": category_list,
                                                   "form": form,
                                                   "dish": dish, })

# This is to print all the comment which have been made by users
def userInfor(request):
    # if user name is correct
    user = User.objects.get(username=request.user.username)
    # get the comment_list of this user
    comment_list = UserComment.objects.filter(username=user)
    context_dict={}
    context_dict['comment_list'] = comment_list
    return render(request, "rango/userInfor.html", context=context_dict)

# this is the internal search of our django website
def test(request):
    context_dict = {}
    category_list = Category.objects.order_by('-category')
    context_dict['categories'] = category_list
    if request.method == "POST":
        # get the keyword
        keyword = request.POST.get("search", None)
        allDish = Dish.objects.all()
        SearchResult = []
        # search all dishes if dish name has this word, add it to search result
        for x in allDish:
            if keyword in x.dish:
                SearchResult.append(x)
        SearchStatus = "Error" if len(SearchResult) == 0 else "Success"
        ResultAmount = len(SearchResult)
        context_dict['keyword'] = keyword
        context_dict['SearchResult'] = SearchResult
        context_dict['SearchStatus'] = SearchStatus
        context_dict['ResultAmount'] = ResultAmount
        return render(request, 'rango/search.html', context=context_dict)
    return render(request, 'rango/search.html')

# this method never used...
def index(request):
    context_dict = {}
    category_list = Category.objects.order_by('-category')
    context_dict['categories'] = category_list

    response = render(request, 'rango/index.html', context=context_dict)
    return response
