import streamlit as st
import pandas as pd
from fpdf import FPDF

# Configuración inicial: Esta línea debe ir primero
st.set_page_config(page_title="ERP con Autenticación", layout="wide")

# Variables de autenticación
USER = "Lira"
PASSWORD = "Lir@1120"

# Inicialización de variables globales
if "auth" not in st.session_state:
    st.session_state["auth"] = False

if "modulo" not in st.session_state:
    st.session_state["modulo"] = "Gestión de Clientes"

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
    st.write("Función de gestión de facturas en construcción.")

def gestion_reportes():
    st.header("Gestión de Reportes")
    st.write("Función de generación de reportes en construcción.")

# Barra lateral
def barra_lateral():
    with st.sidebar:
        st.title("ERP con Autenticación")
        if not st.session_state["auth"]:
            st.subheader("Iniciar Sesión")
            usuario = st.text_input("Usuario")
            contraseña = st.text_input("Contraseña", type="password")
            if st.button("Ingresar"):
                if usuario == USER and contraseña == PASSWORD:
                    st.session_state["auth"] = True
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
                st.session_state["modulo"] = "Gestión de Clientes"

# Control de navegación
barra_lateral()

if st.session_state["auth"]:
    if st.session_state["modulo"] == "Gestión de Clientes":
        gestion_clientes()
    elif st.session_state["modulo"] == "Gestión de Inventario":
        gestion_inventario()
    elif st.session_state["modulo"] == "Gestión de Facturas":
        gestion_facturas()
    elif st.session_state["modulo"] == "Gestión de Reportes":
        gestion_reportes()
else:
    st.warning("Por favor, inicia sesión para continuar.")
