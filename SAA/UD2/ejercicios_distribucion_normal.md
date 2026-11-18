# Ejercicios de distribución normal: resolución

Tipificación: si $X \sim N(\mu, \sigma)$, entonces $Z = \dfrac{X-\mu}{\sigma} \sim N(0,1)$.
Se usa la tabla de la normal estándar $\Phi(z) = P(Z \le z)$.

---

## Ejercicio 1

**Enunciado.** Temperatura máxima en junio: $X \sim N(23, 5)$. Calcular el número de días del mes con máximas entre 21º y 27º.

**Resolución.**

$$P(21 < X < 27) = P\left(\frac{21-23}{5} < Z < \frac{27-23}{5}\right) = P(-0{,}4 < Z < 0{,}8)$$

$$= \Phi(0{,}8) - \Phi(-0{,}4) = \Phi(0{,}8) - \left[1 - \Phi(0{,}4)\right]$$

$$= 0{,}7881 - (1 - 0{,}6554) = 0{,}7881 - 0{,}3446 = 0{,}4435$$

Junio tiene 30 días:

$$30 \times 0{,}4435 = 13{,}3$$

**Solución:** se espera que unos **13 días** tengan máximas entre 21º y 27º.

---

## Ejercicio 2

**Enunciado.** 500 estudiantes, $X \sim N(70, 3)$ kg. Hallar cuántos pesan:

### a) Entre 60 kg y 75 kg

$$P(60 < X < 75) = P\left(\frac{60-70}{3} < Z < \frac{75-70}{3}\right) = P(-3{,}33 < Z < 1{,}67)$$

$$= \Phi(1{,}67) - \Phi(-3{,}33) = 0{,}9525 - 0{,}0004 = 0{,}9521$$

$$500 \times 0{,}9521 = 476{,}05$$

**Solución:** unos **476 estudiantes**.

### b) Más de 90 kg

$$P(X > 90) = P\left(Z > \frac{90-70}{3}\right) = P(Z > 6{,}67) = 1 - \Phi(6{,}67) \approx 0$$

**Solución:** prácticamente **0 estudiantes**.

### c) Menos de 64 kg

$$P(X < 64) = P\left(Z < \frac{64-70}{3}\right) = P(Z < -2) = 1 - \Phi(2) = 1 - 0{,}9772 = 0{,}0228$$

$$500 \times 0{,}0228 = 11{,}4$$

**Solución:** unos **11 estudiantes**.

---

## Ejercicio 3

**Enunciado.** Si $Z \sim N(0,1)$, calcular los percentiles. Se busca el valor $z_p$ tal que $P(Z \le z_p) = p$.

| Percentil | Probabilidad $p$ | Valor $z_p$ |
|---|---|---|
| Percentil 25 (1.er cuartil) | 0,25 | $\approx -0{,}674$ |
| Percentil 50 (mediana) | 0,50 | $0$ |
| Percentil 95 | 0,95 | $\approx 1{,}645$ |
| Percentil 99 | 0,99 | $\approx 2{,}326$ |

**Comentarios.**

- **Percentil 25:** como $\Phi(0{,}67) \approx 0{,}7486$ y $\Phi(0{,}68) \approx 0{,}7517$, el valor $z_{0{,}75} \approx 0{,}674$. Por simetría, $z_{0{,}25} = -z_{0{,}75} = -0{,}674$.
- **Percentil 50:** la normal estándar es simétrica respecto de 0, por lo que la mediana es 0.
- **Percentil 95:** en la tabla, $\Phi(1{,}64) = 0{,}9495$ y $\Phi(1{,}65) = 0{,}9505$, luego $z_{0{,}95} \approx 1{,}645$.
- **Percentil 99:** en la tabla, $\Phi(2{,}32) = 0{,}9898$ y $\Phi(2{,}33) = 0{,}9901$, luego $z_{0{,}99} \approx 2{,}326$.
