#include<stdio.h>
#include<math.h>
#include<conio.h>

int main(){
    
    float a , b , c , d , r1 , r2;

    printf("ENTER THE VALUE OF A B and C : \n");
    scanf("%f %f %f", &a, &b, &c);
    
    d = b*b - 4 * a * c;
    
    if (d == 0)
    {
        printf("roots are real and eaqual\n");

        r1 = -b/(2*a);
        r2 = -b/(2*a);
        printf("ROOTS ARE %f %f",&r1 ,&r2);

    }
    else if (d>0)
    {
        printf("the roots are distinct\n");

        r1 = (-b+sqrt(d))/2*a;
        r2 = (-b-sqrt(d))/2*a;
        printf("the root 1 is  %f and root 2 is %f",r1 ,r2);


    }
    else 
    {
        printf("the rrots are  imaginary");
    }



    
    



   






    return 0;
}
