"""Competencia — o eixo de apuracao do faturamento (fase F4)."""

import uuid
from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import Date, DateTime, ForeignKey, Integer, Numeric, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.db import Base


class Competencia(Base):
    """Mes de apuracao, com estado.

    PK natural `DATE` (primeiro dia do mes), quebrando a convencao de UUID do
    repositorio de proposito: o lancamento guarda `competencia DATE`, que e ao
    mesmo tempo a FK e a dimensao de consulta. Com PK UUID seria preciso
    `competencia_id` E `competencia` denormalizada em cada lancamento — duas
    colunas para o mesmo fato, que podem divergir.

    E uma TABELA, e nao so uma coluna, porque fechamento exige estado, autor,
    instante e totais congelados. Sem isso nao existe "nao pode mais lancar em
    marco".
    """

    __tablename__ = "competencias"

    competencia: Mapped[date] = mapped_column(Date, primary_key=True)
    status: Mapped[str] = mapped_column(String(10), nullable=False, default="ABERTA")

    # Congelados no fechamento. O recebimento continua vivo depois, entao ele
    # NAO entra aqui.
    valor_faturado: Mapped[Decimal | None] = mapped_column(Numeric(14, 2), nullable=True)
    valor_glosado: Mapped[Decimal | None] = mapped_column(Numeric(14, 2), nullable=True)
    valor_liberado: Mapped[Decimal | None] = mapped_column(Numeric(14, 2), nullable=True)
    qtd_laudos: Mapped[int | None] = mapped_column(Integer, nullable=True)
    qtd_guias: Mapped[int | None] = mapped_column(Integer, nullable=True)
    qtd_lotes: Mapped[int | None] = mapped_column(Integer, nullable=True)

    criada_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    fechada_em: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    fechada_por_usuario_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("usuarios.id"), nullable=True
    )
    reaberta_em: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    justificativa: Mapped[str | None] = mapped_column(String(255), nullable=True)

    @property
    def aberta(self) -> bool:
        return self.status == "ABERTA"
