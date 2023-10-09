from django.shortcuts import render



def index(request):
    return render(request, 'core/index.html')

# For about us page
def about_us(request):
    return render(request, 'core/about_us.html')
