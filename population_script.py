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
            "url": "/rango/starter1",
            "likes": 5,
            "images": "/static/images/starter1.png",
        },
        {
            "dish": "Hot and sour chicken feet",
            "url": "/rango/starter2",
            "likes": 7,
            "images": "/static/images/starter2.png",
        },
        {
            "dish": "Honey Pork Jerky",
            "url": "/rango/starter3",
            "likes": 58,
            "images": "/static/images/starter3.png",
        },

    ]

    soup = [
        {
            "dish": "Hot and Sour Soup",
            "url": "/rango/soup1",
            "likes": 15,
            "images": "/static/images/soup1.png",
        },
        {
            "dish": "Duck Bone Soup",
            "url": "/rango/soup2",
            "likes": 54,
            "images": "/static/images/soup2.png",
        },
        {
            "dish": "White Gourd and Pork Ribs Soup",
            "url": "/rango/soup3",
            "likes": 50,
            "images": "/static/images/soup3.png",
        },
    ]

    main_course = [
        {
            "dish": "Oil spilled noodles",
            "url": "/rango/main_course1",
            "likes": 37,
            "images": "/static/images/main_course1.png",
        },
        {
            "dish": "Sambo Rice",
            "url": "/rango/main_course2",
            "likes": 21,
            "images": "/static/images/main_course2.png",
        },
        {
            "dish": "Sesame catsup baked wheat cake",
            "url": "/rango/main_course3",
            "likes": 99,
            "images": "/static/images/main_course3.png",
        },
    ]

    dessert = [
        {
            "dish": "Green Bean Soup",
            "url": "/rango/dessert1",
            "likes": 36,
            "images": "/static/images/dessert1.png",
        },
        {
            "dish": "Black Rice Cake",
            "url": "/rango/dessert2",
            "likes": 3,
            "images": "/static/images/dessert2.png",
        },
        {
            "dish": "Mung Bean Pastry",
            "url": "/rango/dessert3",
            "likes": 75,
            "images": "/static/images/dessert3.png",
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
            add_dish(c, d["dish"], d["url"], d["likes"], d["images"])

    for cat in Category.objects.all():
        for d in Dish.objects.filter(category=cat):
            print(f'-{c}:{d}')


def add_dish(cat, dish, url, likes, images):
    d = Dish.objects.get_or_create(category=cat, dish=dish)[0]
    d.url = url
    d.likes = likes
    d.images = images
    d.save()
    return d


def add_category(cat):
    c = Category.objects.get_or_create(category=cat)[0]
    c.save()
    return c


if __name__ == '__main__':
    print("Starting")
    populate()
