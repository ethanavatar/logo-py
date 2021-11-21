import sys, os

from core import Turtle
from display import App

def main():
    if len(sys.argv) < 2:
        print('\nUsage: python3 LOGO.py <filename>')
        sys.exit(1)

    program = os.path.abspath(sys.argv[1])
    turtle = Turtle(300, 300, 0)
    app = App(turtle)

    with open(program, 'r') as f:
        lines = f.readlines()
        print (lines)
        app.run(lines)

if __name__ == '__main__':
    main()