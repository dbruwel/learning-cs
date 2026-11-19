"""My implementation of standard quadrature used to find the integral of a 1D interval.
This is mainly to learn the math concept, and has no "clever speedups"; it's a very standard implementation.

Standard quadrature integrates a function over the unit ball, [-1, 1], by approximating the function with a polynomial
(in a clever way, more below) and integrating that exactly (up to numeric precision). Typcially, polynomials of two different
orders are fit, and their difference is used as an estimate of the error. In our case we use the standard of a 6th and 14th
order polynomial. Hence, for a function over an arbitrary interval, to achieve some given error bound, you rescale the function
to the unit ball, integrate it, check the error, and if its bad, split the interval in half and try on both halves, repeating until
each section has a small enough relative error (comapred to its size) that the algorithm can terminate.

The core of the above relies on being able to approximatly integrate a funciton over [-1, 1] quickly and efficiently via
polynomial approximation. Of course, typically polynomial interpolation gives different results depending on where the x
values are chosen to interpolate around. Evenly spaced can cause Runge's phenomena, and while Chebychev nodes are good for
approximating the function well, for integration, we don't actually care about approximating the function well, just its
integral. In particular, we usually use the zeros of the Lagendre polynomials, this is motivated because if our function
was a polynomial, and we were using an approxmation of order n, we could find p(x) = q(x) P_{n-1}(x) + r(x), and then
integrating p(x) we get that the q(x) P_{n-1}(x) term goes to zero (because of the) definition of the Legendre polynomials.
So, the integral of p(x) is the same as that of r(x). If we choose the xi as the zeros of the Legendre polynomial, then
p(xi) = r(xi) so interpolating off just the xi gives us the same answer. This sort of logic is the idea, and it's what we use
for the "bad" approximation (in our case, the one of degree 6). We could do the same for the one of degree 14, but in general
none of the nodes would align with eachother, so we'd need 7 + 15 = 22 function evaluations. Instead, we give up on a bit of
accuracy, and for the 14 degree polynomial, we use the Kronrod nodes, which start with the same intial 7 nodes, and then add
8 more that are the best choice by the above logic. This just needs 15 function evaluations for some loss in accuracy.

One of the great things about the above method is that the nodes are fixed regardless of the function. And so the Lagrange basis
polynomials are the same, so for function values yi (for each xi) we just have that our interpolation is p(x) = sum_i y_i L_i(x)
where L_i(x) is the associated Lagrange interpolation polynomial. Then the integral of p(x) just ends up being sum_i y_i * c_i
for some constants c_i which are just the integrals of the Lagrange polynomials over [-1, 1] for the nodes as above. Which is
just a dot product between c_i which can simply be precomputed once. That turns the integration into function evaluations
(to get y_i, unavoidable), and then a fast dot product with some precomputed values. This applies for both the bad 6th degree
approximation, and the good 14th degree one, and is super easy to implement. Most of the implementation is just scaling thigns
and then doing the loop where the error is checked each time.
"""

import numpy as np

KRONROD_15_NODES = np.array(
    [
        -0.9914553711208126,
        -0.9491079123427585,
        -0.8648644233597691,
        -0.7415311855993945,
        -0.5860872354676911,
        -0.4058451513773972,
        -0.2077849550078985,
        0.0,
        0.2077849550078985,
        0.4058451513773972,
        0.5860872354676911,
        0.7415311855993945,
        0.8648644233597691,
        0.9491079123427585,
        0.9914553711208126,
    ]
)

LEGENDRE_7_WEIGHTS = np.array(
    [
        0.1294849661688697,
        0.2797053914892767,
        0.3818300505051189,
        0.4179591836734694,
        0.3818300505051189,
        0.2797053914892767,
        0.1294849661688697,
    ]
)

KRONROD_15_WEIGHTS = np.array(
    [
        0.0229353220105292,
        0.0630920926299786,
        0.1047900103222502,
        0.1406532597155259,
        0.1690047266392679,
        0.1903505780647854,
        0.2044329400752989,
        0.2094821410847278,
        0.2044329400752989,
        0.1903505780647854,
        0.1690047266392679,
        0.1406532597155259,
        0.1047900103222502,
        0.0630920926299786,
        0.0229353220105292,
    ]
)


def integrate_func_uball(func) -> tuple[float, float]:
    """Integrates a function on [-1, 1] using standard quadrature.
    Produces a good and a bad estimate, and compares them to find the error.

    Parameters
    ----------
    func : _type_
        The function to integrate.

    Returns
    -------
    tupple[float, float]
        The integral and an estimate of the error bound
    """
    f_eval = []
    for x in KRONROD_15_NODES:
        f_eval.append(func(x))
    f_eval = np.array(f_eval)

    good_estimate = np.dot(f_eval, KRONROD_15_WEIGHTS)
    bad_estimate = np.dot(f_eval[1::2], LEGENDRE_7_WEIGHTS)

    res = good_estimate
    err = np.abs(good_estimate - bad_estimate)

    return res, err


def single_integrate_func(func, interval: tuple) -> tuple[float, float]:
    """Integrates a function over a specified interval

    Parameters
    ----------
    func : _type_
        The function to integrate
    interval : tuple
        The interval to integrate over

    Returns
    -------
    tuple[float, float]
        The integral and an estimate of the error bound
    """
    inv_grad = (interval[1] - interval[0]) / 2
    mid_point = (interval[1] + interval[0]) / 2

    shift = lambda x: inv_grad * x + mid_point
    shift_func = lambda x: func(shift(x))

    scaled_res, scaled_err = integrate_func_uball(shift_func)
    res = scaled_res * inv_grad
    err = scaled_err * inv_grad

    return res, err


def split_interval(interval: tuple) -> list[tuple[float, float]]:
    """Helper function to split an interval into two

    Parameters
    ----------
    interval : tuple
        The initial interval

    Returns
    -------
    list[tuple[float, float]]
        A list containing the halves
    """
    m = (interval[0] + interval[1]) / 2
    return [(interval[0], m), (m, interval[1])]


def integrate_func(func, interval: tuple, tol: float) -> tuple[float, float]:
    """Integrates a function over a given interval to within a certain tolerance bound.

    Parameters
    ----------
    func : _type_
        The function to integrate
    interval : tuple
        The interval to integrate over
    tol : float
        The tollerance to achieve (not guarenteed)

    Returns
    -------
    tuple[float, float]
        The integral and an estimate of the error bound
    """
    res = 0
    err = 0
    q = [interval]

    while len(q) > 0:
        working_interval = q.pop()
        size = np.abs(
            (working_interval[1] - working_interval[0]) / (interval[1] - interval[0])
        )
        working_res, working_err = single_integrate_func(func, working_interval)
        if working_err / size < tol:
            res = res + working_res
            err = err + working_err
        else:
            q.extend(split_interval(working_interval))

    return res, err


def main():
    func = lambda x: np.cos(x)
    print(integrate_func(func, (-10, 10), 1e-9))


if __name__ == "__main__":
    main()
