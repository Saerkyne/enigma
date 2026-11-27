#pragma once

struct reflector {
    char wiring[26];
};

enum REFLECTOR_OPTIONS {
    REFLECTOR_A,
    REFLECTOR_B,
    REFLECTOR_C
};

void build_reflector(struct reflector* r, enum REFLECTOR_OPTIONS option);
char pass_through_reflector(struct reflector* r, char c);