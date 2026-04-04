#include <iostream>

using namespace std;

class Example {
private:
    int x, y;
    int* arr;
    int n;

public:
    Example() : x(0), y(0), arr(nullptr), n(0) {
        cout << "Default constructor called" << endl;
    }

    Example(int a, int b) : x(a), y(b), arr(nullptr), n(0) {
        cout << "Parameterized constructor called" << endl;
    }

    Example(int* pointer, int size) : x(0), y(0), n(size) {
        arr = new int[n];
        for (int i = 0; i < n; ++i) {
            arr[i] = pointer[i];
        }
        cout << "Pointer constructor called" << endl;
    }

    Example(const Example& obj) : x(obj.x), y(obj.y), n(obj.n) {
        if (obj.arr && obj.n > 0) {
            arr = new int[n];
            for (int i = 0; i < n; ++i) {
                arr[i] = obj.arr[i];
            }
        } else {
            arr = nullptr;
        }
        cout << "Copy constructor called" << endl;
    }

    ~Example() {
        if (arr) {
            delete[] arr;
            arr = nullptr;
        }
        cout << "Destructor called" << endl;
    }

    void display() {
        cout << "X = " << x << ", y = " << y << endl;
        if (arr) {
            cout << "Array contents: ";
            for (int i = 0; i < n; ++i) {
                cout << arr[i] << " ";
            }
            cout << endl;
        }
    }
};

int main() {
    Example obj1;
    Example obj2(10, 20);

    int arr[] = {1, 2, 3, 4, 5};
    Example obj3(arr, 5);

    Example obj4(obj3);
    Example obj5 = obj4;

    obj1.display();
    obj2.display();
    obj3.display();
    obj4.display();
    obj5.display();

    return 0;
}