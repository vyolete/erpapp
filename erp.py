#%%writefile erp_streamlit.py
import streamlit as st
import pandas as pd
from fpdf import FPDF

# Configuración inicial
st.set_page_config(page_title="ERP con Autenticación", layout="wide")
# Personalización
logo_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6e/ERP_logo.png/240px-ERP_logo.png"
empresa_nombre = "Mi Empresa ERP"

# Variables de autenticación
USER = "Lira"
PASSWORD = "Lir@1120"

# Inicialización de variables globales
if "auth" not in st.session_state:
    st.session_state["auth"] = False

if "modulo" not in st.session_state:
    st.session_state["modulo"] = "Gestión de Clientes"

# Parámetros de ID
if "id_cliente" not in st.session_state:
    st.session_state["id_cliente"] = 1  # El primer ID de cliente

if "id_producto" not in st.session_state:
    st.session_state["id_producto"] = 1  # El primer ID de producto

if "id_factura" not in st.session_state:
    st.session_state["id_factura"] = 1  # El primer ID de factura

# Función de autenticación
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
            else:
                st.error("Usuario o contraseña incorrectos.")
    else:
        modulo_seleccionado = st.sidebar.radio("Selecciona un módulo:", ["Gestión de Clientes", "Gestión de Inventario", "Generar Factura","Generar Reportes"])
        if st.button("Cerrar Sesión"):
            st.session_state["auth"] = False
            st.success("Sesión cerrada correctamente.")

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
    if not autenticar_usuario():
        return  # Si no está autenticado, no se permite acceder a los módulos

    st.header("Gestión de Clientes")
    
    # Registro de nuevo cliente
    with st.form("Registro de Cliente"):
        nombre = st.text_input("Nombre")
        correo = st.text_input("Correo Electrónico")
        telefono = st.text_input("Teléfono")
        submitted = st.form_submit_button("Registrar Cliente")
        
        if submitted:
            # Generación de ID para el nuevo cliente
            cliente_id = st.session_state["id_cliente"]
            nuevo_cliente = pd.DataFrame([{
                "ID": cliente_id, "Nombre": nombre, "Correo": correo, "Teléfono": telefono
            }])
            st.session_state["clientes"] = pd.concat([st.session_state["clientes"], nuevo_cliente], ignore_index=True)
            st.session_state["id_cliente"] += 1  # Incrementar el ID para el siguiente cliente
            st.success(f"Cliente {nombre} registrado correctamente con ID: {cliente_id}.")
    
    # Búsqueda de clientes
    st.subheader("Buscar Cliente")
    search_term = st.text_input("Buscar por nombre o ID")
    if search_term:
        clientes_filtrados = st.session_state["clientes"][st.session_state["clientes"]["Nombre"].str.contains(search_term, case=False)]
        st.dataframe(clientes_filtrados)
    else:
        st.dataframe(st.session_state["clientes"])

    # Edición de cliente
    cliente_a_editar = st.selectbox("Seleccionar cliente para editar", st.session_state["clientes"]["ID"])
    cliente_data = st.session_state["clientes"][st.session_state["clientes"]["ID"] == cliente_a_editar]
    if cliente_data.empty:
        st.warning("Cliente no encontrado.")
    else:
        with st.form("Editar Cliente"):
            nombre_edit = st.text_input("Nuevo Nombre", cliente_data["Nombre"].values[0])
            correo_edit = st.text_input("Nuevo Correo", cliente_data["Correo"].values[0])
            telefono_edit = st.text_input("Nuevo Teléfono", cliente_data["Teléfono"].values[0])
            submitted_edit = st.form_submit_button("Actualizar Cliente")
            
            if submitted_edit:
                st.session_state["clientes"].loc[st.session_state["clientes"]["ID"] == cliente_a_editar, "Nombre"] = nombre_edit
                st.session_state["clientes"].loc[st.session_state["clientes"]["ID"] == cliente_a_editar, "Correo"] = correo_edit
                st.session_state["clientes"].loc[st.session_state["clientes"]["ID"] == cliente_a_editar, "Teléfono"] = telefono_edit
                st.success(f"Cliente con ID {cliente_a_editar} actualizado.")

    # Eliminación de cliente
    cliente_a_eliminar = st.selectbox("Seleccionar cliente para eliminar", st.session_state["clientes"]["ID"])
    if st.button("Eliminar Cliente"):
        st.session_state["clientes"] = st.session_state["clientes"][st.session_state["clientes"]["ID"] != cliente_a_eliminar]
        st.success("Cliente eliminado correctamente.")

