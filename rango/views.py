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


def show_category(request, category_name_slug):
    context_dict = {}
    category_list = Category.objects.order_by('-category')
    context_dict['categories'] = category_list
    try:
        category = Category.objects.get(slug=category_name_slug)

        dishes = Dish.objects.filter(category=category)

        context_dict['dishes'] = dishes

        context_dict['category'] = category

    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['pages'] = None

    return render(request, 'rango/category.html', context_dict)


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

    context_dict = {'form': form, 'category': category, 'categories': category_list, 'success': success}
    return render(request, 'rango/add_dish.html', context=context_dict)


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


def main_course1(request):
    category_list = Category.objects.order_by('-category')
    d = "main_course1"
    d2 = "Oil spilled noodles"
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
            dish=d,
            islike=isl,
        )

        info_list = UserComment.objects.filter(dish=d)
        return render(request, "rango/main_course1.html", {"info_list": info_list,
                                                           "categories": category_list,
                                                           "form": form,
                                                           "dish": dish,
                                                           })
    info_list = UserComment.objects.filter(dish=d)
    return render(request, "rango/main_course1.html", {"info_list": info_list,
                                                       "categories": category_list,
                                                       "form": form,
                                                       "dish": dish, })


def main_course2(request):
    category_list = Category.objects.order_by('-category')
    d = "main_course2"
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
            dish=d,
            islike=isl,
        )

        info_list = UserComment.objects.filter(dish=d)
        return render(request, "rango/main_course2.html", {"info_list": info_list,
                                                           "categories": category_list,
                                                           "form": form,
                                                           "dish": dish,
                                                           })
    info_list = UserComment.objects.filter(dish=d)
    return render(request, "rango/main_course2.html", {"info_list": info_list,
                                                       "categories": category_list,
                                                       "form": form,
                                                       "dish": dish, })


def main_course3(request):
    category_list = Category.objects.order_by('-category')
    d = "main_course3"
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
            dish=d,
            islike=isl,
        )

        info_list = UserComment.objects.filter(dish=d)
        return render(request, "rango/main_course3.html", {"info_list": info_list,
                                                           "categories": category_list,
                                                           "form": form,
                                                           "dish": dish,
                                                           })
    info_list = UserComment.objects.filter(dish=d)
    return render(request, "rango/main_course3.html", {"info_list": info_list,
                                                       "categories": category_list,
                                                       "form": form,
                                                       "dish": dish, })


def soup1(request):
    category_list = Category.objects.order_by('-category')
    d = "soup1"
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
            dish=d,
            islike=isl,
        )

        info_list = UserComment.objects.filter(dish=d)
        return render(request, "rango/soup1.html", {"info_list": info_list,
                                                    "categories": category_list,
                                                    "form": form,
                                                    "dish": dish,
                                                    })
    info_list = UserComment.objects.filter(dish=d)
    return render(request, "rango/soup1.html", {"info_list": info_list,
                                                "categories": category_list,
                                                "form": form,
                                                "dish": dish, })


def soup2(request):
    category_list = Category.objects.order_by('-category')
    d = "soup2"
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
            dish=d,
            islike=isl,
        )

        info_list = UserComment.objects.filter(dish=d)
        return render(request, "rango/soup2.html", {"info_list": info_list,
                                                    "categories": category_list,
                                                    "form": form,
                                                    "dish": dish,
                                                    })
    info_list = UserComment.objects.filter(dish=d)
    return render(request, "rango/soup2.html", {"info_list": info_list,
                                                "categories": category_list,
                                                "form": form,
                                                "dish": dish, })


def soup3(request):
    category_list = Category.objects.order_by('-category')
    d = "soup3"
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
            dish=d,
            islike=isl,
        )

        info_list = UserComment.objects.filter(dish=d)
        return render(request, "rango/soup3.html", {"info_list": info_list,
                                                    "categories": category_list,
                                                    "form": form,
                                                    "dish": dish,
                                                    })
    info_list = UserComment.objects.filter(dish=d)
    return render(request, "rango/soup3.html", {"info_list": info_list,
                                                "categories": category_list,
                                                "form": form,
                                                "dish": dish, })


