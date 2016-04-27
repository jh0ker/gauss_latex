#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Jannes Höke (jhoeke@uni-bremen.de)
#
# This program is licensed under the MIT License:
# https://opensource.org/licenses/MIT

import argparse
import sys
from fractions import Fraction

from helpers import print_matrix, bracket


def main():

    # Prevents argparse to break if an equation starts with a minus
    for i in range(len(sys.argv)):
        if ';' in sys.argv[i]:
            sys.argv[i] = ' ' + sys.argv[i]

    parser = argparse.ArgumentParser(
        description='Uses the Gauss-Jordan algorithm to solve a system of '
                    'linear equations.')

    parser.add_argument('line',
                        type=str,
                        nargs='+',
                        help='Add equations to the system in the form '
                             '"a1;a2;..;an;b" where ai are the coefficients '
                             'of one line of the matrix, and b the result. '
                             'Instead of a "..;0;.." you can also write '
                             '"..;;..". You can enter fractions by using the '
                             'x/y notation and decimals using the x.y '
                             'notation.')

    parser.add_argument('--skip-unchanged', '-s',
                        action='store_true',
                        help='Skip steps where the matrix does not change '
                             '(default=disabled)')

    parser.add_argument('--latex',
                        action='store_true',
                        help='Produce LaTeX code instead of text output '
                             '(default=disabled)')

    args = parser.parse_args()

    skip_unchanged = args.skip_unchanged
    produce_latex = args.latex

    # Create the matrix
    matrix = list()

    # Fill matrix with values
    fill_matrix(args, matrix)

    # Check matrix structure
    check_matrix(matrix)

    # Print out all intermediate results of the algorithm
    # Save the last result, because explanations are always one step ahead
    last = None

    # Set the string conversion function
    for step, explanations in gauss(matrix, produce_latex=produce_latex):

        if skip_unchanged and step == last:
            continue

        if (last is not None and step is not None or
                skip_unchanged and step is None):
            print_matrix(last, explanations, produce_latex)
            print('')

        if step:
            last = step


def gauss(a, i=0, j=0, produce_latex=False):
    """
    Perform the Gauss-Jordan-Algorithm and yield results in between
    :param a: The matrix
    :param i: Next vertical position
    :param j: Next horizontal position
    :param produce_latex: If True, explanation texts are formatted in LaTeX
    :yields: tuple (list, dict) where the first entry is the matrix as a two-
        dimensional list [m][n] and the second a dict {line nr: explanation}
    """

    if i == j == 0:
        yield (list(a), None)

    m = len(a)     # Determine the height of the matrix
    n = len(a[0])  # Determine the width of the matrix

    if i == m or j == n:
        yield (None, {})
        return

    if a[i][j] == 0:
        for r in range(i + 1, m):
            if a[r][j] != 0:
                a[r], a[i] = a[i], a[r]
                yield (list(a), {i: "Tausche mit Zeile %d" % (r + 1)})
                break
        else:
            for recursion in gauss(a, i, j + 1, produce_latex):
                yield recursion

    try:
        divisor = a[i][j]
        a[i] = [coeff / divisor for coeff in a[i]]

        divisor_str = bracket(divisor, produce_latex)
        yield (list(a), {i: "Teile durch %s" % divisor_str})

    except ZeroDivisionError:
        return

    explanations = dict()
    for k in range(i + 1, m):
        factor = a[k][j]
        a[k] = [coeff_k - factor * coeff_i
                for (coeff_k, coeff_i)
                in zip(a[k], a[i])]

        factor_str = bracket(factor, produce_latex)
        explanations[k] = "- %s * Zeile %d" % (factor_str, i + 1)

    yield (list(a), explanations)

    for recursion in gauss(a, i + 1, j + 1, produce_latex):
        yield recursion


def fill_matrix(args, matrix):
    """ Fill the matrix with values from console arguments """
    for line_str in args.line:
        line = list()

        for coeff in line_str.split(';'):
            line.append(Fraction(coeff or 0))

        matrix.append(line)


def check_matrix(matrix):
    """ Check if all lines of the matrix have the same length """
    len_first = len(matrix[0])
    if not all([len(line) == len_first for line in matrix]):
        raise ValueError("Not all lines have the same number of coefficients")


if __name__ == "__main__":
    main()
