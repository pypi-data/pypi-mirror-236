import numpy as np


def dp_prob(a_s, lamb, mu):
    """
    a_s: (..., n)
    lambs: (...)
    mus: (...)
    """
    lamb = np.array(lamb)
    mu = np.array(mu)
    bshape = np.broadcast(lamb, mu).shape

    n = a_s.shape[-1]
    a_s = a_s + mu[..., None]

    from scipy.special import softmax, logsumexp

    # forward
    Fs = np.zeros(bshape + (2, n))
    Fs[..., :, 0] = np.array([0, 1]) * a_s[..., 0, None]
    for t in range(1, n):
        Fs[..., :, t] = -logsumexp(
            -Fs[..., :, t - 1, None]
            - a_s[..., t, None, None] * np.array([0, 1])[None, :]
            - lamb[..., None, None] * np.array([[0, 1], [1, 0]]),
            axis=-2,  # (..., 2 for c_t-1, 2 for c_t)
        )

    # backward
    ps = np.zeros(bshape + (2, n))
    ps[..., :, -1] = softmax(-Fs[..., :, -1], axis=-1)
    for t in range(n - 2, -1, -1):
        ps[..., :, t] = np.sum(
            softmax(
                -Fs[..., :, t, None]
                - lamb[..., None, None] * np.array([[0, 1], [1, 0]]),
                axis=-2,  # (..., 2 for c_t, 2 for c_t+1)
            )
            * np.expand_dims(ps[..., :, t + 1], -2),
            axis=-1,
        )

    return ps[..., 1, :]


def dp_opt(a_s, lamb, mu):
    """
    a_s: (..., n)
    lambs: (...)
    mus: (...)
    """
    lamb = np.array(lamb)
    mu = np.array(mu)
    bshape = np.broadcast(lamb, mu).shape

    n = a_s.shape[-1]
    a_s = a_s + mu[..., None]

    # forward
    deltas = np.zeros(bshape + (2, n))
    deltas[..., :, 0] = np.array([0, 1]) * a_s[..., 0, None]
    for t in range(1, n):
        deltas[..., :, t] = np.min(
            deltas[..., :, t - 1, None]
            + a_s[..., t, None, None] * np.array([0, 1])[None, :]
            + lamb[..., None, None] * np.array([[0, 1], [1, 0]]),
            # (..., 2 for c_t-1, 2 for c_t)
            axis=-2,
        )

    # backward
    cs = np.zeros(bshape + (n,), dtype=bool)
    cs[..., -1] = np.argmin(deltas[..., :, -1], axis=-1)
    for t in range(n - 2, -1, -1):
        cs[..., t] = np.argmin(
            deltas[..., :, t]
            + lamb[..., None] * np.abs(np.array([0, 1]) - cs[..., t + 1, None]),
            # (..., 2 for c_t)
            axis=-1,
        )

    return cs
