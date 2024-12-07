from django import forms
from .models import Resort, Booking, User

# Form for creating or editing a resort
class ResortForm(forms.ModelForm):
    class Meta:
        model = Resort
        fields = ['name', 'description', 'price_per_night', 'location', 'image']

# Form for creating a booking
class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['resort', 'check_in_date', 'check_out_date']  
    check_in_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}), 
        label="Check-In Date"
    )
    check_out_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}), 
        label="Check-Out Date"
    )
    # resort = forms.ModelChoiceField(queryset=Resort.objects.all(), required=False)  # Make sure it's required  # Add more fields as necessary


