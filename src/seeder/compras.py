"""Seed de Compras — fornecedores, insumos e pedidos (teste ponta a ponta)."""

from sqlalchemy.orm import Session

from src.compras.fornecedor import repository as fornecedor_repository
from src.compras.fornecedor.dtos import FornecedorCreate
from src.compras.fornecedor.service import criar_fornecedor
from src.compras.insumo import repository as insumo_repository
from src.compras.insumo.dtos import InsumoCreate
from src.compras.insumo.service import criar_insumo
from src.db import session_scope


def executar_seeder_compras() -> dict[str, int]:
    contagem = {"fornecedores": 0, "insumos": 0}

    with session_scope() as session:
        contagem["fornecedores"] = _seed_fornecedores(session)
        contagem["insumos"] = _seed_insumos(session)

    return contagem


def _seed_fornecedores(session: Session) -> int:
    existentes = fornecedor_repository.listar_todos(session)
    if existentes:
        return 0
    dados = [
        FornecedorCreate(nome="LabSupply Ltda", cnpj="11222333000181"),
        FornecedorCreate(nome="BioReagentes S.A.", cnpj="44555666000191"),
        FornecedorCreate(nome="MedInsumos Brasil", cnpj="77888999000101"),
    ]
    for dto in dados:
        criar_fornecedor(session, dto)
    return len(dados)


def _seed_insumos(session: Session) -> int:
    existentes = insumo_repository.listar_insumos(session)
    if existentes:
        return 0
    dados = [
        InsumoCreate(nome="Reagente Hematologia", finalidade="Hemograma completo"),
        InsumoCreate(nome="Reagente Bioquímica", finalidade="Dosagem de glicose e colesterol"),
        InsumoCreate(nome="Tubo de Coleta EDTA", finalidade="Coleta de sangue para hematologia"),
        InsumoCreate(nome="Ponteira 100µL", finalidade="Pipetagem de amostras"),
        InsumoCreate(nome="Lâmina de Microscopia", finalidade="Análise microscópica"),
    ]
    for dto in dados:
        criar_insumo(session, dto)
    return len(dados)


def main() -> None:
    contagem = executar_seeder_compras()
    print("Seed compras finalizado")
    for chave, valor in contagem.items():
        print(f"{chave}: {valor}")


if __name__ == "__main__":
    main()
