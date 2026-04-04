#include <stdio.h>

int main() {
    float p, r, t, simpleInt;

    
    printf("Enter Principal amount: ");
    scanf("%f", &p);

    printf("Enter Annual Interest Rate (in percentage): ");
    scanf("%f", &r);

    printf("Enter Time (in years): ");
    scanf("%f", &t);

    
    simpleInt = (p * r * t) / 100;

    
    printf("Simple Interest: %.2lf\n", simpleInt);

    return 0;
}
