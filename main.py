import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import sqlite3
from datetime import datetime

def crear_tabla():
    conexion = sqlite3.connect("incidencias.db")
    conexion.execute("""
        CREATE TABLE IF NOT EXISTS incidencias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            equipo TEXT NOT NULL,
            descripcion TEXT NOT NULL,
            prioridad TEXT NOT NULL,
            estado TEXT NOT NULL,
            fecha_registro TEXT NOT NULL,
            tecnico_resuelve TEXT,
            fecha_resolucion TEXT
        )
    """)

    columnas = [f[1] for f in conexion.execute("PRAGMA table_info(incidencias)").fetchall()]
    if "tecnico_resuelve" not in columnas:
        conexion.execute("ALTER TABLE incidencias ADD COLUMN tecnico_resuelve TEXT")
    if "fecha_resolucion" not in columnas:
        conexion.execute("ALTER TABLE incidencias ADD COLUMN fecha_resolucion TEXT")

    conexion.commit()
    conexion.close()

crear_tabla()

ventana = tk.Tk()
ventana.title("Sistema de Registro de Incidencias 777")
ventana.geometry("960x740")
ventana.minsize(900, 580)
ventana.resizable(True, True)

# ---------- Paleta ----------
FONDO = "#EEF2F7"
FONDO_PANEL = "#FFFFFF"
FONDO_CAMPO = "#FFFFFF"
TEXTO = "#0F172A"
TEXTO_MEDIO = "#334155"
TEXTO_SECUNDARIO = "#94A3B8"
AZUL = "#2563EB"
AZUL_HOVER = "#1D4ED8"
AZUL_PRESIONADO = "#1E40AF"
BORDE_SUAVE = "#E2E8F0"
FONDO_SUAVE = "#F8FAFC"

ROJO = "#DC2626"
ROJO_HOVER = "#B91C1C"
VERDE = "#16A34A"
VERDE_HOVER = "#15803D"

COLOR_PENDIENTE = "#B45309"
BG_PENDIENTE = "#FEF3C7"
COLOR_PROCESO = "#4338CA"
BG_PROCESO = "#E0E7FF"
COLOR_RESUELTO = "#15803D"
BG_RESUELTO = "#DCFCE7"

COLOR_ALTA = "#B91C1C"
BG_ALTA = "#FEE2E2"
COLOR_MEDIA = "#B45309"
BG_MEDIA = "#FEF3C7"
COLOR_BAJA = "#15803D"
BG_BAJA = "#DCFCE7"

def color_estado(estado):
    return {
        "Pendiente":  (BG_PENDIENTE, COLOR_PENDIENTE),
        "En Proceso": (BG_PROCESO,   COLOR_PROCESO),
        "Resuelto":   (BG_RESUELTO,  COLOR_RESUELTO),
    }.get(estado, ("#E2E8F0", TEXTO_MEDIO))

def color_prioridad(prio):
    return {
        "Alta":  (BG_ALTA,  COLOR_ALTA),
        "Media": (BG_MEDIA, COLOR_MEDIA),
        "Baja":  (BG_BAJA,  COLOR_BAJA),
    }.get(prio, ("#E2E8F0", TEXTO_MEDIO))

ventana.configure(bg=FONDO)

estilo = ttk.Style(ventana)
estilo.theme_use("clam")

estilo.configure("TFrame", background=FONDO)
estilo.configure("TLabel", background=FONDO, foreground=TEXTO, font=("Segoe UI", 9))

estilo.configure("TEntry",
    fieldbackground=FONDO_CAMPO, foreground=TEXTO,
    insertcolor=AZUL, padding=8, borderwidth=0,
    relief="flat", bordercolor=BORDE_SUAVE,
    lightcolor=BORDE_SUAVE, darkcolor=BORDE_SUAVE,
    focuscolor=AZUL, insertwidth=2)
estilo.map("TEntry",
    bordercolor=[("focus", AZUL), ("!focus", BORDE_SUAVE)],
    lightcolor=[("focus", AZUL), ("!focus", BORDE_SUAVE)],
    darkcolor=[("focus", AZUL), ("!focus", BORDE_SUAVE)])

estilo.configure("TCombobox",
    fieldbackground=FONDO_CAMPO, background=FONDO_CAMPO,
    foreground=TEXTO, arrowcolor=TEXTO_MEDIO,
    padding=7, borderwidth=0, relief="flat",
    bordercolor=BORDE_SUAVE, lightcolor=BORDE_SUAVE, darkcolor=BORDE_SUAVE)
estilo.map("TCombobox",
    fieldbackground=[("readonly", FONDO_CAMPO)],
    foreground=[("readonly", TEXTO)],
    selectbackground=[("readonly", FONDO_CAMPO)],
    selectforeground=[("readonly", TEXTO)],
    bordercolor=[("focus", AZUL), ("!focus", BORDE_SUAVE)],
    lightcolor=[("focus", AZUL), ("!focus", BORDE_SUAVE)],
    darkcolor=[("focus", AZUL), ("!focus", BORDE_SUAVE)])

estilo.configure("TButton",
    background=FONDO_PANEL, foreground=TEXTO_MEDIO,
    padding=(14, 9), font=("Segoe UI", 9, "bold"),
    borderwidth=0, relief="flat", focuscolor=FONDO_PANEL)
estilo.map("TButton",
    background=[("active", "#EDF1F7"), ("pressed", "#E2E8F0")],
    foreground=[("active", TEXTO)])

estilo.configure("Primario.TButton",
    background=AZUL, foreground="#FFFFFF",
    padding=(16, 10), font=("Segoe UI", 9, "bold"),
    borderwidth=0, relief="flat", focuscolor=AZUL)
