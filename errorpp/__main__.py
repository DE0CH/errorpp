import argparse
import errorpp

def main():
    parser = argparse.ArgumentParser(description='Propagate Error Symbolically')
    parser.add_argument('expression', help='the expression for which to propagate the error written in latex')
    parser.add_argument('-n', '--no-absolute', dest='no_absolute', action='store_true', help='if this option is specified, the program will assume that all the variables are positive, preventing the program from wrapping variables in absolute sign, which makes a cleaner output as sympy can cancel variables more easily.')
    args = parser.parse_args()
    print(errorpp.propagate_latex(args.expression, absolute=not args.no_absolute)) 

if __name__ == "__main__":
    main()

