from django.template import Context, loader
from django.http import HttpResponse, HttpResponseRedirect
from contest.models import Problems, Ranklist
from submissions.forms import SubmissionsForm
from django.shortcuts import render
import datetime, subprocess, os

problem = {'Hello_World' : 1, 'Sum_Of_Two_Numbers' : 2, 'Small_Factorial' : 3}
contest_time = datetime.datetime(2016, 3, 27, 12, 50, 0)
verdict = ["Accepted", "Internal Error", "Compilation Error", "RunTime Error", "Wrong Answer", "Time Limit Exceeded", "Memory Limit Exceeded"]


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


def compileRun(solution, language, problem_id):
    problem = Problems.objects.get(problemId = problem_id)
    filename = '/home/r3gz3n/CodeKnights/allSubmissions/' + solution
    if language == 'C':
        filename += '.c'
    elif language == 'C++':
        filename += '.cpp'
    else:
        filename += '.py'
    TEST_DIR = '/home/r3gz3n/CodeKnights/logs'
    errfile = os.path.join(TEST_DIR, "error.log")
    outputfile = os.path.join(TEST_DIR, "output.txt")
    num_of_input = problem.numberOfInput
    ferr = open(errfile,'w')
    fout = open(outputfile, 'w')
    fout.close()
    error  = ""
    if language == 'C' or language == 'C++':
        command = ''
        if language == 'C':
            command = ['/usr/bin/gcc', '-lm', '-w', filename]
        else:
            command = ['/usr/bin/g++', '-lm', '-w', filename]
        subprocess.call(command, stderr=ferr)
        with open('/home/r3gz3n/CodeKnights/logs/error.log', 'r') as error_file:
            error = error_file.read()
        if not error:
            for i in range(1, num_of_input+1):
                command = ['/home/r3gz3n/CodeKnights/codechecker',
                       'a.out',
                       '--input=/home/r3gz3n/CodeKnights/problems/'+ problem_id +'/in' + str(i) + '.txt',
                       '--output=' + outputfile,
                       '--mem=' + str(64) + 'm',
                       '--time=' + str(2),
                       '--chroot=.']
                subprocess.call(command, stderr = ferr)
                correct_output = '/home/r3gz3n/CodeKnights/problems/' + problem_id + '/out' + str(i) + '.txt'
                with open(outputfile, 'r') as output, open(correct_output, 'r') as correctOutput:
                    for line1, line2 in zip(output, correctOutput):
                        if line1 != line2:
                            return 'WA Wrong Answer'
            command = ['rm', '/home/r3gz3n/CodeKnights/a.out']
            subprocess.call(command)
        else:
            return ('CE Compilation Error', 0, 0)
    elif language == 'Python':
        pass
    ferr.close()
    with open("/home/r3gz3n/CodeKnights/logs/error.log", 'r') as error_file:
        error = error_file.read()
    if error[0:2] == 'AC':
        x = error.split(' ')
        return ('AC Accepted', float(x[2]), int(x[3]))
    return (error, 0, 0)


def handle_uploaded_file(uploaded_file, language, submission_time):
    filename = "/home/r3gz3n/CodeKnights/allSubmissions/" + submission_time
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
        submission_time = datetime.datetime.now()
        submission_time_string = submission_time.strftime("%Y_%m_%d_%H_%M_%S")
        handle_uploaded_file(request.FILES['solution'], request.POST['language'], submission_time_string)
        if submissionsForm.is_valid():
            submission = submissionsForm.save(commit = False)
            submission.teamName = team_name
            submission.submissionTime = submission_time_string
            (submission.verdict, submission.timeTaken, submission.memoryTaken) = compileRun(submission.submissionTime, request.POST['language'], request.POST['problemId'])
            try:
                rank = Ranklist.objects.get(teamName = team_name)
            except Ranklist.DoesNotExist:
                rank = Ranklist(teamName = team_name)

            if submission.verdict[0] == 'A':
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
            elif (submission.verdict[0] == 'C'):
                pass
            else:
                if problem[request.POST['problemId']] == 1 and rank.problem1score == False:
                    rank.problem1WA += 1
                elif problem[request.POST['problemId']] == 2 and rank.problem2score == False:
                    rank.problem2WA += 1
                elif problem[request.POST['problemId']] == 3 and rank.problem3score == False:
                    rank.problem3WA += 1
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


def getKey1(item):
    return item.score

def getKey2(item):
    return item.totalTime


def ranklistPage(request):
    ranklist = Ranklist.objects.all()
    ranklist = sorted(ranklist, key=getKey2)
    ranklist = sorted(ranklist, key=getKey1, reverse = True)
    t = loader.get_template("ranklistPage.html")
    c = Context({"ranklist" : ranklist})
    return HttpResponse(t.render(c))

