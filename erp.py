#%%writefile erp_streamlit.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from fpdf import FPDF

logo_path = "data:image/png;base64,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"  # Asegúrate de poner la ruta correcta

# Configuración inicial
st.set_page_config(page_title="Módulos del ERP", layout="wide",page_icon=logo_path)
# Ruta del archivo de imagen (logo)

# Mostrar el logo en la parte superior de la aplicación
st.image(logo_path, width=200)  # Puedes ajustar el tamaño cambiando el valor de 'width'

# Agregar un título o contenido a la aplicación
st.title("Sistema ERP")
st.write("Bienvenido al sistema ERP para la gestión de clientes, inventarios, facturación, reportes y análisis de ventas.")

st.sidebar.title("ERP_ITM")

# Variables de autenticación
USER = "Lira"
PASSWORD = "Lir@1120"

# Inicialización de variables globales
if "auth" not in st.session_state:
    st.session_state["auth"] = False

if "modulo_seleccionado" not in st.session_state:
    st.session_state["modulo_seleccionado"] = None

# Parámetros de ID
if "id_cliente" not in st.session_state:
    st.session_state["id_cliente"] = 1  # El primer ID de cliente

if "id_producto" not in st.session_state:
    st.session_state["id_producto"] = 1  # El primer ID de producto

if "id_factura" not in st.session_state:
    st.session_state["id_factura"] = 1  # El primer ID de factura

# Inicialización de DataFrames
if "clientes" not in st.session_state:
    st.session_state["clientes"] = pd.DataFrame(columns=["ID", "Nombre", "Correo", "Teléfono"])

if "productos" not in st.session_state:
    st.session_state["productos"] = pd.DataFrame(columns=["ID", "Producto", "Cantidad", "Precio Unitario"])

if "facturas" not in st.session_state:
    st.session_state["facturas"] = pd.DataFrame(columns=["Factura ID", "Cliente ID", "Cliente Nombre", "Productos", "Total", "IVA", "Fecha"])
    
# Función de autenticación
with st.sidebar:
    st.title("Módulos ERP")
if not st.session_state["auth"]:
    st.sidebar.subheader("Iniciar Sesión")
    usuario = st.sidebar.text_input("Usuario")
    contraseña = st.sidebar.text_input("Contraseña", type="password")
    if st.sidebar.button("Ingresar"):
        if usuario == USER and contraseña == PASSWORD:
            st.session_state["auth"] = True
            st.sidebar.success("Inicio de sesión exitoso.")
        else:
            st.sidebar.error("Usuario o contraseña incorrectos.")
else:
    st.sidebar.subheader(f"Bienvenido, {USER}")
    st.session_state["modulo_seleccionado"] = st.sidebar.radio(
        "Selecciona un módulo:",
        ["Gestión de Clientes", "Gestión de Inventario", "Generar Factura", "Generar Reportes", "Análisis de Ventas"],
    )
    if st.sidebar.button("Cerrar Sesión"):
        st.session_state["auth"] = False
        st.session_state["modulo_seleccionado"] = None
        st.sidebar.success("Sesión cerrada correctamente.")


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
    st.header("Generar Factura")
    st.write("Selecciona un cliente y productos para crear una factura.")
    
    if st.session_state["clientes"].empty:
        st.warning("No hay clientes registrados. Por favor, registra clientes antes de crear una factura.")
        return
    
    if st.session_state["productos"].empty:
        st.warning("No hay productos en el inventario. Por favor, registra productos antes de crear una factura.")
        return
    
    cliente_id = st.selectbox("Seleccionar Cliente", st.session_state["clientes"]["ID"])
    cliente_nombre = st.session_state["clientes"].loc[
        st.session_state["clientes"]["ID"] == cliente_id, "Nombre"
    ].values[0]
    
    # Selección de productos
    productos_seleccionados = st.multiselect(
        "Selecciona productos", 
        st.session_state["productos"]["Producto"].values
    )
    
    if not productos_seleccionados:
        st.info("Selecciona al menos un producto para generar una factura.")
        return
    
    productos_detalle = []
    total = 0
    
    for producto in productos_seleccionados:
        producto_info = st.session_state["productos"].loc[
            st.session_state["productos"]["Producto"] == producto
        ]
        precio_unitario = producto_info["Precio Unitario"].values[0]
        stock_disponible = producto_info["Cantidad"].values[0]
        
        # Selección de cantidad
        cantidad = st.number_input(
            f"Cantidad de {producto} (Disponible: {stock_disponible})", 
            min_value=1, 
            max_value=stock_disponible, 
            step=1
        )
        
        subtotal = precio_unitario * cantidad
        total += subtotal
        productos_detalle.append({
            "Producto": producto,
            "Cantidad": cantidad,
            "Precio Unitario": precio_unitario,
            "Subtotal": subtotal
        })
    
    # Calcular IVA y total final
    iva = total * 0.16
    total_con_iva = total + iva
    
    # Mostrar resumen
    st.subheader("Resumen de Factura")
    st.table(pd.DataFrame(productos_detalle))
    st.write(f"Subtotal: ${total:,.2f}")
    st.write(f"IVA (16%): ${iva:,.2f}")
    st.write(f"Total: ${total_con_iva:,.2f}")
    
    # Confirmación y registro de factura
    if st.button("Confirmar y Generar Factura"):
        factura_id = st.session_state["id_factura"]
        fecha = pd.to_datetime("today").strftime("%Y-%m-%d")
        
        # Registrar factura
        factura = pd.DataFrame([{
            "Factura ID": factura_id, 
            "Cliente ID": cliente_id, 
            "Cliente Nombre": cliente_nombre,
            "Productos": productos_detalle, 
            "Total": total, 
            "IVA": iva, 
            "Fecha": fecha
        }])
        st.session_state["facturas"] = pd.concat([st.session_state["facturas"], factura], ignore_index=True)
        st.session_state["id_factura"] += 1  # Incrementar el ID para la siguiente factura
        
        # Reducir inventario
        for detalle in productos_detalle:
            producto = detalle["Producto"]
            cantidad = detalle["Cantidad"]
            st.session_state["productos"].loc[
                st.session_state["productos"]["Producto"] == producto, "Cantidad"
            ] -= cantidad
        
        st.success(f"Factura {factura_id} generada correctamente.")
        st.write(f"Total con IVA: ${total_con_iva:,.2f}")
        
        # Exportar factura
        exportar_csv(st.session_state["facturas"], f"factura_{factura_id}.csv")

