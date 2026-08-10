--
-- PostgreSQL database dump
--

\restrict dFRUsYUR1RMaQIh8ZqOyrzvDjdcUmQjhfZWIEbJcOk4zfiP01u3POajjViaLWW2

-- Dumped from database version 16.14
-- Dumped by pg_dump version 16.14

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: btree_gist; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS btree_gist WITH SCHEMA public;


--
-- Name: EXTENSION btree_gist; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION btree_gist IS 'support for indexing common datatypes in GiST';


--
-- Name: protocolo_equipamento; Type: TYPE; Schema: public; Owner: labvida
--

CREATE TYPE public.protocolo_equipamento AS ENUM (
    'HL7',
    'ASTM'
);


ALTER TYPE public.protocolo_equipamento OWNER TO labvida;

--
-- Name: sexo_paciente; Type: TYPE; Schema: public; Owner: labvida
--

CREATE TYPE public.sexo_paciente AS ENUM (
    'MASCULINO',
    'FEMININO',
    'NAO_INFORMADO'
);


ALTER TYPE public.sexo_paciente OWNER TO labvida;

--
-- Name: status_laudo; Type: TYPE; Schema: public; Owner: labvida
--

CREATE TYPE public.status_laudo AS ENUM (
    'RASCUNHO',
    'LIBERADO'
);


ALTER TYPE public.status_laudo OWNER TO labvida;

--
-- Name: status_resultado; Type: TYPE; Schema: public; Owner: labvida
--

CREATE TYPE public.status_resultado AS ENUM (
    'AGUARDANDO_REVISAO',
    'REVISADO'
);


ALTER TYPE public.status_resultado OWNER TO labvida;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: labvida
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO labvida;

--
-- Name: amostras; Type: TABLE; Schema: public; Owner: labvida
--

CREATE TABLE public.amostras (
    id uuid NOT NULL,
    ordem_servico_id uuid NOT NULL,
    codigo_barras character varying(20) NOT NULL,
    tipo_material character varying(40) NOT NULL,
    status character varying(20) NOT NULL,
    CONSTRAINT ck_amostra_status CHECK (((status)::text = ANY ((ARRAY['AGUARDANDO_COLETA'::character varying, 'COLETADA'::character varying, 'EM_TRANSITO'::character varying, 'RECEBIDA'::character varying, 'REJEITADA'::character varying])::text[])))
);


ALTER TABLE public.amostras OWNER TO labvida;

--
-- Name: amostras_movimentacoes; Type: TABLE; Schema: public; Owner: labvida
--

CREATE TABLE public.amostras_movimentacoes (
    id uuid NOT NULL,
    amostra_id uuid NOT NULL,
    status character varying(20) NOT NULL,
    usuario_id uuid NOT NULL,
    unidade_id uuid NOT NULL,
    observacao character varying(255),
    ocorrido_em timestamp with time zone NOT NULL,
    CONSTRAINT ck_movimentacao_status CHECK (((status)::text = ANY ((ARRAY['COLETADA'::character varying, 'EM_TRANSITO'::character varying, 'RECEBIDA'::character varying, 'REJEITADA'::character varying])::text[])))
);


ALTER TABLE public.amostras_movimentacoes OWNER TO labvida;

--
-- Name: analitos; Type: TABLE; Schema: public; Owner: labvida
--

CREATE TABLE public.analitos (
    id uuid NOT NULL,
    codigo character varying(30) NOT NULL,
    nome character varying(120) NOT NULL,
    unidade_medida character varying(20),
    casas_decimais smallint DEFAULT '2'::smallint NOT NULL,
    loinc character varying(20),
    ativo boolean DEFAULT true NOT NULL
);


ALTER TABLE public.analitos OWNER TO labvida;

--
-- Name: auditoria_log; Type: TABLE; Schema: public; Owner: labvida
--

