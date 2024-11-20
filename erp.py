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
    st.session_state["facturas"] = pd.DataFrame(columns=["Factura ID", "Cliente ID", "Cliente Nombre", "Productos", "Total", "IVA", "Fecha"])

if "inventario" not in st.session_state:
    st.session_state["inventario"] = pd.DataFrame(columns=["Producto", "Cantidad", "Precio Unitario"])

if "ventas" not in st.session_state:
    st.session_state["ventas"] = pd.DataFrame(columns=["Factura ID", "Cliente ID", "Cliente Nombre", "Total", "IVA", "Fecha"])

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
    # Búsqueda y eliminación de clientes
    st.subheader("Buscar Cliente")
    search_term = st.text_input("Buscar por nombre o ID")
    if search_term:
        clientes_filtrados = st.session_state["clientes"][st.session_state["clientes"]["Nombre"].str.contains(search_term, case=False)]
        st.dataframe(clientes_filtrados)
    else:
        st.dataframe(st.session_state["clientes"])

    # Eliminación de cliente
    cliente_a_eliminar = st.selectbox("Seleccionar cliente para eliminar", st.session_state["clientes"]["ID"])
    if st.button("Eliminar Cliente"):
        st.session_state["clientes"] = st.session_state["clientes"][st.session_state["clientes"]["ID"] != cliente_a_eliminar]
        st.success("Cliente eliminado correctamente.")

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
    
    # Búsqueda de productos
    st.subheader("Buscar Producto")
    search_term = st.text_input("Buscar producto por nombre")
    if search_term:
        inventario_filtrado = st.session_state["inventario"][st.session_state["inventario"]["Producto"].str.contains(search_term, case=False)]
        st.dataframe(inventario_filtrado)
    else:
        st.dataframe(st.session_state["inventario"])

    # Eliminación de producto
    producto_a_eliminar = st.selectbox("Seleccionar producto para eliminar", st.session_state["inventario"]["Producto"])
    if st.button("Eliminar Producto"):
        st.session_state["inventario"] = st.session_state["inventario"][st.session_state["inventario"]["Producto"] != producto_a_eliminar]
        st.success("Producto eliminado correctamente.")

def gestion_facturas():
    st.header("Generar Factura")
    st.write("Selecciona un cliente y productos para crear una factura.")

    cliente_id = st.selectbox("Seleccionar Cliente", st.session_state["clientes"]["ID"])
    cliente_nombre = st.session_state["clientes"][st.session_state["clientes"]["ID"] == cliente_id]["Nombre"].values[0]
    
    productos_seleccionados = []
    total = 0
    iva = 0
    
    for producto in st.session_state["inventario"]["Producto"]:
        cantidad = st.number_input(f"Cantidad de {producto}", min_value=0, step=1)
        if cantidad > 0:
            producto_data = st.session_state["inventario"][st.session_state["inventario"]["Producto"] == producto]
            precio_unitario = producto_data["Precio Unitario"].values[0]
            total += cantidad * precio_unitario
            productos_seleccionados.append((producto, cantidad, precio_unitario))
    
    iva = total * 0.16
    total_con_iva = total + iva
    
    if st.button("Generar Factura"):
        factura_id = f"F-{len(st.session_state['facturas']) + 1}"
        st.session_state["facturas"] = pd.concat([st.session_state["facturas"], pd.DataFrame([{
            "Factura ID": factura_id,
            "Cliente ID": cliente_id,
            "Cliente Nombre": cliente_nombre,
            "Productos": productos_seleccionados,
            "Total": total_con_iva,
            "IVA": iva,
            "Fecha": pd.Timestamp.now().strftime('%Y-%m-%d')
        }])], ignore_index=True)
        st.success(f"Factura {factura_id} generada correctamente.")
    
    st.dataframe(st.session_state["facturas"])
    exportar_csv(st.session_state["facturas"], "facturas.csv")

def analisis_ventas():
    st.header("Análisis de Ventas")
    if st.session_state["facturas"].empty:
        st.warning("No hay ventas registradas.")
    else:
        st.subheader("Ventas Realizadas")
        st.dataframe(st.session_state["facturas"])
        
        # Total de ventas
        total_ventas = st.session_state["facturas"]["Total"].sum()
        st.write(f"**Total de Ventas: ${total_ventas:,.2f}**")
        
        # Reporte de IVA
        total_iva = st.session_state["facturas"]["IVA"].sum()
        st.write(f"**IVA Total: ${total_iva:,.2f}**")

def gestion_reportes():
    st.header("Generación de Reportes Contables")
    if st.session_state["facturas"].empty:
        st.warning("No hay ventas registradas.")
    else:
        st.subheader("Reporte de Ventas")
        st.write("Generación de reporte contable de todas las ventas realizadas.")
        
        # Reporte en formato PDF
        if st.button("Generar Reporte Contable PDF"):
            pdf = FPDF()
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt="Reporte Contable de Ventas", ln=True, align="C")
            
            for _, factura in st.session_state["facturas"].iterrows():
                pdf.cell(200, 10, txt=f"Factura ID: {factura['Factura ID']}, Cliente: {factura['Cliente Nombre']}, Total: ${factura['Total']}, IVA: ${factura['IVA']}", ln=True)
            
            pdf.output("/mnt/data/reporte_contable.pdf")
            st.download_button("Descargar Reporte Contable", "/mnt/data/reporte_contable.pdf")

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
                    st.experimental_rerun()  # Refrescar la app para mostrar los módulos
                else:
                    st.error("Credenciales incorrectas.")
        else:
            st.subheader("Seleccione un Módulo")
            st.session_state["modulo"] = st.selectbox("Módulo", ["Gestión de Clientes", "Gestión de Inventario", "Generar Factura", "Análisis de Ventas", "Generar Reporte Contable"])
            
            if st.session_state["modulo"] == "Gestión de Clientes":
                gestion_clientes()
            elif st.session_state["modulo"] == "Gestión de Inventario":
                gestion_inventario()
            elif st.session_state["modulo"] == "Generar Factura":
                gestion_facturas()
            elif st.session_state["modulo"] == "Análisis de Ventas":
                analisis_ventas()
            elif st.session_state["modulo"] == "Generar Reporte Contable":
                gestion_reportes()

# Función principal
def main():
    barra_lateral()

if __name__ == "__main__":
    main()
