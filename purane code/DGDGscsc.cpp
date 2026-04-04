#include <iostream>
using namespace std;
class MyClass {
public:
    static int count;  
    MyClass() {
        count++;  
    }
    static void displayCount() {
        cout << "Object count: " << count << endl;
    }
};
int MyClass::count = 0;
int main() {
    MyClass obj1;
    MyClass obj2;
    MyClass obj3;
    MyClass::displayCount();
   return 0;
}