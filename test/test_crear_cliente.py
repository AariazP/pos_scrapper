"""
E2E smoke test: crear cliente.
Se modulariza el flujo y se añaden comentarios y buenas practicas.
"""

import random
from typing import TypedDict

from core.browser import get_page
from core.login import login


class Cliente(TypedDict):
    cedula: str
    nombre: str
    direccion: str
    correo: str


def navegar_a_clientes(page) -> None:
    """Ir a la pantalla de clientes usando menu lateral."""
    page.click("a.sidebar-link[routerlink='/app/cliente']")
    page.wait_for_url("**/app/cliente", timeout=60000)
    page.wait_for_selector("app-cliente")


def crear_datos_cliente() -> Cliente:
    """Genera data random controlada para el cliente."""
    r = random.randint(1000000000, 9999999999)
    return {
        "cedula": str(r),
        "nombre": f"Cliente QA AUT",               # SOLO TEXTO ✅
        "direccion": f"Calle {r}",
        "correo": f"qa{r}@test.com"
    }


def llenar_formulario_cliente(page, cliente: Cliente) -> None:
    """Completar formulario de nuevo cliente."""
    page.fill("input[formcontrolname='cedula']", cliente["cedula"])
    page.keyboard.press("Tab")

    page.fill("input[formcontrolname='nombre']", cliente["nombre"])
    page.keyboard.press("Tab")

    page.fill("input[formcontrolname='direccion']", cliente["direccion"])
    page.keyboard.press("Tab")

    page.fill("input[formcontrolname='correo']", cliente["correo"])
    page.keyboard.press("Tab")


def guardar_cliente(page) -> None:
    """Salvar y confirmar swal."""
    page.click("button#azul")  # submit form
    page.wait_for_selector(".swal2-confirm", timeout=60000)
    page.click(".swal2-confirm")
    page.wait_for_timeout(2000)


def validar_cliente(page, cliente: Cliente) -> bool:
    """Valida que el cliente existe filtrando por la cedula."""
    navegar_a_clientes(page)
    page.fill("input#buscar", cliente["cedula"])
    page.wait_for_timeout(2000)
    return page.locator(f"text={cliente['nombre']}").first.is_visible()


def main():
    playwright, browser, context, page = get_page(headless=False)

    login(page)
    navegar_a_clientes(page)

    cliente = crear_datos_cliente()

    # crear nuevo
    page.click("button#nuevo")
    page.wait_for_url("**/app/cliente/nuevo", timeout=60000)
    page.wait_for_selector("h1:has-text('Registro de clientes')", timeout=60000)

    llenar_formulario_cliente(page, cliente)
    guardar_cliente(page)

    ok = validar_cliente(page, cliente)

    if ok:
        print("FLUJO CREAR CLIENTE FUNCIONO CORRECTAMENTE")
    else:
        print("FALLO FLUJO CREAR CLIENTE")

    print(cliente)

    browser.close()
    playwright.stop()


if __name__ == "__main__":
    main()

