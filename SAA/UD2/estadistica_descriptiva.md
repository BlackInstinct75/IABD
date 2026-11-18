# Ejercicios de estadística descriptiva: resolución 

Fórmulas utilizadas (varianza poblacional, dividiendo entre $n$):

$$\bar{x} = \frac{\sum x_i}{n} \qquad DM = \frac{\sum |x_i - \bar{x}|}{n} \qquad \sigma^2 = \frac{\sum (x_i - \bar{x})^2}{n} \qquad \sigma = \sqrt{\sigma^2}$$

---

## Ejercicio 1

**Datos:** 10, 13, 6, 28, 31 ($n = 5$)

**Media:** $\bar{x} = \dfrac{10+13+6+28+31}{5} = \dfrac{88}{5} = 17{,}6$

| $x_i$ | $x_i - \bar{x}$ | $\lvert x_i - \bar{x}\rvert$ | $(x_i - \bar{x})^2$ |
|---|---|---|---|
| 10 | −7,6 | 7,6 | 57,76 |
| 13 | −4,6 | 4,6 | 21,16 |
| 6 | −11,6 | 11,6 | 134,56 |
| 28 | 10,4 | 10,4 | 108,16 |
| 31 | 13,4 | 13,4 | 179,56 |
| **Suma** | 0 | **47,6** | **501,2** |

- **Desviación media:** $DM = \dfrac{47{,}6}{5} = 9{,}52$
- **Varianza:** $\sigma^2 = \dfrac{501{,}2}{5} = 100{,}24$
- **Desviación típica:** $\sigma = \sqrt{100{,}24} \approx 10{,}01$

---

## Ejercicio 2

### a) Serie: 2, 3, 6, 8, 11 ($n = 5$)

**Media:** $\bar{x} = \dfrac{30}{5} = 6$

| $x_i$ | $x_i - \bar{x}$ | $\lvert x_i - \bar{x}\rvert$ | $(x_i - \bar{x})^2$ |
|---|---|---|---|
| 2 | −4 | 4 | 16 |
| 3 | −3 | 3 | 9 |
| 6 | 0 | 0 | 0 |
| 8 | 2 | 2 | 4 |
| 11 | 5 | 5 | 25 |
| **Suma** | 0 | **14** | **54** |

- **Desviación media:** $DM = \dfrac{14}{5} = 2{,}8$
- **Varianza:** $\sigma^2 = \dfrac{54}{5} = 10{,}8$
- **Desviación típica:** $\sigma = \sqrt{10{,}8} \approx 3{,}29$

### b) Serie: 12, 6, 7, 3, 15, 10, 18, 5 ($n = 8$)

**Media:** $\bar{x} = \dfrac{76}{8} = 9{,}5$

| $x_i$ | $x_i - \bar{x}$ | $\lvert x_i - \bar{x}\rvert$ | $(x_i - \bar{x})^2$ |
|---|---|---|---|
| 12 | 2,5 | 2,5 | 6,25 |
| 6 | −3,5 | 3,5 | 12,25 |
| 7 | −2,5 | 2,5 | 6,25 |
| 3 | −6,5 | 6,5 | 42,25 |
| 15 | 5,5 | 5,5 | 30,25 |
| 10 | 0,5 | 0,5 | 0,25 |
| 18 | 8,5 | 8,5 | 72,25 |
| 5 | −4,5 | 4,5 | 20,25 |
| **Suma** | 0 | **34** | **190** |

- **Desviación media:** $DM = \dfrac{34}{8} = 4{,}25$
- **Varianza:** $\sigma^2 = \dfrac{190}{8} = 23{,}75$
- **Desviación típica:** $\sigma = \sqrt{23{,}75} \approx 4{,}87$

---

## Ejercicio 3

**Datos:** 3, 8, 4, 10, 6, 2 ($n = 6$)

### a) Media y varianza

**Media:** $\bar{x} = \dfrac{3+8+4+10+6+2}{6} = \dfrac{33}{6} = 5{,}5$

| $x_i$ | $x_i - \bar{x}$ | $(x_i - \bar{x})^2$ |
|---|---|---|
| 3 | −2,5 | 6,25 |
| 8 | 2,5 | 6,25 |
| 4 | −1,5 | 2,25 |
| 10 | 4,5 | 20,25 |
| 6 | 0,5 | 0,25 |
| 2 | −3,5 | 12,25 |
| **Suma** | 0 | **47,5** |

**Varianza:** $\sigma^2 = \dfrac{47{,}5}{6} \approx 7{,}92$

(Si se usara la varianza muestral, $s^2 = \dfrac{47{,}5}{5} = 9{,}5$.)

### b) Datos multiplicados por 3

Si $y_i = 3x_i$:

- **Nueva media:** $\bar{y} = 3\bar{x} = 3 \cdot 5{,}5 = 16{,}5$
- **Nueva varianza:** $\sigma_y^2 = 3^2 \cdot \sigma_x^2 = 9 \cdot 7{,}92 = 71{,}25$
  (con varianza muestral: $9 \cdot 9{,}5 = 85{,}5$)

**Propiedad general:** al multiplicar todos los datos por una constante $k$, la media queda multiplicada por $k$ y la varianza por $k^2$ (la desviación típica por $|k|$).
