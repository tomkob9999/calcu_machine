## Calculu Machine


The library finds total derivatives (also partials as by-products) from multivariate system of equations of no derivatives.  Then it generates the new system of equations differential equations, and solve them from given inputs.

Sympy is used as the derivative calculation engine.  No integrals are used unlike regular differential equations.  Since integrals are inverse of derivatives, the system of equations calculates the inversions by its nature, and so in effect, it can solve the system of differential equations.

I belive the total derivatives are generally treated as obescure objects shadowed by partial derivatives.  I consider partial derivatives are merely coefficients within total derivatives and generated as by-products within the process.  They also reside in the function domain of the system whereas the total derivatives reside globally within the system.  Therefore, they can be used to derive scalar values by the system.

Expected properties from observation:

| # of variables (1) | # of Equations (2)|  # of Outputs as function | # of Inputs as function (3) | # of Subsystems (functions) (4)| # Partial Derivatives (5)| # Total Derivatives (6)|
|----------:|----------:|----------:|----------:|----------:|----------:|----------:|
| |  | =(2) | =(1)-(2) | ={(1) choose (2)} |  = (2) * (3) * (4) | =(2)|

Note: the number of total derivative equations match the number of the original equations.  While the total functions can be derivated for each output of each function, only the number of the original equations of them are independent and they appear in each function.  Therefore, total derivatives from the first function are added to the system.

Higher drivatives can be calculated by executing derive_derivatives() method multiple times as the privious derivatives are merely treated as scalers.


### Sample output

![derives](https://github.com/tomkob9999/calculu_machine/assets/96751911/77db6e85-9a66-4a56-9f91-e95c552351ab)


