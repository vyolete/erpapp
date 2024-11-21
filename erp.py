#%%writefile erp_streamlit.py

import streamlit as st
import pandas as pd

# Configuración inicial
st.set_page_config(page_title="ERP_ITM", layout="wide")

# Personalización
logo_url = "data:image/jpeg;base64,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"
empresa_nombre = "Mi Empresa ERP"

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
    
    # Crear Cliente
    with st.form(key="form_cliente"):
        cliente_nombre = st.text_input("Nombre del Cliente")
        cliente_correo = st.text_input("Correo del Cliente")
        cliente_telefono = st.text_input("Teléfono del Cliente")
        submit_button = st.form_submit_button(label="Agregar Cliente")
        
        if submit_button and cliente_nombre and cliente_correo and cliente_telefono:
            nuevo_cliente = {
                "ID": st.session_state["id_cliente"],
                "Nombre": cliente_nombre,
                "Correo": cliente_correo,
                "Teléfono": cliente_telefono
            }
            st.session_state["clientes"] = st.session_state["clientes"].append(nuevo_cliente, ignore_index=True)
            st.session_state["id_cliente"] += 1
            st.success(f"Cliente '{cliente_nombre}' agregado correctamente.")
    
    # Mostrar Clientes
    st.subheader("Clientes Registrados")
    st.write(st.session_state["clientes"])

    # Actualizar Cliente
    cliente_id = st.number_input("ID del Cliente a Actualizar", min_value=1, max_value=len(st.session_state["clientes"]))
    if st.button("Actualizar Cliente"):
        cliente = st.session_state["clientes"].iloc[cliente_id - 1]
        nombre_actualizado = st.text_input("Nuevo Nombre", cliente["Nombre"])
        correo_actualizado = st.text_input("Nuevo Correo", cliente["Correo"])
        telefono_actualizado = st.text_input("Nuevo Teléfono", cliente["Teléfono"])

        if st.button("Guardar Cambios"):
            st.session_state["clientes"].loc[cliente_id - 1, "Nombre"] = nombre_actualizado
            st.session_state["clientes"].loc[cliente_id - 1, "Correo"] = correo_actualizado
            st.session_state["clientes"].loc[cliente_id - 1, "Teléfono"] = telefono_actualizado
            st.success("Cliente actualizado correctamente.")

    # Eliminar Cliente
    cliente_a_eliminar = st.number_input("ID del Cliente a Eliminar", min_value=1, max_value=len(st.session_state["clientes"]))
    if st.button("Eliminar Cliente"):
        st.session_state["clientes"] = st.session_state["clientes"].drop(cliente_a_eliminar - 1, axis=0)
        st.session_state["clientes"].reset_index(drop=True, inplace=True)
        st.success(f"Cliente con ID {cliente_a_eliminar} eliminado.")
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
    #empleados = ["Empleado A", "Empleado B", "Empleado C"]
    #ventas_totales = st.session_state["facturas"].groupby("Cliente Nombre")["Total"].sum()
    #comisiones = [{"Empleado": empleado, "Ventas Totales": ventas_totales.sum(), 
    #               "Comisión Ganada": ventas_totales.sum() * comision_rate / 100} for empleado in empleados]
    #st.session_state["comisiones"] = pd.DataFrame(comisiones)
    
    #st.subheader("Comisiones Calculadas")
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

