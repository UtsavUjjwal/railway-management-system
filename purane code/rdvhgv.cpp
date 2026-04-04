#include<iostream>
using namespace std;
int x=6;
class st{
    public:
    void sum();
};
void st ::sum(){
    int x=2;
    int y=3;
    cout<<x+y;
}
int main(){
    int x;
    x=10;
    cout<<::x<<endl;
    st r;
    r.sum();
    return 0;
}
