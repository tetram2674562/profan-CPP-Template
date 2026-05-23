// Template from tetram26 <3
#include <cstdio>
#include <typeinfo>

#include "iostream"
#include "Yippee2.h"
class YIPPEE {
public:
    YIPPEE() {
        printf("Hello YIPPEE! \n");
    }

    ~YIPPEE() {
        printf("Goodbye YIPPEE! \n");
    }
};

class SuperYippee : public YIPPEE {};

class WeakerYippee : public YIPPEE {};

int main() {
    SuperYippee* yippee = new SuperYippee();
    Yippee(23);
    if (typeid(*yippee) == typeid(SuperYippee)) {
        printf("SUPER YIPEEE !\n");
    }
    delete yippee;
    // cout isn't working for some reason ?
    std::cout << "uwu";
    return 0;
}
