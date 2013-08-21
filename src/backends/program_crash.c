//program_crash.c  
//Cause a segmentation fault
//by dereferencing a pointer
//with a value of 0 
int main()
{
    char *s;
    char c;

    s = (char *) 0;
    c = *s;
}
