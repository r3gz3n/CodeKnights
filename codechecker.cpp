#include <iostream>
#include <cstdio>
#include <cstdlib>
#include <cmath>
#include <cassert>
#include <cstring>
#include <getopt.h>
#include <unistd.h>
#include <sys/resource.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <linux/limits.h>

using namespace std;


// options for execution

char *infile = NULL;
char *outfile = NULL;
char *chrootdir = NULL;
bool debug = false;


// execution limits

int limit_stack = 0;    // limit on stack, in bytes
int limit_mem = 0;      // limit on mem, in bytes
int limit_fsize = 0;    // limit on output, in bytes
float limit_time = 0;   // limit on execution time, in seconds
int limit_file = 0;     // limit on number of files that can be opened
int limit_timehard = 0; // hard limit on time
int limit_nproc = 0;    // limit on the number of processes


void init()
{
    limit_stack = 8 * 1024 * 1024;
    limit_mem   = 64 * 1024 * 1024;
    limit_fsize = 50 * 1024 * 1024;
    limit_time  = 2;
    limit_file  = 16;
    limit_nproc = 1;
}


int unFormatedValue(char *s)
{
    char c = '-';
    int val;
    sscanf(s, "%d%c", &val, &c);
    if (c == '-') return val;
    c = tolower(c);
    if (c == 'k') return val * 1024;
    else if (c == 'm') return val * 1024 * 1024;
    else return val;
}


void printUsage()
{
    printf (
        "usage: runner [options] progname progarg1 progarg2 ... \n\
        \n\
        options:\n\
        --input=<file>        redirect program input from file\n\
        --output=<file>       redirect program output to file\n\
        --mem=<size>          set the runtime memory limit to <size>\n\
        --stack=<size>        set the runtime stack limit to <size>\n\
        --time=<seconds>      set the run time limit in seconds (float)    \n\
        --fsize=<size>        set the limit on amount of data outputted\n\
        --chroot=<dir>        chroot to the directory before executing     \n\
        --debug               increase verbosity, do not redirect stderr.\n\
        --help                display this help page\n\
        \n\
        <size> is in human readable format (12M, 12k etc., case insensitive.) \n\
        If no suffix is provided, it is understood to be bytes. 1k is 1024    \n\
        bytes and 1M is 1024k.\n\
        \n\
        This program is a part of the CodeKnights Online Judge.\n\
        \n\
    ");
}


int parseArgs(int argc, char *argv[])
{
    while(1)
    {
        struct option lopts[] = {
            {"input", 1, NULL, 0},
            {"output", 1, NULL, 0},
            {"stack", 1, NULL, 0},
            {"mem", 1, NULL, 0},
            {"fsize", 1, NULL, 0},
            {"time", 1, NULL, 0},
            {"open-files", 1, NULL, 0},
            {"proc", 1, NULL, 0},
            {"timehard", 1, NULL, 0},
            {"chroot", 1, NULL, 0},
            {"debug", 0, NULL, 0},
            {"help", 0, NULL, 0},
            NULL
        };
        int index;
        int c = getopt_long(argc, argv, "", lopts, &index);
        if(c == -1) break;

        if(c != 0)
        {
            // Parsing failed
            printUsage();
            exit(1);
        }

        if(strcmp(lopts[index].name, "input") == 0)
            infile = strdup(optarg);
        else if(strcmp(lopts[index].name, "output") == 0)
            outfile = strdup(optarg);
        else if(strcmp(lopts[index].name, "open-files") == 0)
            limit_file = atoi(optarg);
        else if(strcmp(lopts[index].name, "proc") == 0)
            limit_nproc = atoi(optarg);
        else if(strcmp(lopts[index].name, "chroot") == 0)
            chrootdir = strdup(optarg);
        else if(strcmp(lopts[index].name, "debug") == 0)
            debug = 1;
        else if(strcmp(lopts[index].name, "time") == 0)
            limit_time = atof(optarg);
        else if(strcmp(lopts[index].name, "stack") == 0)
            limit_stack = unFormatedValue(optarg);
        else if(strcmp(lopts[index].name, "mem") == 0)
            limit_mem = unFormatedValue(optarg);
        else if(strcmp(lopts[index].name, "fsize") == 0)
            limit_fsize = unFormatedValue(optarg);
        else if(strcmp(lopts[index].name, "timehard") == 0)
            limit_timehard = atoi(optarg);
        else if(strcmp(lopts[index].name, "help") == 0)
        {
            printUsage();
            exit(0);
        }
        else assert(false);

    }

    if(optind == argc)
    {
        printUsage();
        exit(0);
    }
    return optind;
}


