## Calculu Machine

(Experimental Lab)

The library finds total derivatives (also partials as by-products) from multivariate system of non-linear equations of no derivatives.  Then it generates the system of non-linear differential equations by adding the total derivatives equations.  Then it solves them from given inputs.

Sympy is used as the derivative calculation engine.  Integrals are used to find anti-derivatives from derivatives.  When solving equations, since integrals are inverse of derivatives, the system of equations calculates the inversions by its nature, and so in effect, it can solve the system of differential equations.

Not all derivatives are included in total derivatives.  They cannot be added in the system as they violate independence law.  But they can be derived by simple calculations.  Given dx/dy, dy/dx = 1/(dx/dy).  Given dx/dy and dz/dy, dx/dz = (dx/dy)/(dz/dy)  The approach seems simple and practical.  Once the total derivativess are derived, the rest is all pure algebra with system of equations.

Observed patterns:

| # of variables (1) | # of Equations (2)|  # of Outputs as Function | # of Inputs as Function (3) | # of Subsystems (functions) (4)| # Partial Derivatives (5)| # Total Derivatives (6)|
|:----------|:----------|:----------|:----------|:----------|:----------|:----------|
| |  | = (2) | = (1)-(2) | = {(1) choose (2)} |  = (2) * (3) * (4) | = (2)|

Note: the number of total derivative equations match the number of the original equations.  While the total derivatives can be derivated for each output of each function, only the number of the original equations of them are independent and they appear in each function.  Therefore, total derivatives from the first function are added to the system usually unless it fails and search from the rest.

Higher drivatives and lower anti-derivatives can be found by executing derive() and anti_derive() methods incrementally as the privious derivatives are merely treated as scalers.


### Sample Execution

![exec](https://github.com/tomkob9999/calculu_machine/assets/96751911/252fb176-20f3-4132-bfc7-cec9865c1c2c)

![derives2](https://github.com/tomkob9999/calculu_machine/assets/96751911/6faa20e1-5957-41f7-96ec-1a659e70f7fe)


### Other sample output using anti-derive()


![calc](https://github.com/tomkob9999/calculu_machine/assets/96751911/3ecbe9c5-5394-4bf9-adc4-5a1878f2ef19)





