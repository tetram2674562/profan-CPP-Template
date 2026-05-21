// Template from tetram26 <3
#include <stdio.h>
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


int main() {
    YIPPEE yippee;
    Yippee(23);
    return 0;
}
