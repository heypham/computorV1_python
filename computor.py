from computorv1.utils import parser
from computorv1.computor import solver

def main():
    try:
        computor_parser = parser()
        computor_parser.parse()
        computor_solver = solver(computor_parser.reduced_form, computor_parser.args)
        computor_solver.solve_equation()
    except Exception as e:
        print(e)

if __name__ == '__main__':
    main()