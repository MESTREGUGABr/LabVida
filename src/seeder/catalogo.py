"""Catálogo fixo do laboratório de demonstração.

Dados fictícios porém coerentes com a operação real: os códigos seguem o
formato TUSS (8 dígitos), cada procedimento carrega os analitos que o exame
mede, com faixa de referência e unidade — é o que permite gerar resultados
plausíveis e popular a tela de valores de referência.
"""

from dataclasses import dataclass
from decimal import Decimal

from src.atendimento.amostra.dtos import TipoMaterial
from src.cadastro.unidade.dtos import TipoUnidade


@dataclass(frozen=True)
class Analito:
    nome: str
    unidade: str
    minimo: float
    maximo: float


@dataclass(frozen=True)
class ProcedimentoCatalogo:
    codigo_tuss: str
    nome: str
    setor: str
    material: TipoMaterial
    valor_base: Decimal
    analitos: tuple[Analito, ...]


# --- Rede de unidades (1 central + 4 unidades de coleta) ---
UNIDADES: tuple[tuple[str, TipoUnidade, tuple[str, ...]], ...] = (
    (
        "Laboratório Central Garanhuns",
        TipoUnidade.CENTRAL,
        ("Recepção", "Triagem", "Hematologia", "Bioquímica", "Imunologia", "Microbiologia", "Urinálise"),
    ),
    ("Unidade de Coleta Centro", TipoUnidade.COLETA, ("Recepção", "Coleta")),
    ("Unidade de Coleta Heliópolis", TipoUnidade.COLETA, ("Recepção", "Coleta")),
    ("Unidade de Coleta São José", TipoUnidade.COLETA, ("Recepção", "Coleta")),
    ("Unidade de Coleta Boa Vista", TipoUnidade.COLETA, ("Recepção", "Coleta")),
)


# --- Convênios (nome, registro ANS) ---
CONVENIOS: tuple[tuple[str, str], ...] = (
    ("Unimed", "417033"),
    ("Bradesco Saúde", "005711"),
    ("Hapvida", "368253"),
    ("Amil", "326305"),
    ("SulAmérica Saúde", "006246"),
    ("NotreDame Intermédica", "359017"),
    ("Cassi", "346659"),
    ("Golden Cross", "004049"),
)


