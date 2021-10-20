# Computorv1 

The goal of this project is to create a polynomial equation solver.
The program takes a polynomial equation up to degree 2.

## How to  
Run the project:  
`python computor.py [equation]`  
e.g. `python computor.py "5 * X^0 + 4 * X^1 - 9.3 * X^2 = 1 * X^0"`  
The program should print  
    - The reduced form of the equation
    - Its degree  
    - Its solution(s) (real and complex) and the polarity of the discriminant if it makes sense.

## Bonuses  
- Freeform : `python computor.py "5 + 4x - 9.3x^2 = 1"`
- Spaces are not necessary
- Error management. If input is not as expected specific error is yielded. Caps insensitive
- Handling of complex solutions
- Verbose flag for the details of equation solver `-v`
- Plotting of function if possible (not if complex solution) `-p`
