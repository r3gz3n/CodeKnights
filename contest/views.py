from django.template import Context, loader
from django.http import HttpResponse, HttpResponseRedirect
from contest.models import Problems
from submissions.models import Submissions
from submissions.forms import SubmissionsForm
from django.shortcuts import render


class Problem(object):
    def __init__(self, problemId, problemTitle, problemStatement=''):
        self.problemId = problemId
        self.problemTitle = problemTitle
        self.problemStatement = problemStatement



def problemPage(request):
    if 'team_name' not in request.session:
        return HttpResponseRedirect('http://localhost:8000/team/login')
    problem_id = request.GET.get('q')
    try:
        problem_details = Problems.objects.get(problemId=problem_id)
    except Problems.DoesNotExist:
        return HttpResponseRedirect('http://localhost:8000/contest/firstcontest')
    problem_path = problem_details.problemPath
    problem_title = problem_details.problemTitle
    problem_statement = ''
    with open(problem_path + '/problemStatement.txt', 'r') as problemStatementFile:
        problem_statement += problemStatementFile.read()
    p = Problem(problem_id, problem_title, problem_statement)
    t = loader.get_template('problemPage.html')
    c = Context({'problem':p})
    return HttpResponse(t.render(c))



def contestPage(request):
    if 'team_name' not in request.session:
        return HttpResponseRedirect('http://localhost:8000/team/login')
    problems = Problems.objects.all()
    problem_details = list()
    for p in problems:
        problem_details.append(Problem(p.problemId, p.problemTitle))
    t = loader.get_template('contestPage.html')
    c = Context({'problems':problem_details})
    return HttpResponse(t.render(c))

def submitPage(request):
    if request.method == 'POST':
        print ":P"
        try:
            team_name = request.session['team_name']
        except KeyError:
            return HttpResponseRedirect('http://localhost:8000/team/login')
        submissionsForm = SubmissionsForm(request.POST)
        print request.POST['solution']
        '''
        if submissionsForm.is_valid():
            submission = submissionsForm.save(commit = False)
            submission.teamName = team_name
            submission.submissionTime = datatime.datetime.now()
            submission.solution
        '''
        return HttpResponseRedirect('http://localhost:8000/submissions/my');

    else:
        try:
            team_name = request.session['team_name']
        except KeyError:
            return HttpResponseRedirect('http://localhost:8000/team/login')
        submit = SubmissionsForm()
        return render(request, 'submitPage.html', {'submissionsForm':submit, 'error_message':''})
