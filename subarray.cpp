#include <iostream>
using namespace std;

void subarray(int arr[], int n)
{
    // Pick starting point
    for (int i = 0; i < n; i++)
    {
        // Pick ending point
        for (int j = i; j < n; j++)
        {
            // Print subarray between current starting
            // and ending points
            for (int k = i; k <= j; k++)
                cout << arr[k] << " ";

            cout << endl;
        }
    }
}

int main()
{
    int arr[] = {1, 2, 3, -2, 5};
    int n = sizeof(arr) / sizeof(arr[0]);
    subarray(arr, n);
}
