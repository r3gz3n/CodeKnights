#include <iostream>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <string>
#include <exception>

using namespace std;

int main(int args, char *argv[])
{
    if(args != 4)
    {
        cout << "Wrong Number of arguments!!!" << endl;
        return 1;
    }
    string filename = argv[1], problemName = argv[3];
    string problemPath = "/home/r3gz3n/CodeKnights/problems/" + problemName;
    string numinput = "ls " + problemPath + "/in*.txt | wc -l";
    string cmpout, input, output = problemPath + "/out.txt";
    char buf[130];
    FILE *numFile = popen(numinput.c_str(), "r");
    int numIn = 0, ret;
    fgets(buf, 128, numFile);
    fclose(numFile);
    for(int i = 0, l = strlen(buf)-1;i < l; ++i)
        numIn = (numIn * 10) + buf[i]-'0';
    if(strcmp("C", argv[2]) == 0)
    {
        string submission = "/home/r3gz3n/CodeKnights/allSubmissions/" + filename + ".c";
        string compile_command = "gcc " + submission + " -lm";
        string run_command = "./a.out";
        ret = system(compile_command.c_str());
        if(ret)
            return 2;
        for(int in = 1;in <= numIn;++in)
        {
            input = problemPath + "/in" + to_string(in) + ".txt";
            run_command += " < " + input + " > " + output;
            ret = system(run_command.c_str());
            if(ret)
                return 3;
            cmpout = "diff -Zsq " + output + " " + problemPath + "/out" + to_string(in) + ".txt";
            ret = system(cmpout.c_str());
            if(ret)
                return 4;
        }
        system("rm a.out");
    }
    else if(strcmp("C++", argv[2]) == 0)
    {
        string submission = "/home/r3gz3n/CodeKnights/allSubmissions/" + filename + ".cpp";
        string compile_command = "g++ -std=c++11 " + submission + " -lm";
        string run_command = "./a.out";
        ret = system(compile_command.c_str());
        if(ret)
            return 2;
        for(int in = 1;in <= numIn;++in)
        {
            input = problemPath + "/in" + to_string(in) + ".txt";
            run_command += " < " + input + " > " + output;
            ret = system(run_command.c_str());
            if(ret)
                return 3;
            cmpout = "diff -Zsq " + output + " " + problemPath + "/out" + to_string(in) + ".txt";
            ret = system(cmpout.c_str());
            if(ret)
                return 4;
        }
        system("rm a.out");
    }
    else if(strcmp("Python", argv[2]) == 0)
    {
        string submission = "/home/r3gz3n/CodeKnights/allSubmissions/" + filename + ".py";
        string run_command = "python " + submission;
        for(int in = 1;in <= numIn;++in)
        {
            input = problemPath + "/in" + to_string(in) + ".txt";
            run_command += " < " + input + " > " + output;
            ret = system(run_command.c_str());
            if(ret)
                return 3;
            cmpout = "diff -Zsq " + output + " " + problemPath + "/out" + to_string(in) + ".txt";
            ret = system(cmpout.c_str());
            if(ret)
                return 4;
        }
    }
    string cleanup = "rm " + output;
    system(cleanup.c_str());
    return 0;
}
