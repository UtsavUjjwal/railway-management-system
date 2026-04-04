// OOPS START 

#include<iostream>
using namespace std ; 

class student {
    public:
string name ; 
int rollnumber ;
float Cgpa



//constructor
student(string s , int k ){
    name = s ;
    Cgpa = k ; 
}

};

class cricketer {
    
}
void print(student s ){
    cout<<s.name<< " " << s.rollnumber<< " " <<s.Cgpa<< endl;
}

int main (){ 
    student utsav;
    utsav.name = "BHADRU";
    utsav.rollnumber = 45;
    utsav.Cgpa = 8;

    student bitto ;


  //  print( utsav );

  
  
  







    return 0;
}