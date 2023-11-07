class Client:
    def __init__(self, name, cpf, rg):
        self.name = name
        self.cpf = cpf
        self.rg = rg
    
    def get_name(self):
        return self.name
    
    def get_cpf(self):
        return self.cpf
    def get_rg(self):
        return self.rg
    
    def set_name(self, name):
        self.name = name
    
    def set_cpf(self, cpf):
        self.cpf = cpf
    
    def set_rg(self, rg):
        self.rg = rg
