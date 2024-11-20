from django.core.files.storage import default_storage
from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import storages

class Place(models.Model):
    user = models.ForeignKey('auth.User', null=False, on_delete=models.CASCADE)
    # foreign key user - can't be null, if it is deleted remove all the associated Place data
    name = models.CharField(max_length=200)  # place name
    visited = models.BooleanField(default=False)  # visited boolean
    notes = models.TextField(blank=True, null=True)  # optional note
    date_visited = models.DateField(blank=True, null=True)  # optional date
    photo = models.ImageField(upload_to='user_images/', blank=True, null=True)
    # optional image uploaded to user_images directory
    # user_images directory will be created when user uploads images via app

    # overwrite save function
    def save(self, *args, **kwargs):
        old_place = Place.objects.filter(pk=self.pk).first()
        # delete photo if the saved photo is not the same as the one that is being saved
        if old_place and old_place.photo:
            if old_place.photo != self.photo:
                self.delete_photo(old_place.photo)
        super().save(*args, **kwargs)

    def delete_photo(self, photo):
        if default_storage.exists(photo.name):
            default_storage.delete(photo.name)

    # overwrite delete function
    def delete(self, *args, **kwargs):
        if self.photo:
            self.delete_photo(self.photo)
        super().delete(*args, **kwargs)

    def __str__(self):
        photo_str = self.photo.url if self.photo else 'no photo'
        notes_str = self.notes[100:] if self.notes else 'no notes'

        return f'{self.name} visited? {self.visited} on {self.date_visited}. Notes: {notes_str} Photo: {photo_str}'
