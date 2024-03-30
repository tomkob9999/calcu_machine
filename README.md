## Calculu Machine

(Experimental Lab)

The library finds total derivatives (also partials as by-products) from multivariate system of equations of no derivatives.  Then it generates the new system of equations differential equations, and solve them from given inputs.

Sympy is used as the derivative calculation engine.  No integrals are used unlike regular differential equations.  Since integrals are inverse of derivatives, the system of equations calculates the inversions by its nature, and so in effect, it can solve the system of differential equations.

I belive the total derivatives are generally treated as obescure objects shadowed by partial derivatives.  Here partial derivatives are treated as merely coefficients within total derivatives and generated as by-products within the process.  They also reside in the functional domain (I call subsystems) of the whole system whereas the total derivatives reside globally within the whole system.  Therefore, they can be used to derive scaler values by the system.

In regular math courses, the differential equations are taught using exponential functions from the beginning to the end.  Here exponential patterns are not treated separately from other functions of linear or polynomial or else.  They are inversion of log function, which is integral of reciprocal.  Log can be used as input function and the inversion is derived as exponential function as way of calculation of system of equations.

Not all derivatives seem to be included in total derivatives.  They cannot be added in the system as they violate independence.  But they can be derived by simple calculations.  Given dx/dy, dy/dx = 1/(dx/dy).  Given dx/dy and dz/dy, dx/dz = (dx/dy)/(dz/dy)

Observed patterns:

| # of variables (1) | # of Equations (2)|  # of Outputs as Function | # of Inputs as Function (3) | # of Subsystems (functions) (4)| # Partial Derivatives (5)| # Total Derivatives (6)|
|----------:|----------:|----------:|----------:|----------:|----------:|----------:|
| |  | = (2) | = (1)-(2) | = {(1) choose (2)} |  = (2) * (3) * (4) | = (2)|

Note: the number of total derivative equations match the number of the original equations.  While the total functions can be derivated for each output of each function, only the number of the original equations of them are independent and they appear in each function.  Therefore, total derivatives from the first function are added to the system.

Higher drivatives can be calculated by executing derive_derivatives() method incrementally as the privious derivatives are merely treated as scalers.


### Sample Execution

![exec](https://github.com/tomkob9999/calculu_machine/assets/96751911/252fb176-20f3-4132-bfc7-cec9865c1c2c)

![derives2](https://github.com/tomkob9999/calculu_machine/assets/96751911/6faa20e1-5957-41f7-96ec-1a659e70f7fe)



On a personal side note, I don't see yet the clear difference between total derivatives and partial differential equations(PDE), and thus why PDE seems to focus on partial derivatives not total derivatives in the context of system of equations.  ChatGPT shed some lights, but it seems to be something I need to explore more.

![pde](https://github.com/tomkob9999/calculu_machine/assets/96751911/e53d492e-0807-42e9-820a-e7d15bdfb5f3)






