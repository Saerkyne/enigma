#include "plugboard.h"

struct plugboard pb;

void configure(struct plugboard* pb, char pairs[10][2]) {
    pb->pair_one.first = pairs[0][0];
    pb->pair_one.second = pairs[0][1];
    pb->pair_two.first = pairs[1][0];
    pb->pair_two.second = pairs[1][1];
    pb->pair_three.first = pairs[2][0];
    pb->pair_three.second = pairs[2][1];
    pb->pair_four.first = pairs[3][0];
    pb->pair_four.second = pairs[3][1];
    pb->pair_five.first = pairs[4][0];
    pb->pair_five.second = pairs[4][1];
    pb->pair_six.first = pairs[5][0];
    pb->pair_six.second = pairs[5][1];
    pb->pair_seven.first = pairs[6][0];
    pb->pair_seven.second = pairs[6][1];
    pb->pair_eight.first = pairs[7][0];
    pb->pair_eight.second = pairs[7][1];
    pb->pair_nine.first = pairs[8][0];
    pb->pair_nine.second = pairs[8][1];
    pb->pair_ten.first = pairs[9][0];
    pb->pair_ten.second = pairs[9][1];
}

char encode(struct plugboard* pb, char c) {
    if (c == pb->pair_one.first) return pb->pair_one.second;
    if (c == pb->pair_one.second) return pb->pair_one.first;
    if (c == pb->pair_two.first) return pb->pair_two.second;
    if (c == pb->pair_two.second) return pb->pair_two.first;
    if (c == pb->pair_three.first) return pb->pair_three.second;
    if (c == pb->pair_three.second) return pb->pair_three.first;
    if (c == pb->pair_four.first) return pb->pair_four.second;
    if (c == pb->pair_four.second) return pb->pair_four.first;
    if (c == pb->pair_five.first) return pb->pair_five.second;
    if (c == pb->pair_five.second) return pb->pair_five.first;
    if (c == pb->pair_six.first) return pb->pair_six.second;
    if (c == pb->pair_six.second) return pb->pair_six.first;
    if (c == pb->pair_seven.first) return pb->pair_seven.second;
    if (c == pb->pair_seven.second) return pb->pair_seven.first;
    if (c == pb->pair_eight.first) return pb->pair_eight.second;
    if (c == pb->pair_eight.second) return pb->pair_eight.first;
    if (c == pb->pair_nine.first) return pb->pair_nine.second;
    if (c == pb->pair_nine.second) return pb->pair_nine.first;
    if (c == pb->pair_ten.first) return pb->pair_ten.second;
    if (c == pb->pair_ten.second) return pb->pair_ten.first;
    return c;
}