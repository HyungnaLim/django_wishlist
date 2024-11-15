from django.db import models
from django.contrib.auth.models import User

class Place(models.Model):
    user = models.ForeignKey('auth.User', null=False, on_delete=models.CASCADE)
    # foreign key user - can't be null, if it is deleted remove all the associated Place data
    name = models.CharField(max_length=200)  # place name
    visited = models.BooleanField(default=False)  # visited boolean
    notes = models.TextField(blank=True, null=True)  # optional note
    date_visited = models.DateField(blank=True, null=True)  # optional date
    photo = models.ImageField(upload_to='user_images/', blank=True, null=True)
    # optional image uploaded to user_images directory

    def __str__(self):
        photo_str = self.photo.url if self.photo else 'no photo'
        notes_str = self.notes[100:] if self.notes else 'no notes'

        return f'{self.name} visited? {self.visited} on {self.date_visited}. Notes: {notes_str} Photo: {photo_str}'