# --- Procedimentos por setor, com analitos e faixas de referência ---
PROCEDIMENTOS: tuple[ProcedimentoCatalogo, ...] = (
    ProcedimentoCatalogo("40302016", "Hemograma completo", "Hematologia", TipoMaterial.SANGUE, Decimal("28.50"), (
        Analito("Hemoglobina", "g/dL", 12.0, 17.5),
        Analito("Hematócrito", "%", 36.0, 52.0),
        Analito("Leucócitos", "/mm³", 4000, 11000),
    )),
    ProcedimentoCatalogo("40302040", "Contagem de plaquetas", "Hematologia", TipoMaterial.SANGUE, Decimal("15.00"), (
        Analito("Plaquetas", "/mm³", 150000, 450000),
    )),
    ProcedimentoCatalogo("40304361", "Tempo de protrombina (TAP)", "Hematologia", TipoMaterial.SANGUE, Decimal("22.00"), (
        Analito("TAP", "segundos", 11.0, 14.0),
        Analito("INR", "", 0.9, 1.2),
    )),
    ProcedimentoCatalogo("40304370", "Tempo de tromboplastina (TTPA)", "Hematologia", TipoMaterial.SANGUE, Decimal("24.00"), (
        Analito("TTPA", "segundos", 25.0, 37.0),
    )),
    ProcedimentoCatalogo("40304060", "Hemoglobina glicada (HbA1c)", "Hematologia", TipoMaterial.SANGUE, Decimal("34.00"), (
        Analito("HbA1c", "%", 4.0, 5.7),
    )),
    ProcedimentoCatalogo("40301630", "Glicose", "Bioquímica", TipoMaterial.SANGUE, Decimal("12.50"), (
        Analito("Glicose", "mg/dL", 70, 99),
    )),
    ProcedimentoCatalogo("40301770", "Colesterol total", "Bioquímica", TipoMaterial.SANGUE, Decimal("14.00"), (
        Analito("Colesterol total", "mg/dL", 120, 190),
    )),
    ProcedimentoCatalogo("40301788", "HDL colesterol", "Bioquímica", TipoMaterial.SANGUE, Decimal("16.00"), (
        Analito("HDL", "mg/dL", 40, 80),
    )),
    ProcedimentoCatalogo("40301796", "LDL colesterol", "Bioquímica", TipoMaterial.SANGUE, Decimal("16.00"), (
        Analito("LDL", "mg/dL", 50, 130),
    )),
    ProcedimentoCatalogo("40302113", "Triglicerídeos", "Bioquímica", TipoMaterial.SANGUE, Decimal("15.50"), (
        Analito("Triglicerídeos", "mg/dL", 40, 150),
    )),
    ProcedimentoCatalogo("40301672", "Ureia", "Bioquímica", TipoMaterial.SANGUE, Decimal("11.00"), (
        Analito("Ureia", "mg/dL", 15, 45),
    )),
    ProcedimentoCatalogo("40301680", "Creatinina", "Bioquímica", TipoMaterial.SANGUE, Decimal("11.50"), (
        Analito("Creatinina", "mg/dL", 0.6, 1.3),
    )),
    ProcedimentoCatalogo("40301842", "Ácido úrico", "Bioquímica", TipoMaterial.SANGUE, Decimal("13.00"), (
        Analito("Ácido úrico", "mg/dL", 2.5, 7.0),
    )),
    ProcedimentoCatalogo("40302261", "TGO / AST", "Bioquímica", TipoMaterial.SANGUE, Decimal("13.50"), (
        Analito("AST", "U/L", 10, 40),
    )),
    ProcedimentoCatalogo("40302270", "TGP / ALT", "Bioquímica", TipoMaterial.SANGUE, Decimal("13.50"), (
        Analito("ALT", "U/L", 10, 45),
    )),
    ProcedimentoCatalogo("40302130", "Gama GT", "Bioquímica", TipoMaterial.SANGUE, Decimal("17.00"), (
        Analito("Gama GT", "U/L", 8, 61),
    )),
    ProcedimentoCatalogo("40301974", "Fosfatase alcalina", "Bioquímica", TipoMaterial.SANGUE, Decimal("16.50"), (
        Analito("Fosfatase alcalina", "U/L", 40, 129),
    )),
    ProcedimentoCatalogo("40301541", "Ferro sérico", "Bioquímica", TipoMaterial.SANGUE, Decimal("19.00"), (
        Analito("Ferro", "µg/dL", 50, 170),
    )),
    ProcedimentoCatalogo("40310060", "Ferritina", "Imunologia", TipoMaterial.SANGUE, Decimal("38.00"), (
        Analito("Ferritina", "ng/mL", 20, 300),
    )),
    ProcedimentoCatalogo("40311902", "TSH — hormônio tireoestimulante", "Imunologia", TipoMaterial.SANGUE, Decimal("32.00"), (
        Analito("TSH", "µUI/mL", 0.4, 4.5),
    )),
    ProcedimentoCatalogo("40311945", "T4 livre", "Imunologia", TipoMaterial.SANGUE, Decimal("30.00"), (
        Analito("T4 livre", "ng/dL", 0.7, 1.8),
    )),
    ProcedimentoCatalogo("40316203", "Vitamina D (25-OH)", "Imunologia", TipoMaterial.SANGUE, Decimal("62.00"), (
        Analito("25-OH vitamina D", "ng/mL", 30, 100),
    )),
    ProcedimentoCatalogo("40316300", "Vitamina B12", "Imunologia", TipoMaterial.SANGUE, Decimal("45.00"), (
        Analito("Vitamina B12", "pg/mL", 200, 900),
    )),
    ProcedimentoCatalogo("40316165", "PSA total", "Imunologia", TipoMaterial.SANGUE, Decimal("48.00"), (
        Analito("PSA total", "ng/mL", 0.0, 4.0),
    )),
    ProcedimentoCatalogo("40302172", "Proteína C reativa (PCR)", "Imunologia", TipoMaterial.SANGUE, Decimal("26.00"), (
        Analito("PCR", "mg/L", 0.0, 5.0),
    )),
    ProcedimentoCatalogo("40310354", "Beta HCG quantitativo", "Imunologia", TipoMaterial.SANGUE, Decimal("42.00"), (
        Analito("Beta HCG", "mUI/mL", 0.0, 5.0),
    )),
    ProcedimentoCatalogo("40308635", "VDRL", "Imunologia", TipoMaterial.SANGUE, Decimal("21.00"), (
        Analito("VDRL", "título", 0.0, 1.0),
    )),
    ProcedimentoCatalogo("40307450", "Urina tipo I (EAS)", "Urinálise", TipoMaterial.URINA, Decimal("18.00"), (
        Analito("Densidade", "", 1.005, 1.030),
        Analito("pH urinário", "", 5.0, 7.0),
    )),
    ProcedimentoCatalogo("40310120", "Urocultura com antibiograma", "Microbiologia", TipoMaterial.URINA, Decimal("52.00"), (
        Analito("Contagem de colônias", "UFC/mL", 0, 10000),
    )),
    ProcedimentoCatalogo("40308880", "Parasitológico de fezes", "Microbiologia", TipoMaterial.FEZES, Decimal("23.00"), (
        Analito("Pesquisa de ovos e cistos", "", 0.0, 1.0),
    )),
)


