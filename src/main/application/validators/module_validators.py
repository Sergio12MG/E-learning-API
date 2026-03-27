from src.main.domain.output_ports.module_ports import ModuleRepository
from src.main.domain.exceptions import Module_NotFound_Error, ParentModule_NotFound_Error

class Module_Validator():
    def __init__(self, repository: ModuleRepository):
        self.repository = repository

    def check_parent_module(self, parent_id: int):
        parent = self.repository.find_by_id(parent_id)

        if parent is None:
            raise ParentModule_NotFound_Error(f"Módulo inexistente: No se encuentra con el ID {parent_id}.")
        
        return parent
    
    def find_id(self, module_id: int):
        module = self.repository.find_by_id(module_id)

        if module is None:
            raise Module_NotFound_Error(f"Módulo no encontrado con el ID {module_id}.")
        
        return module
    
    def find_title(self, title: str):
        module = self.repository.find_by_title(title)

        if module is None:
            raise Module_NotFound_Error(f"Módulo no encontrado con el título {title}.")
        
        return module
    
    