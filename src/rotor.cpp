#include "rotor.h"
#include <string>

static std::string ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";

void set_backward_wiring(struct rotor* rotor) {
    for (int i = 0; i < 26; i++) {
        char forward_letter = rotor->wiring_forward[i];
        rotor->wiring_backward[forward_letter - 'A'] = 'A' + i;
    }
}

bool is_at_notch(struct rotor* rotor) {
    return rotor->window_letter == rotor->notch;
}

void step_rotor(struct rotor* rotor) {
    rotor->window_letter = (rotor->window_letter - 'A' + 1) % 26 + 'A';
}

void build_rotor(struct rotor* rotor, enum ROTOR_OPTIONS option, char window_letter, char ring_setting) {
    std::string wiring = "";
    switch (option) {
        case ROTOR_I:
            wiring = "EKMFLGDQVZNTOWYHXUSPAIBRCJ";
            rotor->notch = 'Q';
            rotor->notch2 = 0;
            rotor->ring_setting = ring_setting;
            rotor->window_letter = window_letter;
            break;
        case ROTOR_II:
            wiring = "AJDKSIRUXBLHWTMCQGZNPYFVOE";
            rotor->notch = 'E';
            rotor->notch2 = 0;
            rotor->ring_setting = ring_setting;
            rotor->window_letter = window_letter;
            break;
        case ROTOR_III:
            wiring = "BDFHJLCPRTXVZNYEIWGAKMUSQO";
            rotor->notch = 'V';
            rotor->notch2 = 0;
            rotor->ring_setting = ring_setting;
            rotor->window_letter = window_letter;
            break;
        case ROTOR_IV:
            wiring = "ESOVPZJAYQUIRHXLNFTGKDCMWB";
            rotor->notch = 'J';
            rotor->notch2 = 0;
            rotor->ring_setting = ring_setting;
            rotor->window_letter = window_letter;
            break;
        case ROTOR_V:
            wiring = "VZBRGITYUPSDNHLXAWMJQOFECK";
            rotor->notch = 'Z';
            rotor->notch2 = 0;
            rotor->ring_setting = ring_setting;
            rotor->window_letter = window_letter;
            break;
        case ROTOR_VI:
            wiring = "JPGVOUMFYQBENHZRDKASXLICTW";
            rotor->notch = 'Z';
            rotor->notch2 = 'M';
            rotor->ring_setting = ring_setting;
            rotor->window_letter = window_letter;
            break;
        case ROTOR_VII:
            wiring = "NZJHGRCXMYSWBOUFAIVLPEKQDT";
            rotor->notch = 'Z';
            rotor->notch2 = 'M';
            rotor->ring_setting = ring_setting;
            rotor->window_letter = window_letter;
            break;
        case ROTOR_VIII:
            wiring = "FKQHTLXOCBJSPDZRAMEWNIUYGV";
            rotor->notch = 'Z';
            rotor->notch2 = 'M';
            rotor->ring_setting = ring_setting;
            rotor->window_letter = window_letter;
            break;
    }

    for (int i = 0; i < 26; i++) {
        rotor->wiring_forward[i] = wiring[i];
    }
    set_backward_wiring(rotor);
    rotor->window_letter = window_letter;
    rotor->ring_setting = ring_setting;
}

void step_all_rotors(rotor* left, rotor* middle, rotor* right) {
    bool right_notched = is_at_notch(right);
    bool middle_notched = is_at_notch(middle);

    bool middle_should_step = false;
    bool left_should_step = false;

    if (right_notched) {
        middle_should_step = true;
    }
    if (middle_notched) {
        left_should_step = true;
        middle_should_step = true;
    }

    step_rotor(right);

    if (middle_should_step) {
        step_rotor(middle);
    }
    if (left_should_step) {
        step_rotor(left);
    }
}

char pass_through_rotor(struct rotor* r, char c, bool forward) {
    // Calculate the shifted index based on the rotor's window letter and ring setting
    char result;
    int input_index = ALPHABET.find(c);
    int window_letter_index = ALPHABET.find(r->window_letter);
    int ring_setting_index = ALPHABET.find(r->ring_setting);
    int shift_distance = window_letter_index - ring_setting_index;
    int shifted_char_index = (input_index + shift_distance + 26) % 26;
    if (forward) {
        result = r->wiring_forward[shifted_char_index];
    } else {
        result = r->wiring_backward[shifted_char_index];
    }
    // Reverse the initial shift to get the final character index
    result = ALPHABET[(ALPHABET.find(result) - shift_distance + 26) % 26];
    return result;
}