from django.shortcuts import render


def home(request):
    return render(request, template_name='index.html')

# Home, Open/close of bug (by project manager)
# Bug type, (by PM, not Reporter)
