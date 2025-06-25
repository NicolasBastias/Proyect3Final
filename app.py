import customtkinter as ctk
from tkinter import messagebox, ttk
from database import get_session
from crud.cliente_crud import ClienteCRUD
from crud.pedido_crud import PedidoCRUD
from crud.ingrediente_crud import IngredienteCRUD
from crud.menu_crud import MenuCRUD
from database import get_session, engine, Base
from tkinter import Listbox
from models import Pedido


# Configuración de la ventana principal
ctk.set_appearance_mode("System")  # Opciones: "System", "Dark", "Light"
ctk.set_default_color_theme("blue")  # Opciones: "blue", "green", "dark-blue"

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Gestión de Clientes y Pedidos")
        self.geometry("750x600")

        # Crear el Tabview (pestañas)
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(pady=20, padx=20, fill="both", expand=True)

        # Pestaña de Ingredientes
        self.tab_ingredientes = self.tabview.add("Ingredientes")
        self.crear_formulario_ingredientes(self.tab_ingredientes)

        # Pestaña de Menú
        self.tab_menu = self.tabview.add("Menú")
        self.crear_formulario_menu(self.tab_menu)

        # Pestaña de Clientes
        self.tab_clientes = self.tabview.add("Clientes")
        self.crear_formulario_cliente(self.tab_clientes)

        # Pestaña de Panel de Compra
        self.tab_panel_de_compra = self.tabview.add("Panel de Compra")
        self.crear_formulario_panel_de_compra(self.tab_panel_de_compra)

        # Pestaña de Pedidos
        self.tab_pedidos = self.tabview.add("Pedidos")
        self.crear_formulario_pedido(self.tab_pedidos)

        # Pestaña de Gráficos
        self.tab_graficos = self.tabview.add("Gráficos")

        self.cargar_clientes_para_panel_de_compra()
        self.cargar_menus_en_combobox()
        self.btn_agregar_compra.configure(command=self.crear_pedido_desde_panel)


                # Métodos para crear formularios y Treeviews
    def crear_formulario_ingredientes(self, parent):
        # Parte superior del formulario
        frame_superior = ctk.CTkFrame(parent)
        frame_superior.pack(pady=10, padx=10, fill="x")

        # Nombre
        ctk.CTkLabel(frame_superior, text="Nombre").grid(row=0, column=0, pady=10, padx=10)
        self.entry_nombre = ctk.CTkEntry(frame_superior)
        self.entry_nombre.grid(row=0, column=1, pady=10, padx=10)

        # Tipo
        ctk.CTkLabel(frame_superior, text="Tipo").grid(row=0, column=2, pady=10, padx=10)
        self.entry_tipo = ctk.CTkEntry(frame_superior)
        self.entry_tipo.grid(row=0, column=3, pady=10, padx=10)

        # Cantidad
        ctk.CTkLabel(frame_superior, text="Cantidad").grid(row=1, column=0, pady=10, padx=10)
        self.entry_cantidad = ctk.CTkEntry(frame_superior)
        self.entry_cantidad.grid(row=1, column=1, pady=10, padx=10)

        # Unidad de medida
        ctk.CTkLabel(frame_superior, text="Unidad de Medida").grid(row=1, column=2, pady=10, padx=10)
        self.entry_unidad = ctk.CTkEntry(frame_superior)
        self.entry_unidad.grid(row=1, column=3, pady=10, padx=10)

        # Botón
        self.btn_crear_ingrediente = ctk.CTkButton(
            frame_superior, text="Crear Ingrediente", command=self.crear_ingrediente
        )
        self.btn_crear_ingrediente.grid(row=2, column=0, pady=10, padx=10)
        self.btn_eliminar_ingrediente = ctk.CTkButton(
            frame_superior, text="Eliminar Ingrediente", command=self.eliminar_ingrediente
        )
        self.btn_eliminar_ingrediente.grid(row=2, column=1, pady=10, padx=10)


        # Parte inferior - Treeview
        frame_inferior = ctk.CTkFrame(parent)
        frame_inferior.pack(pady=10, padx=10, fill="both", expand=True)

        # 👉 Incluye las nuevas columnas aquí
        self.treeview_ingredientes = ttk.Treeview(
            frame_inferior,
            columns=("Nombre", "Tipo", "Cantidad", "Unidad"),
            show="headings"
        )
        self.treeview_ingredientes.heading("Nombre", text="Nombre")
        self.treeview_ingredientes.heading("Tipo", text="Tipo")
        self.treeview_ingredientes.heading("Cantidad", text="Cantidad")
        self.treeview_ingredientes.heading("Unidad", text="Unidad de Medida")
        self.treeview_ingredientes.pack(pady=10, padx=10, fill="both", expand=True)

    def eliminar_ingrediente(self):
        seleccion = self.treeview_ingredientes.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un ingrediente para eliminar.")
            return

        nombre = self.treeview_ingredientes.item(seleccion[0], "values")[0]

        confirmacion = messagebox.askyesno("Confirmar", f"¿Eliminar el ingrediente '{nombre}'?")
        if not confirmacion:
            return

        session = get_session()
        exito = IngredienteCRUD.borrar_ingrediente_por_nombre(session, nombre)
        session.close()

        if exito:
            self.treeview_ingredientes.delete(seleccion[0])
            self.cargar_ingredientes_en_listbox()
        else:
            messagebox.showerror("Error", "No se pudo eliminar el ingrediente.")

    def crear_formulario_menu(self, parent):
        # Marco superior: datos de entrada
        frame_superior = ctk.CTkFrame(parent)
        frame_superior.pack(pady=10, padx=10, fill="x")

        # Nombre del menú
        ctk.CTkLabel(frame_superior, text="Nombre del Menú").grid(row=0, column=0, pady=10, padx=10)
        self.entry_nombre_menu = ctk.CTkEntry(frame_superior)
        self.entry_nombre_menu.grid(row=0, column=1, pady=10, padx=10)

        # Listbox con selección múltiple de ingredientes
        ctk.CTkLabel(frame_superior, text="Ingredientes").grid(row=1, column=0, pady=10, padx=10)
        self.ingredientes_listbox = Listbox(
            frame_superior,
            selectmode="multiple",      # permite seleccionar varios
            exportselection=False,      # no pierde selección al cambiar de pestaña
            height=5,
            width=30
        )
        self.ingredientes_listbox.grid(row=1, column=1, columnspan=3, pady=10, padx=10, sticky="w")

        # Cargamos los ingredientes disponibles
        self.cargar_ingredientes_en_listbox()

        # Botón para crear menú
        self.btn_crear_menu = ctk.CTkButton(frame_superior, text="Crear Menú", command=self.crear_menu)
        self.btn_crear_menu.grid(row=2, column=0, pady=10, padx=10)
        
        self.btn_eliminar_menu = ctk.CTkButton(frame_superior, text="Eliminar Menú", command=self.eliminar_menu)
        self.btn_eliminar_menu.grid(row=2, column=1, pady=10, padx=10)


        # Marco inferior: Treeview para mostrar los menús creados
        frame_inferior = ctk.CTkFrame(parent)
        frame_inferior.pack(pady=10, padx=10, fill="both", expand=True)

        self.treeview_menu = ttk.Treeview(
            frame_inferior,
            columns=("nombre", "ingredientes"),   # ← identificadores sencillos en minúsculas
            show="headings"
        )
        self.treeview_menu.heading("nombre", text="Nombre")
        self.treeview_menu.heading("ingredientes", text="Ingredientes")
        self.treeview_menu.pack(fill="both", expand=True, padx=10, pady=10)

        # Cargar lo que ya existe en la BD
        self.cargar_menus_en_treeview()

        # Opcional: selección actualiza labels
        self.treeview_menu.bind("<<TreeviewSelect>>", self.mostrar_detalle_menu)
        
    def eliminar_menu(self):
        seleccion = self.treeview_menu.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un menú para eliminar.")
            return

        menu_id = int(seleccion[0])

        confirmacion = messagebox.askyesno("Confirmar", f"¿Eliminar el menú seleccionado?")
        if not confirmacion:
            return

        session = get_session()
        exito = MenuCRUD.borrar_menu_por_id(session, menu_id)
        session.close()

        if exito:
            self.treeview_menu.delete(seleccion[0])
            self.cargar_menus_en_combobox()
        else:
            messagebox.showerror("Error", "No se pudo eliminar el menú.")
            

    def cargar_menus_en_treeview(self):
        # Vaciar primero
        for iid in self.treeview_menu.get_children():
            self.treeview_menu.delete(iid)

        session = get_session()
        for menu in MenuCRUD.obtener_todos_menus(session):
            ingredientes_txt = ", ".join(ing.nombre for ing in menu.ingrediente)
            # iid = menu.id_menu para evitar duplicados si recargas
            self.treeview_menu.insert(
                "", "end",
                iid=menu.id_menu,
                values=(menu.nombre_menu, ingredientes_txt)
            )
        session.close()

    
    def mostrar_detalle_menu(self, event):
        """Actualiza los rótulos cuando se selecciona un menú en el Treeview."""
        seleccion = self.treeview_menu.selection()
        if not seleccion:
            return

        item_id = seleccion[0]
        nombre_menu, ingredientes_txt = self.treeview_menu.item(item_id, "values")

        self.label_detalle_nombre.configure(
            text=f"Nombre del menú: {nombre_menu}"
        )
        self.label_detalle_ingredientes.configure(
            text=f"Ingredientes: {ingredientes_txt}"
        )

    
    def cargar_ingredientes_en_listbox(self):
        session = get_session()
        ingredientes = IngredienteCRUD.leer_ingredientes(session)
        session.close()

        # Guardamos la lista completa para poder acceder luego por índice
        self.ingredientes_opciones = ingredientes

        # Limpiamos el Listbox y lo rellenamos de nuevo
        self.ingredientes_listbox.delete(0, "end")
        for ing in ingredientes:
            self.ingredientes_listbox.insert("end", ing.nombre)



    def crear_formulario_cliente(self, parent):
        # Formulario para agregar clientes
        frame_superior = ctk.CTkFrame(parent)
        frame_superior.pack(pady=10, padx=10, fill="x")
        ctk.CTkLabel(frame_superior, text="Nombre").grid(row=0, column=0, pady=10, padx=10)
        self.entry_nombre_cliente = ctk.CTkEntry(frame_superior)
        self.entry_nombre_cliente.grid(row=0, column=1, pady=10, padx=10)
        ctk.CTkLabel(frame_superior, text="Email").grid(row=0, column=2, pady=10, padx=10)
        self.entry_email_cliente = ctk.CTkEntry(frame_superior)
        self.entry_email_cliente.grid(row=0, column=3, pady=10, padx=10)

        self.btn_crear_cliente = ctk.CTkButton(frame_superior, text="Crear Cliente", command=self.crear_cliente)
        self.btn_crear_cliente.grid(row=1, column=0, pady=10, padx=10)
        self.btn_eliminar_cliente = ctk.CTkButton(frame_superior, text="Eliminar Cliente", command=self.eliminar_cliente)
        self.btn_eliminar_cliente.grid(row=1, column=1, pady=10, padx=10)


        # Treeview para mostrar clientes
        frame_inferior = ctk.CTkFrame(parent)
        frame_inferior.pack(pady=10, padx=10, fill="both", expand=True)
        self.treeview_clientes = ttk.Treeview(frame_inferior, columns=("Nombre", "Email"), show="headings")
        self.treeview_clientes.heading("Nombre", text="Nombre")
        self.treeview_clientes.heading("Email", text="Email")
        self.treeview_clientes.pack(pady=10, padx=10, fill="both", expand=True)
    
    def eliminar_cliente(self):
        seleccion = self.treeview_clientes.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un cliente para eliminar.")
            return

        email = self.treeview_clientes.item(seleccion[0], "values")[1]

        confirmacion = messagebox.askyesno("Confirmar", f"¿Eliminar al cliente con email '{email}'?")
        if not confirmacion:
            return

        session = get_session()
        exito = ClienteCRUD.borrar_cliente_por_email(session, email)
        session.close()

        if exito:
            self.treeview_clientes.delete(seleccion[0])
            self.cargar_clientes()
        else:
            messagebox.showerror("Error", "No se pudo eliminar el cliente.")


    def crear_formulario_panel_de_compra(self, parent):
        frame_superior = ctk.CTkFrame(parent)
        frame_superior.pack(pady=10, padx=10, fill="x")

        # Cliente
        ctk.CTkLabel(frame_superior, text="Cliente").grid(row=0, column=0, padx=10, pady=10)
        self.cliente_combobox = ctk.CTkComboBox(frame_superior, values=[])
        self.cliente_combobox.grid(row=0, column=1, padx=10, pady=10)

        # Menú
        ctk.CTkLabel(frame_superior, text="Menú").grid(row=0, column=2, padx=10, pady=10)
        self.menu_combobox = ctk.CTkComboBox(frame_superior, values=[])
        self.menu_combobox.grid(row=0, column=3, padx=10, pady=10)

        # Botón
        self.btn_agregar_compra = ctk.CTkButton(frame_superior, text="Agregar a la Compra")
        self.btn_agregar_compra.grid(row=0, column=4, padx=10, pady=10)

        # Treeview
        frame_inferior = ctk.CTkFrame(parent)
        frame_inferior.pack(pady=10, padx=10, fill="both", expand=True)
        self.treeview_compra = ttk.Treeview(frame_inferior, columns=("Cliente", "Menú", "Ingredientes"), show="headings")
        self.treeview_compra.heading("Cliente", text="Cliente")
        self.treeview_compra.heading("Menú", text="Menú")
        self.treeview_compra.heading("Ingredientes", text="Ingredientes")
        self.treeview_compra.pack(pady=10, padx=10, fill="both", expand=True)
        



    def crear_formulario_pedido(self, parent):
        frame_superior = ctk.CTkFrame(parent)
        frame_superior.pack(pady=10, padx=10, fill="x")

        # Botones para mover pedidos
        self.btn_subir = ctk.CTkButton(frame_superior, text="Subir", command=self.subir_pedido)
        self.btn_subir.grid(row=0, column=0, padx=10, pady=10)

        self.btn_bajar = ctk.CTkButton(frame_superior, text="Bajar", command=self.bajar_pedido)
        self.btn_bajar.grid(row=0, column=1, padx=10, pady=10)

        frame_inferior = ctk.CTkFrame(parent)
        frame_inferior.pack(pady=10, padx=10, fill="both", expand=True)

        self.treeview_pedidos = ttk.Treeview(frame_inferior, columns=("Pedido", "Cliente", "Fecha"), show="headings")
        self.treeview_pedidos.heading("Pedido", text="Pedido N°")
        self.treeview_pedidos.heading("Cliente", text="Cliente")
        self.treeview_pedidos.heading("Fecha", text="Fecha")
        self.treeview_pedidos.pack(pady=10, padx=10, fill="both", expand=True)

        self.cargar_pedidos_en_treeview()

    def cargar_pedidos_en_treeview(self):
        session = get_session()
        pedidos = session.query(Pedido).all()

        self.treeview_pedidos.delete(*self.treeview_pedidos.get_children())

        for pedido in pedidos:
            # cliente está disponible porque seguimos dentro de la sesión
            cliente_nombre = pedido.cliente.nombre if pedido.cliente else "Desconocido"
            fecha = pedido.descripcion if pedido.descripcion else ""
            self.treeview_pedidos.insert("", "end", iid=pedido.id, values=(pedido.id, cliente_nombre, fecha))

        session.close()


    def subir_pedido(self):
        seleccion = self.treeview_pedidos.selection()
        if not seleccion:
            return

        item = seleccion[0]
        index = self.treeview_pedidos.index(item)
        if index > 0:
            self.treeview_pedidos.move(item, self.treeview_pedidos.parent(item), index - 1)

    def bajar_pedido(self):
        seleccion = self.treeview_pedidos.selection()
        if not seleccion:
            return

        item = seleccion[0]
        index = self.treeview_pedidos.index(item)
        total = len(self.treeview_pedidos.get_children())
        if index < total - 1:
            self.treeview_pedidos.move(item, self.treeview_pedidos.parent(item), index + 1)

        
    def crear_ingrediente(self):
        nombre = self.entry_nombre.get()
        tipo = self.entry_tipo.get()
        cantidad = self.entry_cantidad.get()
        unidad = self.entry_unidad.get()

        if nombre and tipo and cantidad and unidad:
            try:
                cantidad = int(cantidad)
            except ValueError:
                messagebox.showwarning("Error", "La cantidad debe ser un número entero.")
                return

            session = get_session()  # <-- usa sesión aquí
            ingrediente = IngredienteCRUD.crear_ingrediente(session, nombre, tipo, cantidad, unidad)
            session.close()

            if ingrediente:
                self.treeview_ingredientes.insert("", "end", values=(
                    ingrediente.nombre, ingrediente.tipo, ingrediente.cantidad, ingrediente.unidad_de_medida))
            else:
                messagebox.showwarning("Duplicado", "Este ingrediente ya existe.")
        else:
            messagebox.showwarning("Error", "Por favor, ingrese todos los campos.")



    def crear_menu(self):
        nombre_menu = self.entry_nombre_menu.get().strip()
        indices = self.ingredientes_listbox.curselection()
        if not nombre_menu or not indices:
            messagebox.showwarning("Error",
                                "Ingrese el nombre y seleccione ingredientes.")
            return

        ingredientes = [self.ingredientes_opciones[i] for i in indices]
        session = get_session()
        nuevo_menu = MenuCRUD.crear_menu_con_ingredientes(session,
                                                        nombre_menu,
                                                        ingredientes)
        session.close()

        if nuevo_menu is None:
            messagebox.showwarning("Error", "Ya existe un menú con ese nombre.")
            return

        # Refrescamos todo (más seguro que insertar manualmente)
        self.cargar_menus_en_treeview()

        # Y actualizamos los labels de detalle
        self.label_detalle_nombre.configure(
            text=f"Nombre del menú: {nuevo_menu.nombre_menu}"
        )
        self.label_detalle_ingredientes.configure(
            text="Ingredientes: " + ", ".join(i.nombre for i in ingredientes)
        )
    def cargar_menus_en_combobox(self):
        session = get_session()
        menus = MenuCRUD.obtener_todos_menus(session)
        session.close()

        self.menus_opciones = menus
        self.menu_combobox.configure(values=[menu.nombre_menu for menu in menus])

        
    def cargar_clientes_para_panel_de_compra(self):
        session = get_session()
        clientes = ClienteCRUD.obtener_todos_clientes(session)
        session.close()

        self.clientes_opciones = clientes
        self.cliente_combobox.configure(values=[cliente.email for cliente in clientes])

            
    def crear_pedido_desde_panel(self):
        menu_nombre = self.menu_combobox.get()
        cliente_email = self.cliente_combobox.get()

        if not menu_nombre or not cliente_email:
            messagebox.showwarning("Error", "Debe seleccionar un cliente y un menú.")
            return

        # Buscar objetos
        menu = next((m for m in self.menus_opciones if m.nombre_menu == menu_nombre), None)
        cliente = next((c for c in self.clientes_opciones if c.email == cliente_email), None)

        if not menu or not cliente:
            messagebox.showwarning("Error", "Menú o cliente inválido.")
            return

        from datetime import datetime
        descripcion = f"Pedido generado el {datetime.now().strftime('%Y-%m-%d %H:%M')}"

        session = get_session()
        pedido = PedidoCRUD.crear_pedido(session, cliente_email, descripcion, [menu.id_menu])
        session.close()

        if pedido:
            ingredientes = ", ".join(i.nombre for i in menu.ingrediente)
            self.treeview_compra.insert("", "end", values=(cliente.nombre, menu.nombre_menu, ingredientes))
        else:
            messagebox.showerror("Error", "No se pudo crear el pedido.")
        from boleta import BoletaPDF  # asegúrate de importar esto al principio del archivo

        # Generar la boleta PDF
        pdf = BoletaPDF()
        archivo_pdf = pdf.generar_boleta(pedido, cliente, menu, menu.ingrediente)

        messagebox.showinfo("Boleta generada", f"Boleta creada: {archivo_pdf}")


           
    def crear_cliente(self):
        nombre = self.entry_nombre_cliente.get()
        email = self.entry_email_cliente.get()
        if nombre and email:
            session = get_session()
            cliente = ClienteCRUD.crear_cliente(session, nombre, email)
            session.close()
            if cliente:
                self.treeview_clientes.insert("", "end", values=(cliente.nombre, cliente.email))
                self.cargar_clientes()  # Para actualizar el Combobox de emails en los pedidos
            else:
                messagebox.showwarning("Duplicado", "Ya existe un cliente con ese email.")
        else:
            messagebox.showwarning("Error", "Por favor, ingrese todos los campos.")


    def crear_pedido(self):
        cliente_email = self.combobox_cliente_email.get()
        descripcion = self.entry_descripcion_pedido.get()
        if cliente_email and descripcion:
            session = get_session()
            cliente = ClienteCRUD.obtener_cliente_por_email(session, cliente_email)
            pedido = PedidoCRUD.crear_pedido(session, cliente, descripcion)
            session.close()
            self.treeview_pedidos.insert("", "end", values=(cliente.nombre, pedido.descripcion, pedido.fecha))
        else:
            messagebox.showwarning("Error", "Por favor, ingrese todos los campos.")

    def cargar_clientes(self):
        # Usar la sesión directamente sin 'with'
        session = get_session()  # Obtener sesión de la base de datos
        clientes = ClienteCRUD.obtener_todos_clientes(session)
        
        # Poblar el combobox con los emails de los clientes
        clientes_emails = [cliente.email for cliente in clientes]
        self.combobox_cliente_email['values'] = clientes_emails

        # Cerrar la sesión cuando ya no se necesita
        session.close()



if __name__ == "__main__":
    app = App()
    app.mainloop()
