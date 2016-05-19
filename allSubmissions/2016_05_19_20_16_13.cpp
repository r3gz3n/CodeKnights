#include <iostream>
#include <cstdlib>

using namespace std;

int main()
{
    int i = 0;
    int *a = (int *)malloc(sizeof(int)*100000000000);
    while(i < 100000000)i++;
    cout << "Hello World!!!" << endl;
    return 0;
}
