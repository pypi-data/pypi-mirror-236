import re
import math
import numpy as np
import matplotlib.pyplot as plt

def quadratic(equation):
    equation = equation.replace(" ", "")
  
    pattern = r'(-?\d*)x\^2([-+]?\d*)x([-+]?\d+)'
    matches = re.match(pattern, equation)

    if not matches:
        raise ValueError("Invalid quadratic equation format. Please provide a valid quadratic equation.")

    a_str, b_str, c_str = matches.groups()

    a = int(a_str) if a_str and a_str not in '+-' else 1 if not a_str or a_str == '+' else -1
    b = int(b_str) if b_str and b_str not in '+-' else 1 if not b_str or b_str == '+' else -1
    c = int(c_str) if c_str and c_str not in '+-' else 1 if not c_str or c_str == '+' else -1

    try:
        pos = (-b + math.sqrt(b**2 - 4*a*c)) / (2*a)
        neg = (-b - math.sqrt(b**2 - 4*a*c)) / (2*a)
    except:
        pos, neg = None, None

    if pos == neg:
        return np.array([pos])

    return np.array([pos, neg])

def solve(coefs):
  def factor(num):
    factors = []
    if num < 0:
      num *= -1
    i = 1
    while i <= num/2:
      if num % i == 0:
        factors.append(i)
        factors.append(-i)
      i += 1
    factors.append(num)
    factors.append(-num)
    return factors
  roots = []
  
  deg = coefs.shape[0] - 1

  efactors = factor(coefs[-1])

  if coefs[0] == 1 or coefs[0] == -1:
    for i in efactors:
      res = 0
      for j in range(deg+1):
        res += coefs[j] * i ** (deg - j)

      if res == 0:
        roots.append(i)
    return np.array(roots)

  lfactors = factor(coefs[0])

  proots = []

  for i in efactors:
    for j in lfactors:
      proots.append(i/j)

  for i in proots:
    res = 0
    for j in range(deg+1):
      res += coefs[j] * i ** (deg - j)
    if res == 0:
      roots.append(i)

    if len(roots) == deg:
      break

  return np.array(list(set(roots)))


def ln(num):
  return math.log(num, math.e)

def exp(num):
  return pow(math.e, num)

def log(num, base=10):
  return math.log(num, base)


def parametric_graph(x, y, tmin, tmax):
  ts = np.linspace(tmin, tmax, 100)

  xpoints = np.apply_along_axis(x, 0, ts)

  ypoints = np.apply_along_axis(y, 0, ts)

  plt.plot(xpoints, ypoints)

  plt.show()