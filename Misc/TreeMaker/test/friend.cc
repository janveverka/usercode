#include <iostream>


using namespace std;

class A {

  struct B {
    int m;
    // ctor
    B() : m(42) {}
    void set(int *n) {*n=m;}
  };

  int n;
  B b;

public:
  // ctor
  A() : n(0), b() {}

  void print() {
    cout << "n = " << n << endl;
    cout << "b.m = " << b.m << endl;
  }

  void set_to_b() {b.set(&n);}
};

int main() {
  A a;

  a.print();
  a.set_to_b();
  a.print();

  return 0;
}