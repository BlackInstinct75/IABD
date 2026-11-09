"""Demuestra que las reglas V01..V15 detectan registros inválidos.

1) La fuente original debe dar 0 violaciones.
2) Fuente + data/casos_limite/reservas_invalidas.csv debe dar EXACTAMENTE
   el conjunto de (regla, reservation_id) esperado.
"""
import sys
from common import DATA, connect, load_and_validate

ESPERADO = {
    ("V01_id_unico", "R001"),
    ("V02_fecha_importe_invalido", "INV15"),
    ("V03_inicio_antes_de_fin", "INV02"),
    ("V04_estado_en_dominio", "INV03"),
    ("V05_miembro_existe", "INV04"),
    ("V06_espacio_existe", "INV05"),
    ("V07_servicio_existe_y_formato", "INV06"),
    ("V07_servicio_existe_y_formato", "INV14"),
    ("V08_cantidad_positiva", "INV07"),
    ("V09_sin_solapamiento", "R001"),
    ("V09_sin_solapamiento", "INV08"),
    ("V10_importe_coherente", "INV09"),
    ("V11_plazas_dentro_de_capacidad", "INV10"),
    ("V12_redundancia_coherente", "INV11"),
    ("V13_creada_antes_del_inicio", "INV12"),
    ("V14_canal_en_dominio", "INV13"),
    ("V15_servicio_no_repetido_en_reserva", "INV16"),
    # Efectos colaterales ESPERADOS del id duplicado R001: al existir dos filas con el
    # mismo id, sus servicios se duplican (V15) y el importe de servicios se dobla (V10).
    ("V10_importe_coherente", "R001"),
    ("V15_servicio_no_repetido_en_reserva", "R001"),
}


def main():
    ok = True
    v0 = load_and_validate(connect(), DATA / "reservas_fuente.csv")
    print(f"Fuente original: {len(v0)} violaciones (esperado 0) -> {'OK' if not v0 else 'FALLO'}")
    ok &= not v0

    inv = DATA / "casos_limite" / "reservas_invalidas.csv"
    v1 = set(load_and_validate(connect(), DATA / "reservas_fuente.csv", inv))
    print(f"\nFuente + casos límite: {len(v1)} violaciones distintas")
    for regla, rid in sorted(v1):
        print(f"  {regla:<40} {rid}")
    faltan, sobran = ESPERADO - v1, v1 - ESPERADO
    print(f"\nNo detectadas: {sorted(faltan) or 'ninguna'}")
    print(f"Falsos positivos: {sorted(sobran) or 'ninguno'}")
    ok &= not faltan and not sobran
    print("\nRESULTADO:", "OK" if ok else "FALLO")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
