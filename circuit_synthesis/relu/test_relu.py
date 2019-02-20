#/usr/bin/python3

import os
import subprocess
import random


def int_to_hex(x, HEX_LEN):
    x_hex = hex(x)[2:]
    if (len(x_hex) > HEX_LEN):
        print(x, ' too large to hexify')
    else:
        x_hex = '0' * (HEX_LEN - len(x_hex)) + x_hex
        return x_hex


class FixedPoint:
    def __init__(self, value=0):
        self.WIDTH = 32
        assert (self.WIDTH % 4 == 0)  # To enable HEX_LEN
        self.DEC_WIDTH = 10
        self.HEX_LEN = int(self.WIDTH / 4)
        self.value = value

        self.bignum = int(value * 2**self.DEC_WIDTH) + int(2**self.WIDTH / 2)

    def as_hex(self):
        return int_to_hex(self.bignum, self.HEX_LEN)

    def as_bin(self):
        return bin(self.bignum)

    def as_int(self):
        return self.bignum

    def as_float(self):
        return (self.bignum - 2**(self.WIDTH - 1)) / (2**self.DEC_WIDTH)

    def int_to_float(self, bignum):
        return (bignum - 2**(self.WIDTH - 1)) / (2**self.DEC_WIDTH)


def relu(x):
    return max(0, x)


def test_relu():

    clock_cycles = 1
    N = 8  # bit-width of inputs
    HEX_LEN = int(N / 4)  # HEX width of input
    MAX_N_HALVES = 2**(N - 1)
    relu_scd = './relu.scd'
    scd_eval = '../../build/scd/SCD_Evaluator_Main'

    random.seed(1)

    vals = [
        -10, -5, -2, -1.5, -0.5, -0.25, 0, 0.25, 0.5, 0.5, 0.75, 1.5, 2, 5, 11
    ]

    for x_val in vals:
        for r1_val in vals:
            for r2_val in vals:

                r2 = int(random.random() * MAX_N_HALVES)

                #x_val = 8.5
                #r1_val = -0.25
                #r2_val = -0.75
                e_in_val = x_val - r1_val

                x = FixedPoint(x_val)

                print('x_int', x.as_int())
                print('x_float', x.as_float())
                r1 = FixedPoint(r1_val)
                print('r1_int', r1.as_int())
                print('r1_float', r1.as_float())
                r2 = FixedPoint(r2_val)

                e_in = FixedPoint(e_in_val)
                e_hex_in = e_in.as_hex()
                print('e1_int', e_in.as_int())
                print('e1_float', e_in.as_float())

                r1_hex = r1.as_hex()
                r2_hex = r2.as_hex()

                g_hex_in = r1_hex + r2_hex

                print('g_hex_in', g_hex_in)

                cmd = ' '.join(
                    map(str, [
                        scd_eval, '--scd_file', relu_scd, \
                            '--clock_cycles', clock_cycles, \
                            '--g_input', g_hex_in,
                            '--e_input', e_hex_in
                    ]))

                print("Calling", cmd)

                result = subprocess.run([cmd],
                                        shell=True,
                                        stdout=subprocess.PIPE)
                output = result.stdout.decode('utf-8')
                print('result 0x' + output.strip())
                output = int('0x' + output, 16)

                # exp_output = (x) % 2**N
                #exp_output = x.as_int() % 2**N
                #if exp_output < 2**(N - 1):  # x negative
                #    exp_output = 2**(N - 1)  # x := 0
                #exp_output -= r2_val  # Masking with r2

                exp_output = FixedPoint(relu(x_val) + r2_val)
                output_float = FixedPoint().int_to_float(output)

                print('inputs:')
                print('r1 (int)', r1.as_int(), '(float)', r1.as_float())
                print('r2 (int)', r2.as_int(), '(float)', r2.as_float())
                print('x (int)', x.as_int(), '(float)', x.as_float())
                print('expect: (int)', exp_output.as_int(), '(float)',
                      exp_output.as_float())
                print('output: (int)', output, '(float)', output_float, '\n')

                assert (exp_output.as_int() == output)


def main():
    test_relu()


main()
