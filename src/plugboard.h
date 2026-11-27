#pragma once

struct plugboard {
    struct pair {
        char first;
        char second;
    };
    pair pair_one;
    pair pair_two;
    pair pair_three;
    pair pair_four;
    pair pair_five;
    pair pair_six;
    pair pair_seven;
    pair pair_eight;
    pair pair_nine;
    pair pair_ten;
};

void configure(struct plugboard* pb, char pairs[10][2]);
char encode(struct plugboard* pb, char c);