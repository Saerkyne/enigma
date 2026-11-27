#include "reflector.h"

void build_reflector(struct reflector* r, enum REFLECTOR_OPTIONS option) {
    const char* wiring = nullptr;
    switch (option) {
        case REFLECTOR_A:
            wiring = "EJMZALYXVBWFCRQUONTSPIKHGD";
            break;
        case REFLECTOR_B:
            wiring = "YRUHQSLDPXNGOKMIEBFZCWVJAT";
            break;
        case REFLECTOR_C:
            wiring = "FVPJIAOYEDRZXWGCTKUQSBNMHL";
            break;
    }
    for (int i = 0; i < 26; i++) {
        r->wiring[i] = wiring[i];
    }
}

char pass_through_reflector(struct reflector* r, char c) {
    return r->wiring[c - 'A'];
}