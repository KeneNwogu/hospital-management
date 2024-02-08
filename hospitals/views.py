from django.shortcuts import render
from django.core.exceptions import ValidationError

from hospitals.models import Hospital


def landing_page(request):
    return render(request, 'index.html')

def all_hospitals(request):
    hospitals = Hospital.objects.all()
    return render(request, 'hospitals.html', context={'hospitals': hospitals})


def get_detail(request, hospital_id):
    try:
        hospital = Hospital.objects.get(id=hospital_id)
        return render(request, 'hospital_detail.html', context={'hospital': hospital})
    except (Hospital.DoesNotExist, ValidationError):
        return render(request, 'hospital_detail.html', context={'hospital': None})
