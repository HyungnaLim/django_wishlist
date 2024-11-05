from django.shortcuts import render, redirect
from .models import Place
from .forms import NewPlaceForm

def place_list(request):

    if request.method == 'POST':
        # create new place
        form = NewPlaceForm(request.POST)  # create a form from data in the request
        place = form.save()  # create a model object from form
        if form.is_valid():  # validation against DB constraints
            place.save()  # save place to DB
            return redirect('place_list')  # reload home page

    places = Place.objects.filter(visited=False).order_by('name')
    new_place_form = NewPlaceForm  # used to create html
    return render(request, 'travel_wishlist/wishlist.html', {'places':places, 'new_place_form':new_place_form})

def about(request):
    author = 'Hyungna'
    about = 'A website to create a list of place to visit'
    return render(request, 'travel_wishlist/about.html', {'author':author, 'about':about})

def places_visited(request):
    visited = Place.objects.filter(visited=True).order_by('name')
    return render(request, 'travel_wishlist/visited.html', {'visited':visited})
