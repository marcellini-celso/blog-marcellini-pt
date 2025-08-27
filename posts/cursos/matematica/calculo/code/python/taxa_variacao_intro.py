# arquivo: posts/cursos/matematica/calculo/code/python/taxa_variacao_intro.py
import numpy as np
import matplotlib.pyplot as plt

def secant_slopes(f, x0, hs):
    """
    Retorna um array Nx2 com colunas [h, m_sec(h)],
    onde m_sec(h) = (f(x0+h) - f(x0)) / h.
    """
    hs = np.array(hs, dtype=float)
    msecs = np.array([(f(x0 + h) - f(x0)) / h for h in hs], dtype=float)
    return np.column_stack([hs, msecs])

def _line_through_point_slope(x, x0, y0, m):
    return m * (x - x0) + y0

def plot_secants(f, x0, hs, window=None):
    """
    Plota f(x) e duas secantes (uma com h maior e outra com h menor).
    """
    if window is None:
        window = (x0 - 3, x0 + 3)

    xs = np.linspace(window[0], window[1], 400)
    ys = np.vectorize(f)(xs)

    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    ax.plot(xs, ys, linewidth=2, label="f(x)")
    ax.axvline(x0, linestyle="--", linewidth=1)

    h_big  = float(hs[0])
    h_small = float(hs[-1])

    m_big   = (f(x0 + h_big)   - f(x0)) / h_big
    m_small = (f(x0 + h_small) - f(x0)) / h_small

    y0 = f(x0)
    ax.plot(xs, _line_through_point_slope(xs, x0, y0, m_big),
            linewidth=2, alpha=0.7, label=f"secante (h={h_big})")
    ax.plot(xs, _line_through_point_slope(xs, x0, y0, m_small),
            linewidth=2, alpha=0.85, label=f"secante (h={h_small})")

    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")
    ax.set_title("Secantes aproximando a tangente")
    ax.grid(True, alpha=0.3)
    ax.legend()
    plt.tight_layout()
    plt.show()

