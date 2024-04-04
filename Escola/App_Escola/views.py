from django.shortcuts import render

def abre_index(request):
 return render(request, 'login.html')