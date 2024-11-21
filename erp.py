#%%writefile erp_streamlit.py

import streamlit as st
import pandas as pd

# Configuración inicial
st.set_page_config(page_title="ERP Completo", layout="wide")

# Variables globales
if "clientes" not in st.session_state:
    st.session_state["clientes"] = pd.DataFrame(columns=["ID", "Nombre", "Correo", "Teléfono"])

if "facturas" not in st.session_state:
    st.session_state["facturas"] = pd.DataFrame(columns=["Factura ID", "Cliente ID", "Cliente Nombre", "Producto", "Cantidad", "Precio Unitario", "Total"])

if "inventario" not in st.session_state:
    st.session_state["inventario"] = pd.DataFrame(columns=["Producto", "Cantidad", "Precio Unitario"])

if "comisiones" not in st.session_state:
    st.session_state["comisiones"] = pd.DataFrame(columns=["Empleado", "Ventas Totales", "Comisión Ganada"])

# Barra lateral para la navegación
st.sidebar.title("Módulos del ERP")
module = st.sidebar.radio("Selecciona un módulo:", [
    "Gestión de Clientes", 
    "Gestión de Inventario", 
    "Gestión de Facturas", 
    "Gestión de Nómina", 
    "Análisis de Ventas"
])

# Funciones de cada módulo
def gestion_clientes():
    st.header("Gestión de Clientes")
    with st.form("Registro de Cliente"):
        st.subheader("Registrar Cliente")
        cliente_id = st.text_input("ID del Cliente")
        nombre = st.text_input("Nombre del Cliente")
        correo = st.text_input("Correo Electrónico")
        telefono = st.text_input("Teléfono")
        submitted = st.form_submit_button("Registrar")
        
        if submitted:
            if cliente_id and nombre and correo:
                nuevo_cliente = {"ID": cliente_id, "Nombre": nombre, "Correo": correo, "Teléfono": telefono}
                st.session_state["clientes"] = pd.concat(
                    [st.session_state["clientes"], pd.DataFrame([nuevo_cliente])], ignore_index=True
                )
                st.success("Cliente registrado exitosamente.")
            else:
                st.error("Por favor, completa todos los campos obligatorios.")
    
    st.subheader("Clientes Registrados")
    st.dataframe(st.session_state["clientes"])

def gestion_inventario():
    st.header("Gestión de Inventario")
    with st.form("Agregar Producto"):
        st.subheader("Registrar Producto")
        producto = st.text_input("Nombre del Producto")
        cantidad = st.number_input("Cantidad", min_value=1, step=1)
        precio_unitario = st.number_input("Precio Unitario", min_value=0.0, step=0.1)
        submitted = st.form_submit_button("Agregar al Inventario")
        
        if submitted:
            if producto and cantidad > 0 and precio_unitario >= 0:
                producto_existente = st.session_state["inventario"]["Producto"] == producto
                if producto_existente.any():
                    st.session_state["inventario"].loc[producto_existente, "Cantidad"] += cantidad
                else:
                    nuevo_producto = {"Producto": producto, "Cantidad": cantidad, "Precio Unitario": precio_unitario}
                    st.session_state["inventario"] = pd.concat(
                        [st.session_state["inventario"], pd.DataFrame([nuevo_producto])], ignore_index=True
                    )
                st.success("Producto agregado/actualizado en el inventario.")
            else:
                st.error("Por favor, completa todos los campos correctamente.")
    
    st.subheader("Inventario Actual")
    st.dataframe(st.session_state["inventario"])

def gestion_facturas():
    st.header("Gestión de Facturas")
    
    if st.session_state["clientes"].empty:
        st.warning("No hay clientes registrados. Por favor, registra clientes primero.")
        return
    
    if st.session_state["inventario"].empty:
        st.warning("No hay productos en el inventario. Por favor, agrega productos primero.")
        return
    
    with st.form("Registro de Factura"):
        st.subheader("Registrar Venta")
        cliente_id = st.selectbox("Selecciona Cliente ID", st.session_state["clientes"]["ID"])
        cliente_nombre = st.session_state["clientes"].loc[
            st.session_state["clientes"]["ID"] == cliente_id, "Nombre"
        ].values[0]
        producto = st.selectbox("Selecciona Producto", st.session_state["inventario"]["Producto"])
        cantidad = st.number_input("Cantidad", min_value=1, step=1)
        submitted = st.form_submit_button("Registrar Factura")
        
        if submitted:
            producto_data = st.session_state["inventario"].loc[
                st.session_state["inventario"]["Producto"] == producto
            ]
            stock_disponible = producto_data["Cantidad"].values[0]
            precio_unitario = producto_data["Precio Unitario"].values[0]
            
            if cantidad <= stock_disponible:
                total = cantidad * precio_unitario
                nueva_factura = {
                    "Factura ID": len(st.session_state["facturas"]) + 1,
                    "Cliente ID": cliente_id,
                    "Cliente Nombre": cliente_nombre,
                    "Producto": producto,
                    "Cantidad": cantidad,
                    "Precio Unitario": precio_unitario,
                    "Total": total
                }
                st.session_state["facturas"] = pd.concat(
                    [st.session_state["facturas"], pd.DataFrame([nueva_factura])], ignore_index=True
                )
                
                # Actualizar el inventario
                st.session_state["inventario"].loc[
                    st.session_state["inventario"]["Producto"] == producto, "Cantidad"
                ] -= cantidad
                
                st.success(f"Factura registrada con éxito para {cliente_nombre}.")
            else:
                st.error("Stock insuficiente para esta venta.")
    
    st.subheader("Facturas Registradas")
    st.dataframe(st.session_state["facturas"])

def gestion_nomina():
    st.header("Gestión de Nómina")
    comision_rate = st.slider("Porcentaje de Comisión (%)", min_value=1, max_value=50, value=10)
    
    if st.session_state["facturas"].empty:
        st.warning("No hay facturas registradas. Por favor, registra ventas primero.")
        return
    
    # Calcular comisiones
    empleados = ["Empleado A", "Empleado B", "Empleado C"]
    ventas_totales = st.session_state["facturas"].groupby("Cliente Nombre")["Total"].sum()
    comisiones = [{"Empleado": empleado, "Ventas Totales": ventas_totales.sum(), 
                   "Comisión Ganada": ventas_totales.sum() * comision_rate / 100} for empleado in empleados]
    st.session_state["comisiones"] = pd.DataFrame(comisiones)
    
    st.subheader("Comisiones Calculadas")
    st.dataframe(st.session_state["comisiones"])

def analisis_ventas():
    st.header("Análisis de Ventas")
    
    if st.session_state["facturas"].empty:
        st.warning("No hay datos de ventas disponibles.")
        return
    
    st.subheader("Productos Más Vendidos")
    productos_vendidos = st.session_state["facturas"].groupby("Producto")["Cantidad"].sum().sort_values(ascending=False)
    st.bar_chart(productos_vendidos)
    
    st.subheader("Clientes con Más Ventas")
    clientes_ventas = st.session_state["facturas"].groupby("Cliente Nombre")["Total"].sum().sort_values(ascending=False)
    st.bar_chart(clientes_ventas)

# Navegar entre los módulos
if module == "Gestión de Clientes":
    gestion_clientes()
elif module == "Gestión de Inventario":
    gestion_inventario()
elif module == "Gestión de Facturas":
    gestion_facturas()
elif module == "Gestión de Nómina":
    gestion_nomina()
elif module == "Análisis de Ventas":
    analisis_ventas()

