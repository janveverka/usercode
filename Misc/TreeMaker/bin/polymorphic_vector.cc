#include <boost/shared_ptr.hpp>
#include <boost/ptr_container/ptr_vector.hpp>
#include <iostream>
#include <vector>
// #include <memory>

using namespace std;

class Parent
{
    public:
        Parent(int i) : parent_mem(i) {
          cout << "new Parent: " << i << " at " << this << endl;
        }

        ~Parent() {
          cout << "~Parent: " << parent_mem << " at " << this << endl;
        }

        virtual void write() { cout << "Parent: " << parent_mem << endl; }
        int parent_mem;
};

class Child : public Parent
{
    public:
        Child(int i) : Parent(i), child_mem(i) {
          cout << "new Child: " << i << " at " << this << endl;
        }

        ~Child() {
          cout << "~Child: " << child_mem << " at " << this << endl;
        }

        void write() {
          cout << "Child: " << parent_mem << ", " << child_mem << endl;
        }

        int child_mem;
};

int main(int, const char**)
{
    // I can have a polymorphic container with pointer semantics

    cout << endl << "== vector<Parent*> ==" << endl;

    vector<Parent*> pointerVec;

    pointerVec.push_back(new Parent(1));
    pointerVec.push_back(new Child(2));

    pointerVec[0]->write();
    pointerVec[1]->write();

    // Output:
    //
    // Parent: 1
    // Child: 2, 2

    cout << endl << "== vector<Parent> ==" << endl;
    // But I can't do it with value semantics

    vector<Parent> valueVec;

    valueVec.push_back(Parent(3));
    valueVec.push_back(Child(4));        // gets turned into a Parent object :(

    valueVec[0].write();
    valueVec[1].write();

    // Output:
    //
    // Parent: 1
    // Parent: 2

    cout << endl << "== vector<boost::shared_ptr<Parent> > ==" << endl;

    vector<boost::shared_ptr<Parent> > smartPtrVec;
    smartPtrVec.push_back(boost::shared_ptr<Parent>(new Parent(5)));
    smartPtrVec.push_back(boost::shared_ptr<Parent>(new Child(6)));

    smartPtrVec[0]->write();
    smartPtrVec[1]->write();

    cout << endl << "== boost::ptr_vector<Parent> ==" << endl;

    boost::ptr_vector<Parent> boostPtrVec;
    boostPtrVec.push_back( new Parent(7) );
    boostPtrVec.push_back( new Child(8) );

    boostPtrVec[0].write();
    boostPtrVec[1].write();

    cout << endl << "== Exitting ... ==" << endl;
    // vector<Parent*> leaked memory!
}
