#include <iostream>

using namespace std;

class Bank
{

    string name;
    int account_id;
    float balance = 120000.32;

public:
    void getinfo()
    {
        cout << "Enter your name" << endl;
        cin >> name;

        cout << "Enter you account ID" << endl;
        cin >> account_id;
    }

    string dost()
    {
      return name;
    }

    float dost1()
    {
        return balance;
    }

    void deposit()
    {
        int amount;
        cout << "Enter the deposit amount" << endl;
        cin >> amount;
        if (amount > 0)
        {
            balance += amount;
        }
        else
        {
            cout << "Invalid Input";
        }
    }

    void Withdraw()
    {

        int amount;
        cout << "Enter the amount you have to withdraw" << endl;
        cin >> amount;
        if (amount < balance)
        {
            balance -= amount;
            cout << "The left balance is " << balance<<endl;
        }
        else
        {
            cout << "Invalid Withdraw";
        }
    }

    void enquire()
    {
        int ID;
        cout << "Enter you account ID" << endl;
        cin >> ID;
        if (ID == account_id)
        {
            cout << "Customer Name is " << dost()<< endl;
            cout << "Curent Balance is " << dost1() << endl;
        }
        else
        {
            cout << "Invalide Login";
        };
    }
};

int main()
{

    Bank b1;
    b1.getinfo();
    b1.deposit();
    b1.Withdraw();
    b1.enquire();
    return 0;
}