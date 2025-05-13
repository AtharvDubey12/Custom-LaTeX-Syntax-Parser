# Custom LaTeX Syntax Parser

 ## Partial Differential Parse

 syntax : Pdiff [order](function)[dependent variable(s)]
 breakdown:
   * Pdiff = keyword
   * order = order of partial differentiation, if no order is given, it is implicitly assumed as 1
     example:
     Pdiff(x)[y] , Pdiff[1](x)[y] and Pdiff[](x)[y] are all equivalent expressions
   * dependent variables = function is to be partially differentitated with respect to these dependent variables
     example:
     Pdiff[5](x)[x,y] is equivalent to  \frac{\partial^5 x}{\partial x\partial y^4} in LaTeX (notice parser implicitly allots order as 4 for differentiation with respect to y)

     ## NOTE: Development shifted to C++ based version.
     This version is still not finished yet and will be worked on but the primary version is now the C++ coounterpart (velveX - cpp).
