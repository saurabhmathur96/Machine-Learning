#!/usr/bin/env python
import matplotlib.pyplot as plt
import numpy as np
'''
m training examples (x,y)
h(theta, x) hypothesis function = theta.T * x
J(theta, x, y) cost function = 1/2 sigma (h(theta, x) - y)^2
min J(theta, x, y)
alpha learning rate

use gradient descent for optimization
repeat until convergence
    theta(i) := theta(i) - alpha*diff(J)(theta, x) wrt theta(i)

also, diff(J)(theta, x) wrt theta = sigma 2* 1/2 *(h(theta,x)-y)*x(i)

'''


'''
h(m, x, c) = y = mx + c
J(m, x, c, y) = 1/2 * sigma (h(m, x) - y)**2
find/approximate m by minimizing J(m, x ,y)
'''


def h(m, x, c):
    return m*x + c

def J(ms, xs, cs, ys):
    return 0.5*sum(( (h(m, x, c)-y)**2 for m,x,c,y in zip(ms, xs, cs, ys) ))/len(xs)

def J_prime_wrt_c(xs, ys, m, c):
    return sum(( (h(m, x, c)-y) for x,y in zip( xs, ys) ))/len(xs)

def J_prime_wrt_m(xs, ys, m, c):
    return sum(( (h(m, x, c)-y)*x for x,y in zip( xs, ys) ))/len(xs)

def step_gradient(m_current, xs,  c_current, ys, learningRate=0.1):
    c_grad = J_prime_wrt_c(xs, ys, m_current, c_current)
    m_grad = J_prime_wrt_m(xs, ys, m_current, c_current)

    return [c_current - learningRate*c_grad, m_current - learningRate*m_grad]

def linregr_with_gradient_descent(xs, ys, c_init, m_init, learningRate, nIters):
    c = c_init
    m = m_init
    for i in range(nIters):
            [c, m] = step_gradient(m, xs, c ,ys, learningRate)
    return [c, m]

def main():
    points = np.genfromtxt("data.csv", delimiter=",")
    learningRate = 0.0001

    xs = points[:,0]
    ys = points[:, 1]
    print np.shape(ys)
    [c, m] = linregr_with_gradient_descent(xs, ys, 0, 0, learningRate, 1000)
    plt.plot(xs, ys, marker='o', ls='.')
    plt.plot(xs, [h(m,x,c) for x in xs])
    plt.show()

if __name__ == '__main__':
    main()
