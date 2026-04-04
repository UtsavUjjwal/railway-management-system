#include <iostream>
using namespace std;
 
int digit_sum(int n) {
    int res = 0;
    while (n > 0) {
        res += n%10;
        n /= 10;
    }
    return res;
}
 
int main() {
    int t;
    cin >> t;
    while (t--) {
        int x;
        cin >> x;
 
        int ans = 0;
        for (int dy=1; dy <= 81; dy++) {
            int y = x + dy;
            if (digit_sum(y) == dy)
                ans++;
        }
        cout << ans << "\n";
    }
    return 0;
}