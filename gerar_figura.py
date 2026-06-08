import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

# Funcoes do modelo

def E(x):
    return -(x**6)/6 + 15*(x**5)/5 - 85*(x**4)/4 + 225*(x**3)/3 - 274*(x**2)/2 + 120*x

def dE(x):
    return -(x**5) + 15*(x**4) - 85*(x**3) + 225*(x**2) - 274*x + 120

# Dados e pontos de interesse
x = np.linspace(0, 5.45, 1200)
crit = [1, 2, 3, 4, 5]
maximos = [1, 3, 5]
minimos = [2, 4]

# Cores
AZUL   = "#1f3a5f"
VERDE  = "#1b7f4b"
VERM   = "#b5341f"
CINZA  = "#6b7280"
AREIA  = "#eef2f7"

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7.4, 7.6), sharex=True,
                               gridspec_kw={"height_ratios": [1.45, 1]})

# Painel de cima: E(x)
# Marca a faixa de alta eficiencia e plota a curva E(x).
ax1.axvspan(1, 5, color=AREIA, zorder=0)
ax1.plot(x, E(x), color=AZUL, lw=2.4, zorder=3)

# Maximos e minimos locais
for xm in maximos:
    ax1.plot(xm, E(xm), "^", color=VERM, ms=11, zorder=5,
             markeredgecolor="white", markeredgewidth=1.2)
for xn in minimos:
    ax1.plot(xn, E(xn), "o", color=AZUL, ms=9, zorder=5,
             markeredgecolor="white", markeredgewidth=1.2)

# Destaque do ponto recomendado x = 3
ax1.plot(3, E(3), "*", color=VERDE, ms=22, zorder=6,
         markeredgecolor="white", markeredgewidth=1.3)
ax1.annotate("RECOMENDADO\nx = 3  (300 m)\nmaximo mais plano",
             xy=(3, E(3)), xytext=(3.05, 30.5),
             fontsize=9, color=VERDE, fontweight="bold", ha="center",
             arrowprops=dict(arrowstyle="->", color=VERDE, lw=1.4))

# Rotulos para os picos mais sensiveis
ax1.annotate("pico agudo\n(sensivel)", xy=(1, E(1)), xytext=(0.35, 31),
             fontsize=8, color=VERM, ha="center",
             arrowprops=dict(arrowstyle="->", color=VERM, lw=1.1))
ax1.annotate("pico agudo\n(sensivel)", xy=(5, E(5)), xytext=(5.0, 31),
             fontsize=8, color=VERM, ha="center",
             arrowprops=dict(arrowstyle="->", color=VERM, lw=1.1))

ax1.set_ylabel("Eficiencia do sinal  E(x)", fontsize=10.5)
ax1.set_title("E(x): eficiencia do sinal em funcao da altura da antena",
              fontsize=11.5, fontweight="bold", pad=10)
ax1.set_ylim(28, 42)
ax1.grid(True, alpha=0.25, linewidth=0.7)
ax1.set_axisbelow(True)

leg = [
    plt.Line2D([0],[0], marker="^", color="w", markerfacecolor=VERM, markersize=10, label="Maximo local"),
    plt.Line2D([0],[0], marker="o", color="w", markerfacecolor=AZUL, markersize=9, label="Minimo local"),
    plt.Line2D([0],[0], marker="*", color="w", markerfacecolor=VERDE, markersize=15, label="Altura escolhida"),
    Patch(facecolor=AREIA, label="Faixa de alta eficiencia"),
]
ax1.legend(handles=leg, fontsize=8.3, loc="lower center", ncol=2, framealpha=0.95)

# ===================== Painel de baixo: E'(x) ==============================
ax2.axhline(0, color=CINZA, lw=1.0, zorder=1)
ax2.axvspan(1, 5, color=AREIA, zorder=0)
ax2.plot(x, dE(x), color=VERM, lw=2.2, zorder=3)

# Zeros de E' (mesmos x dos pontos criticos)
for xc in crit:
    ax2.plot(xc, 0, "o", color="black", ms=6, zorder=5,
             markeredgecolor="white", markeredgewidth=1.0)
    ax2.annotate("x={}".format(xc), xy=(xc, 0), xytext=(xc, -7.5),
                 fontsize=8.5, ha="center", color="black")

ax2.set_ylabel("Derivada  E'(x)", fontsize=10.5)
ax2.set_xlabel("Altura da antena  x   (em centenas de metros)", fontsize=10.5)
ax2.set_title("E'(x): os zeros marcam os pontos criticos (1, 2, 3, 4, 5)",
              fontsize=11, fontweight="bold", pad=8)
ax2.set_ylim(-16, 16)
ax2.grid(True, alpha=0.25, linewidth=0.7)
ax2.set_axisbelow(True)

fig.tight_layout(h_pad=2.0)
fig.savefig("figura_eficiencia.png", dpi=200, bbox_inches="tight",
            facecolor="white")
print("Figura salva: figura_eficiencia.png")
