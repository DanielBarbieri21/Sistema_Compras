"""
Validadores para o Sistema de Compras
"""
import re
from typing import List, Optional
from config import VALIDATION_CONFIG


class Validator:
    """Classe base para validadores"""
    
    @staticmethod
    def validate_required(value: str, field_name: str) -> Optional[str]:
        """Valida se um campo obrigatório foi preenchido"""
        if not value or not value.strip():
            return f"{field_name} é obrigatório"
        return None
    
    @staticmethod
    def validate_length(value: str, min_length: int, max_length: int, field_name: str) -> Optional[str]:
        """Valida o comprimento de um campo"""
        if not value:
            return None
        
        length = len(value.strip())
        if length < min_length:
            return f"{field_name} deve ter pelo menos {min_length} caracteres"
        if length > max_length:
            return f"{field_name} deve ter no máximo {max_length} caracteres"
        return None
    
    @staticmethod
    def validate_numeric(value: str, field_name: str, min_value: float = None, max_value: float = None) -> Optional[str]:
        """Valida se um valor é numérico e está dentro dos limites"""
        if not value:
            return f"{field_name} é obrigatório"
        
        try:
            num_value = float(value.replace(',', '.'))
            
            if min_value is not None and num_value < min_value:
                return f"{field_name} deve ser maior ou igual a {min_value}"
            
            if max_value is not None and num_value > max_value:
                return f"{field_name} deve ser menor ou igual a {max_value}"
                
        except ValueError:
            return f"{field_name} deve ser um número válido"
        
        return None
    
    @staticmethod
    def validate_integer(value: str, field_name: str, min_value: int = None, max_value: int = None) -> Optional[str]:
        """Valida se um valor é inteiro e está dentro dos limites"""
        if not value:
            return f"{field_name} é obrigatório"
        
        try:
            int_value = int(value)
            
            if min_value is not None and int_value < min_value:
                return f"{field_name} deve ser maior ou igual a {min_value}"
            
            if max_value is not None and int_value > max_value:
                return f"{field_name} deve ser menor ou igual a {max_value}"
                
        except ValueError:
            return f"{field_name} deve ser um número inteiro válido"
        
        return None


class CNPJValidator:
    """Validador específico para CNPJ"""
    
    @staticmethod
    def validate_cnpj(cnpj: str) -> Optional[str]:
        """Valida CNPJ usando algoritmo oficial"""
        if not cnpj:
            return "CNPJ é obrigatório"
        
        # Remove caracteres não numéricos
        cnpj = re.sub(r'[^0-9]', '', cnpj)
        
        # Verifica se tem 14 dígitos
        if len(cnpj) != 14:
            return "CNPJ deve ter 14 dígitos"
        
        # Verifica se todos os dígitos são iguais
        if cnpj == cnpj[0] * 14:
            return "CNPJ inválido"
        
        # Validação do primeiro dígito verificador
        soma = 0
        peso = 5
        for i in range(12):
            soma += int(cnpj[i]) * peso
            peso = 9 if peso == 2 else peso - 1
        
        resto = soma % 11
        dv1 = 0 if resto < 2 else 11 - resto
        
        if int(cnpj[12]) != dv1:
            return "CNPJ inválido"
        
        # Validação do segundo dígito verificador
        soma = 0
        peso = 6
        for i in range(13):
            soma += int(cnpj[i]) * peso
            peso = 9 if peso == 2 else peso - 1
        
        resto = soma % 11
        dv2 = 0 if resto < 2 else 11 - resto
        
        if int(cnpj[13]) != dv2:
            return "CNPJ inválido"
        
        return None


class ItemValidator:
    """Validador específico para itens"""
    
    @staticmethod
    def validate_item_data(description: str, code: str, brand: str, 
                          supplier: str, price: str, quantity: str) -> List[str]:
        """Valida todos os dados de um item"""
        errors = []
        
        # Validar descrição
        desc_error = Validator.validate_length(
            description, 
            VALIDATION_CONFIG['min_description_length'],
            VALIDATION_CONFIG['max_description_length'],
            "Descrição"
        )
        if desc_error:
            errors.append(desc_error)
        
        # Validar código
        code_error = Validator.validate_length(
            code,
            VALIDATION_CONFIG['min_code_length'],
            VALIDATION_CONFIG['max_code_length'],
            "Código"
        )
        if code_error:
            errors.append(code_error)
        
        # Validar fornecedor
        supplier_error = Validator.validate_required(supplier, "Fornecedor")
        if supplier_error:
            errors.append(supplier_error)
        
        # Validar preço
        price_error = Validator.validate_numeric(
            price,
            "Preço",
            VALIDATION_CONFIG['min_price'],
            VALIDATION_CONFIG['max_price']
        )
        if price_error:
            errors.append(price_error)
        
        # Validar quantidade
        quantity_error = Validator.validate_numeric(
            quantity,
            "Quantidade",
            VALIDATION_CONFIG['min_quantity'],
            VALIDATION_CONFIG['max_quantity']
        )
        if quantity_error:
            errors.append(quantity_error)
        
        return errors


class CompanyValidator:
    """Validador específico para empresas"""
    
    @staticmethod
    def validate_company_data(name: str, cnpj: str, buyer_name: str) -> List[str]:
        """Valida todos os dados de uma empresa"""
        errors = []
        
        # Validar nome
        name_error = Validator.validate_required(name, "Nome da empresa")
        if name_error:
            errors.append(name_error)
        
        # Validar CNPJ
        cnpj_error = CNPJValidator.validate_cnpj(cnpj)
        if cnpj_error:
            errors.append(cnpj_error)
        
        # Validar nome do comprador
        buyer_error = Validator.validate_required(buyer_name, "Nome do comprador")
        if buyer_error:
            errors.append(buyer_error)
        
        return errors


class SupplierValidator:
    """Validador específico para fornecedores"""
    
    @staticmethod
    def validate_supplier_data(name: str, cnpj: str, seller_name: str) -> List[str]:
        """Valida todos os dados de um fornecedor"""
        errors = []
        
        # Validar nome
        name_error = Validator.validate_required(name, "Nome do fornecedor")
        if name_error:
            errors.append(name_error)
        
        # Validar CNPJ
        cnpj_error = CNPJValidator.validate_cnpj(cnpj)
        if cnpj_error:
            errors.append(cnpj_error)
        
        # Validar nome do vendedor
        seller_error = Validator.validate_required(seller_name, "Nome do vendedor")
        if seller_error:
            errors.append(seller_error)
        
        return errors


class ExcelValidator:
    """Validador para dados importados do Excel"""
    
    @staticmethod
    def validate_excel_row(row_data: tuple) -> List[str]:
        """Valida uma linha de dados do Excel"""
        errors = []
        
        if len(row_data) < 6:
            errors.append("Linha deve ter pelo menos 6 colunas")
            return errors
        
        description, code, brand, supplier, price, quantity = row_data[:6]
        
        # Validar dados básicos
        item_errors = ItemValidator.validate_item_data(
            str(description) if description else "",
            str(code) if code else "",
            str(brand) if brand else "",
            str(supplier) if supplier else "",
            str(price) if price else "",
            str(quantity) if quantity else ""
        )
        
        errors.extend(item_errors)
        
        return errors



