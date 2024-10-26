from django import forms

class WishlistNoteForm(forms.Form):
    car_id = forms.IntegerField(widget=forms.HiddenInput())
    note = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Enter your note here...'}), required=False)