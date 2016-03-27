from django.template import Context, loader
from django.http import HttpResponse, HttpResponseRedirect
from contest.models import Problems, Ranklist
from submissions.forms import SubmissionsForm
from django.shortcuts import render
import datetime, subprocess

problem = {'Hello_World' : 1, 'Sum_Of_Two_Numbers' : 2, 'Small_Factorial' : 3}
contest_time = datetime.datetime(2016, 3, 27, 12, 50, 0)

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


def codecheckerDriver(solution, language, problemId):
    verdict = ["Accepted", "Internal Error", "Compilation Error", "RunTime Error", "Wrong Answer"]
    run_cmd = "/home/r3gz3n/CodeKnights/submissions/codechecker " + solution + " " + language + " " + problemId
    process = subprocess.Popen(run_cmd ,stdout=subprocess.PIPE,shell=True)
    (output, err) = process.communicate()
    exit_code = process.wait()
    return verdict[exit_code]


def handle_uploaded_file(uploaded_file, language):
    filename = "/home/r3gz3n/CodeKnights/allSubmissions/" + datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    if language == 'C':
        filename += ".c"
    elif language == 'C++':
        filename += ".cpp"
    elif language == "Python":
        filename += ".py"
    with open(filename, "w") as f:
        for line in uploaded_file:
            f.write(line)


def submitPage(request):
    if request.method == 'POST':
        try:
            team_name = request.session['team_name']
        except KeyError:
            return HttpResponseRedirect('http://localhost:8000/team/login')
        submissionsForm = SubmissionsForm(request.POST, request.FILES)
        handle_uploaded_file(request.FILES['solution'], request.POST['language'])
        if submissionsForm.is_valid():
            submission = submissionsForm.save(commit = False)
            submission.teamName = team_name
            submission_time = datetime.datetime.now()
            submission.submissionTime = submission_time.strftime("%Y_%m_%d_%H_%M_%S")
            submission.timeTaken = 1
            submission.memoryTaken = 0.2
            submission.verdict = codecheckerDriver(submission.submissionTime, request.POST['language'], request.POST['problemId'])
            try:
                rank = Ranklist.objects.get(teamName = team_name)
            except Ranklist.DoesNotExist:
                rank = Ranklist(teamName = team_name)

            if (submission.verdict[0] == 'W' or submission.verdict[0] == 'R'):
                if problem[request.POST['problemId']] == 1 and rank.problem1score == False:
                    rank.problem1WA += 1
                elif problem[request.POST['problemId']] == 2 and rank.problem2score == False:
                    rank.problem2WA += 1
                elif problem[request.POST['problemId']] == 3 and rank.problem3score == False:
                    rank.problem3WA += 1
            elif submission.verdict[0] == 'A':
                if problem[request.POST['problemId']] == 1 and rank.problem1score == False:
                    rank.problem1score = True
                    rank.score += 1
                    rank.totalWA += rank.problem1WA
                    time_taken = submission_time - contest_time
                    rank.totalTime += time_taken.seconds + 20*60*rank.problem1WA
                elif problem[request.POST['problemId']] == 2 and rank.problem2score == False:
                    rank.problem2score = True
                    rank.score += 1
                    rank.totalWA += rank.problem2WA
                    time_taken = submission_time - contest_time
                    rank.totalTime += time_taken.seconds + 20*60*rank.problem2WA
                elif problem[request.POST['problemId']] == 3 and rank.problem3score == False:
                    rank.problem3score = True
                    rank.score += 1
                    rank.totalWA += rank.problem3WA
                    time_taken = submission_time - contest_time
                    rank.totalTime += time_taken.seconds + 20*60*rank.problem3WA
            rank.save()
            submission.save()
            submissionsForm.save_m2m()


        return HttpResponseRedirect('http://localhost:8000/submissions/my');
    else:
        try:
            team_name = request.session['team_name']
        except KeyError:
            return HttpResponseRedirect('http://localhost:8000/team/login')
        submit = SubmissionsForm()
        return render(request, 'submitPage.html', {'submissionsForm':submit, 'error_message':''})


def getKey(item):
    return (item.score, item.totalTime)

def ranklistPage(request):
    ranklist = Ranklist.objects.all()
    ranklist = sorted(ranklist, key=getKey)
    t = loader.get_template("ranklistPage.html")
    c = Context({"ranklist" : ranklist})
    return HttpResponse(t.render(c))