estilo.map("Primario.TButton",
    background=[("active", AZUL_HOVER), ("pressed", AZUL_PRESIONADO)],
    foreground=[("active", "#FFFFFF"), ("pressed", "#FFFFFF")])

estilo.configure("Secundario.TButton",
    background="#E0EAFB", foreground="#1E40AF",
    padding=(16, 10), font=("Segoe UI", 9, "bold"),
    borderwidth=0, relief="flat", focuscolor="#E0EAFB")
estilo.map("Secundario.TButton",
    background=[("active", "#D0DFF7"), ("pressed", "#C0D2F2")],
    foreground=[("active", "#1E40AF"), ("pressed", "#1E40AF")])

estilo.configure("Exito.TButton",
    background=VERDE, foreground="#FFFFFF",
    padding=(16, 10), font=("Segoe UI", 9, "bold"),
    borderwidth=0, relief="flat", focuscolor=VERDE)
estilo.map("Exito.TButton",
    background=[("active", VERDE_HOVER), ("pressed", "#166534")],
    foreground=[("active", "#FFFFFF"), ("pressed", "#FFFFFF")])

estilo.configure("Peligro.TButton",
    background="#FEE2E2", foreground=ROJO,
    padding=(16, 10), font=("Segoe UI", 9, "bold"),
    borderwidth=0, relief="flat", focuscolor="#FEE2E2")
estilo.map("Peligro.TButton",
    background=[("active", "#FECACA"), ("pressed", "#FCA5A5")],
    foreground=[("active", ROJO_HOVER), ("pressed", ROJO_HOVER)])

estilo.configure("Panel.TFrame", background=FONDO_PANEL)
estilo.configure("Panel.TLabel", background=FONDO_PANEL, foreground=TEXTO_MEDIO, font=("Segoe UI", 9, "bold"))

estilo.configure("Treeview",
    background=FONDO_PANEL, foreground=TEXTO,
    fieldbackground=FONDO_PANEL,
    font=("Segoe UI", 9), rowheight=32,
    borderwidth=0, relief="flat")
estilo.configure("Treeview.Heading", background="#F1F5F9", foreground="#334155", font=("Segoe UI", 9, "bold"), padding=(8, 8), relief="flat", borderwidth=0)
estilo.map("Treeview.Heading", background=[("active", "#E2E8F0")])
estilo.map("Treeview", background=[("selected", "#DBEAFE")], foreground=[("selected", "#1E40AF")])

contenedor_scroll = tk.Frame(ventana, bg=FONDO)
contenedor_scroll.pack(fill="both", expand=True)

canvas_principal = tk.Canvas(contenedor_scroll, bg=FONDO, highlightthickness=0)
barra_principal = ttk.Scrollbar(contenedor_scroll, orient="vertical", command=canvas_principal.yview)
canvas_principal.configure(yscrollcommand=barra_principal.set)

barra_principal.pack(side="right", fill="y")
canvas_principal.pack(side="left", fill="both", expand=True)

contenido_principal = tk.Frame(canvas_principal, bg=FONDO)
ventana_canvas = canvas_principal.create_window((0, 0), window=contenido_principal, anchor="nw")

contenido_principal.bind("<Configure>", lambda e: canvas_principal.configure(scrollregion=canvas_principal.bbox("all")))
canvas_principal.bind("<Configure>", lambda e: canvas_principal.itemconfigure(ventana_canvas, width=e.width))

def _scroll_rueda(evento): canvas_principal.yview_scroll(int(-1 * (evento.delta / 120)), "units")
def _activar_rueda(evento): canvas_principal.bind_all("<MouseWheel>", _scroll_rueda)
def _desactivar_rueda(evento): canvas_principal.unbind_all("<MouseWheel>")

canvas_principal.bind("<Enter>", _activar_rueda)
canvas_principal.bind("<Leave>", _desactivar_rueda)

titulo = tk.Label(contenido_principal, text="Registro de Incidencias", font=("Segoe UI", 22, "bold"), bg=FONDO, fg=TEXTO)
titulo.pack(pady=(24, 4))

subtitulo = tk.Label(contenido_principal, text="Centro de soporte técnico  ·  Sistema 777", font=("Segoe UI", 10), bg=FONDO, fg=TEXTO_SECUNDARIO)
subtitulo.pack(pady=(0, 18))

envoltorio_form = tk.Frame(contenido_principal, bg=FONDO)
envoltorio_form.pack(fill="x", padx=50, pady=(0, 28))

formulario = tk.Frame(envoltorio_form, bg=FONDO_PANEL, padx=32, pady=26)
formulario.pack(fill="x")

formulario.columnconfigure(0, weight=0, minsize=220)
formulario.columnconfigure(1, weight=1)

def label_panel(texto, fila, sticky="w"):
    lbl = tk.Label(formulario, text=texto,
        font=("Segoe UI", 9, "bold"),
        bg=FONDO_PANEL, fg=TEXTO_MEDIO)
    lbl.grid(row=fila, column=0, sticky=sticky, padx=(0, 18), pady=11)
    return lbl

label_panel("Nombre de quien reporta:", 0)
entrada_nombre = ttk.Entry(formulario)
entrada_nombre.grid(row=0, column=1, sticky="ew", pady=11, ipady=1)

label_panel("Equipo o dispositivo:", 1)
entrada_equipo = ttk.Entry(formulario)
entrada_equipo.grid(row=1, column=1, sticky="ew", pady=11, ipady=1)

label_panel("Descripción del problema:", 2, sticky="nw")

