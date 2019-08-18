from django import forms
from django.forms import ModelForm
from futground.models import Reservation,Ground,Rating
from django.contrib.auth.models import User


class UserReservationForm(forms.Form):
    ground = forms.ModelChoiceField(queryset=Ground.objects.all())
    starting_time = forms.TimeField()
    ending_time = forms.TimeField()
    reserved_date = forms.DateField()

    class Meta:
        model = Reservation
        fields = ['ground', 'starting_time', 'ending_time', 'reserved_date']


class RatingForm(forms.Form):
       user = forms.ModelChoiceField(queryset=User.objects.all())
       ground = forms.ModelChoiceField(queryset=Ground.objects.all())
       rate = forms.IntegerField(min_value=1,max_value=5)

       class Meta:
           model= Rating
           fields=['user','ground','rate']