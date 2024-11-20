import streamlit as st
import pandas as pd
from fpdf import FPDF

# Configuración inicial
st.set_page_config(page_title="ERP con Autenticación", layout="wide")

# Variables de autenticación
USER = "Lira"
PASSWORD = "Lir@1120"

# Inicialización de estados en sesión
if "auth" not in st.session_state:
    st.session_state["auth"] = False

if "modulo" not in st.session_state:
    st.session_state["modulo"] = None

if "clientes" not in st.session_state:
    st.session_state["clientes"] = pd.DataFrame(columns=["ID", "Nombre", "Correo", "Teléfono"])

if "facturas" not in st.session_state:
    st.session_state["facturas"] = pd.DataFrame(columns=["Factura ID", "Cliente ID", "Cliente Nombre", "Detalles", "Total"])

if "inventario" not in st.session_state:
    st.session_state["inventario"] = pd.DataFrame(columns=["Producto", "Cantidad", "Precio Unitario"])

# Funciones auxiliares
def exportar_csv(df, nombre_archivo):
    """Permite exportar un DataFrame como archivo CSV."""
    st.download_button(
        label="Exportar Datos",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name=nombre_archivo,
        mime="text/csv",
    )

def generar_pdf(factura_id, factura):
    """Genera un PDF con los detalles de la factura."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Factura #{factura_id}", ln=True, align="C")
    pdf.cell(200, 10, txt=f"Cliente: {factura['Cliente Nombre']}", ln=True, align="L")
    pdf.ln(10)
    pdf.cell(200, 10, txt="Detalles de la Factura:", ln=True, align="L")
    pdf.ln(5)
    for detalle in factura["Detalles"]:
        pdf.cell(200, 10, txt=f"Producto: {detalle['Producto']}, Cantidad: {detalle['Cantidad']}, Subtotal: ${detalle['Subtotal']}", ln=True, align="L")
    pdf.ln(5)
    pdf.cell(200, 10, txt=f"Total: ${factura['Total']}", ln=True, align="L")
    return pdf.output(dest="S").encode("latin1")

# Funciones de los módulos
def gestion_clientes():
    st.header("Gestión de Clientes")
    with st.form("Registro de Cliente"):
        cliente_id = st.text_input("ID del Cliente")
        nombre = st.text_input("Nombre")
        correo = st.text_input("Correo Electrónico")
        telefono = st.text_input("Teléfono")
        submitted = st.form_submit_button("Registrar Cliente")
        if submitted:
            nuevo_cliente = {"ID": cliente_id, "Nombre": nombre, "Correo": correo, "Teléfono": telefono}
            st.session_state["clientes"] = pd.concat([st.session_state["clientes"], pd.DataFrame([nuevo_cliente])], ignore_index=True)
            st.success("Cliente registrado correctamente.")
    st.dataframe(st.session_state["clientes"])
    exportar_csv(st.session_state["clientes"], "clientes.csv")

def gestion_inventario():
    st.header("Gestión de Inventario")
    with st.form("Registro de Producto"):
        producto = st.text_input("Producto")
        cantidad = st.number_input("Cantidad", min_value=1, step=1)
        precio_unitario = st.number_input("Precio Unitario", min_value=0.0, step=0.1)
        submitted = st.form_submit_button("Registrar Producto")
        if submitted:
            nuevo_producto = {"Producto": producto, "Cantidad": cantidad, "Precio Unitario": precio_unitario}
            st.session_state["inventario"] = pd.concat([st.session_state["inventario"], pd.DataFrame([nuevo_producto])], ignore_index=True)
            st.success("Producto registrado correctamente.")
    st.dataframe(st.session_state["inventario"])
    exportar_csv(st.session_state["inventario"], "inventario.csv")

def gestion_facturas():
    st.header("Gestión de Facturas")
    if st.session_state["clientes"].empty or st.session_state["inventario"].empty:
        st.warning("Debe registrar al menos un cliente y un producto antes de generar una factura.")
        return
    with st.form("Registrar Factura"):
        cliente_id = st.selectbox("Seleccionar Cliente", st.session_state["clientes"]["ID"])
        productos = st.multiselect("Seleccionar Productos", st.session_state["inventario"]["Producto"])
        submitted = st.form_submit_button("Registrar Factura")
        if submitted and productos:
            total = 0
            detalles = []
            for producto in productos:
                cantidad = st.session_state["inventario"].loc[st.session_state["inventario"]["Producto"] == producto, "Cantidad"].values[0]
                precio = st.session_state["inventario"].loc[st.session_state["inventario"]["Producto"] == producto, "Precio Unitario"].values[0]
                subtotal = cantidad * precio
                total += subtotal
                detalles.append({"Producto": producto, "Cantidad": cantidad, "Subtotal": subtotal})
            nueva_factura = {
                "Factura ID": len(st.session_state["facturas"]) + 1,
                "Cliente ID": cliente_id,
                "Cliente Nombre": st.session_state["clientes"].loc[st.session_state["clientes"]["ID"] == cliente_id, "Nombre"].values[0],
                "Detalles": detalles,
                "Total": total,
            }
            st.session_state["facturas"] = pd.concat([st.session_state["facturas"], pd.DataFrame([nueva_factura])], ignore_index=True)
            st.success(f"Factura registrada con un total de ${total}.")
    st.dataframe(st.session_state["facturas"])
    exportar_csv(st.session_state["facturas"], "facturas.csv")
    if st.button("Imprimir Factura"):
        factura_id = st.number_input("Factura ID", min_value=1, step=1)
        factura = st.session_state["facturas"].iloc[factura_id - 1].to_dict()
        pdf = generar_pdf(factura_id, factura)
        st.download_button("Descargar Factura PDF", data=pdf, file_name=f"factura_{factura_id}.pdf", mime="application/pdf")

def gestion_reportes():
    st.header("Gestión de Reportes")
    total_ventas = st.session_state["facturas"]["Total"].sum()
    st.write(f"Ventas Totales: ${total_ventas}")
    # Generar más reportes aquí
    exportar_csv(st.session_state["facturas"], "reporte.csv")

# Interfaz principal
with st.sidebar:
    st.title("ERP con Autenticación")
    if not st.session_state["auth"]:
        st.subheader("Iniciar Sesión")
        usuario = st.text_input("Usuario")
        contraseña = st.text_input("Contraseña", type="password")
        if st.button("Ingresar"):
            if usuario == USER and contraseña == PASSWORD:
                st.session_state["auth"] = True
                st.success("Inicio de sesión exitoso.")
                st.experimental_rerun()
            else:
                st.error("Usuario o contraseña incorrectos.")
    else:
        st.session_state["modulo"] = st.radio("Módulos:", [
            "Gestión de Clientes", 
            "Gestión de Inventario", 
            "Gestión de Facturas", 
            "Gestión de Reportes"
        ])
        if st.button("Cerrar Sesión"):
            st.session_state["auth"] = False
            st.session_state["modulo"] = None
            st.success("Sesión cerrada correctamente.")
            st.experimental_rerun()

# Renderización de módulos
if st.session_state["auth"]:
    if st.session_state["modulo"] == "Gestión de Clientes":
        gestion_clientes()
    elif st.session_state["modulo"] == "Gestión de Inventario":
        gestion_inventario()
    elif st.session_state["modulo"] == "Gestión de Facturas":
        gestion_facturas()
    elif st.session_state["modulo"] == "Gestión de Reportes":
        gestion_reportes()
