from django.shortcuts import render
import requests as req
from django.shortcuts import redirect
from .models import Session

CLIENT_ID = "kHeXakyMxd3kdLUP8xutrZ333fUqTKpTuw0zuFUS"
CLIENT_SECRET = "OEJ7XDgh92xTP049SWGuGe3oCw6eYbIt8sKSOcwcthtDMCWbQqQjv46T0VOcu8rGbvC8NDLZtvPGPHFYHhGTyYQIUCvGTSegEXe49w9mfgn10EqInjSeOxrFLGkq1Nfq"
REDIRECT_URI = "http://localhost:4000/oauth/"
BASE_AUTH_URL = 'http://localhost:8000/oauth/authorize/'
TOKEN_URL = 'http://localhost:8000/oauth/token/'


def home(request):
    if 'sess' in request.COOKIES:
        return redirect('/events')
    auth = BASE_AUTH_URL + f"?response_type=code&client_id={CLIENT_ID}&scope=event.read"
    return render(request, 'app/index.html', context={'url': auth, 'error': request.GET.get('error', '')})


def oauth(request):
    err = request.GET.get('error', None)
    if err is not None:
        return redirect(f'/?error={err}')
    else:
        code = request.GET.get('code')
        res = req.post(TOKEN_URL, data={'code': code, 'grant_type': 'authorization_code', 'client_id': CLIENT_ID,
                                        'client_secret': CLIENT_SECRET})
        data = res.json()
        acc = data['access_token']
        so = Session.objects.create(access=acc)
        response = redirect('/events')
        response.set_cookie('sess', so.session, 360000, httponly=True, samesite='strict')
        return response


def events(request):
    if 'sess' in request.COOKIES:
        s = request.COOKIES.get('sess')
        try:
            session = Session.objects.get(session=s)
            acc = session.access
            res = req.get('http://localhost:8000/api/event', headers={
                'authorization': 'Bearer ' + acc
            })
            if res.status_code != 200:
                response = redirect('/?error=Access%20Token%20Expired')
                response.delete_cookie('session')
                return response
            else:
                data = res.json()['results']
                return render(request, 'app/events.html', context={'data': data})
        except Session.DoesNotExist:
            pass
    return redirect('/?error=Login%20First')


def logout(request):
    res = redirect('/')
    res.delete_cookie('sess')
    return res
