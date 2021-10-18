import argparse
from functools import reduce
import re

class polynomial():
    """
    Stores string form as well as coefficients of a polynomial. Key of coef dict is degree, value of coef dict is factor. If we parse a higher degree, we add it to the coef dict
    e.g. 3x^2 + 5x + 4 
        -> {
            0:4,
            1:5,
            2:3
            }
    """
    def __init__(self):
        self.str = ""
        self.coefs = {
            0:0,
            1:0,
            2:0
        }

class parser():
    """
    Parse class that verifies validity of equation given in command line
    """
    def __init__(self):
        self.args = self._parse_arguments()
        self.left_poly = polynomial()
        self.right_poly = polynomial()

    def _parse_arguments(self):
        """
        Parse arguments from command line and stores equation/verbose arguments
        """
        try:
            parser = argparse.ArgumentParser(prog='computor', usage='python3 %(prog)s.py [-h] equation', description='Equation solver')
            parser.add_argument('-v', '--verbose', help='increase output verbosity', action='store_true')
            parser.add_argument('equation', help='equation in the form "a * x^2 + b * x^1 + c * x^0 = d * x^2 + e * x^1 + f * x^0"', type=str)
            args = parser.parse_args()
            return args
        except NameError as e:
            print(e)

    def _verify_equation(self, equation):
        """
        Check equation string : only accepted characters + make sure it is an equation (one = sign)
        """
        accepted_char = "0123456789xX*^=+-. "
        if equation.count('=') != 1:
            raise NameError("[parser._verify_equation] Incorrect number of '=' symbol detected. You either have more than one equation or no equation at all!")
        for char in self.args.equation:
            if char not in accepted_char:
                raise NameError("[parser._verify_equation] Invalid character {} at position {}".format(char, str(self.args.equation.index(char) + 1)))

    def _split_equation(self, equation):
        """
        Parse left/right polynomial
        """
        equation = equation.split('=')
        self.left_poly.str = equation[0].lower()
        self.right_poly.str = equation[1].lower()

    def _update_polynomial(self, state, group, match):
        """
        After analysing each group of regex match, update the corresponding polynomial with the new coefficients/degrees
        """
        if group['sign'] != None and match.span()[0] == match.span()[1] and group['coef'] == None:
            raise NameError("There is a trailing sign at the end of {} equation.".format(state['side']))
        elif group['sign'] == None:
            group['sign'] = 1
        if group['degree'] == None:
            group['degree'] = 0
        if group['coef'] == None:
            group['coef'] = 1 * group['sign']
        else:
            group['coef'] = group['coef'] * group['sign']
        if state['side'] == 'left':
            poly = self.left_poly
        else:
            poly = self.right_poly
        if group['degree'] in poly.coefs.keys():
            poly.coefs[group['degree']] += group['coef']
        else:
            poly.coefs[group['degree']] = group['coef']
        group = {
            'degree': None,
            'coef': None,
            'sign': 1
        }
        state['multiplication_accepted'] = False
        return group, state

    def _get_coefficient_value(self, state, group, regex_match):
        """
        Verify if position for having a coefficient is valid from state and get its value
        """
        if state['new_factor'] == True:
            state['new_factor'] = False
            state['multiplication_accepted'] = True
            group['coef'] = float(regex_match[2])
            return group, state
        else:
            raise NameError("There is a sign missing before {} on {} equation.".format(regex_match[0], state['side']))

    def _get_operation(self, state, group, match):
        """
        Verify if position for having a sign +- is valid from state and get its value
        """
        if state['new_factor'] == True and state['first_coef'] == False:
            raise NameError("Two operation signs detected one after the other at pos {} on the {} side of equation.".format(state['pos'], state['side']))
        else:
            # If new operation, save previous group and update polynomial coef dict
            if state['first_coef'] == False:
                group, state = self._update_polynomial(state, group, match)
            # Setting up new group
            if match[7] == '-':
                group['sign'] = -1
            else:
                group['sign'] = 1
            if state['sign_needed'] == True:
                state['sign_needed'] = False
            state['new_factor'] = True
        return group, state

    def _get_degree(self, state, group, match):
        if state['sign_needed'] == True:
            raise NameError("There is a sign missing before {} on {} equation.".format(match[0], state['side']))
        if match[5] == None:
            group['degree'] = 1
        else:
            group['degree'] = int(match[5])
        if group['coef'] == None:
            group['coef'] = 1
        if state['new_factor'] == True:
            state['new_factor'] = False
        if state['sign_needed'] == False:
            state['sign_needed'] = True
        state['multiplication_accepted'] = False
        return group, state

    def _parse_coefficients(self, poly, side):
        """
        parse coefficients of polynomial from string
        regex matches group:
        1. Multiplication sign
        2. Digits (ints and floats)
        3. x^a (a can be negative)
        4. not important
        5. power value of x
        6. space
        7. sign or operation + -
        """
        matches = re.finditer(r"(\*)|(\d*\.?\d+)|([Xx]{1}(\^(-?\d+))?)|(\ )+|([+-])?", poly.str)
        state = {
            'first_coef': True,
            'new_factor': True,
            'multiplication_accepted': False,
            'pos': 0,
            'side': side,
            'sign_needed': False
        }
        group = {
            'degree': None,
            'coef': None,
            'sign': None
        }
        for match in matches:
            if state['pos'] != match.span()[0]:
                raise NameError("Unexpected character at position {} on the {} side of the equation.".format(state['pos'], side))
            if match[2] != None:
                group, state = self._get_coefficient_value(state, group, match)
            elif match[7] != None:
                group, state = self._get_operation(state, group, match)
            elif match[3] != None:
                group, state = self._get_degree(state, group, match)
            elif match[1] != None:
                if state['multiplication_accepted'] == False:
                    raise NameError("Misplaced multiplication sign at pos {} of {} side of equation.".format(state['pos'], side))
                else:
                    state['multiplication_accepted'] = False
            if state['first_coef'] == True and (match[2] != None or match[3] != None):
                state['first_coef'] = False
            state['pos'] += len(match[0])
        # Getting factors and degree for last match
        if state['first_coef'] == False:
            group, state = self._update_polynomial(state, group, match)

    def _create_reduced_form(self):
        """
        Once both left and right equations have been parsed and verified, we compute the reduced form
        """
        reduced = {}
        left = self.left_poly.coefs
        right = self.right_poly.coefs
        for degree, coef in list(left.items()):
            if degree in right.keys():
                reduced[degree] = left[degree] - right[degree]
                del left[degree], right[degree]
            else:
                reduced[degree] = left[degree]
                del left[degree]
        for degree, coef in right.items():
            reduced[degree] = -right[degree]
        for degree, coef in list(reduced.items()):
            if coef == 0:
                del reduced[degree]
        return reduced

    def _print_reduced_form(self):
        """
        Organisation to print as shown on subject
        """
        reduced_str = "Reduced form: "
        first = True
        for degree, coef in self.reduced_form.items():
            if coef < 0:
                reduced_str = reduced_str + "- "
                coef = -coef
            else:
                if first == False:
                    reduced_str = reduced_str + "+ "
            if coef.is_integer() == True:
                coef = int(coef)
            reduced_str = reduced_str + str(coef)
            reduced_str = reduced_str + " * X^"
            reduced_str = reduced_str + str(degree) + " "
            if first == True:
                first = False
        reduced_str = reduced_str + "= 0\n"
        reduced_str = reduced_str + "Polynomial degree: {}".format(max(self.reduced_form))
        return reduced_str

    def parse(self):
        """
        Parsing method called from main
        """
        try:
            self._verify_equation(self.args.equation)
            self._split_equation(self.args.equation)
            self._parse_coefficients(self.left_poly, 'left')
            self._parse_coefficients(self.right_poly, 'right')
            self.reduced_form = self._create_reduced_form()
            reduced_str = self._print_reduced_form()
            print(reduced_str)
        except Exception as e:
            print("Error: {}".format(e))