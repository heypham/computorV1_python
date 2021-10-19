import matplotlib.pyplot as plt
import numpy as np

class solver():
    def __init__(self, polynomial, args):
        self.polynomial = self._clean_polynomial(polynomial)
        self.verbose = args.verbose
        self.plot = args.plot
        if polynomial != {}:
            self.degree = max(polynomial)
        else:
            self.degree = None

    def _clean_polynomial(self, polynomial_dict):
        """
        Removes floating points if value is int
        """
        for degree, coef in polynomial_dict.items():
            if type(coef) == float and coef.is_integer():
                polynomial_dict[degree] = int(coef)
        return polynomial_dict

    def _print_verbose(self, a, b):
        """
        Select lines to print if verbose is activated
        """
        if self.degree == 2:
            if self.discriminant > 0:
                print("x1 = (−b − √Δ)/(2a)")
                print("x2 = (−b + √Δ)/(2a)\n")
                print("x1 = ({} - {})/(2*{})".format(-b, self.root_discriminant, a))
                print("x2 = ({} + {})/(2*{})\n".format(-b, self.root_discriminant, a))
                print("x1 = {}/{}".format(-b -(self.root_discriminant), 2*a))
                print("x2 = {}/{}\n".format(-b +(self.root_discriminant), 2*a))
            elif self.discriminant == 0:
                print("x0 = -b / (2a)")
                print("x0 = {} / (2 * {})".format(-b, a))
                print("x0 = {} / {}".format(-b, 2*a))
            else:
                if b == 0:
                    print_b = ""
                else:
                    print_b = -b
                print("x1 = (−b − √Δ)/(2a)")
                print("x2 = (−b + √Δ)/(2a)\n")
                print("x1 = ({} - √{})/(2*{})".format(print_b, self.discriminant, a))
                print("x2 = ({} + √{})/(2*{})\n".format(print_b, self.discriminant, a))
                print("x1 = ({} - √{})/{}".format(print_b, self.discriminant, 2*a))
                print("x2 = ({} + √{})/{}\n".format(print_b, self.discriminant, 2*a))
                print("x1 = ({} - i√{})/{}".format(print_b, -self.discriminant, 2*a))
                print("x2 = ({} + i√{})/{}\n".format(print_b, -self.discriminant, 2*a))
                print("x1 = {}/{} - i(√{}/{})".format(print_b, 2*a, -self.discriminant, 2*a))
                print("x2 = {}/{} + i(√{}/{})\n".format(print_b, 2*a, -self.discriminant, 2*a))

    def _solve_first_degree(self):
        """
        Equation solver for polynomial degrees <= 1
        """
        fraction = None
        if self.degree == 0:
            print("You're asking me to solve {} = 0. Yeah, no, there are no real solutions to this equation.".format(self.polynomial[0]))
        else:
            if 0 in self.polynomial.keys():
                self.x0 = (0 - self.polynomial[0]) / self.polynomial[1]
                if len(str(self.x0)) - len(str(int(self.x0))) > 4:
                    fraction = str(-self.polynomial[0]) + " / {}".format(self.polynomial[1])
                if self.verbose == True:
                    print("X = {} / {}".format(- self.polynomial[0], self.polynomial[1]))
            else:
                self.x0 = 0
            if fraction != None:
                solution = str(self.x0) + " (or {}).".format(fraction)
            else:
                solution = self.x0
            print("The solution is: {}".format(solution))

    def _solve_second_degree(self):
        """
        Equation solver for degree 2
        """
        for i in range(3):
            if i not in self.polynomial.keys():
                self.polynomial[i] = 0
        a = self.polynomial[2]
        b = self.polynomial[1]
        c = self.polynomial[0]
        self.discriminant = b**2 - 4*a*c
        if self.verbose == True:
            print("a = {}, b = {}, c = {}".format(a, b, c))
            print("Δ = b² - 4ac")
            print("Δ = ({})² - 4 * {} * {}".format(b, a, c))
            print("Δ = {}\n".format(self.discriminant))
        if self.discriminant > 0:
            self.root_discriminant = self.discriminant ** 0.5
            print("√Δ = {}\n".format(self.root_discriminant))
            print("Discriminant is strictly positive, the two real solutions are:")
            self.x1 = (-b - self.root_discriminant)/(2*a)
            self.x2 = (-b + self.root_discriminant)/(2*a)
            if self.x1.is_integer() == True:
                self.x1 = int(self.x1)
            if self.x2.is_integer() == True:
                self.x2 = int(self.x2)
            if self.verbose == True:
                self._print_verbose(a, b)
            print("x1 = {}".format(self.x1))
            print("x2 = {}".format(self.x2))
        elif self.discriminant == 0:
            print("Discriminant is 0, the solution is:")
            self.x0 = -b/2*a
            if self.x0.is_integer() == True:
                self.x0 = int(self.x0)
            if self.verbose == True:
                self._print_verbose(a, b, self.discriminant)
            print("x0 = {}".format(self.x0))
        else:
            print("Discriminant is strictly negative, the two complex solutions are:")
            complex_root = (-self.discriminant) ** 0.5
            if self.verbose == True:
                self._print_verbose(a, b)
            print("x1 = {} - i * {}".format(-b/(2*a), complex_root/(2*a)))
            print("x2 = {} + i * {}".format(-b/(2*a), complex_root/(2*a)))

    def _plot_equation(self):
        """
        Bonus : plotting equation curve to visualise roots
        """
        fig = plt.figure()
        # Setting margins
        margin_ratio = 1.2
        if self.degree == 2:
            if self.discriminant > 0:
                left_border = self.x1 * margin_ratio
                right_border = self.x2 * margin_ratio
            elif self.discriminant == 0:
                left_border = self.x0 * margin_ratio
                right_border = self.x0 * margin_ratio
            else:
                print("Cannot plot a polynomial with complex roots.")
                return
        elif self.degree == 1:
            if self.x0 != 0:
                left_border = self.x0 - self.x0*margin_ratio
                right_border = self.x0 + self.x0*margin_ratio
            else:
                left_border = self.x0 - margin_ratio
                right_border = self.x0 + margin_ratio
        else:
            left_border = -5
            right_border = 5
        # setting the axes at the centre
        ax = fig.add_subplot(1, 1, 1)
        ax.spines['left'].set_position('zero')
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')
        ax.spines['bottom'].set_position('zero')
        ax.xaxis.set_ticks_position('bottom')
        ax.yaxis.set_ticks_position('left')
        x = np.linspace(left_border,right_border,1000)
        # Label corresponding functions
        for i in range(self.degree + 1):
            if i not in self.polynomial.keys():
                self.polynomial[i] = 0
        if self.degree == 2:
            a = self.polynomial[2]
            b = self.polynomial[1]
            c = self.polynomial[0]
            y = (a * x**2) + (b * x) + c
            plt.plot(x,y, 'r', label='y={}x^2 + {}x + {}'.format(a, b, c))
        elif self.degree == 1:
            b = self.polynomial[1]
            c = self.polynomial[0]
            y = (b * x) + c
            plt.plot(x,y, 'r', label='y={}x + {}'.format(b, c))
        else:
            c = self.polynomial[0]
            y = np.repeat(c, 1000)
            plt.plot(x,y, 'r', label='y={}'.format(c))
        # plot the function
        plt.plot(x,y, 'r')
        plt.legend(loc='upper left')
        # show the plot
        plt.show()

    def solve_equation(self):
        """
        Solver method called from main
        """
        if self.degree == None:
            print("Each real number is a solution to this equation.")
            return
        elif self.degree > 2:
            print("Sorry, I don't do polynomials of degree higher than 2.")
            return
        elif self.degree == 2:
            self._solve_second_degree()
        else:
            self._solve_first_degree()
        if self.plot == True:
            self._plot_equation()