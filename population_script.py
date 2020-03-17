import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'django_team_project.settings')

import django

django.setup()
from rango.models import Category, Dish

#

def populate():
    appetizer = [
        {
            "dish": "Water steamed buns",
            "url": "http://127.0.0.1:8000/rango/starter1",
            "likes": 5,
        },
        {
            "dish": "Hot and sour chicken feet",
            "url": "http://127.0.0.1:8000/rango/starter2",
            "likes": 7,
        },
        {
            "dish": "Honey Pork Jerky",
            "url": "http://127.0.0.1:8000/rango/starter3",
            "likes": 58,
        },

    ]

    soup = [
        {
            "dish": "Hot and Sour Soup",
            "url": "http://127.0.0.1:8000/rango/soup1",
            "likes": 15,
        },
        {
            "dish": "Duck Bone Soup",
            "url": "http://127.0.0.1:8000/rango/soup2",
            "likes": 54,
        },
        {
            "dish": "White Gourd and Pork Ribs Soup",
            "url": "http://127.0.0.1:8000/rango/soup3",
            "likes": 50,
        },
    ]

    main_course = [
        {
            "dish": "Oil spilled noodles",
            "url": "http://127.0.0.1:8000/rango/main_course1",
            "likes": 37,
        },
        {
            "dish": "Sambo Rice",
            "url": "http://127.0.0.1:8000/rango/main_course2",
            "likes": 21,
        },
        {
            "dish": "Sesame catsup baked wheat cake",
            "url": "http://127.0.0.1:8000/rango/main_course3",
            "likes": 99,
        },
    ]

    dessert = [
        {
            "dish": "Green Bean Soup",
            "url": "http://127.0.0.1:8000/rango/dessert1",
            "likes": 36,
        },
        {
            "dish": "Black Rice Cake",
            "url": "http://127.0.0.1:8000/rango/dessert2",
            "likes": 3,
        },
        {
            "dish": "Mung Bean Pastry",
            "url": "http://127.0.0.1:8000/rango/dessert3",
            "likes": 75,
        },
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
            add_dish(c, d["dish"], d["url"])

    for cat in Category.objects.all():
        for d in Dish.objects.filter(category=cat):
            print(f'-{c}:{d}')


def add_dish(cat, dish, url):
    d = Dish.objects.get_or_create(category=cat, dish=dish)[0]
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
