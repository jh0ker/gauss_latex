#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Jannes Höke (jhoeke@uni-bremen.de)
#
# This program is licensed under the MIT License:
# https://opensource.org/licenses/MIT

from roman import write_roman


def bracket(fraction, produce_latex):
    """ Convert a fraction to string and put it in brackets if negative """

    if fraction < 0:
        if produce_latex:
            fraction_str = r'\left(%s\right)' % fraction_tex(fraction)
        else:
            fraction_str = '(%s)' % str(fraction)
    else:
        if produce_latex:
            fraction_str = fraction_tex(fraction)
        elif fraction.denominator != 1:
            fraction_str = '(%s)' % str(fraction)
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
        for row in matrix:
            pattern = ' & '.join('%{}s'.format(width) for width in widths)
            print(pattern % tuple(map(fraction_tex, row)) + r' \\ ')

        # matrix footer
        print(r'\end{array}\right)')

        # explanations
        print(r"\begin{array}{l}")

        for i in range(m):
            print(explanations.get(i, '') + r" \\ ")

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
        if fraction < 0:
            return r'-\frac{%d}{%d}' % \
                   (-1 * fraction.numerator, fraction.denominator)
        else:
            return r'\frac{%d}{%d}' % \
                   (fraction.numerator, fraction.denominator)

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

    for row in matrix:
        for j in range(0, m):
            widths[j] = max(widths[j], len(str_fn(row[j])))

    return widths


def exp_swap(source, dest, produce_latex):
    if produce_latex:
        source_roman = r'\textsc{%s}' % write_roman(source + 1)
        dest_roman = r'\textsc{%s}' % write_roman(dest + 1)
        operation = r' \leftrightarrows '
    else:
        source_roman = write_roman(source + 1)
        dest_roman = write_roman(dest + 1)
        operation = " <-> "
    return source_roman + operation + dest_roman


def exp_divide(divisor, produce_latex):
    divisor_str = bracket(divisor, produce_latex)
    if produce_latex:
        operation = r'\div '
    else:
        operation = "/"
    return operation + divisor_str


def exp_minus(factor, row, produce_latex):
    factor_str = bracket(factor, produce_latex)

    if produce_latex:
        pattern = r'- %s \cdot %s'
        row_roman = r'\textsc{%s}' % write_roman(row + 1)
    else:
        pattern = '- %s * %s'
        row_roman = write_roman(row + 1)

    return pattern % (factor_str, row_roman)
