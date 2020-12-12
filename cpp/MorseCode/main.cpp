#include <iostream>

#include "code.h"

void test_morse() {
    MorseCode code;
    auto c = code.encode("abc def");
    std::cout << "[" << c << "]" << std::endl;
    std::cout << "[" << code.decode(c) << "]" << std::endl;
}

void test_braille() {
    BrailleCode code;
    auto c = code.encode("abc def");
    std::cout << "[" << c << "]" << std::endl;
    std::cout << "[" << code.decode(c) << "]" << std::endl;
}

int main() {
    test_morse();
    test_braille();
    return 0;
}