CREATE TABLE public.auditoria_log (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    usuario_id uuid NOT NULL,
    entidade character varying(50) NOT NULL,
    entidade_id uuid,
    acao character varying(30) NOT NULL,
    dados jsonb DEFAULT '{}'::jsonb NOT NULL,
    ocorrido_em timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.auditoria_log OWNER TO labvida;

--
-- Name: autorizacoes_convenio; Type: TABLE; Schema: public; Owner: labvida
--

CREATE TABLE public.autorizacoes_convenio (
    id uuid NOT NULL,
    ordem_servico_id uuid NOT NULL,
    numero_guia character varying(40) NOT NULL,
    status character varying(10) NOT NULL,
    validade date,
    CONSTRAINT ck_autorizacao_status CHECK (((status)::text = ANY ((ARRAY['PENDENTE'::character varying, 'VALIDA'::character varying, 'NEGADA'::character varying])::text[])))
);


ALTER TABLE public.autorizacoes_convenio OWNER TO labvida;

--
-- Name: bi_dim_convenio; Type: TABLE; Schema: public; Owner: labvida
--

CREATE TABLE public.bi_dim_convenio (
    sk_convenio integer NOT NULL,
    id_origem uuid NOT NULL,
    nome character varying(120) NOT NULL,
    registro_ans character varying(20)
);


ALTER TABLE public.bi_dim_convenio OWNER TO labvida;

--
-- Name: bi_dim_convenio_sk_convenio_seq; Type: SEQUENCE; Schema: public; Owner: labvida
--

CREATE SEQUENCE public.bi_dim_convenio_sk_convenio_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.bi_dim_convenio_sk_convenio_seq OWNER TO labvida;

--
-- Name: bi_dim_convenio_sk_convenio_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: labvida
--

ALTER SEQUENCE public.bi_dim_convenio_sk_convenio_seq OWNED BY public.bi_dim_convenio.sk_convenio;


--
-- Name: bi_dim_faixa_etaria; Type: TABLE; Schema: public; Owner: labvida
--

CREATE TABLE public.bi_dim_faixa_etaria (
    sk_faixa_etaria integer NOT NULL,
    chave_natural character varying(20) NOT NULL,
    descricao character varying(20) NOT NULL,
    ordem smallint NOT NULL
);


ALTER TABLE public.bi_dim_faixa_etaria OWNER TO labvida;

--
-- Name: bi_dim_faixa_etaria_sk_faixa_etaria_seq; Type: SEQUENCE; Schema: public; Owner: labvida
--

CREATE SEQUENCE public.bi_dim_faixa_etaria_sk_faixa_etaria_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.bi_dim_faixa_etaria_sk_faixa_etaria_seq OWNER TO labvida;

--
-- Name: bi_dim_faixa_etaria_sk_faixa_etaria_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: labvida
--

ALTER SEQUENCE public.bi_dim_faixa_etaria_sk_faixa_etaria_seq OWNED BY public.bi_dim_faixa_etaria.sk_faixa_etaria;


--
-- Name: bi_dim_motivo_glosa; Type: TABLE; Schema: public; Owner: labvida
--

CREATE TABLE public.bi_dim_motivo_glosa (
    sk_motivo_glosa integer NOT NULL,
    chave_natural character varying(255) NOT NULL,
    descricao character varying(255) NOT NULL
);


ALTER TABLE public.bi_dim_motivo_glosa OWNER TO labvida;

--
-- Name: bi_dim_motivo_glosa_sk_motivo_glosa_seq; Type: SEQUENCE; Schema: public; Owner: labvida
--

CREATE SEQUENCE public.bi_dim_motivo_glosa_sk_motivo_glosa_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.bi_dim_motivo_glosa_sk_motivo_glosa_seq OWNER TO labvida;

--
-- Name: bi_dim_motivo_glosa_sk_motivo_glosa_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: labvida
--

ALTER SEQUENCE public.bi_dim_motivo_glosa_sk_motivo_glosa_seq OWNED BY public.bi_dim_motivo_glosa.sk_motivo_glosa;


--
-- Name: bi_dim_paciente_anon; Type: TABLE; Schema: public; Owner: labvida
--

CREATE TABLE public.bi_dim_paciente_anon (
    sk_paciente integer NOT NULL,
    id_origem character varying(64) NOT NULL,
    sexo character varying(20) NOT NULL
);


ALTER TABLE public.bi_dim_paciente_anon OWNER TO labvida;

--
-- Name: bi_dim_paciente_anon_sk_paciente_seq; Type: SEQUENCE; Schema: public; Owner: labvida
--

CREATE SEQUENCE public.bi_dim_paciente_anon_sk_paciente_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.bi_dim_paciente_anon_sk_paciente_seq OWNER TO labvida;

--
-- Name: bi_dim_paciente_anon_sk_paciente_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: labvida
--

ALTER SEQUENCE public.bi_dim_paciente_anon_sk_paciente_seq OWNED BY public.bi_dim_paciente_anon.sk_paciente;


--
-- Name: bi_dim_procedimento; Type: TABLE; Schema: public; Owner: labvida
--

CREATE TABLE public.bi_dim_procedimento (
    sk_procedimento integer NOT NULL,
    id_origem uuid NOT NULL,
    codigo_tuss character varying(20) NOT NULL,
    nome character varying(120) NOT NULL,
    setor character varying(60),
    sk_setor integer,
    ativo boolean DEFAULT true NOT NULL
);


ALTER TABLE public.bi_dim_procedimento OWNER TO labvida;

--
-- Name: bi_dim_procedimento_sk_procedimento_seq; Type: SEQUENCE; Schema: public; Owner: labvida
--

CREATE SEQUENCE public.bi_dim_procedimento_sk_procedimento_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.bi_dim_procedimento_sk_procedimento_seq OWNER TO labvida;

--
-- Name: bi_dim_procedimento_sk_procedimento_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: labvida
--

ALTER SEQUENCE public.bi_dim_procedimento_sk_procedimento_seq OWNED BY public.bi_dim_procedimento.sk_procedimento;


--
-- Name: bi_dim_setor; Type: TABLE; Schema: public; Owner: labvida
--

CREATE TABLE public.bi_dim_setor (
    sk_setor integer NOT NULL,
    chave_natural character varying(60) NOT NULL,
    nome character varying(60) NOT NULL
);


ALTER TABLE public.bi_dim_setor OWNER TO labvida;

--
-- Name: bi_dim_setor_sk_setor_seq; Type: SEQUENCE; Schema: public; Owner: labvida
--

CREATE SEQUENCE public.bi_dim_setor_sk_setor_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.bi_dim_setor_sk_setor_seq OWNER TO labvida;

--
-- Name: bi_dim_setor_sk_setor_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: labvida
--

ALTER SEQUENCE public.bi_dim_setor_sk_setor_seq OWNED BY public.bi_dim_setor.sk_setor;


--
-- Name: bi_dim_tempo; Type: TABLE; Schema: public; Owner: labvida
--

CREATE TABLE public.bi_dim_tempo (
    sk_tempo integer NOT NULL,
    data date NOT NULL,
    ano integer NOT NULL,
    mes integer NOT NULL,
    dia integer NOT NULL,
    dia_semana character varying(20) NOT NULL,
    dia_semana_num smallint NOT NULL,
    trimestre smallint NOT NULL,
    semestre smallint NOT NULL,
    semana_iso smallint NOT NULL,
    nome_mes character varying(20) NOT NULL,
    ano_mes character varying(7) NOT NULL,
    competencia date NOT NULL,
    dia_util boolean DEFAULT true NOT NULL
);


ALTER TABLE public.bi_dim_tempo OWNER TO labvida;

--
-- Name: bi_dim_tempo_sk_tempo_seq; Type: SEQUENCE; Schema: public; Owner: labvida
--

CREATE SEQUENCE public.bi_dim_tempo_sk_tempo_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.bi_dim_tempo_sk_tempo_seq OWNER TO labvida;

--
-- Name: bi_dim_tempo_sk_tempo_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: labvida
--

ALTER SEQUENCE public.bi_dim_tempo_sk_tempo_seq OWNED BY public.bi_dim_tempo.sk_tempo;


--
-- Name: bi_dim_unidade; Type: TABLE; Schema: public; Owner: labvida
--

CREATE TABLE public.bi_dim_unidade (
    sk_unidade integer NOT NULL,
    id_origem uuid NOT NULL,
    nome character varying(120) NOT NULL,
    tipo character varying(10) NOT NULL
);


ALTER TABLE public.bi_dim_unidade OWNER TO labvida;

--
-- Name: bi_dim_unidade_sk_unidade_seq; Type: SEQUENCE; Schema: public; Owner: labvida
--

CREATE SEQUENCE public.bi_dim_unidade_sk_unidade_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.bi_dim_unidade_sk_unidade_seq OWNER TO labvida;

--
-- Name: bi_dim_unidade_sk_unidade_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: labvida
--

ALTER SEQUENCE public.bi_dim_unidade_sk_unidade_seq OWNED BY public.bi_dim_unidade.sk_unidade;


--
-- Name: bi_etl_execucao; Type: TABLE; Schema: public; Owner: labvida
--

CREATE TABLE public.bi_etl_execucao (
    id uuid NOT NULL,
    iniciado_em timestamp with time zone DEFAULT now() NOT NULL,
    finalizado_em timestamp with time zone,
    status character varying(12) DEFAULT 'EXECUTANDO'::character varying NOT NULL,
    modo character varying(12) DEFAULT 'FULL'::character varying NOT NULL,
    linhas jsonb,
    duracao_seg numeric(10,2),
    erro text
);


ALTER TABLE public.bi_etl_execucao OWNER TO labvida;

--
-- Name: bi_fato_atendimento; Type: TABLE; Schema: public; Owner: labvida
--

CREATE TABLE public.bi_fato_atendimento (
    sk_fato integer NOT NULL,
    os_item_id uuid NOT NULL,
    sk_tempo integer NOT NULL,
    sk_unidade integer NOT NULL,
    sk_convenio integer,
    sk_procedimento integer NOT NULL,
    sk_paciente integer NOT NULL,
    sk_faixa_etaria integer NOT NULL,
    sk_setor integer,
    qtd_exames integer DEFAULT 1 NOT NULL,
    valor_negociado numeric(12,2) DEFAULT '0'::numeric NOT NULL,
    cancelado boolean DEFAULT false NOT NULL,
    laudo_liberado boolean DEFAULT false NOT NULL
);


ALTER TABLE public.bi_fato_atendimento OWNER TO labvida;

--
-- Name: bi_fato_atendimento_sk_fato_seq; Type: SEQUENCE; Schema: public; Owner: labvida
--

CREATE SEQUENCE public.bi_fato_atendimento_sk_fato_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.bi_fato_atendimento_sk_fato_seq OWNER TO labvida;

--
-- Name: bi_fato_atendimento_sk_fato_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: labvida
--

ALTER SEQUENCE public.bi_fato_atendimento_sk_fato_seq OWNED BY public.bi_fato_atendimento.sk_fato;


--
-- Name: bi_fato_faturamento; Type: TABLE; Schema: public; Owner: labvida
--

CREATE TABLE public.bi_fato_faturamento (
    sk_fato integer NOT NULL,
    guia_item_id uuid NOT NULL,
    sk_tempo integer NOT NULL,
    sk_unidade integer NOT NULL,
    sk_convenio integer,
    sk_procedimento integer NOT NULL,
    sk_paciente integer NOT NULL,
    sk_setor integer,
    valor_faturado numeric(12,2) DEFAULT '0'::numeric NOT NULL,
    valor_glosado numeric(12,2) DEFAULT '0'::numeric NOT NULL,
    valor_liberado numeric(12,2) DEFAULT '0'::numeric NOT NULL,
    qtd_itens integer DEFAULT 1 NOT NULL
);


ALTER TABLE public.bi_fato_faturamento OWNER TO labvida;

--
-- Name: bi_fato_faturamento_sk_fato_seq; Type: SEQUENCE; Schema: public; Owner: labvida
--

CREATE SEQUENCE public.bi_fato_faturamento_sk_fato_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.bi_fato_faturamento_sk_fato_seq OWNER TO labvida;

--
-- Name: bi_fato_faturamento_sk_fato_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: labvida
--

ALTER SEQUENCE public.bi_fato_faturamento_sk_fato_seq OWNED BY public.bi_fato_faturamento.sk_fato;


--
-- Name: bi_fato_financeiro; Type: TABLE; Schema: public; Owner: labvida
--

CREATE TABLE public.bi_fato_financeiro (
    sk_fato integer NOT NULL,
    regime character varying(10) NOT NULL,
    origem_tabela character varying(24) NOT NULL,
    origem_id uuid NOT NULL,
    sk_tempo integer NOT NULL,
    sk_unidade integer NOT NULL,
    sk_convenio integer,
    fluxo character varying(10) NOT NULL,
    valor_previsto numeric(12,2) DEFAULT '0'::numeric NOT NULL,
    valor_realizado numeric(12,2) DEFAULT '0'::numeric NOT NULL,
    liquidado boolean DEFAULT false NOT NULL
);


ALTER TABLE public.bi_fato_financeiro OWNER TO labvida;

--
-- Name: bi_fato_financeiro_sk_fato_seq; Type: SEQUENCE; Schema: public; Owner: labvida
--

CREATE SEQUENCE public.bi_fato_financeiro_sk_fato_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.bi_fato_financeiro_sk_fato_seq OWNER TO labvida;

--
-- Name: bi_fato_financeiro_sk_fato_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: labvida
--

ALTER SEQUENCE public.bi_fato_financeiro_sk_fato_seq OWNED BY public.bi_fato_financeiro.sk_fato;


--
-- Name: bi_fato_glosa; Type: TABLE; Schema: public; Owner: labvida
--

CREATE TABLE public.bi_fato_glosa (
    sk_fato integer NOT NULL,
    glosa_id uuid NOT NULL,
    sk_tempo integer NOT NULL,
    sk_unidade integer NOT NULL,
    sk_convenio integer,
    sk_procedimento integer NOT NULL,
    sk_motivo_glosa integer NOT NULL,
    valor_glosado numeric(12,2) DEFAULT '0'::numeric NOT NULL,
    valor_faturado_item numeric(12,2) DEFAULT '0'::numeric NOT NULL,
    qtd_glosas integer DEFAULT 1 NOT NULL
);


ALTER TABLE public.bi_fato_glosa OWNER TO labvida;

--
-- Name: bi_fato_glosa_sk_fato_seq; Type: SEQUENCE; Schema: public; Owner: labvida
--

CREATE SEQUENCE public.bi_fato_glosa_sk_fato_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.bi_fato_glosa_sk_fato_seq OWNER TO labvida;

--
-- Name: bi_fato_glosa_sk_fato_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: labvida
--

ALTER SEQUENCE public.bi_fato_glosa_sk_fato_seq OWNED BY public.bi_fato_glosa.sk_fato;


--
-- Name: bi_fato_logistica; Type: TABLE; Schema: public; Owner: labvida
--

CREATE TABLE public.bi_fato_logistica (
    sk_fato integer NOT NULL,
    amostra_id uuid NOT NULL,
    sk_tempo integer NOT NULL,
    sk_unidade integer NOT NULL,
    sk_unidade_destino integer,
    qtd_amostras integer DEFAULT 1 NOT NULL,
    tempo_transito_horas numeric(10,2),
    tempo_coleta_recebimento_horas numeric(10,2),
    rejeitada boolean DEFAULT false NOT NULL,
    amostras_divergentes integer DEFAULT 0 NOT NULL,
    status_atual character varying(20) DEFAULT ''::character varying NOT NULL
);


ALTER TABLE public.bi_fato_logistica OWNER TO labvida;

--
-- Name: bi_fato_logistica_sk_fato_seq; Type: SEQUENCE; Schema: public; Owner: labvida
--

CREATE SEQUENCE public.bi_fato_logistica_sk_fato_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.bi_fato_logistica_sk_fato_seq OWNER TO labvida;

--
-- Name: bi_fato_logistica_sk_fato_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: labvida
--

ALTER SEQUENCE public.bi_fato_logistica_sk_fato_seq OWNED BY public.bi_fato_logistica.sk_fato;


--
-- Name: bi_fato_ordem_servico; Type: TABLE; Schema: public; Owner: labvida
--

CREATE TABLE public.bi_fato_ordem_servico (
    sk_fato integer NOT NULL,
    ordem_servico_id uuid NOT NULL,
    sk_tempo integer NOT NULL,
    sk_unidade integer NOT NULL,
    sk_convenio integer,
    sk_paciente integer NOT NULL,
    sk_faixa_etaria integer NOT NULL,
    qtd_itens integer DEFAULT 0 NOT NULL,
    qtd_itens_cancelados integer DEFAULT 0 NOT NULL,
    valor_total numeric(12,2) DEFAULT '0'::numeric NOT NULL,
    tempo_ciclo_horas numeric(10,2),
    tempo_coleta_recebimento_horas numeric(10,2),
    tempo_recebimento_laudo_horas numeric(10,2),
    concluida boolean DEFAULT false NOT NULL
);


ALTER TABLE public.bi_fato_ordem_servico OWNER TO labvida;

--
-- Name: bi_fato_ordem_servico_sk_fato_seq; Type: SEQUENCE; Schema: public; Owner: labvida
--

CREATE SEQUENCE public.bi_fato_ordem_servico_sk_fato_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.bi_fato_ordem_servico_sk_fato_seq OWNER TO labvida;

--
-- Name: bi_fato_ordem_servico_sk_fato_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: labvida
--

ALTER SEQUENCE public.bi_fato_ordem_servico_sk_fato_seq OWNED BY public.bi_fato_ordem_servico.sk_fato;


--
-- Name: coletas; Type: TABLE; Schema: public; Owner: labvida
--

CREATE TABLE public.coletas (
    id uuid NOT NULL,
    amostra_id uuid NOT NULL,
    coletor_id uuid NOT NULL,
    coletada_em timestamp with time zone NOT NULL
);


ALTER TABLE public.coletas OWNER TO labvida;

--
-- Name: competencias; Type: TABLE; Schema: public; Owner: labvida
--

CREATE TABLE public.competencias (
    competencia date NOT NULL,
    status character varying(10) DEFAULT 'ABERTA'::character varying NOT NULL,
    valor_faturado numeric(14,2),
    valor_glosado numeric(14,2),
    valor_liberado numeric(14,2),
    qtd_laudos integer,
    qtd_guias integer,
    qtd_lotes integer,
    criada_em timestamp with time zone DEFAULT now() NOT NULL,
    fechada_em timestamp with time zone,
    fechada_por_usuario_id uuid,
    reaberta_em timestamp with time zone,
    justificativa character varying(255),
    CONSTRAINT ck_competencia_dia_um CHECK ((EXTRACT(day FROM competencia) = (1)::numeric)),
    CONSTRAINT ck_competencia_fechamento CHECK ((((status)::text = 'ABERTA'::text) OR (fechada_em IS NOT NULL))),
    CONSTRAINT ck_competencia_status CHECK (((status)::text = ANY ((ARRAY['ABERTA'::character varying, 'FECHADA'::character varying])::text[])))
);


ALTER TABLE public.competencias OWNER TO labvida;

--
-- Name: conciliacoes_pagamento; Type: TABLE; Schema: public; Owner: labvida
--

CREATE TABLE public.conciliacoes_pagamento (
    id uuid NOT NULL,
    titulo_receber_id uuid NOT NULL,
    valor_recebido numeric(12,2) NOT NULL,
    divergencia numeric(12,2) DEFAULT '0'::numeric NOT NULL,
    conciliado_em timestamp with time zone DEFAULT now() NOT NULL,
    observacao character varying(255)
);


ALTER TABLE public.conciliacoes_pagamento OWNER TO labvida;

--
-- Name: convenios; Type: TABLE; Schema: public; Owner: labvida
--

CREATE TABLE public.convenios (
    id uuid NOT NULL,
    nome character varying(120) NOT NULL,
    nome_normalizado character varying(120) NOT NULL,
    cnpj character varying(14),
    telefone character varying(11),
    email character varying(254),
    registro_ans character varying(20),
    ativo boolean NOT NULL,
    status character varying(7) NOT NULL,
    prazo_pagamento_dias integer DEFAULT 30 NOT NULL,
    dia_vencimento smallint,
    CONSTRAINT ck_convenio_dia_vencimento CHECK (((dia_vencimento IS NULL) OR ((dia_vencimento >= 1) AND (dia_vencimento <= 28)))),
    CONSTRAINT ck_convenio_prazo CHECK (((prazo_pagamento_dias >= 0) AND (prazo_pagamento_dias <= 365))),
    CONSTRAINT ck_convenio_status CHECK (((status)::text = ANY ((ARRAY['ATIVO'::character varying, 'INATIVO'::character varying])::text[])))
);


ALTER TABLE public.convenios OWNER TO labvida;

--
-- Name: equipamentos; Type: TABLE; Schema: public; Owner: labvida
--

CREATE TABLE public.equipamentos (
    id uuid NOT NULL,
    setor_id uuid NOT NULL,
    nome character varying(120) NOT NULL,
    protocolo public.protocolo_equipamento NOT NULL
);


ALTER TABLE public.equipamentos OWNER TO labvida;

--
-- Name: estoque_movimentos; Type: TABLE; Schema: public; Owner: labvida
--

CREATE TABLE public.estoque_movimentos (
    id uuid NOT NULL,
    insumo_material_id uuid NOT NULL,
    tipo character varying(20) NOT NULL,
    quantidade numeric(12,3) NOT NULL,
    ocorrido_em timestamp with time zone DEFAULT now() NOT NULL,
    observacao character varying(255)
);


ALTER TABLE public.estoque_movimentos OWNER TO labvida;

--
-- Name: fornecedores; Type: TABLE; Schema: public; Owner: labvida
--

CREATE TABLE public.fornecedores (
    id uuid NOT NULL,
    nome character varying(150) NOT NULL,
    cnpj character varying(14) NOT NULL,
    status character varying(20) DEFAULT 'ATIVO'::character varying NOT NULL,
    criado_em timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.fornecedores OWNER TO labvida;

--
-- Name: glosas; Type: TABLE; Schema: public; Owner: labvida
--

CREATE TABLE public.glosas (
    id uuid NOT NULL,
    guia_item_id uuid NOT NULL,
    motivo character varying(255) NOT NULL,
    valor_glosado numeric(12,2) NOT NULL,
    unidade_origem_id uuid NOT NULL,
    criado_em timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.glosas OWNER TO labvida;

--
-- Name: guias_itens; Type: TABLE; Schema: public; Owner: labvida
--

CREATE TABLE public.guias_itens (
    id uuid NOT NULL,
    guia_tiss_id uuid NOT NULL,
    laudo_id uuid NOT NULL,
    procedimento_id uuid NOT NULL,
    valor_faturado numeric(12,2) NOT NULL,
    status character varying(20) DEFAULT 'FATURADO'::character varying NOT NULL,
    criado_em timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.guias_itens OWNER TO labvida;

--
-- Name: guias_tiss; Type: TABLE; Schema: public; Owner: labvida
--

CREATE TABLE public.guias_tiss (
    id uuid NOT NULL,
    lote_faturamento_id uuid NOT NULL,
    codigo_tiss character varying(30) NOT NULL,
    status_pre_auditoria character varying(30) DEFAULT 'PENDENTE'::character varying NOT NULL,
    xml_tiss text,
    criado_em timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.guias_tiss OWNER TO labvida;

--
-- Name: insumos_materiais; Type: TABLE; Schema: public; Owner: labvida
--

CREATE TABLE public.insumos_materiais (
    id uuid NOT NULL,
    nome character varying(150) NOT NULL,
    finalidade character varying(255) NOT NULL,
    quantidade_estoque numeric(12,3) DEFAULT '0'::numeric NOT NULL,
    criado_em timestamp with time zone DEFAULT now() NOT NULL,
    estoque_minimo numeric(12,3) DEFAULT '0'::numeric NOT NULL
);


ALTER TABLE public.insumos_materiais OWNER TO labvida;

--
-- Name: laudos; Type: TABLE; Schema: public; Owner: labvida
--

CREATE TABLE public.laudos (
    id uuid NOT NULL,
    os_item_id uuid NOT NULL,
    responsavel_tecnico_id uuid,
    status public.status_laudo DEFAULT 'RASCUNHO'::public.status_laudo NOT NULL,
    liberado_em timestamp with time zone,
    assinatura_digital text
);


ALTER TABLE public.laudos OWNER TO labvida;

--
-- Name: lotes_faturamento; Type: TABLE; Schema: public; Owner: labvida
--

CREATE TABLE public.lotes_faturamento (
    id uuid NOT NULL,
    codigo_lote character varying(20) NOT NULL,
    convenio_id uuid,
    status character varying(20) DEFAULT 'ABERTO'::character varying NOT NULL,
    valor_total numeric(12,2) DEFAULT '0'::numeric NOT NULL,
    criado_em timestamp with time zone DEFAULT now() NOT NULL,
    fechado_em timestamp with time zone,
    competencia date NOT NULL
);


ALTER TABLE public.lotes_faturamento OWNER TO labvida;

--
-- Name: malotes; Type: TABLE; Schema: public; Owner: labvida
--

CREATE TABLE public.malotes (
    id uuid NOT NULL,
    codigo_malote character varying(20) NOT NULL,
    unidade_origem_id uuid NOT NULL,
    unidade_destino_id uuid NOT NULL,
    enviado_por_usuario_id uuid NOT NULL,
    status character varying(20) NOT NULL,
    criado_em timestamp with time zone NOT NULL,
    despachado_em timestamp with time zone,
    CONSTRAINT ck_malote_status CHECK (((status)::text = ANY ((ARRAY['ABERTO'::character varying, 'EM_TRANSITO'::character varying, 'RECEBIDO'::character varying])::text[])))
);


ALTER TABLE public.malotes OWNER TO labvida;

--
-- Name: malotes_amostras; Type: TABLE; Schema: public; Owner: labvida
--

CREATE TABLE public.malotes_amostras (
    id uuid NOT NULL,
    malote_id uuid NOT NULL,
    amostra_id uuid NOT NULL
);


ALTER TABLE public.malotes_amostras OWNER TO labvida;

--
-- Name: medicos; Type: TABLE; Schema: public; Owner: labvida
--

CREATE TABLE public.medicos (
    id uuid NOT NULL,
    nome character varying(120) NOT NULL,
    crm character varying(10) NOT NULL,
    uf_crm character varying(2) NOT NULL,
    responsavel_tecnico boolean NOT NULL,
    ativo boolean NOT NULL
);


ALTER TABLE public.medicos OWNER TO labvida;

--
-- Name: movimentos_caixa; Type: TABLE; Schema: public; Owner: labvida
--

CREATE TABLE public.movimentos_caixa (
    id uuid NOT NULL,
    titulo_receber_id uuid,
    titulo_pagar_id uuid,
    tipo character varying(20) NOT NULL,
    valor numeric(12,2) NOT NULL,
    ocorrido_em timestamp with time zone DEFAULT now() NOT NULL,
    descricao character varying(255)
);


ALTER TABLE public.movimentos_caixa OWNER TO labvida;

--
-- Name: ordens_servico; Type: TABLE; Schema: public; Owner: labvida
--

CREATE TABLE public.ordens_servico (
    id uuid NOT NULL,
    codigo_os character varying(20) NOT NULL,
    paciente_id uuid NOT NULL,
    medico_id uuid,
    convenio_id uuid,
    unidade_id uuid NOT NULL,
    status character varying(20) NOT NULL,
    aberta_em timestamp with time zone NOT NULL,
    CONSTRAINT ck_os_status CHECK (((status)::text = ANY ((ARRAY['ABERTA'::character varying, 'EM_COLETA'::character varying, 'COLETADA'::character varying, 'EM_ANALISE'::character varying, 'CONCLUIDA'::character varying, 'CANCELADA'::character varying])::text[])))
);


ALTER TABLE public.ordens_servico OWNER TO labvida;

--
-- Name: os_itens; Type: TABLE; Schema: public; Owner: labvida
--

CREATE TABLE public.os_itens (
    id uuid NOT NULL,
    ordem_servico_id uuid NOT NULL,
    procedimento_id uuid NOT NULL,
    valor_negociado numeric(12,2) NOT NULL,
    status character varying(20) NOT NULL,
    cancelado_por_usuario_id uuid,
    valor_tabela numeric(12,2),
    origem_valor character varying(16) DEFAULT 'TABELA'::character varying NOT NULL,
    motivo_excecao character varying(255),
    CONSTRAINT ck_os_item_origem_valor CHECK (((origem_valor)::text = ANY ((ARRAY['TABELA'::character varying, 'NEGOCIADO'::character varying, 'SEM_TABELA'::character varying])::text[]))),
    CONSTRAINT ck_os_item_status CHECK (((status)::text = ANY ((ARRAY['SOLICITADO'::character varying, 'COLETADO'::character varying, 'RESULTADO_LIBERADO'::character varying, 'FATURADO'::character varying, 'CANCELADO'::character varying])::text[])))
);


ALTER TABLE public.os_itens OWNER TO labvida;

--
-- Name: os_status_historico; Type: TABLE; Schema: public; Owner: labvida
--

CREATE TABLE public.os_status_historico (
    id uuid NOT NULL,
    ordem_servico_id uuid NOT NULL,
    status character varying(20) NOT NULL,
    ocorrido_em timestamp with time zone NOT NULL,
    usuario_id uuid,
    CONSTRAINT ck_os_historico_status CHECK (((status)::text = ANY ((ARRAY['ABERTA'::character varying, 'EM_COLETA'::character varying, 'COLETADA'::character varying, 'EM_ANALISE'::character varying, 'CONCLUIDA'::character varying, 'CANCELADA'::character varying])::text[])))
);


ALTER TABLE public.os_status_historico OWNER TO labvida;

--
-- Name: pacientes; Type: TABLE; Schema: public; Owner: labvida
--

CREATE TABLE public.pacientes (
    id uuid NOT NULL,
    nome character varying(120) NOT NULL,
    data_nascimento date NOT NULL,
    telefone character varying(11) NOT NULL,
    sexo public.sexo_paciente NOT NULL,
    ativo boolean NOT NULL,
    cpf_hash character varying(64) NOT NULL,
    cpf_encrypted bytea NOT NULL
);


ALTER TABLE public.pacientes OWNER TO labvida;

--
-- Name: pedidos_compra; Type: TABLE; Schema: public; Owner: labvida
--

CREATE TABLE public.pedidos_compra (
    id uuid NOT NULL,
    solicitacao_compra_id uuid NOT NULL,
    fornecedor_id uuid NOT NULL,
    status character varying(20) DEFAULT 'RASCUNHO'::character varying NOT NULL,
    valor_total numeric(12,2) DEFAULT '0'::numeric NOT NULL,
    criado_em timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.pedidos_compra OWNER TO labvida;

--
-- Name: pedidos_itens; Type: TABLE; Schema: public; Owner: labvida
--

CREATE TABLE public.pedidos_itens (
    id uuid NOT NULL,
    pedido_compra_id uuid NOT NULL,
    insumo_material_id uuid NOT NULL,
    quantidade numeric(12,3) NOT NULL,
    valor_unitario numeric(12,2) NOT NULL
);


ALTER TABLE public.pedidos_itens OWNER TO labvida;

--
-- Name: perfil_permissao; Type: TABLE; Schema: public; Owner: labvida
--

CREATE TABLE public.perfil_permissao (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    perfil_id uuid NOT NULL,
    permissao_id uuid NOT NULL
);


ALTER TABLE public.perfil_permissao OWNER TO labvida;

--
-- Name: perfis; Type: TABLE; Schema: public; Owner: labvida
--

CREATE TABLE public.perfis (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    nome character varying(60) NOT NULL,
    descricao text
);


ALTER TABLE public.perfis OWNER TO labvida;

--
-- Name: permissoes; Type: TABLE; Schema: public; Owner: labvida
--

CREATE TABLE public.permissoes (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    codigo character varying(80) NOT NULL,
    descricao text
);


ALTER TABLE public.permissoes OWNER TO labvida;

--
-- Name: procedimento_analitos; Type: TABLE; Schema: public; Owner: labvida
--

CREATE TABLE public.procedimento_analitos (
    procedimento_id uuid NOT NULL,
    analito_id uuid NOT NULL,
    ordem smallint DEFAULT '1'::smallint NOT NULL
);


ALTER TABLE public.procedimento_analitos OWNER TO labvida;

--
-- Name: procedimento_valores; Type: TABLE; Schema: public; Owner: labvida
--

CREATE TABLE public.procedimento_valores (
    id uuid NOT NULL,
    procedimento_id uuid NOT NULL,
    convenio_id uuid,
    valor numeric(12,2) NOT NULL,
    vigencia_inicio date NOT NULL,
    vigencia_fim date,
    CONSTRAINT ck_pv_valor CHECK ((valor >= (0)::numeric)),
    CONSTRAINT ck_pv_vigencia CHECK (((vigencia_fim IS NULL) OR (vigencia_fim >= vigencia_inicio)))
);


ALTER TABLE public.procedimento_valores OWNER TO labvida;

--
-- Name: procedimentos; Type: TABLE; Schema: public; Owner: labvida
--

CREATE TABLE public.procedimentos (
    id uuid NOT NULL,
    codigo_tuss character varying(10) NOT NULL,
    nome character varying(120) NOT NULL,
    setor character varying(60),
    ativo boolean NOT NULL,
    mnemonico character varying(20),
    tipo_material character varying(40),
    metodo character varying(80),
    prazo_entrega_dias smallint,
    preparo_paciente text,
    CONSTRAINT ck_procedimento_prazo CHECK (((prazo_entrega_dias IS NULL) OR ((prazo_entrega_dias >= 0) AND (prazo_entrega_dias <= 365))))
);


ALTER TABLE public.procedimentos OWNER TO labvida;

--
-- Name: procedimentos_insumos; Type: TABLE; Schema: public; Owner: labvida
--

CREATE TABLE public.procedimentos_insumos (
    id uuid NOT NULL,
    procedimento_id uuid NOT NULL,
    insumo_material_id uuid NOT NULL,
    quantidade_necessaria numeric(12,3) DEFAULT 1.000 NOT NULL
);


ALTER TABLE public.procedimentos_insumos OWNER TO labvida;

--
-- Name: protocolos_recebimento; Type: TABLE; Schema: public; Owner: labvida
--

CREATE TABLE public.protocolos_recebimento (
    id uuid NOT NULL,
    malote_id uuid NOT NULL,
    recebido_por_usuario_id uuid NOT NULL,
    integridade_ok boolean NOT NULL,
    observacao text,
    recebido_em timestamp with time zone NOT NULL
);


ALTER TABLE public.protocolos_recebimento OWNER TO labvida;

--
-- Name: recebimentos_insumo; Type: TABLE; Schema: public; Owner: labvida
--

CREATE TABLE public.recebimentos_insumo (
    id uuid NOT NULL,
    pedido_compra_id uuid NOT NULL,
    recebido_em timestamp with time zone DEFAULT now() NOT NULL,
    conferido boolean DEFAULT true NOT NULL
);


ALTER TABLE public.recebimentos_insumo OWNER TO labvida;

--
-- Name: resultados; Type: TABLE; Schema: public; Owner: labvida
--

CREATE TABLE public.resultados (
    id uuid NOT NULL,
    os_item_id uuid NOT NULL,
    equipamento_id uuid,
    analito character varying(120) NOT NULL,
    valor character varying(255) NOT NULL,
    status public.status_resultado DEFAULT 'AGUARDANDO_REVISAO'::public.status_resultado NOT NULL,
    importado_em timestamp with time zone DEFAULT now() NOT NULL,
    analito_id uuid,
    valor_numerico numeric(14,4)
);


ALTER TABLE public.resultados OWNER TO labvida;

--
-- Name: resultados_auditoria; Type: TABLE; Schema: public; Owner: labvida
--

CREATE TABLE public.resultados_auditoria (
    id uuid NOT NULL,
    resultado_id uuid NOT NULL,
    usuario_id uuid NOT NULL,
    valor_anterior character varying(255) NOT NULL,
    valor_novo character varying(255) NOT NULL,
    ocorrido_em timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.resultados_auditoria OWNER TO labvida;

--
-- Name: setores; Type: TABLE; Schema: public; Owner: labvida
--

CREATE TABLE public.setores (
    id uuid NOT NULL,
    unidade_id uuid NOT NULL,
    nome character varying(120) NOT NULL,
    ativo boolean NOT NULL
);


ALTER TABLE public.setores OWNER TO labvida;

--
-- Name: solicitacoes_compra; Type: TABLE; Schema: public; Owner: labvida
--

CREATE TABLE public.solicitacoes_compra (
    id uuid NOT NULL,
    solicitante_id uuid NOT NULL,
    status character varying(20) DEFAULT 'ABERTA'::character varying NOT NULL,
    criada_em timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.solicitacoes_compra OWNER TO labvida;

--
-- Name: titulos_pagar; Type: TABLE; Schema: public; Owner: labvida
--

CREATE TABLE public.titulos_pagar (
    id uuid NOT NULL,
    pedido_compra_id uuid,
    valor numeric(12,2) NOT NULL,
    vencimento date NOT NULL,
    status character varying(20) DEFAULT 'PENDENTE'::character varying NOT NULL,
    criado_em timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.titulos_pagar OWNER TO labvida;

--
-- Name: titulos_receber; Type: TABLE; Schema: public; Owner: labvida
--

CREATE TABLE public.titulos_receber (
    id uuid NOT NULL,
    lote_faturamento_id uuid NOT NULL,
    valor numeric(12,2) NOT NULL,
    vencimento date NOT NULL,
    status character varying(20) DEFAULT 'PENDENTE'::character varying NOT NULL,
    criado_em timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.titulos_receber OWNER TO labvida;

--
-- Name: unidades; Type: TABLE; Schema: public; Owner: labvida
--

CREATE TABLE public.unidades (
    id uuid NOT NULL,
    nome character varying(120) NOT NULL,
    tipo character varying(7) NOT NULL,
    endereco character varying(255),
    ativo boolean NOT NULL,
    CONSTRAINT ck_unidade_tipo CHECK (((tipo)::text = ANY ((ARRAY['CENTRAL'::character varying, 'COLETA'::character varying])::text[])))
);


ALTER TABLE public.unidades OWNER TO labvida;

--
-- Name: usuarios; Type: TABLE; Schema: public; Owner: labvida
--

CREATE TABLE public.usuarios (
    id uuid NOT NULL,
    email character varying(255) NOT NULL,
    nome character varying(120) NOT NULL,
    ativo boolean NOT NULL,
    perfil_id uuid,
    senha_hash character varying(255),
    senha_definida_em timestamp with time zone
);


ALTER TABLE public.usuarios OWNER TO labvida;

--
-- Name: valores_referencia; Type: TABLE; Schema: public; Owner: labvida
--

CREATE TABLE public.valores_referencia (
    id uuid NOT NULL,
    procedimento_id uuid NOT NULL,
    analito character varying(120) NOT NULL,
    minimo numeric(10,4),
    maximo numeric(10,4),
    valor_esperado_texto character varying(255),
    unidade_medida character varying(50),
    analito_id uuid,
    sexo character varying(20),
    idade_min smallint,
    idade_max smallint,
    CONSTRAINT ck_vr_idade CHECK (((idade_min IS NULL) OR (idade_max IS NULL) OR (idade_max >= idade_min))),
    CONSTRAINT ck_vr_sexo CHECK (((sexo IS NULL) OR ((sexo)::text = ANY ((ARRAY['MASCULINO'::character varying, 'FEMININO'::character varying])::text[]))))
);


ALTER TABLE public.valores_referencia OWNER TO labvida;

--
-- Name: bi_dim_convenio sk_convenio; Type: DEFAULT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.bi_dim_convenio ALTER COLUMN sk_convenio SET DEFAULT nextval('public.bi_dim_convenio_sk_convenio_seq'::regclass);


--
-- Name: bi_dim_faixa_etaria sk_faixa_etaria; Type: DEFAULT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.bi_dim_faixa_etaria ALTER COLUMN sk_faixa_etaria SET DEFAULT nextval('public.bi_dim_faixa_etaria_sk_faixa_etaria_seq'::regclass);


--
-- Name: bi_dim_motivo_glosa sk_motivo_glosa; Type: DEFAULT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.bi_dim_motivo_glosa ALTER COLUMN sk_motivo_glosa SET DEFAULT nextval('public.bi_dim_motivo_glosa_sk_motivo_glosa_seq'::regclass);


--
-- Name: bi_dim_paciente_anon sk_paciente; Type: DEFAULT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.bi_dim_paciente_anon ALTER COLUMN sk_paciente SET DEFAULT nextval('public.bi_dim_paciente_anon_sk_paciente_seq'::regclass);


--
-- Name: bi_dim_procedimento sk_procedimento; Type: DEFAULT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.bi_dim_procedimento ALTER COLUMN sk_procedimento SET DEFAULT nextval('public.bi_dim_procedimento_sk_procedimento_seq'::regclass);


--
-- Name: bi_dim_setor sk_setor; Type: DEFAULT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.bi_dim_setor ALTER COLUMN sk_setor SET DEFAULT nextval('public.bi_dim_setor_sk_setor_seq'::regclass);


--
-- Name: bi_dim_tempo sk_tempo; Type: DEFAULT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.bi_dim_tempo ALTER COLUMN sk_tempo SET DEFAULT nextval('public.bi_dim_tempo_sk_tempo_seq'::regclass);


--
-- Name: bi_dim_unidade sk_unidade; Type: DEFAULT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.bi_dim_unidade ALTER COLUMN sk_unidade SET DEFAULT nextval('public.bi_dim_unidade_sk_unidade_seq'::regclass);


--
-- Name: bi_fato_atendimento sk_fato; Type: DEFAULT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.bi_fato_atendimento ALTER COLUMN sk_fato SET DEFAULT nextval('public.bi_fato_atendimento_sk_fato_seq'::regclass);


--
-- Name: bi_fato_faturamento sk_fato; Type: DEFAULT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.bi_fato_faturamento ALTER COLUMN sk_fato SET DEFAULT nextval('public.bi_fato_faturamento_sk_fato_seq'::regclass);


--
-- Name: bi_fato_financeiro sk_fato; Type: DEFAULT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.bi_fato_financeiro ALTER COLUMN sk_fato SET DEFAULT nextval('public.bi_fato_financeiro_sk_fato_seq'::regclass);


--
-- Name: bi_fato_glosa sk_fato; Type: DEFAULT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.bi_fato_glosa ALTER COLUMN sk_fato SET DEFAULT nextval('public.bi_fato_glosa_sk_fato_seq'::regclass);


--
-- Name: bi_fato_logistica sk_fato; Type: DEFAULT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.bi_fato_logistica ALTER COLUMN sk_fato SET DEFAULT nextval('public.bi_fato_logistica_sk_fato_seq'::regclass);


--
-- Name: bi_fato_ordem_servico sk_fato; Type: DEFAULT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.bi_fato_ordem_servico ALTER COLUMN sk_fato SET DEFAULT nextval('public.bi_fato_ordem_servico_sk_fato_seq'::regclass);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: amostras_movimentacoes amostras_movimentacoes_pkey; Type: CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.amostras_movimentacoes
    ADD CONSTRAINT amostras_movimentacoes_pkey PRIMARY KEY (id);


--
-- Name: amostras amostras_pkey; Type: CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.amostras
    ADD CONSTRAINT amostras_pkey PRIMARY KEY (id);


--
-- Name: analitos analitos_codigo_key; Type: CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.analitos
    ADD CONSTRAINT analitos_codigo_key UNIQUE (codigo);


--
-- Name: analitos analitos_pkey; Type: CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.analitos
    ADD CONSTRAINT analitos_pkey PRIMARY KEY (id);


--
-- Name: auditoria_log auditoria_log_pkey; Type: CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.auditoria_log
    ADD CONSTRAINT auditoria_log_pkey PRIMARY KEY (id);


--
-- Name: autorizacoes_convenio autorizacoes_convenio_pkey; Type: CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.autorizacoes_convenio
    ADD CONSTRAINT autorizacoes_convenio_pkey PRIMARY KEY (id);


--
-- Name: bi_dim_convenio bi_dim_convenio_id_origem_key; Type: CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.bi_dim_convenio
    ADD CONSTRAINT bi_dim_convenio_id_origem_key UNIQUE (id_origem);


--
-- Name: bi_dim_convenio bi_dim_convenio_pkey; Type: CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.bi_dim_convenio
    ADD CONSTRAINT bi_dim_convenio_pkey PRIMARY KEY (sk_convenio);


--
-- Name: bi_dim_faixa_etaria bi_dim_faixa_etaria_chave_natural_key; Type: CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.bi_dim_faixa_etaria
    ADD CONSTRAINT bi_dim_faixa_etaria_chave_natural_key UNIQUE (chave_natural);


--
-- Name: bi_dim_faixa_etaria bi_dim_faixa_etaria_pkey; Type: CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.bi_dim_faixa_etaria
    ADD CONSTRAINT bi_dim_faixa_etaria_pkey PRIMARY KEY (sk_faixa_etaria);


--
-- Name: bi_dim_motivo_glosa bi_dim_motivo_glosa_chave_natural_key; Type: CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.bi_dim_motivo_glosa
    ADD CONSTRAINT bi_dim_motivo_glosa_chave_natural_key UNIQUE (chave_natural);


--
-- Name: bi_dim_motivo_glosa bi_dim_motivo_glosa_pkey; Type: CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.bi_dim_motivo_glosa
    ADD CONSTRAINT bi_dim_motivo_glosa_pkey PRIMARY KEY (sk_motivo_glosa);


--
-- Name: bi_dim_paciente_anon bi_dim_paciente_anon_id_origem_key; Type: CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.bi_dim_paciente_anon
    ADD CONSTRAINT bi_dim_paciente_anon_id_origem_key UNIQUE (id_origem);


--
-- Name: bi_dim_paciente_anon bi_dim_paciente_anon_pkey; Type: CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.bi_dim_paciente_anon
    ADD CONSTRAINT bi_dim_paciente_anon_pkey PRIMARY KEY (sk_paciente);


--
-- Name: bi_dim_procedimento bi_dim_procedimento_id_origem_key; Type: CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.bi_dim_procedimento
    ADD CONSTRAINT bi_dim_procedimento_id_origem_key UNIQUE (id_origem);


--
-- Name: bi_dim_procedimento bi_dim_procedimento_pkey; Type: CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.bi_dim_procedimento
    ADD CONSTRAINT bi_dim_procedimento_pkey PRIMARY KEY (sk_procedimento);


--
-- Name: bi_dim_setor bi_dim_setor_chave_natural_key; Type: CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.bi_dim_setor
    ADD CONSTRAINT bi_dim_setor_chave_natural_key UNIQUE (chave_natural);


--
-- Name: bi_dim_setor bi_dim_setor_pkey; Type: CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.bi_dim_setor
    ADD CONSTRAINT bi_dim_setor_pkey PRIMARY KEY (sk_setor);


--
-- Name: bi_dim_tempo bi_dim_tempo_data_key; Type: CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.bi_dim_tempo
    ADD CONSTRAINT bi_dim_tempo_data_key UNIQUE (data);


--
-- Name: bi_dim_tempo bi_dim_tempo_pkey; Type: CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.bi_dim_tempo
    ADD CONSTRAINT bi_dim_tempo_pkey PRIMARY KEY (sk_tempo);


--
-- Name: bi_dim_unidade bi_dim_unidade_id_origem_key; Type: CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.bi_dim_unidade
    ADD CONSTRAINT bi_dim_unidade_id_origem_key UNIQUE (id_origem);


--
-- Name: bi_dim_unidade bi_dim_unidade_pkey; Type: CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.bi_dim_unidade
    ADD CONSTRAINT bi_dim_unidade_pkey PRIMARY KEY (sk_unidade);


--
-- Name: bi_etl_execucao bi_etl_execucao_pkey; Type: CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.bi_etl_execucao
    ADD CONSTRAINT bi_etl_execucao_pkey PRIMARY KEY (id);


--
-- Name: bi_fato_atendimento bi_fato_atendimento_os_item_id_key; Type: CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.bi_fato_atendimento
    ADD CONSTRAINT bi_fato_atendimento_os_item_id_key UNIQUE (os_item_id);


--
-- Name: bi_fato_atendimento bi_fato_atendimento_pkey; Type: CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.bi_fato_atendimento
    ADD CONSTRAINT bi_fato_atendimento_pkey PRIMARY KEY (sk_fato);


--
-- Name: bi_fato_faturamento bi_fato_faturamento_guia_item_id_key; Type: CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.bi_fato_faturamento
    ADD CONSTRAINT bi_fato_faturamento_guia_item_id_key UNIQUE (guia_item_id);


--
-- Name: bi_fato_faturamento bi_fato_faturamento_pkey; Type: CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.bi_fato_faturamento
    ADD CONSTRAINT bi_fato_faturamento_pkey PRIMARY KEY (sk_fato);


--
-- Name: bi_fato_financeiro bi_fato_financeiro_pkey; Type: CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.bi_fato_financeiro
    ADD CONSTRAINT bi_fato_financeiro_pkey PRIMARY KEY (sk_fato);


--
-- Name: bi_fato_glosa bi_fato_glosa_glosa_id_key; Type: CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.bi_fato_glosa
    ADD CONSTRAINT bi_fato_glosa_glosa_id_key UNIQUE (glosa_id);


--
-- Name: bi_fato_glosa bi_fato_glosa_pkey; Type: CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.bi_fato_glosa
    ADD CONSTRAINT bi_fato_glosa_pkey PRIMARY KEY (sk_fato);


--
-- Name: bi_fato_logistica bi_fato_logistica_amostra_id_key; Type: CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.bi_fato_logistica
    ADD CONSTRAINT bi_fato_logistica_amostra_id_key UNIQUE (amostra_id);


--
-- Name: bi_fato_logistica bi_fato_logistica_pkey; Type: CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.bi_fato_logistica
    ADD CONSTRAINT bi_fato_logistica_pkey PRIMARY KEY (sk_fato);


--
-- Name: bi_fato_ordem_servico bi_fato_ordem_servico_ordem_servico_id_key; Type: CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.bi_fato_ordem_servico
    ADD CONSTRAINT bi_fato_ordem_servico_ordem_servico_id_key UNIQUE (ordem_servico_id);


--
-- Name: bi_fato_ordem_servico bi_fato_ordem_servico_pkey; Type: CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.bi_fato_ordem_servico
    ADD CONSTRAINT bi_fato_ordem_servico_pkey PRIMARY KEY (sk_fato);


--
-- Name: coletas coletas_pkey; Type: CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.coletas
    ADD CONSTRAINT coletas_pkey PRIMARY KEY (id);


--
-- Name: competencias competencias_pkey; Type: CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.competencias
    ADD CONSTRAINT competencias_pkey PRIMARY KEY (competencia);


--
-- Name: conciliacoes_pagamento conciliacoes_pagamento_pkey; Type: CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.conciliacoes_pagamento
    ADD CONSTRAINT conciliacoes_pagamento_pkey PRIMARY KEY (id);


--
-- Name: convenios convenios_pkey; Type: CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.convenios
    ADD CONSTRAINT convenios_pkey PRIMARY KEY (id);


--
-- Name: equipamentos equipamentos_pkey; Type: CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.equipamentos
    ADD CONSTRAINT equipamentos_pkey PRIMARY KEY (id);


--
-- Name: estoque_movimentos estoque_movimentos_pkey; Type: CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.estoque_movimentos
    ADD CONSTRAINT estoque_movimentos_pkey PRIMARY KEY (id);


--
-- Name: procedimento_valores ex_pv_sem_sobreposicao; Type: CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.procedimento_valores
    ADD CONSTRAINT ex_pv_sem_sobreposicao EXCLUDE USING gist (procedimento_id WITH =, COALESCE(convenio_id, '00000000-0000-0000-0000-000000000000'::uuid) WITH =, daterange(vigencia_inicio, COALESCE(vigencia_fim, 'infinity'::date), '[]'::text) WITH &&);


--
-- Name: fornecedores fornecedores_cnpj_key; Type: CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.fornecedores
    ADD CONSTRAINT fornecedores_cnpj_key UNIQUE (cnpj);


--
-- Name: fornecedores fornecedores_pkey; Type: CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.fornecedores
    ADD CONSTRAINT fornecedores_pkey PRIMARY KEY (id);


--
-- Name: glosas glosas_pkey; Type: CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.glosas
    ADD CONSTRAINT glosas_pkey PRIMARY KEY (id);


--
-- Name: guias_itens guias_itens_laudo_id_key; Type: CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.guias_itens
    ADD CONSTRAINT guias_itens_laudo_id_key UNIQUE (laudo_id);


--
-- Name: guias_itens guias_itens_pkey; Type: CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.guias_itens
    ADD CONSTRAINT guias_itens_pkey PRIMARY KEY (id);


--
-- Name: guias_tiss guias_tiss_pkey; Type: CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.guias_tiss
    ADD CONSTRAINT guias_tiss_pkey PRIMARY KEY (id);


--
-- Name: insumos_materiais insumos_materiais_pkey; Type: CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.insumos_materiais
    ADD CONSTRAINT insumos_materiais_pkey PRIMARY KEY (id);


--
-- Name: laudos laudos_os_item_id_key; Type: CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.laudos
    ADD CONSTRAINT laudos_os_item_id_key UNIQUE (os_item_id);


--
-- Name: laudos laudos_pkey; Type: CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.laudos
    ADD CONSTRAINT laudos_pkey PRIMARY KEY (id);


--
-- Name: lotes_faturamento lotes_faturamento_pkey; Type: CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.lotes_faturamento
    ADD CONSTRAINT lotes_faturamento_pkey PRIMARY KEY (id);


--
-- Name: malotes_amostras malotes_amostras_pkey; Type: CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.malotes_amostras
    ADD CONSTRAINT malotes_amostras_pkey PRIMARY KEY (id);


--
-- Name: malotes malotes_pkey; Type: CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.malotes
    ADD CONSTRAINT malotes_pkey PRIMARY KEY (id);


--
-- Name: medicos medicos_pkey; Type: CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.medicos
    ADD CONSTRAINT medicos_pkey PRIMARY KEY (id);


--
-- Name: movimentos_caixa movimentos_caixa_pkey; Type: CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.movimentos_caixa
    ADD CONSTRAINT movimentos_caixa_pkey PRIMARY KEY (id);


--
-- Name: ordens_servico ordens_servico_pkey; Type: CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.ordens_servico
    ADD CONSTRAINT ordens_servico_pkey PRIMARY KEY (id);


--
-- Name: os_itens os_itens_pkey; Type: CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.os_itens
    ADD CONSTRAINT os_itens_pkey PRIMARY KEY (id);


--
-- Name: os_status_historico os_status_historico_pkey; Type: CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.os_status_historico
    ADD CONSTRAINT os_status_historico_pkey PRIMARY KEY (id);


--
-- Name: pacientes pacientes_pkey; Type: CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.pacientes
    ADD CONSTRAINT pacientes_pkey PRIMARY KEY (id);


--
-- Name: pedidos_compra pedidos_compra_pkey; Type: CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.pedidos_compra
    ADD CONSTRAINT pedidos_compra_pkey PRIMARY KEY (id);


--
-- Name: pedidos_itens pedidos_itens_pkey; Type: CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.pedidos_itens
    ADD CONSTRAINT pedidos_itens_pkey PRIMARY KEY (id);


--
-- Name: perfil_permissao perfil_permissao_pkey; Type: CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.perfil_permissao
    ADD CONSTRAINT perfil_permissao_pkey PRIMARY KEY (id);


--
-- Name: perfis perfis_nome_key; Type: CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.perfis
    ADD CONSTRAINT perfis_nome_key UNIQUE (nome);


--
-- Name: perfis perfis_pkey; Type: CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.perfis
    ADD CONSTRAINT perfis_pkey PRIMARY KEY (id);


--
-- Name: permissoes permissoes_codigo_key; Type: CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.permissoes
    ADD CONSTRAINT permissoes_codigo_key UNIQUE (codigo);


--
-- Name: permissoes permissoes_pkey; Type: CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.permissoes
    ADD CONSTRAINT permissoes_pkey PRIMARY KEY (id);


--
-- Name: procedimento_analitos procedimento_analitos_pkey; Type: CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.procedimento_analitos
    ADD CONSTRAINT procedimento_analitos_pkey PRIMARY KEY (procedimento_id, analito_id);


--
-- Name: procedimento_valores procedimento_valores_pkey; Type: CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.procedimento_valores
    ADD CONSTRAINT procedimento_valores_pkey PRIMARY KEY (id);


--
-- Name: procedimentos_insumos procedimentos_insumos_pkey; Type: CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.procedimentos_insumos
    ADD CONSTRAINT procedimentos_insumos_pkey PRIMARY KEY (id);


--
-- Name: procedimentos procedimentos_pkey; Type: CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.procedimentos
    ADD CONSTRAINT procedimentos_pkey PRIMARY KEY (id);


--
-- Name: protocolos_recebimento protocolos_recebimento_pkey; Type: CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.protocolos_recebimento
    ADD CONSTRAINT protocolos_recebimento_pkey PRIMARY KEY (id);


--
-- Name: recebimentos_insumo recebimentos_insumo_pkey; Type: CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.recebimentos_insumo
    ADD CONSTRAINT recebimentos_insumo_pkey PRIMARY KEY (id);


--
-- Name: resultados_auditoria resultados_auditoria_pkey; Type: CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.resultados_auditoria
    ADD CONSTRAINT resultados_auditoria_pkey PRIMARY KEY (id);


--
-- Name: resultados resultados_pkey; Type: CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.resultados
    ADD CONSTRAINT resultados_pkey PRIMARY KEY (id);


--
-- Name: setores setores_pkey; Type: CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.setores
    ADD CONSTRAINT setores_pkey PRIMARY KEY (id);


--
-- Name: solicitacoes_compra solicitacoes_compra_pkey; Type: CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.solicitacoes_compra
    ADD CONSTRAINT solicitacoes_compra_pkey PRIMARY KEY (id);


--
-- Name: titulos_pagar titulos_pagar_pkey; Type: CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.titulos_pagar
    ADD CONSTRAINT titulos_pagar_pkey PRIMARY KEY (id);


--
-- Name: titulos_receber titulos_receber_pkey; Type: CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.titulos_receber
    ADD CONSTRAINT titulos_receber_pkey PRIMARY KEY (id);


--
-- Name: unidades unidades_pkey; Type: CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.unidades
    ADD CONSTRAINT unidades_pkey PRIMARY KEY (id);


--
-- Name: bi_fato_financeiro uq_fato_financeiro_origem; Type: CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.bi_fato_financeiro
    ADD CONSTRAINT uq_fato_financeiro_origem UNIQUE (regime, origem_tabela, origem_id);


--
-- Name: medicos uq_medico_crm_uf; Type: CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.medicos
    ADD CONSTRAINT uq_medico_crm_uf UNIQUE (crm, uf_crm);


--
-- Name: pacientes uq_pacientes_cpf_hash; Type: CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.pacientes
    ADD CONSTRAINT uq_pacientes_cpf_hash UNIQUE (cpf_hash);


--
-- Name: procedimentos_insumos uq_procedimento_insumo; Type: CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.procedimentos_insumos
    ADD CONSTRAINT uq_procedimento_insumo UNIQUE (procedimento_id, insumo_material_id);


--
-- Name: usuarios usuarios_pkey; Type: CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_pkey PRIMARY KEY (id);


--
-- Name: valores_referencia valores_referencia_pkey; Type: CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.valores_referencia
    ADD CONSTRAINT valores_referencia_pkey PRIMARY KEY (id);


--
-- Name: idx_auditoria_entidade; Type: INDEX; Schema: public; Owner: labvida
--

CREATE INDEX idx_auditoria_entidade ON public.auditoria_log USING btree (entidade, entidade_id);


--
-- Name: idx_perfil_permissao_perfil; Type: INDEX; Schema: public; Owner: labvida
--

CREATE INDEX idx_perfil_permissao_perfil ON public.perfil_permissao USING btree (perfil_id);


--
-- Name: idx_perfil_permissao_permissao; Type: INDEX; Schema: public; Owner: labvida
--

CREATE INDEX idx_perfil_permissao_permissao ON public.perfil_permissao USING btree (permissao_id);


--
-- Name: ix_amostras_codigo_barras; Type: INDEX; Schema: public; Owner: labvida
--

CREATE UNIQUE INDEX ix_amostras_codigo_barras ON public.amostras USING btree (codigo_barras);


--
-- Name: ix_amostras_movimentacoes_amostra_id; Type: INDEX; Schema: public; Owner: labvida
--

CREATE INDEX ix_amostras_movimentacoes_amostra_id ON public.amostras_movimentacoes USING btree (amostra_id);


--
-- Name: ix_amostras_ordem_servico_id; Type: INDEX; Schema: public; Owner: labvida
--

CREATE INDEX ix_amostras_ordem_servico_id ON public.amostras USING btree (ordem_servico_id);


--
-- Name: ix_analitos_nome; Type: INDEX; Schema: public; Owner: labvida
--

CREATE INDEX ix_analitos_nome ON public.analitos USING btree (nome);


--
-- Name: ix_auditoria_log_usuario_id; Type: INDEX; Schema: public; Owner: labvida
--

CREATE INDEX ix_auditoria_log_usuario_id ON public.auditoria_log USING btree (usuario_id);


--
-- Name: ix_autorizacoes_convenio_ordem_servico_id; Type: INDEX; Schema: public; Owner: labvida
--

CREATE INDEX ix_autorizacoes_convenio_ordem_servico_id ON public.autorizacoes_convenio USING btree (ordem_servico_id);


--
-- Name: ix_bi_dim_tempo_ano_mes; Type: INDEX; Schema: public; Owner: labvida
--

CREATE INDEX ix_bi_dim_tempo_ano_mes ON public.bi_dim_tempo USING btree (ano_mes);


--
-- Name: ix_bi_dim_tempo_competencia; Type: INDEX; Schema: public; Owner: labvida
--

CREATE INDEX ix_bi_dim_tempo_competencia ON public.bi_dim_tempo USING btree (competencia);


--
-- Name: ix_bi_dim_tempo_data; Type: INDEX; Schema: public; Owner: labvida
--

CREATE INDEX ix_bi_dim_tempo_data ON public.bi_dim_tempo USING btree (data);


--
-- Name: ix_bi_fato_atendimento_natural; Type: INDEX; Schema: public; Owner: labvida
--

CREATE INDEX ix_bi_fato_atendimento_natural ON public.bi_fato_atendimento USING btree (os_item_id);


--
-- Name: ix_bi_fato_faturamento_natural; Type: INDEX; Schema: public; Owner: labvida
--

CREATE INDEX ix_bi_fato_faturamento_natural ON public.bi_fato_faturamento USING btree (guia_item_id);


--
-- Name: ix_bi_fato_financeiro_regime; Type: INDEX; Schema: public; Owner: labvida
--

CREATE INDEX ix_bi_fato_financeiro_regime ON public.bi_fato_financeiro USING btree (regime);


--
-- Name: ix_bi_fato_glosa_natural; Type: INDEX; Schema: public; Owner: labvida
--

CREATE INDEX ix_bi_fato_glosa_natural ON public.bi_fato_glosa USING btree (glosa_id);


--
-- Name: ix_bi_fato_logistica_natural; Type: INDEX; Schema: public; Owner: labvida
--

CREATE INDEX ix_bi_fato_logistica_natural ON public.bi_fato_logistica USING btree (amostra_id);


--
-- Name: ix_bi_fato_os_natural; Type: INDEX; Schema: public; Owner: labvida
--

CREATE INDEX ix_bi_fato_os_natural ON public.bi_fato_ordem_servico USING btree (ordem_servico_id);


--
-- Name: ix_coletas_amostra_id; Type: INDEX; Schema: public; Owner: labvida
--

CREATE UNIQUE INDEX ix_coletas_amostra_id ON public.coletas USING btree (amostra_id);


--
-- Name: ix_competencias_status; Type: INDEX; Schema: public; Owner: labvida
--

CREATE INDEX ix_competencias_status ON public.competencias USING btree (status);


--
-- Name: ix_convenios_cnpj; Type: INDEX; Schema: public; Owner: labvida
--

CREATE UNIQUE INDEX ix_convenios_cnpj ON public.convenios USING btree (cnpj);


--
-- Name: ix_convenios_nome_normalizado; Type: INDEX; Schema: public; Owner: labvida
--

CREATE UNIQUE INDEX ix_convenios_nome_normalizado ON public.convenios USING btree (nome_normalizado);


--
-- Name: ix_lotes_faturamento_codigo_lote; Type: INDEX; Schema: public; Owner: labvida
--

CREATE UNIQUE INDEX ix_lotes_faturamento_codigo_lote ON public.lotes_faturamento USING btree (codigo_lote);


--
-- Name: ix_lotes_faturamento_competencia; Type: INDEX; Schema: public; Owner: labvida
--

CREATE INDEX ix_lotes_faturamento_competencia ON public.lotes_faturamento USING btree (competencia);


--
-- Name: ix_malotes_amostras_amostra_id; Type: INDEX; Schema: public; Owner: labvida
--

CREATE UNIQUE INDEX ix_malotes_amostras_amostra_id ON public.malotes_amostras USING btree (amostra_id);


--
-- Name: ix_malotes_amostras_malote_id; Type: INDEX; Schema: public; Owner: labvida
--

CREATE INDEX ix_malotes_amostras_malote_id ON public.malotes_amostras USING btree (malote_id);


--
-- Name: ix_malotes_codigo_malote; Type: INDEX; Schema: public; Owner: labvida
--

CREATE UNIQUE INDEX ix_malotes_codigo_malote ON public.malotes USING btree (codigo_malote);


--
-- Name: ix_malotes_unidade_destino_id; Type: INDEX; Schema: public; Owner: labvida
--

CREATE INDEX ix_malotes_unidade_destino_id ON public.malotes USING btree (unidade_destino_id);


--
-- Name: ix_malotes_unidade_origem_id; Type: INDEX; Schema: public; Owner: labvida
--

CREATE INDEX ix_malotes_unidade_origem_id ON public.malotes USING btree (unidade_origem_id);


--
-- Name: ix_medicos_crm; Type: INDEX; Schema: public; Owner: labvida
--

CREATE INDEX ix_medicos_crm ON public.medicos USING btree (crm);


--
-- Name: ix_ordens_servico_codigo_os; Type: INDEX; Schema: public; Owner: labvida
--

CREATE UNIQUE INDEX ix_ordens_servico_codigo_os ON public.ordens_servico USING btree (codigo_os);


--
-- Name: ix_ordens_servico_paciente_id; Type: INDEX; Schema: public; Owner: labvida
--

CREATE INDEX ix_ordens_servico_paciente_id ON public.ordens_servico USING btree (paciente_id);


--
-- Name: ix_ordens_servico_unidade_id; Type: INDEX; Schema: public; Owner: labvida
--

CREATE INDEX ix_ordens_servico_unidade_id ON public.ordens_servico USING btree (unidade_id);


--
-- Name: ix_os_itens_ordem_servico_id; Type: INDEX; Schema: public; Owner: labvida
--

CREATE INDEX ix_os_itens_ordem_servico_id ON public.os_itens USING btree (ordem_servico_id);


--
-- Name: ix_os_status_historico_ordem_servico_id; Type: INDEX; Schema: public; Owner: labvida
--

CREATE INDEX ix_os_status_historico_ordem_servico_id ON public.os_status_historico USING btree (ordem_servico_id);


--
-- Name: ix_pacientes_cpf_hash; Type: INDEX; Schema: public; Owner: labvida
--

CREATE INDEX ix_pacientes_cpf_hash ON public.pacientes USING btree (cpf_hash);


--
-- Name: ix_procedimento_valores_convenio_id; Type: INDEX; Schema: public; Owner: labvida
--

CREATE INDEX ix_procedimento_valores_convenio_id ON public.procedimento_valores USING btree (convenio_id);


--
-- Name: ix_procedimento_valores_procedimento_id; Type: INDEX; Schema: public; Owner: labvida
--

CREATE INDEX ix_procedimento_valores_procedimento_id ON public.procedimento_valores USING btree (procedimento_id);


--
-- Name: ix_procedimentos_codigo_tuss; Type: INDEX; Schema: public; Owner: labvida
--

CREATE UNIQUE INDEX ix_procedimentos_codigo_tuss ON public.procedimentos USING btree (codigo_tuss);


--
-- Name: ix_procedimentos_insumos_insumo_material_id; Type: INDEX; Schema: public; Owner: labvida
--

CREATE INDEX ix_procedimentos_insumos_insumo_material_id ON public.procedimentos_insumos USING btree (insumo_material_id);


--
-- Name: ix_procedimentos_insumos_procedimento_id; Type: INDEX; Schema: public; Owner: labvida
--

CREATE INDEX ix_procedimentos_insumos_procedimento_id ON public.procedimentos_insumos USING btree (procedimento_id);


--
-- Name: ix_protocolos_recebimento_malote_id; Type: INDEX; Schema: public; Owner: labvida
--

CREATE UNIQUE INDEX ix_protocolos_recebimento_malote_id ON public.protocolos_recebimento USING btree (malote_id);


--
-- Name: ix_resultados_auditoria_resultado_id; Type: INDEX; Schema: public; Owner: labvida
--

CREATE INDEX ix_resultados_auditoria_resultado_id ON public.resultados_auditoria USING btree (resultado_id);


--
-- Name: ix_resultados_os_item_id; Type: INDEX; Schema: public; Owner: labvida
--

CREATE INDEX ix_resultados_os_item_id ON public.resultados USING btree (os_item_id);


--
-- Name: ix_setores_unidade_id; Type: INDEX; Schema: public; Owner: labvida
--

CREATE INDEX ix_setores_unidade_id ON public.setores USING btree (unidade_id);


--
-- Name: ix_usuarios_email; Type: INDEX; Schema: public; Owner: labvida
--

CREATE UNIQUE INDEX ix_usuarios_email ON public.usuarios USING btree (email);


--
-- Name: uq_lote_aberto_convenio_competencia; Type: INDEX; Schema: public; Owner: labvida
--

CREATE UNIQUE INDEX uq_lote_aberto_convenio_competencia ON public.lotes_faturamento USING btree (convenio_id, competencia) NULLS NOT DISTINCT WHERE ((status)::text = 'ABERTO'::text);


--
-- Name: uq_pv_vigencia; Type: INDEX; Schema: public; Owner: labvida
--

CREATE UNIQUE INDEX uq_pv_vigencia ON public.procedimento_valores USING btree (procedimento_id, convenio_id, vigencia_inicio) NULLS NOT DISTINCT;


--
-- Name: amostras_movimentacoes amostras_movimentacoes_amostra_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.amostras_movimentacoes
    ADD CONSTRAINT amostras_movimentacoes_amostra_id_fkey FOREIGN KEY (amostra_id) REFERENCES public.amostras(id);


--
-- Name: amostras_movimentacoes amostras_movimentacoes_unidade_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.amostras_movimentacoes
    ADD CONSTRAINT amostras_movimentacoes_unidade_id_fkey FOREIGN KEY (unidade_id) REFERENCES public.unidades(id);


--
-- Name: amostras_movimentacoes amostras_movimentacoes_usuario_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.amostras_movimentacoes
    ADD CONSTRAINT amostras_movimentacoes_usuario_id_fkey FOREIGN KEY (usuario_id) REFERENCES public.usuarios(id);


--
-- Name: amostras amostras_ordem_servico_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.amostras
    ADD CONSTRAINT amostras_ordem_servico_id_fkey FOREIGN KEY (ordem_servico_id) REFERENCES public.ordens_servico(id);


--
-- Name: auditoria_log auditoria_log_usuario_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.auditoria_log
    ADD CONSTRAINT auditoria_log_usuario_id_fkey FOREIGN KEY (usuario_id) REFERENCES public.usuarios(id);


--
-- Name: autorizacoes_convenio autorizacoes_convenio_ordem_servico_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.autorizacoes_convenio
    ADD CONSTRAINT autorizacoes_convenio_ordem_servico_id_fkey FOREIGN KEY (ordem_servico_id) REFERENCES public.ordens_servico(id);


--
-- Name: bi_dim_procedimento bi_dim_procedimento_sk_setor_fkey; Type: FK CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.bi_dim_procedimento
    ADD CONSTRAINT bi_dim_procedimento_sk_setor_fkey FOREIGN KEY (sk_setor) REFERENCES public.bi_dim_setor(sk_setor);


--
-- Name: bi_fato_atendimento bi_fato_atendimento_sk_convenio_fkey; Type: FK CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.bi_fato_atendimento
    ADD CONSTRAINT bi_fato_atendimento_sk_convenio_fkey FOREIGN KEY (sk_convenio) REFERENCES public.bi_dim_convenio(sk_convenio);


--
-- Name: bi_fato_atendimento bi_fato_atendimento_sk_faixa_etaria_fkey; Type: FK CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.bi_fato_atendimento
    ADD CONSTRAINT bi_fato_atendimento_sk_faixa_etaria_fkey FOREIGN KEY (sk_faixa_etaria) REFERENCES public.bi_dim_faixa_etaria(sk_faixa_etaria);


--
-- Name: bi_fato_atendimento bi_fato_atendimento_sk_paciente_fkey; Type: FK CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.bi_fato_atendimento
    ADD CONSTRAINT bi_fato_atendimento_sk_paciente_fkey FOREIGN KEY (sk_paciente) REFERENCES public.bi_dim_paciente_anon(sk_paciente);


--
-- Name: bi_fato_atendimento bi_fato_atendimento_sk_procedimento_fkey; Type: FK CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.bi_fato_atendimento
    ADD CONSTRAINT bi_fato_atendimento_sk_procedimento_fkey FOREIGN KEY (sk_procedimento) REFERENCES public.bi_dim_procedimento(sk_procedimento);


--
-- Name: bi_fato_atendimento bi_fato_atendimento_sk_setor_fkey; Type: FK CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.bi_fato_atendimento
    ADD CONSTRAINT bi_fato_atendimento_sk_setor_fkey FOREIGN KEY (sk_setor) REFERENCES public.bi_dim_setor(sk_setor);


--
-- Name: bi_fato_atendimento bi_fato_atendimento_sk_tempo_fkey; Type: FK CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.bi_fato_atendimento
    ADD CONSTRAINT bi_fato_atendimento_sk_tempo_fkey FOREIGN KEY (sk_tempo) REFERENCES public.bi_dim_tempo(sk_tempo);


--
-- Name: bi_fato_atendimento bi_fato_atendimento_sk_unidade_fkey; Type: FK CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.bi_fato_atendimento
    ADD CONSTRAINT bi_fato_atendimento_sk_unidade_fkey FOREIGN KEY (sk_unidade) REFERENCES public.bi_dim_unidade(sk_unidade);


--
-- Name: bi_fato_faturamento bi_fato_faturamento_sk_convenio_fkey; Type: FK CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.bi_fato_faturamento
    ADD CONSTRAINT bi_fato_faturamento_sk_convenio_fkey FOREIGN KEY (sk_convenio) REFERENCES public.bi_dim_convenio(sk_convenio);


--
-- Name: bi_fato_faturamento bi_fato_faturamento_sk_paciente_fkey; Type: FK CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.bi_fato_faturamento
    ADD CONSTRAINT bi_fato_faturamento_sk_paciente_fkey FOREIGN KEY (sk_paciente) REFERENCES public.bi_dim_paciente_anon(sk_paciente);


--
-- Name: bi_fato_faturamento bi_fato_faturamento_sk_procedimento_fkey; Type: FK CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.bi_fato_faturamento
    ADD CONSTRAINT bi_fato_faturamento_sk_procedimento_fkey FOREIGN KEY (sk_procedimento) REFERENCES public.bi_dim_procedimento(sk_procedimento);


--
-- Name: bi_fato_faturamento bi_fato_faturamento_sk_setor_fkey; Type: FK CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.bi_fato_faturamento
    ADD CONSTRAINT bi_fato_faturamento_sk_setor_fkey FOREIGN KEY (sk_setor) REFERENCES public.bi_dim_setor(sk_setor);


--
-- Name: bi_fato_faturamento bi_fato_faturamento_sk_tempo_fkey; Type: FK CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.bi_fato_faturamento
    ADD CONSTRAINT bi_fato_faturamento_sk_tempo_fkey FOREIGN KEY (sk_tempo) REFERENCES public.bi_dim_tempo(sk_tempo);


--
-- Name: bi_fato_faturamento bi_fato_faturamento_sk_unidade_fkey; Type: FK CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.bi_fato_faturamento
    ADD CONSTRAINT bi_fato_faturamento_sk_unidade_fkey FOREIGN KEY (sk_unidade) REFERENCES public.bi_dim_unidade(sk_unidade);


--
-- Name: bi_fato_financeiro bi_fato_financeiro_sk_convenio_fkey; Type: FK CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.bi_fato_financeiro
    ADD CONSTRAINT bi_fato_financeiro_sk_convenio_fkey FOREIGN KEY (sk_convenio) REFERENCES public.bi_dim_convenio(sk_convenio);


--
-- Name: bi_fato_financeiro bi_fato_financeiro_sk_tempo_fkey; Type: FK CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.bi_fato_financeiro
    ADD CONSTRAINT bi_fato_financeiro_sk_tempo_fkey FOREIGN KEY (sk_tempo) REFERENCES public.bi_dim_tempo(sk_tempo);


--
-- Name: bi_fato_financeiro bi_fato_financeiro_sk_unidade_fkey; Type: FK CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.bi_fato_financeiro
    ADD CONSTRAINT bi_fato_financeiro_sk_unidade_fkey FOREIGN KEY (sk_unidade) REFERENCES public.bi_dim_unidade(sk_unidade);


--
-- Name: bi_fato_glosa bi_fato_glosa_sk_convenio_fkey; Type: FK CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.bi_fato_glosa
    ADD CONSTRAINT bi_fato_glosa_sk_convenio_fkey FOREIGN KEY (sk_convenio) REFERENCES public.bi_dim_convenio(sk_convenio);


--
-- Name: bi_fato_glosa bi_fato_glosa_sk_motivo_glosa_fkey; Type: FK CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.bi_fato_glosa
    ADD CONSTRAINT bi_fato_glosa_sk_motivo_glosa_fkey FOREIGN KEY (sk_motivo_glosa) REFERENCES public.bi_dim_motivo_glosa(sk_motivo_glosa);


--
-- Name: bi_fato_glosa bi_fato_glosa_sk_procedimento_fkey; Type: FK CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.bi_fato_glosa
    ADD CONSTRAINT bi_fato_glosa_sk_procedimento_fkey FOREIGN KEY (sk_procedimento) REFERENCES public.bi_dim_procedimento(sk_procedimento);


--
-- Name: bi_fato_glosa bi_fato_glosa_sk_tempo_fkey; Type: FK CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.bi_fato_glosa
    ADD CONSTRAINT bi_fato_glosa_sk_tempo_fkey FOREIGN KEY (sk_tempo) REFERENCES public.bi_dim_tempo(sk_tempo);


--
-- Name: bi_fato_glosa bi_fato_glosa_sk_unidade_fkey; Type: FK CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.bi_fato_glosa
    ADD CONSTRAINT bi_fato_glosa_sk_unidade_fkey FOREIGN KEY (sk_unidade) REFERENCES public.bi_dim_unidade(sk_unidade);


--
-- Name: bi_fato_logistica bi_fato_logistica_sk_tempo_fkey; Type: FK CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.bi_fato_logistica
    ADD CONSTRAINT bi_fato_logistica_sk_tempo_fkey FOREIGN KEY (sk_tempo) REFERENCES public.bi_dim_tempo(sk_tempo);


--
-- Name: bi_fato_logistica bi_fato_logistica_sk_unidade_destino_fkey; Type: FK CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.bi_fato_logistica
    ADD CONSTRAINT bi_fato_logistica_sk_unidade_destino_fkey FOREIGN KEY (sk_unidade_destino) REFERENCES public.bi_dim_unidade(sk_unidade);


--
-- Name: bi_fato_logistica bi_fato_logistica_sk_unidade_fkey; Type: FK CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.bi_fato_logistica
    ADD CONSTRAINT bi_fato_logistica_sk_unidade_fkey FOREIGN KEY (sk_unidade) REFERENCES public.bi_dim_unidade(sk_unidade);


--
-- Name: bi_fato_ordem_servico bi_fato_ordem_servico_sk_convenio_fkey; Type: FK CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.bi_fato_ordem_servico
    ADD CONSTRAINT bi_fato_ordem_servico_sk_convenio_fkey FOREIGN KEY (sk_convenio) REFERENCES public.bi_dim_convenio(sk_convenio);


--
-- Name: bi_fato_ordem_servico bi_fato_ordem_servico_sk_faixa_etaria_fkey; Type: FK CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.bi_fato_ordem_servico
    ADD CONSTRAINT bi_fato_ordem_servico_sk_faixa_etaria_fkey FOREIGN KEY (sk_faixa_etaria) REFERENCES public.bi_dim_faixa_etaria(sk_faixa_etaria);


--
-- Name: bi_fato_ordem_servico bi_fato_ordem_servico_sk_paciente_fkey; Type: FK CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.bi_fato_ordem_servico
    ADD CONSTRAINT bi_fato_ordem_servico_sk_paciente_fkey FOREIGN KEY (sk_paciente) REFERENCES public.bi_dim_paciente_anon(sk_paciente);


--
-- Name: bi_fato_ordem_servico bi_fato_ordem_servico_sk_tempo_fkey; Type: FK CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.bi_fato_ordem_servico
    ADD CONSTRAINT bi_fato_ordem_servico_sk_tempo_fkey FOREIGN KEY (sk_tempo) REFERENCES public.bi_dim_tempo(sk_tempo);


--
-- Name: bi_fato_ordem_servico bi_fato_ordem_servico_sk_unidade_fkey; Type: FK CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.bi_fato_ordem_servico
    ADD CONSTRAINT bi_fato_ordem_servico_sk_unidade_fkey FOREIGN KEY (sk_unidade) REFERENCES public.bi_dim_unidade(sk_unidade);


--
-- Name: coletas coletas_amostra_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.coletas
    ADD CONSTRAINT coletas_amostra_id_fkey FOREIGN KEY (amostra_id) REFERENCES public.amostras(id);


--
-- Name: coletas coletas_coletor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.coletas
    ADD CONSTRAINT coletas_coletor_id_fkey FOREIGN KEY (coletor_id) REFERENCES public.usuarios(id);


--
-- Name: competencias competencias_fechada_por_usuario_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.competencias
    ADD CONSTRAINT competencias_fechada_por_usuario_id_fkey FOREIGN KEY (fechada_por_usuario_id) REFERENCES public.usuarios(id);


--
-- Name: conciliacoes_pagamento conciliacoes_pagamento_titulo_receber_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.conciliacoes_pagamento
    ADD CONSTRAINT conciliacoes_pagamento_titulo_receber_id_fkey FOREIGN KEY (titulo_receber_id) REFERENCES public.titulos_receber(id);


--
-- Name: equipamentos equipamentos_setor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.equipamentos
    ADD CONSTRAINT equipamentos_setor_id_fkey FOREIGN KEY (setor_id) REFERENCES public.setores(id);


--
-- Name: estoque_movimentos estoque_movimentos_insumo_material_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.estoque_movimentos
    ADD CONSTRAINT estoque_movimentos_insumo_material_id_fkey FOREIGN KEY (insumo_material_id) REFERENCES public.insumos_materiais(id);


--
-- Name: lotes_faturamento fk_lotes_faturamento_competencia; Type: FK CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.lotes_faturamento
    ADD CONSTRAINT fk_lotes_faturamento_competencia FOREIGN KEY (competencia) REFERENCES public.competencias(competencia);


--
-- Name: os_itens fk_os_itens_cancelado_por_usuario_id; Type: FK CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.os_itens
    ADD CONSTRAINT fk_os_itens_cancelado_por_usuario_id FOREIGN KEY (cancelado_por_usuario_id) REFERENCES public.usuarios(id);


--
-- Name: resultados fk_resultado_analito; Type: FK CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.resultados
    ADD CONSTRAINT fk_resultado_analito FOREIGN KEY (analito_id) REFERENCES public.analitos(id);


--
-- Name: valores_referencia fk_valor_referencia_analito; Type: FK CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.valores_referencia
    ADD CONSTRAINT fk_valor_referencia_analito FOREIGN KEY (analito_id) REFERENCES public.analitos(id);


--
-- Name: glosas glosas_guia_item_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.glosas
    ADD CONSTRAINT glosas_guia_item_id_fkey FOREIGN KEY (guia_item_id) REFERENCES public.guias_itens(id);


--
-- Name: glosas glosas_unidade_origem_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.glosas
    ADD CONSTRAINT glosas_unidade_origem_id_fkey FOREIGN KEY (unidade_origem_id) REFERENCES public.unidades(id);


--
-- Name: guias_itens guias_itens_guia_tiss_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.guias_itens
    ADD CONSTRAINT guias_itens_guia_tiss_id_fkey FOREIGN KEY (guia_tiss_id) REFERENCES public.guias_tiss(id);


--
-- Name: guias_itens guias_itens_laudo_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.guias_itens
    ADD CONSTRAINT guias_itens_laudo_id_fkey FOREIGN KEY (laudo_id) REFERENCES public.laudos(id);


--
-- Name: guias_itens guias_itens_procedimento_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.guias_itens
    ADD CONSTRAINT guias_itens_procedimento_id_fkey FOREIGN KEY (procedimento_id) REFERENCES public.procedimentos(id);


--
-- Name: guias_tiss guias_tiss_lote_faturamento_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.guias_tiss
    ADD CONSTRAINT guias_tiss_lote_faturamento_id_fkey FOREIGN KEY (lote_faturamento_id) REFERENCES public.lotes_faturamento(id);


--
-- Name: laudos laudos_os_item_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.laudos
    ADD CONSTRAINT laudos_os_item_id_fkey FOREIGN KEY (os_item_id) REFERENCES public.os_itens(id);


--
-- Name: laudos laudos_responsavel_tecnico_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.laudos
    ADD CONSTRAINT laudos_responsavel_tecnico_id_fkey FOREIGN KEY (responsavel_tecnico_id) REFERENCES public.medicos(id);


--
-- Name: lotes_faturamento lotes_faturamento_convenio_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.lotes_faturamento
    ADD CONSTRAINT lotes_faturamento_convenio_id_fkey FOREIGN KEY (convenio_id) REFERENCES public.convenios(id);


--
-- Name: malotes_amostras malotes_amostras_amostra_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.malotes_amostras
    ADD CONSTRAINT malotes_amostras_amostra_id_fkey FOREIGN KEY (amostra_id) REFERENCES public.amostras(id);


--
-- Name: malotes_amostras malotes_amostras_malote_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.malotes_amostras
    ADD CONSTRAINT malotes_amostras_malote_id_fkey FOREIGN KEY (malote_id) REFERENCES public.malotes(id);


--
-- Name: malotes malotes_enviado_por_usuario_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.malotes
    ADD CONSTRAINT malotes_enviado_por_usuario_id_fkey FOREIGN KEY (enviado_por_usuario_id) REFERENCES public.usuarios(id);


--
-- Name: malotes malotes_unidade_destino_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.malotes
    ADD CONSTRAINT malotes_unidade_destino_id_fkey FOREIGN KEY (unidade_destino_id) REFERENCES public.unidades(id);


--
-- Name: malotes malotes_unidade_origem_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.malotes
    ADD CONSTRAINT malotes_unidade_origem_id_fkey FOREIGN KEY (unidade_origem_id) REFERENCES public.unidades(id);


--
-- Name: movimentos_caixa movimentos_caixa_titulo_pagar_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.movimentos_caixa
    ADD CONSTRAINT movimentos_caixa_titulo_pagar_id_fkey FOREIGN KEY (titulo_pagar_id) REFERENCES public.titulos_pagar(id);


--
-- Name: movimentos_caixa movimentos_caixa_titulo_receber_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.movimentos_caixa
    ADD CONSTRAINT movimentos_caixa_titulo_receber_id_fkey FOREIGN KEY (titulo_receber_id) REFERENCES public.titulos_receber(id);


--
-- Name: ordens_servico ordens_servico_convenio_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.ordens_servico
    ADD CONSTRAINT ordens_servico_convenio_id_fkey FOREIGN KEY (convenio_id) REFERENCES public.convenios(id);


--
-- Name: ordens_servico ordens_servico_medico_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.ordens_servico
    ADD CONSTRAINT ordens_servico_medico_id_fkey FOREIGN KEY (medico_id) REFERENCES public.medicos(id);


--
-- Name: ordens_servico ordens_servico_paciente_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.ordens_servico
    ADD CONSTRAINT ordens_servico_paciente_id_fkey FOREIGN KEY (paciente_id) REFERENCES public.pacientes(id);


--
-- Name: ordens_servico ordens_servico_unidade_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.ordens_servico
    ADD CONSTRAINT ordens_servico_unidade_id_fkey FOREIGN KEY (unidade_id) REFERENCES public.unidades(id);


--
-- Name: os_itens os_itens_ordem_servico_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.os_itens
    ADD CONSTRAINT os_itens_ordem_servico_id_fkey FOREIGN KEY (ordem_servico_id) REFERENCES public.ordens_servico(id);


--
-- Name: os_itens os_itens_procedimento_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.os_itens
    ADD CONSTRAINT os_itens_procedimento_id_fkey FOREIGN KEY (procedimento_id) REFERENCES public.procedimentos(id);


--
-- Name: os_status_historico os_status_historico_ordem_servico_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.os_status_historico
    ADD CONSTRAINT os_status_historico_ordem_servico_id_fkey FOREIGN KEY (ordem_servico_id) REFERENCES public.ordens_servico(id);


--
-- Name: os_status_historico os_status_historico_usuario_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.os_status_historico
    ADD CONSTRAINT os_status_historico_usuario_id_fkey FOREIGN KEY (usuario_id) REFERENCES public.usuarios(id);


--
-- Name: pedidos_compra pedidos_compra_fornecedor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.pedidos_compra
    ADD CONSTRAINT pedidos_compra_fornecedor_id_fkey FOREIGN KEY (fornecedor_id) REFERENCES public.fornecedores(id);


--
-- Name: pedidos_compra pedidos_compra_solicitacao_compra_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.pedidos_compra
    ADD CONSTRAINT pedidos_compra_solicitacao_compra_id_fkey FOREIGN KEY (solicitacao_compra_id) REFERENCES public.solicitacoes_compra(id);


--
-- Name: pedidos_itens pedidos_itens_insumo_material_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.pedidos_itens
    ADD CONSTRAINT pedidos_itens_insumo_material_id_fkey FOREIGN KEY (insumo_material_id) REFERENCES public.insumos_materiais(id);


--
-- Name: pedidos_itens pedidos_itens_pedido_compra_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.pedidos_itens
    ADD CONSTRAINT pedidos_itens_pedido_compra_id_fkey FOREIGN KEY (pedido_compra_id) REFERENCES public.pedidos_compra(id);


--
-- Name: perfil_permissao perfil_permissao_perfil_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.perfil_permissao
    ADD CONSTRAINT perfil_permissao_perfil_id_fkey FOREIGN KEY (perfil_id) REFERENCES public.perfis(id);


--
-- Name: perfil_permissao perfil_permissao_permissao_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.perfil_permissao
    ADD CONSTRAINT perfil_permissao_permissao_id_fkey FOREIGN KEY (permissao_id) REFERENCES public.permissoes(id);


--
-- Name: procedimento_analitos procedimento_analitos_analito_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.procedimento_analitos
    ADD CONSTRAINT procedimento_analitos_analito_id_fkey FOREIGN KEY (analito_id) REFERENCES public.analitos(id);


--
-- Name: procedimento_analitos procedimento_analitos_procedimento_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.procedimento_analitos
    ADD CONSTRAINT procedimento_analitos_procedimento_id_fkey FOREIGN KEY (procedimento_id) REFERENCES public.procedimentos(id) ON DELETE CASCADE;


--
-- Name: procedimento_valores procedimento_valores_convenio_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.procedimento_valores
    ADD CONSTRAINT procedimento_valores_convenio_id_fkey FOREIGN KEY (convenio_id) REFERENCES public.convenios(id);


--
-- Name: procedimento_valores procedimento_valores_procedimento_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.procedimento_valores
    ADD CONSTRAINT procedimento_valores_procedimento_id_fkey FOREIGN KEY (procedimento_id) REFERENCES public.procedimentos(id);


--
-- Name: procedimentos_insumos procedimentos_insumos_insumo_material_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.procedimentos_insumos
    ADD CONSTRAINT procedimentos_insumos_insumo_material_id_fkey FOREIGN KEY (insumo_material_id) REFERENCES public.insumos_materiais(id) ON DELETE CASCADE;


--
-- Name: procedimentos_insumos procedimentos_insumos_procedimento_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.procedimentos_insumos
    ADD CONSTRAINT procedimentos_insumos_procedimento_id_fkey FOREIGN KEY (procedimento_id) REFERENCES public.procedimentos(id) ON DELETE CASCADE;


--
-- Name: protocolos_recebimento protocolos_recebimento_malote_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.protocolos_recebimento
    ADD CONSTRAINT protocolos_recebimento_malote_id_fkey FOREIGN KEY (malote_id) REFERENCES public.malotes(id);


--
-- Name: protocolos_recebimento protocolos_recebimento_recebido_por_usuario_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.protocolos_recebimento
    ADD CONSTRAINT protocolos_recebimento_recebido_por_usuario_id_fkey FOREIGN KEY (recebido_por_usuario_id) REFERENCES public.usuarios(id);


--
-- Name: recebimentos_insumo recebimentos_insumo_pedido_compra_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.recebimentos_insumo
    ADD CONSTRAINT recebimentos_insumo_pedido_compra_id_fkey FOREIGN KEY (pedido_compra_id) REFERENCES public.pedidos_compra(id);


--
-- Name: resultados_auditoria resultados_auditoria_resultado_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.resultados_auditoria
    ADD CONSTRAINT resultados_auditoria_resultado_id_fkey FOREIGN KEY (resultado_id) REFERENCES public.resultados(id);


--
-- Name: resultados_auditoria resultados_auditoria_usuario_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.resultados_auditoria
    ADD CONSTRAINT resultados_auditoria_usuario_id_fkey FOREIGN KEY (usuario_id) REFERENCES public.usuarios(id);


--
-- Name: resultados resultados_equipamento_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.resultados
    ADD CONSTRAINT resultados_equipamento_id_fkey FOREIGN KEY (equipamento_id) REFERENCES public.equipamentos(id);


--
-- Name: resultados resultados_os_item_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.resultados
    ADD CONSTRAINT resultados_os_item_id_fkey FOREIGN KEY (os_item_id) REFERENCES public.os_itens(id);


--
-- Name: setores setores_unidade_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.setores
    ADD CONSTRAINT setores_unidade_id_fkey FOREIGN KEY (unidade_id) REFERENCES public.unidades(id);


--
-- Name: solicitacoes_compra solicitacoes_compra_solicitante_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.solicitacoes_compra
    ADD CONSTRAINT solicitacoes_compra_solicitante_id_fkey FOREIGN KEY (solicitante_id) REFERENCES public.usuarios(id);


--
-- Name: titulos_pagar titulos_pagar_pedido_compra_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.titulos_pagar
    ADD CONSTRAINT titulos_pagar_pedido_compra_id_fkey FOREIGN KEY (pedido_compra_id) REFERENCES public.pedidos_compra(id);


--
-- Name: titulos_receber titulos_receber_lote_faturamento_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.titulos_receber
    ADD CONSTRAINT titulos_receber_lote_faturamento_id_fkey FOREIGN KEY (lote_faturamento_id) REFERENCES public.lotes_faturamento(id);


--
-- Name: usuarios usuarios_perfil_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_perfil_id_fkey FOREIGN KEY (perfil_id) REFERENCES public.perfis(id);


--
-- Name: valores_referencia valores_referencia_procedimento_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: labvida
--

ALTER TABLE ONLY public.valores_referencia
    ADD CONSTRAINT valores_referencia_procedimento_id_fkey FOREIGN KEY (procedimento_id) REFERENCES public.procedimentos(id);


--
-- PostgreSQL database dump complete
--

\unrestrict dFRUsYUR1RMaQIh8ZqOyrzvDjdcUmQjhfZWIEbJcOk4zfiP01u3POajjViaLWW2

