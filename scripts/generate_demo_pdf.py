import os
from pathlib import Path

from models import ItemRepository, CompanyRepository, Item
from models.company import Company

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def ensure_demo_data():
    company = CompanyRepository.get_default()
    if not company:
        CompanyRepository.create(Company(name='Empresa Demo', cnpj='11222333000181', buyer_name='Comprador Demo'))
        company = CompanyRepository.get_default()

    items = ItemRepository.get_all()
    if not items:
        ItemRepository.create(
            Item(
                description='Parafuso', code='P001', brand='ABC',
                status='A Comprar', quantity=10, suppliers_prices={'Fornecedor A': 5.5}
            )
        )
        items = ItemRepository.get_all()

    return company, items


def generate_pdf(output_path: Path):
    company, items = ensure_demo_data()

    c = canvas.Canvas(str(output_path), pagesize=letter)
    c.drawString(100, 750, 'Pedido Demo')
    c.drawString(100, 730, f'Empresa: {company.name} - CNPJ: {company.cnpj}')
    c.drawString(100, 710, f'Comprador: {company.buyer_name}')

    y = 690
    for it in items:
        prices = ', '.join([f"{s}: R${p:.2f}" for s, p in it.suppliers_prices.items()]) if it.suppliers_prices else 'Sem preços'
        line = f'I: {it.description}  Cdg: {it.code}  M: {it.brand}  Qtd: {it.quantity}  Prç: {prices}'
        c.drawString(100, y, line)
        y -= 20
        if y < 100:
            c.showPage()
            y = 750
    c.save()


if __name__ == '__main__':
    out = Path(os.getcwd()) / 'pedido_demo.pdf'
    generate_pdf(out)
    print(f'OK: pedido_demo.pdf gerado em {out}')


