#include <stdio.h>
#include <math.h>

int main() {
    
    float p, r, t, amount, compoundInt;

    
    printf("Enter Principal amount: ");
    scanf("%f", &p);

    printf("Enter Annual Interest Rate (in percentage): ");
    scanf("%ff", &r);

    printf("Enter Time (in years): ");
    scanf("%f", &t);

    
    amount = p * pow((1 + r / 100), t);
    compoundInt = amount - p;

    
    printf("Final Amount: %.2f\n", amount);
    printf("Compound Interest: %.2lf\n", compoundInt);

    return 0;
}
