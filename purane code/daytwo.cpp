#include<iostream>
using namespace std;

int main(){
    int a;
    
    cout<<"enter marks of student "<<endl;
    cin>>a;

    if (a>=90&& (a<=100)){
        cout<<"excellent"<<endl;
    }
    else if ((a<90) && (a>=40)){
        
        cout<<"get better"<<endl;
    }
    else if (a<40){
        cout<<"failed"<<endl;
    }
    else if (a>100){
        cout<<"TUMSE NA HO PAYGA"<<endl;
    }

    
    







    return 0;
}