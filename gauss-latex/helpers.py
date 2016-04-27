#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Jannes Höke (jhoeke@uni-bremen.de)
#
# This program is licensed under the MIT License:
# https://opensource.org/licenses/MIT


def bracket(fraction, produce_latex=False):
    """ Convert a fraction to string and put it in brackets if negative """

    if fraction < 0:
        if produce_latex:
            fraction_str = r'$ \left(%s\right) $' % fraction_tex(fraction)
        else:
            fraction_str = '(%s)' % str(fraction)
    else:
        if produce_latex:
            fraction_str = fraction_tex(fraction)
        else:
            fraction_str = str(fraction)
    return fraction_str


def print_matrix(matrix, explanations, produce_latex):
    """
    Print a matrix with explanations to standard output
    :param matrix: The matrix
    :param explanations: A dict of explanations
    :param produce_latex:
    """
    m = len(matrix)
    n = len(matrix[0])

    if produce_latex:
        widths = column_widths(matrix, fraction_tex)
    else:
        widths = column_widths(matrix)

    if produce_latex:
        # matrix header
        print(r"\begin{equation}\left(\begin{array}{%s|c}" % ((n - 1) * 'c'))

        # matrix body
        for line in matrix:
            pattern = ' & '.join('%{}s'.format(width) for width in widths)
            print(pattern % tuple(map(fraction_tex, line)) + r' \\ ')

        # matrix footer
        print(r'\end{array}\right)')

        # explanations
        print(r"\begin{array}{l}")

        for i in range(m):
            explanation = explanations.get(i, '')

            if explanation:
                explanation = r' \textsl{%s}' % explanation

            print(explanation + r" \\ ")

        print(r'\end{array}\end{equation}')

    else:
        for i in range(m):
            pattern = '  '.join('%{}s'.format(width) for width in widths[:-1])
            pattern += ' | %{}s'.format(widths[-1])

            explanation = explanations.get(i, '')
            if explanation:
                explanation = '  # ' + explanation

            print(pattern % tuple(matrix[i]) + explanation)


def fraction_tex(fraction):
    """ Get the LaTeX code for a Fraction instance """
    if fraction.denominator != 1:
        return r'\frac{%d}{%d}' % (fraction.numerator, fraction.denominator)
    else:
        return str(fraction.numerator)


def column_widths(matrix, str_fn=str):
    """
    Generate a list that contains the maximum length of strings in each column
    :param matrix: The matrix
    :param str_fn: The string conversion function (defaults to str)
    :return: list of ints
    """
    m = len(matrix[0])
    widths = [0] * m

    for line in matrix:
        for j in range(0, m):
            widths[j] = max(widths[j], len(str_fn(line[j])))

    return widths
