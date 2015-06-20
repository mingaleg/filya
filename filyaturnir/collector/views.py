from collector.models import Submit, get_lasts_ok_submits, Battle, BattleSerial
from django.http import Http404
from django.shortcuts import render_to_response, redirect, render
from django.contrib.auth.models import User
import os, tempfile, zipfile
from django.core.servers.basehttp import FileWrapper
from django.http import HttpResponse, HttpResponseRedirect

from django.contrib import auth

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/")


from django import forms

class UploadSubmitForm(forms.Form):
    source = forms.FileField()
    language = forms.CharField(max_length=100)

def download_finals(request):
    temp = tempfile.TemporaryFile()
    archive = zipfile.ZipFile(temp, 'w', zipfile.ZIP_DEFLATED)
    for submit in get_lasts_ok_submits():
        filename = os.path.split(submit.source_file)[-1]
        archive.write(submit.source_file, filename)
    archive.close()
    wrapper = FileWrapper(temp)
    response = HttpResponse(wrapper, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=filya.zip'
    response['Content-Length'] = temp.tell()
    temp.seek(0)
    return response

def upload_submit(request):
    if request.method == 'POST':
        form = UploadSubmitForm(request.POST, request.FILES)
        if form.is_valid():
            source = ''.join(map(lambda x: x.decode(), request.FILES['source'].chunks()))
            Submit.objects.create(
                user = request.user,
                source = source,
                language = form.cleaned_data['language'],
            )
            return redirect('/submit')
    else:
            form = UploadSubmitForm()
    return render(request, 'upload.html', {'form': form})

def page_for_submit(request, submit_id, page):
    try:
        foo = Submit.objects.get(sid = submit_id)
    except:
        raise Http404
    if request.user.is_staff or (request.user == foo.user):
        return render_to_response(page, {'submit': foo})
    else:
        return render_to_response('permission_denied.html', {'submit': foo})

def view_battle(request, battle_id):
    try:
        foo = Battle.objects.get(sid = battle_id)
    except:
        raise 404
    return render_to_response('battle.html', {'battle': foo})

def view_all_serials(request):
    foo = list(BattleSerial.objects.order_by('-sid'))
    if not request.user.is_staff:
        for i in range(len(foo)-1, -1, -1):
            if foo[i].player1.user.is_staff or foo[i].player2.user.is_staff:
                foo.pop(i)
    return render(request, 'all_serials.html', {'serials': foo})

def view_serial(request, serial_id):
    try:
        foo = BattleSerial.objects.get(sid = serial_id)
    except:
        raise 404
    return render_to_response('serial.html', {'serial': foo})

def view_own_submits(request):
    if request.method == 'POST':
        form = UploadSubmitForm(request.POST, request.FILES)
        if form.is_valid():
            source = ''.join(map(lambda x: x.decode(), request.FILES['source'].chunks()))
            submit = Submit.objects.create(
                user = request.user,
                source = source,
                language = form.cleaned_data['language'],
            )
            submit.submit()
            return redirect('/submit')
    else:
            form = UploadSubmitForm()
    foo = Submit.objects.filter(user=request.user).order_by("-sid")
    return render(request, 'own_submits.html', {'submits': foo, 'form': form})

def view_all_submits(request):
    foo = []
    if request.user.is_staff:
        foo = Submit.objects.order_by("-sid")
    return render(request, 'all_submits.html', {'submits': foo})

def view_last_ok_submits(request):
    foo = []
    if request.user.is_staff:
        foo = get_lasts_ok_submits()
    return render(request, 'final_submits.html', {'submits': foo})

def view_all_submits_by_user(request, username):
    foo = []
    if request.user.is_staff:
        try:
            user = User.objects.get(username = username)
        except:
            raise Http404
        foo = Submit.objects.filter(user=user).order_by("-sid")
    return render(request, 'all_submits.html', {'submits': foo, 'username': username})

def view_source(request, submit_id):
    return page_for_submit(request, submit_id, 'view_source.html')

def view_log(request, submit_id):
    return page_for_submit(request, submit_id, 'compile_log.html')

def view_rules(request):
    if request.user.is_authenticated():
        return render(request, 'rules.html')
    else:
        return redirect('/login/')


def make_serial_1(request):
    if request.user.is_authenticated():
        return render(request, 'makeserial1.html', {'submits': get_lasts_ok_submits()})
    else:
        return redirect('/login/')

def make_serial_2(request, firstsubmit):
    try:
        firstsubmit = Submit.objects.get(sid = firstsubmit)
    except:
        raise 404
    if request.user.is_authenticated():
        return render(request, 'makeserial2.html', {'submits': get_lasts_ok_submits(), 'firstsubmit': firstsubmit})
    else:
        return redirect('/login/')

def make_serial(request, firstsubmit, secondsubmit, bo=5):
    try:
        firstsubmit = Submit.objects.get(sid = firstsubmit)
    except:
        raise 404
    try:
        secondsubmit = Submit.objects.get(sid = secondsubmit)
    except:
        raise 404
    serial = BattleSerial.objects.create(
        player1=firstsubmit,
        player2=secondsubmit,
        games=bo,
    )
    return redirect('/serial/3')

def runserial(request, serial_id):
    try:
        foo = BattleSerial.objects.get(sid = serial_id)
    except:
        raise 404
    foo.run()
    return HttpResponse('done')
