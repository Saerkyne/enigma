#pragma once

struct rotor {
    char rotor_identifier;
    char notch;
    char notch2;
    char window_letter;
    char ring_setting;
    char wiring_forward[26];
    char wiring_backward[26];
};

enum ROTOR_OPTIONS {
    ROTOR_I,
    ROTOR_II,
    ROTOR_III,
    ROTOR_IV,
    ROTOR_V,
    ROTOR_VI,
    ROTOR_VII,
    ROTOR_VIII
};

void set_backward_wiring(struct rotor* r);
bool is_at_notch(struct rotor* r);
void step_rotor(struct rotor* r);
char pass_through_rotor(struct rotor* r, char c, bool forward);
void step_all_rotors(struct rotor* left, struct rotor* middle, struct rotor* right);
void build_rotor(struct rotor* r, enum ROTOR_OPTIONS option, char window_letter, char ring_setting);