def gestion_inventario():
    if not autenticar_usuario():
        return  # Si no está autenticado, no se permite acceder a los módulos

    st.header("Gestión de Inventario")
    
    # Registro de producto
    with st.form("Registro de Producto"):
        producto = st.text_input("Producto")
        cantidad = st.number_input("Cantidad", min_value=1, step=1)
        precio_unitario = st.number_input("Precio Unitario", min_value=0.0, step=0.1)
        submitted = st.form_submit_button("Registrar Producto")
        
        if submitted:
            # Generación de ID para el nuevo producto
            producto_id = st.session_state["id_producto"]
            nuevo_producto = pd.DataFrame([{
                "ID": producto_id, "Producto": producto, "Cantidad": cantidad, "Precio Unitario": precio_unitario
            }])
            st.session_state["productos"] = pd.concat([st.session_state["productos"], nuevo_producto], ignore_index=True)
            st.session_state["id_producto"] += 1  # Incrementar el ID para el siguiente producto
            st.success(f"Producto {producto} registrado correctamente con ID: {producto_id}.")
    
    # Búsqueda de productos
    st.subheader("Buscar Producto")
    search_term = st.text_input("Buscar producto por nombre")
    if search_term:
        inventario_filtrado = st.session_state["productos"][st.session_state["productos"]["Producto"].str.contains(search_term, case=False)]
        st.dataframe(inventario_filtrado)
    else:
        st.dataframe(st.session_state["productos"])

    # Eliminación de producto
    producto_a_eliminar = st.selectbox("Seleccionar producto para eliminar", st.session_state["productos"]["Producto"])
    if st.button("Eliminar Producto"):
        st.session_state["productos"] = st.session_state["productos"][st.session_state["productos"]["Producto"] != producto_a_eliminar]
        st.success("Producto eliminado correctamente.")

def gestion_facturas():
    if not autenticar_usuario():
        return  # Si no está autenticado, no se permite acceder a los módulos

    st.header("Generar Factura")
    st.write("Selecciona un cliente y productos para crear una factura.")

    cliente_id = st.selectbox("Seleccionar Cliente", st.session_state["clientes"]["ID"])
    cliente_nombre = st.session_state["clientes"][st.session_state["clientes"]["ID"] == cliente_id]["Nombre"].values[0]
    
    # Selección múltiple de productos
    productos_seleccionados = st.multiselect("Selecciona productos", st.session_state["productos"]["Producto"].values)
    productos_detalle = []
    total = 0

    for producto in productos_seleccionados:
        cantidad = st.number_input(f"Cantidad de {producto}", min_value=1, step=1)
        producto_info = st.session_state["productos"][st.session_state["productos"]["Producto"] == producto]
        precio_unitario = producto_info["Precio Unitario"].values[0]
        total += precio_unitario * cantidad
        productos_detalle.append((producto, cantidad, precio_unitario))
    
    iva = total * 0.19
    total_con_iva = total + iva

    # Botón de generar factura
    if st.button("Generar Factura"):
        factura_id = st.session_state["id_factura"]
        fecha = pd.to_datetime("today").strftime("%Y-%m-%d")
        factura = pd.DataFrame([{
            "Factura ID": factura_id, "Cliente ID": cliente_id, "Cliente Nombre": cliente_nombre,
            "Productos": productos_detalle, "Total": total, "IVA": iva, "Fecha": fecha
        }])
        st.session_state["facturas"] = pd.concat([st.session_state["facturas"], factura], ignore_index=True)
        st.session_state["id_factura"] += 1  # Incrementar el ID para la siguiente factura

        st.success(f"Factura {factura_id} generada correctamente.")
        st.write(f"Total: {total_con_iva}")

        # Exportar la factura
        exportar_csv(st.session_state["facturas"], "facturas.csv")

def gestion_reportes():
    if not autenticar_usuario():
        return

    st.header("Generar Reportes")

    # Generación de reportes contables
    st.write("Aquí pueden ir los reportes contables.")
    st.write("Funciones específicas para reportes como ingresos, gastos y balances se agregarán aquí.")
    
    # Simulando el reporte básico
    st.text_area("Resumen", "Reporte generado: ingresos, gastos, balance general, etc.")
    
    # Exportar el reporte a CSV
    exportar_csv(st.session_state["facturas"], "reportes_contables.csv")

# Menú de navegación
st.sidebar.title("Módulos del ERP")
#modulo_seleccionado = st.sidebar.radio("Selecciona un módulo:", ["Gestión de Clientes", "Gestión de Inventario", "Generar Factura","Generar Reportes"])


if modulo_seleccionado == "Gestión de Clientes":
    gestion_clientes()
elif modulo_seleccionado == "Gestión de Inventario":
    gestion_inventario()
elif modulo_seleccionado == "Generar Factura":
    gestion_facturas()
elif modulo_seleccionado == "Generar Reportes":
    gestion_reportes()