int subprocess(int argc, char *argv[])
{
    struct rlimit rlp;
    char **commands;
    int i;
    rlp.rlim_cur = (int) ceil(limit_time);
    rlp.rlim_max = limit_timehard;
    if(setrlimit(RLIMIT_CPU, &rlp) != 0)
        exit(1);

    rlp.rlim_cur = rlp.rlim_max = limit_mem;
    if(setrlimit(RLIMIT_DATA, &rlp) != 0)
        //exit(1);

    rlp.rlim_cur = rlp.rlim_max = limit_mem;
    if(setrlimit(RLIMIT_AS, &rlp) != 0)
        //exit(1);

    rlp.rlim_cur = rlp.rlim_max = limit_fsize;
    if(setrlimit(RLIMIT_FSIZE, &rlp) != 0)
        //exit(1);

    rlp.rlim_cur = rlp.rlim_max = limit_file;
    if(setrlimit(RLIMIT_NOFILE, &rlp) != 0)
        //exit(1);

    rlp.rlim_cur = limit_stack;
    rlp.rlim_max = limit_stack + 1024;
    if(setrlimit(RLIMIT_STACK, &rlp) != 0)
        //exit(1);

    if (infile and freopen(infile, "r", stdin) == NULL)
        return 23;

    if (outfile and freopen(outfile, "w", stdout) == NULL)
        return 24;

    if(!chrootdir)
        if(chroot(chrootdir) != 0)
            chrootdir = NULL;

    if (setresgid(65534, 65534, 65534) != 0 or setresuid(65534, 65534, 65534) != 0)
    {

    }

    if(debug)
        fprintf(stderr, "nproc limit: %d\n", limit_nproc);

    rlp.rlim_cur = rlp.rlim_max = limit_nproc;
    if(setrlimit(RLIMIT_NPROC, &rlp) != 0)
        if(geteuid() == 0 or getegid() == 0)
        {
            fprintf(stderr, "FATAL: We're running as root!");
            return 1;
        }

    if(!debug)
    {
        if(freopen("/dev/null", "w", stderr) == NULL)
            return 25;
    }


    commands = (char **) malloc(sizeof (char *)*(argc + 1));
    for(i = 0;i < argc;++i)
    {
        commands[i] = argv[i];
    }
    commands[argc] = NULL;
    execve(argv[0], commands, NULL);
    perror("Unable to execute program");
    exit(26);
}


int get_memory_usage(pid_t pid) {
    int fd, data, stack;
    char buf[4096], status_child[NAME_MAX];
    char *vm;

    sprintf(status_child, "/proc/%d/status", pid);
    if ((fd = open(status_child, O_RDONLY)) < 0)
        return 0;

    read(fd, buf, 4095);
    buf[4095] = '\0';
    close(fd);

    data = stack = 0;

    vm = strstr(buf, "VmData:");
    if (vm)
        sscanf(vm, "%*s %d", &data);

    vm = strstr(buf, "VmStk:");
    if (vm)
        sscanf(vm, "%*s %d", &stack);

    return (data + stack);
}


int main(int argc, char* argv[])
{
    int cmd_start_index = 0, i;
    pid_t pid, hardlimit_monitor;

    init();
    cmd_start_index = parseArgs(argc, argv);

    if(limit_timehard < 1 + ceil(limit_time))
        limit_timehard = 1 + ceil(limit_time);

    for(i = 3;i < (1 << 16);++i)
        close(i);

    pid = fork();
    if(pid == 0)
    {
        return subprocess(argc - cmd_start_index, argv + cmd_start_index);
    }
    hardlimit_monitor = fork();
    if(hardlimit_monitor == 0)
    {
        sleep(6*limit_timehard);
        kill(pid, 9);
        return 0;
    }

    int status;
    struct rusage usage;
    int memory_used = 0;


    pid_t pid2;

    do {
        memory_used = max(memory_used, get_memory_usage(pid));
        // wait for the child process to change state
        pid2 = wait4(pid, &status, WUNTRACED | WCONTINUED, &usage);
    } while (pid2 == 0);
    kill(hardlimit_monitor, 9);
    waitpid(hardlimit_monitor, NULL, 0);

    fflush(stderr);

    double usertime = (float) (usage.ru_utime.tv_sec) + ((float) usage.ru_utime.tv_usec) / 1000000;
    double systime = (float) (usage.ru_stime.tv_sec) + ((float) usage.ru_stime.tv_usec) / 1000000;

    if(WIFSIGNALED(status))
    {
        int signal = WTERMSIG(status);
        if(signal == SIGXCPU)
        {
            fprintf(stderr, "TLE Time Limit Exceeded (H)");
            exit(0);
        }
        if(signal == SIGFPE)
        {
            fprintf(stderr, "FPE Floating Point Exception");
            exit(0);
        }
        if(signal == SIGILL)
        {
            fprintf(stderr, "ILL Illegal Instruction");
            exit(0);
        }
        if(signal == SIGSEGV)
        {
            fprintf(stderr, "SEG Segmentation Fault");
            exit(0);
        }
        if(signal == SIGABRT)
        {
            fprintf(stderr, "ABRT Aborted");
            exit(0);
        }
        if(signal == SIGBUS)
        {
            fprintf(stderr, "BUS Bus Error (Bad Memory Access)");
            exit(0);
        }
        if(signal == SIGSYS)
        {
            fprintf(stderr, "SYS Invalid System Call");
            exit(0);
        }
        if(signal == SIGXFSZ)
        {
            fprintf(stderr, "XFSZ Output File Too Large");
            exit(0);
        }
        if(signal == SIGKILL)
        {
            fprintf(stderr, "KILL Your Program Was Killed (Probably Because Of Excessive Memory Usage)");
            exit(0);
        }

        fprintf(stderr, "UNK Unknown error, possibly your program does not return 0, or maybe its some fault of ours!");
        exit(0);
    }

    if(usertime + systime > limit_time)
    {
        fprintf(stderr, "TLE Time Limit Exceeded");
        exit(0);
    }

    if(!WIFEXITED(status))
    {
        fprintf(stderr, "EXIT Program Exited Abnormally. This Could Be Due To Excessive Memory Usage, Or Any Runtime Error That Is Impossible To Determine.");
        exit(0);
    }

    if(WEXITSTATUS(status) != 0)
    {
        fprintf(stderr, "EXIT Program Did Not Return %d", WEXITSTATUS(status));
        exit(0);
    }
    fprintf(stderr, "AC Accepted %lf %d", (usertime + systime), memory_used);
    return 0;
}
