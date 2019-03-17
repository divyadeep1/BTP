from django.shortcuts import render

from django.http import HttpResponse, JsonResponse

def index(request):

    return render(request, 'analyzerBot/index.html')

def report(request):

    url = request.GET['url']

    ##Use the url obtained for performing scrapping and sentiment analysis
    ##Right now, returning a simple value for the purpose of testing.

    print("URL received %s" % url)
    return JsonResponse({"val":5})