entrada_descripcion = tk.Text(formulario,
    height=5, font=("Segoe UI", 9),
    bg=FONDO_CAMPO, fg=TEXTO, insertbackground=AZUL, insertwidth=2,
    relief="flat", bd=0,
    highlightthickness=2,
    highlightbackground=BORDE_SUAVE,
    highlightcolor=AZUL,
    wrap="word", padx=12, pady=10)
entrada_descripcion.grid(row=2, column=1, sticky="ew", pady=11)

label_panel("Prioridad:", 3)
seleccion_prioridad = ttk.Combobox(formulario, values=["Alta", "Media", "Baja"], state="readonly")
seleccion_prioridad.grid(row=3, column=1, sticky="ew", pady=11, ipady=1)
seleccion_prioridad.set("Media")

label_panel("Estado:", 4)
seleccion_estado = ttk.Combobox(formulario, values=["Pendiente", "En Proceso", "Resuelto"], state="readonly")
seleccion_estado.grid(row=4, column=1, sticky="ew", pady=11, ipady=1)
seleccion_estado.set("Pendiente")

def registrar_incidencia():
    nombre = entrada_nombre.get().strip()
    equipo = entrada_equipo.get().strip()
    descripcion = entrada_descripcion.get("1.0", tk.END).strip()
    prioridad = seleccion_prioridad.get()
    estado = seleccion_estado.get()

    if not nombre or not equipo or not descripcion:
        messagebox.showerror("Error", "Por favor, complete todos los campos.")
        return

    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    tecnico = None
    fecha_res = None

    if estado == "Resuelto":
        tecnico = simpledialog.askstring(
            "Técnico que resuelve",
            "Ingresa el nombre del técnico que resuelve la incidencia:",
            parent=ventana)
        if not tecnico or not tecnico.strip():
            messagebox.showwarning("Cancelado",
                "No se registró: falta el técnico para un estado 'Resuelto'.")
            return
        tecnico = tecnico.strip()
        fecha_res = fecha

    try:
        with sqlite3.connect("incidencias.db") as conexion:
            cursor = conexion.execute("""
                INSERT INTO incidencias
                (nombre, equipo, descripcion, prioridad, estado, fecha_registro,
                 tecnico_resuelve, fecha_resolucion)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (nombre, equipo, descripcion, prioridad, estado, fecha,
                  tecnico, fecha_res))
            id_incidencia = cursor.lastrowid

        messagebox.showinfo("Incidencia guardada",
            f"Incidencia #(ID: {id_incidencia}) guardada correctamente")

        entrada_nombre.delete(0, tk.END)
        entrada_equipo.delete(0, tk.END)
        entrada_descripcion.delete("1.0", tk.END)
        seleccion_prioridad.set("Media")
        seleccion_estado.set("Pendiente")

    except sqlite3.Error as error:
        messagebox.showerror("Error", f"No se pudo guardar la incidencia: {error}")

def abrir_ventana_consulta():
    ventana_consulta = tk.Toplevel(ventana)
    ventana_consulta.title("Sistema 777 | Consultar incidencias")
    ventana_consulta.geometry("1180x700")
    ventana_consulta.minsize(950, 540)
    ventana_consulta.configure(bg=FONDO)

    contenedor_scroll_c = tk.Frame(ventana_consulta, bg=FONDO)
    contenedor_scroll_c.pack(fill="both", expand=True)

    canvas_c = tk.Canvas(contenedor_scroll_c, bg=FONDO, highlightthickness=0)
    barra_c = ttk.Scrollbar(contenedor_scroll_c, orient="vertical", command=canvas_c.yview)
    canvas_c.configure(yscrollcommand=barra_c.set)

    barra_c.pack(side="right", fill="y")
    canvas_c.pack(side="left", fill="both", expand=True)

    contenido = tk.Frame(canvas_c, bg=FONDO)
    ventana_canvas_c = canvas_c.create_window((0, 0), window=contenido, anchor="nw")

    contenido.bind("<Configure>", lambda e: canvas_c.configure(scrollregion=canvas_c.bbox("all")))
    canvas_c.bind("<Configure>", lambda e: canvas_c.itemconfigure(ventana_canvas_c, width=e.width))

    def _scroll_rueda_c(evento): canvas_c.yview_scroll(int(-1 * (evento.delta / 120)), "units")
    def _activar_rueda_c(evento): canvas_c.bind_all("<MouseWheel>", _scroll_rueda_c)
    def _desactivar_rueda_c(evento): canvas_c.unbind_all("<MouseWheel>")

    canvas_c.bind("<Enter>", _activar_rueda_c)
    canvas_c.bind("<Leave>", _desactivar_rueda_c)

    encabezado = tk.Frame(contenido, bg=FONDO)
    encabezado.pack(fill="x", padx=30, pady=(20, 14))

    tk.Label(encabezado, text="Consultar incidencias", font=("Segoe UI", 20, "bold"), bg=FONDO, fg=TEXTO).pack(anchor="w")
    tk.Label(encabezado, text="Consulta registros, busca reportes y gestiona su estado.",
        font=("Segoe UI", 9), bg=FONDO, fg=TEXTO_SECUNDARIO).pack(anchor="w", pady=(4, 0))

    panel_estadisticas = tk.Frame(contenido, bg=FONDO)
    panel_estadisticas.pack(fill="x", padx=30, pady=(0, 12))

    datos_tarjetas = [
        ("Total de incidencias", "#1D4ED8"),
        ("Pendientes",         "#B45309"),
        ("En proceso",         "#4338CA"),
        ("Resueltas",          "#15803D"),
    ]
    estadisticas = {}

    for columna, (nombre, color_numero) in enumerate(datos_tarjetas):
        tarjeta = tk.Frame(panel_estadisticas, bg=FONDO_PANEL)
        tarjeta.grid(row=0, column=columna, sticky="nsew", padx=5)
        barra = tk.Frame(tarjeta, bg=color_numero, width=4)
        barra.pack(side="left", fill="y")
        cuerpo = tk.Frame(tarjeta, bg=FONDO_PANEL, padx=12, pady=10)
        cuerpo.pack(side="left", fill="both", expand=True)
        tk.Label(cuerpo, text=nombre, bg=FONDO_PANEL, fg=TEXTO_SECUNDARIO, font=("Segoe UI", 8, "bold")).pack(anchor="w")
        etiqueta_numero = tk.Label(cuerpo, text="0", bg=FONDO_PANEL, fg=color_numero, font=("Segoe UI", 20, "bold"))
        etiqueta_numero.pack(anchor="w", pady=(4, 0))
        estadisticas[nombre] = etiqueta_numero

    for col in range(4):
        panel_estadisticas.columnconfigure(col, weight=1)

    def actualizar_estadisticas():
        try:
            with sqlite3.connect("incidencias.db") as conexion:
                total, pendientes, en_proceso, resueltas = conexion.execute("""
                    SELECT COUNT(*),
                        SUM(CASE WHEN estado='Pendiente' THEN 1 ELSE 0 END),
                        SUM(CASE WHEN estado='En Proceso' THEN 1 ELSE 0 END),
                        SUM(CASE WHEN estado='Resuelto' THEN 1 ELSE 0 END)
                    FROM incidencias
                """).fetchone()
            estadisticas["Total de incidencias"].config(text=total)
            estadisticas["Pendientes"].config(text=pendientes or 0)
            estadisticas["En proceso"].config(text=en_proceso or 0)
            estadisticas["Resueltas"].config(text=resueltas or 0)
        except sqlite3.Error as error:
            messagebox.showerror("Error",
                f"No se pudieron cargar las estadísticas: {error}",
                parent=ventana_consulta)

    actualizar_estadisticas()

    marco_busqueda = tk.Frame(contenido, bg=FONDO_PANEL, padx=18, pady=14)
    marco_busqueda.pack(fill="x", padx=30, pady=(0, 12))

    ttk.Label(marco_busqueda, text="Buscar por ID, nombre o equipo:", style="Panel.TLabel").grid(row=0, column=0, sticky="w", padx=(0, 10))
    entrada_busqueda = ttk.Entry(marco_busqueda)
    entrada_busqueda.grid(row=0, column=1, sticky="ew", padx=(0, 10), ipady=1)
    marco_busqueda.columnconfigure(1, weight=1)

    marco_tabla = tk.Frame(contenido, bg=FONDO_PANEL, padx=10, pady=10)
    marco_tabla.pack(fill="x", padx=30, pady=(0, 12))

    columnas = ("id", "nombre", "equipo", "descripcion", "prioridad", "estado", "fecha", "resuelto")
    tabla = ttk.Treeview(marco_tabla, columns=columnas, show="headings", height=8)

    tabla.heading("id", text="ID")
    tabla.heading("nombre", text="Reporta")
    tabla.heading("equipo", text="Equipo")
    tabla.heading("descripcion", text="Descripción")
    tabla.heading("prioridad", text="Prioridad")
    tabla.heading("estado", text="Estado")
    tabla.heading("fecha", text="Fecha de registro")
    tabla.heading("resuelto", text="Resuelto por")

    tabla.column("id", width=45, anchor="center")
    tabla.column("nombre", width=110)
    tabla.column("equipo", width=105)
    tabla.column("descripcion", width=200)
    tabla.column("prioridad", width=80, anchor="center")
    tabla.column("estado", width=95, anchor="center")
    tabla.column("fecha", width=130, anchor="center")
    tabla.column("resuelto", width=170, anchor="center")

    tabla.tag_configure("par", background="#F8FAFC")
    tabla.tag_configure("impar", background="#FFFFFF")

    barra_vertical = ttk.Scrollbar(marco_tabla, orient="vertical", command=tabla.yview)
    barra_horizontal = ttk.Scrollbar(marco_tabla, orient="horizontal", command=tabla.xview)
    tabla.configure(yscrollcommand=barra_vertical.set, xscrollcommand=barra_horizontal.set)
    tabla.grid(row=0, column=0, sticky="nsew")
    barra_vertical.grid(row=0, column=1, sticky="ns")
    barra_horizontal.grid(row=1, column=0, sticky="ew")

    marco_tabla.rowconfigure(0, weight=1)
    marco_tabla.columnconfigure(0, weight=1)

    def ver_detalle_con_datos(datos):
        detalle = tk.Toplevel(ventana_consulta)
        detalle.title(f"Sistema 777 | Incidencia #{datos[0]}")
        detalle.geometry("520x620")
        detalle.minsize(460, 520)
        detalle.configure(bg=FONDO)

        enc_det = tk.Frame(detalle, bg=FONDO)
        enc_det.pack(fill="x", padx=24, pady=(20, 14))

        tk.Label(enc_det, text=f"Incidencia #{datos[0]}", font=("Segoe UI", 18, "bold"), bg=FONDO, fg=TEXTO).pack(anchor="w")
        tk.Label(enc_det, text="Información completa del reporte", font=("Segoe UI", 9), bg=FONDO, fg=TEXTO_SECUNDARIO).pack(anchor="w", pady=(4, 0))

        badges = tk.Frame(enc_det, bg=FONDO)
        badges.pack(anchor="w", pady=(10, 0))

        bg_p, fg_p = color_prioridad(datos[4])
        badge_p = tk.Frame(badges, bg=bg_p, padx=10, pady=3)
        badge_p.pack(side="left", padx=(0, 6))
        tk.Label(badge_p, text=f"● {datos[4]}", bg=bg_p, fg=fg_p, font=("Segoe UI", 8, "bold")).pack()
        bg_e, fg_e = color_estado(datos[5])
        badge_e = tk.Frame(badges, bg=bg_e, padx=10, pady=3)
        badge_e.pack(side="left")
        tk.Label(badge_e, text=f"● {datos[5]}", bg=bg_e, fg=fg_e, font=("Segoe UI", 8, "bold")).pack()

        panel_detalle = tk.Frame(detalle, bg=FONDO_PANEL, padx=20, pady=16)
        panel_detalle.pack(fill="both", expand=True, padx=24, pady=(0, 14))

        campos = [
            ("Persona que reporta", datos[1]),
            ("Equipo", datos[2]),
            ("Descripción", datos[3]),
            ("Fecha de registro", datos[6]),
        ]

        for fila, (titulo_campo, valor) in enumerate(campos):
            tk.Label(panel_detalle, text=titulo_campo,
                font=("Segoe UI", 8, "bold"),
                bg=FONDO_PANEL, fg=TEXTO_SECUNDARIO).grid(
                    row=fila*2, column=0, sticky="w", pady=(6, 2))
            tk.Label(panel_detalle, text=str(valor),
                font=("Segoe UI", 9), bg=FONDO_PANEL, fg=TEXTO,
                justify="left", anchor="w", wraplength=420).grid(
                    row=fila*2+1, column=0, sticky="ew", pady=(0, 6))

        fila_actual = len(campos) * 2

        if datos[5] == "Resuelto" and datos[7]:
            tk.Label(panel_detalle, text="Resolución",
                font=("Segoe UI", 8, "bold"),
                bg=FONDO_PANEL, fg=TEXTO_SECUNDARIO).grid(
                    row=fila_actual, column=0, sticky="w", pady=(10, 2))
            bloque_res = tk.Frame(panel_detalle, bg=BG_RESUELTO, padx=12, pady=10)
            bloque_res.grid(row=fila_actual + 1, column=0, sticky="ew", pady=(0, 6))
            tk.Label(bloque_res, text=f"✓  {datos[7]}",
                font=("Segoe UI", 9, "bold"), bg=BG_RESUELTO,
                fg=COLOR_RESUELTO, anchor="w").pack(anchor="w")
            fecha_res = datos[7].split(" · ")[-1] if " · " in datos[7] else ""
            tk.Label(bloque_res, text=f"Fecha: {fecha_res}",
                font=("Segoe UI", 8), bg=BG_RESUELTO,
                fg=COLOR_RESUELTO, anchor="w").pack(anchor="w")

        panel_detalle.columnconfigure(0, weight=1)

        acciones = tk.Frame(detalle, bg=FONDO)
        acciones.pack(fill="x", padx=24, pady=(0, 20))

        def copiar_descripcion():
            detalle.clipboard_clear()
            detalle.clipboard_append(datos[3])
            messagebox.showinfo("Copiado",
                "Descripción copiada al portapapeles.", parent=detalle)

        def eliminar_detalle():
            if messagebox.askyesno("Confirmar eliminación",
                f"¿Eliminar la incidencia #{datos[0]} de {datos[1]}?\n\n"
                f"Esta acción no se puede deshacer.",
                parent=detalle, icon="warning"):
                try:
                    with sqlite3.connect("incidencias.db") as conexion:
                        conexion.execute("DELETE FROM incidencias WHERE id=?", (datos[0],))
                    detalle.destroy()
                    cargar_incidencias()
                    actualizar_estadisticas()
                    messagebox.showinfo("Eliminada",
                        f"Incidencia #{datos[0]} eliminada correctamente.",
                        parent=ventana_consulta)
                except sqlite3.Error as error:
                    messagebox.showerror("Error",
                        f"No se pudo eliminar: {error}", parent=detalle)

        def marcar_resuelto_detalle():
            if datos[5] == "Resuelto":
                messagebox.showinfo("Ya resuelta",
                    "Esta incidencia ya está marcada como resuelta.",
                    parent=detalle)
                return
            dlg = tk.Toplevel(detalle)
            dlg.title("Marcar como resuelta")
            dlg.geometry("360x210")
            dlg.configure(bg=FONDO)
            dlg.transient(detalle)
            dlg.grab_set()

            tk.Label(dlg, text="Técnico que resolvió:",
                font=("Segoe UI", 10, "bold"), bg=FONDO, fg=TEXTO).pack(
                anchor="w", padx=24, pady=(20, 8))
            entrada_tec = ttk.Entry(dlg)
            entrada_tec.pack(fill="x", padx=24, ipady=2)
            entrada_tec.focus_set()

            tk.Label(dlg, text=f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                font=("Segoe UI", 8, "italic"), bg=FONDO,
                fg=TEXTO_SECUNDARIO).pack(anchor="w", padx=24, pady=(6, 0))

            def confirmar_res():
                tecnico = entrada_tec.get().strip()
                if not tecnico:
                    messagebox.showwarning("Falta técnico",
                        "Ingresa el nombre del técnico.", parent=dlg)
                    return
                fecha_res = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                try:
                    with sqlite3.connect("incidencias.db") as conexion:
                        conexion.execute("""
                            UPDATE incidencias
                            SET estado='Resuelto', tecnico_resuelve=?, fecha_resolucion=?
                            WHERE id=?
                        """, (tecnico, fecha_res, datos[0]))
                    dlg.destroy()
                    detalle.destroy()
                    cargar_incidencias()
                    actualizar_estadisticas()
                except sqlite3.Error as error:
                    messagebox.showerror("Error",
                        f"No se pudo actualizar: {error}", parent=dlg)

            frame_btn = tk.Frame(dlg, bg=FONDO)
            frame_btn.pack(fill="x", padx=24, pady=(16, 20))
            ttk.Button(frame_btn, text="Cancelar",
                command=dlg.destroy).pack(side="right", padx=(8, 0))
            ttk.Button(frame_btn, text="Confirmar resolución",
                command=confirmar_res, style="Exito.TButton").pack(side="right")

        ttk.Button(acciones, text="Copiar descripción",
            command=copiar_descripcion).pack(side="left", padx=(0, 6))

        if datos[5] != "Resuelto":
            ttk.Button(acciones, text="Marcar resuelto",
                command=marcar_resuelto_detalle,
                style="Exito.TButton").pack(side="left", padx=(0, 6))

        ttk.Button(acciones, text="Eliminar",
            command=eliminar_detalle,
            style="Peligro.TButton").pack(side="left", padx=(0, 6))

        ttk.Button(acciones, text="Cerrar",
            command=detalle.destroy).pack(side="right")

    def ver_detalle():
        seleccion = tabla.selection()
        if not seleccion:
            messagebox.showwarning("Sin selección",
                "Primero selecciona una incidencia de la tabla.",
                parent=ventana_consulta)
            return
        datos = tabla.item(seleccion[0], "values")
        ver_detalle_con_datos(datos)

    marco_estado = tk.Frame(contenido, bg=FONDO_PANEL, padx=22, pady=18)
    marco_estado.pack(fill="x", padx=30, pady=(0, 22))

    encabezado_estado = tk.Frame(marco_estado, bg=FONDO_PANEL)
    encabezado_estado.grid(row=0, column=0, columnspan=5, sticky="ew", pady=(0, 12))

    tk.Label(encabezado_estado, text="Gestión de incidencia", font=("Segoe UI", 13, "bold"), bg=FONDO_PANEL, fg=TEXTO).pack(anchor="w")
    tk.Label(encabezado_estado, text="Selecciona una fila de la tabla para gestionarla.", font=("Segoe UI", 8), bg=FONDO_PANEL, fg=TEXTO_SECUNDARIO).pack( anchor="w", pady=(3, 0))

    info_seleccion = tk.Label(marco_estado, text="Ninguna incidencia seleccionada", font=("Segoe UI", 9, "italic"), bg=FONDO_PANEL, fg=TEXTO_SECUNDARIO, anchor="w")
    info_seleccion.grid(row=1, column=0, columnspan=5, sticky="w", pady=(0, 12))

    tk.Label(marco_estado, text="Cambiar estado:", font=("Segoe UI", 9, "bold"), bg=FONDO_PANEL, fg=TEXTO_MEDIO).grid(row=2, column=0, sticky="w", padx=(0, 12), pady=(0, 6))

    frame_combo_estado = tk.Frame(marco_estado, bg=FONDO_PANEL)
    frame_combo_estado.grid(row=3, column=0, sticky="w", padx=(0, 12))

    seleccion_nuevo_estado = ttk.Combobox(frame_combo_estado,
        values=["Pendiente", "En Proceso", "Resuelto"],
        state="readonly", width=22)
    seleccion_nuevo_estado.pack(side="left")
    seleccion_nuevo_estado.set("Pendiente")

    badge_estado = tk.Label(frame_combo_estado, text="  ● Pendiente  ", font=("Segoe UI", 8, "bold"), bg=BG_PENDIENTE, fg=COLOR_PENDIENTE)
    badge_estado.pack(side="left", padx=(8, 0))

    def actualizar_badge(evento=None):
        est = seleccion_nuevo_estado.get()
        bg, fg = color_estado(est)
        badge_estado.config(text=f"  ● {est}  ", bg=bg, fg=fg)

    seleccion_nuevo_estado.bind("<<ComboboxSelected>>", actualizar_badge)

    def pedir_tecnico_si_resuelto(nuevo_estado):
        """Devuelve (tecnico, fecha) si el estado es Resuelto, o (None, None)."""
        if nuevo_estado == "Resuelto":
            tecnico = simpledialog.askstring(
                "Técnico que resuelve",
                "Ingresa el nombre del técnico que resolvió:",
                parent=ventana_consulta)
            if not tecnico or not tecnico.strip():
                messagebox.showwarning("Cancelado",
                    "Para estado 'Resuelto' debes indicar el técnico.",
                    parent=ventana_consulta)
                return None, None
            return tecnico.strip(), datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return None, None

    def actualizar_estado():
        seleccion = tabla.selection()
        if not seleccion:
            messagebox.showwarning("Sin selección",
                "Primero selecciona una incidencia de la tabla.",
                parent=ventana_consulta)
            return
        nuevo_estado = seleccion_nuevo_estado.get()
        if not nuevo_estado:
            messagebox.showwarning("Estado requerido",
                "Selecciona el nuevo estado.", parent=ventana_consulta)
            return

        datos = tabla.item(seleccion[0], "values")
        id_incidencia = datos[0]

        tecnico, fecha_res = pedir_tecnico_si_resuelto(nuevo_estado)
        if nuevo_estado == "Resuelto" and tecnico is None:
            return

        try:
            with sqlite3.connect("incidencias.db") as conexion:
                if nuevo_estado == "Resuelto":
                    conexion.execute("""
                        UPDATE incidencias
                        SET estado=?, tecnico_resuelve=?, fecha_resolucion=?
                        WHERE id=?
                    """, (nuevo_estado, tecnico, fecha_res, id_incidencia))
                    nuevos_datos = list(datos)
                    nuevos_datos[5] = nuevo_estado
                    nuevos_datos[7] = f"{tecnico} · {fecha_res}"
                else:
                    conexion.execute("""
                        UPDATE incidencias
                        SET estado=?, tecnico_resuelve=NULL, fecha_resolucion=NULL
                        WHERE id=?
                    """, (nuevo_estado, id_incidencia))
                    nuevos_datos = list(datos)
                    nuevos_datos[5] = nuevo_estado
                    nuevos_datos[7] = ""

                tabla.item(seleccion[0], values=nuevos_datos)

            actualizar_estadisticas()
            actualizar_badge()
            al_seleccionar_fila()

            messagebox.showinfo("Estado actualizado",
                f"La incidencia #{id_incidencia} ahora está: {nuevo_estado}.",
                parent=ventana_consulta)
        except sqlite3.Error as error:
            messagebox.showerror("Error",
                f"No se pudo actualizar el estado: {error}",
                parent=ventana_consulta)
            
    def marcar_resuelto_rapido():
        seleccion = tabla.selection()
        if not seleccion:
            messagebox.showwarning("Sin selección",
                "Primero selecciona una incidencia de la tabla.",
                parent=ventana_consulta)
            return
        datos = tabla.item(seleccion[0], "values")
        if datos[5] == "Resuelto":
            messagebox.showinfo("Ya resuelta",
                f"La incidencia #{datos[0]} ya está resuelta.",
                parent=ventana_consulta)
            return

        dlg = tk.Toplevel(ventana_consulta)
        dlg.title("Marcar como resuelta")
        dlg.geometry("380x220")
        dlg.configure(bg=FONDO)
        dlg.transient(ventana_consulta)
        dlg.grab_set()

        tk.Label(dlg, text=f"Incidencia #{datos[0]}",
            font=("Segoe UI", 11, "bold"), bg=FONDO, fg=TEXTO).pack(
            anchor="w", padx=24, pady=(18, 2))
        tk.Label(dlg, text=f"{datos[1]}  ·  {datos[2]}",
            font=("Segoe UI", 8), bg=FONDO, fg=TEXTO_SECUNDARIO).pack(
            anchor="w", padx=24, pady=(0, 12))

        tk.Label(dlg, text="Técnico que resolvió:",
            font=("Segoe UI", 9, "bold"), bg=FONDO, fg=TEXTO_MEDIO).pack(
            anchor="w", padx=24, pady=(0, 4))
        entrada_tec = ttk.Entry(dlg)
        entrada_tec.pack(fill="x", padx=24, ipady=2)
        entrada_tec.focus_set()

        tk.Label(dlg, text=f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            font=("Segoe UI", 8, "italic"), bg=FONDO,
            fg=TEXTO_SECUNDARIO).pack(anchor="w", padx=24, pady=(6, 0))

        def confirmar():
            tecnico = entrada_tec.get().strip()
            if not tecnico:
                messagebox.showwarning("Falta técnico",
                    "Ingresa el nombre del técnico.", parent=dlg)
                return
            fecha_res = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            try:
                with sqlite3.connect("incidencias.db") as conexion:
                    conexion.execute("""
                        UPDATE incidencias
                        SET estado='Resuelto', tecnico_resuelve=?, fecha_resolucion=?
                        WHERE id=?
                    """, (tecnico, fecha_res, datos[0]))
                dlg.destroy()
                cargar_incidencias()
                actualizar_estadisticas()
                seleccion_nuevo_estado.set("Resuelto")
                actualizar_badge()
                messagebox.showinfo("Resuelta",
                    f"Incidencia #{datos[0]} marcada como resuelta por {tecnico}.",
                    parent=ventana_consulta)
            except sqlite3.Error as error:
                messagebox.showerror("Error",
                    f"No se pudo actualizar: {error}", parent=dlg)

        frame_btn = tk.Frame(dlg, bg=FONDO)
        frame_btn.pack(fill="x", padx=24, pady=(14, 18))
        ttk.Button(frame_btn, text="Cancelar", command=dlg.destroy).pack(
            side="right", padx=(8, 0))
        ttk.Button(frame_btn, text="Confirmar", command=confirmar,
            style="Exito.TButton").pack(side="right")

    def eliminar_seleccionada():
        seleccion = tabla.selection()
        if not seleccion:
            messagebox.showwarning("Sin selección",
                "Primero selecciona una incidencia de la tabla.",
                parent=ventana_consulta)
            return
        datos = tabla.item(seleccion[0], "values")
        if not messagebox.askyesno("Confirmar eliminación",
            f"¿Eliminar la incidencia #{datos[0]} de {datos[1]}?\n\n"
            f"Equipo: {datos[2]}\n"
            f"Esta acción no se puede deshacer.",
            parent=ventana_consulta, icon="warning"):
            return
        try:
            with sqlite3.connect("incidencias.db") as conexion:
                conexion.execute("DELETE FROM incidencias WHERE id=?", (datos[0],))
            cargar_incidencias()
            actualizar_estadisticas()
            info_seleccion.config(
                text="Ninguna incidencia seleccionada",
                fg=TEXTO_SECUNDARIO, font=("Segoe UI", 9, "italic"))
            messagebox.showinfo("Eliminada",
                f"Incidencia #{datos[0]} eliminada correctamente.",
                parent=ventana_consulta)
        except sqlite3.Error as error:
            messagebox.showerror("Error",
                f"No se pudo eliminar: {error}", parent=ventana_consulta)
            
    def al_seleccionar_fila(evento=None):
        seleccion = tabla.selection()
        if not seleccion:
            info_seleccion.config(
                text="Ninguna incidencia seleccionada",
                fg=TEXTO_SECUNDARIO, font=("Segoe UI", 9, "italic"))
            return
        datos = tabla.item(seleccion[0], "values")
        texto = f"Incidencia #{datos[0]}  ·  {datos[1]}  ·  {datos[2]}"
        if datos[5] == "Resuelto" and datos[7]:
            texto += f"  ·  Resuelta por {datos[7]}"
        info_seleccion.config(text=texto, fg=TEXTO, font=("Segoe UI", 9, "bold"))
        seleccion_nuevo_estado.set(datos[5])
        actualizar_badge()

    tabla.bind("<<TreeviewSelect>>", al_seleccionar_fila)
    tabla.bind("<Double-1>", lambda e: ver_detalle())

    ttk.Button(marco_estado, text="Guardar cambio", command=actualizar_estado, style="Primario.TButton").grid( row=3, column=1, sticky="w", padx=(0, 8))
    ttk.Button(marco_estado, text="✓  Marcar resuelto", command=marcar_resuelto_rapido, style="Exito.TButton").grid(row=3, column=2, sticky="w", padx=(0, 8))
    ttk.Button(marco_estado, text="Ver detalle", command=ver_detalle).grid(row=3, column=3, sticky="w", padx=(0, 8))
    ttk.Button(marco_estado, text="🗑  Eliminar", command=eliminar_seleccionada, style="Peligro.TButton").grid( row=3, column=4, sticky="w")
    sep = tk.Frame(marco_estado, bg=BORDE_SUAVE, height=1)
    sep.grid(row=4, column=0, columnspan=5, sticky="ew", pady=14)
    tk.Label(marco_estado, text="Consejo: doble clic en una fila abre el detalle con todas las acciones.", font=("Segoe UI", 8, "italic"), bg=FONDO_PANEL, fg=TEXTO_SECUNDARIO).grid( row=5, column=0, columnspan=5, sticky="w")
    marco_estado.columnconfigure(5, weight=1)

    def cargar_incidencias():
        for fila in tabla.get_children():
            tabla.delete(fila)
        try:
            with sqlite3.connect("incidencias.db") as conexion:
                registros = conexion.execute("""
                    SELECT id, nombre, equipo, descripcion,
                           prioridad, estado, fecha_registro,
                           tecnico_resuelve, fecha_resolucion
                    FROM incidencias ORDER BY id DESC
                """).fetchall()

            for i, r in enumerate(registros):
                # r = (id, nombre, equipo, desc, prio, estado, fecha, tecnico, fecha_res)
                tecnico = r[7]
                fecha_res = r[8]
                resumen_res = ""
                if r[5] == "Resuelto" and tecnico:
                    fecha_corta = fecha_res[:16] if fecha_res else ""
                    resumen_res = f"{tecnico} · {fecha_corta}" if fecha_corta else tecnico
                valores = (r[0], r[1], r[2], r[3], r[4], r[5], r[6], resumen_res)
                tag = "par" if i % 2 == 0 else "impar"
                tabla.insert("", tk.END, values=valores, tags=(tag,))

            if not registros:
                messagebox.showinfo("Sin incidencias",
                    "Todavía no hay incidencias registradas.",
                    parent=ventana_consulta)
        except sqlite3.Error as error:
            messagebox.showerror("Error",
                f"No se pudieron cargar las incidencias: {error}",
                parent=ventana_consulta)

    def buscar_incidencias():
        busqueda = entrada_busqueda.get().strip()
        if not busqueda:
            cargar_incidencias()
            return
        for fila in tabla.get_children():
            tabla.delete(fila)
        try:
            with sqlite3.connect("incidencias.db") as conexion:
                registros = conexion.execute("""
                    SELECT id, nombre, equipo, descripcion,
                           prioridad, estado, fecha_registro,
                           tecnico_resuelve, fecha_resolucion
                    FROM incidencias
                    WHERE CAST(id AS TEXT) LIKE ?
                       OR nombre LIKE ?
                       OR equipo LIKE ?
                    ORDER BY id ASC
                """, (f"%{busqueda}%", f"%{busqueda}%", f"%{busqueda}%")).fetchall()

            for i, r in enumerate(registros):
                tecnico = r[7]
                fecha_res = r[8]
                resumen_res = ""
                if r[5] == "Resuelto" and tecnico:
                    fecha_corta = fecha_res[:16] if fecha_res else ""
                    resumen_res = f"{tecnico} · {fecha_corta}" if fecha_corta else tecnico
                valores = (r[0], r[1], r[2], r[3], r[4], r[5], r[6], resumen_res)
                tag = "par" if i % 2 == 0 else "impar"
                tabla.insert("", tk.END, values=valores, tags=(tag,))

            if not registros:
                messagebox.showinfo("Sin resultados",
                    "No se encontraron incidencias.",
                    parent=ventana_consulta)
        except sqlite3.Error as error:
            messagebox.showerror("Error",
                f"No se pudo realizar la búsqueda: {error}",
                parent=ventana_consulta)

    ttk.Button(marco_busqueda, text="Buscar", command=buscar_incidencias, style="Primario.TButton").grid( row=0, column=2, padx=(0, 8))
    ttk.Button(marco_busqueda, text="Mostrar todos", command=cargar_incidencias, style="Secundario.TButton").grid(row=0, column=3)

    entrada_busqueda.bind("<Return>", lambda e: buscar_incidencias())
    cargar_incidencias()

ttk.Button(formulario, text="＋   Registrar incidencia", command=registrar_incidencia, style="Primario.TButton").grid( row=5, column=0, columnspan=2, sticky="ew", pady=(22, 8))
ttk.Button(formulario, text="Consultar incidencias", command=abrir_ventana_consulta, style="Secundario.TButton").grid( row=6, column=0, columnspan=2, sticky="ew", pady=8)

ventana.mainloop()