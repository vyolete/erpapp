import streamlit as st
import pandas as pd
from fpdf import FPDF

# Configuración inicial
st.set_page_config(page_title="ERP con Autenticación", layout="wide")

# Variables de autenticación
USER = "Lira"
PASSWORD = "Lir@1120"

# Inicialización de session_state
if "clientes" not in st.session_state:
    st.session_state["clientes"] = pd.DataFrame(columns=["ID", "Nombre", "Correo", "Teléfono"])

if "productos" not in st.session_state:
    st.session_state["productos"] = pd.DataFrame(columns=["ID", "Producto", "Precio Unitario"])

if "facturas" not in st.session_state:
    st.session_state["facturas"] = pd.DataFrame(columns=["Factura ID", "Cliente ID", "Cliente Nombre", "Productos", "Total", "IVA", "Fecha"])

if "id_cliente" not in st.session_state:
    st.session_state["id_cliente"] = 1

if "id_producto" not in st.session_state:
    st.session_state["id_producto"] = 1

if "id_factura" not in st.session_state:
    st.session_state["id_factura"] = 1


# Función para exportar a CSV
def exportar_csv(df, nombre_archivo):
    df.to_csv(nombre_archivo, index=False)
    st.download_button(
        label="Descargar CSV",
        data=df.to_csv(index=False),
        file_name=nombre_archivo,
        mime="text/csv"
    )


# CRUD Clientes
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


# CRUD Productos
def gestion_productos():
    st.header("Gestión de Productos")
    
    # Crear Producto
    with st.form(key="form_producto"):
        producto_nombre = st.text_input("Nombre del Producto")
        precio_unitario = st.number_input("Precio Unitario", min_value=0.0, format="%.2f")
        submit_button = st.form_submit_button(label="Agregar Producto")
        
        if submit_button and producto_nombre and precio_unitario > 0:
            nuevo_producto = {
                "ID": st.session_state["id_producto"],
                "Producto": producto_nombre,
                "Precio Unitario": precio_unitario
            }
            st.session_state["productos"] = st.session_state["productos"].append(nuevo_producto, ignore_index=True)
            st.session_state["id_producto"] += 1
            st.success(f"Producto '{producto_nombre}' agregado correctamente.")
    
    # Mostrar Productos
    st.subheader("Productos Registrados")
    st.write(st.session_state["productos"])

    # Actualizar Producto
    producto_id = st.number_input("ID del Producto a Actualizar", min_value=1, max_value=len(st.session_state["productos"]))
    if st.button("Actualizar Producto"):
        producto = st.session_state["productos"].iloc[producto_id - 1]
        nombre_actualizado = st.text_input("Nuevo Nombre", producto["Producto"])
        precio_actualizado = st.number_input("Nuevo Precio Unitario", min_value=0.0, format="%.2f", value=producto["Precio Unitario"])

        if st.button("Guardar Cambios"):
            st.session_state["productos"].loc[producto_id - 1, "Producto"] = nombre_actualizado
            st.session_state["productos"].loc[producto_id - 1, "Precio Unitario"] = precio_actualizado
            st.success("Producto actualizado correctamente.")

    # Eliminar Producto
    producto_a_eliminar = st.number_input("ID del Producto a Eliminar", min_value=1, max_value=len(st.session_state["productos"]))
    if st.button("Eliminar Producto"):
        st.session_state["productos"] = st.session_state["productos"].drop(producto_a_eliminar - 1, axis=0)
        st.session_state["productos"].reset_index(drop=True, inplace=True)
        st.success(f"Producto con ID {producto_a_eliminar} eliminado.")


# CRUD Facturas
def gestion_facturas():
    st.header("Gestión de Facturas")
    
    # Crear Factura
    cliente_id = st.number_input("ID del Cliente", min_value=1, max_value=len(st.session_state["clientes"]))
    productos_seleccionados = st.multiselect("Selecciona los productos", st.session_state["productos"]["Producto"])

    if len(productos_seleccionados) > 0:
        st.subheader("Detalles de la Factura")
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
        
        if st.button("Generar Factura"):
            cliente = st.session_state["clientes"].iloc[cliente_id - 1]
            factura = {
                "Factura ID": st.session_state["id_factura"],
                "Cliente ID": cliente_id,
                "Cliente Nombre": cliente["Nombre"],
                "Productos": productos_detalle,
                "Total": total,
                "IVA": iva,
                "Fecha": pd.to_datetime("today").strftime("%Y-%m-%d")
            }
            st.session_state["facturas"] = st.session_state["facturas"].append(factura, ignore_index=True)
            st.session_state["id_factura"] += 1
            st.success(f"Factura generada correctamente para el cliente {cliente['Nombre']}.")
            st.write(f"Total con IVA: {total_con_iva}")

    # Mostrar Facturas
    st.subheader("Facturas Registradas")
    st.write(st.session_state["facturas"])

    # Exportar CSV
    exportar_csv(st.session_state["facturas"], "facturas.csv")


# Menú de navegación
modulo_seleccionado = st.sidebar.selectbox("Selecciona el módulo", ["Gestión de Clientes", "Gestión de Productos", "Gestión de Facturas"])

if modulo_seleccionado == "Gestión de Clientes":
    gestion_clientes()
elif modulo_seleccionado == "Gestión de Productos":
    gestion_productos()
elif modulo_seleccionado == "Gestión de Facturas":
    gestion_facturas()
