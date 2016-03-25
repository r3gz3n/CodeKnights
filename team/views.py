from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader, Context
from team.models import TeamDetails
from team.forms import TeamDetailsForm, TeamPassForm


def teamPage(request):
    try:
        team_name = request.session['team_name']
    except KeyError:
        return HttpResponseRedirect('http://localhost:8000/team/login')
    team_details = TeamDetails.objects.get(teamName=team_name)
    t = loader.get_template('teamPage.html')
    c = Context({'team':team_details})
    return HttpResponse(t.render(c))

def signupPage(request):
    if request.method == 'POST':
        signup_form = TeamDetailsForm(request.POST)
        if signup_form.is_valid():
            team_name = signup_form.cleaned_data['teamName']
            try:
                team_details = TeamDetails.objects.get(teamName=team_name)
                signup_form.save()
            except TeamDetails.DoesNotExist:
                signup_form = TeamDetailsForm()
                return render(request, 'signupPage.html', {'signup_form':signup_form, 'error_message':'Team Name Already Exists'})
        login_form = TeamPassForm()
        try:
            del request.session['team_name']
        except KeyError:
            pass
        return HttpResponseRedirect('http://localhost:8000/team/login', {'form':login_form, 'error_message':''})
    else:
        signup_form = TeamDetailsForm()
        return render(request, 'signupPage.html', {'signup_form':signup_form, 'error_message':''})

def loginPage(request):
    if request.method == 'POST':
        login_form = TeamPassForm(request.POST)
        if login_form.is_valid():
            team_name = login_form.cleaned_data['teamName']
            try:
                team_pass = TeamDetails.objects.get(teamName=team_name)
            except TeamDetails.DoesNotExist:
                return render(request, 'loginPage.html', {'login_form':login_form, 'error_message':'Wrong Team Name or Password'})
            if team_pass.password == login_form.cleaned_data['password']:
                request.session['team_name'] = team_name
                return HttpResponseRedirect('http://localhost:8000/team/teampage')
            else:
                login_form = TeamPassForm()
                try:
                    del request.session['team_name']
                except KeyError:
                    pass
                return render(request, 'loginPage.html', {'login_form':login_form, 'error_message':'Wrong Team Name or Password'})
        else:
            login_form = TeamPassForm()
            try:
                del request.session['team_name']
            except KeyError:
                pass
            return render(request, 'loginPage.html', {'login_form':login_form})

    else:
        login_form = TeamPassForm()
        try:
            del request.session['team_name']
        except KeyError:
            pass
        return render(request, 'loginPage.html', {'login_form':login_form})

def editPage(request):
    if request.method == 'POST':
        try:
            team_name = request.session['team_name']
        except KeyError:
            return HttpResponseRedirect('http://localhost:8000/team/login')
        team_details = TeamDetails.objects.get(teamName=team_name)
        edit_form = TeamDetailsForm(request.POST, instance = team_details)
        edit_form.save()
        login_form = TeamPassForm()
        try:
            del request.session['team_name']
        except KeyError:
            pass
        return HttpResponseRedirect('http://localhost:8000/team/login', {'form':login_form})
    else:
        try:
            team_name = request.session['team_name']
        except KeyError:
            return HttpResponseRedirect('http://localhost:8000/team/login')
        team_details = TeamDetails.objects.get(teamName=team_name)
        edit_form = TeamDetailsForm(initial={'teamName':team_details.teamName,
                                                'member1Name':team_details.member1Name,
                                                'member1Branch':team_details.member1Branch,
                                                'member2Name':team_details.member2Name,
                                                'member2Branch':team_details.member2Branch,
                                                'member3Name':team_details.member3Name,
                                                'member3Branch':team_details.member3Branch,
                                                }
                                        )
        return render(request, 'editPage.html', {'edit_form':edit_form})


def logout(request):
    try:
        del request.session['team_name']
    except KeyError:
        pass
    return HttpResponseRedirect('http://localhost:8000/team/login')
