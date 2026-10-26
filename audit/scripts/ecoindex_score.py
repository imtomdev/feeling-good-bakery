"""EcoIndex score calculator (official quantiles, from cnumr/GreenIT-Analysis ecoIndex.js)."""
import sys
QUANTILES_DOM = [0, 47, 75, 159, 233, 298, 358, 417, 476, 537, 603, 674, 753, 843, 949, 1076, 1237, 1459, 1801, 2479, 594601]
QUANTILES_REQ = [0, 2, 15, 25, 34, 42, 49, 56, 63, 70, 78, 86, 95, 105, 117, 130, 147, 170, 205, 281, 3920]
QUANTILES_SIZE = [0, 1.37, 144.7, 319.53, 479.46, 631.97, 783.38, 937.91, 1098.62, 1265.47, 1448.32, 1648.27, 1876.08, 2142.06, 2465.37, 2866.31, 3401.59, 4155.73, 5400.08, 8037.54, 223212.26]

def quantile(q, value):
    for i in range(1, len(q)):
        if value < q[i]:
            return i - 1 + (value - q[i-1]) / (q[i] - q[i-1])
    return len(q) - 1

def score(dom, req, size_kb):
    return 100 - 5 * (3*quantile(QUANTILES_DOM, dom) + 2*quantile(QUANTILES_REQ, req) + quantile(QUANTILES_SIZE, size_kb)) / 6

def grade(s):
    for g, t in (("A",80),("B",70),("C",55),("D",40),("E",25),("F",10)):
        if s > t: return g
    return "G"

if __name__ == "__main__":
    dom, req, size = float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3])
    s = score(dom, req, size)
    print(f"dom={dom:g} req={req:g} size={size:g}Ko -> score={s:.2f} (rounded {round(s)}) grade={grade(s)} ges={2+2*(50-s)/100:.2f}gCO2e water={3+3*(50-s)/100:.2f}cl")
