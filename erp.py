import streamlit as st
import pandas as pd

# Configuración inicial
st.set_page_config(page_title="ERP ITM", layout="wide")

# Personalización
logo_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6e/ERP_logo.png/240px-ERP_logo.png"
empresa_nombre = "Mi Empresa ERP"

# Variables globales
if "clientes" not in st.session_state:
    st.session_state["clientes"] = pd.DataFrame(columns=["ID", "Nombre", "Correo", "Teléfono"])

if "facturas" not in st.session_state:
    st.session_state["facturas"] = pd.DataFrame(columns=["Factura ID", "Cliente ID", "Cliente Nombre", "Detalles", "Total"])

if "inventario" not in st.session_state:
    st.session_state["inventario"] = pd.DataFrame(columns=["Producto", "Cantidad", "Precio Unitario"])

if "comisiones" not in st.session_state:
    st.session_state["comisiones"] = pd.DataFrame(columns=["Empleado", "Ventas Totales", "Comisión Ganada"])

# Barra lateral personalizada
with st.sidebar:
    st.image(logo_url, width=150)
    st.title(empresa_nombre)
    module = st.radio("Módulos:", [
        "Gestión de Clientes", 
        "Gestión de Inventario", 
        "Gestión de Facturas", 
        "Gestión de Nómina", 
        "Análisis de Ventas"
    ])

# Funciones de los módulos
def buscar_en_dataframe(df, columna, valor):
    """Devuelve los registros que coincidan con el valor en una columna específica."""
    return df[df[columna].str.contains(valor, case=False, na=False)]

def eliminar_registro(df, index):
    """Elimina un registro del DataFrame."""
    return df.drop(index=index).reset_index(drop=True)

def gestion_clientes():
    st.header("Gestión de Clientes")
    
    # Buscar clientes
    search_term = st.text_input("Buscar Cliente por Nombre:")
    if search_term:
        resultados = buscar_en_dataframe(st.session_state["clientes"], "Nombre", search_term)
        st.dataframe(resultados)
    
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
    
    st.subheader("Clientes Registrados")
    st.dataframe(st.session_state["clientes"])
    
    # Eliminar cliente
    eliminar = st.selectbox("Selecciona un Cliente para Eliminar:", st.session_state["clientes"]["Nombre"])
    if st.button("Eliminar Cliente"):
        st.session_state["clientes"] = eliminar_registro(st.session_state["clientes"], st.session_state["clientes"][st.session_state["clientes"]["Nombre"] == eliminar].index[0])
        st.success(f"Cliente '{eliminar}' eliminado correctamente.")

def gestion_inventario():
    st.header("Gestión de Inventario")
    
    # Buscar productos
    search_term = st.text_input("Buscar Producto:")
    if search_term:
        resultados = buscar_en_dataframe(st.session_state["inventario"], "Producto", search_term)
        st.dataframe(resultados)
    
    with st.form("Agregar Producto"):
        producto = st.text_input("Producto")
        cantidad = st.number_input("Cantidad", min_value=1, step=1)
        precio_unitario = st.number_input("Precio Unitario", min_value=0.0, step=0.1)
        submitted = st.form_submit_button("Registrar Producto")
        
        if submitted:
            nuevo_producto = {"Producto": producto, "Cantidad": cantidad, "Precio Unitario": precio_unitario}
            st.session_state["inventario"] = pd.concat([st.session_state["inventario"], pd.DataFrame([nuevo_producto])], ignore_index=True)
            st.success("Producto registrado correctamente.")
    
    st.subheader("Inventario")
    st.dataframe(st.session_state["inventario"])
    
    # Eliminar producto
    eliminar = st.selectbox("Selecciona un Producto para Eliminar:", st.session_state["inventario"]["Producto"])
    if st.button("Eliminar Producto"):
        st.session_state["inventario"] = eliminar_registro(st.session_state["inventario"], st.session_state["inventario"][st.session_state["inventario"]["Producto"] == eliminar].index[0])
        st.success(f"Producto '{eliminar}' eliminado correctamente.")

def gestion_facturas():
    st.header("Gestión de Facturas")
    
    if st.session_state["clientes"].empty or st.session_state["inventario"].empty:
        st.warning("Es necesario registrar clientes y productos primero.")
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
            
            st.session_state["facturas"] = pd.concat([st.session_state["facturas"], pd.DataFrame([{
                "Factura ID": len(st.session_state["facturas"]) + 1,
                "Cliente ID": cliente_id,
                "Cliente Nombre": st.session_state["clientes"].loc[st.session_state["clientes"]["ID"] == cliente_id, "Nombre"].values[0],
                "Detalles": detalles,
                "Total": total
            }])], ignore_index=True)
            st.success(f"Factura registrada correctamente con un total de ${total}.")
    
    st.subheader("Facturas Registradas")
    st.dataframe(st.session_state["facturas"])

# Navegación entre módulos
if module == "Gestión de Clientes":
    gestion_clientes()
elif module == "Gestión de Inventario":
    gestion_inventario()
elif module == "Gestión de Facturas":
    gestion_facturas()