def dessert1(request):
    category_list = Category.objects.order_by('-category')
    d = "dessert1"
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
            dish=d,
            islike=isl,
        )

        info_list = UserComment.objects.filter(dish=d)
        return render(request, "rango/dessert1.html", {"info_list": info_list,
                                                       "categories": category_list,
                                                       "form": form,
                                                       "dish": dish,
                                                       })
    info_list = UserComment.objects.filter(dish=d)
    return render(request, "rango/dessert1.html", {"info_list": info_list,
                                                   "categories": category_list,
                                                   "form": form,
                                                   "dish": dish, })


def dessert2(request):
    category_list = Category.objects.order_by('-category')
    d = "dessert2"
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
            dish=d,
            islike=isl,
        )

        info_list = UserComment.objects.filter(dish=d)
        return render(request, "rango/dessert2.html", {"info_list": info_list,
                                                       "categories": category_list,
                                                       "form": form,
                                                       "dish": dish,
                                                       })
    info_list = UserComment.objects.filter(dish=d)
    return render(request, "rango/dessert2.html", {"info_list": info_list,
                                                   "categories": category_list,
                                                   "form": form,
                                                   "dish": dish, })


def dessert3(request):
    category_list = Category.objects.order_by('-category')
    d = "dessert3"
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
            dish=d,
            islike=isl,
        )

        info_list = UserComment.objects.filter(dish=d)
        return render(request, "rango/dessert3.html", {"info_list": info_list,
                                                       "categories": category_list,
                                                       "form": form,
                                                       "dish": dish,
                                                       })
    info_list = UserComment.objects.filter(dish=d)
    return render(request, "rango/dessert3.html", {"info_list": info_list,
                                                   "categories": category_list,
                                                   "form": form,
                                                   "dish": dish, })


def starter1(request):
    category_list = Category.objects.order_by('-category')
    d = "starter1"
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
            dish=d,
            islike=isl,
        )

        info_list = UserComment.objects.filter(dish=d)
        return render(request, "rango/starter1.html", {"info_list": info_list,
                                                       "categories": category_list,
                                                       "form": form,
                                                       "dish": dish,
                                                       })
    info_list = UserComment.objects.filter(dish=d)
    return render(request, "rango/starter1.html", {"info_list": info_list,
                                                   "categories": category_list,
                                                   "form": form,
                                                   "dish": dish, })


def starter2(request):
    category_list = Category.objects.order_by('-category')
    d = "starter2"
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
            dish=d,
            islike=isl,
        )

        info_list = UserComment.objects.filter(dish=d)
        return render(request, "rango/starter2.html", {"info_list": info_list,
                                                       "categories": category_list,
                                                       "form": form,
                                                       "dish": dish,
                                                       })
    info_list = UserComment.objects.filter(dish=d)
    return render(request, "rango/starter2.html", {"info_list": info_list,
                                                   "categories": category_list,
                                                   "form": form,
                                                   "dish": dish, })


def starter3(request):
    category_list = Category.objects.order_by('-category')
    d = "starter3"

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
            dish=d,
            islike=isl,
        )

        info_list = UserComment.objects.filter(dish=d)
        return render(request, "rango/starter3.html", {"info_list": info_list,
                                                       "categories": category_list,
                                                       "form": form,
                                                       "dish": dish,
                                                       })
    info_list = UserComment.objects.filter(dish=d)
    return render(request, "rango/starter3.html", {"info_list": info_list,
                                                   "categories": category_list,
                                                   "form": form,
                                                   "dish": dish, })


def userInfor(request):
    user = User.objects.get(username=request.user.username)
    comment_list = UserComment.objects.filter(username=user)
    context_dict={}
    context_dict['comment_list'] = comment_list
    return render(request, "rango/userInfor.html", context=context_dict)


def test(request):
    context_dict = {}
    category_list = Category.objects.order_by('-category')
    context_dict['categories'] = category_list
    if request.method == "POST":
        keyword = request.POST.get("search", None)
        allDish = Dish.objects.all()
        SearchResult = []
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


def index(request):
    context_dict = {}
    category_list = Category.objects.order_by('-category')
    context_dict['categories'] = category_list

    response = render(request, 'rango/index.html', context=context_dict)
    return response


def test(request):
    user = User.objects.get(username=request.user.username)
    context_dict = {}
    context_dict['user'] = user
    return render(request, 'rango/test.html', context=context_dict)
