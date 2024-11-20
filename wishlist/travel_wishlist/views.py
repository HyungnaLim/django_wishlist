from django.shortcuts import render, redirect, get_object_or_404
from .models import Place
from .forms import NewPlaceForm, TripReviewForm
from django.contrib.auth.decorators import login_required # login decorators to enable user can see their own places
from django.http import HttpResponseForbidden
from django.contrib import messages


@login_required()
def place_list(request):

    if request.method == 'POST':
        # create new place
        form = NewPlaceForm(request.POST)  # create a form from data in the request
        place = form.save(commit=False)  # create a model object from form. commit=False means to get the data but not save yet
        place.user = request.user
        if form.is_valid():  # validation against DB constraints
            place.save()  # save place to DB
            return redirect('place_list')  # reload home page

    places = Place.objects.filter(visited=False).filter(user=request.user).order_by('name')
    new_place_form = NewPlaceForm  # used to create html
    return render(request, 'travel_wishlist/wishlist.html', {'places':places, 'new_place_form':new_place_form})


@login_required()
def about(request):
    author = 'Hyungna'
    about = 'A website to create a list of place to visit'
    return render(request, 'travel_wishlist/about.html', {'author':author, 'about':about})


@login_required()
def places_visited(request):
    visited = Place.objects.filter(visited=True).filter(user=request.user).order_by('name')
    return render(request, 'travel_wishlist/visited.html', {'visited':visited})


@login_required()
def place_was_visited(request, place_pk):
    if request.method == 'POST':
        # place = Place.objects.get(pk=place_pk)
        place = get_object_or_404(Place, pk=place_pk)   # if object is not found, return 404 error response
        if place.user == request.user:  # only allow changing visited data for user who created the place
            place.visited = True
            place.save()
        else:
            return HttpResponseForbidden  # prevent making change from user who didn't create the place
    return redirect('place_list')   # redirect to the path 'place_list'


@login_required()
def place_details(request, place_pk):
    place = get_object_or_404(Place, pk=place_pk)

    # check for user
    if place.user != request.user:
        return HttpResponseForbidden()

    # if POST request, validate form data and update
    if request.method == 'POST':
        form = TripReviewForm(request.POST, request.FILES, instance=place)
        if form.is_valid():
            form.save()
            messages.info(request, 'Trip information updated!')
            return redirect('place_details', place_pk=place_pk)
        else:
            messages.error(request, form.errors)  #TODO refine later

    else:  # if get request, show Place info and optional form
        if place.visited:
            review_form = TripReviewForm(instance=place)
            return render(request, 'travel_wishlist/place_details.html', {'place':place, 'review_form':review_form})
        else:
            return render(request, 'travel_wishlist/place_details.html', {'place': place})


@login_required()
def delete_place(request, place_pk):
    place = get_object_or_404(Place, pk=place_pk)
    if place.user == request.user:
        place.delete()
        return redirect('place_list')
    else:
        return HttpResponseForbidden