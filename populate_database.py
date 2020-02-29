import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'django_team_project.settings')

import django

django.setup()
from rango.models import Category, Dish

def populate():
    appetizer = [
        {
            "dish": "ABC",
            "ingredient": "none",
            "cost": "1pound",
            "url": "http://127.0.0.1:8000/rango/",
        },


    ]

    soup = [
        {
            "dish": "BCD",
            "ingredient": "none",
            "cost": "1 pound",
            "url": "http://127.0.0.1:8000/rango/",
        },
    ]

    main_course = [
        {
            "dish": "CDE",
            "ingredient": "none",
            "cost": "1 pound",
            "url": "http://127.0.0.1:8000/rango/",
        }
    ]

    dessert = [
        {
            "dish": "DEF",
            "ingredient": "none",
            "cost": "1 pound",
            "url": "http://127.0.0.1:8000/rango/",
        }
    ]

    categories = {
        "appetizer": {"Dishes": appetizer, },
        "soup": {"Dishes": soup, },
        "main_course": {"Dishes": main_course, },
        "dessert": {"Dishes": dessert, },
    }

    for cat, cat_data in categories.items():
        c = add_category(cat)
        for d in cat_data["Dishes"]:
            add_dish(c, d["dish"], d["ingredient"], d["cost"], d["url"])

    for cat in Category.objects.all():
        for d in Dish.objects.filter(category=cat):
            print(f'-{c}:{d}')


def add_dish(cat, dish, ingredient, cost, url):
    d = Dish.objects.get_or_create(category=cat, dish=dish)[0]
    d.ingredient = ingredient
    d.cost = cost
    d.url = url
    d.save()
    return d


def add_category(cat):
    c = Category.objects.get_or_create(category=cat)[0]
    c.save()
    return c


if __name__ == '__main__':
    print("Starting")
    populate()
