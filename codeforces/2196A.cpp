#include <iostream>
using namespace std;

int main() {
    int t;
    cin >> t;
        while (t--) {
        long long p, q;
        cin >> p >> q;
            
        if (p < q && 3 * p >= 2 * q) {
            cout << "Bob" << endl;
        } else {
            cout << "Alice" << endl;
        }
    }

    return 0;
}