def gestion_reportes():
 

    st.header("Generar Reportes")

    # Generación de reportes contables
    st.write("Aquí pueden ir los reportes contables.")
    st.write("Funciones específicas para reportes como ingresos, gastos y balances se agregarán aquí.")
    
    # Simulando el reporte básico
    st.text_area("Resumen", "Reporte generado: ingresos, gastos, balance general, etc.")
    
    # Exportar el reporte a CSV
    exportar_csv(st.session_state["facturas"], "reportes_contables.csv")

import plotly.express as px

def analisis_ventas():
    st.header("Análisis de Ventas")
    
    # Verificar si hay datos en las facturas
    if st.session_state["facturas"].empty:
        st.warning("No hay datos de facturas para analizar.")
        return

    # Crear una lista para desglosar productos en facturas
    productos_desglosados = []
    for _, fila in st.session_state["facturas"].iterrows():
        for producto in fila["Productos"]:
            productos_desglosados.append({
                "Producto": producto["Producto"],
                "Cantidad": producto["Cantidad"],
                "Subtotal": producto["Subtotal"],
                "Fecha": fila["Fecha"]
            })

    # Crear un DataFrame con los datos desglosados
    df_productos = pd.DataFrame(productos_desglosados)

    # Verificar si hay datos en el DataFrame desglosado
    if df_productos.empty:
        st.warning("No hay datos suficientes para generar análisis.")
        return

    # Análisis de ventas por producto
    st.subheader("Ventas por Producto")
    ventas_por_producto = df_productos.groupby("Producto").sum().reset_index()
    fig1 = px.bar(
        ventas_por_producto, 
        x="Producto", 
        y="Subtotal", 
        title="Ingresos por Producto", 
        labels={"Subtotal": "Ingresos ($)"},
        text="Subtotal"
    )
    st.plotly_chart(fig1, use_container_width=True)

    # Análisis de cantidades vendidas por producto
    st.subheader("Cantidad Vendida por Producto")
    fig2 = px.pie(
        ventas_por_producto, 
        names="Producto", 
        values="Cantidad", 
        title="Distribución de Cantidades Vendidas"
    )
    st.plotly_chart(fig2, use_container_width=True)

    # Análisis temporal de ventas
    st.subheader("Ingresos Totales por Fecha")
    df_productos["Fecha"] = pd.to_datetime(df_productos["Fecha"])
    ingresos_por_fecha = df_productos.groupby("Fecha").sum().reset_index()
    fig3 = px.line(
        ingresos_por_fecha, 
        x="Fecha", 
        y="Subtotal", 
        title="Evolución de Ingresos en el Tiempo",
        labels={"Subtotal": "Ingresos ($)", "Fecha": "Fecha"}
    )
    st.plotly_chart(fig3, use_container_width=True)

    st.success("Gráficos interactivos generados correctamente.")

# Navegación entre módulos
if st.session_state["auth"]:
    if st.session_state["modulo_seleccionado"] == "Gestión de Clientes":
        gestion_clientes()
    elif st.session_state["modulo_seleccionado"] == "Gestión de Inventario":
        gestion_inventario()
    elif st.session_state["modulo_seleccionado"] == "Generar Factura":
        gestion_facturas()
    elif st.session_state["modulo_seleccionado"] == "Generar Reportes":
        gestion_reportes()
    elif st.session_state["modulo_seleccionado"] == "Análisis de Ventas":
        analisis_ventas()
else:
    st.warning("Por favor, inicia sesión para continuar.")
