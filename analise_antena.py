"""
analise_antena.py - DPS (Differentiated Problem Solving) | Global Solution 2026

PROBLEMA
--------
A eficiencia de um sinal de satelite em funcao da altura 'x' de uma antena em
relacao ao solo (x medido em CENTENAS DE METROS) e modelada por:

    E(x) = -x^6/6 + 15x^5/5 - 85x^4/4 + 225x^3/3 - 274x^2/2 + 120x

Queremos a altura que combine boa eficiencia, estabilidade operacional
(eficiencia que varia pouco -> longe de picos muito sensiveis) e menor custo
estrutural (custo cresce com a altura).

ESTRATEGIA
----------
1) Pontos criticos sao as raizes de E'(x). Vamos acha-las com NEWTON-RAPHSON.
2) Classificamos cada ponto critico (maximo/minimo) pelo sinal de E''(x).
3) Medimos a "sensibilidade" de cada extremo por |E''| (quanto MENOR, mais
   plano -> mais estavel -> mais desejavel operacionalmente).
4) Cruzamos eficiencia, estabilidade e custo para recomendar uma altura.

Implementacao em Python puro (so biblioteca padrao), para deixar explicito
que o metodo numerico foi implementado a mao, nao chamado de uma biblioteca.
"""

# ===========================================================================
# 1. A FUNCAO E SUAS DERIVADAS
# ===========================================================================
#
# E'(x) sai limpa porque a funcao foi montada como a primitiva de
#        E'(x) = -(x-1)(x-2)(x-3)(x-4)(x-5).
# Expandindo o produto:
#        E'(x) = -x^5 + 15x^4 - 85x^3 + 225x^2 - 274x + 120
# E derivando de novo:
#        E''(x) = -5x^4 + 60x^3 - 255x^2 + 450x - 274


def E(x):
    """Eficiencia do sinal na altura x (x em centenas de metros)."""
    return (-(x**6) / 6 + 15 * (x**5) / 5 - 85 * (x**4) / 4
            + 225 * (x**3) / 3 - 274 * (x**2) / 2 + 120 * x)


def dE(x):
    """Primeira derivada E'(x). Suas raizes sao os pontos criticos."""
    return -(x**5) + 15 * (x**4) - 85 * (x**3) + 225 * (x**2) - 274 * x + 120


def d2E(x):
    """Segunda derivada E''(x). O sinal classifica max/min; |E''| mede a
    'sensibilidade' (curvatura) do extremo."""
    return -5 * (x**4) + 60 * (x**3) - 255 * (x**2) + 450 * x - 274


# ===========================================================================
# 2. METODO DE NEWTON-RAPHSON
# ===========================================================================
#
# Para achar um ZERO de uma funcao f, Newton-Raphson parte de um chute x0 e
# repete:
#        x_{n+1} = x_n - f(x_n) / f'(x_n)
# ate a correcao ficar menor que uma tolerancia.
#
# Como aqui queremos os zeros de E' (os pontos criticos de E), usamos
# f = E'  e  f' = E''. Logo a iteracao fica:
#        x_{n+1} = x_n - E'(x_n) / E''(x_n)


def newton_raphson(f, df, x0, tol=1e-10, max_iter=100):
    """Acha uma raiz de f a partir do chute x0.

    Retorna (raiz, num_iteracoes, convergiu). Robusto: se a derivada ficar
    perto de zero (risco de divisao por zero), aborta sem travar.
    """
    x = float(x0)
    for i in range(1, max_iter + 1):
        fx = f(x)
        dfx = df(x)
        if abs(dfx) < 1e-14:          # derivada quase nula -> nao da para dividir
            return x, i, False
        passo = fx / dfx
        x = x - passo
        if abs(passo) < tol:          # correcao desprezivel -> convergiu
            return x, i, True
    return x, max_iter, False


def encontrar_pontos_criticos(seeds, tol=1e-10, casas=6):
    """Roda Newton-Raphson a partir de varios chutes e junta as raizes
    distintas encontradas (arredondando para evitar duplicatas numericas).

    Retorna uma lista de dicionarios, um por ponto critico, ja ordenada.
    """
    encontradas = []
    for s in seeds:
        raiz, iters, convergiu = newton_raphson(dE, d2E, s, tol=tol)
        if not convergiu:
            continue
        raiz_arred = round(raiz, casas)
        if all(abs(raiz_arred - r["x"]) > 1e-4 for r in encontradas):
            encontradas.append({"x": raiz_arred, "seed": s, "iters": iters})
    encontradas.sort(key=lambda r: r["x"])
    return encontradas


