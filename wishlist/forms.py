from django import forms
from .models import Wishlist

class WishlistNoteForm(forms.ModelForm):
    class Meta:
        model = Wishlist
        fields = ['notes']  