# --- Corpo clínico (nome, CRM, UF, responsável técnico) ---
MEDICOS: tuple[tuple[str, str, str, bool], ...] = (
    ("Dra. Helena Vasconcelos", "12345", "PE", True),
    ("Dr. Rafael Lins", "54321", "PE", False),
    ("Dra. Beatriz Colares", "20984", "PE", True),
    ("Dr. Anderson Maciel", "31877", "PE", True),
    ("Dra. Luciana Peixoto", "44520", "AL", True),
    ("Dr. Fernando Uchôa", "50163", "PE", False),
    ("Dra. Mariana Tenório", "60274", "PE", False),
    ("Dr. Otávio Bandeira", "70385", "BA", False),
    ("Dra. Priscila Gouveia", "80496", "PE", False),
    ("Dr. Sérgio Albuquerque", "90507", "PE", False),
    ("Dra. Tatiana Bezerra", "10618", "AL", False),
    ("Dr. Vinícius Rolim", "11729", "PE", False),
)


# --- Equipe operacional (email, nome, perfil RBAC) ---
USUARIOS: tuple[tuple[str, str, str], ...] = (
    ("seeder@labvida.com.br", "Seeder do Sistema", "admin"),
    ("direcao@labvida.com.br", "Carolina Menezes", "admin"),
    ("recepcao.centro@labvida.com.br", "Juliana Farias", "atendente"),
    ("recepcao.heliopolis@labvida.com.br", "Marcos Antônio Dias", "atendente"),
    ("coleta.centro@labvida.com.br", "Patrícia Nogueira", "coletador"),
    ("coleta.heliopolis@labvida.com.br", "Rodrigo Sampaio", "coletador"),
    ("coleta.saojose@labvida.com.br", "Elaine Cordeiro", "coletador"),
    ("coleta.boavista@labvida.com.br", "Thiago Monteiro", "coletador"),
    ("bancada.hematologia@labvida.com.br", "Camila Duarte", "tecnico_laboratorio"),
    ("bancada.bioquimica@labvida.com.br", "Bruno Siqueira", "tecnico_laboratorio"),
    ("rt@labvida.com.br", "Helena Vasconcelos", "responsavel_tecnico"),
    ("faturamento@labvida.com.br", "Renata Lacerda", "faturista"),
    ("financeiro@labvida.com.br", "Gustavo Paes", "financeiro"),
    ("compras@labvida.com.br", "Sandra Vieira", "requisitante_compras"),
    ("aprovacao.compras@labvida.com.br", "Eduardo Falcão", "aprovador_compras"),
    ("almoxarifado@labvida.com.br", "Wagner Torres", "almoxarife"),
)


# --- Cadeia de suprimentos ---
FORNECEDORES: tuple[str, ...] = (
    "LabSupply Ltda",
    "BioReagentes S.A.",
    "MedInsumos Brasil",
    "Diagnóstica Nordeste",
    "Vitro Científica",
    "Alfa Reagentes",
    "Nordeste Hospitalar",
    "PontoLab Distribuidora",
)

