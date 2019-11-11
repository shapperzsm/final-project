import sympy as sym
import numpy as np
sym.init_printing()

x, y = sym.symbols("x, y")

A = sym.Matrix([[3, 0], [5, 1]])
B = A.transpose()

sigma_r = sym.Matrix([[x, 1-x]])
sigma_c = sym.Matrix([y, 1-y])
#A * sigma_c, sigma_r * B

import matplotlib
import matplotlib.pyplot as plt

graph1 = plt.figure()
y_domain = [0, 1]
row_payoff = [[(A * sigma_c)[i].subs({y: value}) for value in y_domain] for i in range(2)]
plt.plot(y_domain, row_payoff[0], label="$(A\sigma_c^T)_1$")
plt.plot(y_domain, row_payoff[1], label="$(A\sigma_c^T)_2$")
plt.xlabel("$\sigma_c=(y, 1-y)$")
plt.title("Row player payoffs, when the col. player's strategy is $\sigma_c=(y, 1-y)$")
plt.legend()
graph1.savefig("..\..\images\PD-row-payoff.pdf")



graph2 = plt.figure()
x_domain = [0, 1]
col_payoff = [[(sigma_r * B)[i].subs({x: value}) for value in x_domain] for i in range(2)]
plt.plot(x_domain, col_payoff[0], label="$(\sigma_rB)_1$")
plt.plot(y_domain, row_payoff[1], label="$(\sigma_rB)_2$")
plt.xlabel("$\sigma_r=(x, 1-x)$")
plt.title("Col. player's payoffs, when the row player's strategy is $\sigma_r=(x, 1-x)$")
plt.legend()
graph2.savefig("..\..\images\PD-col-payoff.pdf")