def classificar(x):
    """Classifica o ponto critico x pelo teste da segunda derivada.

    E''(x) < 0 -> maximo local ; E''(x) > 0 -> minimo local ; ~0 -> indefinido.
    Retorna (tipo, valor_de_E, valor_de_E2).
    """
    e2 = d2E(x)
    if e2 < -1e-9:
        tipo = "MAXIMO"
    elif e2 > 1e-9:
        tipo = "MINIMO"
    else:
        tipo = "INDEFINIDO"
    return tipo, E(x), e2


# ===========================================================================
# 3. RELATORIO
# ===========================================================================

LARGURA = 70


def cabecalho(titulo):
    print("=" * LARGURA)
    print(titulo.center(LARGURA))
    print("=" * LARGURA)


def main():
    cabecalho("DPS - ESCOLHA DA ALTURA DA ANTENA (Newton-Raphson)")

    # Chutes iniciais espalhados pela faixa fisica de interesse.
    # x e dado em centenas de metros; alturas negativas nao fazem sentido.
    seeds = [0.5, 1.4, 1.7, 2.4, 2.7, 3.4, 3.7, 4.4, 4.7, 5.3]

    print("\nFuncao: E(x) = -x^6/6 + 3x^5 - 85x^4/4 + 75x^3 - 137x^2 + 120x")
    print("E'(x)  = -(x-1)(x-2)(x-3)(x-4)(x-5)")
    print("       = -x^5 + 15x^4 - 85x^3 + 225x^2 - 274x + 120")
    print("E''(x) = -5x^4 + 60x^3 - 255x^2 + 450x - 274")
    print("\nProcurando os pontos criticos (zeros de E') por Newton-Raphson...")
    print("(x em centenas de metros)\n")

    criticos = encontrar_pontos_criticos(seeds)

    # Tabela de pontos criticos
    print("-" * LARGURA)
    print("{:>6} {:>10} {:>12} {:>10} {:>8} {:>6}".format(
        "x", "altura(m)", "tipo", "E(x)", "E''(x)", "iter"))
    print("-" * LARGURA)

    maximos = []
    for c in criticos:
        x = c["x"]
        tipo, ex, e2 = classificar(x)
        if tipo == "MAXIMO":
            maximos.append({"x": x, "E": ex, "e2": e2})
        print("{:>6.3f} {:>10.0f} {:>12} {:>10.3f} {:>8.1f} {:>6}".format(
            x, x * 100, tipo, ex, e2, c["iters"]))
    print("-" * LARGURA)

    # ---- Analise da decisao -------------------------------------------------
    print("\nLEITURA DOS RESULTADOS")
    print("- |E''| mede a sensibilidade do extremo: quanto MENOR, mais plano")
    print("  (eficiencia varia pouco -> mais estavel -> mais desejavel).")
    print("- Custo cresce com a altura, entao alturas menores sao preferiveis.\n")

    if maximos:
        # Eficiencia de pico atingida nos maximos
        melhor_E = max(m["E"] for m in maximos)

        print("Maximos locais (candidatos a 'boa eficiencia'):")
        for m in maximos:
            sens = abs(m["e2"])
            perda = (melhor_E - m["E"]) / melhor_E * 100
            print("  x={:.0f}00 m | E={:.2f} ({:.1f}% abaixo do melhor) | "
                  "sensibilidade |E''|={:.0f}".format(m["x"], m["E"], perda, sens))

        # Recomendacao: entre os maximos, o de MENOR sensibilidade (mais estavel),
        # desde que mantenha eficiencia alta. Esse e o melhor compromisso.
        recomendado = min(maximos, key=lambda m: abs(m["e2"]))
        mais_barato = min(maximos, key=lambda m: m["x"])

        print("\nRECOMENDACAO")
        print("  Altura recomendada: x = {:.0f}  ->  {:.0f} metros".format(
            recomendado["x"], recomendado["x"] * 100))
        print("  Por que: e um MAXIMO (eficiencia alta, E={:.2f}) e ao mesmo".format(
            recomendado["E"]))
        print("  tempo o extremo MAIS PLANO (|E''|={:.0f}), ou seja, o mais".format(
            abs(recomendado["e2"])))
        print("  estavel - exatamente o que o enunciado valoriza.")
        print("\n  Alternativa de menor custo: x = {:.0f} -> {:.0f} m (E={:.2f}),".format(
            mais_barato["x"], mais_barato["x"] * 100, mais_barato["E"]))
        print("  mas e o pico MAIS sensivel (|E''|={:.0f}): so vale a pena se".format(
            abs(mais_barato["e2"])))
        print("  a instabilidade puder ser tolerada em troca de torre mais baixa.")

    cabecalho("FIM DA ANALISE")


if __name__ == "__main__":
    main()
