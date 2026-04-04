#include<iostream>
using namespace std;

#include<cmath>

int main (){


    float a,b,c,d,e,f,g,h ;

    cout<<"ENTER A"<<endl;
    cin>>a;
    cout<<"ENTER B"<<endl;
    cin>>b;

    while(abs(b-a>0.001)){

        h=abs(a+b)/2;

        e=(a*a*a)-a-1;
        f=(b*b*b)-b-1;
        g=(h*h*h)-h-1;
        if(f==0){
            cout<<h<<" ";

        }
        else if (e*g==h){
            b=h;
            cout<<h<<" ";

        }
        else{
            a=h;
            cout<<h<<" ";
        }
        return 0;

    }




}