from django.shortcuts import render
from django.views import View
from django.shortcuts import render
# Create your views here.


def TempView(request):
    ctxt = {"words": "temp page"}
    return render(request, "matching/temp.html", ctxt)
