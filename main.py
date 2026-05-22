import uvicorn
from fastapi import FastAPI, Request, Depends, Form, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from starlette.middleware.sessions import SessionMiddleware
from passlib.context import CryptContext

# Importamos todo desde nuestro archivo database.py
from database import SessionLocal, engine, Base, Institucion, Municipio, Proyecto, Contacto, AdminUser

# 1. Crear las tablas en la base de datos al iniciar
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Configuración de Sesiones
app.add_middleware(SessionMiddleware, secret_key="super_secret_key_change_in_production")

# Configuración de Hashes de Contraseña
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 2. Configurar la carpeta donde estarán tus archivos HTML
templates = Jinja2Templates(directory="templates")

# 3. Función para abrir y cerrar la conexión a la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Dependencia de Autenticación
def get_current_user(request: Request):
    user = request.session.get("user")
    if not user:
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            headers={"Location": "/login"}
        )
    return user

# --- RUTAS DE ADMINISTRACIÓN Y LOGIN ---

@app.get("/login")
def login_page(request: Request):
    if request.session.get("user"):
        return RedirectResponse(url="/admin", status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse(request=request, name="login.html", context={"request": request})

@app.post("/login")
def login_post(request: Request, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(AdminUser).filter(AdminUser.username == username).first()
    if not user or not pwd_context.verify(password, user.hashed_password):
        return templates.TemplateResponse(
            request=request, 
            name="login.html", 
            context={"request": request, "error": "Usuario o contraseña incorrectos"}
        )
    request.session["user"] = username
    return RedirectResponse(url="/admin", status_code=status.HTTP_302_FOUND)

@app.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)

@app.get("/admin")
def admin_dashboard(request: Request, user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    return templates.TemplateResponse(request=request, name="admin.html", context={
        "request": request, 
        "user": user,
        "instituciones": db.query(Institucion).all(),
        "municipios": db.query(Municipio).all(),
        "proyectos": db.query(Proyecto).all(),
        "contacto": db.query(Contacto).first()
    })

@app.post("/admin/delete/{table}/{id}")
def delete_record(table: str, id: int, request: Request, user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    model = {"instituciones": Institucion, "municipios": Municipio, "proyectos": Proyecto}.get(table)
    if model:
        record = db.query(model).filter(model.id == id).first()
        if record:
            db.delete(record)
            db.commit()
    return RedirectResponse(url=f"/admin?tab={table}", status_code=status.HTTP_302_FOUND)

@app.post("/admin/add/instituciones")
def add_institucion(request: Request, nombre: str = Form(...), tipo: str = Form(...), user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    db.add(Institucion(nombre=nombre, tipo=tipo))
    db.commit()
    return RedirectResponse(url="/admin?tab=instituciones", status_code=status.HTTP_302_FOUND)

@app.post("/admin/add/municipios")
def add_municipio(request: Request, nombre: str = Form(...), estado: str = Form("Puebla"), user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    db.add(Municipio(nombre=nombre, estado=estado))
    db.commit()
    return RedirectResponse(url="/admin?tab=municipios", status_code=status.HTTP_302_FOUND)

@app.post("/admin/add/proyectos")
def add_proyecto(request: Request, titulo: str = Form(...), descripcion: str = Form(...), municipio_trabajo: str = Form(...), user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    db.add(Proyecto(titulo=titulo, descripcion=descripcion, municipio_trabajo=municipio_trabajo))
    db.commit()
    return RedirectResponse(url="/admin?tab=proyectos", status_code=status.HTTP_302_FOUND)

@app.post("/admin/contacto")
def update_contacto(request: Request, correo: str = Form(...), telefono: str = Form(...), user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    contacto = db.query(Contacto).first()
    if contacto:
        contacto.correo = correo
        contacto.telefono = telefono
    else:
        db.add(Contacto(correo=correo, telefono=telefono))
    db.commit()
    return RedirectResponse(url="/admin?tab=contacto", status_code=status.HTTP_302_FOUND)

# --- RUTAS DE LAS PÁGINAS INDIVIDUALES ---

@app.get("/")
def inicio(request: Request):
    # La página principal (Hero image y bienvenida)
    return templates.TemplateResponse(request=request, name="index.html", context={"request": request})

@app.get("/acerca-de")
def acerca_de(request: Request, db: Session = Depends(get_db)):
    # Aquí mandamos los municipios (Zonas de trabajo)
    municipios = db.query(Municipio).all()
    return templates.TemplateResponse(request=request, name="acerca.html", context={"request": request, "municipios": municipios})

@app.get("/proyectos")
def proyectos(request: Request, db: Session = Depends(get_db)):
    # Aquí mandaremos los proyectos cuando los registres
    proyectos = db.query(Proyecto).all()
    return templates.TemplateResponse(request=request, name="proyectos.html", context={"request": request, "proyectos": proyectos})

@app.get("/investigadores")
def investigadores(request: Request):
    # Página para semblanzas, roles y estudiantes (Guía de registro)
    return templates.TemplateResponse(request=request, name="investigadores.html", context={"request": request})

@app.get("/alianzas")
def alianzas(request: Request, db: Session = Depends(get_db)):
    # Aquí mandamos a los participantes (TecNM, Sabana, Ayuntamiento, etc.)
    instituciones = db.query(Institucion).all()
    return templates.TemplateResponse(request=request, name="alianzas.html", context={"request": request, "instituciones": instituciones})

@app.get("/vinculacion")
def vinculacion(request: Request):
    # Página para Red de investigación, Divulgación y Galería
    return templates.TemplateResponse(request=request, name="vinculacion.html", context={"request": request})

@app.get("/contacto")
def contacto(request: Request, db: Session = Depends(get_db)):
    # Aquí mandamos el correo y teléfono
    contacto_info = db.query(Contacto).first()
    return templates.TemplateResponse(request=request, name="contacto.html", context={"request": request, "contacto": contacto_info})

# --- RUTA DE CARGA AUTOMÁTICA (Para llenar tu base de datos rápido) ---

@app.get("/init-db")
def inicializar_base_datos(db: Session = Depends(get_db)):
    # Crear usuario administrador si no existe
    if not db.query(AdminUser).first():
        db.add(AdminUser(username="admin", hashed_password=pwd_context.hash("admin123")))
        db.commit()

    # Verificamos si ya hay datos para no duplicarlos
    if db.query(Institucion).first():
        return {"mensaje": "La base de datos ya tiene información. Ve a la ruta '/' para ver la página."}
    
    # Lista de Instituciones (Participantes)
    lista_instituciones = [
        Institucion(nombre="TecNM Campus Teziutlán", tipo="Institución Educativa"),
        Institucion(nombre="TecNM Campus Puebla", tipo="Institución Educativa"),
        Institucion(nombre="TecNM Campus Minatitlán", tipo="Institución Educativa"),
        Institucion(nombre="CICATA-IPN, Unidad Legaria", tipo="Institución Educativa"),
        Institucion(nombre="Universidad de la Sabana, Colombia", tipo="Institución Educativa"),
        Institucion(nombre="H. Ayuntamiento Municipal de Tenampulco", tipo="Instancia de Gobierno"),
        Institucion(nombre="Sociedad Cooperativa Sabores de Calpan S.C.", tipo="OSSE")
    ]
    db.add_all(lista_instituciones)

    # Lista de Municipios
    lista_municipios = [
        Municipio(nombre="Tenampulco"),
        Municipio(nombre="San Andrés Calpan"),
        Municipio(nombre="Teziutlán")
    ]
    db.add_all(lista_municipios)

    # Contacto
    nuevo_contacto = Contacto(correo="deagro@teziutlan.tecnm.mx", telefono="N/A")
    db.add(nuevo_contacto)

    # Guardar los cambios
    db.commit()
    return {"mensaje": "¡Datos del Pre-NODESS cargados exitosamente! Ya puedes ir a localhost:8000/"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)