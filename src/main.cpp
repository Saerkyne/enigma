#include "rotor.h"
#include "reflector.h"
#include "plugboard.h"
#include <iostream>

int main() {
    struct rotor left;
    build_rotor(&left, ROTOR_I, 'A', 'A');
    struct rotor middle;
    build_rotor(&middle, ROTOR_II, 'A', 'A');
    struct rotor right;
    build_rotor(&right, ROTOR_III, 'A', 'A');
    struct reflector refl;
    build_reflector(&refl, REFLECTOR_B);
    struct plugboard pb;
    char pairs[10][2] = {{'A', 'B'}, {'C', 'D'}, {'E', 'F'}, {'G', 'H'}, {'I', 'J'}, {'K', 'L'}, {'M', 'N'}, {'O', 'P'}, {'Q', 'R'}, {'S', 'T'}};
    configure(&pb, pairs);

    char message[] = "HELLO";
    for (int i = 0; message[i] != '\0'; i++) {
        char c = message[i];
        step_all_rotors(&left, &middle, &right);
        c = encode(&pb, c);
        c = pass_through_rotor(&right, c, true);
        c = pass_through_rotor(&middle, c, true);
        c = pass_through_rotor(&left, c, true);
        c = pass_through_reflector(&refl, c);
        c = pass_through_rotor(&left, c, false);
        c = pass_through_rotor(&middle, c, false);
        c = pass_through_rotor(&right, c, false);
        c = encode(&pb, c);
        std::cout << c;
    }
    std::cout << std::endl;

    return 0;
}