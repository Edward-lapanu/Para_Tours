# views.py
from django.contrib.auth.models import User 
from django.shortcuts import render, get_object_or_404, redirect
from .models import Resort, Booking, Message
from .forms import ResortForm, BookingForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required,permission_required
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView,DeleteView
from .forms import ResortForm
from django.contrib.admin.views.decorators import staff_member_required
from django.core.mail import send_mail
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.contrib.auth import authenticate

#My views
def index(request):
    # Get the search query from the GET request
    search_query = request.GET.get('search', '')
    
    # Filter resorts based on the search query, if provided
    if search_query:
        resorts = Resort.objects.filter(name__icontains=search_query)
    else:
        resorts = Resort.objects.all()
    
    # Render the home template with the filtered resorts
    return render(request, 'index.html', {'resorts': resorts})

def about(request):
    return render(request, 'about.html')
from django.contrib import messages  # Import messages

@login_required
def contact(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        message_content = request.POST.get('message')

        # Authenticate the user
        user = authenticate(username=username, password=password)
        if user is not None:
            # Debugging: Log user and content before saving
            print(f"DEBUG: Saving message for user {user.username} with content '{message_content}'")
            # Save the message to the database
            Message.objects.create(user=user, content=message_content)
            messages.success(request, 'Message sent successfully!')  # Set success message
            return redirect('perl_app:dashboard')  # Redirect to dashboard
        else:
            messages.error(request, 'Invalid password.')  # Set error message
            return render(request, 'contact.html', {'error': 'Invalid password.'})

    # If it's not POST, just render the contact page
    return render(request, 'contact.html')

def services(request):
    return render(request, 'services.html')
def resort_edit(request):
    return render(request, 'resort_form.html')

@login_required
def client_dashboard(request):
    # Fetch all bookings for the logged-in user
    bookings = Booking.objects.filter(user=request.user)

    # Count bookings for display
    total_bookings = bookings.count()
    
    return render(request, 'client_dashboard.html', {
        'bookings': bookings,
        'total_bookings': total_bookings,
    })

#dashboards for user views
@login_required
def dashboard(request):
    if request.user.is_staff:  # Admin dashboard
        total_resorts = Resort.objects.count()
        total_bookings = Booking.objects.count()
        
        # filters to use existing fields
        s_confirmed = Booking.objects.filter(is_confirmed=False).count()  # Pending bookings
        s_approved = Booking.objects.filter(is_approved=True).count()     # Approved bookings
        
        users_count = User.objects.count()
        resorts = Resort.objects.all()
        bookings = Booking.objects.filter(is_approved=True)
        #fetch all messages
        messages_list = Message.objects.all()
        print("DEBUG: Messages passed to dashboard", messages_list)  # Print to console
    
        return render(request, 'dashboard.html', {
            'total_resorts': total_resorts,
            'total_bookings': total_bookings,
            's_confirmed': s_confirmed,  
            's_approved': s_approved,    
            'users_count': users_count,
            'resorts': resorts,
            'bookings': bookings,
            'messages': messages_list,  # Pass the actual messages

        })
    else:  # Client dashboard
        bookings = Booking.objects.filter(user=request.user)
        return render(request, 'client_dashboard.html', {'bookings': bookings})


# Resort Management Views
@login_required
def resort_list(request):
    if request.user.is_staff:  # Admins can view all resorts
        resorts = Resort.objects.all()
        can_edit_any_resort = True  # Admins can edit any resort
    else:
        resorts = Resort.objects.filter(owner=request.user)  # Owners can only see their own resorts
        can_edit_any_resort = request.user.has_perm('resorts.can_edit_any_resort')

    return render(request, 'resort_list.html', {
        'resorts': resorts,
        'can_edit_any_resort': can_edit_any_resort,
    })

@login_required
def add_edit_resort(request, pk=None):
    if pk:
        resort = get_object_or_404(Resort, pk=pk)
        
        # Check if the user is either the owner or an admin with permission to edit any resort
        if resort.owner != request.user and not request.user.has_perm('resorts.can_edit_any_resort'):
            raise PermissionDenied  # If not, deny access
        
    else:
        resort = None

    if request.method == 'POST':
        form = ResortForm(request.POST, request.FILES, instance=resort)
        if form.is_valid():
            resort = form.save(commit=False)
            resort.owner = request.user  # Ensure the owner is set to the current user
            resort.save()
            return redirect('perl_app:resort_list')
    else:
        form = ResortForm(instance=resort)

    return render(request, 'resort_form.html', {'form': form})


class ResortEditView(UpdateView):
    model = Resort
    form_class = ResortForm  # The form to use for editing
    template_name = 'resort_form.html'  # The template to render the form
    success_url = reverse_lazy('perl_app:resort_list')  # Redirect after successful update




class ResortDeleteView(DeleteView):
    model = Resort
    template_name = 'resort_confirm_delete.html'
    success_url = reverse_lazy('perl_app:resort_list')

@login_required
def delete_resort(request, pk):
    resort = get_object_or_404(Resort, pk=pk, owner=request.user)  # Ensure the user is the owner
    resort.delete()
    return redirect('resort_list')

# Booking Management Views
def booking_list(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'booking_list.html', {'bookings': bookings})

def calculate_total_price(booking):
    # Example calculation: price per night * number of nights
    return booking.price_per_night * booking.number_of_nights

@login_required
def book_resort(request):
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            
            # Calculate and set the total price before saving
            booking.total_price = booking.calculate_total_price()
            
            booking.save()
            return redirect('perl_app:client_dashboard')  # Redirect to the booking list page
    else:
        form = BookingForm()

    return render(request, 'book_resort.html', {'form': form})

#user want to cancel booking

@login_required
def booking_cancel(request, pk):
    # Fetch the booking object
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    
    # Perform cancellation logic (e.g., mark as canceled or delete)
    if request.method == "POST":
        booking.status = "Canceled"  # Update the status
        booking.save()
        messages.success(request, "Booking canceled successfully.")
        return redirect('perl_app:client_dashboard')  # Redirect to the client dashboard

    # For GET request, show confirmation page
    return render(request, 'booking_cancel.html', {'booking': booking})

@login_required
def confirm_booking(request, pk):
    resort = get_object_or_404(Resort, pk=pk)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.resort = resort
            booking.user = request.user

            # Validate check-out date
            if booking.check_out_date <= booking.check_in_date:
                form.add_error('check_out_date', 'Check-out date must be later than check-in date.')
                return render(request, 'confirm_booking.html', {'form': form, 'resort': resort})

            # Calculate the total price
            total_price = (booking.check_out_date - booking.check_in_date).days * resort.price_per_night
            booking.total_price = total_price
            booking.save()

            # Redirect to confirmation page
            return redirect('perl_app:booking_confirmation', pk=booking.pk)
    else:
        form = BookingForm()

    return render(request, 'confirm_booking.html', {'form': form, 'resort': resort})


@login_required
def booking_confirmation(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    return render(request, 'booking_confirmation.html', {'booking': booking})


@staff_member_required  # Only admin users can approve bookings
def approve_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    if request.method == 'POST':
        booking.is_approved = True  # Set the booking as approved
        booking.save()
        return redirect('perl_app:booking_list')  # Redirect to a booking list page after approval
    return render(request, 'approve_booking.html', {'booking': booking})

@staff_member_required  # only admin users can access
def booking_list(request):
    bookings = Booking.objects.all()
    return render(request, 'booking_list.html', {'bookings': bookings})

# Settings View
def settings(request):
    # Example: settings could be site-wide settings or admin configurations
    return render(request, 'settings.html')





 

