# src/main/infraestructure/db/models/__init__.py

# Importar en este orden para asegurar que las dependencias se registren
from .User import User
from .Course import Course
from .CModule import CModule
from .Topic import TopicType, Topic

# Esto fuerza a que todas las clases se carguen en el registry de SQLAlchemy
# antes de que se intente crear la sesión o las tablas.
__all__ = ["User", "Course", "CModule", "TopicType", "Topic"]