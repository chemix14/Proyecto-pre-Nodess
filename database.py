from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# 1. Configuración de la conexión (SQLite)
SQLALCHEMY_DATABASE_URL = "sqlite:///./nodess_prenodes.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 2. Tablas Intermedias (Para relaciones Muchos a Muchos)
# Un proyecto puede tener muchas instituciones y viceversa
proyecto_institucion = Table(
    'proyecto_institucion', Base.metadata,
    Column('proyecto_id', Integer, ForeignKey('proyectos.id')),
    Column('institucion_id', Integer, ForeignKey('instituciones.id'))
)

# 3. Modelos de la Base de Datos

class Institucion(Base):
    __tablename__ = "instituciones"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    # Ejemplo: 'Educativa', 'Gobierno', 'OSSE'
    tipo = Column(String) 
    logo_url = Column(String, nullable=True) # Para futuras imágenes

    # Relación con proyectos
    proyectos = relationship("Proyecto", secondary=proyecto_institucion, back_populates="participantes")

class Municipio(Base):
    __tablename__ = "municipios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, nullable=False)
    estado = Column(String, default="Puebla")

class Proyecto(Base):
    __tablename__ = "proyectos"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, nullable=False)
    descripcion = Column(Text)
    municipio_trabajo = Column(String) # O podrías hacer relación con Municipio
    
    # Relación Muchos a Muchos
    participantes = relationship("Institucion", secondary=proyecto_institucion, back_populates="proyectos")

class Contacto(Base):
    __tablename__ = "contacto_info"
    id = Column(Integer, primary_key=True, index=True)
    correo = Column(String, default="deagro@teziutlan.tecnm.mx")
    telefono = Column(String, nullable=True)

# 4. Tabla de Administrador
class AdminUser(Base):
    __tablename__ = "admin_users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

# 5. Función para crear las tablas en el archivo .db
def create_db():
    Base.metadata.create_all(bind=engine)