# (nome, finalidade, valor unitário, quantidade típica de compra). Preço e
# quantidade andam juntos: kit de reagente sai em unidades, descartável em
# centenas — é o que mantém o valor do pedido na ordem de grandeza real.
INSUMOS: tuple[tuple[str, str, Decimal, int], ...] = (
    ("Reagente Hematologia", "Hemograma completo", Decimal("285.00"), 2),
    ("Reagente Bioquímica", "Dosagem de glicose e colesterol", Decimal("320.00"), 2),
    ("Reagente Imunologia", "Dosagens hormonais e sorologias", Decimal("410.00"), 1),
    ("Tubo de Coleta EDTA", "Coleta de sangue para hematologia", Decimal("0.42"), 500),
    ("Tubo de Coleta com Gel Separador", "Coleta de soro para bioquímica", Decimal("0.55"), 500),
    ("Tubo de Coleta Citrato", "Coleta para provas de coagulação", Decimal("0.48"), 300),
    ("Ponteira 100µL", "Pipetagem de amostras", Decimal("0.09"), 1000),
    ("Ponteira 1000µL", "Pipetagem de reagentes", Decimal("0.14"), 1000),
    ("Lâmina de Microscopia", "Análise microscópica", Decimal("0.22"), 500),
    ("Lamínula 22x22mm", "Cobertura de lâminas", Decimal("0.08"), 1000),
    ("Luva de Procedimento M", "Proteção individual na coleta", Decimal("0.38"), 400),
    ("Luva de Procedimento G", "Proteção individual na bancada", Decimal("0.38"), 400),
    ("Álcool 70%", "Antissepsia de punção", Decimal("11.90"), 24),
    ("Algodão Hidrófilo", "Antissepsia e curativo pós-punção", Decimal("8.40"), 30),
    ("Agulha de Coleta 25x7", "Punção venosa", Decimal("0.19"), 600),
    ("Escalpe 23G", "Punção em veia de calibre fino", Decimal("0.86"), 300),
    ("Garrote Descartável", "Estase venosa na coleta", Decimal("1.35"), 100),
    ("Frasco Coletor Universal", "Coleta de urina e fezes", Decimal("0.62"), 400),
    ("Meio de Cultura Ágar Sangue", "Cultura microbiológica", Decimal("78.00"), 5),
    ("Meio de Cultura MacConkey", "Isolamento de enterobactérias", Decimal("72.00"), 5),
    ("Kit Antibiograma", "Teste de sensibilidade a antimicrobianos", Decimal("240.00"), 2),
    ("Papel Termossensível para Etiqueta", "Etiquetagem de amostras", Decimal("18.50"), 20),
    ("Caixa Térmica para Malote", "Transporte de amostras entre unidades", Decimal("165.00"), 2),
    ("Gelo Reciclável", "Conservação de amostras em trânsito", Decimal("9.80"), 20),
)


# --- Glosas: motivos reais de recusa de convênio ---
MOTIVOS_GLOSA: tuple[str, ...] = (
    "Procedimento não coberto pelo plano contratado",
    "Guia sem autorização prévia do convênio",
    "Divergência entre código TUSS e procedimento executado",
    "Beneficiário com carência não cumprida",
    "Valor apresentado acima da tabela negociada",
    "Documentação incompleta no envio do lote",
    "Prazo de apresentação da guia expirado",
    "Duplicidade de cobrança no período",
)


# --- Ocorrências de logística ---
MOTIVOS_REJEICAO: tuple[str, ...] = (
    "Frasco trincado e material extravasado",
    "Amostra hemolisada durante o transporte",
    "Identificação da etiqueta ilegível",
    "Volume insuficiente para o exame solicitado",
    "Temperatura fora da faixa de conservação",
    "Tubo sem tampa de vedação adequada",
)


EQUIPAMENTOS: tuple[tuple[str, str, str], ...] = (
    ("Analisador Hematológico X-2000", "Hematologia", "HL7"),
    ("Analisador Bioquímico BQ-500", "Bioquímica", "HL7"),
    ("Analisador de Imunoensaio IM-300", "Imunologia", "ASTM"),
    ("Coagulômetro CG-120", "Hematologia", "ASTM"),
    ("Leitor de Urinálise UR-80", "Urinálise", "HL7"),
    ("Incubadora Microbiológica MB-40", "Microbiologia", "ASTM"),
)
