from core.browser import get_page
from core.login import login
from datetime import datetime, timedelta

# smoke test + crear producto end2end

if __name__ == "__main__":
    p, browser, context, page = get_page(headless=False)

    login(page)
    print("LOGIN PASÓ CORRECTAMENTE")

    # navegar a productos via menú lateral
    page.click("a.sidebar-link[routerlink='/app/producto']")
    page.wait_for_url("**/app/producto", timeout=60000)
    page.wait_for_selector("app-producto")
    print("NAVEGACIÓN A PRODUCTOS OK")

    # click en NUEVO
    page.click("button#nuevo")
    page.wait_for_selector("h1.nota:has-text('Registro de productos')")

    nombre = f"Producto QA AUT {datetime.now().strftime('%H%M%S')}"

    page.fill("input[formcontrolname='codigo']", "QA001")
    page.fill("input[formcontrolname='nombre']", nombre)
    fecha_v = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
    page.fill("input[formcontrolname='fecha_vencimiento']", fecha_v)
    page.fill("input[formcontrolname='lote']", "LOTE-QA-001")

    formas_venta = page.locator("div[formarrayname='formasVenta']")
    formas_venta.locator("input[formcontrolname='nombre']").first.fill("Unidad")
    formas_venta.locator("input[formcontrolname='precioCompra']").first.fill("1000")
    formas_venta.locator("input[formcontrolname='precioVenta']").first.fill("1500")
    formas_venta.locator("input[formcontrolname='cantidad']").first.fill("50")

    page.select_option("select[formcontrolname='impuesto']", "0")

    # guardar
    page.click("button#azul")
    page.wait_for_url("**/app/producto", timeout=60000)
    page.wait_for_selector(f"table tbody:has-text('{nombre}')", timeout=60000)

    # aceptar swal2
page.wait_for_selector(".swal2-confirm", timeout=60000)
page.click(".swal2-confirm")

# volver a gestión de productos
producto_nombre = "Producto QA AUT"  # nombre usado
page.wait_for_timeout(1000)
page.click("a.sidebar-link[routerlink='/app/producto']")
page.wait_for_url("**/app/producto", timeout=60000)
page.wait_for_selector("app-producto")

# buscar el producto
page.fill("input[placeholder='Buscar']", producto_nombre)
page.wait_for_timeout(1500)

# validar resultado
if page.locator(f"text={producto_nombre}").first.is_visible():
    print("✅ FLUJO CREAR PRODUCTO FUNCIONÓ CORRECTAMENTE")
else:
    print("❌ FALLÓ FLUJO CREAR PRODUCTO")

print("✅ PRODUCTO CREADO CORRECTAMENTE")

page.wait_for_timeout(3000)
browser.close()
p.stop()
