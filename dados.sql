--
-- PostgreSQL database dump
--

\restrict r9mpLnDEXRg6lUWW6201AfEJAhf8Q8SXnJVVGUKyey3wFscuIcQQUXiMSu1ixOv

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
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: labvida
--

INSERT INTO public.alembic_version VALUES ('0021_procedimento_insumo');


--
-- Data for Name: convenios; Type: TABLE DATA; Schema: public; Owner: labvida
--



--
-- Data for Name: medicos; Type: TABLE DATA; Schema: public; Owner: labvida
--



--
-- Data for Name: pacientes; Type: TABLE DATA; Schema: public; Owner: labvida
--



--
-- Data for Name: unidades; Type: TABLE DATA; Schema: public; Owner: labvida
--



--
-- Data for Name: ordens_servico; Type: TABLE DATA; Schema: public; Owner: labvida
--



--
-- Data for Name: amostras; Type: TABLE DATA; Schema: public; Owner: labvida
--



--
-- Data for Name: perfis; Type: TABLE DATA; Schema: public; Owner: labvida
--



--
-- Data for Name: usuarios; Type: TABLE DATA; Schema: public; Owner: labvida
--



--
-- Data for Name: amostras_movimentacoes; Type: TABLE DATA; Schema: public; Owner: labvida
--



--
-- Data for Name: analitos; Type: TABLE DATA; Schema: public; Owner: labvida
--

INSERT INTO public.analitos VALUES ('4dc3452e-0dae-4587-b751-60f439b08349', 'BETAHCG', 'Beta HCG', 'mUI/mL', 2, NULL, true);
INSERT INTO public.analitos VALUES ('bfea72a2-34a4-41b1-8a5b-205ed40d7039', 'COLESTEROLTOTAL', 'Colesterol total', 'mg/dL', 2, NULL, true);
INSERT INTO public.analitos VALUES ('d5b52f79-f1cb-407f-baa0-278aa4c981ae', 'PLAQUETAS', 'Plaquetas', '/mm³', 2, NULL, true);
INSERT INTO public.analitos VALUES ('62d576fc-9955-481f-969a-aec6f4deb69f', 'CREATININA', 'Creatinina', 'mg/dL', 2, NULL, true);
INSERT INTO public.analitos VALUES ('cdfb24a2-fe24-4410-add1-ea22a1c1f21d', 'FERRITINA', 'Ferritina', 'ng/mL', 2, NULL, true);
INSERT INTO public.analitos VALUES ('ca1ed98a-566e-4a42-9452-d3d9f6a3cc3c', 'FERRO', 'Ferro', 'µg/dL', 2, NULL, true);
INSERT INTO public.analitos VALUES ('142a9732-6a7a-4e91-9a05-d9f6a4deeb38', 'FOSFATASEALCALINA', 'Fosfatase alcalina', 'U/L', 2, NULL, true);
INSERT INTO public.analitos VALUES ('e49789c9-700f-4e7d-a445-6efd75e9b297', 'GAMAGT', 'Gama GT', 'U/L', 2, NULL, true);
INSERT INTO public.analitos VALUES ('42934ba5-472e-4b46-88cd-2d6e336ede69', 'GLICOSE', 'Glicose', 'mg/dL', 2, NULL, true);
INSERT INTO public.analitos VALUES ('5b123719-88d2-4d42-817a-0ef09fadb0e5', 'HDL', 'HDL', 'mg/dL', 2, NULL, true);
INSERT INTO public.analitos VALUES ('1ff5497a-40e5-4653-9c08-e613f2fdfe52', 'HBA1C', 'HbA1c', '%', 2, NULL, true);
INSERT INTO public.analitos VALUES ('bf62ece3-beee-4f1c-a3fa-89101f6c0e62', 'HEMOGLOBINA', 'Hemoglobina', 'g/dL', 2, NULL, true);
INSERT INTO public.analitos VALUES ('2e850ec2-7660-4539-9382-9f3cebc12e83', 'HEMATCRITO', 'Hematócrito', '%', 2, NULL, true);
INSERT INTO public.analitos VALUES ('f457746c-e79b-4f59-80c2-47f548380cdb', 'LEUCCITOS', 'Leucócitos', '/mm³', 2, NULL, true);
INSERT INTO public.analitos VALUES ('e00602fb-f6ba-430c-b412-2007a199d574', 'LDL', 'LDL', 'mg/dL', 2, NULL, true);
INSERT INTO public.analitos VALUES ('5f003ff8-baeb-46c0-80ef-cde5c010fcab', 'PSATOTAL', 'PSA total', 'ng/mL', 2, NULL, true);
INSERT INTO public.analitos VALUES ('29bf6377-1506-42b5-98b6-907be67b8999', 'PESQUISADEOVOSECISTOS', 'Pesquisa de ovos e cistos', NULL, 2, NULL, true);
INSERT INTO public.analitos VALUES ('b579471c-95f0-4e46-ae70-3f41b2d687b7', 'PCR', 'PCR', 'mg/L', 2, NULL, true);
INSERT INTO public.analitos VALUES ('59ab956d-c890-4579-b999-9fc2a6eaa657', 'T4LIVRE', 'T4 livre', 'ng/dL', 2, NULL, true);
INSERT INTO public.analitos VALUES ('fa207c5e-56ea-460a-a95f-806d4995b155', 'AST', 'AST', 'U/L', 2, NULL, true);
INSERT INTO public.analitos VALUES ('5156c17d-7d3b-47b5-9d25-894913672961', 'ALT', 'ALT', 'U/L', 2, NULL, true);
INSERT INTO public.analitos VALUES ('288772e3-2d58-496a-8fa3-39f0259bb99b', 'TSH', 'TSH', 'µUI/mL', 2, NULL, true);
INSERT INTO public.analitos VALUES ('87fa13be-54a6-41a8-a308-ebc83af9c724', 'TAP', 'TAP', 'segundos', 2, NULL, true);
INSERT INTO public.analitos VALUES ('0e07547b-495d-4d66-bcdc-626ed8300bcc', 'INR', 'INR', NULL, 2, NULL, true);
INSERT INTO public.analitos VALUES ('a4b8c8f9-f70b-4c43-a3f9-48bca3f4c0d4', 'TTPA', 'TTPA', 'segundos', 2, NULL, true);
INSERT INTO public.analitos VALUES ('1292d793-329d-4804-ae57-c90938269039', 'TRIGLICERDEOS', 'Triglicerídeos', 'mg/dL', 2, NULL, true);
INSERT INTO public.analitos VALUES ('e81da553-9b96-42a6-9e1a-98869ca6db9c', 'UREIA', 'Ureia', 'mg/dL', 2, NULL, true);
INSERT INTO public.analitos VALUES ('a4400fc2-750f-4776-9c57-c74060759496', 'DENSIDADE', 'Densidade', NULL, 2, NULL, true);
INSERT INTO public.analitos VALUES ('9a72f31a-302c-4139-9d9d-f3fb81385073', 'PHURINRIO', 'pH urinário', NULL, 2, NULL, true);
INSERT INTO public.analitos VALUES ('564e3b13-6205-4c54-9cec-f14b47d2ccf9', 'CONTAGEMDECOLNIAS', 'Contagem de colônias', 'UFC/mL', 2, NULL, true);
INSERT INTO public.analitos VALUES ('5347d26e-e926-4d45-96b1-536cf5e42d77', 'VDRL', 'VDRL', 'título', 2, NULL, true);
INSERT INTO public.analitos VALUES ('51a01eca-dbff-4840-aa35-cc4962f42211', 'VITAMINAB12', 'Vitamina B12', 'pg/mL', 2, NULL, true);
INSERT INTO public.analitos VALUES ('8b38f8eb-82c5-442e-9682-ef03e862e1aa', '25OHVITAMINAD', '25-OH vitamina D', 'ng/mL', 2, NULL, true);
INSERT INTO public.analitos VALUES ('6479e8dd-3876-4d74-aaca-ea920dd84639', 'CIDORICO', 'Ácido úrico', 'mg/dL', 2, NULL, true);


--
-- Data for Name: auditoria_log; Type: TABLE DATA; Schema: public; Owner: labvida
--



--
-- Data for Name: autorizacoes_convenio; Type: TABLE DATA; Schema: public; Owner: labvida
--



--
-- Data for Name: bi_dim_convenio; Type: TABLE DATA; Schema: public; Owner: labvida
--

INSERT INTO public.bi_dim_convenio VALUES (1, '19e6ba60-4c67-4e5d-b2c7-4f4c58c7313d', 'Unimed', '417033');
INSERT INTO public.bi_dim_convenio VALUES (2, 'a5dc9462-361b-41fe-adf4-0745f254dc11', 'Bradesco Saúde', '005711');
INSERT INTO public.bi_dim_convenio VALUES (3, '9d26a25d-c68d-4511-bfb4-417f6cb422ec', 'Hapvida', '368253');
INSERT INTO public.bi_dim_convenio VALUES (4, '9e0fa6f4-6812-4fdc-9c89-2f97b9f2a1dd', 'Amil', '326305');
INSERT INTO public.bi_dim_convenio VALUES (5, 'f130f005-8b28-4d6b-85df-f4bf405f7706', 'SulAmérica Saúde', '006246');
INSERT INTO public.bi_dim_convenio VALUES (6, 'a8c31bcc-af51-423e-9ab0-778366735644', 'NotreDame Intermédica', '359017');
INSERT INTO public.bi_dim_convenio VALUES (7, '0d6c6a64-b658-4d7d-bc18-b12fc3ae4cee', 'Cassi', '346659');
INSERT INTO public.bi_dim_convenio VALUES (8, 'e0b56403-b9b5-4296-80ea-042f3364dbef', 'Golden Cross', '004049');


--
-- Data for Name: bi_dim_faixa_etaria; Type: TABLE DATA; Schema: public; Owner: labvida
--

INSERT INTO public.bi_dim_faixa_etaria VALUES (1, '0-12', '0-12 anos', 1);
INSERT INTO public.bi_dim_faixa_etaria VALUES (2, '13-18', '13-18 anos', 2);
INSERT INTO public.bi_dim_faixa_etaria VALUES (3, '19-30', '19-30 anos', 3);
INSERT INTO public.bi_dim_faixa_etaria VALUES (4, '31-50', '31-50 anos', 4);
INSERT INTO public.bi_dim_faixa_etaria VALUES (5, '51-65', '51-65 anos', 5);
INSERT INTO public.bi_dim_faixa_etaria VALUES (6, '66+', '66+ anos', 6);
INSERT INTO public.bi_dim_faixa_etaria VALUES (7, 'DESCONHECIDA', 'Desconhecida', 9);


--
-- Data for Name: bi_dim_motivo_glosa; Type: TABLE DATA; Schema: public; Owner: labvida
--

INSERT INTO public.bi_dim_motivo_glosa VALUES (1, 'NAO_INFORMADO', 'Nao informado');
INSERT INTO public.bi_dim_motivo_glosa VALUES (2, 'documentação incompleta no envio do lote', 'Documentação incompleta no envio do lote');
INSERT INTO public.bi_dim_motivo_glosa VALUES (3, 'duplicidade de cobrança no período', 'Duplicidade de cobrança no período');
INSERT INTO public.bi_dim_motivo_glosa VALUES (4, 'beneficiário com carência não cumprida', 'Beneficiário com carência não cumprida');
INSERT INTO public.bi_dim_motivo_glosa VALUES (5, 'prazo de apresentação da guia expirado', 'Prazo de apresentação da guia expirado');
INSERT INTO public.bi_dim_motivo_glosa VALUES (6, 'procedimento não coberto pelo plano contratado', 'Procedimento não coberto pelo plano contratado');
INSERT INTO public.bi_dim_motivo_glosa VALUES (7, 'divergência entre código tuss e procedimento executado', 'Divergência entre código TUSS e procedimento executado');
INSERT INTO public.bi_dim_motivo_glosa VALUES (8, 'valor apresentado acima da tabela negociada', 'Valor apresentado acima da tabela negociada');
INSERT INTO public.bi_dim_motivo_glosa VALUES (9, 'guia sem autorização prévia do convênio', 'Guia sem autorização prévia do convênio');


--
-- Data for Name: bi_dim_paciente_anon; Type: TABLE DATA; Schema: public; Owner: labvida
--

INSERT INTO public.bi_dim_paciente_anon VALUES (1, 'ea133bfd627c94ba9dae9c54bb808738f2ad1cac26681c71409c7be44673d6b5', 'NAO_INFORMADO');
INSERT INTO public.bi_dim_paciente_anon VALUES (2, '7f19cd1c8f57f518decab2999b348d708cb00bb08cf74091de5dbc74c1465b14', 'MASCULINO');
INSERT INTO public.bi_dim_paciente_anon VALUES (3, '765b36ec8e40545538ee9346b56a8956839215a5c948f93e7d1bfbf40f440b86', 'NAO_INFORMADO');
INSERT INTO public.bi_dim_paciente_anon VALUES (4, '045cd73d9331b3597f80af1076de331dbd1155f514d4c3eea7c5ff8bd83b5562', 'MASCULINO');
INSERT INTO public.bi_dim_paciente_anon VALUES (5, '94bc24b5255cf24efabe43ac4f31000f43d14025ae805df190e58a706a0d688d', 'FEMININO');
INSERT INTO public.bi_dim_paciente_anon VALUES (6, 'd15f94f320ac1f7a5902c7a78a9685b71de4877b552a2447aade3143a18954f2', 'FEMININO');
INSERT INTO public.bi_dim_paciente_anon VALUES (7, '987da6e8c0a60c5d6ab9a070e3f0a4ba4164abfd06f50f64f24e569d75eb7cbd', 'MASCULINO');
INSERT INTO public.bi_dim_paciente_anon VALUES (8, '62717f6bb27c7127d7fb18ec3940124856d767e3457935372cbf183b1564bae8', 'FEMININO');
INSERT INTO public.bi_dim_paciente_anon VALUES (9, '6162e3fac6882bae46e74fb17452f3b0905b3b65a5ba5f93518e4cd8d9377799', 'NAO_INFORMADO');
INSERT INTO public.bi_dim_paciente_anon VALUES (10, '7b247bd14fcdfd10996ca8a9ad37d3e6037c54d49bbd50d9ccb7881b78aeb0ae', 'NAO_INFORMADO');
INSERT INTO public.bi_dim_paciente_anon VALUES (11, '694ae9ae8ae576a30ee19ec2dd23118596a1d11afaf856229578bba15b0d2467', 'MASCULINO');
INSERT INTO public.bi_dim_paciente_anon VALUES (12, '7ab71bcd1889adffc4ac3b32a750899738da2287bff0f430a10d75ac34322b86', 'NAO_INFORMADO');
INSERT INTO public.bi_dim_paciente_anon VALUES (13, 'd0917b570b81b55d70aa05b74458954af96e81aa9abf13888082878e57c3e2d1', 'FEMININO');
INSERT INTO public.bi_dim_paciente_anon VALUES (14, 'c60c48144bde4d850455300a230aea4a2b55d21b4bacfb30d6eef55deb963be6', 'MASCULINO');
INSERT INTO public.bi_dim_paciente_anon VALUES (15, '2aa9484569e645039edd723e534ce348683629b932e63a588663abbdaaf9b06a', 'MASCULINO');
INSERT INTO public.bi_dim_paciente_anon VALUES (16, '09fda4ba5050c4f132cd2173fb846a0628079edf073e7c9289aac05eac272c39', 'NAO_INFORMADO');
INSERT INTO public.bi_dim_paciente_anon VALUES (17, 'bc2ead3b11ebf4bbd59f062735a20ece2870415c26bd7f5c0600983f463cb94e', 'NAO_INFORMADO');
INSERT INTO public.bi_dim_paciente_anon VALUES (18, '3f7396fdf86870093ce8f59e5b4c3352c8622f5cd871d870b8c678e68104ad06', 'MASCULINO');
INSERT INTO public.bi_dim_paciente_anon VALUES (19, 'bb2b8c54838260f3c0523af77f65c39344744d82acef5a084b7fd826b515dcf1', 'NAO_INFORMADO');
INSERT INTO public.bi_dim_paciente_anon VALUES (20, 'e5dec802cc8e4b8c9d54e62a78b35f6462fc290213dacb37efeac0ba7ca5edbc', 'NAO_INFORMADO');
INSERT INTO public.bi_dim_paciente_anon VALUES (21, '2b698b1a66ec04717df355aef0db4be2abc0834253d69e77a6e3570761117769', 'NAO_INFORMADO');
INSERT INTO public.bi_dim_paciente_anon VALUES (22, '54fe2c1adefeb259852689d62e5ede4ad6db3c37e1cb2a7c7fe6dc9d320b14b5', 'MASCULINO');
INSERT INTO public.bi_dim_paciente_anon VALUES (23, '8f46bc7cce2262940cafeb691601d0445276b13ab7e1da6b4b8769ac74c184e6', 'NAO_INFORMADO');
INSERT INTO public.bi_dim_paciente_anon VALUES (24, 'a3e295d0c38772755d6da3c3a1142c686a69a80b91536d85cfd5ba5d09644dcf', 'NAO_INFORMADO');
INSERT INTO public.bi_dim_paciente_anon VALUES (25, '21de2768fc324684c28f7a172f9d8155bd7104b8cb6d72d7487fb7de73a1a0b5', 'NAO_INFORMADO');
INSERT INTO public.bi_dim_paciente_anon VALUES (26, '74b7e4638378af04d6de26027dd5c63122bb3705d975ad301931ca0c90d7c3a2', 'MASCULINO');
INSERT INTO public.bi_dim_paciente_anon VALUES (27, '46a347f43516efa6be46ef2cb76898aa64ba133d7f311e087f7f9fca80b990f7', 'FEMININO');
INSERT INTO public.bi_dim_paciente_anon VALUES (28, 'ec9232f767b6a4f68695223cc64be7f8909fd806e0796003544587016e1ea011', 'MASCULINO');
INSERT INTO public.bi_dim_paciente_anon VALUES (29, 'dceda36b815c019c8801b9435e0c7079452b42577f2a4d9e721d90246dff34dd', 'MASCULINO');
INSERT INTO public.bi_dim_paciente_anon VALUES (30, '859444f9e3f267d694f3feaf5a45eb94644f70418ae6f3c73154280ff87cbaa0', 'NAO_INFORMADO');
INSERT INTO public.bi_dim_paciente_anon VALUES (31, '8a7ebed9a14bf1ca343cff62a411ddaf221c06a1214b42c4b206f697efd5d16f', 'NAO_INFORMADO');
INSERT INTO public.bi_dim_paciente_anon VALUES (32, 'ff77623bb25f1479e8d2b80c4e26353ba36f1b50e1f9307380c74efa33cc22bd', 'MASCULINO');
INSERT INTO public.bi_dim_paciente_anon VALUES (33, '33c5c3d14348d5515ae18e5ba3bf8a14cdd15003b3f0c797fa1006b35c96e445', 'MASCULINO');
INSERT INTO public.bi_dim_paciente_anon VALUES (34, '960bf43b4127a58685407deffdca564b890643b0c98e2cbe3e075c88547952c3', 'NAO_INFORMADO');
INSERT INTO public.bi_dim_paciente_anon VALUES (35, '5f0cc572770073a49fe9655c7a709984d24428dc448817b294a63e973f1ceee8', 'FEMININO');
INSERT INTO public.bi_dim_paciente_anon VALUES (36, '74343fb164cceec5a72189abb710c572ef300bc6f6f834ef1552976442eeb3c8', 'MASCULINO');
INSERT INTO public.bi_dim_paciente_anon VALUES (37, '5c3895dc635d161a12adb9d66163603f19a82d093898fb7b3b16c51d4088ef80', 'FEMININO');
INSERT INTO public.bi_dim_paciente_anon VALUES (38, '96cdd9aa3eb9e80e50ddfa04d14a43f55869c436332c091c4c480a1f295868dc', 'NAO_INFORMADO');
INSERT INTO public.bi_dim_paciente_anon VALUES (39, 'd7a6b330d48abaad983e18afa821005e1a628b2c14c651a8d929d7ae19edeaf6', 'FEMININO');
INSERT INTO public.bi_dim_paciente_anon VALUES (40, '0cb74883e45f1b85b6e8c607c52844c43e04adfa4b4ed027a89a726f2aeb5527', 'FEMININO');
INSERT INTO public.bi_dim_paciente_anon VALUES (41, '68303675bb980c10138b158b6fe05f00b3cab4646ce9f41f4214cdc2d5995036', 'FEMININO');
INSERT INTO public.bi_dim_paciente_anon VALUES (42, '669e2fa18792d6edc4a4d552275826abbf064079da6c3abd354f989fe3ffab64', 'NAO_INFORMADO');
INSERT INTO public.bi_dim_paciente_anon VALUES (43, '51e024634cb7682ef4c2cbad188eba06f3220823bb040f7f875d01148a5666a2', 'NAO_INFORMADO');
INSERT INTO public.bi_dim_paciente_anon VALUES (44, '2d29035b3e1377acde7be9373c8300519c1c90182a2a4ad80346b77a3fe7cbb8', 'FEMININO');
INSERT INTO public.bi_dim_paciente_anon VALUES (45, '2e5a9af43a7c9e8f631ebecc7bc6b78e2e1b0a67548db52a8260553b047a8000', 'FEMININO');
INSERT INTO public.bi_dim_paciente_anon VALUES (46, 'ec4c6a2cb53fdae94e842364336cabc29f24176b746aa0ebb1e99c6fa7c993b7', 'FEMININO');
INSERT INTO public.bi_dim_paciente_anon VALUES (47, 'f066ff4700f8d2deca56eea908be9dc0047c5a3f403d8d2f50c50fd7ba72b66f', 'FEMININO');
INSERT INTO public.bi_dim_paciente_anon VALUES (48, '71827ffd3c24a11488768a639ea85d0872701454896c82ac4c5436bba1ec21ea', 'NAO_INFORMADO');
INSERT INTO public.bi_dim_paciente_anon VALUES (49, '77f4c35417eb12d618ca8c6b35e94fafbcee69464178b9208932ccce8a7cf1cb', 'NAO_INFORMADO');
INSERT INTO public.bi_dim_paciente_anon VALUES (50, '5109a833ddbb81c8ee80941041851b3c36b74363af4149ab7027bdb13ae07d1d', 'NAO_INFORMADO');
INSERT INTO public.bi_dim_paciente_anon VALUES (51, 'd375685a0939f2c5350e9383297e61cc72d5682d6989ff823154a470177b6bde', 'MASCULINO');
INSERT INTO public.bi_dim_paciente_anon VALUES (52, '0f35a837d9b6817e28be868e0d781080c5e75ab9cf589ac4070b9e563912d173', 'MASCULINO');
INSERT INTO public.bi_dim_paciente_anon VALUES (53, '06c9be00413bf58e9bd8f7d63697a780b63a3224083b44d87a5a85fffebf2166', 'FEMININO');
INSERT INTO public.bi_dim_paciente_anon VALUES (54, '22ecbaa2e4315aab648bb04ae12a07ab863399b977aa1f60600ab958290d4674', 'NAO_INFORMADO');
INSERT INTO public.bi_dim_paciente_anon VALUES (55, '33f8eba5a1666376f370c29e17f9a2e7c2d06a0ff31c3fd1f187afd4bdd0b594', 'MASCULINO');
INSERT INTO public.bi_dim_paciente_anon VALUES (56, '7fee3fa2dc5de2d31b861c1bf6f2413133c2609e3a79c9b74c2071ce4b350e94', 'MASCULINO');
INSERT INTO public.bi_dim_paciente_anon VALUES (57, '24876370e2c89f0b3bd733e279d9b12dbfb067af4fb2f095b16ea41794ca22b5', 'FEMININO');
INSERT INTO public.bi_dim_paciente_anon VALUES (58, '41e3206c8a8f73de69edfb010d832a0f2714f8554ecc6b6470731b260454eef6', 'NAO_INFORMADO');
INSERT INTO public.bi_dim_paciente_anon VALUES (59, 'e5f407c6202a5b099037bb7d6fe12b8b4425bff96cc0b6d8ce17cc490875a0ae', 'FEMININO');
INSERT INTO public.bi_dim_paciente_anon VALUES (60, '030227616e47b6f657a4b49df43d666cf6fd4d640985c31412165d61721306b7', 'MASCULINO');
INSERT INTO public.bi_dim_paciente_anon VALUES (61, 'c53d0dab281b1552fb138d829138c1372d898ee5831d59a689e86a5cd6e29882', 'MASCULINO');
INSERT INTO public.bi_dim_paciente_anon VALUES (62, '2f5c9147b6fb0cc0bc71d6c960b72d6b09ffecaaee12300dff2991d71e52c5b0', 'FEMININO');
INSERT INTO public.bi_dim_paciente_anon VALUES (63, '115a3f47e405367a3ca549d35e8fa441883253caeb8c43119e578258e0967645', 'NAO_INFORMADO');
INSERT INTO public.bi_dim_paciente_anon VALUES (64, '77d96169fd299c701226fbfa89fa7c80be9b7a258c63229e0f8339e48d004b68', 'MASCULINO');
INSERT INTO public.bi_dim_paciente_anon VALUES (65, '4424fbf92789375a1243d4e2b4df46a99d1ac50154ff1edc7174b1a3c0fa3f50', 'FEMININO');
INSERT INTO public.bi_dim_paciente_anon VALUES (66, '666941e7d46e1dafaccce6e3dc0d5a5582e5993b5c582333d31110ab0e34af9d', 'NAO_INFORMADO');
INSERT INTO public.bi_dim_paciente_anon VALUES (67, '2808a1ac0932a669894338dcb0107b9029e38e975460fb13588a0be0c729212c', 'FEMININO');
INSERT INTO public.bi_dim_paciente_anon VALUES (68, '750faf05de0442b2440941e031549697342c69186efa58ee7f58cf467e68449f', 'MASCULINO');
INSERT INTO public.bi_dim_paciente_anon VALUES (69, '747b646dc20a6f6b622dc063c3e3ed2108b983f73f66f3a9da814a6aa86c4c80', 'MASCULINO');
INSERT INTO public.bi_dim_paciente_anon VALUES (70, 'e8e91f8eeb8cc9d52509f1e01594db738d1449421ab4ca4b3f4b7a66e9e7df18', 'MASCULINO');
INSERT INTO public.bi_dim_paciente_anon VALUES (71, '8d942cae758960aabcce0940918f0afd1f0e265ef9304f5e7c440bc30771b175', 'FEMININO');
INSERT INTO public.bi_dim_paciente_anon VALUES (72, 'a41d4b87a72c3411ee7f16168cb32f8d572320c6e5c2d483b86aae2062ef31f4', 'FEMININO');
INSERT INTO public.bi_dim_paciente_anon VALUES (73, '99530ca4975912d4fc903f8a20f4104a261f0ae6c146039bff315e81faaee8f2', 'MASCULINO');
INSERT INTO public.bi_dim_paciente_anon VALUES (74, '660fb71a1cfc9a7b5a938b703583aae261badfaf43b6dbf241face0b18eeb480', 'MASCULINO');
INSERT INTO public.bi_dim_paciente_anon VALUES (75, '852201cfe2c913a19dd80b37728f2cf4f9cd67d5b6de6f9cc5606aeede683d92', 'FEMININO');
INSERT INTO public.bi_dim_paciente_anon VALUES (76, 'ac4b017a178055468acbc2f8fa885486abb8f987612df86cdea492197ab8d94f', 'NAO_INFORMADO');
INSERT INTO public.bi_dim_paciente_anon VALUES (77, 'a6060a8fdb66ba0feef466bfb71f4f67dc0d6563283f7a07bca47c0afbd8b852', 'NAO_INFORMADO');
INSERT INTO public.bi_dim_paciente_anon VALUES (78, '28f893fb8b4ba4ac736117d3cda4abf0dd43a60fe1aac2cf3043d141600b4be0', 'FEMININO');
INSERT INTO public.bi_dim_paciente_anon VALUES (79, '4a2e8756068e22b7a68683db45a5c7b67712fac79981cb71ed33184582768d2d', 'MASCULINO');
INSERT INTO public.bi_dim_paciente_anon VALUES (80, '7d1bd403c57080b83c9f5443f9a1312aa58f9b0d46ec5d36a9be1e9f3e5ea8dd', 'NAO_INFORMADO');
INSERT INTO public.bi_dim_paciente_anon VALUES (81, '593cdd0f27aa632fcf1667932429e6f63ba7783dc0f1c8bc5e172de374b8fba1', 'FEMININO');
INSERT INTO public.bi_dim_paciente_anon VALUES (82, '64e649d6010817163e21693af896df73f1af6464bb56c70d9f6c51439ac7c24c', 'FEMININO');
INSERT INTO public.bi_dim_paciente_anon VALUES (83, 'c78d319614950759c75c564b8cb2e688978170c61422109dc870fc9608a00f5b', 'MASCULINO');
INSERT INTO public.bi_dim_paciente_anon VALUES (84, '81b23aafd418a38beabb9ba4c24055108c48f848f2d48f9744903611c08ac6cb', 'NAO_INFORMADO');
INSERT INTO public.bi_dim_paciente_anon VALUES (85, '4934979b6df1b172ba67c89a8f3ea28e859e0e0ca332c5812ee49b252fda064c', 'MASCULINO');
INSERT INTO public.bi_dim_paciente_anon VALUES (86, 'e3391ebb974791fa928021ff6f061751cb00b24cf725ce2e4ca6cbf4161ea3d9', 'FEMININO');
INSERT INTO public.bi_dim_paciente_anon VALUES (87, 'eca365d0cb3f465efe46c127f97de468ac6f598656f3c11040dc2976e0d35667', 'NAO_INFORMADO');
INSERT INTO public.bi_dim_paciente_anon VALUES (88, 'a6416952b6cb98b7e9319a78ebd08e69a56047621805b00644de5d2511be109a', 'MASCULINO');
INSERT INTO public.bi_dim_paciente_anon VALUES (89, '94feaa0ec5e22d9dcc436aef0e958bb531c02d4c2943550dd07e93810f8d140a', 'NAO_INFORMADO');
INSERT INTO public.bi_dim_paciente_anon VALUES (90, '1f55006ad9eedfc796ea160b346f867925299d40b8e7f12e01c5eb0b68e9a10e', 'FEMININO');
INSERT INTO public.bi_dim_paciente_anon VALUES (91, '448ba6fac5a3ef47cd6cdf1c3729b4df25a32734250ff307be012d6f6f023a08', 'NAO_INFORMADO');
INSERT INTO public.bi_dim_paciente_anon VALUES (92, 'd97688b0440ed26aa96d00c99562b057a46584b46144e8eb7ba8bbb2324256cf', 'MASCULINO');
INSERT INTO public.bi_dim_paciente_anon VALUES (93, 'd280ac3c6f9fd722e02d75d01d732947687e7ca427fa051e543eb322de474e15', 'MASCULINO');
INSERT INTO public.bi_dim_paciente_anon VALUES (94, 'a2df0098c5ee19a395bd1b90dc03a4f212a8fa2134cf3e3c15cae1d734656fe1', 'NAO_INFORMADO');
INSERT INTO public.bi_dim_paciente_anon VALUES (95, '0c93f521dbf92fc33240e691b69c3ad1ec13bf2e6e85ebc9dd90286760309123', 'NAO_INFORMADO');
INSERT INTO public.bi_dim_paciente_anon VALUES (96, '8331f7bdb0ccf2c384c7916bcbad53f84c7ce741813a178abe67b63c6b9a2cc9', 'NAO_INFORMADO');
INSERT INTO public.bi_dim_paciente_anon VALUES (97, 'b657b16d3dfa1aa42b4975afbebb90587a01907033f3aff73a058317f965d811', 'FEMININO');
INSERT INTO public.bi_dim_paciente_anon VALUES (98, '1b6604b0c69c83f0e4e3f79ebde46143cd9070c8ce6a2617abc124cdc7b8d209', 'FEMININO');
INSERT INTO public.bi_dim_paciente_anon VALUES (99, '842e7b33748d876b6c36e0f810778d3a756a47e70bf1da3bbd6361af4d246400', 'FEMININO');
INSERT INTO public.bi_dim_paciente_anon VALUES (100, '36b9e0fdc334a25d0468c53b8014733a381331af90e9c38bb73ebe834a39b860', 'MASCULINO');
INSERT INTO public.bi_dim_paciente_anon VALUES (101, '4ceb640de2d2a7927c9528da0177614a2ebdcdebdb85b4c41ccae7feeaf2d03e', 'FEMININO');
INSERT INTO public.bi_dim_paciente_anon VALUES (102, '1ccc1f71fac3eeb5aa33cbca761cfbdef3f4d85c3d9593c2256398c5131aa6ba', 'MASCULINO');
INSERT INTO public.bi_dim_paciente_anon VALUES (103, 'edae190c42c020cc00baf0928e58b14d53b7b2825af1ef53d275cb6010834828', 'FEMININO');
INSERT INTO public.bi_dim_paciente_anon VALUES (104, '6fc4ce4c4f297c9cda1f1b92117d6d665339c5deee8ce774efaecce5cfa8db80', 'NAO_INFORMADO');
INSERT INTO public.bi_dim_paciente_anon VALUES (105, '24649020104ac495a5b90479f0006ee90d5e60a2454fa6c3ef7a714b6a203925', 'MASCULINO');
INSERT INTO public.bi_dim_paciente_anon VALUES (106, '863f150903719f47c6bd44e17a6cd7d2086ff980fef6c6b8fbfbbe542d16a3fd', 'FEMININO');
INSERT INTO public.bi_dim_paciente_anon VALUES (107, 'a0aaa0ba6467e0e4437d0ea8d4de9075168dabd87981df2d660fdabbbb268a3a', 'MASCULINO');
INSERT INTO public.bi_dim_paciente_anon VALUES (108, '5975de7aef329e30fef714928d36da655c8b2a1473a371ee0f984c6200359878', 'NAO_INFORMADO');
INSERT INTO public.bi_dim_paciente_anon VALUES (109, 'b93b3f2cb08d872ce212cc85f364a4a2b459cefb62307f8c6c78e8830b0b00de', 'MASCULINO');
INSERT INTO public.bi_dim_paciente_anon VALUES (110, 'd25543bb35fbfd3f9dd8c1635daa5ff2d4204aabee0e700beb255deb400b298f', 'MASCULINO');
INSERT INTO public.bi_dim_paciente_anon VALUES (111, '84b64f582b450b4e2cfdd54e4a5aec4c712ac17e44d5cd50f2b285b064a1995e', 'MASCULINO');
INSERT INTO public.bi_dim_paciente_anon VALUES (112, '23f8307ff6689a696d673f7faca150dc8e8d9fd5f44b65779417c99a9bdcb24b', 'NAO_INFORMADO');
INSERT INTO public.bi_dim_paciente_anon VALUES (113, 'fdbd00ea211e8af94282f4a05d1bcf0e2316484dc693843336fa701d173f855d', 'MASCULINO');
INSERT INTO public.bi_dim_paciente_anon VALUES (114, 'ccba219b4dd67575d586f2c2b5c7c06e73dac400c99af645e934e6e01cf46cb7', 'FEMININO');
INSERT INTO public.bi_dim_paciente_anon VALUES (115, '58d6ab6c2087a0078e8430db7c34578d67a8c2450dc892ff57fc3311939b0cb4', 'MASCULINO');
INSERT INTO public.bi_dim_paciente_anon VALUES (116, 'e5672abd324c322e008575669fb8bd4832f2d7235447f4a116be225c62af61d2', 'MASCULINO');
INSERT INTO public.bi_dim_paciente_anon VALUES (117, '3aeb3ad5a3598d28d1df36c57f4a63f3c5edadf62151a99dfb96fe0087511edb', 'FEMININO');
INSERT INTO public.bi_dim_paciente_anon VALUES (118, 'adfb14ea25ee57c4f14e175c73a348fbcaa8fe7059f90b1edb2488b81a80ff99', 'MASCULINO');
INSERT INTO public.bi_dim_paciente_anon VALUES (119, 'bdff514ba4247530c7564ea9f9d75eff34b6579455757a2c3f49fdc3154a5e54', 'NAO_INFORMADO');
INSERT INTO public.bi_dim_paciente_anon VALUES (120, '6f41e282556cabfb7ed05191c1ba45e73d8d004764fbf1ed5bd2aae6791c40dd', 'FEMININO');
INSERT INTO public.bi_dim_paciente_anon VALUES (121, 'c792a415bf321627086f830ddd40a952d2324b12744ccc9fc8050870635462ae', 'NAO_INFORMADO');
INSERT INTO public.bi_dim_paciente_anon VALUES (122, '7922a781a5840db71258d45a2107c495d15b1a4882700f76451911fdd82d0784', 'MASCULINO');
INSERT INTO public.bi_dim_paciente_anon VALUES (123, 'f09b65b57519e83acbaaf7c3724000ffb19dda91de82fa12ce27a21a8768fdab', 'NAO_INFORMADO');
INSERT INTO public.bi_dim_paciente_anon VALUES (124, '05e201150aefe9e99074b4372d196c32d0ae02f7142e47302db2766a8cb3961e', 'FEMININO');
INSERT INTO public.bi_dim_paciente_anon VALUES (125, '078e697e9922168544a5ca36f4503923a8180ed649984086996b089e8f995548', 'NAO_INFORMADO');
INSERT INTO public.bi_dim_paciente_anon VALUES (126, '4be9e600ae689860594f0829dc8d1276b85d0986d96babf927a3bd682866bd9d', 'NAO_INFORMADO');
INSERT INTO public.bi_dim_paciente_anon VALUES (127, '53ebeb69f1b6cb91b7cfa5387e81fe795eba5adb9a36252c8eaa21e143f33156', 'MASCULINO');
INSERT INTO public.bi_dim_paciente_anon VALUES (128, 'ad9fb70ce133af2c7e6a87a4fbe4ca8974c933a00c2a028c4dd5e7f4983fa1d8', 'MASCULINO');
INSERT INTO public.bi_dim_paciente_anon VALUES (129, '9428fcf4167d75c847ec8a3751fc58ae41b1bdd4edca9041ce6cd4d5465b71e4', 'NAO_INFORMADO');
INSERT INTO public.bi_dim_paciente_anon VALUES (130, 'f0a990c01f567a2110b0ad3b5fff316a1d3dab3fb82157028c0f28186b898bc7', 'MASCULINO');
INSERT INTO public.bi_dim_paciente_anon VALUES (131, '1cb0bf9063ce82a37b753117d4fc3a1c1b3fa872c52e40a233e2529d561b3510', 'MASCULINO');
INSERT INTO public.bi_dim_paciente_anon VALUES (132, '1b5d75155745d15056ad8b7eca4e3c0f737c18fb7bbb2b4f4f17033a0a7f4d2b', 'MASCULINO');
INSERT INTO public.bi_dim_paciente_anon VALUES (133, 'cb701997c97b8831ee72713ab4adbebcb63e6bc72397901619da7390a7d8f573', 'NAO_INFORMADO');
INSERT INTO public.bi_dim_paciente_anon VALUES (134, '7b937e7c1d74b03639036e0efbd972b2a45f55677b3f8def8afe42732ca51dee', 'MASCULINO');
INSERT INTO public.bi_dim_paciente_anon VALUES (135, 'fb477efc66e4540077772bd7d5963a21bf6f4dd584ce592afe9052d3b212ee36', 'NAO_INFORMADO');
INSERT INTO public.bi_dim_paciente_anon VALUES (136, '8674d6e1dd7f36be89c8b0998e5197ccca15e0a01c403300308b9c3ecb326b78', 'MASCULINO');
INSERT INTO public.bi_dim_paciente_anon VALUES (137, 'b693b29cb25deab84face2f3f51438fe2f7b025185a7cb4447dd51b5d9f64ff6', 'MASCULINO');
INSERT INTO public.bi_dim_paciente_anon VALUES (138, '7ba6030af1196fe7a49c0d595994cdb796b1201779a07ea7951104c4f28e0209', 'FEMININO');
INSERT INTO public.bi_dim_paciente_anon VALUES (139, 'd9b5f387651a7de6c2db7d70f42de1214858541f890be370dbbf4826b014f657', 'FEMININO');
INSERT INTO public.bi_dim_paciente_anon VALUES (140, 'c629e55f8f79965c5f8c6f355d68b4e65866e1d24765bf912c8d8687b8558dbb', 'FEMININO');
INSERT INTO public.bi_dim_paciente_anon VALUES (141, 'c029e72eaf772067631751fe856d0183b9518d0688b862d30e5f1b2bd5667480', 'MASCULINO');
INSERT INTO public.bi_dim_paciente_anon VALUES (142, '9499d592725386c3c2d1af3a5c8a945ab5f173ba0790dc352ab1b7238043dbd1', 'NAO_INFORMADO');
INSERT INTO public.bi_dim_paciente_anon VALUES (143, '3a6a355196338f5f97be9cb93f33f1142647bca8bac1fd8a2d06c41d2c04e338', 'FEMININO');
INSERT INTO public.bi_dim_paciente_anon VALUES (144, 'f144449dd653eea7914d58ec599e81773fe3c9a259343d9f3e33e9ca96bb24aa', 'NAO_INFORMADO');
INSERT INTO public.bi_dim_paciente_anon VALUES (145, 'e91a0f5f060a32f86a14b29fa7d94f9fff718077d2edb4974d58203cea0dd403', 'NAO_INFORMADO');
INSERT INTO public.bi_dim_paciente_anon VALUES (146, 'd5c5ec692aa0ee746e89bb65ccd51f19228d93ca57bf54fe4a264b45eb042c1b', 'MASCULINO');
INSERT INTO public.bi_dim_paciente_anon VALUES (147, '7a7116150400d91e4c65d4fe54fb8eac9b2b152901df9f5e3eae78ee08817b10', 'MASCULINO');
INSERT INTO public.bi_dim_paciente_anon VALUES (148, '52e294a78ea90c2dfadff4f97e0f515dec40b14128d545ced6393da6f6981900', 'MASCULINO');
INSERT INTO public.bi_dim_paciente_anon VALUES (149, 'e3fd4611b8a3b39b18d40efee3b59888e65249d40fd1a5b403f2dec940586262', 'NAO_INFORMADO');
INSERT INTO public.bi_dim_paciente_anon VALUES (150, '19dbfb767d5607548fa1a0d3a04e5e8349ff4b09ff61569e9803b6814cfb7b85', 'FEMININO');
INSERT INTO public.bi_dim_paciente_anon VALUES (151, '573b6ab1d80de0d27aa8ef95ffb4b3698886d6aeb61535b49fa2766bd166a069', 'FEMININO');
INSERT INTO public.bi_dim_paciente_anon VALUES (152, '28c7298941a1543caebf283687f67b20a9874122adda366aec12beef7240e4ea', 'MASCULINO');
INSERT INTO public.bi_dim_paciente_anon VALUES (153, 'a5e6f30c2061082c18362da0709be63a38a569ace7b9910b7c45a584299def53', 'FEMININO');
INSERT INTO public.bi_dim_paciente_anon VALUES (154, 'ad84792eca98882db72b5c48807e1707bdfba6ed29664afe23e834eeda4ae154', 'MASCULINO');
INSERT INTO public.bi_dim_paciente_anon VALUES (155, '45dfa48f8af2324cb546a958461970a72181ae1f5aa1ff3f289fade53081e68c', 'MASCULINO');
INSERT INTO public.bi_dim_paciente_anon VALUES (156, 'c2e9555fbc5a4707731d661cabd3da84903f65121f26897b32ab80de73a46c58', 'FEMININO');
INSERT INTO public.bi_dim_paciente_anon VALUES (157, '7f2bff542b900b516dd1905fe88e413bea423d3bc851a4c0101f598769b85814', 'MASCULINO');
INSERT INTO public.bi_dim_paciente_anon VALUES (158, 'e2567d0e968ef2432fb7dcb249b6b4b3fdfc89d8226a9c39b6044e96ce5c0ca7', 'FEMININO');
INSERT INTO public.bi_dim_paciente_anon VALUES (159, 'd9b332857c9c4fb6033030efd2cd8ae252db5b350175087e3db4e58238314844', 'MASCULINO');
INSERT INTO public.bi_dim_paciente_anon VALUES (160, 'bc18dbc164f035acb127c5b2ad0ea5bb84e4fba0cc95d6a7cc42d81df64cec97', 'FEMININO');
INSERT INTO public.bi_dim_paciente_anon VALUES (161, '8813f728a22e83728657ae8147b6db0f3b171e56f938a2bfcecd47a04cc72083', 'FEMININO');
INSERT INTO public.bi_dim_paciente_anon VALUES (162, '21a5ef3e0b337ca90bdec5342a625ae103926999c3f630a31e1444405c9b6e64', 'MASCULINO');
INSERT INTO public.bi_dim_paciente_anon VALUES (163, 'fac6803fbe33fb84c0fc09acb214b09725897799cf3ae1a44032c1acb89a0c56', 'FEMININO');
INSERT INTO public.bi_dim_paciente_anon VALUES (164, '08d926db65b96c0ea87088fe66476ca900a18b77525fea57d2d1bdb2de8ea110', 'FEMININO');
INSERT INTO public.bi_dim_paciente_anon VALUES (165, 'cc5b66536f72c0b27fbb348312b0334639f6cf21e25cb40c8f7f7545b1a6f252', 'FEMININO');
INSERT INTO public.bi_dim_paciente_anon VALUES (166, '56cc68c783f0ab167195e6dd717e81d26a48d7de5e541ad48656589088bb9fe5', 'NAO_INFORMADO');
INSERT INTO public.bi_dim_paciente_anon VALUES (167, '5883fabf13ace9a35eff785ca0de3b4d2c35329d1bf63c8d0288e3ec133d344d', 'MASCULINO');
INSERT INTO public.bi_dim_paciente_anon VALUES (168, '7f5c5bf0b10ba93c59aa08ee1d4476cdc005ab238668f559b26c2ee98c6ea613', 'MASCULINO');
INSERT INTO public.bi_dim_paciente_anon VALUES (169, 'bbd387fbf0acee11678691f8a90fd68d763543976d68b02e9afd0861e4ac569b', 'FEMININO');
INSERT INTO public.bi_dim_paciente_anon VALUES (170, '9d003a7495854e9d4c1d89f2267a6474025e038e34616cf3243e0533a2826c7a', 'NAO_INFORMADO');
INSERT INTO public.bi_dim_paciente_anon VALUES (171, 'eda788dbe04d17e0ba05ac6e28c0d2c8e592095a0398b721eaf5c8e92d362c41', 'FEMININO');
INSERT INTO public.bi_dim_paciente_anon VALUES (172, '4ffc4ae5b14066abe236e68fba4584620bb74fda8ea536702d5825fdf2397a15', 'NAO_INFORMADO');
INSERT INTO public.bi_dim_paciente_anon VALUES (173, '38261c18dba3be1fb7341b3bd890468f0fb5e4a8a49adea68ba412bf5bb7859a', 'NAO_INFORMADO');
INSERT INTO public.bi_dim_paciente_anon VALUES (174, '795da32d0ffde1c873e520b2338ae7421d798f2157b1cbf2b37fed00fd371fc1', 'NAO_INFORMADO');
INSERT INTO public.bi_dim_paciente_anon VALUES (175, 'eb7e85705df3c6b8ec90b60dbf6d61d0ff9f81b38bcaa992fadf063863b9fb9b', 'FEMININO');
INSERT INTO public.bi_dim_paciente_anon VALUES (176, '7793a272310649a0ad6b5b4eb6e3d1c019d3748cf5293fc461d5aa9ea83f291c', 'MASCULINO');
INSERT INTO public.bi_dim_paciente_anon VALUES (177, '99a3f951d24f6f071e93b7bee98f339e3c747c80ed13554fa9d5cd2484a108ef', 'MASCULINO');
INSERT INTO public.bi_dim_paciente_anon VALUES (178, 'e8a4bcb27049ac8f4ebd178d1896ac9f97a21bb96c43d3599aec2254aa17de5f', 'FEMININO');
INSERT INTO public.bi_dim_paciente_anon VALUES (179, '5e54a31fec819a4958b85f039f23a1333a142a05d4c1673ad7d91b693a986fdf', 'NAO_INFORMADO');
INSERT INTO public.bi_dim_paciente_anon VALUES (180, '60957565b303c79d14414cd70e9a321ab8a36da66aecbf1c17015a2d9640b3a6', 'FEMININO');
INSERT INTO public.bi_dim_paciente_anon VALUES (181, '47926068d93a0f97e20b0779e8c0ea50a61889b510c9116a18a370c6bcfe68e7', 'FEMININO');
INSERT INTO public.bi_dim_paciente_anon VALUES (182, 'a9899cf8f922251887c11ba5b6d02e95de87dc2da76ce13599fc340f00e047be', 'MASCULINO');
INSERT INTO public.bi_dim_paciente_anon VALUES (183, '408579ec50fe6a5dff79190f92952d81b39f7b26536a597241f6ca3ee581c709', 'FEMININO');
INSERT INTO public.bi_dim_paciente_anon VALUES (184, '61b731d1315c304caa9b6f073ade43870cdedbdcf355cb6263ed4e14189e163c', 'NAO_INFORMADO');
INSERT INTO public.bi_dim_paciente_anon VALUES (185, '3018122325d76de2302b58c1b3724627217ec923b0d2ce237a72f4ac718759e3', 'NAO_INFORMADO');
INSERT INTO public.bi_dim_paciente_anon VALUES (186, '71724f0266475bd9c74711a80cbd3ff77ea8d69ab2eb89d04116ac90a6d2c0da', 'NAO_INFORMADO');
INSERT INTO public.bi_dim_paciente_anon VALUES (187, '0d819b85174930d4a2671d7b54c99d5d398d9d97fbf1358118afa2f3594f8fe5', 'FEMININO');
INSERT INTO public.bi_dim_paciente_anon VALUES (188, '638e07d99195f2a33680700e766a016dd173fb8edad9fe24c55a4f9488b30f30', 'NAO_INFORMADO');
INSERT INTO public.bi_dim_paciente_anon VALUES (189, '6648cee210d7e9b3dc3eb311b9c92dd6dd5e0341b250430223f9738c99454810', 'MASCULINO');
INSERT INTO public.bi_dim_paciente_anon VALUES (190, '0e19b99d61b700d2d27ad1704bce1cdd1dd2a8dd859ffaabc29a97ba7308a47f', 'MASCULINO');
INSERT INTO public.bi_dim_paciente_anon VALUES (191, '27f58c62ef04db054fe2b8495943156e40048aa3531de35cae48eb9a76848a6b', 'NAO_INFORMADO');
INSERT INTO public.bi_dim_paciente_anon VALUES (192, '893436e839e370ab365fb4abaf53cb1ad06d69c798c69f33e9db13e9b416a0e2', 'MASCULINO');
INSERT INTO public.bi_dim_paciente_anon VALUES (193, 'eb7b474f010558c4f8543dc65b3fe3375b0db0951e7f4ac3da4462366fadd7f8', 'MASCULINO');
INSERT INTO public.bi_dim_paciente_anon VALUES (194, 'b12b2ff6bca9b4d2a02151b6cf747858135e2fdd07b02feaed51efca7324764f', 'NAO_INFORMADO');
INSERT INTO public.bi_dim_paciente_anon VALUES (195, '40da0e69c4d12f92f7c2b073ca6024fdab3954a7d21b19119bc3ebc0908884ff', 'MASCULINO');
INSERT INTO public.bi_dim_paciente_anon VALUES (196, '66366a4edb4b2875aaa0e3b804dbb97d170701f3bd055c27f225166786652246', 'NAO_INFORMADO');
INSERT INTO public.bi_dim_paciente_anon VALUES (197, '4fea14b1f85c18e1649123bb4cd8dc619994ef62c72636fb16e957bacd24ffe8', 'FEMININO');
INSERT INTO public.bi_dim_paciente_anon VALUES (198, 'f7d5a20e5cfa6fd9daa329a2be02142b15382b39b229cfb963cdd12512d536b5', 'MASCULINO');
INSERT INTO public.bi_dim_paciente_anon VALUES (199, 'f1d57f9204689687cb2e74a1211851350baaf73c8f84d2453113c3ee31746e56', 'MASCULINO');
INSERT INTO public.bi_dim_paciente_anon VALUES (200, '0940f5281fc0cdbffa1b88ffdd71d98b32c449c199be3ad7432a6f406bc867fb', 'MASCULINO');
INSERT INTO public.bi_dim_paciente_anon VALUES (201, '452500f0a1ba2834da1fac3a42182cef0e2bc522dc2b0466896461147d2b8b02', 'MASCULINO');
INSERT INTO public.bi_dim_paciente_anon VALUES (202, 'b507e2419965c9bb22635a2d69cf1a135f213a7cd449dbff0f405ced893460e3', 'FEMININO');
INSERT INTO public.bi_dim_paciente_anon VALUES (203, '68cf80df1d129ba4f2b090d7720b6f430565fd86da2edb7b84e0417f32d4dd67', 'NAO_INFORMADO');
INSERT INTO public.bi_dim_paciente_anon VALUES (204, '67f6a0e6d84f1a80c33382c99b545eb1560b587457bca9120e084707e379da59', 'NAO_INFORMADO');
INSERT INTO public.bi_dim_paciente_anon VALUES (205, '33a60064895c32e035bb01872cdbb39ac882f242503b18a06e60fdc9905d32e9', 'MASCULINO');
INSERT INTO public.bi_dim_paciente_anon VALUES (206, '87162be83a31c8ba8f0122801d74ae1a210b073c751fc766ae565562a98ccd82', 'MASCULINO');
INSERT INTO public.bi_dim_paciente_anon VALUES (207, '482f295027fdead2300f87e3f2c6c545121b62c32e5b456898c1e44f3e259729', 'FEMININO');
INSERT INTO public.bi_dim_paciente_anon VALUES (208, '9c27ec72e4d93167f834ece42c701b080a63f81a40365fb81cd4398fbf4410ee', 'NAO_INFORMADO');
INSERT INTO public.bi_dim_paciente_anon VALUES (209, '5ab170255d6f3e229fa2a5ccc7fe1590bed4b62b958de5e2245ed20a2edeed53', 'MASCULINO');
INSERT INTO public.bi_dim_paciente_anon VALUES (210, 'b3f068006bc75d629098d6da5a19ae4d5087b9c5d9dd923623c5576ae658ed61', 'MASCULINO');
INSERT INTO public.bi_dim_paciente_anon VALUES (211, '6cedca955ba5b3b3cd827b708d2225c237219b4529a198ea64ea6ff72fe4ec48', 'MASCULINO');
INSERT INTO public.bi_dim_paciente_anon VALUES (212, 'bc64f0ef315d28cb959c3729947e9e41dd3a2916414ffd21f3b7433a36bd737d', 'FEMININO');
INSERT INTO public.bi_dim_paciente_anon VALUES (213, 'c4e2bf16186cf668e0160eda449c286b5b900bcbe20132cd54c1a47fde4b9df5', 'FEMININO');
INSERT INTO public.bi_dim_paciente_anon VALUES (214, '5ed048f048fd68113c7c68293918163027e310be059c31f2ed44c1364359e82a', 'MASCULINO');
INSERT INTO public.bi_dim_paciente_anon VALUES (215, '87c151af5174a900b4793cdaeec0a623d4f7665364445c98c47ff1b53c026d2d', 'MASCULINO');
INSERT INTO public.bi_dim_paciente_anon VALUES (216, '32856739d515d5f7300ba3ed6065a645b021c7f3a5206e03848558ab467bb54f', 'FEMININO');
INSERT INTO public.bi_dim_paciente_anon VALUES (217, 'a54fbe0dc95aeca119df61ef34fe3baa130d8d502ebdf19ec45e3bea980adafb', 'MASCULINO');
INSERT INTO public.bi_dim_paciente_anon VALUES (218, '07f7d009e1e97da898de6580dd67d33fb6d97fde441468a7200517c4a49f2c57', 'MASCULINO');
INSERT INTO public.bi_dim_paciente_anon VALUES (219, '39914604233b94ba178e9aa32131d8a6deae0105f25b1599d239597b8c6e61e4', 'MASCULINO');
INSERT INTO public.bi_dim_paciente_anon VALUES (220, 'daf5eaaf9e7a6644d0a72cd0276cac07ea98d5c6c0e56d387167d3cea336bfb7', 'MASCULINO');


--
-- Data for Name: bi_dim_setor; Type: TABLE DATA; Schema: public; Owner: labvida
--

INSERT INTO public.bi_dim_setor VALUES (1, 'SEM_SETOR', 'Sem setor');
INSERT INTO public.bi_dim_setor VALUES (2, 'hematologia', 'Hematologia');
INSERT INTO public.bi_dim_setor VALUES (3, 'bioquímica', 'Bioquímica');
INSERT INTO public.bi_dim_setor VALUES (4, 'imunologia', 'Imunologia');
INSERT INTO public.bi_dim_setor VALUES (5, 'urinálise', 'Urinálise');
INSERT INTO public.bi_dim_setor VALUES (6, 'microbiologia', 'Microbiologia');


--
-- Data for Name: bi_dim_procedimento; Type: TABLE DATA; Schema: public; Owner: labvida
--

INSERT INTO public.bi_dim_procedimento VALUES (1, 'a04b1b8a-f87c-4e0f-a7ac-2bf6b5f8249f', '40302016', 'Hemograma completo', 'Hematologia', 2, true);
INSERT INTO public.bi_dim_procedimento VALUES (2, '3447243c-c361-4cd9-99d2-71efdc0dd9cc', '40302040', 'Contagem de plaquetas', 'Hematologia', 2, true);
INSERT INTO public.bi_dim_procedimento VALUES (3, '0401871d-a92c-478f-8fe4-81203fea94e0', '40304361', 'Tempo de protrombina (TAP)', 'Hematologia', 2, true);
INSERT INTO public.bi_dim_procedimento VALUES (4, '9fb46fe1-6a88-4fed-b039-b690d98e8336', '40304370', 'Tempo de tromboplastina (TTPA)', 'Hematologia', 2, true);
INSERT INTO public.bi_dim_procedimento VALUES (5, '089461ba-d5d7-4af4-b377-0c4f93693d7b', '40304060', 'Hemoglobina glicada (HbA1c)', 'Hematologia', 2, true);
INSERT INTO public.bi_dim_procedimento VALUES (6, 'f57a5298-4454-4648-8046-83b3c5786ed9', '40301630', 'Glicose', 'Bioquímica', 3, true);
INSERT INTO public.bi_dim_procedimento VALUES (7, '647a5ccd-2417-48e2-9eaf-eda95dfac347', '40301770', 'Colesterol total', 'Bioquímica', 3, true);
INSERT INTO public.bi_dim_procedimento VALUES (8, '63b5238c-a7d4-419f-82ec-5e857e7bcf8d', '40301788', 'HDL colesterol', 'Bioquímica', 3, true);
INSERT INTO public.bi_dim_procedimento VALUES (9, '5c072820-2256-49cd-8965-82d31f75cff0', '40301796', 'LDL colesterol', 'Bioquímica', 3, true);
INSERT INTO public.bi_dim_procedimento VALUES (10, 'a49b4f7f-fb1f-4df0-b23d-a89df3266348', '40302113', 'Triglicerídeos', 'Bioquímica', 3, true);
INSERT INTO public.bi_dim_procedimento VALUES (11, '053bdc36-13b6-4c79-a2ab-415dec1cda76', '40301672', 'Ureia', 'Bioquímica', 3, true);
INSERT INTO public.bi_dim_procedimento VALUES (12, '60f84c84-284c-4d5f-a551-ff6baeb82ef8', '40301680', 'Creatinina', 'Bioquímica', 3, true);
INSERT INTO public.bi_dim_procedimento VALUES (13, '6f3bedc2-676e-49e0-a55d-bfec75ea2f59', '40301842', 'Ácido úrico', 'Bioquímica', 3, true);
INSERT INTO public.bi_dim_procedimento VALUES (14, '75047dd7-1944-4464-a787-645036c6a256', '40302261', 'TGO / AST', 'Bioquímica', 3, true);
INSERT INTO public.bi_dim_procedimento VALUES (15, '40e2fb45-6866-4fe4-b966-9259a4b29333', '40302270', 'TGP / ALT', 'Bioquímica', 3, true);
INSERT INTO public.bi_dim_procedimento VALUES (16, '8bdc21ed-ae3e-4137-aa9f-83c58076adf3', '40302130', 'Gama GT', 'Bioquímica', 3, true);
INSERT INTO public.bi_dim_procedimento VALUES (17, '1254e336-9074-4006-8056-88c2814155ef', '40301974', 'Fosfatase alcalina', 'Bioquímica', 3, true);
INSERT INTO public.bi_dim_procedimento VALUES (18, '5af8e8ba-9820-4c4b-9778-df089b076214', '40301541', 'Ferro sérico', 'Bioquímica', 3, true);
INSERT INTO public.bi_dim_procedimento VALUES (19, 'af9068a5-6da2-4d82-b530-b3e1220963b3', '40310060', 'Ferritina', 'Imunologia', 4, true);
INSERT INTO public.bi_dim_procedimento VALUES (20, '7da23239-1a29-48b3-a3ba-1c3fd8fc88d8', '40311902', 'TSH — hormônio tireoestimulante', 'Imunologia', 4, true);
INSERT INTO public.bi_dim_procedimento VALUES (21, '31ae4369-05d5-48ee-a60c-fc45e6ea138d', '40311945', 'T4 livre', 'Imunologia', 4, true);
INSERT INTO public.bi_dim_procedimento VALUES (22, 'bd97b306-3cb7-4f53-a8d6-107477c57a8c', '40316203', 'Vitamina D (25-OH)', 'Imunologia', 4, true);
INSERT INTO public.bi_dim_procedimento VALUES (23, '1c3f4be4-ff6e-4c1b-8249-6665edfc8f62', '40316300', 'Vitamina B12', 'Imunologia', 4, true);
INSERT INTO public.bi_dim_procedimento VALUES (24, '61d011dd-fb23-4fd4-8c26-1ad1bccf3cda', '40316165', 'PSA total', 'Imunologia', 4, true);
INSERT INTO public.bi_dim_procedimento VALUES (25, '0b975ec3-3268-491d-b1d1-81778a8b4596', '40302172', 'Proteína C reativa (PCR)', 'Imunologia', 4, true);
INSERT INTO public.bi_dim_procedimento VALUES (26, '0b7dbbaf-0908-4b73-a57c-a73f0003266e', '40310354', 'Beta HCG quantitativo', 'Imunologia', 4, true);
INSERT INTO public.bi_dim_procedimento VALUES (27, '5a810975-0c2b-44f3-89cf-6c9fcddcb7db', '40308635', 'VDRL', 'Imunologia', 4, true);
INSERT INTO public.bi_dim_procedimento VALUES (28, 'c1a37911-f27c-420c-a633-7a8656eee5b4', '40307450', 'Urina tipo I (EAS)', 'Urinálise', 5, true);
INSERT INTO public.bi_dim_procedimento VALUES (29, 'c24c7ad0-68e9-425c-b9f8-d257510d2201', '40310120', 'Urocultura com antibiograma', 'Microbiologia', 6, true);
INSERT INTO public.bi_dim_procedimento VALUES (30, 'abeb6525-15ea-4e8f-9d22-ee0ef7ed97af', '40308880', 'Parasitológico de fezes', 'Microbiologia', 6, true);


--
-- Data for Name: bi_dim_tempo; Type: TABLE DATA; Schema: public; Owner: labvida
--

INSERT INTO public.bi_dim_tempo VALUES (1, '2026-05-01', 2026, 5, 1, 'Sexta-feira', 4, 2, 1, 18, 'Maio', '2026-05', '2026-05-01', true);
INSERT INTO public.bi_dim_tempo VALUES (2, '2026-05-02', 2026, 5, 2, 'Sabado', 5, 2, 1, 18, 'Maio', '2026-05', '2026-05-01', false);
INSERT INTO public.bi_dim_tempo VALUES (3, '2026-05-03', 2026, 5, 3, 'Domingo', 6, 2, 1, 18, 'Maio', '2026-05', '2026-05-01', false);
INSERT INTO public.bi_dim_tempo VALUES (4, '2026-05-04', 2026, 5, 4, 'Segunda-feira', 0, 2, 1, 19, 'Maio', '2026-05', '2026-05-01', true);
INSERT INTO public.bi_dim_tempo VALUES (5, '2026-05-05', 2026, 5, 5, 'Terca-feira', 1, 2, 1, 19, 'Maio', '2026-05', '2026-05-01', true);
INSERT INTO public.bi_dim_tempo VALUES (6, '2026-05-06', 2026, 5, 6, 'Quarta-feira', 2, 2, 1, 19, 'Maio', '2026-05', '2026-05-01', true);
INSERT INTO public.bi_dim_tempo VALUES (7, '2026-05-07', 2026, 5, 7, 'Quinta-feira', 3, 2, 1, 19, 'Maio', '2026-05', '2026-05-01', true);
INSERT INTO public.bi_dim_tempo VALUES (8, '2026-05-08', 2026, 5, 8, 'Sexta-feira', 4, 2, 1, 19, 'Maio', '2026-05', '2026-05-01', true);
INSERT INTO public.bi_dim_tempo VALUES (9, '2026-05-09', 2026, 5, 9, 'Sabado', 5, 2, 1, 19, 'Maio', '2026-05', '2026-05-01', false);
INSERT INTO public.bi_dim_tempo VALUES (10, '2026-05-10', 2026, 5, 10, 'Domingo', 6, 2, 1, 19, 'Maio', '2026-05', '2026-05-01', false);
INSERT INTO public.bi_dim_tempo VALUES (11, '2026-05-11', 2026, 5, 11, 'Segunda-feira', 0, 2, 1, 20, 'Maio', '2026-05', '2026-05-01', true);
INSERT INTO public.bi_dim_tempo VALUES (12, '2026-05-12', 2026, 5, 12, 'Terca-feira', 1, 2, 1, 20, 'Maio', '2026-05', '2026-05-01', true);
INSERT INTO public.bi_dim_tempo VALUES (13, '2026-05-13', 2026, 5, 13, 'Quarta-feira', 2, 2, 1, 20, 'Maio', '2026-05', '2026-05-01', true);
INSERT INTO public.bi_dim_tempo VALUES (14, '2026-05-14', 2026, 5, 14, 'Quinta-feira', 3, 2, 1, 20, 'Maio', '2026-05', '2026-05-01', true);
INSERT INTO public.bi_dim_tempo VALUES (15, '2026-05-15', 2026, 5, 15, 'Sexta-feira', 4, 2, 1, 20, 'Maio', '2026-05', '2026-05-01', true);
INSERT INTO public.bi_dim_tempo VALUES (16, '2026-05-16', 2026, 5, 16, 'Sabado', 5, 2, 1, 20, 'Maio', '2026-05', '2026-05-01', false);
INSERT INTO public.bi_dim_tempo VALUES (17, '2026-05-17', 2026, 5, 17, 'Domingo', 6, 2, 1, 20, 'Maio', '2026-05', '2026-05-01', false);
INSERT INTO public.bi_dim_tempo VALUES (18, '2026-05-18', 2026, 5, 18, 'Segunda-feira', 0, 2, 1, 21, 'Maio', '2026-05', '2026-05-01', true);
INSERT INTO public.bi_dim_tempo VALUES (19, '2026-05-19', 2026, 5, 19, 'Terca-feira', 1, 2, 1, 21, 'Maio', '2026-05', '2026-05-01', true);
INSERT INTO public.bi_dim_tempo VALUES (20, '2026-05-20', 2026, 5, 20, 'Quarta-feira', 2, 2, 1, 21, 'Maio', '2026-05', '2026-05-01', true);
INSERT INTO public.bi_dim_tempo VALUES (21, '2026-05-21', 2026, 5, 21, 'Quinta-feira', 3, 2, 1, 21, 'Maio', '2026-05', '2026-05-01', true);
INSERT INTO public.bi_dim_tempo VALUES (22, '2026-05-22', 2026, 5, 22, 'Sexta-feira', 4, 2, 1, 21, 'Maio', '2026-05', '2026-05-01', true);
INSERT INTO public.bi_dim_tempo VALUES (23, '2026-05-23', 2026, 5, 23, 'Sabado', 5, 2, 1, 21, 'Maio', '2026-05', '2026-05-01', false);
INSERT INTO public.bi_dim_tempo VALUES (24, '2026-05-24', 2026, 5, 24, 'Domingo', 6, 2, 1, 21, 'Maio', '2026-05', '2026-05-01', false);
INSERT INTO public.bi_dim_tempo VALUES (25, '2026-05-25', 2026, 5, 25, 'Segunda-feira', 0, 2, 1, 22, 'Maio', '2026-05', '2026-05-01', true);
INSERT INTO public.bi_dim_tempo VALUES (26, '2026-05-26', 2026, 5, 26, 'Terca-feira', 1, 2, 1, 22, 'Maio', '2026-05', '2026-05-01', true);
INSERT INTO public.bi_dim_tempo VALUES (27, '2026-05-27', 2026, 5, 27, 'Quarta-feira', 2, 2, 1, 22, 'Maio', '2026-05', '2026-05-01', true);
INSERT INTO public.bi_dim_tempo VALUES (28, '2026-05-28', 2026, 5, 28, 'Quinta-feira', 3, 2, 1, 22, 'Maio', '2026-05', '2026-05-01', true);
INSERT INTO public.bi_dim_tempo VALUES (29, '2026-05-29', 2026, 5, 29, 'Sexta-feira', 4, 2, 1, 22, 'Maio', '2026-05', '2026-05-01', true);
INSERT INTO public.bi_dim_tempo VALUES (30, '2026-05-30', 2026, 5, 30, 'Sabado', 5, 2, 1, 22, 'Maio', '2026-05', '2026-05-01', false);
INSERT INTO public.bi_dim_tempo VALUES (31, '2026-05-31', 2026, 5, 31, 'Domingo', 6, 2, 1, 22, 'Maio', '2026-05', '2026-05-01', false);
INSERT INTO public.bi_dim_tempo VALUES (32, '2026-06-01', 2026, 6, 1, 'Segunda-feira', 0, 2, 1, 23, 'Junho', '2026-06', '2026-06-01', true);
INSERT INTO public.bi_dim_tempo VALUES (33, '2026-06-02', 2026, 6, 2, 'Terca-feira', 1, 2, 1, 23, 'Junho', '2026-06', '2026-06-01', true);
INSERT INTO public.bi_dim_tempo VALUES (34, '2026-06-03', 2026, 6, 3, 'Quarta-feira', 2, 2, 1, 23, 'Junho', '2026-06', '2026-06-01', true);
INSERT INTO public.bi_dim_tempo VALUES (35, '2026-06-04', 2026, 6, 4, 'Quinta-feira', 3, 2, 1, 23, 'Junho', '2026-06', '2026-06-01', true);
INSERT INTO public.bi_dim_tempo VALUES (36, '2026-06-05', 2026, 6, 5, 'Sexta-feira', 4, 2, 1, 23, 'Junho', '2026-06', '2026-06-01', true);
INSERT INTO public.bi_dim_tempo VALUES (37, '2026-06-06', 2026, 6, 6, 'Sabado', 5, 2, 1, 23, 'Junho', '2026-06', '2026-06-01', false);
INSERT INTO public.bi_dim_tempo VALUES (38, '2026-06-07', 2026, 6, 7, 'Domingo', 6, 2, 1, 23, 'Junho', '2026-06', '2026-06-01', false);
INSERT INTO public.bi_dim_tempo VALUES (39, '2026-06-08', 2026, 6, 8, 'Segunda-feira', 0, 2, 1, 24, 'Junho', '2026-06', '2026-06-01', true);
INSERT INTO public.bi_dim_tempo VALUES (40, '2026-06-09', 2026, 6, 9, 'Terca-feira', 1, 2, 1, 24, 'Junho', '2026-06', '2026-06-01', true);
INSERT INTO public.bi_dim_tempo VALUES (41, '2026-06-10', 2026, 6, 10, 'Quarta-feira', 2, 2, 1, 24, 'Junho', '2026-06', '2026-06-01', true);
INSERT INTO public.bi_dim_tempo VALUES (42, '2026-06-11', 2026, 6, 11, 'Quinta-feira', 3, 2, 1, 24, 'Junho', '2026-06', '2026-06-01', true);
INSERT INTO public.bi_dim_tempo VALUES (43, '2026-06-12', 2026, 6, 12, 'Sexta-feira', 4, 2, 1, 24, 'Junho', '2026-06', '2026-06-01', true);
INSERT INTO public.bi_dim_tempo VALUES (44, '2026-06-13', 2026, 6, 13, 'Sabado', 5, 2, 1, 24, 'Junho', '2026-06', '2026-06-01', false);
INSERT INTO public.bi_dim_tempo VALUES (45, '2026-06-14', 2026, 6, 14, 'Domingo', 6, 2, 1, 24, 'Junho', '2026-06', '2026-06-01', false);
INSERT INTO public.bi_dim_tempo VALUES (46, '2026-06-15', 2026, 6, 15, 'Segunda-feira', 0, 2, 1, 25, 'Junho', '2026-06', '2026-06-01', true);
INSERT INTO public.bi_dim_tempo VALUES (47, '2026-06-16', 2026, 6, 16, 'Terca-feira', 1, 2, 1, 25, 'Junho', '2026-06', '2026-06-01', true);
INSERT INTO public.bi_dim_tempo VALUES (48, '2026-06-17', 2026, 6, 17, 'Quarta-feira', 2, 2, 1, 25, 'Junho', '2026-06', '2026-06-01', true);
INSERT INTO public.bi_dim_tempo VALUES (49, '2026-06-18', 2026, 6, 18, 'Quinta-feira', 3, 2, 1, 25, 'Junho', '2026-06', '2026-06-01', true);
INSERT INTO public.bi_dim_tempo VALUES (50, '2026-06-19', 2026, 6, 19, 'Sexta-feira', 4, 2, 1, 25, 'Junho', '2026-06', '2026-06-01', true);
INSERT INTO public.bi_dim_tempo VALUES (51, '2026-06-20', 2026, 6, 20, 'Sabado', 5, 2, 1, 25, 'Junho', '2026-06', '2026-06-01', false);
INSERT INTO public.bi_dim_tempo VALUES (52, '2026-06-21', 2026, 6, 21, 'Domingo', 6, 2, 1, 25, 'Junho', '2026-06', '2026-06-01', false);
INSERT INTO public.bi_dim_tempo VALUES (53, '2026-06-22', 2026, 6, 22, 'Segunda-feira', 0, 2, 1, 26, 'Junho', '2026-06', '2026-06-01', true);
INSERT INTO public.bi_dim_tempo VALUES (54, '2026-06-23', 2026, 6, 23, 'Terca-feira', 1, 2, 1, 26, 'Junho', '2026-06', '2026-06-01', true);
INSERT INTO public.bi_dim_tempo VALUES (55, '2026-06-24', 2026, 6, 24, 'Quarta-feira', 2, 2, 1, 26, 'Junho', '2026-06', '2026-06-01', true);
INSERT INTO public.bi_dim_tempo VALUES (56, '2026-06-25', 2026, 6, 25, 'Quinta-feira', 3, 2, 1, 26, 'Junho', '2026-06', '2026-06-01', true);
INSERT INTO public.bi_dim_tempo VALUES (57, '2026-06-26', 2026, 6, 26, 'Sexta-feira', 4, 2, 1, 26, 'Junho', '2026-06', '2026-06-01', true);
INSERT INTO public.bi_dim_tempo VALUES (58, '2026-06-27', 2026, 6, 27, 'Sabado', 5, 2, 1, 26, 'Junho', '2026-06', '2026-06-01', false);
INSERT INTO public.bi_dim_tempo VALUES (59, '2026-06-28', 2026, 6, 28, 'Domingo', 6, 2, 1, 26, 'Junho', '2026-06', '2026-06-01', false);
INSERT INTO public.bi_dim_tempo VALUES (60, '2026-06-29', 2026, 6, 29, 'Segunda-feira', 0, 2, 1, 27, 'Junho', '2026-06', '2026-06-01', true);
INSERT INTO public.bi_dim_tempo VALUES (61, '2026-06-30', 2026, 6, 30, 'Terca-feira', 1, 2, 1, 27, 'Junho', '2026-06', '2026-06-01', true);
INSERT INTO public.bi_dim_tempo VALUES (62, '2026-07-01', 2026, 7, 1, 'Quarta-feira', 2, 3, 2, 27, 'Julho', '2026-07', '2026-07-01', true);
INSERT INTO public.bi_dim_tempo VALUES (63, '2026-07-02', 2026, 7, 2, 'Quinta-feira', 3, 3, 2, 27, 'Julho', '2026-07', '2026-07-01', true);
INSERT INTO public.bi_dim_tempo VALUES (64, '2026-07-03', 2026, 7, 3, 'Sexta-feira', 4, 3, 2, 27, 'Julho', '2026-07', '2026-07-01', true);
INSERT INTO public.bi_dim_tempo VALUES (65, '2026-07-04', 2026, 7, 4, 'Sabado', 5, 3, 2, 27, 'Julho', '2026-07', '2026-07-01', false);
INSERT INTO public.bi_dim_tempo VALUES (66, '2026-07-05', 2026, 7, 5, 'Domingo', 6, 3, 2, 27, 'Julho', '2026-07', '2026-07-01', false);
INSERT INTO public.bi_dim_tempo VALUES (67, '2026-07-06', 2026, 7, 6, 'Segunda-feira', 0, 3, 2, 28, 'Julho', '2026-07', '2026-07-01', true);
INSERT INTO public.bi_dim_tempo VALUES (68, '2026-07-07', 2026, 7, 7, 'Terca-feira', 1, 3, 2, 28, 'Julho', '2026-07', '2026-07-01', true);
INSERT INTO public.bi_dim_tempo VALUES (69, '2026-07-08', 2026, 7, 8, 'Quarta-feira', 2, 3, 2, 28, 'Julho', '2026-07', '2026-07-01', true);
INSERT INTO public.bi_dim_tempo VALUES (70, '2026-07-09', 2026, 7, 9, 'Quinta-feira', 3, 3, 2, 28, 'Julho', '2026-07', '2026-07-01', true);
INSERT INTO public.bi_dim_tempo VALUES (71, '2026-07-10', 2026, 7, 10, 'Sexta-feira', 4, 3, 2, 28, 'Julho', '2026-07', '2026-07-01', true);
INSERT INTO public.bi_dim_tempo VALUES (72, '2026-07-11', 2026, 7, 11, 'Sabado', 5, 3, 2, 28, 'Julho', '2026-07', '2026-07-01', false);
INSERT INTO public.bi_dim_tempo VALUES (73, '2026-07-12', 2026, 7, 12, 'Domingo', 6, 3, 2, 28, 'Julho', '2026-07', '2026-07-01', false);
INSERT INTO public.bi_dim_tempo VALUES (74, '2026-07-13', 2026, 7, 13, 'Segunda-feira', 0, 3, 2, 29, 'Julho', '2026-07', '2026-07-01', true);
INSERT INTO public.bi_dim_tempo VALUES (75, '2026-07-14', 2026, 7, 14, 'Terca-feira', 1, 3, 2, 29, 'Julho', '2026-07', '2026-07-01', true);
INSERT INTO public.bi_dim_tempo VALUES (76, '2026-07-15', 2026, 7, 15, 'Quarta-feira', 2, 3, 2, 29, 'Julho', '2026-07', '2026-07-01', true);
INSERT INTO public.bi_dim_tempo VALUES (77, '2026-07-16', 2026, 7, 16, 'Quinta-feira', 3, 3, 2, 29, 'Julho', '2026-07', '2026-07-01', true);
INSERT INTO public.bi_dim_tempo VALUES (78, '2026-07-17', 2026, 7, 17, 'Sexta-feira', 4, 3, 2, 29, 'Julho', '2026-07', '2026-07-01', true);
INSERT INTO public.bi_dim_tempo VALUES (79, '2026-07-18', 2026, 7, 18, 'Sabado', 5, 3, 2, 29, 'Julho', '2026-07', '2026-07-01', false);
INSERT INTO public.bi_dim_tempo VALUES (80, '2026-07-19', 2026, 7, 19, 'Domingo', 6, 3, 2, 29, 'Julho', '2026-07', '2026-07-01', false);
INSERT INTO public.bi_dim_tempo VALUES (81, '2026-07-20', 2026, 7, 20, 'Segunda-feira', 0, 3, 2, 30, 'Julho', '2026-07', '2026-07-01', true);
INSERT INTO public.bi_dim_tempo VALUES (82, '2026-07-21', 2026, 7, 21, 'Terca-feira', 1, 3, 2, 30, 'Julho', '2026-07', '2026-07-01', true);
INSERT INTO public.bi_dim_tempo VALUES (83, '2026-07-22', 2026, 7, 22, 'Quarta-feira', 2, 3, 2, 30, 'Julho', '2026-07', '2026-07-01', true);
INSERT INTO public.bi_dim_tempo VALUES (84, '2026-07-23', 2026, 7, 23, 'Quinta-feira', 3, 3, 2, 30, 'Julho', '2026-07', '2026-07-01', true);
INSERT INTO public.bi_dim_tempo VALUES (85, '2026-07-24', 2026, 7, 24, 'Sexta-feira', 4, 3, 2, 30, 'Julho', '2026-07', '2026-07-01', true);
INSERT INTO public.bi_dim_tempo VALUES (86, '2026-07-25', 2026, 7, 25, 'Sabado', 5, 3, 2, 30, 'Julho', '2026-07', '2026-07-01', false);
INSERT INTO public.bi_dim_tempo VALUES (87, '2026-07-26', 2026, 7, 26, 'Domingo', 6, 3, 2, 30, 'Julho', '2026-07', '2026-07-01', false);
INSERT INTO public.bi_dim_tempo VALUES (88, '2026-07-27', 2026, 7, 27, 'Segunda-feira', 0, 3, 2, 31, 'Julho', '2026-07', '2026-07-01', true);
INSERT INTO public.bi_dim_tempo VALUES (89, '2026-07-28', 2026, 7, 28, 'Terca-feira', 1, 3, 2, 31, 'Julho', '2026-07', '2026-07-01', true);
INSERT INTO public.bi_dim_tempo VALUES (90, '2026-07-29', 2026, 7, 29, 'Quarta-feira', 2, 3, 2, 31, 'Julho', '2026-07', '2026-07-01', true);
INSERT INTO public.bi_dim_tempo VALUES (91, '2026-07-30', 2026, 7, 30, 'Quinta-feira', 3, 3, 2, 31, 'Julho', '2026-07', '2026-07-01', true);
INSERT INTO public.bi_dim_tempo VALUES (92, '2026-07-31', 2026, 7, 31, 'Sexta-feira', 4, 3, 2, 31, 'Julho', '2026-07', '2026-07-01', true);
INSERT INTO public.bi_dim_tempo VALUES (93, '2026-08-01', 2026, 8, 1, 'Sabado', 5, 3, 2, 31, 'Agosto', '2026-08', '2026-08-01', false);
INSERT INTO public.bi_dim_tempo VALUES (94, '2026-08-02', 2026, 8, 2, 'Domingo', 6, 3, 2, 31, 'Agosto', '2026-08', '2026-08-01', false);
INSERT INTO public.bi_dim_tempo VALUES (95, '2026-08-03', 2026, 8, 3, 'Segunda-feira', 0, 3, 2, 32, 'Agosto', '2026-08', '2026-08-01', true);
INSERT INTO public.bi_dim_tempo VALUES (96, '2026-08-04', 2026, 8, 4, 'Terca-feira', 1, 3, 2, 32, 'Agosto', '2026-08', '2026-08-01', true);
INSERT INTO public.bi_dim_tempo VALUES (97, '2026-08-05', 2026, 8, 5, 'Quarta-feira', 2, 3, 2, 32, 'Agosto', '2026-08', '2026-08-01', true);
INSERT INTO public.bi_dim_tempo VALUES (98, '2026-08-06', 2026, 8, 6, 'Quinta-feira', 3, 3, 2, 32, 'Agosto', '2026-08', '2026-08-01', true);
INSERT INTO public.bi_dim_tempo VALUES (99, '2026-08-07', 2026, 8, 7, 'Sexta-feira', 4, 3, 2, 32, 'Agosto', '2026-08', '2026-08-01', true);
INSERT INTO public.bi_dim_tempo VALUES (100, '2026-08-08', 2026, 8, 8, 'Sabado', 5, 3, 2, 32, 'Agosto', '2026-08', '2026-08-01', false);
INSERT INTO public.bi_dim_tempo VALUES (101, '2026-08-09', 2026, 8, 9, 'Domingo', 6, 3, 2, 32, 'Agosto', '2026-08', '2026-08-01', false);
INSERT INTO public.bi_dim_tempo VALUES (102, '2026-08-10', 2026, 8, 10, 'Segunda-feira', 0, 3, 2, 33, 'Agosto', '2026-08', '2026-08-01', true);
INSERT INTO public.bi_dim_tempo VALUES (103, '2026-08-11', 2026, 8, 11, 'Terca-feira', 1, 3, 2, 33, 'Agosto', '2026-08', '2026-08-01', true);
INSERT INTO public.bi_dim_tempo VALUES (104, '2026-08-12', 2026, 8, 12, 'Quarta-feira', 2, 3, 2, 33, 'Agosto', '2026-08', '2026-08-01', true);
INSERT INTO public.bi_dim_tempo VALUES (105, '2026-08-13', 2026, 8, 13, 'Quinta-feira', 3, 3, 2, 33, 'Agosto', '2026-08', '2026-08-01', true);
INSERT INTO public.bi_dim_tempo VALUES (106, '2026-08-14', 2026, 8, 14, 'Sexta-feira', 4, 3, 2, 33, 'Agosto', '2026-08', '2026-08-01', true);
INSERT INTO public.bi_dim_tempo VALUES (107, '2026-08-15', 2026, 8, 15, 'Sabado', 5, 3, 2, 33, 'Agosto', '2026-08', '2026-08-01', false);
INSERT INTO public.bi_dim_tempo VALUES (108, '2026-08-16', 2026, 8, 16, 'Domingo', 6, 3, 2, 33, 'Agosto', '2026-08', '2026-08-01', false);
INSERT INTO public.bi_dim_tempo VALUES (109, '2026-08-17', 2026, 8, 17, 'Segunda-feira', 0, 3, 2, 34, 'Agosto', '2026-08', '2026-08-01', true);
INSERT INTO public.bi_dim_tempo VALUES (110, '2026-08-18', 2026, 8, 18, 'Terca-feira', 1, 3, 2, 34, 'Agosto', '2026-08', '2026-08-01', true);
INSERT INTO public.bi_dim_tempo VALUES (111, '2026-08-19', 2026, 8, 19, 'Quarta-feira', 2, 3, 2, 34, 'Agosto', '2026-08', '2026-08-01', true);
INSERT INTO public.bi_dim_tempo VALUES (112, '2026-08-20', 2026, 8, 20, 'Quinta-feira', 3, 3, 2, 34, 'Agosto', '2026-08', '2026-08-01', true);
INSERT INTO public.bi_dim_tempo VALUES (113, '2026-08-21', 2026, 8, 21, 'Sexta-feira', 4, 3, 2, 34, 'Agosto', '2026-08', '2026-08-01', true);
INSERT INTO public.bi_dim_tempo VALUES (114, '2026-08-22', 2026, 8, 22, 'Sabado', 5, 3, 2, 34, 'Agosto', '2026-08', '2026-08-01', false);
INSERT INTO public.bi_dim_tempo VALUES (115, '2026-08-23', 2026, 8, 23, 'Domingo', 6, 3, 2, 34, 'Agosto', '2026-08', '2026-08-01', false);
INSERT INTO public.bi_dim_tempo VALUES (116, '2026-08-24', 2026, 8, 24, 'Segunda-feira', 0, 3, 2, 35, 'Agosto', '2026-08', '2026-08-01', true);
INSERT INTO public.bi_dim_tempo VALUES (117, '2026-08-25', 2026, 8, 25, 'Terca-feira', 1, 3, 2, 35, 'Agosto', '2026-08', '2026-08-01', true);
INSERT INTO public.bi_dim_tempo VALUES (118, '2026-08-26', 2026, 8, 26, 'Quarta-feira', 2, 3, 2, 35, 'Agosto', '2026-08', '2026-08-01', true);
INSERT INTO public.bi_dim_tempo VALUES (119, '2026-08-27', 2026, 8, 27, 'Quinta-feira', 3, 3, 2, 35, 'Agosto', '2026-08', '2026-08-01', true);
INSERT INTO public.bi_dim_tempo VALUES (120, '2026-08-28', 2026, 8, 28, 'Sexta-feira', 4, 3, 2, 35, 'Agosto', '2026-08', '2026-08-01', true);
INSERT INTO public.bi_dim_tempo VALUES (121, '2026-08-29', 2026, 8, 29, 'Sabado', 5, 3, 2, 35, 'Agosto', '2026-08', '2026-08-01', false);
INSERT INTO public.bi_dim_tempo VALUES (122, '2026-08-30', 2026, 8, 30, 'Domingo', 6, 3, 2, 35, 'Agosto', '2026-08', '2026-08-01', false);
INSERT INTO public.bi_dim_tempo VALUES (123, '2026-08-31', 2026, 8, 31, 'Segunda-feira', 0, 3, 2, 36, 'Agosto', '2026-08', '2026-08-01', true);
INSERT INTO public.bi_dim_tempo VALUES (124, '2026-09-01', 2026, 9, 1, 'Terca-feira', 1, 3, 2, 36, 'Setembro', '2026-09', '2026-09-01', true);


--
-- Data for Name: bi_dim_unidade; Type: TABLE DATA; Schema: public; Owner: labvida
--

INSERT INTO public.bi_dim_unidade VALUES (1, 'e0159f3c-8860-4094-9e6f-94e9c948eb32', 'Laboratório Central Garanhuns', 'CENTRAL');
INSERT INTO public.bi_dim_unidade VALUES (2, 'd4abc2a8-ba5a-4cd1-8059-244d8aa3afec', 'Unidade de Coleta Centro', 'COLETA');
INSERT INTO public.bi_dim_unidade VALUES (3, 'fe245ba0-74f0-45ee-b923-ed5529d10cae', 'Unidade de Coleta Heliópolis', 'COLETA');
INSERT INTO public.bi_dim_unidade VALUES (4, '6b49128a-9875-486e-aad3-330f6a5890d6', 'Unidade de Coleta São José', 'COLETA');
INSERT INTO public.bi_dim_unidade VALUES (5, '43fd100f-1325-4563-baff-5cdfa318a3df', 'Unidade de Coleta Boa Vista', 'COLETA');


--
-- Data for Name: bi_etl_execucao; Type: TABLE DATA; Schema: public; Owner: labvida
--

INSERT INTO public.bi_etl_execucao VALUES ('6fb5580f-7036-416a-8a2f-b6ba7549e065', '2026-08-10 20:45:44.085092+00', '2026-08-10 20:45:45.69069+00', 'SUCESSO', 'FULL', '{"fato_glosa": 55, "fato_logistica": 306, "fato_financeiro": 87, "fato_atendimento": 1345, "fato_faturamento": 438, "fato_ordem_servico": 334}', 1.61, NULL);


--
-- Data for Name: bi_fato_atendimento; Type: TABLE DATA; Schema: public; Owner: labvida
--

INSERT INTO public.bi_fato_atendimento VALUES (1, '1d711cee-41df-4883-b253-74dd973bfa0e', 15, 3, 3, 27, 106, 1, 4, 1, 22.47, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (2, 'b0603d8d-a8ed-4f78-8813-6d5b8a7d0ad9', 15, 3, 3, 10, 106, 1, 3, 1, 16.58, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (3, '3d67b201-6d19-41b0-84f9-76b94423395d', 17, 4, 6, 7, 186, 6, 3, 1, 15.68, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (4, '8844dd0a-5e22-421c-974b-b10c640e3a02', 17, 4, 6, 10, 186, 6, 3, 1, 17.36, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (5, 'ce0eae2c-62b1-4b4e-a807-66b1e66320cf', 20, 4, 2, 15, 29, 6, 3, 1, 13.10, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (6, '9a9b07b9-0a63-4b8a-beaf-78b708adf182', 20, 4, 2, 11, 29, 6, 3, 1, 10.67, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (7, 'c51a4ef6-eeed-4caf-90c6-a49bbcca76de', 20, 4, 2, 19, 29, 6, 4, 1, 36.86, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (8, 'bba91106-0f97-4e28-b455-53a66a29b18a', 20, 4, 2, 14, 29, 6, 3, 1, 13.10, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (9, '667eec6a-2b26-4f75-b529-5d2b2d3782ef', 20, 4, 2, 5, 29, 6, 2, 1, 32.98, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (10, '28dab1c6-67fb-433a-aa77-5006682d642d', 20, 4, 2, 25, 29, 6, 4, 1, 25.22, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (11, '6efe82ad-f81a-4a3e-b5ec-e05a2aedc1d2', 20, 4, 5, 5, 45, 6, 2, 1, 32.64, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (12, '5c56f9f4-42cc-4d0c-ad6d-ab2515afe55e', 20, 4, 5, 6, 45, 6, 3, 1, 12.00, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (13, 'a610b1a6-85d0-48cd-a1a9-48f33e176638', 20, 5, 4, 3, 177, 6, 2, 1, 18.26, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (14, '2014fc65-d5e9-475a-9152-394f663108b9', 20, 5, 4, 7, 177, 6, 3, 1, 11.62, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (15, '1d9970fa-da13-4029-8e00-e688ccca2553', 20, 4, 1, 18, 70, 1, 3, 1, 20.52, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (16, 'b6140b97-bc39-48f9-a639-d8460f5a8931', 20, 4, 1, 6, 70, 1, 3, 1, 13.50, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (17, '730ac01e-180e-4351-8110-5a6c89801c56', 20, 4, 1, 24, 70, 1, 4, 1, 51.84, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (18, '0b2935fb-ec3e-4a7f-a912-b49f2a9ac06b', 20, 4, 1, 12, 70, 1, 3, 1, 12.42, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (19, '2691bd66-15dd-471d-80db-eb53f7ece8d2', 17, 4, 5, 16, 14, 6, 3, 1, 16.32, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (20, '024ff50f-18ce-46bd-ac61-32e21cd1c295', 17, 4, 5, 7, 14, 6, 3, 1, 13.44, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (21, '9e8e1193-79f3-44d1-b90b-b10331f16455', 17, 4, 5, 17, 14, 6, 3, 1, 15.84, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (22, 'd280d3b2-ebb3-440e-a204-23f8a6e8850f', 17, 4, 5, 4, 14, 6, 2, 1, 23.04, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (23, '0121698e-339d-4080-8d92-3d81373e7eb9', 17, 4, 2, 10, 88, 6, 3, 1, 15.04, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (24, '19d556b4-e6ed-4a01-a290-082b380a080f', 17, 4, 2, 20, 88, 6, 4, 1, 31.04, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (25, '0031d5ab-5cfa-4c21-9943-3857d79f0b30', 17, 4, 2, 12, 88, 6, 3, 1, 11.16, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (26, '623a8c01-bc09-47d7-ac48-98d8474eea44', 17, 4, 2, 1, 88, 6, 2, 1, 27.64, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (27, 'a951dfc7-d00a-47ae-9ae5-b14b68603863', 17, 4, 2, 2, 88, 6, 2, 1, 14.55, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (28, 'c267a40b-83e1-4f5f-8fce-6ff8698e4f30', 17, 4, 7, 10, 206, 6, 3, 1, 15.34, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (29, '5903eba7-8471-48e2-927a-503b2f7f68d4', 17, 4, 7, 11, 206, 6, 3, 1, 10.89, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (30, '167c2fc2-b301-4ea9-a6ac-b0c29e77fe5e', 17, 4, 7, 17, 206, 6, 3, 1, 16.34, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (31, 'e956b5ff-34cb-4583-8a31-2fd0696f33d1', 17, 4, 7, 21, 206, 6, 4, 1, 29.70, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (32, 'a99a5a4a-7675-4812-855a-fc36d5c372da', 17, 4, 7, 23, 206, 6, 4, 1, 44.55, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (33, '333ae05d-453c-449b-bcab-84e2fb43d88d', 17, 4, 2, 6, 127, 4, 3, 1, 12.12, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (34, '596b7663-6954-4c49-b749-a8a9075fa907', 17, 4, 2, 1, 127, 4, 2, 1, 27.64, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (35, 'd3d67d41-71b8-463c-9886-66cac81ef731', 17, 4, 2, 15, 127, 4, 3, 1, 13.10, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (36, 'efff0a5d-fac7-438a-9314-38d13f6fa811', 17, 4, 2, 29, 127, 4, 6, 1, 50.44, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (37, '493ba161-1ccc-4e88-9012-46bc7bd67957', 17, 4, 6, 17, 186, 6, 3, 1, 18.48, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (38, 'c0ff839b-da40-430a-aba4-2841c23b989f', 17, 4, 6, 22, 186, 6, 4, 1, 69.44, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (39, '279048d8-9956-4a93-b1e2-4515c84b0552', 15, 3, 6, 30, 29, 6, 6, 1, 25.76, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (40, '18bd8574-f5a5-48c1-987b-88fc9e808a3c', 15, 3, 6, 9, 29, 6, 3, 1, 17.92, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (41, 'f3df140a-35de-48fa-afd5-fb8ac5454db7', 15, 3, 8, 28, 16, 4, 5, 1, 21.06, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (42, '7553da81-4bf9-43bb-a9bf-af3f7bef8e3e', 15, 3, 8, 27, 16, 4, 4, 1, 24.57, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (43, '5666d444-3eed-483e-a14e-d133389a6b37', 16, 5, 5, 12, 191, 5, 3, 1, 11.04, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (44, '589880da-e4e4-4c07-b9a8-8b6d9e2add63', 16, 5, 5, 2, 191, 5, 2, 1, 14.40, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (45, 'fc36584e-136c-4a64-86a7-38f44139bde5', 16, 5, 5, 11, 191, 5, 3, 1, 10.56, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (46, '8737cf36-195f-4bff-9191-438c765d9214', 16, 5, 5, 4, 191, 5, 2, 1, 23.04, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (47, '88b70170-8af1-4924-ac3c-5a175303b044', 16, 5, 3, 17, 31, 6, 3, 1, 17.66, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (48, '33dfa65d-4c24-4ebd-afa2-2bf7d1311a52', 16, 5, 3, 12, 31, 6, 3, 1, 12.30, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (49, '122219e7-6bca-49d0-81eb-be6a8cd4a010', 16, 5, 3, 21, 31, 6, 4, 1, 32.10, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (50, '61d7f03f-3db2-4a53-90ca-bb6a5ef2bfc0', 20, 5, 2, 14, 202, 4, 3, 1, 13.10, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (51, 'b7749cc1-9a92-492b-b676-6e91d31247b0', 20, 5, 2, 23, 202, 4, 4, 1, 43.65, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (52, 'b2c788df-2fa8-4b58-8d08-7d98127fdd69', 20, 5, 2, 29, 202, 4, 6, 1, 50.44, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (53, '04596af7-8633-45d2-975f-adefa24b0a81', 20, 5, 2, 22, 202, 4, 4, 1, 60.14, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (54, 'e21b0e14-74c4-4235-ac9c-2a730ed0eefb', 20, 5, 2, 12, 202, 4, 3, 1, 11.16, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (55, '3d542425-c47b-4978-8b01-ad864bbe3dc3', 20, 3, 3, 26, 41, 6, 4, 1, 44.94, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (56, '74fb25f1-530b-4329-9409-a8f8389b409c', 20, 3, 3, 23, 41, 6, 4, 1, 48.15, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (57, '61c4f9b7-f8de-4094-8cbb-583ee3c1212d', 20, 3, 3, 17, 41, 6, 3, 1, 17.66, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (58, '448492b1-1482-4d9f-b6df-579cd8382e05', 20, 3, 3, 20, 41, 6, 4, 1, 34.24, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (59, '6de10a2a-d21b-494f-9982-94ca64bc0cd5', 20, 3, 3, 19, 41, 6, 4, 1, 40.66, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (60, 'd25ac51b-728a-4efb-9a21-5ff08f33f3fa', 20, 5, 4, 17, 177, 6, 3, 1, 13.70, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (61, '2fb7a076-66f1-4c15-b386-f3577d986b44', 20, 5, 4, 22, 177, 6, 4, 1, 51.46, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (62, '85fa454b-d4fa-44d4-83a7-8c70c5c3bd28', 20, 5, 4, 2, 177, 6, 2, 1, 12.45, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (63, '5c06bf69-96f3-48d3-a7c2-c3ecb9fcd5f7', 20, 5, 4, 4, 177, 6, 2, 1, 19.92, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (64, '00bcf38e-a65c-401c-ab16-27d20c85ca0e', 21, 5, 5, 16, 159, 1, 3, 1, 16.32, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (65, 'ba068887-4a1b-47ab-9def-c845d32ebd37', 21, 5, 5, 6, 159, 1, 3, 1, 12.00, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (66, '9c9159c9-6d06-40df-8a28-7e499d6ca289', 21, 5, 5, 5, 159, 1, 2, 1, 32.64, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (67, '3a399d57-9b20-4c65-9020-21c9c69f4b6e', 21, 5, 1, 14, 96, 5, 3, 1, 14.58, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (68, '45e5b49d-072a-449e-89c4-28bbf16ac1b9', 21, 5, 1, 21, 96, 5, 4, 1, 32.40, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (69, '436915e8-e311-4b41-8b6a-ad2d7e5a5064', 25, 5, 8, 21, 128, 4, 4, 1, 35.10, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (70, '6b783b93-8fe3-43d0-8c10-232525e9c5e2', 25, 5, 8, 16, 128, 4, 3, 1, 19.89, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (71, '4a00b800-a680-4b54-8ec0-78896d70da5e', 25, 5, 8, 12, 128, 4, 3, 1, 13.46, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (72, '29e98c03-d010-4e1a-9386-14bd4900f7d2', 25, 5, 8, 17, 128, 4, 3, 1, 19.30, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (73, 'f73c6d7d-4dfd-4586-93d3-020f844adb6f', 25, 5, 8, 6, 128, 4, 3, 1, 14.62, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (74, 'f68f6b4f-6329-4a6c-a3b8-921adb478440', 26, 5, 1, 3, 200, 6, 2, 1, 23.76, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (75, '5de2128e-307f-4524-99d2-e965de5669e1', 26, 5, 1, 13, 200, 6, 3, 1, 14.04, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (76, '3844e3fb-a696-4bd4-883a-60f59a0babc2', 26, 5, 1, 27, 200, 6, 4, 1, 22.68, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (77, 'e9e00ee3-bd3e-4eff-b7b7-ab308f7f797f', 26, 5, 1, 2, 200, 6, 2, 1, 16.20, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (78, '0bcb69b8-5eec-4418-941f-937a08845035', 26, 5, 3, 23, 88, 6, 4, 1, 48.15, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (79, '7e080a1b-c942-40de-a219-961f6ae02d1f', 26, 5, 3, 22, 88, 6, 4, 1, 66.34, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (80, '5d345ba8-9ecb-4a7a-91af-7d9c53b139d7', 26, 5, 3, 11, 88, 6, 3, 1, 11.77, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (81, '2b65a841-243d-436d-a8a7-42318c5c9ef2', 20, 5, 6, 11, 170, 2, 3, 1, 12.32, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (82, 'f38c37e4-ebb7-4162-aad8-2ea9996b0e07', 20, 5, 6, 17, 170, 2, 3, 1, 18.48, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (83, '64d377f0-9109-4835-99a0-01b8e5f5e982', 20, 5, 6, 12, 170, 2, 3, 1, 12.88, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (84, 'a588949a-e58b-4e60-8aed-ffc0ff57ed36', 20, 5, 6, 14, 170, 2, 3, 1, 15.12, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (85, '3b8cdea3-c404-4309-9aca-40efce6be8cd', 20, 5, 7, 1, 120, 2, 2, 1, 28.22, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (86, '199a912a-b4a6-465f-b2aa-48b2b4c29532', 20, 5, 7, 7, 120, 2, 3, 1, 13.86, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (87, 'fd0f5789-e488-4cf4-b905-2584083523db', 20, 5, 4, 2, 152, 6, 2, 1, 12.45, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (88, 'b1d09740-260d-40e2-848a-02b34521aec1', 20, 5, 4, 27, 152, 6, 4, 1, 17.43, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (89, '5ec32080-1e90-4faf-9a50-d8293b25bb9a', 20, 5, 4, 17, 152, 6, 3, 1, 13.70, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (90, '8ac4d4a5-caff-49a2-b04d-2e79555e71b0', 20, 5, 4, 24, 152, 6, 4, 1, 39.84, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (91, '066902ea-2f90-4643-a8c3-4096df37a20a', 21, 5, 5, 19, 159, 1, 4, 1, 36.48, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (92, '15b8342d-1e51-4f62-96ff-ab209268205c', 21, 5, 5, 27, 159, 1, 4, 1, 20.16, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (93, 'feb37a59-2bec-464b-883b-82136fcd3c76', 21, 5, 5, 28, 159, 1, 5, 1, 17.28, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (94, '22702b49-4bd2-40ec-b769-bfab5b0cf28f', 21, 5, 4, 21, 109, 6, 4, 1, 24.90, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (95, '80b87193-bfea-4ee6-a4f5-cc60cdb61ca1', 21, 5, 4, 4, 109, 6, 2, 1, 19.92, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (96, '23f09147-fd3a-44ce-a335-8644194843db', 21, 5, 4, 11, 109, 6, 3, 1, 9.13, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (97, 'e019e4f0-9e8d-4d52-a12a-422fa4c8f2cc', 21, 5, 4, 2, 109, 6, 2, 1, 12.45, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (98, '14cfbe72-e408-47bb-8565-ac6aae49e8c5', 21, 5, 1, 15, 209, 3, 3, 1, 14.58, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (99, 'd5999931-9444-4b61-ab94-639297381e73', 21, 5, 1, 19, 209, 3, 4, 1, 41.04, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (100, 'c7e010b8-ee54-4c0b-9ddf-0a9e7eb2fdf2', 27, 4, 2, 12, 199, 5, 3, 1, 11.16, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (101, 'c7e14704-38da-402f-af2e-10943440374f', 27, 4, 2, 17, 199, 5, 3, 1, 16.00, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (102, '94a0936c-7f8c-49db-89f6-ed07b3ea8611', 27, 4, 2, 2, 199, 5, 2, 1, 14.55, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (103, '5d9b3f41-f10d-4195-8bf2-f2820e9fa05a', 27, 4, 2, 15, 164, 6, 3, 1, 13.10, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (104, '1cd53880-0d54-4e7e-8d3f-1067768badfd', 27, 4, 2, 8, 164, 6, 3, 1, 15.52, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (105, 'e8e81e21-4282-448e-9552-184698fea5c7', 27, 4, 2, 22, 164, 6, 4, 1, 60.14, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (106, 'bb8df438-bcd8-496a-ac31-e90bd1f1c94b', 25, 5, 2, 16, 17, 6, 3, 1, 16.49, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (107, 'f50c2db2-e22b-49fe-8770-f454ceaadbc8', 25, 5, 2, 8, 17, 6, 3, 1, 15.52, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (108, '4fff9af5-2e52-466c-871e-ebc0d1728b13', 25, 5, 2, 18, 17, 6, 3, 1, 18.43, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (109, '8a73a920-a49b-4290-be8c-8d73bd87dd30', 25, 5, 7, 5, 103, 4, 2, 1, 33.66, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (110, 'a0ca9828-f8ff-4d53-bba8-864ea36fbe92', 25, 5, 7, 8, 103, 4, 3, 1, 15.84, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (111, '8e7daf09-0e10-4d6e-92e5-4edf41e4de53', 25, 5, 7, 26, 103, 4, 4, 1, 41.58, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (112, 'c761b511-7bf7-4458-8d2d-ebe1e627fb81', 25, 5, 4, 15, 58, 6, 3, 1, 11.20, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (113, '90bacaa7-3009-44ef-ac6f-5f3a0d9efccd', 25, 5, 4, 14, 58, 6, 3, 1, 11.20, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (114, '6957300c-6381-4c22-9193-d5868c8d26ae', 27, 5, 7, 7, 165, 6, 3, 1, 13.86, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (115, 'a8dbcf7d-37af-41c5-a571-54a11184d83a', 27, 5, 7, 3, 165, 6, 2, 1, 21.78, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (116, '33375140-ec01-490f-9a8a-50b6f2291219', 27, 5, 7, 27, 165, 6, 4, 1, 20.79, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (117, '69ca321b-57a8-4b04-8118-d1ef16741dd0', 27, 5, 7, 9, 2, 4, 3, 1, 15.84, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (118, '6a1cdf3a-bc88-4259-9f8a-51d0fdb339b8', 27, 5, 7, 11, 2, 4, 3, 1, 10.89, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (119, 'd1811954-b5c7-4d55-8fb8-9f7960c234b4', 30, 2, 4, 10, 16, 4, 3, 1, 12.86, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (120, '28734863-0111-4255-b6d3-6b1c9aa8280b', 30, 2, 4, 24, 16, 4, 4, 1, 39.84, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (121, '8b455c6b-ce54-4267-98cb-96a37fe4a3c3', 30, 2, 4, 30, 16, 4, 6, 1, 19.09, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (122, 'fe6239e9-7d0b-4f30-b560-ce11e1f226cc', 30, 2, 4, 11, 16, 4, 3, 1, 9.13, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (123, 'e27ae338-8216-4692-8f61-62dee4bd11fe', 30, 2, 8, 25, 216, 3, 4, 1, 30.42, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (124, 'cae0c831-f109-4680-b661-3cf3520bb49c', 30, 2, 8, 22, 216, 3, 4, 1, 72.54, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (125, '37c861a8-0b9c-490b-b823-1160952f273d', 30, 2, 8, 29, 216, 3, 6, 1, 60.84, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (126, '77b240cd-de68-4660-a148-a1c6c5f32c7a', 32, 4, 5, 6, 141, 3, 3, 1, 12.00, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (127, '27f330ab-5f4d-4060-b3f2-c10ce9e5e591', 32, 4, 5, 4, 141, 3, 2, 1, 23.04, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (128, '72d732fa-8e87-4639-88aa-5cc4872a4692', 32, 4, 5, 19, 141, 3, 4, 1, 36.48, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (129, '77758b90-f08b-49c2-b864-6d5941376bea', 28, 2, 4, 14, 164, 6, 3, 1, 11.20, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (130, 'ac5d1ee4-1f60-4d91-b7ce-8f45231767b6', 28, 2, 4, 19, 164, 6, 4, 1, 31.54, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (131, '51174217-987c-4bae-b4e3-86d76ac6be12', 28, 2, 4, 24, 164, 6, 4, 1, 39.84, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (132, 'c0998c6b-a047-4339-a945-dd81c1c30bb4', 28, 2, 4, 15, 164, 6, 3, 1, 11.20, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (133, '6db0e5a4-d0dc-4bc6-9bbf-9ef2a9cc94d4', 28, 2, 6, 25, 213, 5, 4, 1, 29.12, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (134, '38d579eb-24f2-47a4-9376-4fa5d38691de', 28, 2, 6, 13, 213, 5, 3, 1, 14.56, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (135, 'f887e7ec-2bf5-4459-9035-e26d6ea81bb0', 28, 2, 6, 2, 213, 5, 2, 1, 16.80, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (136, '4d64ae44-643a-4ac5-8b2b-bbf34ed367dc', 28, 2, 6, 1, 213, 5, 2, 1, 31.92, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (137, '60dff5d4-2dc8-42b5-8975-1a27bf782a1b', 28, 2, 6, 19, 213, 5, 4, 1, 42.56, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (138, 'e064b778-26c9-44e1-908d-eafddeb5adf9', 28, 2, 3, 12, 110, 6, 3, 1, 12.30, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (139, '4e834a0f-df70-4184-9637-7b2d2bcee45f', 28, 2, 3, 9, 110, 6, 3, 1, 17.12, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (140, 'c4f27e8a-e0f2-4b44-98d0-d183f8fb0855', 28, 2, 3, 25, 156, 5, 4, 1, 27.82, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (141, '670fef2b-3af9-4cc7-9363-066fa44dc111', 28, 2, 3, 30, 156, 5, 6, 1, 24.61, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (142, '609425c9-e200-4957-a243-f55c712fd812', 28, 2, 3, 27, 156, 5, 4, 1, 22.47, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (143, 'd2d2bf44-de3a-43bb-bd76-a88da6e06ee5', 28, 2, 3, 3, 156, 5, 2, 1, 23.54, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (144, '11adb419-8c49-4d26-81fc-517b4bb0a3ba', 31, 2, 6, 25, 24, 4, 4, 1, 29.12, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (145, 'ae03b32e-af12-4349-9189-6da67dd7952a', 31, 2, 6, 16, 24, 4, 3, 1, 19.04, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (146, 'd055cae0-1883-4d69-9194-2ec3dadc9dee', 30, 5, 5, 8, 10, 5, 3, 1, 15.36, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (147, '946876fe-a0e8-4581-a0e4-de1861437f9c', 30, 5, 5, 6, 10, 5, 3, 1, 12.00, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (148, 'da670540-3ccb-4d01-b950-bb6c8f253c4d', 30, 5, 5, 1, 10, 5, 2, 1, 27.36, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (149, '4916e50d-b351-42c4-b5b0-7dd419d7ff22', 30, 5, 5, 13, 10, 5, 3, 1, 12.48, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (150, '2659dd1c-44e7-46c3-9e4c-b6bb785caa89', 30, 5, 7, 9, 113, 6, 3, 1, 15.84, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (151, '948041e0-ed3e-4273-aac6-29d30a17909a', 30, 5, 7, 15, 113, 6, 3, 1, 13.36, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (152, 'a044c816-9ca3-4bc1-a4b7-ebc23dd506af', 30, 5, 7, 18, 113, 6, 3, 1, 18.81, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (153, 'f465284d-8007-45db-a3db-d90baed6bfc3', 27, 5, 5, 19, 173, 6, 4, 1, 36.48, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (154, '2860ace3-eec6-4a83-b2ec-1dae8a4f58c3', 27, 5, 5, 17, 173, 6, 3, 1, 15.84, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (155, '8088d299-3e6a-4fdb-93da-9896e1350bf4', 27, 5, 5, 9, 173, 6, 3, 1, 15.36, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (156, 'e86b592c-5e70-4749-bf3d-bf131e932f74', 27, 5, 5, 10, 173, 6, 3, 1, 14.88, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (157, 'aa0f20b4-7c5e-476d-a273-27e6597c4d36', 27, 5, 5, 23, 60, 6, 4, 1, 43.20, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (158, 'b33751d0-5cae-4e7e-af33-f3b26745bcc2', 27, 5, 5, 17, 60, 6, 3, 1, 15.84, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (159, '9225843f-eb9e-4895-b1a3-a7f45e1f85ff', 27, 5, 7, 15, 165, 6, 3, 1, 13.36, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (160, 'f251675c-d778-4045-96da-033e017dc84b', 27, 5, 7, 14, 165, 6, 3, 1, 13.36, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (161, '1d1765d9-4631-4e88-a0cd-e92b4625a6c6', 30, 2, 4, 21, 102, 3, 4, 1, 24.90, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (162, 'f4d13425-463c-4e51-abbb-8396d3c66aef', 30, 2, 4, 29, 102, 3, 6, 1, 43.16, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (163, '0c991440-e869-4b01-add4-df7724677a13', 30, 2, 4, 2, 102, 3, 2, 1, 12.45, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (164, '7866d3a6-9257-4e64-a1f2-b9424ca5146e', 30, 2, 4, 9, 102, 3, 3, 1, 13.28, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (165, 'e315820a-8512-49aa-a763-0e376ab97dce', 30, 5, 4, 24, 100, 4, 4, 1, 39.84, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (166, '29b414d5-a929-41b3-8efc-25c7d3b64565', 30, 5, 4, 11, 100, 4, 3, 1, 9.13, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (167, '7393ed1d-cb8c-4ccc-a3d2-1d2cffbd4d91', 32, 4, 8, 20, 107, 4, 4, 1, 37.44, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (168, '3f95b95c-1187-4138-b13a-c2a31c6162f5', 32, 4, 8, 26, 107, 4, 4, 1, 49.14, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (169, '9aeffdb8-b48e-4690-acc4-942876813250', 32, 4, 8, 14, 107, 4, 3, 1, 15.80, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (170, '6494d462-b844-49eb-8e61-6657fc301366', 32, 4, 8, 27, 107, 4, 4, 1, 24.57, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (171, '9a0132cc-faf5-4d6d-9a97-abeb82a72339', 32, 4, 2, 15, 186, 6, 3, 1, 13.10, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (172, 'b11e6a9b-96c2-4bb0-929c-4f3947b4454e', 32, 4, 2, 2, 186, 6, 2, 1, 14.55, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (173, '45329af3-4c0b-4cd8-b68d-448066f63918', 32, 4, 2, 7, 186, 6, 3, 1, 13.58, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (174, 'da182792-ac4f-41e4-9051-50a6f27b91ad', 32, 4, 2, 30, 186, 6, 6, 1, 22.31, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (175, '17137c0f-a3e3-4e05-ae27-8806d12f149c', 31, 2, 6, 13, 71, 3, 3, 1, 14.56, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (176, '8eb75072-649a-4f75-b41b-159b02f854bd', 31, 2, 6, 11, 71, 3, 3, 1, 12.32, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (177, '5654d2a4-5c69-4e57-bf3b-724a5838e28e', 31, 2, 6, 28, 71, 3, 5, 1, 20.16, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (178, 'a071c1e7-18fd-49a7-845b-b40924908421', 31, 2, 6, 10, 71, 3, 3, 1, 17.36, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (179, '13dd5f42-7818-46f7-89fa-9b2e19297cf0', 33, 5, 1, 12, 218, 6, 3, 1, 12.42, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (180, '1c1854ea-4616-4d78-96d9-64e2c14149b3', 33, 5, 1, 18, 218, 6, 3, 1, 20.52, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (181, 'b503a08b-41d2-40f1-88e9-541e56e3200a', 33, 5, 1, 10, 218, 6, 3, 1, 16.74, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (182, 'e1a7a793-e468-4b52-8c2c-681725f2d099', 33, 5, 4, 7, 54, 3, 3, 1, 11.62, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (183, '7edc09dd-5782-4e4d-b397-bee1b81184e3', 33, 5, 4, 19, 54, 3, 4, 1, 31.54, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (184, 'e43e9462-2c39-406a-82c3-204004cb18b9', 33, 5, 4, 21, 54, 3, 4, 1, 24.90, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (185, '9c5d9e25-6e9a-412e-bf8a-ad21fceba930', 33, 5, 4, 13, 54, 3, 3, 1, 10.79, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (186, '8e7be99d-f5c5-4b4b-824d-e59421b4089f', 33, 5, 4, 14, 54, 3, 3, 1, 11.20, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (187, '59c5eddb-7d85-475b-b13f-8cb221bf3410', 34, 4, 6, 26, 147, 6, 4, 1, 47.04, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (188, '66dd6ecf-5f51-4e2d-b900-eb44aca11dd4', 34, 4, 6, 10, 147, 6, 3, 1, 17.36, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (189, 'e408bd5e-4d92-43e7-accc-6c260ecbd695', 34, 4, 6, 17, 147, 6, 3, 1, 18.48, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (190, '6f922785-fe98-4014-8be2-9afe6336a565', 37, 3, 5, 15, 18, 5, 3, 1, 12.96, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (191, '43b59c1e-4f9b-40d3-b441-6f7e601b7c01', 37, 3, 5, 6, 18, 5, 3, 1, 12.00, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (192, '6458c3e9-8fc0-4fcb-a92c-fe653fda6597', 37, 3, 3, 17, 13, 1, 3, 1, 17.66, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (193, '52e54760-62ee-43cb-ae6e-9089f77dffc4', 37, 3, 3, 28, 13, 1, 5, 1, 19.26, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (194, '75f0db7a-3739-4ef6-ab58-22455a4dd25c', 37, 3, 8, 4, 214, 2, 2, 1, 28.08, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (195, 'b513e919-d004-490f-8766-ed7ff84bacda', 37, 3, 8, 17, 214, 2, 3, 1, 19.30, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (196, 'c71ba586-cda2-4e72-9473-30d84dd17705', 37, 3, 8, 26, 214, 2, 4, 1, 49.14, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (197, '3a8d2fe2-b298-4e12-98cf-073cf9a0f681', 37, 3, 8, 5, 214, 2, 2, 1, 39.78, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (198, '694edf97-b2fc-46f8-a568-0a883db9fb2a', 37, 3, 8, 6, 214, 2, 3, 1, 14.62, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (199, '253869c3-0009-458c-8e08-27549849b733', 38, 2, 7, 3, 141, 3, 2, 1, 21.78, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (200, '89e5ffff-757e-4072-8649-1dc7725a62ed', 38, 2, 7, 9, 141, 3, 3, 1, 15.84, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (201, 'dadfb616-544c-4c0b-8c20-3d0e839a1c30', 37, 3, 6, 21, 63, 4, 4, 1, 33.60, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (202, 'bf7414f9-3ef3-47d4-b92b-04d8a67bc575', 37, 3, 6, 1, 63, 4, 2, 1, 31.92, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (203, 'c2f1f54c-fe60-46cc-b0e6-0a049a3b7fb1', 37, 3, 6, 11, 63, 4, 3, 1, 12.32, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (204, '59e59949-ca7b-4db6-b05b-e626f8891ed3', 37, 3, 6, 24, 63, 4, 4, 1, 53.76, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (205, '02fb19bf-de34-4649-b2f2-e26531c6dc88', 37, 3, 5, 20, 18, 5, 4, 1, 30.72, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (206, '7a7686d7-1d9c-45f6-853d-34c3c74a084a', 37, 3, 5, 29, 18, 5, 6, 1, 49.92, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (207, '51b16bf3-1c9f-4e74-be3e-76bfb64ab5df', 37, 3, 7, 30, 108, 6, 6, 1, 22.77, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (208, '55149073-8c7b-4318-b2b8-d28c3fcfcaf4', 37, 3, 7, 12, 108, 6, 3, 1, 11.38, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (209, '563f378a-32f6-4eb4-8938-1cd3800cb998', 37, 3, 7, 14, 108, 6, 3, 1, 13.36, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (210, '55add3b3-08bd-46b7-b54d-3f65ae038ee1', 37, 3, 7, 16, 108, 6, 3, 1, 16.83, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (211, '87c76260-6459-48de-95b4-c01e002325b0', 37, 3, 7, 21, 108, 6, 4, 1, 29.70, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (212, 'e105e28e-50e9-4f97-9213-d3abf8e57c55', 37, 3, 8, 14, 212, 4, 3, 1, 15.80, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (213, '5bd0b492-5bca-46b1-b487-c52fcbbf4724', 37, 3, 8, 13, 212, 4, 3, 1, 15.21, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (214, '9442fb04-6bcd-48dd-8c96-fe1ca0e24228', 37, 3, 8, 18, 212, 4, 3, 1, 22.23, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (215, 'fd475733-aba2-4824-8939-8fe078cc2467', 37, 3, 8, 25, 212, 4, 4, 1, 30.42, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (216, '3646b669-d8dd-4563-bbe3-94d8312beae5', 37, 3, 3, 24, 76, 2, 4, 1, 51.36, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (217, 'e0930765-0354-496b-ab41-65eeca127daf', 37, 3, 3, 23, 76, 2, 4, 1, 48.15, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (218, '4d9e531d-5bea-4a70-ab81-769296276a80', 37, 3, 3, 10, 76, 2, 3, 1, 16.58, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (219, 'dc555881-d0fc-4563-b8df-b86387ef0c1a', 37, 3, 3, 1, 76, 2, 2, 1, 30.50, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (220, '2b9f565a-df83-4505-953c-fca69966b10a', 37, 3, 3, 30, 76, 2, 6, 1, 24.61, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (221, 'c44cc4ab-c13f-43ed-a413-006b071bc4c7', 37, 3, 4, 27, 54, 3, 4, 1, 17.43, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (222, '85ea6131-5d5f-4a27-9e7d-775ea07bd343', 37, 3, 4, 9, 54, 3, 3, 1, 13.28, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (223, '403bb14a-7889-4a62-a547-d80e290e1056', 37, 3, 4, 12, 54, 3, 3, 1, 9.54, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (224, '8f9e3484-a045-4799-a4fe-1cd8e1aeb053', 37, 3, 4, 11, 54, 3, 3, 1, 9.13, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (225, 'ac1d39b7-f267-4cac-933e-cb05102f2a36', 38, 2, 1, 15, 185, 1, 3, 1, 14.58, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (226, '6e9e6baa-cd3b-427e-886c-853c3698915e', 38, 2, 1, 11, 185, 1, 3, 1, 11.88, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (227, '88979bf7-4c4c-4cf9-b887-2ed33d121191', 38, 2, 1, 17, 185, 1, 3, 1, 17.82, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (228, '047f7895-f0a7-4ae3-88f1-dd520c460762', 38, 2, 1, 5, 185, 1, 2, 1, 36.72, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (229, '170af931-41df-4b1a-9eba-135f44364a3b', 33, 5, 7, 4, 143, 6, 2, 1, 23.76, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (230, '2076e152-2156-4461-9fb0-25587d93ab6d', 33, 5, 7, 16, 143, 6, 3, 1, 16.83, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (231, '713ced76-7448-4074-8633-8ba1cde43435', 33, 5, 7, 25, 143, 6, 4, 1, 25.74, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (232, 'e0cdd176-f0be-44a8-9b33-34d681e60e96', 34, 4, 8, 7, 145, 3, 3, 1, 16.38, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (233, '4818d46d-a490-46e5-9395-f628a161c54b', 34, 4, 8, 24, 145, 3, 4, 1, 56.16, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (234, '87bc0754-160c-4efb-a29e-9811fdb096af', 34, 4, 8, 13, 145, 3, 3, 1, 15.21, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (235, '1917d58d-269b-48b3-9b2c-1f58e7650ac6', 34, 4, 8, 11, 145, 3, 3, 1, 12.87, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (236, '0de339b2-88c4-4fa9-b34c-25cbbe6877f0', 39, 3, 4, 28, 177, 6, 5, 1, 14.94, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (237, '635d3e11-d5f0-4e1a-a32e-e3568d1de73c', 39, 3, 4, 11, 177, 6, 3, 1, 9.13, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (238, 'db68cf3c-9f8d-4a20-ab77-ff7541e2ec66', 39, 3, 6, 26, 203, 4, 4, 1, 47.04, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (239, 'd33a3d98-4f92-48bd-8c07-77a678b0819c', 42, 2, 4, 7, 53, 4, 3, 1, 11.62, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (240, 'a47a5acd-f3a9-4af4-bfc9-b98ea13b462c', 42, 2, 4, 17, 53, 4, 3, 1, 13.70, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (241, '93861f2f-4e02-46b4-9106-ed7234f5b840', 42, 2, 3, 20, 123, 4, 4, 1, 34.24, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (242, '8ee1a493-3035-45ad-ba71-7d29047544d8', 42, 2, 3, 18, 123, 4, 3, 1, 20.33, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (243, '75b61643-3a0c-4a59-9c07-a71f7f03a871', 42, 2, 3, 14, 123, 4, 3, 1, 14.44, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (244, '8def4ca9-b603-4ccc-852a-144af197d22d', 42, 2, 3, 30, 123, 4, 6, 1, 24.61, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (245, '57092065-2f39-49a7-b111-9de98253abb1', 42, 2, 3, 28, 123, 4, 5, 1, 19.26, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (246, 'db0008ce-327a-4cb3-9f21-59a90b62f9a2', 42, 2, 5, 29, 29, 6, 6, 1, 49.92, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (247, '91e4b338-3982-451d-a824-b9e59c4640f7', 42, 2, 5, 9, 29, 6, 3, 1, 15.36, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (248, '602d65ee-ef3f-4a97-a0bb-6818f4089cfd', 44, 5, 1, 27, 184, 1, 4, 1, 22.68, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (249, '604bd662-1ee3-4a7a-ad71-cd9402fa2687', 44, 5, 1, 17, 184, 1, 3, 1, 17.82, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (250, '734bf69f-0ef4-4463-871e-d5f282b1bc59', 44, 5, 2, 26, 113, 6, 4, 1, 40.74, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (251, 'c64661ea-1dae-400e-9f52-33c1c81deb77', 44, 5, 2, 22, 113, 6, 4, 1, 60.14, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (252, '92f42f4e-3e7f-4520-9f32-419c976fd5ff', 44, 5, 2, 20, 113, 6, 4, 1, 31.04, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (253, '99259fd8-bd69-409a-9a39-69e8fd495707', 44, 5, 2, 25, 113, 6, 4, 1, 25.22, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (254, '8a00d720-1e80-43b8-83ab-25bbe359c913', 44, 5, 5, 28, 83, 6, 5, 1, 17.28, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (255, '784edf11-3d76-4a1a-9e7c-088a6a3c43d2', 44, 5, 5, 26, 83, 6, 4, 1, 40.32, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (256, 'f56a9e78-6458-4451-89e6-bf6b4bed306a', 44, 5, 5, 22, 83, 6, 4, 1, 59.52, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (257, 'd86a44d2-270e-4e0c-852e-c66eca1d99c8', 45, 2, 6, 22, 180, 1, 4, 1, 69.44, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (258, '522ff05f-8a6e-499b-8e06-f84f311e4883', 45, 2, 6, 6, 180, 1, 3, 1, 14.00, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (259, '1580a540-a16d-4340-8189-efebc3fe4cfe', 45, 2, 6, 7, 180, 1, 3, 1, 15.68, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (260, '322ae6c7-13df-4c9f-853c-3354e6f1f4af', 45, 2, 6, 29, 180, 1, 6, 1, 58.24, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (261, '07eb1a98-a365-4eb4-a6ab-c53318e60f68', 45, 2, 6, 13, 180, 1, 3, 1, 14.56, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (262, 'c5defe9e-6792-4fe3-a5e6-986ee3fd8dac', 45, 2, 6, 9, 180, 1, 3, 1, 17.92, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (263, 'e13552b0-ac4d-42d9-8266-18ed41cba926', 46, 2, 7, 3, 109, 6, 2, 1, 21.78, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (264, '2d55966c-f71f-43b8-aef4-1ee5870b6007', 46, 2, 7, 10, 109, 6, 3, 1, 15.34, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (265, 'f6c8b35a-84c1-41d0-941f-10b5b4fc0bd4', 46, 2, 7, 27, 109, 6, 4, 1, 20.79, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (266, '4350029e-1e2a-4d13-acaf-6ffde8097211', 46, 2, 7, 8, 109, 6, 3, 1, 15.84, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (267, '1870858d-e777-4ea8-96bf-79aaa95bbcfd', 46, 2, 7, 28, 109, 6, 5, 1, 17.82, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (268, 'f3cb09d4-f31a-4be7-b1ae-431d1e732066', 42, 2, 7, 10, 95, 6, 3, 1, 15.34, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (269, '2ab5b95b-2cb6-455e-aa12-1838a3816969', 42, 2, 7, 25, 95, 6, 4, 1, 25.74, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (270, '181f696c-085c-476d-8d3f-d0d17805fb22', 42, 2, 7, 3, 95, 6, 2, 1, 21.78, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (271, 'c273f1b8-91e7-401f-81e9-e61b0d2abb56', 42, 2, 7, 1, 95, 6, 2, 1, 28.22, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (272, '2b13283f-1da4-4c98-8c64-76dd48ad3e2b', 42, 2, 7, 13, 118, 4, 3, 1, 12.87, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (273, 'a388fd1a-d613-4c6c-aa3e-2baad2898f3f', 42, 2, 7, 25, 118, 4, 4, 1, 25.74, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (274, 'fb0a6dc4-73b4-4678-b8b4-2dc01243d355', 42, 2, 7, 4, 118, 4, 2, 1, 23.76, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (275, '9c37ffcc-39a5-48f5-b15e-a52b9fb79523', 42, 2, 7, 17, 118, 4, 3, 1, 16.34, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (276, '622e44b0-8078-4a5f-8bcb-12e1c029de98', 42, 2, 7, 21, 118, 4, 4, 1, 29.70, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (277, 'e41da033-419e-499f-a461-6c1cafed9afb', 42, 2, 4, 5, 53, 4, 2, 1, 28.22, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (278, '1f9beaf7-f69f-4055-9d9f-cca647352136', 42, 2, 4, 29, 53, 4, 6, 1, 43.16, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (279, 'bd11244f-eebf-4a5a-a3f2-cd383bd6042b', 42, 2, 4, 27, 53, 4, 4, 1, 17.43, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (280, '1eba21d2-2380-44d5-b6a8-e5ad615fac3f', 39, 3, 8, 3, 12, 5, 2, 1, 25.74, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (281, 'b1ac58b8-9ade-43ca-939b-1966fb9c0161', 39, 3, 8, 9, 12, 5, 3, 1, 18.72, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (282, '6dbaeaf6-0551-479d-a14e-57c385589004', 39, 3, 8, 20, 12, 5, 4, 1, 37.44, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (283, 'd001585b-3518-4d65-bef1-53d90a28713f', 39, 3, 8, 12, 12, 5, 3, 1, 13.46, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (284, 'e059aead-fa30-4d62-bbe6-2b09f1f8affb', 39, 3, 8, 11, 12, 5, 3, 1, 12.87, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (285, '350d8f4f-066f-4493-900b-c14c3414a116', 39, 3, 2, 19, 197, 6, 4, 1, 36.86, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (286, 'aa4c3cb1-26ce-4fe7-95ea-e71e4d0bdbb5', 39, 3, 2, 10, 197, 6, 3, 1, 15.04, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (287, 'afa1b603-ca62-4a97-a062-b66a461dc17a', 39, 3, 6, 14, 203, 4, 3, 1, 15.12, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (288, '0343be0f-40f0-4857-9223-ac26aed729dd', 39, 3, 6, 22, 203, 4, 4, 1, 69.44, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (289, '42994070-fe0c-446e-808c-19577d7cb98d', 39, 3, 6, 27, 203, 4, 4, 1, 23.52, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (290, '2ff3a210-7416-4319-bbdd-79b7314ce27c', 39, 3, 6, 5, 203, 4, 2, 1, 38.08, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (291, '33317d8e-f2f9-4c43-82d0-fc1da53f1cec', 44, 5, 6, 4, 75, 4, 2, 1, 26.88, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (292, '7667a0fd-75fc-4382-a8ed-ca42d3ab6e85', 44, 5, 6, 16, 75, 4, 3, 1, 19.04, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (293, '492ff363-e498-4a35-be9a-abdb07e26124', 44, 5, 6, 21, 75, 4, 4, 1, 33.60, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (294, '5f229f66-7665-4d3c-bdbe-a84ee02c84f4', 44, 5, 6, 8, 75, 4, 3, 1, 17.92, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (295, '2961b5ed-94a5-486c-941c-83687c5718d4', 44, 5, 6, 11, 75, 4, 3, 1, 12.32, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (296, '785f9b69-293f-4f10-89cd-921dacf7feb8', 46, 2, 5, 10, 54, 3, 3, 1, 14.88, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (297, '17da2cfb-965a-45fb-a0b4-2f1eca839fa2', 46, 2, 5, 18, 54, 3, 3, 1, 18.24, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (298, '8863fc28-cff2-4b55-ab04-8113ec2426dc', 46, 2, 5, 23, 54, 3, 4, 1, 43.20, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (299, '07c1df0b-e500-4bce-99e8-731cc3bde5b4', 46, 2, 5, 13, 54, 3, 3, 1, 12.48, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (300, '7fad7e73-9ad0-4197-a345-c42bdd966c5c', 46, 3, 5, 30, 191, 5, 6, 1, 22.08, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (301, 'e16dc96e-62a1-47be-a771-52b73327a188', 46, 3, 5, 15, 191, 5, 3, 1, 12.96, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (302, '9e622432-6eae-4725-9f48-0404b6de7860', 46, 3, 5, 24, 191, 5, 4, 1, 46.08, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (303, 'ed1a4298-3005-4e18-9402-4f12492b5789', 46, 3, 5, 13, 191, 5, 3, 1, 12.48, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (304, '3ee824d1-634e-4bef-aaa5-b4bd7fdfda31', 46, 3, 5, 20, 191, 5, 4, 1, 30.72, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (305, 'ccc7c6f3-5d47-4b4f-ba94-385570ad420f', 46, 3, 5, 25, 191, 5, 4, 1, 24.96, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (306, '4cc19fcb-2a8f-42a2-abde-a56feec21400', 46, 3, 7, 20, 121, 4, 4, 1, 31.68, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (307, '69a9f6f2-dcb4-4ee4-b7d5-08e8d3c3b63f', 46, 3, 7, 24, 121, 4, 4, 1, 47.52, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (308, '9532a7bc-6550-43f6-acad-26b8836fa4de', 46, 3, 7, 26, 121, 4, 4, 1, 41.58, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (309, '9b3f21ea-fa2f-4ec9-bd00-390eef4491bc', 46, 3, 7, 12, 121, 4, 3, 1, 11.38, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (310, '9f441103-122f-4e2b-9304-e0cb2affc678', 46, 3, 7, 18, 121, 4, 3, 1, 18.81, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (311, 'd47d0b1d-678b-4418-98fc-28e4f878ca17', 48, 4, 1, 20, 99, 3, 4, 1, 34.56, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (312, '40cd39ef-b3b6-49ec-9a39-3bca089ff46f', 48, 4, 1, 27, 99, 3, 4, 1, 22.68, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (313, '30010b0f-ae6f-441d-99ec-ffc45e0a19fc', 48, 4, 1, 14, 99, 3, 3, 1, 14.58, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (314, '23099d3a-3354-4ad4-a37a-f361a8d7ef8a', 48, 4, 5, 15, 25, 1, 3, 1, 12.96, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (315, 'e7a6803b-3f4e-420c-958a-d41e3682930f', 48, 4, 5, 29, 25, 1, 6, 1, 49.92, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (316, 'c80d1173-e12f-4c76-aa2c-201fd147d483', 46, 2, 2, 10, 145, 3, 3, 1, 15.04, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (317, 'b36a4993-9a36-4d7e-a673-3b946d6dc142', 46, 2, 2, 26, 145, 3, 4, 1, 40.74, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (318, '146a34a5-6e2b-453b-b05c-bee4632451aa', 46, 2, 2, 9, 145, 3, 3, 1, 15.52, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (319, '9076f7a4-07d2-4ae6-b575-27b237f0873b', 46, 2, 2, 7, 145, 3, 3, 1, 13.58, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (320, '0ab95fca-5cb8-4ffe-b67d-0f3f8631ff36', 46, 2, 3, 26, 151, 6, 4, 1, 44.94, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (321, 'c3bccb93-5f33-4eb9-9ce1-71886ea12e55', 46, 2, 3, 5, 151, 6, 2, 1, 36.38, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (322, 'c5604814-7c18-491d-aa18-2b899300c432', 46, 2, 3, 15, 151, 6, 3, 1, 14.44, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (323, '2a2ddb5e-87dd-4ab2-aa19-73333d810934', 46, 2, 3, 18, 151, 6, 3, 1, 20.33, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (324, '4e682c2b-cef1-4455-8c4d-f785cda95862', 46, 3, 7, 3, 73, 6, 2, 1, 21.78, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (325, 'd3f03bd5-5624-4943-a06b-36a6097b845e', 46, 3, 7, 18, 73, 6, 3, 1, 18.81, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (326, 'b0dba412-0b6c-423e-b0ae-1108f72a79db', 46, 3, 7, 17, 73, 6, 3, 1, 16.34, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (327, '8d40fc53-5205-4ca8-b89f-d9ff8865ce75', 46, 3, 7, 27, 73, 6, 4, 1, 20.79, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (328, 'cd491dbd-4ca1-4a99-83e0-0df90747c64f', 46, 3, 7, 21, 73, 6, 4, 1, 29.70, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (329, '52d38935-7aeb-473a-933a-fa3735d8bba2', 46, 3, 6, 1, 77, 6, 2, 1, 31.92, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (330, '19ad8b95-b7e9-44ce-97bf-2d7b69f29108', 46, 3, 6, 11, 77, 6, 3, 1, 12.32, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (331, '93ee38ce-9f91-42de-baf0-654c634d7bce', 46, 3, 6, 12, 77, 6, 3, 1, 12.88, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (332, 'a6501a9b-7c97-45d8-8cea-7fbd7c083e29', 48, 4, 7, 13, 165, 6, 3, 1, 12.87, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (333, 'e90c7631-ef48-4e43-8357-0c811dfd6e7a', 48, 4, 7, 14, 165, 6, 3, 1, 13.36, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (334, '35d0dff1-49f4-41ae-b60e-5c39e1db6cc4', 48, 4, 7, 22, 165, 6, 4, 1, 61.38, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (335, '8a8a0522-f6b0-4f5f-86b1-fbebbad986c8', 48, 4, 7, 9, 165, 6, 3, 1, 15.84, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (336, 'b9cdce3b-86e8-4b82-8f74-17f24a2c5982', 48, 4, 7, 16, 165, 6, 3, 1, 16.83, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (337, 'd899a53c-9bcf-45bc-8a63-c038de0f4468', 48, 4, 8, 9, 114, 1, 3, 1, 18.72, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (338, '47369131-e1b6-4afa-bd32-6f37d9c3fa15', 48, 4, 8, 8, 114, 1, 3, 1, 18.72, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (339, '6a1a9200-858c-4645-9faf-36c662835359', 48, 4, 8, 10, 114, 1, 3, 1, 18.14, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (340, '0c7af96e-23b4-4b26-ad2b-4fc8b2891a0f', 48, 4, 8, 16, 114, 1, 3, 1, 19.89, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (341, '2dbb358c-0810-4070-8277-dd8cadc8414d', 48, 4, 5, 4, 25, 1, 2, 1, 23.04, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (342, '73c4d959-78a8-4262-8b8e-d8cc86d140c5', 48, 4, 5, 25, 25, 1, 4, 1, 24.96, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (343, 'e92a599c-c508-4bbc-9ccf-02e34e6df5e0', 48, 4, 5, 16, 25, 1, 3, 1, 16.32, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (344, '3898b9cf-6391-4f43-b282-e106a112483a', 48, 4, 2, 5, 73, 6, 2, 1, 32.98, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (345, 'bbf6c798-e88c-4548-a111-4302918ec7a5', 48, 4, 2, 26, 73, 6, 4, 1, 40.74, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (346, '29a22c3e-e92e-4e8d-8032-a89e7103600d', 48, 4, 2, 15, 73, 6, 3, 1, 13.10, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (347, '0d8fcfa4-5438-4f1f-b6bd-7d96b1ba24af', 46, 5, 1, 26, 205, 4, 4, 1, 45.36, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (348, 'd1eedcb7-5ebd-420d-83ee-9ab8851fbd3a', 46, 5, 1, 3, 205, 4, 2, 1, 23.76, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (349, '6fae9cd2-85cc-470c-be99-0c327abe7e50', 46, 5, 1, 6, 205, 4, 3, 1, 13.50, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (350, '6b85d782-3fbc-491d-bb51-b546246e480d', 46, 5, 1, 11, 205, 4, 3, 1, 11.88, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (351, 'bc4be956-26af-4776-a107-3dff64ef1c59', 50, 5, 4, 12, 61, 1, 3, 1, 9.54, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (352, 'a09851fd-c8fe-425a-b712-37eda491eb4d', 50, 5, 4, 1, 61, 1, 2, 1, 23.66, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (353, 'fe72a7a1-08f5-4782-81dd-63acb1195b72', 46, 2, 5, 26, 54, 3, 4, 1, 40.32, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (354, '7d0ba063-e18e-43d1-a322-dc42b3b94366', 46, 2, 5, 24, 54, 3, 4, 1, 46.08, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (355, '32a79c40-d8b1-4e3d-9ae0-c8bbcba38a1d', 46, 2, 5, 22, 124, 6, 4, 1, 59.52, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (356, '4ce4a4b7-63c6-4d59-adfb-e0c1efadc26e', 46, 2, 5, 7, 124, 6, 3, 1, 13.44, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (357, '58213334-3120-4a5e-9321-bc54573b0358', 46, 2, 5, 6, 124, 6, 3, 1, 12.00, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (358, 'a64bde16-4b33-41fa-b2ad-6f92564319d6', 46, 2, 5, 10, 124, 6, 3, 1, 14.88, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (359, '81f2fd19-7ead-4e60-8628-cb28b71b2784', 46, 2, 5, 27, 124, 6, 4, 1, 20.16, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (360, '7d45574c-d8ff-4093-be98-5c701728adab', 50, 5, 5, 8, 135, 6, 3, 1, 15.36, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (361, '94c463dc-c7aa-4995-93cb-4ca54ef61119', 50, 5, 5, 21, 135, 6, 4, 1, 28.80, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (362, '3c893d57-61f1-421a-b703-74adc7cee6b3', 50, 5, 5, 23, 135, 6, 4, 1, 43.20, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (363, '6e6050f3-0e53-435d-9020-6401327d41a7', 50, 5, 5, 4, 135, 6, 2, 1, 23.04, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (364, 'd7247ba0-7857-471d-a4e0-338bfe4b8aa0', 50, 5, 5, 14, 22, 6, 3, 1, 12.96, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (365, '0f24612d-fd45-4015-8d57-7df942e3b026', 50, 5, 5, 20, 22, 6, 4, 1, 30.72, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (366, 'b3dc7ae2-bb61-4287-904f-670ac849758b', 50, 5, 5, 15, 22, 6, 3, 1, 12.96, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (367, '193f8cf7-3194-4687-817d-4a6e837251de', 50, 5, 5, 17, 22, 6, 3, 1, 15.84, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (368, '3e6ef7a0-05a6-4b54-9c2a-095583f50228', 50, 5, 5, 24, 22, 6, 4, 1, 46.08, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (369, '2e1c9746-1bb3-495f-bbd9-d69a6fed3482', 50, 5, 5, 12, 22, 6, 3, 1, 11.04, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (370, '7eec052e-a259-416c-9235-4f2ead7b4972', 53, 3, 3, 27, 187, 5, 4, 1, 22.47, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (371, '9080cb7f-e4c0-4d66-bdfd-9d375c7650b0', 53, 3, 3, 9, 187, 5, 3, 1, 17.12, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (372, 'e8bc3fcc-bc38-4765-9c9c-3997e18a7419', 53, 3, 3, 12, 187, 5, 3, 1, 12.30, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (373, '5a8b744c-e4b6-43f4-8c42-f2279727ebf5', 53, 3, 3, 8, 187, 5, 3, 1, 17.12, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (374, 'b55c6454-c972-4059-bb3f-ae19b07397f9', 53, 3, 8, 27, 58, 6, 4, 1, 24.57, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (375, '981bf44e-23a4-4536-91c8-d1627f94b6e0', 55, 3, 5, 9, 68, 4, 3, 1, 15.36, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (376, 'cf0c44eb-b2b1-4fc7-a7b2-740d1d7a39f1', 55, 3, 5, 18, 68, 4, 3, 1, 18.24, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (377, '95207111-4a68-4451-bdd3-fe05cd8d8e6a', 55, 3, 5, 5, 68, 4, 2, 1, 32.64, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (378, '10dec814-eda1-472e-901f-ec430a0ec80a', 55, 3, 5, 22, 68, 4, 4, 1, 59.52, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (379, '0d1bdb72-fc57-4606-9ae4-29d5cfbad949', 55, 3, 5, 26, 68, 4, 4, 1, 40.32, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (380, 'ec2f9429-a90d-429e-9291-33298b4c7f41', 55, 3, 2, 10, 95, 6, 3, 1, 15.04, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (381, '9a88a3d3-20db-4c40-9f90-95204348b87f', 55, 3, 2, 25, 95, 6, 4, 1, 25.22, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (382, '73321654-2d8e-474e-8651-a27c049af229', 55, 3, 2, 15, 95, 6, 3, 1, 13.10, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (383, 'de6a0065-1445-4c96-901d-587616420580', 55, 3, 2, 14, 95, 6, 3, 1, 13.10, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (384, '9ea1992c-7454-45a9-a645-70f492b157cc', 55, 3, 2, 17, 95, 6, 3, 1, 16.00, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (385, '440822da-44fd-4b40-a156-9b26f1ae6493', 55, 3, 2, 19, 95, 6, 4, 1, 36.86, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (386, 'b3ba7c98-89e3-4397-83cd-ce7ec87d332e', 55, 5, 1, 11, 73, 6, 3, 1, 11.88, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (387, 'ea974792-6fee-45cd-9f0c-2199a2d4c16c', 55, 5, 1, 2, 73, 6, 2, 1, 16.20, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (388, 'e0931d81-a893-49a2-931a-ba0cf13c02ee', 55, 5, 1, 10, 73, 6, 3, 1, 16.74, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (389, '4b20ef2e-0048-416f-928e-122b78f49b1e', 55, 5, 1, 1, 73, 6, 2, 1, 30.78, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (390, '8eb657bd-ec4f-4594-8816-740ef8c8f492', 55, 5, 1, 13, 73, 6, 3, 1, 14.04, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (391, '5f75a493-b767-4312-a835-5a9c6bf25ba0', 55, 5, 1, 4, 73, 6, 2, 1, 25.92, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (392, '3815f468-c1db-4112-8d12-240883724200', 55, 5, 7, 14, 57, 3, 3, 1, 13.36, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (393, '3aceb105-e088-404b-8ad2-331d9eeddfc4', 55, 5, 7, 28, 57, 3, 5, 1, 17.82, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (394, '5f889008-53f8-49f8-aa29-65f00a5d29b1', 55, 5, 7, 26, 57, 3, 4, 1, 41.58, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (395, 'b2c86e2e-35ce-4475-8fda-5599b2f35df3', 55, 5, 7, 18, 57, 3, 3, 1, 18.81, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (396, 'e24fbd14-c091-4972-b356-74a633328bb3', 50, 5, 3, 22, 130, 6, 4, 1, 66.34, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (397, '98bd9d3f-9922-4970-a7ba-28c3f56a9cb3', 50, 5, 3, 24, 130, 6, 4, 1, 51.36, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (398, 'f29053a1-6123-41dc-aa5f-7f7cac626185', 50, 5, 3, 15, 130, 6, 3, 1, 14.44, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (399, 'abd909b3-b3e6-4a8f-9bc8-f4e036083008', 50, 5, 3, 30, 130, 6, 6, 1, 24.61, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (400, '6e661fc3-336b-4f29-9af7-fdb3d6623682', 50, 5, 5, 24, 77, 6, 4, 1, 46.08, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (401, '383e1c66-236e-4f22-b3fa-f320f93711e4', 50, 5, 5, 3, 77, 6, 2, 1, 21.12, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (402, '89e6da06-ab24-4d8e-a7be-dcf654486c8e', 50, 5, 5, 5, 77, 6, 2, 1, 32.64, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (403, '223cecec-05b1-493b-8951-e369ffcfe73d', 50, 5, 2, 13, 88, 6, 3, 1, 12.61, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (404, '4ad34bbe-9d08-4c43-8253-34b33213c9ef', 50, 5, 2, 30, 88, 6, 6, 1, 22.31, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (405, '0b84ea2b-d6d6-437e-bcae-2418c6c97acf', 50, 5, 2, 27, 88, 6, 4, 1, 20.37, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (406, 'ef56c377-420c-4909-9ae2-aff16e18641f', 50, 5, 2, 24, 88, 6, 4, 1, 46.56, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (407, '1982dad2-356c-4f32-8a6c-6651f8866745', 53, 3, 6, 21, 131, 6, 4, 1, 33.60, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (408, '068e204a-018c-4374-b395-1cab0f0f3a8c', 53, 3, 6, 10, 131, 6, 3, 1, 17.36, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (409, '8aca2a99-d26b-4774-b6fc-3956ebac98c2', 53, 3, 6, 16, 131, 6, 3, 1, 19.04, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (410, 'db9eeff4-544d-440b-96ae-56d0d992d414', 53, 3, 8, 12, 58, 6, 3, 1, 13.46, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (411, 'e2193586-14a6-4986-8078-ed7fa41da87f', 55, 3, 8, 19, 194, 1, 4, 1, 44.46, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (412, '867b8c46-d6e6-4e9d-95ff-7741c5cf20c3', 55, 3, 8, 6, 194, 1, 3, 1, 14.62, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (413, 'cab5fe33-f387-49c1-b541-30b5d72ca96a', 55, 3, 8, 3, 194, 1, 2, 1, 25.74, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (414, '8ea79132-de9d-4961-8332-240d53aaf7ab', 55, 3, 3, 12, 156, 5, 3, 1, 12.30, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (415, '40ecc594-ec7c-4c7c-98a3-6625a0e83fcf', 55, 3, 3, 15, 156, 5, 3, 1, 14.44, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (416, 'a50d7e08-ea16-426b-90be-8141fb3da06a', 55, 3, 2, 17, 139, 5, 3, 1, 16.00, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (417, '960ae0ee-9f1e-40f1-98b7-c9c2f0309175', 55, 3, 2, 6, 139, 5, 3, 1, 12.12, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (418, '8b831eea-d703-4884-b612-494dfa79af22', 55, 3, 2, 8, 139, 5, 3, 1, 15.52, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (419, '738dd612-6e2f-4824-b17f-477db87112a1', 55, 3, 2, 26, 139, 5, 4, 1, 40.74, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (420, 'c16acb3c-b9a8-4348-ab96-6eda5d61007b', 50, 4, 1, 8, 204, 5, 3, 1, 17.28, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (421, '6081a20c-3d92-4e8c-85cf-1c17512e7bc3', 50, 4, 1, 14, 204, 5, 3, 1, 14.58, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (422, '51bc82d7-6238-4c03-95d5-352664bc54f8', 56, 5, 6, 20, 147, 6, 4, 1, 35.84, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (423, '398fc7e1-844f-477f-a5ba-129019b8ad94', 56, 5, 6, 26, 147, 6, 4, 1, 47.04, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (424, '9ae61b25-f28d-483b-b977-638aba2f9e97', 56, 5, 6, 3, 147, 6, 2, 1, 24.64, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (425, 'b031c1ad-a6a4-40e1-b5c1-ffc5f006fdbf', 59, 2, 3, 18, 24, 4, 3, 1, 20.33, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (426, 'b51eeffe-9113-48fb-92c1-f5071818dccc', 59, 2, 3, 11, 24, 4, 3, 1, 11.77, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (427, 'eac9f96c-8e7c-42b9-9826-ff159bc880bb', 60, 4, 6, 22, 83, 6, 4, 1, 69.44, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (428, '979c7917-8dfa-4f80-9a73-a86714f7845a', 60, 4, 6, 1, 83, 6, 2, 1, 31.92, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (429, 'c04b0207-fb76-49f1-909f-2b5abe1dd36b', 60, 4, 6, 21, 83, 6, 4, 1, 33.60, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (430, '62f123bd-19f7-48ee-9eff-665a9225d60a', 60, 4, 6, 28, 83, 6, 5, 1, 20.16, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (431, '0b126729-71d6-4d03-b8ec-8c14fe6907a3', 60, 4, 6, 17, 83, 6, 3, 1, 18.48, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (432, 'cdfecf2e-ee98-46a3-abd2-2e39be96ab58', 60, 4, 3, 4, 117, 4, 2, 1, 25.68, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (433, 'e691d8f5-c2b6-4b3e-bc9e-361c1cc6cfa9', 60, 4, 3, 22, 117, 4, 4, 1, 66.34, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (434, 'a2653ab1-216e-45b2-adb3-d6297dd2e3cc', 60, 4, 3, 26, 117, 4, 4, 1, 44.94, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (435, 'fd024c38-578b-4e90-919d-646aa9e9b3fa', 60, 4, 3, 14, 117, 4, 3, 1, 14.44, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (436, '93a33774-2663-4475-ae81-d93818a3ab3c', 60, 4, 1, 4, 3, 6, 2, 1, 25.92, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (437, '3a37caa2-b372-4f5d-9f28-2ef83d4a43bc', 60, 4, 1, 11, 3, 6, 3, 1, 11.88, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (438, '4e73fa6c-cb69-45c8-8315-7d2936fda80d', 60, 4, 1, 3, 3, 6, 2, 1, 23.76, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (439, '572df856-7bd9-43a2-97df-912c99eda2c7', 60, 4, 1, 27, 3, 6, 4, 1, 22.68, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (440, 'bd960055-f1a8-492c-9cfc-aced259206c4', 60, 4, 1, 20, 3, 6, 4, 1, 34.56, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (441, '4b8a58d2-2ae8-4dbd-8cc5-1a9ccaffe492', 60, 4, 1, 2, 3, 6, 2, 1, 16.20, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (442, 'dcf9e364-719a-4f40-934f-b632bce41ab9', 60, 4, 4, 15, 53, 4, 3, 1, 11.20, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (443, 'f5344481-a4bd-451f-a7a6-4e032c5c031c', 59, 2, 1, 27, 182, 4, 4, 1, 22.68, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (444, 'f20d9c1a-5364-4420-b8ab-f09932739a8d', 59, 2, 1, 18, 182, 4, 3, 1, 20.52, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (445, '6c512600-d02a-4d3c-af0c-154a16957022', 59, 2, 1, 4, 182, 4, 2, 1, 25.92, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (446, '2b4f928c-7c86-434a-b869-85922fc17a11', 57, 3, 6, 18, 73, 6, 3, 1, 21.28, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (447, '64eeaf64-2aff-4443-97c8-5adb1fcb32b9', 57, 3, 6, 24, 73, 6, 4, 1, 53.76, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (448, '9ec11323-a963-4421-9ddf-5b4039a322e3', 57, 3, 6, 15, 73, 6, 3, 1, 15.12, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (449, '8d8863e8-5afe-4b0d-a7ba-304730a953fc', 57, 3, 1, 14, 150, 4, 3, 1, 14.58, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (450, '39652309-9541-4dc0-8ed0-ee24f283074d', 57, 3, 1, 12, 150, 4, 3, 1, 12.42, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (451, '9c1dd4f2-7fe9-49e5-a6de-1cb73df53cb9', 57, 3, 1, 1, 150, 4, 2, 1, 30.78, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (452, 'b388b435-b1f8-477f-8cb0-239034f6c174', 57, 3, 1, 15, 150, 4, 3, 1, 14.58, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (453, 'f4100f07-08f3-430c-a6dc-af39e6cfee4a', 59, 3, 6, 29, 86, 4, 6, 1, 58.24, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (454, '8514fb6b-9cbf-4d8d-8847-e2679a9ba271', 59, 3, 6, 14, 86, 4, 3, 1, 15.12, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (455, 'dff01c19-750e-4450-993c-89f5d7268ab7', 59, 3, 6, 24, 86, 4, 4, 1, 53.76, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (456, '4200d522-5422-4c55-ad04-343c34410c93', 59, 3, 7, 28, 10, 5, 5, 1, 17.82, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (457, 'ef71b9a6-6322-4277-b76e-0de0b3564742', 59, 3, 7, 7, 10, 5, 3, 1, 13.86, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (458, 'ceeff99e-a057-4c3a-af6a-14a67f6985e4', 58, 3, 6, 9, 80, 4, 3, 1, 17.92, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (459, 'c1ea3f8d-ca9d-4928-8415-27ac7d0da48b', 58, 3, 6, 25, 80, 4, 4, 1, 29.12, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (460, 'b02fe0c9-ba08-4215-95bc-40223018d522', 58, 3, 7, 6, 180, 1, 3, 1, 12.38, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (461, '1f027d6c-e4ba-480b-a80f-40264f1dfbeb', 58, 3, 7, 11, 180, 1, 3, 1, 10.89, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (462, '23f36200-0f40-4113-a19f-205db5e3742f', 58, 3, 7, 16, 180, 1, 3, 1, 16.83, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (463, 'b2ee1729-d82d-4abc-912d-de72f56da14f', 60, 4, 6, 10, 179, 4, 3, 1, 17.36, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (464, '9d6e5a31-1aa7-4beb-ab70-4baa11b149c3', 60, 4, 6, 24, 179, 4, 4, 1, 53.76, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (465, 'f96705d8-66f4-4df1-b66b-ba704895706c', 60, 4, 8, 21, 154, 4, 4, 1, 35.10, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (466, 'ea626c34-b4ea-4138-b874-e25e31462574', 60, 4, 8, 16, 154, 4, 3, 1, 19.89, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (467, '70c5faf0-7c17-46d5-b5b4-f030c8ac8789', 60, 4, 8, 5, 154, 4, 2, 1, 39.78, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (468, 'f8293908-43f6-4cb3-a2da-fa96ca0268cb', 57, 5, 3, 1, 151, 6, 2, 1, 30.50, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (469, '1e3000f1-2556-469a-9e35-ce183ab29e6a', 57, 5, 3, 3, 151, 6, 2, 1, 23.54, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (470, '3c8287e2-ddac-49cd-bbe4-cacc6a3d60a3', 57, 5, 3, 30, 151, 6, 6, 1, 24.61, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (471, '5653c22b-f4ee-4074-b62e-6b6936c3d1f5', 57, 5, 3, 13, 151, 6, 3, 1, 13.91, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (472, '0dca7764-89d5-4aea-9f01-1313526bc2dd', 57, 5, 4, 16, 118, 4, 3, 1, 14.11, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (473, '3faef35a-c035-49e0-9ee4-f3541b3c06fd', 57, 5, 4, 18, 118, 4, 3, 1, 15.77, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (474, '4854d976-92ad-4bdb-8e76-3b4ca45ab4d9', 57, 5, 4, 9, 118, 4, 3, 1, 13.28, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (475, '598124d1-c408-4755-a7f7-f8f02f14e5df', 57, 5, 7, 7, 51, 5, 3, 1, 13.86, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (476, 'dac8d829-51b3-4ddc-bdfe-74f81811149c', 57, 5, 7, 28, 51, 5, 5, 1, 17.82, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (477, '9fbcc31c-9d74-41b5-9450-33c4d8b9f8c0', 57, 5, 7, 21, 51, 5, 4, 1, 29.70, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (478, 'a2383dc6-2aef-4867-967a-8fb4cfffd55f', 57, 5, 7, 12, 51, 5, 3, 1, 11.38, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (479, 'a888e696-15ef-43dd-933b-efef189353f9', 59, 2, 8, 22, 171, 1, 4, 1, 72.54, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (480, 'e8d51c0b-f346-4e16-8687-1154fec1c96c', 59, 2, 8, 7, 171, 1, 3, 1, 16.38, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (481, '5a0933e7-ee16-4607-93ca-ab0e2cce7594', 59, 2, 3, 30, 24, 4, 6, 1, 24.61, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (482, '9dc6c761-5c21-4fc3-9ec6-d2b5ab6e665e', 59, 2, 3, 5, 24, 4, 2, 1, 36.38, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (483, '003199e4-bc9c-4b8d-8e01-011160d4c3e9', 60, 4, 4, 5, 53, 4, 2, 1, 28.22, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (484, 'be2e7f31-a5e1-4faa-bb08-ff5997489d3b', 60, 4, 4, 25, 53, 4, 4, 1, 21.58, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (485, 'e2daf0bf-64ac-42fd-9026-b779294165f4', 60, 4, 4, 12, 53, 4, 3, 1, 9.54, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (486, '80732cc5-446f-496a-8037-2d451518961f', 60, 4, 4, 20, 53, 4, 4, 1, 26.56, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (487, '59d7bbab-7544-4ffb-8067-2158688ef890', 62, 3, 3, 1, 127, 4, 2, 1, 30.50, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (488, '285c4134-75dc-4695-a3b6-eab52493eaa7', 62, 3, 3, 12, 127, 4, 3, 1, 12.30, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (489, 'a5d3ec6c-26c6-4afd-9edf-d130ffa00c1e', 62, 3, 3, 29, 127, 4, 6, 1, 55.64, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (490, '106e4289-42cf-4899-ba7b-1e2e15ce6708', 62, 3, 3, 22, 127, 4, 4, 1, 66.34, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (491, '9a44ddb2-d202-4051-856a-35fe2f70f08f', 62, 3, 3, 21, 127, 4, 4, 1, 32.10, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (492, 'a97e49ea-ff1c-4f6e-903b-001b82118c9b', 62, 3, 3, 18, 127, 4, 3, 1, 20.33, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (493, '6866b828-42cd-42c1-bd50-c5223fc70496', 62, 3, 7, 16, 162, 4, 3, 1, 16.83, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (494, 'a172a294-c841-440f-adbc-c9fa3a2a3ec4', 62, 3, 7, 17, 162, 4, 3, 1, 16.34, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (495, '5bf05232-7d97-40a8-8f24-70222b5116bb', 62, 3, 7, 3, 162, 4, 2, 1, 21.78, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (496, 'e1d6b372-a8a7-4fb9-bce7-7ee71e543567', 62, 3, 7, 9, 162, 4, 3, 1, 15.84, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (497, '89bc52aa-892c-4513-ba9d-09e1ee71da23', 62, 3, 7, 12, 162, 4, 3, 1, 11.38, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (498, 'ea2481bd-38f7-4023-ab3d-ea7fa8ecc15d', 62, 3, 7, 5, 162, 4, 2, 1, 33.66, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (499, '6a411067-0341-4e8a-83ae-095312752834', 65, 5, 6, 23, 207, 4, 4, 1, 50.40, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (500, '0e6e3dfe-2f35-4e9b-b1d5-d99519c47781', 65, 5, 6, 15, 207, 4, 3, 1, 15.12, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (501, '0edd047b-e631-4eb4-ae31-60d0531e7ebd', 66, 2, 4, 17, 30, 4, 3, 1, 13.70, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (502, '49652dd4-98e1-493b-80fa-79f06df0d2ac', 66, 2, 4, 7, 30, 4, 3, 1, 11.62, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (503, '3490b11f-544a-4ec4-a9f5-3d8f04957c70', 65, 5, 5, 5, 29, 6, 2, 1, 32.64, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (504, '2746c4b5-2316-4e83-be49-e1b0258af5ff', 65, 5, 5, 27, 29, 6, 4, 1, 20.16, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (505, '0f3f429c-a20b-498e-8bc7-417d3d8cfa82', 65, 5, 2, 18, 181, 4, 3, 1, 18.43, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (506, '59decf22-0fa8-4284-bd94-1a3a2654d774', 65, 5, 2, 9, 181, 4, 3, 1, 15.52, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (507, '19f76e66-ddb7-4af0-83a8-7a5f35e2f2be', 65, 5, 6, 4, 207, 4, 2, 1, 26.88, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (508, 'bccc65db-c4a9-4824-8b62-d286c0f92ee6', 65, 5, 6, 20, 207, 4, 4, 1, 35.84, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (509, 'daebc461-dda6-4e5b-9aad-9166489e8cc4', 65, 5, 6, 1, 207, 4, 2, 1, 31.92, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (510, '2c587e14-6898-448d-8da0-cb37142fe3ac', 62, 3, 5, 25, 157, 6, 4, 1, 24.96, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (511, '943dc884-6fba-4d3f-aec8-084c2d75f5a1', 62, 3, 5, 30, 157, 6, 6, 1, 22.08, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (512, '64267159-f33f-415e-a41d-9caba7306e4e', 62, 3, 5, 22, 157, 6, 4, 1, 59.52, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (513, 'c22cbffa-d5b9-485c-bf3f-21cf331b9100', 62, 3, 5, 15, 157, 6, 3, 1, 12.96, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (514, 'b89aff85-c2fe-4ff8-b32b-f2ee499ee595', 62, 3, 4, 29, 76, 2, 6, 1, 43.16, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (515, 'ad80644c-b67e-4b87-8575-1b3bc496a371', 62, 3, 4, 28, 76, 2, 5, 1, 14.94, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (516, 'e39a899e-9bb4-40fb-831c-58f693347277', 62, 3, 4, 24, 76, 2, 4, 1, 39.84, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (517, '5def27d7-f65b-47fb-87d0-323670c66707', 62, 3, 4, 17, 76, 2, 3, 1, 13.70, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (518, 'c2f94920-9858-4999-9d51-137b3995e954', 69, 5, 6, 29, 60, 6, 6, 1, 58.24, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (519, 'ee129954-1abd-4ab6-a813-7218a98afc88', 69, 3, 4, 5, 9, 5, 2, 1, 28.22, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (520, 'da8ffefc-b13c-4754-ba28-023abe3fdda0', 69, 3, 4, 21, 9, 5, 4, 1, 24.90, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (521, '5744d583-7c17-4495-aed4-b7146d066bfe', 69, 3, 4, 26, 9, 5, 4, 1, 34.86, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (522, '4886a4f3-54a1-481c-8d72-12b8f519c63a', 69, 3, 4, 16, 9, 5, 3, 1, 14.11, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (523, 'b96cd14a-43c1-4f77-a5e0-37c98d54dab8', 69, 3, 4, 30, 9, 5, 6, 1, 19.09, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (524, 'd7f633ac-b1e6-4e22-8349-151b39604fdd', 69, 3, 2, 10, 183, 1, 3, 1, 15.04, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (525, '0a20ef71-0d46-47e2-9f3f-c47fe3e4558b', 69, 3, 2, 22, 183, 1, 4, 1, 60.14, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (526, '0c1cb0fb-228b-47f9-9ea8-023963e1d7f3', 69, 3, 2, 2, 183, 1, 2, 1, 14.55, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (527, 'd93c3f31-66eb-4f96-b16e-e59cfa10523c', 69, 3, 8, 29, 80, 4, 6, 1, 60.84, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (528, 'b92c7066-c314-4db4-9497-8d888f9c4257', 69, 3, 8, 5, 80, 4, 2, 1, 39.78, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (529, '73be0e57-8fbf-4cc9-a7c8-f82364975b71', 69, 3, 8, 7, 80, 4, 3, 1, 16.38, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (530, '6a3c2f37-5110-4883-90e1-61c937f84a94', 69, 3, 8, 27, 80, 4, 4, 1, 24.57, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (531, '670533c5-fedb-45a7-8b83-0a4c8279e35b', 69, 3, 8, 15, 80, 4, 3, 1, 15.80, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (532, 'a83257a6-54a1-4818-915d-c946a3925d3f', 66, 2, 4, 20, 30, 4, 4, 1, 26.56, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (533, '9760a577-a86a-4740-816f-fd32b1d0479f', 66, 2, 4, 1, 30, 4, 2, 1, 23.66, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (534, '9c902124-21f3-4033-948f-8b2c3d2e8e91', 66, 2, 7, 21, 114, 1, 4, 1, 29.70, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (535, '0f59b187-966d-4bb8-abe6-f96b92efc57b', 66, 2, 7, 1, 114, 1, 2, 1, 28.22, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (536, '0213ec46-247a-4418-a221-3566e6d31646', 66, 2, 6, 8, 28, 2, 3, 1, 17.92, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (537, '7478b2a4-ea01-4a36-871a-0a7a1b306e88', 66, 2, 6, 4, 28, 2, 2, 1, 26.88, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (538, '3230ca4c-ed6d-42e7-bac3-b138c14e0939', 66, 2, 6, 29, 28, 2, 6, 1, 58.24, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (539, '39d57672-fdfd-46f7-9777-c37d308359bb', 66, 2, 6, 28, 28, 2, 5, 1, 20.16, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (540, '819adefe-841b-4205-b77d-4d9e1c82f842', 66, 2, 5, 22, 77, 6, 4, 1, 59.52, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (541, 'f2afa623-e10f-47dc-a869-bbd49081a112', 66, 2, 5, 24, 77, 6, 4, 1, 46.08, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (542, '45a6d836-bbd2-447a-8d75-56ed71db30cd', 66, 2, 5, 15, 77, 6, 3, 1, 12.96, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (543, '9c9d1f59-d512-4a44-96e1-6acc0561297f', 66, 2, 5, 13, 77, 6, 3, 1, 12.48, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (544, '3efa0c5b-07a5-401e-8dc9-6fa053eb4c29', 69, 5, 4, 1, 59, 4, 2, 1, 23.66, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (545, '8e12db4d-6676-4220-a799-977c1901991c', 69, 5, 4, 7, 59, 4, 3, 1, 11.62, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (546, 'c79b2286-336f-4f0c-9f07-aa66b4d0a2e6', 69, 5, 4, 2, 59, 4, 2, 1, 12.45, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (547, '021205f7-0b9d-4633-9e01-56e6327a57c5', 69, 5, 4, 17, 59, 4, 3, 1, 13.70, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (548, '81295a3d-0533-411a-b333-4c036b0ad69d', 69, 5, 7, 12, 23, 3, 3, 1, 11.38, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (549, 'eaeddc59-f8c5-4d8f-9e4c-0fcdc27a09fc', 69, 5, 6, 12, 209, 3, 3, 1, 12.88, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (550, '80148ba0-babb-4136-9580-d1638bf2c552', 69, 5, 6, 26, 209, 3, 4, 1, 47.04, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (551, '38ae048f-d9a5-4a10-ae0e-ed387771dfc8', 69, 5, 6, 21, 209, 3, 4, 1, 33.60, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (552, '90582347-0fd1-4459-a88d-1be7896896b1', 69, 5, 6, 22, 209, 3, 4, 1, 69.44, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (553, '881906c4-68b1-41c1-a32e-a746aa73acf6', 69, 5, 6, 6, 209, 3, 3, 1, 14.00, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (554, 'c6b8c63c-4188-4c0a-ac4d-c466102ccea2', 69, 5, 6, 30, 209, 3, 6, 1, 25.76, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (555, 'a830fd10-3e74-4889-aaa1-c38aa3bd2cef', 69, 5, 7, 21, 131, 6, 4, 1, 29.70, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (556, '50a7b9e4-04df-45bc-bde5-5ec14f2aa8b5', 69, 5, 7, 27, 131, 6, 4, 1, 20.79, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (557, '43aaefea-e5c7-4f8e-a28b-88a887737f95', 69, 5, 7, 2, 131, 6, 2, 1, 14.85, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (558, '850a84f7-f0ed-4b66-bd86-1c512d37f2df', 69, 5, 7, 19, 131, 6, 4, 1, 37.62, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (559, 'b7cc5d26-ac7b-4538-86cf-64f84dcee546', 69, 5, 7, 4, 131, 6, 2, 1, 23.76, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (560, '75768926-a520-4435-a11c-2e0010d0a5d0', 69, 5, 7, 29, 131, 6, 6, 1, 51.48, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (561, 'f52d625f-b980-4e6d-acf8-2fc458d86b8b', 69, 5, 1, 15, 173, 6, 3, 1, 14.58, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (562, 'b1cbcab9-31a0-4e84-a5ae-58be932f597e', 69, 5, 1, 9, 173, 6, 3, 1, 17.28, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (563, '694e9d3f-0797-4edf-b9fe-cb57864cb6d1', 69, 5, 2, 3, 83, 6, 2, 1, 21.34, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (564, 'f41f221d-56f2-41e8-b3fe-5cf127abbb8d', 69, 5, 2, 24, 83, 6, 4, 1, 46.56, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (565, '6e0c7aef-2b56-4057-bd06-be882e4930e2', 69, 5, 6, 21, 168, 1, 4, 1, 33.60, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (566, '69cd3cc4-47e4-4863-abee-47c1e5b56fba', 69, 5, 6, 10, 168, 1, 3, 1, 17.36, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (567, 'd36e92a5-b4e1-4f16-aa40-9cc0e4acebcb', 69, 5, 6, 19, 168, 1, 4, 1, 42.56, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (568, 'd3ebb55d-18e9-4bac-b325-8b6e19a2f6e6', 69, 5, 7, 27, 23, 3, 4, 1, 20.79, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (569, 'e497c06f-e72a-4b10-a669-af7b3646ee09', 69, 5, 4, 16, 132, 4, 3, 1, 14.11, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (570, 'cc797f40-fcd4-42cd-a45d-c6f726e42bc6', 69, 5, 4, 11, 132, 4, 3, 1, 9.13, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (571, '15ae3298-cf04-4624-a158-d60317a8efdc', 69, 5, 4, 6, 132, 4, 3, 1, 10.38, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (572, '4ca969cb-39c1-4759-990e-84c36e9591f7', 69, 5, 4, 22, 132, 4, 4, 1, 51.46, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (573, '4ee8bf20-6034-4750-bcd2-a130a6956996', 71, 3, 6, 29, 89, 4, 6, 1, 58.24, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (574, '48bb088a-6b68-4f9a-84b6-70861ad3f6e3', 71, 3, 6, 10, 89, 4, 3, 1, 17.36, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (575, '7223decd-53ec-45f6-94c6-01fcf367fe64', 71, 3, 6, 25, 89, 4, 4, 1, 29.12, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (576, '187570ef-298c-4104-82b7-e84eff9f3e0e', 70, 4, 4, 25, 137, 6, 4, 1, 21.58, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (577, 'd2eafeb4-073b-449b-9222-7fc3aa68e54f', 70, 4, 4, 12, 137, 6, 3, 1, 9.54, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (578, '56e99f3f-d914-48d5-9c47-f5b13a4c32ae', 70, 4, 7, 27, 138, 4, 4, 1, 20.79, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (579, '8d0c9eea-a762-47a0-806c-11a8f6611c21', 70, 4, 7, 24, 138, 4, 4, 1, 47.52, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (580, 'c3664627-04ef-4894-9f33-2c3dc4b3bc8e', 70, 4, 7, 15, 138, 4, 3, 1, 13.36, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (581, '882cc909-ae54-4c10-bb79-b5f8547264ca', 70, 4, 7, 16, 138, 4, 3, 1, 16.83, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (582, '67d3382d-230b-4664-a033-5fe5a2eacb3c', 70, 4, 2, 1, 211, 1, 2, 1, 27.64, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (583, '94c0faca-cb97-4a9e-92d6-dce035b9ed78', 70, 4, 2, 26, 211, 1, 4, 1, 40.74, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (584, 'ddb3b694-55cc-47ee-81f7-1047fe57a101', 70, 4, 2, 30, 211, 1, 6, 1, 22.31, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (585, 'afaf51a5-07e4-47d8-b050-ebbe2a378b4d', 69, 5, 2, 6, 83, 6, 3, 1, 12.12, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (586, '29c1bc34-42ea-4d98-9608-0a643d082c3c', 69, 5, 2, 18, 83, 6, 3, 1, 18.43, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (587, '22ed7194-b83f-481f-bf26-8415f1a0d51d', 69, 5, 2, 17, 83, 6, 3, 1, 16.00, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (588, '603d62fc-d737-4ab4-bd42-09f5517965ec', 69, 5, 6, 14, 39, 4, 3, 1, 15.12, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (589, 'e39a874e-6338-4489-b907-402f6de3f731', 69, 5, 6, 9, 39, 4, 3, 1, 17.92, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (590, 'c8a86302-8494-4fc4-a67e-ce486de312e1', 69, 5, 6, 29, 39, 4, 6, 1, 58.24, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (591, '37e7e535-e7b0-4cf1-97f1-16125c4ff624', 69, 5, 6, 24, 39, 4, 4, 1, 53.76, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (592, '10d891a8-ac0a-4841-9b40-5332fdc49c7f', 69, 5, 1, 7, 173, 6, 3, 1, 15.12, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (593, 'e73734b1-0f3a-458c-956c-ebeccbc5bbbf', 69, 5, 1, 2, 173, 6, 2, 1, 16.20, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (594, 'f31a0517-2774-4a15-83be-5e96fdd1d3dc', 71, 3, 2, 30, 149, 6, 6, 1, 22.31, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (595, '2abc6c47-3376-48f9-b6d4-1c65a5c2c042', 71, 3, 2, 22, 149, 6, 4, 1, 60.14, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (596, 'fc437d12-f1e1-43a9-8920-19c8241f3b01', 71, 3, 2, 4, 149, 6, 2, 1, 23.28, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (597, '3a2d1f75-67fa-4499-b3eb-db75e780c7bd', 70, 4, 8, 30, 136, 4, 6, 1, 26.91, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (598, '77a85ae3-f369-49e5-b4ed-137a43220344', 70, 4, 8, 23, 136, 4, 4, 1, 52.65, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (599, 'cc1d5544-ea41-42d7-ba4d-e6401585101f', 70, 4, 8, 14, 136, 4, 3, 1, 15.80, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (600, 'e64b2255-f35a-4888-b1f5-0864b824fcd6', 70, 4, 8, 28, 136, 4, 5, 1, 21.06, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (601, '84d78950-de40-410c-b5c2-411045cf87b9', 70, 4, 8, 15, 136, 4, 3, 1, 15.80, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (602, '5551fce1-6cca-4745-a2af-6c9ebbbfb1b4', 70, 4, 6, 15, 85, 6, 3, 1, 15.12, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (603, 'cbd6f96d-101e-4cf2-8704-461e8a87df68', 70, 4, 6, 14, 85, 6, 3, 1, 15.12, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (604, '5c989454-827c-45de-858b-059339158362', 71, 4, 7, 4, 123, 4, 2, 1, 23.76, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (605, '516d5a6e-7029-4738-92a4-09940ba0ac16', 71, 4, 7, 17, 123, 4, 3, 1, 16.34, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (606, 'a3674adf-bd1b-44ff-9296-c9c57e089996', 71, 4, 7, 27, 123, 4, 4, 1, 20.79, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (607, '80be0445-4989-4e64-b494-674860bc59b8', 71, 4, 7, 25, 123, 4, 4, 1, 25.74, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (608, 'bb4e37a9-14a0-441f-bf69-f6da9edcad03', 71, 4, 7, 16, 123, 4, 3, 1, 16.83, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (609, '886d8126-78bf-401d-93f4-59c16686383f', 71, 5, 4, 7, 205, 4, 3, 1, 11.62, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (610, '1129fb14-4249-4650-8658-bad6508f327a', 71, 5, 4, 26, 205, 4, 4, 1, 34.86, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (611, '58530a27-3458-4068-8ade-1cc00740de4f', 71, 5, 6, 30, 140, 3, 6, 1, 25.76, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (612, '227934ea-058a-427f-9021-334571fc799c', 71, 5, 3, 8, 54, 3, 3, 1, 17.12, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (613, '654c6586-1050-4ec4-aa76-95a2ed92728b', 71, 5, 3, 10, 54, 3, 3, 1, 16.58, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (614, 'f7dab40b-9f86-4294-b40e-c905cc8dc9cf', 71, 5, 3, 13, 54, 3, 3, 1, 13.91, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (615, '4db3e1f3-16c1-427a-9c5f-88a14c6f8fbb', 71, 5, 3, 9, 54, 3, 3, 1, 17.12, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (616, 'c536e4ad-e7c9-4f53-807b-4c4a14e6b482', 71, 5, 3, 16, 54, 3, 3, 1, 18.19, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (617, '5f22489b-95c0-4ea1-ba6f-3e1aef5e6c52', 71, 5, 3, 1, 54, 3, 2, 1, 30.50, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (618, 'ed7c4122-39e5-42ef-84b1-157854743f1d', 72, 2, 5, 15, 67, 4, 3, 1, 12.96, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (619, '72fae6c7-f702-4d72-ac4c-964002426212', 72, 2, 5, 24, 67, 4, 4, 1, 46.08, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (620, '2fb2d9cd-3c20-456f-a6c6-eff8b0b623f6', 72, 2, 5, 3, 67, 4, 2, 1, 21.12, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (621, 'cf98c397-8e5e-42a8-9130-9290828a7919', 72, 2, 5, 7, 67, 4, 3, 1, 13.44, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (622, 'a24953be-af89-43f8-9d17-1dfbad00f0a0', 75, 3, 3, 15, 16, 4, 3, 1, 14.44, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (623, '4130bb38-37ee-408e-aa59-f19cf66f8cf0', 75, 3, 3, 9, 16, 4, 3, 1, 17.12, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (624, '5c9f05d4-b3b9-4c37-8ef6-64bc4efaf28c', 75, 3, 3, 11, 16, 4, 3, 1, 11.77, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (625, 'cc2a4505-9e2e-4a56-a86c-e034d6414a86', 75, 3, 3, 5, 16, 4, 2, 1, 36.38, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (626, 'dfc5db40-57b4-4441-a1fb-243354cb35b7', 76, 5, 7, 19, 120, 2, 4, 1, 37.62, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (627, 'ff2f584b-4370-4a79-95aa-64220af49ebd', 76, 5, 7, 17, 120, 2, 3, 1, 16.34, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (628, 'a5758bb5-caef-44b4-94ee-ed757e56ed98', 76, 5, 7, 14, 120, 2, 3, 1, 13.36, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (629, 'c6af9e85-95da-4358-8bb6-bf0f98a1561d', 71, 5, 6, 24, 140, 3, 4, 1, 53.76, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (630, '339a27eb-4797-4e3b-9bbf-9c686f30dfbf', 71, 5, 6, 26, 140, 3, 4, 1, 47.04, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (631, '18670528-b3c3-4deb-87fa-dd46877562e0', 71, 5, 6, 20, 72, 6, 4, 1, 35.84, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (632, '08a3bac2-c4f2-4984-a48c-504aa8ef5953', 71, 5, 6, 29, 72, 6, 6, 1, 58.24, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (633, '12831a4b-59aa-47b5-b71b-ba2cf279ff91', 71, 5, 6, 16, 72, 6, 3, 1, 19.04, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (634, 'c4152c6b-27d5-4595-8b9c-16a65f1964ba', 71, 5, 1, 5, 140, 3, 2, 1, 36.72, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (635, 'b065883b-e1e9-41b8-8395-d3ee8476b05d', 71, 5, 1, 26, 140, 3, 4, 1, 45.36, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (636, '1f1e3ed9-1092-4af5-8509-45660c94d7b2', 71, 5, 1, 22, 140, 3, 4, 1, 66.96, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (637, '666bc257-5465-4cbe-87da-a5229557ece5', 71, 5, 4, 20, 205, 4, 4, 1, 26.56, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (638, '07926ecc-a537-45eb-b9eb-a47f5de5e1d9', 71, 5, 4, 8, 205, 4, 3, 1, 13.28, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (639, '8914ab47-35a5-4712-ab30-90cbdc44b0a9', 72, 2, 8, 23, 220, 5, 4, 1, 52.65, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (640, 'e9a22216-9970-4520-845c-87d4cc39e3e3', 72, 2, 8, 29, 220, 5, 6, 1, 60.84, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (641, 'a0589d92-89ea-4121-b27b-678bf85e7f40', 75, 3, 7, 25, 47, 6, 4, 1, 25.74, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (642, '10052b74-26c8-45b6-9617-0be2c88f691c', 75, 3, 7, 18, 47, 6, 3, 1, 18.81, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (643, '5ab28b34-8707-4abf-be67-2808c36db2ea', 75, 3, 3, 29, 40, 6, 6, 1, 55.64, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (644, '3ceb71a1-66f7-4734-b001-a825b38ba15e', 75, 3, 3, 8, 40, 6, 3, 1, 17.12, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (645, 'b97d59ef-e6ec-41b3-8f84-719e25887f21', 75, 3, 3, 21, 40, 6, 4, 1, 32.10, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (646, '99b1e1f1-f516-461a-be85-572439c2081f', 75, 3, 3, 12, 40, 6, 3, 1, 12.30, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (647, 'ec54f168-35e4-415d-860c-b4047c2b422f', 75, 3, 3, 11, 40, 6, 3, 1, 11.77, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (648, '7f96fd01-b054-4818-90d1-d63cac5bb716', 75, 3, 4, 7, 202, 4, 3, 1, 11.62, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (649, 'ca3ed5cb-edcb-4e35-80f8-5a66025a4d00', 75, 3, 4, 4, 202, 4, 2, 1, 19.92, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (650, 'b71650ac-5b3d-4977-af88-a1f293c9914d', 71, 4, 8, 5, 174, 5, 2, 1, 39.78, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (651, 'ae118725-48db-4b48-a523-02fe9754c9f2', 71, 4, 8, 19, 174, 5, 4, 1, 44.46, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (652, '1659eb78-5f4e-41f3-9ba2-49c332319bb5', 71, 4, 8, 24, 174, 5, 4, 1, 56.16, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (653, '0c5eaa18-6ac0-4289-bbb6-bcba56181725', 71, 4, 8, 13, 174, 5, 3, 1, 15.21, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (654, 'e9da8b4f-1d71-4af2-86ec-17dcbfc4f3a1', 71, 4, 8, 25, 174, 5, 4, 1, 30.42, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (655, '73893f97-ed51-4b77-bc29-6d1e81b9cec1', 71, 4, 3, 16, 196, 5, 3, 1, 18.19, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (656, 'a69f0731-8777-439e-8bb5-3e80e97e2312', 71, 4, 3, 5, 196, 5, 2, 1, 36.38, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (657, '3538fcc8-f1b8-4a77-bb4b-4f04ddb5c5d7', 71, 4, 3, 28, 196, 5, 5, 1, 19.26, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (658, 'd9b41db7-b83c-4e43-a4a5-55b7c51c8c89', 71, 4, 8, 26, 201, 3, 4, 1, 49.14, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (659, 'aaf07024-da6b-45ee-acbc-ffd0a2eda1a3', 71, 4, 8, 4, 201, 3, 2, 1, 28.08, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (660, '27be7c1e-05e2-4ad3-b1c4-8cbe74ffada9', 71, 4, 8, 19, 201, 3, 4, 1, 44.46, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (661, '42eea5e4-c256-4d09-ba31-f2109d1552e0', 71, 4, 8, 9, 201, 3, 3, 1, 18.72, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (662, 'd769b6f0-3dd0-475a-83fa-4edbabcf63cf', 71, 4, 8, 23, 201, 3, 4, 1, 52.65, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (663, '67f26895-5e26-41ca-9961-307d18682536', 71, 4, 3, 24, 80, 4, 4, 1, 51.36, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (664, 'fe2aa92f-d5fd-43ad-8a01-93058d79dedd', 71, 4, 3, 3, 80, 4, 2, 1, 23.54, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (665, '98437857-a3fd-4534-8eb6-cad97ef93d45', 76, 5, 7, 25, 120, 2, 4, 1, 25.74, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (666, 'f57de6dc-0f40-4da7-864b-16a3655b23d4', 76, 5, 7, 22, 120, 2, 4, 1, 61.38, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (667, '37c6d554-130e-41c6-8926-21911719c77b', 77, 3, 8, 6, 195, 6, 3, 1, 14.62, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (668, 'd0b007cc-09f9-424b-95a3-1c632ff57f7c', 77, 3, 8, 14, 195, 6, 3, 1, 15.80, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (669, '42d1a82b-e6fd-4d3e-8961-7c9e41c10ba5', 77, 3, 8, 1, 195, 6, 2, 1, 33.34, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (670, '6b703a0d-00a3-42d6-b948-710f7d3a6560', 77, 3, 8, 24, 195, 6, 4, 1, 56.16, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (671, '8f877b33-a4f9-409c-9146-c3dbd7a8d7c4', 77, 3, 8, 7, 195, 6, 3, 1, 16.38, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (672, '4beb8f27-7f66-4b23-9f74-69c105bb2330', 77, 3, 6, 6, 70, 1, 3, 1, 14.00, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (673, 'b757a8dd-e384-4083-9ec9-e12f89f72190', 77, 3, 6, 26, 70, 1, 4, 1, 47.04, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (674, '836190ce-bc7d-4e7e-b691-f2b875425226', 77, 3, 6, 20, 209, 3, 4, 1, 35.84, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (675, 'ff02196b-ca88-4de0-b259-33579717fb61', 78, 3, 1, 9, 182, 4, 3, 1, 17.28, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (676, 'd8d995c3-ab37-410b-9ced-54623bc6bb7e', 78, 3, 7, 11, 195, 6, 3, 1, 10.89, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (677, '0d9c5d0d-0a81-4d9c-b705-87bb6cc4dfb7', 78, 3, 7, 26, 195, 6, 4, 1, 41.58, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (678, '049ab305-fc03-4b5c-a1eb-322827f96e3c', 78, 3, 7, 19, 195, 6, 4, 1, 37.62, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (679, '19a1e6fa-5a2e-46b0-9edd-7c03c9ed5265', 78, 3, 7, 22, 195, 6, 4, 1, 61.38, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (680, '4ee77dc3-8e11-4c58-a900-411daff494fb', 78, 3, 7, 5, 195, 6, 2, 1, 33.66, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (681, '3d284592-59f7-48f8-8f93-e71472f0acb1', 78, 3, 7, 25, 195, 6, 4, 1, 25.74, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (682, '539d490b-4a4b-4ad9-9586-e9472b2048ab', 82, 4, 6, 15, 133, 4, 3, 1, 15.12, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (683, '8dcf4a6a-436d-42c0-9042-c9bebd8b79ca', 82, 4, 6, 23, 133, 4, 4, 1, 50.40, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (684, '66faa6b7-362f-49d8-99db-d6cd2488b088', 82, 4, 8, 14, 82, 4, 3, 1, 15.80, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (685, 'b7ee7d27-ce74-4c1e-99b9-30cbeb8e44aa', 82, 4, 8, 28, 82, 4, 5, 1, 21.06, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (686, 'dc3b5a26-7f54-478b-9bda-75f309e79b1c', 82, 4, 8, 26, 82, 4, 4, 1, 49.14, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (687, '8808f222-7cb7-4e9c-a6b2-1a46cd23444b', 82, 3, 5, 5, 217, 5, 2, 1, 32.64, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (688, 'ab1a8e4a-db9a-4f6a-af12-c3e784972ab1', 82, 3, 5, 17, 217, 5, 3, 1, 15.84, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (689, 'cb834323-a012-4e8b-b9c0-e939f045c91a', 84, 2, 5, 7, 162, 4, 3, 1, 13.44, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (690, '387ca795-3b7b-42db-a31f-976ef7f5c590', 84, 2, 5, 13, 162, 4, 3, 1, 12.48, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (691, 'ec642996-4650-47b8-bdcd-a3e48020fc60', 77, 3, 7, 5, 205, 4, 2, 1, 33.66, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (692, '17a2874a-80ac-41fc-b5ea-28d9c7e1557a', 77, 3, 7, 15, 205, 4, 3, 1, 13.36, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (693, 'e8261292-1a59-40f1-acd6-e06abedcf42c', 77, 3, 7, 9, 205, 4, 3, 1, 15.84, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (694, '21770801-1422-458c-8b50-dd8000559de5', 77, 3, 6, 9, 209, 3, 3, 1, 17.92, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (695, '477fd7f3-bd96-4fe3-9b93-ead119cf9b35', 77, 3, 6, 21, 209, 3, 4, 1, 33.60, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (696, 'e4063a76-6c54-436c-b309-aaa8ddbf7c8b', 77, 3, 2, 24, 121, 4, 4, 1, 46.56, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (697, '9f0587eb-ae8a-445e-acd9-c9836fd55dd3', 77, 3, 2, 3, 121, 4, 2, 1, 21.34, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (698, 'd88e6f21-c6dc-4406-894b-22ebf3d70f4f', 77, 3, 6, 8, 70, 1, 3, 1, 17.92, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (699, '319acbe2-8bbe-45fa-a6e1-fa4b344f2daa', 77, 3, 6, 4, 70, 1, 2, 1, 26.88, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (700, '239bd504-e381-4745-99f2-be38a78a22ab', 77, 3, 6, 29, 70, 1, 6, 1, 58.24, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (701, '54230c1b-e354-4ab4-af5f-4b932ef391de', 78, 3, 5, 27, 210, 6, 4, 1, 20.16, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (702, '199136cd-3fb2-42a9-b3e7-f559f51ba08b', 78, 3, 5, 20, 210, 6, 4, 1, 30.72, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (703, '6dc29f5d-361f-4687-8b1f-1cb316e6f779', 78, 3, 5, 28, 210, 6, 5, 1, 17.28, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (704, '3a5fff3c-c016-4cbe-ac86-306d0d53180a', 78, 3, 1, 18, 182, 4, 3, 1, 20.52, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (705, '19dada58-eeda-43fd-9cc4-9fb12359c708', 78, 3, 2, 16, 147, 6, 3, 1, 16.49, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (706, '554bd07c-150e-462c-a864-5941a5c67b63', 78, 3, 2, 21, 147, 6, 4, 1, 29.10, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (707, '2224454d-ee44-4003-8da6-ab2cc2225634', 78, 3, 8, 21, 134, 5, 4, 1, 35.10, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (708, '27a7df33-5299-43f7-887a-2484dc9fa10e', 78, 3, 8, 22, 134, 5, 4, 1, 72.54, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (709, '84ef5cf6-a6f5-41d5-8539-8730830c62ec', 78, 3, 8, 18, 134, 5, 3, 1, 22.23, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (710, '0c134fae-d1ef-42af-8b19-e4ffdb367b76', 78, 3, 8, 19, 134, 5, 4, 1, 44.46, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (711, '89234180-f4d1-4e16-ae1e-feb2d64905b9', 82, 3, 5, 12, 217, 5, 3, 1, 11.04, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (712, '6f3a5f3a-2ec2-4b64-b820-f4fa78a543b1', 82, 3, 5, 6, 217, 5, 3, 1, 12.00, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (713, '627544c7-6e94-422f-85d3-ea5d8d2f722e', 82, 3, 5, 15, 217, 5, 3, 1, 12.96, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (714, '201e831d-9408-453a-8691-0b4e80b648e4', 82, 3, 6, 29, 90, 2, 6, 1, 58.24, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (715, '91e2901d-ba89-4b89-afa6-ff85f747b73d', 82, 3, 6, 21, 90, 2, 4, 1, 33.60, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (716, '0a2d6924-8d06-4137-9bf9-c3fbdc2b8423', 82, 3, 6, 12, 90, 2, 3, 1, 12.88, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (717, 'd495f77b-0181-4a59-897c-a968dd34b77e', 82, 3, 6, 14, 90, 2, 3, 1, 15.12, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (718, 'ea7efd73-49a8-4630-a4da-8d6a14f791c3', 82, 4, 8, 19, 82, 4, 4, 1, 44.46, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (719, 'de3864ea-4bb0-4f95-a5df-30121a23e686', 82, 4, 8, 6, 82, 4, 3, 1, 14.62, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (720, 'f2caa193-e4ea-481b-86bf-13604f4eca24', 82, 4, 8, 12, 82, 4, 3, 1, 13.46, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (721, 'cb99230d-d2ba-4a4a-bbdb-c19a989abc6f', 82, 4, 1, 19, 143, 6, 4, 1, 41.04, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (722, 'd601d651-82fc-44ef-8034-fff5b469ab5c', 82, 4, 1, 8, 143, 6, 3, 1, 17.28, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (723, '57bec9f7-5fa9-45a1-a5ba-d0fff8aade14', 82, 4, 1, 23, 143, 6, 4, 1, 48.60, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (724, 'bab71e89-853a-4425-b84e-8425819ce5fa', 82, 4, 1, 25, 143, 6, 4, 1, 28.08, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (725, 'd63b04ff-8cd3-492e-9efc-a4917aa5daa8', 84, 2, 8, 21, 67, 4, 4, 1, 35.10, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (726, '52a9e242-5a35-4e14-bd16-f960fa57a2da', 84, 2, 4, 2, 26, 6, 2, 1, 12.45, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (727, 'b5b5520f-55a7-4b9f-bbc9-875fe1cf238d', 85, 3, 7, 14, 6, 4, 3, 1, 13.36, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (728, '8e4695d6-5532-4e87-bb36-a3c39e9aff7e', 85, 3, 7, 8, 6, 4, 3, 1, 15.84, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (729, '324ed846-6602-4acd-bf58-715c3dbad3d1', 85, 3, 7, 28, 6, 4, 5, 1, 17.82, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (730, '04bacaf8-51a0-4418-8816-9c9e8130c008', 85, 3, 7, 27, 6, 4, 4, 1, 20.79, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (731, '32097762-379e-4058-b1ec-f9377c29c3ef', 85, 3, 7, 10, 6, 4, 3, 1, 15.34, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (732, '49e0303c-5d82-46aa-b238-42582c488181', 85, 3, 7, 22, 6, 4, 4, 1, 61.38, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (733, '4cfb4840-423f-41d5-83fb-a2159f3d078b', 85, 3, 5, 24, 19, 4, 4, 1, 46.08, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (734, '4722dda3-56a0-478e-99a6-85fab9112359', 85, 3, 5, 5, 19, 4, 2, 1, 32.64, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (735, 'f43e2aaf-7988-441f-8e81-e6788f54108d', 85, 3, 5, 2, 19, 4, 2, 1, 14.40, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (736, '2a88e978-595c-4ce0-ab1b-d4d97df9d872', 85, 3, 4, 3, 19, 4, 2, 1, 18.26, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (737, 'b50f6a7f-da4a-4120-be67-03e0f177a59b', 85, 3, 4, 17, 19, 4, 3, 1, 13.70, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (738, 'f074c831-0d4a-4dd9-affe-bb92c33f3408', 86, 2, 4, 26, 105, 4, 4, 1, 34.86, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (739, '104f0425-5b08-44c2-83c6-e344744e5911', 86, 2, 4, 2, 105, 4, 2, 1, 12.45, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (740, '3cf84b3e-ba2b-46ef-ad9b-82577d60d367', 86, 2, 6, 11, 179, 4, 3, 1, 12.32, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (741, '2f23d654-7787-4cf4-a2ba-4e7449475a04', 86, 2, 6, 27, 179, 4, 4, 1, 23.52, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (742, 'ef83e3e0-893d-4f10-bfee-b89d7be7956e', 86, 2, 6, 9, 179, 4, 3, 1, 17.92, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (743, '5ade5613-66fd-4814-b7f3-b504a58dbeb4', 86, 2, 6, 23, 179, 4, 4, 1, 50.40, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (744, '3f330119-9ad3-4794-88fa-ade6de9630f1', 87, 4, 2, 26, 45, 6, 4, 1, 40.74, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (745, '3767d9a1-bdd6-452a-a851-d616bf88fa80', 87, 4, 2, 16, 45, 6, 3, 1, 16.49, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (746, 'd569c2ed-0006-4c8e-bf6a-5f87ed2d57e1', 86, 2, 5, 12, 25, 1, 3, 1, 11.04, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (747, '48c4806f-4c1e-44c5-8d88-eec0eeb3f13e', 86, 2, 5, 16, 25, 1, 3, 1, 16.32, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (748, '8c53eae0-6a6c-4f20-996d-8a1b20565dc3', 86, 2, 2, 8, 214, 2, 3, 1, 15.52, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (749, '0d895f92-aa87-4c1c-9c11-db192626b382', 86, 2, 2, 26, 214, 2, 4, 1, 40.74, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (750, '615abb82-cf44-4924-bf37-5418e4cbf88d', 86, 2, 2, 3, 214, 2, 2, 1, 21.34, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (751, 'fb937ab0-2383-4fe1-8b02-15432e279024', 84, 2, 4, 28, 26, 6, 5, 1, 14.94, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (752, '651d861c-3900-474e-9874-3ea8b4d5dbfc', 84, 2, 8, 27, 67, 4, 4, 1, 24.57, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (753, '8791e5ba-18c6-43ed-8288-0aea1846f647', 84, 2, 8, 5, 67, 4, 2, 1, 39.78, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (754, 'b4c7dfad-e61e-48f0-9e15-2417d0a04e50', 84, 2, 3, 26, 32, 3, 4, 1, 44.94, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (755, '0a89f6ab-fe31-4cbb-8d57-0efb16529197', 84, 2, 3, 16, 32, 3, 3, 1, 18.19, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (756, 'efa5067c-ccb1-4506-a0df-36ca31834e28', 84, 2, 3, 8, 32, 3, 3, 1, 17.12, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (757, '63b4495e-f131-46a6-9d8a-f1ae6a98489e', 84, 2, 3, 29, 32, 3, 6, 1, 55.64, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (758, 'b1af259d-23c4-4d68-8e35-b324facd8ee9', 87, 4, 3, 8, 96, 5, 3, 1, 17.12, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (759, '19ea02bf-c985-4044-b918-4ddec091a962', 87, 4, 3, 21, 96, 5, 4, 1, 32.10, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (760, '7e144ac9-9ab4-4154-9543-f3d6de5e40e7', 87, 4, 3, 18, 96, 5, 3, 1, 20.33, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (761, 'c20a2918-4a8b-4f41-9032-63959d5ce3c1', 87, 4, 3, 27, 96, 5, 4, 1, 22.47, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (762, 'c268f3f0-80f9-46ee-bf8d-bc3cde11adf5', 87, 4, 3, 3, 96, 5, 2, 1, 23.54, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (763, 'e5d8a2af-7ef6-4547-b8d1-9b8b3e0eca24', 85, 3, 4, 1, 13, 1, 2, 1, 23.66, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (764, '8e490e50-3e15-439c-9d80-daa57384355b', 85, 3, 4, 24, 13, 1, 4, 1, 39.84, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (765, '76bc0d8b-87d9-4031-9766-37d33b26f932', 85, 3, 4, 19, 13, 1, 4, 1, 31.54, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (766, 'ea2b1df0-7351-4c59-8d3a-78008777b096', 85, 3, 4, 9, 13, 1, 3, 1, 13.28, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (767, 'c210a6a1-8893-4bf7-bcb7-e4014174f2ba', 85, 3, 4, 17, 13, 1, 3, 1, 13.70, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (768, '7688aa6a-d972-4feb-9e57-9de59fb21f4f', 85, 3, 6, 6, 74, 5, 3, 1, 14.00, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (769, 'c92d0441-e520-4168-8e85-514f79ea0197', 85, 3, 6, 2, 74, 5, 2, 1, 16.80, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (770, 'be0698be-9a5f-4dcb-b1f8-3ba1980df1ec', 85, 3, 6, 8, 74, 5, 3, 1, 17.92, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (771, 'a5354c7b-ca51-4521-94f6-c32bbc24002c', 85, 3, 6, 24, 74, 5, 4, 1, 53.76, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (772, '6a711f7a-b7fd-44c5-a757-8421b3bae68f', 85, 3, 6, 17, 156, 5, 3, 1, 18.48, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (773, 'cf7eac35-f43b-43fd-8db9-ee105c9cd5ca', 85, 3, 6, 25, 156, 5, 4, 1, 29.12, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (774, 'e4176b1f-5c91-43aa-a28b-3bf50a7df7b0', 87, 4, 1, 7, 177, 6, 3, 1, 15.12, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (775, 'f0a40814-8773-4bba-b833-14449e532363', 87, 4, 1, 6, 177, 6, 3, 1, 13.50, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (776, '9a4e607e-8d77-464d-bfa0-fc547f7d5aa6', 87, 2, 7, 19, 18, 5, 4, 1, 37.62, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (777, 'b691c9f2-0a03-4794-929c-307b9c0ce0a3', 87, 2, 7, 26, 18, 5, 4, 1, 41.58, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (778, '4297bf84-b6b6-41e9-9ba6-b967ce62fc03', 87, 2, 7, 30, 18, 5, 6, 1, 22.77, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (779, '964dd98b-f62a-4325-aefd-910f7a8a6c15', 87, 2, 7, 8, 18, 5, 3, 1, 15.84, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (780, '96223b89-162e-4c27-b6b4-e1886ecbb8d6', 87, 2, 2, 21, 207, 4, 4, 1, 29.10, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (781, '6183ff96-8e75-47ad-a900-2d8e81cfcc2e', 87, 2, 2, 5, 207, 4, 2, 1, 32.98, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (782, '697a33c7-6591-46cb-9e2a-20027b71492a', 87, 2, 5, 11, 102, 3, 3, 1, 10.56, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (783, '4229c60e-ee5d-40b1-b749-37963e884d80', 87, 2, 5, 5, 102, 3, 2, 1, 32.64, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (784, '9896ec3b-9656-46ee-bcd2-2031ec1cdba6', 87, 2, 5, 3, 102, 3, 2, 1, 21.12, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (785, 'eb8bd924-f524-41c8-937a-cae5be5d84ab', 89, 3, 8, 27, 132, 4, 4, 1, 24.57, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (786, '79ca13e3-f37a-4958-9ec9-4fb4244d0343', 89, 5, 3, 11, 152, 6, 3, 1, 11.77, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (787, 'fabd79d1-2f86-441b-9457-fbb136201754', 89, 5, 3, 16, 152, 6, 3, 1, 18.19, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (788, 'e7ad6542-5c12-4515-b652-df9b1928f6b2', 89, 5, 3, 18, 152, 6, 3, 1, 20.33, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (789, '4e4f05e6-dcb7-470f-8611-1e87cca02efd', 92, 2, 4, 19, 69, 6, 4, 1, 31.54, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (790, '129cca94-8272-455b-a69f-5883f51c7e59', 92, 2, 4, 9, 69, 6, 3, 1, 13.28, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (791, '4c67c873-c5fd-4fa7-a533-07efd184f5ee', 92, 2, 4, 27, 69, 6, 4, 1, 17.43, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (792, 'c7530d1f-f306-451c-89cf-5c8f541016e4', 92, 2, 4, 18, 69, 6, 3, 1, 15.77, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (793, '569fbe34-7074-4bb8-894c-773c1ac1bc9b', 92, 2, 5, 15, 35, 1, 3, 1, 12.96, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (794, '318941df-7063-4a81-a9ee-5f13c1f762d3', 92, 2, 5, 9, 35, 1, 3, 1, 15.36, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (795, 'e9abd84d-aed3-4a99-9902-e7c3ca9dbb13', 92, 2, 5, 6, 35, 1, 3, 1, 12.00, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (796, '9537b87c-60d5-4a97-8b27-b8182ede79eb', 92, 2, 5, 5, 35, 1, 2, 1, 32.64, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (797, 'ee44048d-727a-402d-82bc-4f304fe3b4f3', 92, 2, 6, 5, 191, 5, 2, 1, 38.08, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (798, '02661a24-c309-4a60-bf36-51436ef11d49', 92, 2, 6, 11, 191, 5, 3, 1, 12.32, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (799, '7291d808-609e-464b-bbed-75f45cdac430', 92, 2, 6, 14, 191, 5, 3, 1, 15.12, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (800, 'a3f20be4-3774-4eab-9990-1288ebbcd966', 92, 2, 6, 2, 191, 5, 2, 1, 16.80, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (801, 'a0dc85ae-6faf-4ddf-a1b8-11745d094ff6', 92, 2, 6, 19, 191, 5, 4, 1, 42.56, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (802, '1ffc95dc-b874-4825-b3fe-e092114b2e87', 92, 2, 6, 8, 191, 5, 3, 1, 17.92, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (803, '0e42dfc9-9c57-4dd3-8ec7-c43f70e211eb', 87, 4, 7, 10, 132, 4, 3, 1, 15.34, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (804, '7556acce-a92c-42af-a89a-31fa05abe3b6', 87, 4, 7, 18, 132, 4, 3, 1, 18.81, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (805, '27c1a2f8-a390-4c36-905c-cb35e25e771d', 87, 4, 7, 23, 132, 4, 4, 1, 44.55, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (806, '0bb5d3bf-b03f-480c-b84c-0ab21dd6b7ef', 87, 4, 7, 3, 132, 4, 2, 1, 21.78, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (807, 'e3be6cb1-e2ad-41ff-81da-89e43bb6a396', 87, 4, 7, 8, 132, 4, 3, 1, 15.84, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (808, '38ea2a10-1c63-4e39-804f-b9daf2cc79fb', 87, 4, 1, 18, 177, 6, 3, 1, 20.52, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (809, 'c01ac077-6189-4177-b71f-8e671859f356', 93, 4, 4, 19, 214, 2, 4, 1, 31.54, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (810, '14079434-cabd-4f7d-9241-49a9f8f52801', 93, 4, 4, 15, 214, 2, 3, 1, 11.20, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (811, '80f75502-a5e3-4d77-bd64-14be8b077c7d', 93, 4, 4, 12, 214, 2, 3, 1, 9.54, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (812, 'c931c6be-01b5-46f3-b4da-56ba07ee38d4', 93, 4, 4, 24, 214, 2, 4, 1, 39.84, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (813, 'e49edc0d-fc22-478f-8d17-a8cf1a57ac8e', 93, 4, 4, 11, 214, 2, 3, 1, 9.13, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (814, '5fb55625-d834-4724-860a-55ecf680fbe1', 89, 5, 3, 26, 217, 5, 4, 1, 44.94, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (815, '4a21cfc3-60da-43f2-a5c4-8112571f66e4', 89, 5, 3, 13, 217, 5, 3, 1, 13.91, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (816, 'caa7fe6f-3309-4940-9e09-777f9ca2e10d', 89, 5, 8, 6, 35, 1, 3, 1, 14.62, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (817, '5e0c4ea5-2c2e-43ca-8a2b-652060226642', 89, 5, 8, 15, 35, 1, 3, 1, 15.80, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (818, '70ea4a31-8b92-4156-8c91-4b9773f6b539', 89, 5, 8, 5, 35, 1, 2, 1, 39.78, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (819, '29bd70d2-0bc8-4a7e-824e-19d982d6cee8', 89, 5, 8, 29, 35, 1, 6, 1, 60.84, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (820, '6af28e24-4c6e-4d5a-b20a-42a111b0fe37', 89, 5, 3, 22, 152, 6, 4, 1, 66.34, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (821, '7855eba0-391d-4db3-a0c3-991e59d54749', 89, 5, 3, 28, 152, 6, 5, 1, 19.26, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (822, '55de88d8-08b6-4fd4-b86a-1f7c992abe76', 89, 5, 3, 17, 152, 6, 3, 1, 17.66, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (823, '674288ec-d4df-4ad5-98ff-0cba2d5f99b5', 89, 5, 1, 24, 179, 4, 4, 1, 51.84, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (824, 'fae8d58d-8612-47c5-92ab-f9ca5645dc40', 89, 5, 1, 5, 179, 4, 2, 1, 36.72, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (825, 'd95c7680-51b1-4c79-80c6-55c7d3481a59', 92, 2, 5, 22, 207, 4, 4, 1, 59.52, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (826, '1142d41d-7cd7-449b-87ea-afa50dd1d760', 92, 2, 5, 17, 207, 4, 3, 1, 15.84, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (827, '40fe96c0-f0c3-469b-b35c-47b3c74b46f7', 92, 2, 5, 19, 207, 4, 4, 1, 36.48, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (828, '625a5abc-5dd6-4ed1-aa98-518532d74588', 92, 2, 5, 18, 207, 4, 3, 1, 18.24, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (829, '3de2a44b-1e05-43ec-8dbe-047305574b2a', 92, 2, 5, 27, 207, 4, 4, 1, 20.16, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (830, 'a47cba10-01a2-4e5e-81b4-739e3a07a308', 89, 3, 8, 7, 187, 5, 3, 1, 16.38, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (831, 'b5e5aa5f-8abd-4f46-8af3-957148e77055', 89, 3, 8, 26, 187, 5, 4, 1, 49.14, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (832, 'e7f6f568-7425-4b2c-a2e1-7de0b0d54644', 89, 3, 8, 13, 187, 5, 3, 1, 15.21, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (833, '4d2c8301-bd25-4c86-8a22-8062f1b97f82', 89, 3, 8, 19, 187, 5, 4, 1, 44.46, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (834, 'a7ac1255-e285-4e8f-a894-68ac67c0ddf7', 89, 3, 8, 3, 187, 5, 2, 1, 25.74, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (835, '487461cd-39b8-43a1-9ab4-382c0d32bde8', 89, 3, 4, 7, 48, 4, 3, 1, 11.62, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (836, 'c4b65b17-a382-407e-893f-9d2ca280fb58', 89, 3, 4, 21, 48, 4, 4, 1, 24.90, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (837, '4b5dce26-b9e0-4af3-855a-f6c797d9c4c6', 89, 3, 4, 25, 48, 4, 4, 1, 21.58, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (838, '92cda2f6-6f51-4dcb-ad8e-bdb84794c5e0', 89, 3, 4, 17, 48, 4, 3, 1, 13.70, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (839, '45a27aeb-b9bd-4a66-a87d-ead3fcfb751e', 89, 3, 8, 20, 132, 4, 4, 1, 37.44, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (840, 'b7eb963d-fc20-4237-ac00-5b8ce3595207', 89, 3, 8, 9, 132, 4, 3, 1, 18.72, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (841, '6857483a-872a-41fa-a874-2357fc85d686', 89, 3, 6, 15, 95, 6, 3, 1, 15.12, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (842, '8f9e81d8-1e6e-4322-b2d5-59fa7eda2d02', 89, 3, 6, 2, 95, 6, 2, 1, 16.80, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (843, 'da32ea82-52ef-4cb6-a544-7a75b9ad777a', 89, 3, 6, 1, 95, 6, 2, 1, 31.92, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (844, '2382a273-0bf9-4d6d-ac0b-bafad016cdb4', 89, 3, 6, 22, 95, 6, 4, 1, 69.44, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (845, 'd21ee8c3-2e93-4238-bda5-d8d595c543cc', 93, 4, 3, 27, 94, 4, 4, 1, 22.47, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (846, '187c1e16-b5a9-4b35-a743-aead07ff7a31', 93, 4, 3, 20, 94, 4, 4, 1, 34.24, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (847, '8b79b718-dba3-45ce-b15c-84f18f18161a', 93, 4, 3, 25, 94, 4, 4, 1, 27.82, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (848, '2287f47d-7bd6-49cf-9595-9b9232f4c8c1', 93, 4, 3, 9, 94, 4, 3, 1, 17.12, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (849, '0b7e8737-630c-4a92-b8f2-de3b3f7eb0ca', 93, 4, 3, 7, 94, 4, 3, 1, 14.98, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (850, 'ec35123a-c858-4200-a0fa-1cb8194b3b74', 93, 4, 3, 18, 94, 4, 3, 1, 20.33, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (851, '86754701-be10-409f-a152-5ea53d5d19e7', 93, 4, 7, 30, 95, 6, 6, 1, 22.77, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (852, '7fda7990-421c-45e8-aa25-9948d069ada2', 93, 4, 7, 8, 95, 6, 3, 1, 15.84, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (853, '139267e5-f37f-46e1-be98-2fd06776308e', 93, 4, 7, 11, 95, 6, 3, 1, 10.89, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (854, '3898a721-7ab1-44ce-bfa9-9fb1e8a96dd7', 93, 4, 6, 1, 57, 3, 2, 1, 31.92, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (855, '6db25184-d53c-4efd-9d31-586e6ec62341', 93, 4, 6, 14, 57, 3, 3, 1, 15.12, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (856, 'af9a7d5a-ccf9-4afd-99dd-d7e565ed8cb1', 93, 4, 6, 19, 57, 3, 4, 1, 42.56, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (857, 'c36e629d-7dd4-4830-bde8-fec39edd1a3d', 93, 4, 6, 28, 57, 3, 5, 1, 20.16, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (858, 'e55aea92-7d03-4c7d-bceb-e6c4dbbd5436', 93, 4, 6, 25, 57, 3, 4, 1, 29.12, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (859, '0bffea65-6cda-46b3-aee6-5400730920cb', 93, 2, 8, 10, 79, 5, 3, 1, 18.14, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (860, '17cfbc1f-69d2-4067-978c-4fd0e7290332', 93, 2, 8, 4, 79, 5, 2, 1, 28.08, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (861, '1484ac01-34de-4569-9424-cf7ce410d64c', 93, 2, 8, 15, 79, 5, 3, 1, 15.80, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (862, 'df684369-c071-4fcc-8352-84a23357a143', 93, 2, 8, 2, 79, 5, 2, 1, 17.55, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (863, '749638e9-22bc-432f-93c7-09f0e21353f9', 93, 2, 8, 13, 79, 5, 3, 1, 15.21, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (864, 'db073c9a-1520-439b-9c79-f51afe98a1f0', 93, 2, 8, 6, 79, 5, 3, 1, 14.62, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (865, '7a3656fc-30db-4e04-b695-e1672d9743cc', 93, 2, 4, 14, 196, 5, 3, 1, 11.20, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (866, '8c6cb7c3-f436-426b-9798-df6f5710f342', 93, 2, 4, 2, 196, 5, 2, 1, 12.45, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (867, 'd4d19ce3-1781-4d4a-8bc7-bd4a62da0615', 93, 2, 4, 22, 196, 5, 4, 1, 51.46, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (868, '4c042378-c5ff-40fd-b9f1-522e3fae92a6', 93, 2, 4, 13, 196, 5, 3, 1, 10.79, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (869, '510fc4e9-f193-49c5-accc-2a410a482368', 93, 4, 4, 27, 182, 4, 4, 1, 17.43, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (870, '32f82cd6-225e-4195-9f68-a6d42fcd7194', 93, 4, 4, 17, 182, 4, 3, 1, 13.70, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (871, 'f3961d23-769a-4876-a966-492f1746edfd', 93, 4, 4, 28, 182, 4, 5, 1, 14.94, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (872, '2c492864-8ecc-4669-b1ed-ee136a22628c', 93, 4, 4, 21, 182, 4, 4, 1, 24.90, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (873, 'a141d366-b4fe-424b-ad48-3c2a118e3912', 94, 5, 2, 24, 148, 6, 4, 1, 46.56, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (874, '595b045c-25c3-483e-8a27-b116cdce1514', 94, 5, 2, 6, 148, 6, 3, 1, 12.12, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (875, '1e99b687-5305-4010-a0f5-e611078ab63b', 94, 5, 2, 29, 148, 6, 6, 1, 50.44, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (876, 'dda6f986-3404-486f-827f-8029528a9217', 94, 5, 2, 11, 148, 6, 3, 1, 10.67, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (877, '72c24cb1-4401-41e1-a79f-f6a4238c1755', 94, 5, 2, 10, 148, 6, 3, 1, 15.04, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (878, '1857f6df-75d5-4e0d-8c70-1a22f80d83bb', 94, 5, 8, 1, 29, 6, 2, 1, 33.34, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (879, 'd78289c3-e45e-4a8b-9105-a36f92ecbb52', 94, 5, 8, 9, 29, 6, 3, 1, 18.72, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (880, 'adc1a811-c88c-4ce7-bd72-c2dea845c926', 94, 5, 8, 28, 29, 6, 5, 1, 21.06, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (881, 'c6251e0d-b14d-4a30-85d1-32fbfb0d176c', 94, 5, 8, 26, 111, 5, 4, 1, 49.14, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (882, '7de67bd7-2037-4d02-9f28-54423b69b6bb', 94, 5, 8, 20, 111, 5, 4, 1, 37.44, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (883, 'e09bf64c-6c79-4249-a5ac-c215a8bc6a3d', 94, 5, 8, 10, 111, 5, 3, 1, 18.14, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (884, 'a6163869-32e3-419c-b7c5-80333c019c67', 94, 5, 8, 19, 111, 5, 4, 1, 44.46, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (885, '9d5c93fd-e553-4048-839d-f1c7e285eb0e', 94, 5, 7, 29, 96, 5, 6, 1, 51.48, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (886, 'f3adccac-5811-49a5-bba8-2a265360b48e', 94, 5, 7, 9, 96, 5, 3, 1, 15.84, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (887, '0d9329ed-539e-4f83-b77b-a20ca4ccaab8', 94, 5, 7, 16, 96, 5, 3, 1, 16.83, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (888, '9781af8c-002f-4314-b84d-a62c9a40779d', 94, 5, 7, 13, 96, 5, 3, 1, 12.87, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (889, '20847270-be96-4bdc-814c-77e9e7eb76b0', 94, 5, 2, 4, 41, 6, 2, 1, 23.28, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (890, '1b4cd677-f5e6-4af0-92d8-595465293d88', 94, 5, 2, 26, 41, 6, 4, 1, 40.74, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (891, '5ee808fc-5e33-4d9b-ac39-ec798538de84', 94, 5, 2, 29, 41, 6, 6, 1, 50.44, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (892, '708ba8f4-2528-4d94-b25b-5fb6f824dfdc', 94, 5, 5, 27, 117, 4, 4, 1, 20.16, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (893, 'cc9110ee-0be0-4bc8-b837-49a785fdaeb9', 94, 5, 5, 9, 117, 4, 3, 1, 15.36, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (894, '51ac6d7e-92a4-4ed7-a134-3f484c8ffe88', 94, 3, 7, 3, 163, 1, 2, 1, 21.78, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (895, 'e7ad223e-c68a-4f89-93a5-22aba6b6b2c2', 94, 3, 7, 30, 163, 1, 6, 1, 22.77, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (896, '09e6a943-92a6-4fe7-b995-28b24d80546a', 93, 4, 4, 26, 214, 2, 4, 1, 34.86, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (897, 'd70a766e-27ed-4de0-a2f6-c84db88219bd', 93, 4, 6, 30, 119, 5, 6, 1, 25.76, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (898, '8a2abc53-ecaf-400e-a504-351ced84ddef', 93, 4, 6, 2, 119, 5, 2, 1, 16.80, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (899, '5b118de4-7da4-4863-8739-1738b9a99561', 93, 4, 6, 11, 119, 5, 3, 1, 12.32, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (900, '10b40662-d755-4996-a6ee-a6ee5d5558bb', 93, 4, 1, 23, 81, 5, 4, 1, 48.60, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (901, '9b125ca7-cced-4f99-b680-470dcedbddc2', 93, 4, 1, 7, 81, 5, 3, 1, 15.12, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (902, '1fe821e8-8aac-41c9-964d-a88b2516a186', 93, 4, 1, 2, 81, 5, 2, 1, 16.20, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (903, '25547819-fbe3-4a62-b142-709adfb79f95', 93, 4, 1, 17, 81, 5, 3, 1, 17.82, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (904, 'b20b39a7-8139-4a91-98be-cf64752e1c5d', 94, 3, 7, 5, 163, 1, 2, 1, 33.66, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (905, '78106852-7c5c-4abd-b634-6b1f791d825d', 94, 3, 7, 27, 163, 1, 4, 1, 20.79, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (906, '89fd094f-419c-4e18-ab50-61f3bf32d011', 94, 3, 6, 11, 211, 1, 3, 1, 12.32, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (907, 'fc49cde5-ad32-4e07-9e2a-f3713efd4f32', 94, 3, 6, 21, 211, 1, 4, 1, 33.60, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (908, 'e3824555-8442-4e76-b712-95f048ceeaf7', 94, 3, 6, 28, 211, 1, 5, 1, 20.16, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (909, 'f2256b8c-8f03-440e-ac01-1fb9ec569afa', 94, 3, 7, 30, 84, 6, 6, 1, 22.77, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (910, '9aa0be0e-b504-4def-a63d-f85cf7620968', 94, 3, 7, 20, 84, 6, 4, 1, 31.68, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (911, '92c90ca9-0cf5-4d21-be4e-f0f0ee23f77b', 95, 3, 3, 21, 209, 3, 4, 1, 32.10, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (912, 'ddd26890-b2dd-4648-87e2-92402ae2268e', 95, 3, 3, 5, 209, 3, 2, 1, 36.38, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (913, 'daa482d6-3c9a-483c-85ef-44bcb2b004e9', 95, 3, 3, 27, 209, 3, 4, 1, 22.47, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (914, '9e946cfa-c904-4430-a44a-c2687ca52ce2', 95, 3, 3, 19, 209, 3, 4, 1, 40.66, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (915, '4675e589-e634-4251-92df-30771e7add4d', 95, 3, 8, 27, 57, 3, 4, 1, 24.57, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (916, '8d570ede-b980-414a-b353-1355df7e6305', 95, 3, 8, 28, 57, 3, 5, 1, 21.06, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (917, 'adb5f29c-1a19-4fb8-a345-205514ec2d85', 95, 3, 8, 15, 57, 3, 3, 1, 15.80, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (918, '41b8904a-fc7f-4328-9ecf-19ab2a6e4295', 95, 3, 5, 18, 24, 4, 3, 1, 18.24, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (919, '0a99f8db-f0c0-4b0a-9952-ab0a9adc0b15', 95, 3, 5, 20, 24, 4, 4, 1, 30.72, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (920, 'fd052c79-3648-4237-bb6c-76e34ef1f710', 95, 5, 8, 20, 88, 6, 4, 1, 37.44, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (921, 'd3730bc1-ce83-4156-869f-ee3fbcb434d9', 95, 5, 8, 7, 88, 6, 3, 1, 16.38, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (922, '071c045e-4885-4d78-83ec-00003bdcb6b8', 95, 5, 8, 28, 88, 6, 5, 1, 21.06, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (923, '6ad443e4-44c8-4ceb-a532-8c3893c58112', 95, 5, 8, 12, 88, 6, 3, 1, 13.46, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (924, '0ff15c1f-5264-4641-8f53-47f514e308ea', 96, 2, 5, 28, 137, 6, 5, 1, 17.28, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (925, 'c34e4156-133e-44c0-a7c2-f59570ff79a3', 96, 2, 5, 25, 137, 6, 4, 1, 24.96, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (926, '93d90875-ea68-490e-bd11-cf3f30afea85', 96, 2, 5, 4, 137, 6, 2, 1, 23.04, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (927, 'e273b236-b92e-48c0-a501-63e1ccd397b1', 96, 2, 1, 14, 205, 4, 3, 1, 14.58, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (928, 'a6122aeb-ec50-49c8-b66c-18e937539229', 96, 2, 4, 6, 88, 6, 3, 1, 10.38, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (929, 'bece50b0-6d7d-41e5-8e09-ea443d26b96d', 96, 2, 4, 2, 88, 6, 2, 1, 12.45, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (930, 'cf7821a0-636a-4cd5-97d5-e5a12d572c6e', 96, 2, 4, 17, 88, 6, 3, 1, 13.70, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (931, 'b6c05330-b248-4e9a-9f9b-f115295cb925', 96, 2, 4, 18, 88, 6, 3, 1, 15.77, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (932, '7ab6254f-67da-49f9-a710-bc417c024824', 96, 2, 4, 11, 88, 6, 3, 1, 9.13, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (933, '8e9eb7f6-6b1e-433d-8672-6f261f1102e2', 96, 2, 4, 7, 88, 6, 3, 1, 11.62, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (934, '3f695ec5-6bc8-4a01-9973-9cd03e33045f', 96, 3, 7, 20, 88, 6, 4, 1, 31.68, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (935, '7e8e1406-7c20-4710-bd51-11b968da0b2a', 96, 3, 7, 16, 88, 6, 3, 1, 16.83, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (936, '4e7797ab-3563-4ce9-b0aa-5069fb8b8e51', 96, 3, 7, 7, 88, 6, 3, 1, 13.86, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (937, 'c84f5fc6-8132-4528-8975-c73a010d6a13', 97, 5, 4, 11, 109, 6, 3, 1, 9.13, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (938, '67dd3062-d627-4c69-ad7a-6fec0d844134', 97, 5, 4, 9, 109, 6, 3, 1, 13.28, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (939, '349989ac-72c5-4554-af15-fcee655ea5fe', 94, 3, 8, 3, 160, 4, 2, 1, 25.74, true, false);
INSERT INTO public.bi_fato_atendimento VALUES (940, '490aa0c4-7dd0-46de-bb6c-e1eac864dd87', 94, 3, 8, 18, 160, 4, 3, 1, 22.23, true, false);
INSERT INTO public.bi_fato_atendimento VALUES (941, '709c05eb-d71f-4da5-ab0f-e8d92630b7b5', 94, 3, 8, 22, 160, 4, 4, 1, 72.54, true, false);
INSERT INTO public.bi_fato_atendimento VALUES (942, '7ad1c547-9c1b-44cc-8254-e92c9e43f5dc', 94, 3, 8, 20, 160, 4, 4, 1, 37.44, true, false);
INSERT INTO public.bi_fato_atendimento VALUES (943, 'a96b5947-5b87-4c04-9366-a6099bcd96e9', 94, 3, 6, 17, 211, 1, 3, 1, 18.48, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (944, 'dab85cf4-292e-4fb0-8895-4984a2fc27a6', 95, 3, 3, 22, 148, 6, 4, 1, 66.34, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (945, '13d7b13a-6e7c-4c06-af8a-9a048d01d47b', 95, 3, 3, 12, 148, 6, 3, 1, 12.30, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (946, 'c58b4701-ac39-436d-a051-51d6065591fe', 95, 3, 3, 4, 148, 6, 2, 1, 25.68, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (947, 'f251bbe8-1a02-42d3-a1a6-f67d86a95c12', 95, 3, 3, 25, 148, 6, 4, 1, 27.82, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (948, '04e79f86-5c1f-4d09-9257-6fda465500b5', 95, 3, 1, 17, 216, 3, 3, 1, 17.82, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (949, '4dfd1946-e3af-4604-839e-eed802851b59', 95, 3, 1, 23, 216, 3, 4, 1, 48.60, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (950, '1f1dfc47-4379-4595-956b-56a829ab4183', 95, 3, 1, 12, 216, 3, 3, 1, 12.42, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (951, 'c4731def-beba-4b2b-85c8-e20947df97ba', 95, 3, 1, 28, 216, 3, 5, 1, 19.44, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (952, 'aa42cd52-db2c-4013-9a6d-1ccc74961926', 95, 3, 1, 16, 216, 3, 3, 1, 18.36, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (953, '1311b553-07d9-4348-b6f3-67db55829511', 96, 2, 1, 25, 205, 4, 4, 1, 28.08, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (954, '9363c113-3067-426f-a92a-2715d7e0caaa', 96, 2, 1, 12, 205, 4, 3, 1, 12.42, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (955, '1ad530ab-fdd7-4280-af7a-1982c037f12c', 96, 2, 6, 17, 83, 6, 3, 1, 18.48, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (956, '0dfaaaeb-2871-4795-be97-01505ed04c80', 96, 2, 6, 14, 83, 6, 3, 1, 15.12, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (957, 'c0e9afb9-75a6-44aa-8e84-5f84eca34a83', 96, 2, 5, 3, 135, 6, 2, 1, 21.12, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (958, '6c4f2405-a21a-44de-84d5-a50b7235db4b', 96, 2, 5, 12, 135, 6, 3, 1, 11.04, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (959, 'ec345890-6097-454c-a7a2-16ea92222fdb', 96, 2, 5, 15, 135, 6, 3, 1, 12.96, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (960, 'a746d392-be62-4505-95c6-771243bcf8df', 96, 3, 1, 20, 4, 4, 4, 1, 34.56, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (961, '029bcc09-e15d-4793-88f4-fc62490b683d', 96, 3, 1, 2, 4, 4, 2, 1, 16.20, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (962, 'e57de6fe-d2f8-418f-8193-3fed1a262f40', 96, 3, 1, 27, 4, 4, 4, 1, 22.68, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (963, '367acae7-5a07-4ee3-961d-25fc6683037c', 97, 5, 7, 6, 152, 6, 3, 1, 12.38, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (964, '248e435d-5d46-4bf7-8ef8-59adecd9d283', 97, 5, 7, 4, 152, 6, 2, 1, 23.76, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (965, '4203a9d0-50cb-4172-a442-f02c542ed2e1', 97, 5, 7, 17, 152, 6, 3, 1, 16.34, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (966, '7e1f7e09-a38b-46c2-a3f3-ed4b0c459a40', 97, 5, 7, 24, 152, 6, 4, 1, 47.52, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (967, 'cd354b7e-38a2-44f4-9528-a3ac7eae6760', 97, 5, 7, 15, 152, 6, 3, 1, 13.36, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (968, 'c2b473ce-40e9-40bd-8774-83348e744701', 97, 5, 3, 26, 97, 6, 4, 1, 44.94, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (969, '9f5d90b9-5551-47ad-8206-7787c3633271', 97, 5, 3, 10, 97, 6, 3, 1, 16.58, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (970, '73c37f4d-6819-4fae-b711-e2f3057bb00f', 97, 5, 3, 4, 97, 6, 2, 1, 25.68, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (971, '8766b5c4-12bf-4fcc-8092-dca62de8d36f', 97, 5, 4, 7, 109, 6, 3, 1, 11.62, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (972, '02de435a-a215-4109-a193-f68903a3f5f6', 97, 5, 4, 6, 109, 6, 3, 1, 10.38, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (973, 'ee0ab6b5-1c95-4242-ae02-b63858a0a158', 97, 2, 1, 5, 41, 6, 2, 1, 36.72, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (974, 'ed2778c8-e23c-447d-9047-66c8ffc84d64', 97, 2, 1, 8, 41, 6, 3, 1, 17.28, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (975, 'e9f6d725-4a3d-4389-aea0-b79ae0404a06', 97, 2, 8, 4, 203, 4, 2, 1, 28.08, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (976, '741427da-a21f-45ec-ab6c-079a77ba8d11', 97, 2, 8, 8, 203, 4, 3, 1, 18.72, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (977, 'd15442c7-9631-442a-98b7-dcb1f0413190', 97, 2, 3, 28, 87, 6, 5, 1, 19.26, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (978, '4f3472ef-157b-4577-844b-820d60061a63', 97, 2, 3, 11, 87, 6, 3, 1, 11.77, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (979, '55aabb9c-bfd1-44e9-9d34-e810a0f86085', 97, 2, 3, 4, 87, 6, 2, 1, 25.68, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (980, '24a900b1-8fd0-4702-8f2f-423ef27e794c', 97, 2, 3, 1, 87, 6, 2, 1, 30.50, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (981, '8f09b694-ebb4-4d05-85db-90b7f10ce05c', 97, 2, 3, 6, 87, 6, 3, 1, 13.38, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (982, 'dfbb13fd-efd1-4fd6-9023-7585a14ee60d', 97, 2, 3, 23, 87, 6, 4, 1, 48.15, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (983, '82658c47-cfbd-436c-b3b7-2c3281712657', 97, 4, 7, 24, 88, 6, 4, 1, 47.52, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (984, '6dd9a799-0ad9-4ae6-b3f3-f23a5dab3179', 97, 4, 7, 11, 88, 6, 3, 1, 10.89, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (985, '083732a3-bad6-46d9-bf3f-16e1327188ef', 97, 4, 7, 20, 88, 6, 4, 1, 31.68, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (986, '9e31c36a-b3ce-417e-8b01-6e45d4a0f0e4', 97, 4, 7, 26, 88, 6, 4, 1, 41.58, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (987, 'b6c3ae46-d466-434e-af31-9e4118f1c959', 97, 4, 7, 2, 88, 6, 2, 1, 14.85, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (988, 'a6b37148-a116-4767-b687-71e6681d8bcb', 97, 2, 5, 28, 105, 4, 5, 1, 17.28, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (989, '4827222a-e1f8-474d-a489-8a4dc17e7315', 97, 2, 5, 15, 105, 4, 3, 1, 12.96, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (990, 'fe5bd550-2ba2-49d4-bf37-4b8c5314e5f0', 98, 3, 6, 23, 46, 6, 4, 1, 50.40, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (991, 'd6b48974-0a2a-4469-b40b-dfc3b5ed2633', 98, 3, 6, 6, 46, 6, 3, 1, 14.00, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (992, 'e40be780-8a92-40f3-a551-0112692fa84a', 98, 3, 6, 14, 46, 6, 3, 1, 15.12, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (993, '43f51ceb-cd8e-4d10-bfdc-1dd125068c58', 98, 3, 6, 28, 83, 6, 5, 1, 20.16, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (994, 'fdf585ae-3787-43ec-83ab-1f81dd434bd1', 98, 3, 6, 19, 83, 6, 4, 1, 42.56, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (995, '8258514d-ef80-445c-89e3-c9043134b6fd', 98, 3, 6, 8, 83, 6, 3, 1, 17.92, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (996, 'fdb9bd9d-06a5-44c0-9cf1-d0378f0a1ab2', 98, 3, 6, 13, 83, 6, 3, 1, 14.56, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (997, '45ad3bbf-4f90-401c-a1c1-4e9770db8976', 98, 3, 6, 4, 83, 6, 2, 1, 26.88, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (998, 'fbdca3be-a5ae-456b-910a-99ac12a60d91', 98, 3, 6, 20, 4, 4, 4, 1, 35.84, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (999, 'b25478d4-dda4-498f-a024-9f2cf8198b50', 98, 3, 6, 1, 4, 4, 2, 1, 31.92, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1000, '75b862bb-c3b8-4813-9e13-4e7780e8515f', 98, 3, 6, 26, 4, 4, 4, 1, 47.04, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1001, '13e25ecb-ef85-477e-804e-7ebeac6df2cc', 98, 3, 6, 9, 4, 4, 3, 1, 17.92, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1002, 'abbf8206-2642-4f7c-b13c-c1b9f32bfa59', 98, 3, 6, 19, 4, 4, 4, 1, 42.56, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1003, 'dde06c98-4652-4831-99d1-a12a9fc194d9', 98, 3, 8, 16, 169, 6, 3, 1, 19.89, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1004, '0a6bb0b2-6e9f-400d-b706-2f61d87b9797', 98, 3, 8, 19, 169, 6, 4, 1, 44.46, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1005, '282b208a-c549-4f4a-878f-08a844ec8d8a', 98, 3, 8, 9, 169, 6, 3, 1, 18.72, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1006, '37fd5081-fea5-4c7e-b099-fb3351049f4a', 98, 5, 7, 23, 15, 4, 4, 1, 44.55, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1007, '6ecfef87-b953-4d7c-bc9d-53af3c0099a0', 98, 5, 7, 29, 15, 4, 6, 1, 51.48, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1008, '040c9160-24d5-4140-8449-1443c18279c4', 98, 5, 7, 22, 15, 4, 4, 1, 61.38, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1009, 'baeb83ad-4f7c-408f-a83e-fb1445535d4d', 98, 5, 7, 8, 15, 4, 3, 1, 15.84, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1010, '08f1011d-ae0c-4272-816c-094cfca5ebe4', 98, 5, 7, 17, 15, 4, 3, 1, 16.34, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1011, '773f34fc-d57a-4931-b864-972455183e20', 98, 5, 7, 9, 15, 4, 3, 1, 15.84, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1012, '43a5f617-80db-45f0-a96e-cc97d9e42b09', 98, 5, 3, 30, 22, 6, 6, 1, 24.61, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1013, 'be95f78a-ae91-467d-b36e-6b67d95f169a', 98, 5, 3, 18, 22, 6, 3, 1, 20.33, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1014, '7125daae-7ae2-4466-8960-7d7290090c1b', 98, 5, 3, 17, 22, 6, 3, 1, 17.66, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1015, '69574b18-5407-44be-a823-3fde98bdd768', 99, 4, 6, 4, 97, 6, 2, 1, 26.88, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1016, '860919a4-5eff-4603-9d65-bb7943f347f3', 99, 4, 6, 18, 97, 6, 3, 1, 21.28, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1017, '2d096e76-ddae-4f62-aad3-e8cafc4ac541', 99, 4, 6, 6, 97, 6, 3, 1, 14.00, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1018, '7eef9725-baa2-4f67-8e16-101964f850ce', 97, 2, 5, 14, 105, 4, 3, 1, 12.96, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1019, '3c040bcb-67b2-432f-ac74-3c9271c16ff1', 97, 2, 5, 17, 105, 4, 3, 1, 15.84, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1020, '1be552e5-4d24-4d5f-928a-12cca6d3d986', 97, 2, 5, 21, 105, 4, 4, 1, 28.80, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1021, '4e64734c-fa88-40eb-af81-5da04d52fe3f', 97, 2, 8, 15, 203, 4, 3, 1, 15.80, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1022, 'aa4ba540-1705-4f9c-a8c4-db35c20ae515', 97, 2, 8, 9, 203, 4, 3, 1, 18.72, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1023, 'ebb60261-5101-4e5e-aeef-458fedd22790', 97, 2, 8, 10, 203, 4, 3, 1, 18.14, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1024, '5c2e3251-0921-4ed6-b85a-b546c0edf604', 97, 5, 4, 30, 23, 3, 6, 1, 19.09, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1025, '7ca65580-225e-445e-8a6c-f5f9ea53c175', 97, 5, 4, 8, 23, 3, 3, 1, 13.28, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1026, 'db3aef6f-5d22-496a-99ae-692282e8de63', 97, 5, 4, 11, 23, 3, 3, 1, 9.13, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1027, '8987c619-afd0-42f8-a47d-912d547fe074', 97, 4, 2, 23, 50, 1, 4, 1, 43.65, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1028, '73ff95a5-99bb-4bc2-a151-429b3f50c1ae', 97, 4, 2, 16, 50, 1, 3, 1, 16.49, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1029, '923f1063-7c87-4aa2-83df-022427e22f8e', 97, 4, 2, 17, 50, 1, 3, 1, 16.00, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1030, '6810b819-5b73-4eab-a31d-1a54a73d51c8', 97, 4, 2, 3, 50, 1, 2, 1, 21.34, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1031, '1d9de329-43ac-40e1-b9b4-9c34e597c5fd', 98, 5, 2, 27, 74, 5, 4, 1, 20.37, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1032, 'b77eadea-daaf-4ee5-9561-979f44372643', 98, 5, 2, 19, 74, 5, 4, 1, 36.86, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1033, '2a2c4069-22e3-48d1-a634-2d342e431f56', 98, 5, 2, 25, 74, 5, 4, 1, 25.22, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1034, 'f70c8a56-0e6f-416b-aecc-f9eb54fa707b', 99, 4, 6, 14, 97, 6, 3, 1, 15.12, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1035, '34b7e8c1-ca6a-4c3d-98bd-18ad57478351', 99, 4, 6, 24, 97, 6, 4, 1, 53.76, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1036, '1df57976-b260-4812-9853-f02bfacea8f1', 99, 4, 5, 24, 1, 3, 4, 1, 46.08, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1037, '056d9744-a122-4c07-b914-1eeb6073f4fd', 99, 4, 5, 29, 1, 3, 6, 1, 49.92, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1038, '74645c7a-8a6e-4a7b-8f68-e0017f97fb3c', 99, 4, 5, 21, 1, 3, 4, 1, 28.80, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1039, '5966cf09-8912-41a8-93f7-206140135232', 99, 4, 5, 17, 1, 3, 3, 1, 15.84, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1040, '082992fc-cde0-4111-a680-a68b15dbea89', 99, 4, 5, 13, 1, 3, 3, 1, 12.48, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1041, 'a2c38f87-c527-4740-8f7a-c0aca0192e21', 99, 4, 5, 28, 1, 3, 5, 1, 17.28, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1042, '2ce9b52b-b438-405a-ad54-016355c915b8', 99, 4, 5, 2, 177, 6, 2, 1, 14.40, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1043, 'bc0a9a08-c3f9-40b5-991c-7d094c0b2d14', 99, 4, 5, 18, 177, 6, 3, 1, 18.24, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1044, '59d90842-96cf-4c53-a480-354c12a6bda0', 99, 4, 5, 1, 177, 6, 2, 1, 27.36, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1045, 'c17407c3-1b6b-4adf-b4e5-6d32b1cc2e03', 99, 4, 5, 19, 177, 6, 4, 1, 36.48, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1046, 'dc6a5e23-b984-4d18-b048-f1633441d0e5', 99, 4, 8, 8, 52, 5, 3, 1, 18.72, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1047, 'd728bc80-8aab-4841-9571-c12c23fba949', 99, 4, 4, 14, 188, 5, 3, 1, 11.20, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1048, 'e17f3ace-a092-413c-9d3a-36df674ad95d', 99, 4, 4, 22, 188, 5, 4, 1, 51.46, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1049, 'cbe4a768-989c-4efa-adea-a2b77f5b5eb9', 99, 4, 4, 9, 188, 5, 3, 1, 13.28, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1050, '4ba1e8a3-8f4c-4d19-8516-9b04b78bc021', 99, 4, 4, 27, 188, 5, 4, 1, 17.43, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1051, '31c54f83-637d-4045-8904-d94e0dab9b3e', 99, 4, 4, 23, 188, 5, 4, 1, 37.35, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1052, '6036539b-cde1-4f85-a57f-078a8fb181e8', 99, 4, 4, 10, 188, 5, 3, 1, 12.86, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1053, '43e9b54e-d1c6-4b68-9f4f-d7766f00d337', 99, 4, 8, 29, 84, 6, 6, 1, 60.84, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1054, '46f129f7-150d-4140-a837-d68157b8b87f', 99, 4, 8, 21, 84, 6, 4, 1, 35.10, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1055, '40e56fe7-d789-4a33-b71f-f9c5257aeebc', 99, 4, 8, 3, 84, 6, 2, 1, 25.74, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1056, 'd4d7d898-51a5-4155-8aa3-85968dff23ef', 99, 4, 7, 26, 127, 4, 4, 1, 41.58, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1057, 'e9df2fdb-82ec-45d1-90a8-9b51554591ae', 99, 4, 7, 10, 127, 4, 3, 1, 15.34, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1058, 'a013c5c0-c56b-4b36-8881-972ce9833aa7', 99, 4, 7, 7, 127, 4, 3, 1, 13.86, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1059, 'af1e1fdb-4d39-4c2a-a847-8a6458958004', 99, 4, 7, 15, 127, 4, 3, 1, 13.36, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1060, 'a55d4995-6c5a-4a8d-a761-5c9cdf279382', 100, 4, 2, 1, 163, 1, 2, 1, 27.64, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1061, 'f8238c70-9111-4068-9a21-a43896548dc0', 100, 4, 2, 24, 163, 1, 4, 1, 46.56, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1062, '5675e951-f744-4e91-b0e3-5a1fa9bea330', 100, 4, 2, 16, 163, 1, 3, 1, 16.49, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1063, 'b81019e5-f079-4240-b50e-3d05b9bd1758', 100, 4, 2, 30, 163, 1, 6, 1, 22.31, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1064, '751108a8-6b4d-4753-b2c8-087ee5ed18ad', 100, 4, 2, 6, 163, 1, 3, 1, 12.12, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1065, '4c203447-f778-4f9a-a2fc-0f7d69a224f6', 100, 4, 6, 10, 59, 4, 3, 1, 17.36, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1066, '18d1c3f7-7ee2-4df7-8499-aeff9ef7cccc', 100, 4, 6, 15, 59, 4, 3, 1, 15.12, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1067, '56a87ef5-2d4d-4f12-bd89-2d6ec8be4f4c', 100, 4, 6, 22, 59, 4, 4, 1, 69.44, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1068, 'c825a8e7-a49f-4911-a394-e9c10a63cf1b', 100, 4, 6, 25, 59, 4, 4, 1, 29.12, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1069, 'ffe39e83-8c54-4975-8ec3-4fe53ada1c03', 100, 4, 6, 11, 59, 4, 3, 1, 12.32, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1070, 'e9163235-6308-4c36-b8bc-49150fde7664', 100, 4, 6, 20, 59, 4, 4, 1, 35.84, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1071, 'a08bb0b3-cbd6-47d9-8e86-bdf985e147d8', 100, 4, 7, 5, 3, 6, 2, 1, 33.66, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1072, '5699a385-bfc4-4a75-ae08-a6b69cad884a', 100, 4, 7, 25, 3, 6, 4, 1, 25.74, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1073, '01c3292e-3f8d-40f5-9b0e-262ae35be663', 100, 4, 8, 19, 140, 3, 4, 1, 44.46, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1074, '6b113452-dce9-443d-aea0-6382811453f4', 100, 4, 8, 7, 140, 3, 3, 1, 16.38, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1075, '47186155-2414-4a2a-b7ad-13c5a0d211df', 100, 4, 8, 1, 140, 3, 2, 1, 33.34, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1076, '0226a87b-b408-4a2c-9d0e-813badf24742', 100, 4, 7, 15, 177, 6, 3, 1, 13.36, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1077, '6186e636-dba8-4205-8e52-5e0ca4e82ed6', 100, 4, 7, 21, 177, 6, 4, 1, 29.70, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1078, '504ca012-154e-4d00-8fcf-bcc547a1d0f0', 100, 4, 7, 15, 49, 2, 3, 1, 13.36, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1079, 'fe2254d7-c434-4210-a2f0-1e61d9251f60', 100, 4, 7, 16, 49, 2, 3, 1, 16.83, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1080, 'ac376741-10d8-4c47-97a6-04af07ca3e40', 101, 2, 4, 11, 164, 6, 3, 1, 9.13, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1081, '0eaef01a-bbff-46da-80ee-da8015bb9456', 101, 2, 4, 4, 164, 6, 2, 1, 19.92, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1082, '7942cb2e-50a0-47a8-bee8-e272000f5d68', 101, 2, 3, 15, 32, 3, 3, 1, 14.44, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1083, '49bac61d-1779-4900-87e1-49466b998eed', 101, 2, 3, 28, 32, 3, 5, 1, 19.26, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1084, 'db276f41-4f21-4c15-9d24-8c173bd47bbc', 101, 2, 3, 12, 32, 3, 3, 1, 12.30, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1085, 'dba00c1d-ac69-406e-acc5-2798a0061427', 101, 2, 3, 23, 32, 3, 4, 1, 48.15, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1086, 'c5b4b588-fec1-4d95-ac94-1ab228635af6', 101, 2, 3, 22, 32, 3, 4, 1, 66.34, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1087, 'b2879a41-52ed-409f-a555-7790e56dba0e', 101, 2, 3, 25, 32, 3, 4, 1, 27.82, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1088, '4b75fd05-ab7c-41e0-87b4-804e8a03be52', 99, 4, 3, 17, 92, 1, 3, 1, 17.66, true, false);
INSERT INTO public.bi_fato_atendimento VALUES (1089, '5dca262b-dc7a-4d34-9efc-be7cb0b20b46', 99, 4, 3, 13, 92, 1, 3, 1, 13.91, true, false);
INSERT INTO public.bi_fato_atendimento VALUES (1090, '3ebd576a-97b1-4382-a807-e43ae5fbb094', 99, 4, 8, 2, 52, 5, 2, 1, 17.55, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1091, 'c9a272d9-88b5-405a-9c58-f1e0820acff7', 100, 4, 4, 10, 56, 4, 3, 1, 12.86, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1092, 'fd8bf965-3c07-49a5-8310-191fa3e12d73', 100, 4, 4, 15, 56, 4, 3, 1, 11.20, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1093, 'ef07f84b-72d8-411f-8277-e4ca44969c6c', 100, 4, 4, 27, 56, 4, 4, 1, 17.43, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1094, 'fd064762-7771-469e-a327-4d004463dad3', 100, 4, 5, 25, 33, 6, 4, 1, 24.96, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1095, 'd7e7488e-893f-4773-ba44-b0935bac8ae8', 100, 4, 5, 15, 33, 6, 3, 1, 12.96, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1096, 'e3562694-cd7a-492e-a9ea-b44967cf3b70', 100, 4, 5, 23, 33, 6, 4, 1, 43.20, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1097, 'f3452dc1-f9bb-4ae5-8db1-919651abdfb6', 101, 2, 7, 15, 100, 4, 3, 1, 13.36, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1098, 'ffeae691-5777-470e-a5d3-382497148cbc', 101, 2, 7, 24, 100, 4, 4, 1, 47.52, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1099, 'ff3455ce-87e6-4ce8-8ea3-a66f6adc6339', 101, 2, 7, 5, 100, 4, 2, 1, 33.66, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1100, 'e7f9a336-fa04-4c79-a2df-7e370ec61ed4', 101, 2, 6, 30, 205, 4, 6, 1, 25.76, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1101, 'd0691739-0114-4d63-a300-26925013b96b', 101, 2, 6, 23, 205, 4, 4, 1, 50.40, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1102, '65cdf7e2-3548-460b-ac65-3daef1b39756', 101, 2, 6, 2, 205, 4, 2, 1, 16.80, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1103, 'ecb57b7b-791f-4415-bc8b-d4b3d140551e', 101, 2, 6, 10, 205, 4, 3, 1, 17.36, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1104, '6b890a16-7e32-473c-8b2e-eaf2f876eaec', 101, 2, 6, 14, 205, 4, 3, 1, 15.12, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1105, '07c565e0-8b76-4cc3-9f0b-01c1219c2a2c', 101, 5, 7, 19, 109, 6, 4, 1, 37.62, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1106, '3c74116f-6d58-4477-b81a-78a916863d41', 101, 5, 7, 24, 109, 6, 4, 1, 47.52, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1107, 'bb39a729-be54-4f51-859c-1b2f4b3e0c4d', 101, 5, 7, 28, 109, 6, 5, 1, 17.82, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1108, 'c489d2fb-7a32-432b-84ae-7e90f51a9cc5', 101, 5, 4, 6, 135, 6, 3, 1, 10.38, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1109, '7a68fbc8-b34d-4275-9779-0d001fad8eab', 101, 5, 4, 21, 135, 6, 4, 1, 24.90, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1110, '818a699a-743c-4c08-be22-4719c9566ef5', 101, 5, 4, 17, 135, 6, 3, 1, 13.70, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1111, 'd79e3780-a756-4f64-821d-3bcde7188b7d', 101, 5, 4, 26, 135, 6, 4, 1, 34.86, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1112, '8dfc1b5a-a2a1-4ffc-876a-fd04aa89c015', 101, 5, 4, 12, 135, 6, 3, 1, 9.54, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1113, '989cd85d-031c-42ba-8a0b-127c852ad3bf', 101, 5, 4, 23, 135, 6, 4, 1, 37.35, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1114, 'a7ac2930-ddc4-4a82-90b3-2e4859084248', 101, 5, 6, 4, 1, 3, 2, 1, 26.88, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1115, '87ed1c16-7be8-496a-bea9-87f8106ef585', 101, 5, 6, 9, 1, 3, 3, 1, 17.92, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1116, '0cac945b-33a0-413a-a0df-5f4479a5f3e5', 101, 5, 6, 16, 1, 3, 3, 1, 19.04, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1117, 'f3985bc9-6c20-431b-b467-45fec9576e54', 101, 5, 6, 7, 1, 3, 3, 1, 15.68, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1118, '431edfaa-4ed0-4623-9db9-34a672b017e0', 101, 5, 6, 8, 1, 3, 3, 1, 17.92, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1119, 'bfe2cf1a-9112-4e64-bbc4-f20ce347d865', 101, 3, 4, 20, 86, 4, 4, 1, 26.56, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1120, '5601b546-e92f-442a-8da1-ce3fa7887c46', 101, 3, 4, 15, 86, 4, 3, 1, 11.20, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1121, '13398441-e581-4c69-a290-5f9af606babd', 101, 3, 4, 10, 86, 4, 3, 1, 12.86, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1122, 'c7a238c6-2698-4331-8d7e-79c8ca256592', 101, 3, 4, 5, 86, 4, 2, 1, 28.22, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1123, '860b6c69-8bdc-48ff-981c-a605bce1b75f', 101, 3, 4, 21, 86, 4, 4, 1, 24.90, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1124, '835df98a-45e3-4a64-9f9b-79b324f6cef9', 101, 5, 7, 29, 129, 6, 6, 1, 51.48, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1125, 'ff434bfa-5464-4ddf-9fc8-cea5779f83dd', 101, 5, 7, 20, 129, 6, 4, 1, 31.68, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1126, '44197b8b-553e-4c05-8176-e2d671ae9a8d', 101, 5, 7, 25, 129, 6, 4, 1, 25.74, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1127, 'fc58ead0-f14d-4b48-906d-1a9d632cb85b', 101, 5, 6, 16, 160, 4, 3, 1, 19.04, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1128, 'f4730844-98b0-4d08-9b46-b10e9c45518e', 101, 5, 6, 6, 160, 4, 3, 1, 14.00, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1129, 'a0471614-1bf5-4fcc-856a-67b7fa5163eb', 101, 5, 6, 18, 160, 4, 3, 1, 21.28, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1130, 'f3033227-2e42-42b9-9607-e04947cdf324', 101, 5, 6, 24, 160, 4, 4, 1, 53.76, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1131, 'cfe7ba4c-11ce-4079-9129-7c31c92a3e34', 101, 3, 3, 2, 19, 4, 2, 1, 16.05, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1132, '6726d8a6-9650-40e2-a938-c8a977bfe06e', 101, 3, 3, 17, 19, 4, 3, 1, 17.66, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1133, '2207e501-5ead-4b64-abe4-5e2d96dc9a32', 101, 3, 3, 28, 19, 4, 5, 1, 19.26, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1134, 'bd443656-d11d-41e3-a0f1-d1f0e40eabcb', 101, 3, 3, 22, 19, 4, 4, 1, 66.34, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1135, 'b5164952-b2f3-4226-88e2-0beb9b06d39c', 101, 3, 1, 17, 171, 1, 3, 1, 17.82, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1136, '30577d01-99d6-4aec-8f4a-5a6934bd9214', 101, 3, 1, 21, 171, 1, 4, 1, 32.40, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1137, 'fc2745cb-c665-497c-94d9-5790a830b658', 101, 5, 7, 2, 109, 6, 2, 1, 14.85, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1138, 'ea719157-2fa7-42d9-bb9c-9f69134f5585', 101, 5, 7, 8, 109, 6, 3, 1, 15.84, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1139, 'ec8cdbe7-ece4-49d3-bdee-2ddaf7012da4', 101, 5, 7, 30, 109, 6, 6, 1, 22.77, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1140, 'a7bad51a-9ec5-4e93-a286-2ee2c8098655', 101, 5, 2, 10, 110, 6, 3, 1, 15.04, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1141, '574e6a52-ba9c-4d99-83b9-ca972e33b8df', 101, 5, 2, 20, 110, 6, 4, 1, 31.04, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1142, '87db487c-77b5-49b5-af28-80de75aee6f4', 101, 5, 2, 12, 110, 6, 3, 1, 11.16, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1143, '1e34a1a3-f112-482a-9bf4-4ad6416cdff7', 101, 5, 1, 14, 123, 4, 3, 1, 14.58, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1144, 'ec417a4b-117e-4525-bcfa-20e8598fb5e9', 101, 5, 1, 27, 123, 4, 4, 1, 22.68, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1145, 'cbe5b679-46ed-4255-aba4-d44dc0e25816', 101, 5, 1, 25, 123, 4, 4, 1, 28.08, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1146, 'a669ad84-b4cb-4d05-bebd-b319bf2719dd', 101, 5, 1, 22, 123, 4, 4, 1, 66.96, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1147, 'b478a6ba-ebd3-4c16-8eef-237451be6725', 101, 2, 7, 10, 53, 4, 3, 1, 15.34, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1148, '43968e32-0958-4a1a-ad63-1c07d0607334', 101, 2, 7, 27, 53, 4, 4, 1, 20.79, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1149, '03b52130-e02d-47e7-94b1-47afde9e9015', 101, 2, 7, 15, 53, 4, 3, 1, 13.36, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1150, '1259af61-1b84-477a-a278-4e0074793e6e', 101, 3, 7, 25, 52, 5, 4, 1, 25.74, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1151, '1994aa1b-881e-44ed-8c1a-27f2da0685a3', 101, 3, 7, 20, 52, 5, 4, 1, 31.68, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1152, 'bfa781c1-a477-4cd9-ac4a-ee8dbd793c6f', 101, 3, 7, 6, 52, 5, 3, 1, 12.38, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1153, '3a685964-074b-406c-9e54-8511f8e44c07', 101, 3, 7, 27, 52, 5, 4, 1, 20.79, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1154, '2a23beff-d798-4977-9dc1-7509ef4e0ba2', 101, 3, 1, 1, 115, 6, 2, 1, 30.78, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1155, '031c48ec-7859-4613-a884-aa59f5556666', 101, 3, 1, 28, 115, 6, 5, 1, 19.44, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1156, '92f5db36-cf23-4800-8362-1f446a72050e', 101, 3, 1, 21, 115, 6, 4, 1, 32.40, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1157, 'bba9917d-4d84-4873-b188-074f4f588975', 101, 3, 1, 13, 115, 6, 3, 1, 14.04, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1158, '81029693-c98c-4853-ae85-da7b8c867a63', 101, 3, 1, 20, 115, 6, 4, 1, 34.56, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1159, '7815252a-3e1c-4f3c-b117-0210f79f5175', 102, 4, 6, 21, 57, 3, 4, 1, 33.60, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1160, 'c68e2e90-197c-4715-adc0-0739f1c051a4', 102, 4, 6, 16, 57, 3, 3, 1, 19.04, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1161, '4529777d-01ef-4a1b-85cf-97521ff77d46', 102, 4, 6, 13, 57, 3, 3, 1, 14.56, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1162, '2d4c00d8-ed7a-4337-975b-0475d290b4ab', 102, 4, 8, 21, 71, 3, 4, 1, 35.10, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1163, '13b789ba-a686-421b-93b1-2528c34b898d', 102, 4, 8, 2, 71, 3, 2, 1, 17.55, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1164, '1994e9cf-e079-49a2-b38b-98849e56e7e3', 102, 4, 8, 23, 109, 6, 4, 1, 52.65, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1165, '391fa0f8-9772-46d6-9b04-54fb71372522', 102, 4, 8, 8, 109, 6, 3, 1, 18.72, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1166, 'dfce3228-20b3-4c5f-a197-10b59a629793', 102, 4, 8, 20, 109, 6, 4, 1, 37.44, false, false);
INSERT INTO public.bi_fato_atendimento VALUES (1167, '17ebf679-b57d-4c6d-9187-ee0de88e9ce6', 27, 4, 2, 4, 176, 4, 2, 1, 23.28, true, false);
INSERT INTO public.bi_fato_atendimento VALUES (1168, '91d81d21-79b9-4acd-a503-99ab8241dd42', 27, 4, 2, 23, 176, 4, 4, 1, 43.65, true, false);
INSERT INTO public.bi_fato_atendimento VALUES (1169, '9c04db59-1d35-4f71-af33-db098fb4b29a', 27, 4, 2, 30, 176, 4, 6, 1, 22.31, true, false);
INSERT INTO public.bi_fato_atendimento VALUES (1170, 'b156af2c-fa60-4a72-a767-d9d949fbbc06', 27, 4, 2, 5, 176, 4, 2, 1, 32.98, true, false);
INSERT INTO public.bi_fato_atendimento VALUES (1171, '80002eee-5dbe-4aaf-ac93-08f80a5b9018', 33, 5, 8, 25, 210, 6, 4, 1, 30.42, true, false);
INSERT INTO public.bi_fato_atendimento VALUES (1172, '9db66b32-9ec1-4716-b2a6-a13f4434dcab', 33, 5, 8, 26, 210, 6, 4, 1, 49.14, true, false);
INSERT INTO public.bi_fato_atendimento VALUES (1173, 'b0dc758c-3ca5-4b27-98e8-2766ea9998ea', 33, 5, 8, 28, 210, 6, 5, 1, 21.06, true, false);
INSERT INTO public.bi_fato_atendimento VALUES (1174, 'be05bebb-6446-4f2f-8fcb-3a5374bd337e', 33, 5, 8, 12, 210, 6, 3, 1, 13.46, true, false);
INSERT INTO public.bi_fato_atendimento VALUES (1175, 'e0a6e758-29af-45f9-9db8-386141cfb28d', 33, 5, 8, 2, 210, 6, 2, 1, 17.55, true, false);
INSERT INTO public.bi_fato_atendimento VALUES (1176, '66450b7b-a1bb-424b-bfff-2aedd70634ba', 101, 5, 1, 19, 102, 3, 4, 1, 41.04, true, false);
INSERT INTO public.bi_fato_atendimento VALUES (1177, '99705194-f0b1-4c86-b426-7616982abd75', 101, 5, 1, 8, 102, 3, 3, 1, 17.28, true, false);
INSERT INTO public.bi_fato_atendimento VALUES (1178, 'cdcd23ff-8853-465c-a43a-4f6c9b1e57a3', 101, 5, 1, 16, 102, 3, 3, 1, 18.36, true, false);
INSERT INTO public.bi_fato_atendimento VALUES (1179, 'ed907cb3-a3a5-454a-88cc-cf75ec4d5075', 101, 5, 1, 28, 102, 3, 5, 1, 19.44, true, false);
INSERT INTO public.bi_fato_atendimento VALUES (1180, '59f0fa61-ad76-4e5b-ac98-4b78f5d003ae', 100, 4, 8, 5, 197, 6, 2, 1, 39.78, true, false);
INSERT INTO public.bi_fato_atendimento VALUES (1181, 'ce5e19d1-81f8-4341-9ec0-a5e129310e39', 100, 4, 8, 28, 197, 6, 5, 1, 21.06, true, false);
INSERT INTO public.bi_fato_atendimento VALUES (1182, '2122146e-3b3b-48f6-b453-ab545042e47e', 59, 2, 6, 12, 81, 5, 3, 1, 12.88, true, false);
INSERT INTO public.bi_fato_atendimento VALUES (1183, '9a59f3ac-b625-48bc-8918-842a84939df7', 59, 2, 6, 4, 81, 5, 2, 1, 26.88, true, false);
INSERT INTO public.bi_fato_atendimento VALUES (1184, 'e68b77c4-a244-43cf-8d1a-4c61eabfb5fc', 59, 2, 6, 14, 81, 5, 3, 1, 15.12, true, false);
INSERT INTO public.bi_fato_atendimento VALUES (1185, '20a91e60-6723-4742-92e2-079f3fb174de', 97, 2, 8, 10, 32, 3, 3, 1, 18.14, true, false);
INSERT INTO public.bi_fato_atendimento VALUES (1186, '44bde032-936d-4ea2-861c-a1bd4b1b7f76', 97, 2, 8, 21, 32, 3, 4, 1, 35.10, true, false);
INSERT INTO public.bi_fato_atendimento VALUES (1187, '4fae4708-d277-4cc1-b5c4-ef992f0ab3d4', 97, 2, 8, 14, 32, 3, 3, 1, 15.80, true, false);
INSERT INTO public.bi_fato_atendimento VALUES (1188, '53ff91b0-05a3-4344-9907-3c15d00b80cf', 97, 2, 8, 18, 32, 3, 3, 1, 22.23, true, false);
INSERT INTO public.bi_fato_atendimento VALUES (1189, '89faf08c-ad9b-44aa-b2cb-c281b3e19a06', 97, 2, 8, 9, 32, 3, 3, 1, 18.72, true, false);
INSERT INTO public.bi_fato_atendimento VALUES (1190, 'fbaf5283-f117-4f59-9509-6c685a3af29b', 97, 2, 8, 8, 32, 3, 3, 1, 18.72, true, false);
INSERT INTO public.bi_fato_atendimento VALUES (1191, '1a1590f4-f52d-4ec7-b2f1-170754bed382', 95, 5, 3, 19, 49, 2, 4, 1, 40.66, true, false);
INSERT INTO public.bi_fato_atendimento VALUES (1192, '2adabcd8-a2c5-47e6-bd40-55353f8300a0', 95, 5, 3, 7, 49, 2, 3, 1, 14.98, true, false);
INSERT INTO public.bi_fato_atendimento VALUES (1193, '79aeb9ea-018a-4ef8-9b49-4202f03b5fa1', 95, 5, 3, 15, 49, 2, 3, 1, 14.44, true, false);
INSERT INTO public.bi_fato_atendimento VALUES (1194, 'cc71d78e-916e-45a5-aa4e-a3dc169b8574', 95, 5, 3, 4, 49, 2, 2, 1, 25.68, true, false);
INSERT INTO public.bi_fato_atendimento VALUES (1195, 'cf9ae150-271b-471d-86d1-e04614f1559e', 95, 5, 3, 18, 49, 2, 3, 1, 20.33, true, false);
INSERT INTO public.bi_fato_atendimento VALUES (1196, 'd1df1168-17b4-4076-b9a2-a33f188d7ea3', 99, 4, 3, 21, 92, 1, 4, 1, 32.10, true, false);
INSERT INTO public.bi_fato_atendimento VALUES (1197, 'f0df427d-48b3-43de-9ca7-d8f9a9ea60ed', 99, 4, 3, 12, 92, 1, 3, 1, 12.30, true, false);
INSERT INTO public.bi_fato_atendimento VALUES (1198, '5c22ba9e-869e-46be-abf2-1a4fe6f322b8', 50, 4, 2, 23, 49, 2, 4, 1, 43.65, true, false);
INSERT INTO public.bi_fato_atendimento VALUES (1199, '95f473f9-34b3-4c98-a2ef-98c07d82214f', 50, 4, 2, 26, 49, 2, 4, 1, 40.74, true, false);
INSERT INTO public.bi_fato_atendimento VALUES (1200, 'c744c10e-586a-4f26-a321-5ed5380f49db', 94, 3, 8, 24, 160, 4, 4, 1, 56.16, true, false);
INSERT INTO public.bi_fato_atendimento VALUES (1201, 'cf4d1ab9-5353-4289-8b02-04d2a460b170', 94, 3, 8, 25, 160, 4, 4, 1, 30.42, true, false);
INSERT INTO public.bi_fato_atendimento VALUES (1202, 'abc6c213-1f8b-42ab-b002-972a01cf0c42', 66, 2, 6, 28, 188, 5, 5, 1, 20.16, true, false);
INSERT INTO public.bi_fato_atendimento VALUES (1203, 'b8d0786f-539b-4d4f-b157-b2267845161b', 66, 2, 6, 23, 188, 5, 4, 1, 50.40, true, false);
INSERT INTO public.bi_fato_atendimento VALUES (1204, 'b923ac1c-7a2f-4258-ae93-07d614270945', 66, 2, 6, 10, 188, 5, 3, 1, 17.36, true, false);
INSERT INTO public.bi_fato_atendimento VALUES (1205, '099d04b3-93b5-4f8a-846e-18ecb6a3d008', 92, 2, 5, 18, 177, 6, 3, 1, 18.24, true, false);
INSERT INTO public.bi_fato_atendimento VALUES (1206, '34cc6ea7-ed5e-4a56-9a73-4767a04f64f5', 92, 2, 5, 6, 177, 6, 3, 1, 12.00, true, false);
INSERT INTO public.bi_fato_atendimento VALUES (1207, '5c99ebf5-42ec-457e-80a1-32f80a673caf', 92, 2, 5, 29, 177, 6, 6, 1, 49.92, true, false);
INSERT INTO public.bi_fato_atendimento VALUES (1208, 'd2278bcb-e784-4478-b587-11b429ce1b70', 92, 2, 5, 5, 177, 6, 2, 1, 32.64, true, false);
INSERT INTO public.bi_fato_atendimento VALUES (1209, 'd9846333-c4e0-4cb7-a6f7-14c2dcfa9cdd', 92, 2, 5, 21, 177, 6, 4, 1, 28.80, true, false);
INSERT INTO public.bi_fato_atendimento VALUES (1210, 'e2cff1ef-f488-4670-ae54-2b44e68c4dcb', 92, 2, 5, 9, 177, 6, 3, 1, 15.36, true, false);
INSERT INTO public.bi_fato_atendimento VALUES (1211, '2ec52a64-9c86-47ab-a6f4-48aafbaab7f4', 78, 3, 8, 12, 54, 3, 3, 1, 13.46, true, false);
INSERT INTO public.bi_fato_atendimento VALUES (1212, 'b5b5a814-b49a-4842-8ef4-6b8ee64528ef', 78, 3, 8, 20, 54, 3, 4, 1, 37.44, true, false);
INSERT INTO public.bi_fato_atendimento VALUES (1213, 'c54d7cee-adad-4c1c-b011-6cc059f4d9a6', 78, 3, 8, 27, 54, 3, 4, 1, 24.57, true, false);
INSERT INTO public.bi_fato_atendimento VALUES (1214, 'f9b401a7-7b9f-4359-84be-da5a216a5382', 20, 4, 5, 22, 218, 6, 4, 1, 59.52, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1215, '80a3b9c3-2d85-4e81-b7f2-2c1e4c65e5cf', 102, 4, 4, 24, 56, 4, 4, 1, 39.84, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1216, '069ba612-bedf-4b90-9e13-631afa08a888', 102, 4, 4, 13, 56, 4, 3, 1, 10.79, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1217, '78a3fd74-5205-4fe2-9f26-07180ea29cf4', 102, 4, 5, 23, 114, 1, 4, 1, 43.20, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1218, '6e951064-f164-4845-a787-3991ae2fc19b', 102, 4, 5, 26, 114, 1, 4, 1, 40.32, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1219, 'd88218f2-5bfc-4ee1-b426-582ee3808d7a', 20, 4, 5, 27, 218, 6, 4, 1, 20.16, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1220, 'd3dd846b-cd67-4e71-a826-f687427db5f5', 20, 4, 5, 29, 218, 6, 6, 1, 49.92, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1221, '67b2abe0-c8b3-4ed0-8494-d586db1efb68', 20, 4, 5, 11, 218, 6, 3, 1, 10.56, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1222, '6f60412c-b271-4a54-a131-9652ebd21734', 20, 4, 5, 7, 218, 6, 3, 1, 13.44, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1223, '64ab6bc2-7b83-4f5e-9119-73ec2088a9c2', 17, 4, 5, 5, 14, 6, 2, 1, 32.64, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1224, 'a5c9f345-5ae1-4858-8e55-18e76b86d384', 17, 4, 2, 27, 88, 6, 4, 1, 20.37, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1225, '2e2d5a83-9db6-47da-b6f3-d187dcb8e39c', 17, 4, 7, 3, 206, 6, 2, 1, 21.78, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1226, '96266976-39a9-4e30-944b-06a4f6ad378b', 26, 5, 3, 6, 88, 6, 3, 1, 13.38, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1227, '099cdc52-4b07-4e4d-be02-49ac775f3be6', 16, 5, 5, 24, 191, 5, 4, 1, 46.08, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1228, 'd051df0a-89a5-423f-b4d4-e35ea90b751d', 16, 5, 5, 7, 191, 5, 3, 1, 13.44, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1229, '8308f0c8-ca0b-475f-8ba1-68e3b96f9254', 20, 5, 6, 10, 170, 2, 3, 1, 17.36, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1230, '16da912a-809c-4684-aba2-6e9fea318538', 20, 5, 6, 1, 170, 2, 2, 1, 31.92, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1231, 'c9838219-a070-41cb-ae52-789fe0723407', 28, 2, 2, 8, 16, 4, 3, 1, 15.52, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1232, '71d3bbf3-77b5-416c-9696-803a139caa62', 28, 2, 2, 22, 16, 4, 4, 1, 60.14, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1233, '0a380dc7-d85c-4e98-be94-f3ff2525807a', 28, 2, 2, 23, 16, 4, 4, 1, 43.65, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1234, 'f7ff2421-248a-4ece-9b78-98e283d0b924', 28, 2, 2, 14, 16, 4, 3, 1, 13.10, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1235, '896d58e6-a1a0-4f18-9309-6fe6f806a596', 28, 2, 2, 4, 16, 4, 2, 1, 23.28, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1236, '062e34ad-bbf5-47fa-909a-462294485603', 28, 2, 4, 29, 164, 6, 6, 1, 43.16, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1237, '9a64334f-2621-49bc-9c43-4f755bfd34cc', 30, 5, 5, 22, 10, 5, 4, 1, 59.52, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1238, '85382548-83bd-4fa3-a808-bb09b2bf67a2', 27, 5, 5, 6, 173, 6, 3, 1, 12.00, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1239, '17263573-c6a4-449f-bfe9-5998277ff819', 27, 5, 7, 24, 2, 4, 4, 1, 47.52, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1240, '92e03e87-da99-4c67-a2b7-5a8edbea5b55', 27, 5, 7, 19, 2, 4, 4, 1, 37.62, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1241, '39cc80d0-b55e-4c12-85c5-646b020e8961', 27, 5, 7, 4, 2, 4, 2, 1, 23.76, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1242, 'd1eff92d-b47e-4813-bbab-424490edf0ec', 27, 5, 7, 16, 2, 4, 3, 1, 16.83, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1243, 'df8f40f2-aae2-4d2c-8d1b-e341b7fc053f', 30, 2, 4, 5, 102, 3, 2, 1, 28.22, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1244, 'd67cb4ec-cc02-42bb-a3a8-e38b2c096541', 30, 2, 4, 18, 102, 3, 3, 1, 15.77, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1245, 'eb3abfa8-3571-4f60-9873-e8d721b2a9bd', 37, 3, 6, 26, 63, 4, 4, 1, 47.04, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1246, 'f10839c4-4348-4be6-ac26-a313eb34d303', 20, 3, 3, 2, 41, 6, 2, 1, 16.05, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1247, 'ff9278e7-b2f0-486b-8c98-f4433bbff2a1', 37, 3, 7, 19, 108, 6, 4, 1, 37.62, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1248, 'eea18af8-11ab-4cdf-9ad6-6fd7da69277c', 38, 2, 1, 27, 185, 1, 4, 1, 22.68, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1249, '9cd61b21-e7a1-4693-bd03-ecf793cfc943', 45, 2, 4, 9, 81, 5, 3, 1, 13.28, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1250, 'f8301b78-1ec0-425a-81a0-46bd84bad1dd', 45, 2, 4, 1, 81, 5, 2, 1, 23.66, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1251, '0002adaa-f994-48a4-b225-93d40d9e9dc2', 45, 2, 4, 10, 81, 5, 3, 1, 12.86, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1252, '02838188-57cb-462d-ae09-67d8d5258e2d', 45, 2, 4, 20, 81, 5, 4, 1, 26.56, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1253, '72bd2cee-dc20-4ca9-8193-ad073e5ed8a9', 45, 2, 4, 25, 81, 5, 4, 1, 21.58, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1254, 'b1da3f39-e261-4c29-9c98-6ceb7039854a', 45, 2, 4, 13, 81, 5, 3, 1, 10.79, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1255, 'ca65ee4a-fb58-465c-ab3d-8a7405e57555', 42, 2, 7, 2, 118, 4, 2, 1, 14.85, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1256, '213357b3-67a8-48d9-b985-9ded7bd16b2d', 46, 5, 5, 3, 194, 1, 2, 1, 21.12, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1257, '5996f437-f5b2-4812-9222-cad692e65940', 46, 5, 5, 7, 194, 1, 3, 1, 13.44, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1258, '507fd678-97e5-4ce4-b8f0-cf28f6d0c439', 46, 5, 5, 29, 194, 1, 6, 1, 49.92, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1259, 'fa49be88-7889-4d06-9e80-3c84859a249b', 46, 5, 5, 18, 194, 1, 3, 1, 18.24, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1260, '64b28605-8a20-4ece-990b-ff5772794dc6', 46, 5, 5, 13, 194, 1, 3, 1, 12.48, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1261, 'b9bbcc14-bfcc-4b5a-9df5-120446c21a47', 34, 4, 8, 20, 145, 3, 4, 1, 37.44, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1262, 'd3408e45-9a81-4b0b-9eb3-96df42a9397b', 34, 4, 8, 8, 145, 3, 3, 1, 18.72, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1263, '410ac567-6968-419d-afbd-0209ca135a96', 39, 3, 8, 18, 12, 5, 3, 1, 22.23, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1264, 'f5852c8f-5584-4326-89b1-969ad9a31890', 46, 2, 3, 19, 151, 6, 4, 1, 40.66, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1265, '021a02a1-9e11-49a1-9455-6e3d233c0a3a', 46, 2, 3, 12, 151, 6, 3, 1, 12.30, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1266, '0346a872-787e-4077-958b-d393cad1927a', 44, 5, 6, 5, 75, 4, 2, 1, 38.08, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1267, '52a6a16e-e702-4d03-ac2b-d77c8ef9b3ff', 55, 5, 1, 4, 73, 6, 2, 1, 25.92, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1268, 'f06e2c72-b0f7-4c34-bc37-4ba422115f7a', 55, 5, 1, 22, 73, 6, 4, 1, 66.96, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1269, 'f4fa349f-bb4a-4021-b3ec-e3c00f369306', 55, 5, 1, 13, 73, 6, 3, 1, 14.04, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1270, '201b012a-2b00-49e2-b169-32b2c4e8987c', 48, 4, 7, 17, 165, 6, 3, 1, 16.34, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1271, 'c3093853-1ed6-4b55-9476-e4cde170ce07', 46, 5, 1, 16, 205, 4, 3, 1, 18.36, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1272, '39136e64-11d8-45fc-b684-2e0f03f7c6d1', 46, 5, 1, 8, 205, 4, 3, 1, 17.28, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1273, 'af46b7cb-42e5-4d53-ae15-cdb00c59f089', 50, 5, 3, 5, 130, 6, 2, 1, 36.38, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1274, '7fa694f0-a06b-461e-a790-33f6b233d56d', 59, 2, 1, 20, 182, 4, 4, 1, 34.56, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1275, 'cf0bc3d1-1b72-4878-a386-5479b4b561f5', 57, 3, 6, 8, 73, 6, 3, 1, 17.92, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1276, '2320b919-e845-4889-b938-64f5ae4a9b77', 57, 3, 6, 11, 73, 6, 3, 1, 12.32, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1277, '633b21c2-cca1-47bb-8167-8d75626b2f05', 55, 3, 8, 17, 194, 1, 3, 1, 19.30, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1278, 'c56ac13c-d840-464f-b149-1aceba6d14f7', 55, 3, 8, 22, 194, 1, 4, 1, 72.54, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1279, '804993f0-db9e-446b-bae4-eae830c93f74', 60, 4, 8, 9, 154, 4, 3, 1, 18.72, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1280, '91441319-adb8-4c8b-bc51-7e2fa7920824', 65, 5, 2, 16, 181, 4, 3, 1, 16.49, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1281, 'be4e571c-12b5-46df-bc63-4e865204fe65', 65, 5, 2, 6, 181, 4, 3, 1, 12.12, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1282, '830161b2-5920-4664-829c-4def10daaa12', 65, 5, 2, 2, 181, 4, 2, 1, 14.55, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1283, '9d8fb995-edc0-4860-b1a2-4eb990e5ba63', 57, 5, 4, 29, 118, 4, 6, 1, 43.16, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1284, 'f4f3bdad-fe16-41b0-8666-b86760ceb41d', 57, 5, 4, 23, 118, 4, 4, 1, 37.35, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1285, 'bb563d84-4d7c-4869-8524-e4cbac756d33', 62, 3, 4, 3, 76, 2, 2, 1, 18.26, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1286, '7b0fc0fb-d428-4438-981e-ef4495c4f419', 62, 3, 4, 10, 76, 2, 3, 1, 12.86, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1287, '4ccc69a7-8e2d-49e8-81d2-5b6aa151b614', 69, 5, 6, 20, 60, 6, 4, 1, 35.84, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1288, '3d3bccf3-501f-4444-bb03-0206e3f568ff', 69, 5, 6, 24, 60, 6, 4, 1, 53.76, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1289, 'bd3c7b50-db10-47a5-bf93-4797afdf6eb3', 69, 5, 6, 1, 60, 6, 2, 1, 31.92, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1290, '6f78f2b9-f929-4fb5-9abf-90f153d52068', 69, 5, 6, 16, 168, 1, 3, 1, 19.04, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1291, '7413293e-ec67-438a-9eea-c9b2330cbd90', 69, 5, 6, 13, 168, 1, 3, 1, 14.56, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1292, 'c3ef82cf-2b5f-4b19-a115-6872dd098b3b', 69, 5, 6, 29, 168, 1, 6, 1, 58.24, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1293, '5d00f131-dd2b-46b4-8f5e-866c3fcc45b8', 71, 4, 7, 2, 13, 1, 2, 1, 14.85, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1294, '02f818f7-3acd-4dd8-9e1b-075493ca1197', 71, 4, 7, 18, 13, 1, 3, 1, 18.81, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1295, 'f5bc9cb6-3c77-470f-a47e-7da5a78f33f7', 71, 4, 7, 30, 13, 1, 6, 1, 22.77, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1296, '38e10284-93b6-497b-bb22-9a3bd8b2194d', 71, 4, 7, 5, 13, 1, 2, 1, 33.66, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1297, '15269dc6-1fdb-4046-9463-26ea5dd1df05', 70, 4, 7, 13, 138, 4, 3, 1, 12.87, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1298, 'ab9c1e92-31d8-453d-bb02-d4827dafc839', 71, 3, 2, 12, 149, 6, 3, 1, 11.16, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1299, '0756e7e0-23d1-497d-a5ec-15c4ff7e5e28', 71, 3, 2, 6, 149, 6, 3, 1, 12.12, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1300, '45f0237c-12a0-4d2c-8c30-f5df733333b9', 71, 3, 2, 2, 149, 6, 2, 1, 14.55, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1301, '2978ce4c-77eb-4de1-9751-5b2a1fbbb12a', 66, 2, 5, 1, 77, 6, 2, 1, 27.36, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1302, '24747635-6054-403d-b99a-56d7e1a2dc49', 86, 2, 3, 25, 136, 4, 4, 1, 27.82, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1303, '09bb9f9d-b11a-4be1-aa66-2b1ab34cb530', 86, 2, 3, 10, 136, 4, 3, 1, 16.58, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1304, 'abd1458d-3224-4407-a48b-fc133ca024fd', 86, 2, 3, 14, 136, 4, 3, 1, 14.44, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1305, 'e813cb88-8f74-4790-988a-b539a60b1e30', 86, 2, 3, 26, 136, 4, 4, 1, 44.94, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1306, 'eb7cac7c-d66f-4922-916b-41ec08310531', 75, 3, 7, 7, 47, 6, 3, 1, 13.86, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1307, '9fbcba9f-92f2-43d1-9f67-8368224ae9c8', 75, 3, 7, 3, 47, 6, 2, 1, 21.78, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1308, '8dfac5ee-2c6b-4391-8d22-2816239a368f', 75, 3, 7, 13, 47, 6, 3, 1, 12.87, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1309, '1a35623b-888f-4fea-b017-80798837bb9e', 75, 3, 3, 3, 40, 6, 2, 1, 23.54, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1310, 'e9dba189-fdf7-4b10-a6bb-0f0292e22d32', 86, 2, 2, 27, 214, 2, 4, 1, 20.37, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1311, '03e7eae8-6833-414d-94bf-aaff4a01346f', 86, 2, 2, 13, 214, 2, 3, 1, 12.61, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1312, '01f71334-c5d5-4ea6-a130-86a3fadc960c', 86, 2, 2, 15, 214, 2, 3, 1, 13.10, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1313, 'eb653cfa-9325-4696-98ee-1ec8303270ba', 77, 3, 2, 21, 121, 4, 4, 1, 29.10, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1314, '28ac03df-c009-4552-9eec-fb0486c9d261', 78, 3, 5, 14, 210, 6, 3, 1, 12.96, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1315, '75ca1546-d6b3-4da0-901f-192ce8f43029', 78, 3, 5, 6, 210, 6, 3, 1, 12.00, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1316, '6e199c07-9845-4528-9060-13a958aa712f', 78, 3, 5, 12, 210, 6, 3, 1, 11.04, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1317, '5cba3622-deea-4789-94ac-4b9a3bfb850e', 71, 4, 8, 21, 174, 5, 4, 1, 35.10, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1318, 'a73a07f1-1d0f-46fb-ae77-0ba170facb99', 82, 3, 6, 6, 90, 2, 3, 1, 14.00, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1319, '678ff9de-fd91-4c97-894e-1667706d3fa7', 82, 4, 1, 12, 143, 6, 3, 1, 12.42, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1320, '95ee4b28-b949-451b-b74f-ef395045d2f2', 82, 4, 1, 4, 143, 6, 2, 1, 25.92, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1321, '811ffd1b-4305-4087-b085-126c412e84e8', 85, 3, 6, 5, 74, 5, 2, 1, 38.08, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1322, '24ce8451-d71f-4bd8-ad3c-0e7570288be6', 87, 2, 7, 2, 18, 5, 2, 1, 14.85, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1323, '13e6f13b-d093-4734-b139-626a9d920f17', 87, 2, 7, 9, 18, 5, 3, 1, 15.84, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1324, '409234b4-17de-48b2-8330-4fc712398a7d', 93, 4, 1, 2, 205, 4, 2, 1, 16.20, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1325, '57bcd5f9-3122-49fd-8782-6c90d62d6136', 93, 4, 1, 13, 205, 4, 3, 1, 14.04, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1326, '712d6c15-2d9d-46f1-b280-a8ac9c3692d9', 93, 4, 1, 6, 205, 4, 3, 1, 13.50, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1327, 'd01e1945-36e6-413c-acdd-9d58dae6c058', 93, 4, 6, 17, 119, 5, 3, 1, 18.48, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1328, '20855dc7-181b-40ce-a38a-9df4d39e1e7d', 93, 4, 6, 21, 119, 5, 4, 1, 33.60, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1329, 'bb77bdee-a7b9-4ec6-8c23-706f691062e6', 93, 4, 1, 24, 81, 5, 4, 1, 51.84, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1330, '1cb3aa3b-b44b-48e2-b741-fb1e3d25ed38', 89, 5, 8, 8, 35, 1, 3, 1, 18.72, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1331, '39cda243-8c1e-4e15-90e8-0dac5aa82d17', 89, 5, 8, 16, 35, 1, 3, 1, 19.89, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1332, '3a2c89d1-2644-463c-838f-40daa4ff311d', 92, 2, 5, 15, 207, 4, 3, 1, 12.96, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1333, '727262e2-4d3f-4c6b-ab96-ac11451a9d42', 89, 3, 6, 3, 95, 6, 2, 1, 24.64, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1334, 'eea28f50-896c-474a-966d-a8ade56a1444', 95, 3, 1, 7, 216, 3, 3, 1, 15.12, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1335, 'b647aebe-198c-4ed6-a7f4-65f512a32691', 97, 4, 2, 22, 50, 1, 4, 1, 60.14, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1336, 'f96b896f-3249-4f78-83b6-a42d50b9e130', 101, 5, 2, 13, 110, 6, 3, 1, 12.61, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1337, 'b4b4d3ea-e7b3-4c6f-8e85-959188376265', 101, 2, 7, 30, 53, 4, 6, 1, 22.77, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1338, 'd87325f9-ddd0-45d0-b2c8-427fe9cf4610', 100, 4, 5, 26, 33, 6, 4, 1, 40.32, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1339, '09c50bf8-85e8-498f-8ef4-07e82fb0a6e8', 100, 4, 5, 19, 33, 6, 4, 1, 36.48, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1340, '9f9b53a7-2a9a-49e1-a72d-acc910f3a479', 100, 4, 5, 16, 33, 6, 3, 1, 16.32, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1341, '76384c2f-f17d-4769-bb2d-e85ab8520fe0', 101, 3, 7, 4, 52, 5, 2, 1, 23.76, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1342, '2352e5cb-9a05-4814-a071-1302a797a76d', 101, 3, 7, 17, 52, 5, 3, 1, 16.34, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1343, '2af01a92-1785-4701-b5ca-2edfb57a2272', 101, 3, 1, 3, 110, 6, 2, 1, 23.76, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1344, '1c1bb197-dc6e-48cd-8df1-280f796dccae', 101, 3, 1, 7, 110, 6, 3, 1, 15.12, false, true);
INSERT INTO public.bi_fato_atendimento VALUES (1345, '719beecb-9c19-4594-a11c-59fae4c8f1d4', 102, 4, 4, 19, 56, 4, 4, 1, 31.54, false, true);


--
-- Data for Name: bi_fato_faturamento; Type: TABLE DATA; Schema: public; Owner: labvida
--

INSERT INTO public.bi_fato_faturamento VALUES (1, 'b183ceb9-e41a-4996-ab27-781a2a7cdd05', 31, 4, 1, 18, 70, 3, 20.52, 0.00, 20.52, 1);
INSERT INTO public.bi_fato_faturamento VALUES (2, '47915520-1fff-450a-8398-a8e1bc0b23d6', 31, 4, 1, 6, 70, 3, 13.50, 0.00, 13.50, 1);
INSERT INTO public.bi_fato_faturamento VALUES (3, '84c9acdd-ffaa-4a50-9fa7-34cb455d5af1', 31, 4, 1, 24, 70, 4, 51.84, 0.00, 51.84, 1);
INSERT INTO public.bi_fato_faturamento VALUES (4, '7ddf9cb1-da3c-43a2-a013-d99beb4778be', 31, 4, 1, 12, 70, 3, 12.42, 0.00, 12.42, 1);
INSERT INTO public.bi_fato_faturamento VALUES (5, '14690e47-e562-43d8-8ff7-1f20f3fdc3f7', 34, 4, 5, 16, 14, 3, 16.32, 0.00, 16.32, 1);
INSERT INTO public.bi_fato_faturamento VALUES (6, 'b649887c-24ae-439f-bcc3-bb8c7d3e3efa', 34, 4, 5, 7, 14, 3, 13.44, 0.00, 13.44, 1);
INSERT INTO public.bi_fato_faturamento VALUES (7, '908d7cae-327f-4ee3-9523-a46e77065d00', 34, 4, 5, 17, 14, 3, 15.84, 0.00, 15.84, 1);
INSERT INTO public.bi_fato_faturamento VALUES (8, '5e11b924-0ff3-4382-a6e9-981c5bac9b60', 34, 4, 5, 4, 14, 2, 23.04, 0.00, 23.04, 1);
INSERT INTO public.bi_fato_faturamento VALUES (9, 'bb58aa9d-c70c-49a6-80b4-e15b19c68202', 33, 4, 7, 10, 206, 3, 15.34, 0.00, 15.34, 1);
INSERT INTO public.bi_fato_faturamento VALUES (10, '059bf514-fb9f-4a10-86b5-116b23b98467', 33, 4, 7, 11, 206, 3, 10.89, 5.44, 5.45, 1);
INSERT INTO public.bi_fato_faturamento VALUES (11, '3990c565-4edf-4ec5-8cda-3bf742b003bf', 33, 4, 7, 17, 206, 3, 16.34, 0.00, 16.34, 1);
INSERT INTO public.bi_fato_faturamento VALUES (12, 'eaf2851a-9d81-47e2-a948-fcdc32362444', 33, 4, 7, 21, 206, 4, 29.70, 0.00, 29.70, 1);
INSERT INTO public.bi_fato_faturamento VALUES (13, 'e0da05f9-0d78-44a6-96c7-8f4c784fb5d6', 33, 4, 7, 23, 206, 4, 44.55, 13.36, 31.19, 1);
INSERT INTO public.bi_fato_faturamento VALUES (14, '3d860b77-508c-4e13-9254-146111db8690', 32, 4, 6, 17, 186, 3, 18.48, 0.00, 18.48, 1);
INSERT INTO public.bi_fato_faturamento VALUES (15, '166d5fcf-6bf4-48b3-ac38-7fe4e8679ca2', 32, 4, 6, 22, 186, 4, 69.44, 0.00, 69.44, 1);
INSERT INTO public.bi_fato_faturamento VALUES (16, '469ca520-70a7-4d65-9486-5cb11af49774', 32, 3, 6, 30, 29, 6, 25.76, 0.00, 25.76, 1);
INSERT INTO public.bi_fato_faturamento VALUES (17, '1a2ded08-3f47-48a5-9c4f-38bc3f226a9c', 32, 3, 6, 9, 29, 3, 17.92, 0.00, 17.92, 1);
INSERT INTO public.bi_fato_faturamento VALUES (18, '37f8a387-a30c-4f48-999c-2e81a9476414', 19, 3, 8, 28, 16, 5, 21.06, 0.00, 21.06, 1);
INSERT INTO public.bi_fato_faturamento VALUES (19, 'e74eab72-70f4-4c58-bcc4-97b8c19e66a4', 19, 3, 8, 27, 16, 4, 24.57, 0.00, 24.57, 1);
INSERT INTO public.bi_fato_faturamento VALUES (20, 'e324c239-469b-42a1-b67e-8172d639ce97', 34, 5, 5, 12, 191, 3, 11.04, 0.00, 11.04, 1);
INSERT INTO public.bi_fato_faturamento VALUES (21, '706cd5a4-0715-47f3-9e4f-a7b88195bee3', 34, 5, 5, 2, 191, 2, 14.40, 0.00, 14.40, 1);
INSERT INTO public.bi_fato_faturamento VALUES (22, '2f679db9-f098-4fd7-96c1-e76129f03076', 34, 5, 5, 11, 191, 3, 10.56, 3.16, 7.40, 1);
INSERT INTO public.bi_fato_faturamento VALUES (23, 'bd7ac994-f021-4ef9-92be-f964157a42f0', 34, 5, 5, 4, 191, 2, 23.04, 0.00, 23.04, 1);
INSERT INTO public.bi_fato_faturamento VALUES (24, '51919f6f-e230-4dc8-bd5b-464a6bd19887', 31, 5, 1, 27, 200, 4, 22.68, 0.00, 22.68, 1);
INSERT INTO public.bi_fato_faturamento VALUES (25, 'e4dfbac9-5689-4c05-94b3-afb4a0f084d5', 31, 5, 1, 2, 200, 2, 16.20, 0.00, 16.20, 1);
INSERT INTO public.bi_fato_faturamento VALUES (26, '1de7e04e-89ad-4101-830a-b00c066175ef', 32, 5, 6, 11, 170, 3, 12.32, 0.00, 12.32, 1);
INSERT INTO public.bi_fato_faturamento VALUES (27, 'c696b91e-8c86-4010-a869-75f3fbd3675b', 32, 5, 6, 17, 170, 3, 18.48, 0.00, 18.48, 1);
INSERT INTO public.bi_fato_faturamento VALUES (28, '71600d96-5aca-4eaf-b345-143f7ca79457', 32, 5, 6, 12, 170, 3, 12.88, 0.00, 12.88, 1);
INSERT INTO public.bi_fato_faturamento VALUES (29, '1fb41375-96c9-4f1e-93e6-563d839a5fb0', 32, 5, 6, 14, 170, 3, 15.12, 0.00, 15.12, 1);
INSERT INTO public.bi_fato_faturamento VALUES (30, 'ddca761f-cc51-40bc-b64e-498dcb56c41e', 33, 5, 7, 1, 120, 2, 28.22, 28.22, 0.00, 1);
INSERT INTO public.bi_fato_faturamento VALUES (31, 'd5274dc0-a022-4936-bc82-4902bbb6262e', 33, 5, 7, 7, 120, 3, 13.86, 0.00, 13.86, 1);
INSERT INTO public.bi_fato_faturamento VALUES (32, '8853d8a3-cef9-41db-86e8-ff04775109f2', 34, 5, 4, 2, 152, 2, 12.45, 0.00, 12.45, 1);
INSERT INTO public.bi_fato_faturamento VALUES (33, '57618ba7-4fd7-46b0-a735-312f0b8de47a', 34, 5, 4, 27, 152, 4, 17.43, 0.00, 17.43, 1);
INSERT INTO public.bi_fato_faturamento VALUES (34, 'e9f5931b-f356-4df2-a996-b1ceea22bd35', 34, 5, 4, 17, 152, 3, 13.70, 0.00, 13.70, 1);
INSERT INTO public.bi_fato_faturamento VALUES (35, 'bc15f8a3-f1c8-4772-b197-aac4c318a1e9', 34, 5, 4, 24, 152, 4, 39.84, 11.95, 27.89, 1);
INSERT INTO public.bi_fato_faturamento VALUES (36, '46a94710-2156-42c5-aa7e-a40a1c0a14e5', 34, 5, 5, 19, 159, 4, 36.48, 0.00, 36.48, 1);
INSERT INTO public.bi_fato_faturamento VALUES (37, 'ecdaca75-af18-47ab-b4d5-7075b2c01353', 34, 5, 5, 27, 159, 4, 20.16, 0.00, 20.16, 1);
INSERT INTO public.bi_fato_faturamento VALUES (38, 'ac0c1244-71c8-485f-90dd-8e3643e3290e', 34, 5, 5, 28, 159, 5, 17.28, 0.00, 17.28, 1);
INSERT INTO public.bi_fato_faturamento VALUES (39, '54d687dc-7395-4e27-8dc0-46f8976f66f9', 34, 5, 4, 21, 109, 4, 24.90, 12.45, 12.45, 1);
INSERT INTO public.bi_fato_faturamento VALUES (40, 'dd87873f-d7ed-4a60-b393-8bd6486ae7a8', 34, 5, 4, 4, 109, 2, 19.92, 0.00, 19.92, 1);
INSERT INTO public.bi_fato_faturamento VALUES (41, 'fe42ac56-94f9-4073-8693-b2659935ceb2', 34, 5, 4, 11, 109, 3, 9.13, 0.00, 9.13, 1);
INSERT INTO public.bi_fato_faturamento VALUES (42, '835c43c0-04c7-4dd1-a1b4-a39c0cea7281', 34, 5, 4, 2, 109, 2, 12.45, 0.00, 12.45, 1);
INSERT INTO public.bi_fato_faturamento VALUES (43, '116244af-f11c-44fe-9f16-10c7fea8b248', 31, 5, 1, 15, 209, 3, 14.58, 14.58, 0.00, 1);
INSERT INTO public.bi_fato_faturamento VALUES (44, 'c4cdc4bb-c31c-4bad-9cb1-a0237a23d606', 31, 5, 1, 19, 209, 4, 41.04, 0.00, 41.04, 1);
INSERT INTO public.bi_fato_faturamento VALUES (45, 'f48d802a-f1fe-46a7-8471-7aff45936d28', 33, 5, 7, 5, 103, 2, 33.66, 0.00, 33.66, 1);
INSERT INTO public.bi_fato_faturamento VALUES (46, '58fd2c47-5af4-4a95-8874-3143edc00dc1', 33, 5, 7, 8, 103, 3, 15.84, 0.00, 15.84, 1);
INSERT INTO public.bi_fato_faturamento VALUES (47, 'd86a3143-10e0-492f-adb8-843e20c46f2c', 33, 5, 7, 26, 103, 4, 41.58, 0.00, 41.58, 1);
INSERT INTO public.bi_fato_faturamento VALUES (48, '56bc8e13-5d5d-42d9-be04-052c9b93c9c9', 34, 5, 4, 15, 58, 3, 11.20, 0.00, 11.20, 1);
INSERT INTO public.bi_fato_faturamento VALUES (49, 'e1ca3a70-484d-4ed5-a990-06668ca5828c', 34, 5, 4, 14, 58, 3, 11.20, 0.00, 11.20, 1);
INSERT INTO public.bi_fato_faturamento VALUES (50, 'eae967d0-b4ae-4aa1-bce8-7208ca1bb942', 33, 5, 7, 7, 165, 3, 13.86, 0.00, 13.86, 1);
INSERT INTO public.bi_fato_faturamento VALUES (51, '690d1feb-1792-4c4d-bf33-f7f79147b10a', 33, 5, 7, 3, 165, 2, 21.78, 0.00, 21.78, 1);
INSERT INTO public.bi_fato_faturamento VALUES (52, '0cd9fb22-2db8-49ce-8d38-8db69e601f28', 33, 5, 7, 27, 165, 4, 20.79, 20.79, 0.00, 1);
INSERT INTO public.bi_fato_faturamento VALUES (53, '5b1cafb1-92ba-47ed-8bab-179226d1df3b', 33, 5, 7, 9, 2, 3, 15.84, 0.00, 15.84, 1);
INSERT INTO public.bi_fato_faturamento VALUES (54, '4ab8e003-645a-40f6-90a3-d058092f3764', 33, 5, 7, 11, 2, 3, 10.89, 0.00, 10.89, 1);
INSERT INTO public.bi_fato_faturamento VALUES (55, 'fb19f1b3-a2e0-47e0-85fe-cc7bc545da70', 34, 2, 4, 14, 164, 3, 11.20, 0.00, 11.20, 1);
INSERT INTO public.bi_fato_faturamento VALUES (56, '0310bd61-1acb-4659-905a-0625cff781f7', 34, 2, 4, 19, 164, 4, 31.54, 0.00, 31.54, 1);
INSERT INTO public.bi_fato_faturamento VALUES (57, '29e34ebe-40e0-4197-b1b1-bb76a901aa55', 34, 2, 4, 24, 164, 4, 39.84, 0.00, 39.84, 1);
INSERT INTO public.bi_fato_faturamento VALUES (58, '335fcea1-ff4d-4e3b-b3ab-15ee4d153569', 34, 2, 4, 15, 164, 3, 11.20, 0.00, 11.20, 1);
INSERT INTO public.bi_fato_faturamento VALUES (59, '2378fc26-2eee-4794-b48a-629dc96b9b06', 32, 2, 6, 25, 213, 4, 29.12, 0.00, 29.12, 1);
INSERT INTO public.bi_fato_faturamento VALUES (60, '5a65f74b-db77-4529-88fe-e4d1fb80537b', 32, 2, 6, 13, 213, 3, 14.56, 0.00, 14.56, 1);
INSERT INTO public.bi_fato_faturamento VALUES (61, '1fe11055-145d-4a5e-b8a9-e4a1593cce62', 32, 2, 6, 2, 213, 2, 16.80, 16.80, 0.00, 1);
INSERT INTO public.bi_fato_faturamento VALUES (62, 'fcde517c-54c2-4284-a03c-0694a0d3228f', 32, 2, 6, 1, 213, 2, 31.92, 0.00, 31.92, 1);
INSERT INTO public.bi_fato_faturamento VALUES (63, '887b8f3c-34a5-44bd-8a54-305f6062da0d', 32, 2, 6, 19, 213, 4, 42.56, 0.00, 42.56, 1);
INSERT INTO public.bi_fato_faturamento VALUES (64, 'b66d08b5-d978-4067-b8d9-fa1a4195d59f', 34, 5, 5, 8, 10, 3, 15.36, 0.00, 15.36, 1);
INSERT INTO public.bi_fato_faturamento VALUES (65, '294d35fe-1a69-4c82-b7f4-d44bdad062c6', 34, 5, 5, 6, 10, 3, 12.00, 0.00, 12.00, 1);
INSERT INTO public.bi_fato_faturamento VALUES (66, '07944290-ed83-479f-b740-372d6b2c8d01', 34, 5, 5, 1, 10, 2, 27.36, 8.20, 19.16, 1);
INSERT INTO public.bi_fato_faturamento VALUES (67, '899ce71a-bd30-483b-a514-92a0b815b3f0', 34, 5, 5, 13, 10, 3, 12.48, 0.00, 12.48, 1);
INSERT INTO public.bi_fato_faturamento VALUES (68, 'd287e87c-1878-4ed0-9d23-4a5d8672a9e5', 33, 5, 7, 9, 113, 3, 15.84, 0.00, 15.84, 1);
INSERT INTO public.bi_fato_faturamento VALUES (69, 'e9c034ee-2812-45ae-a0e4-22aa1615278f', 33, 5, 7, 15, 113, 3, 13.36, 0.00, 13.36, 1);
INSERT INTO public.bi_fato_faturamento VALUES (70, '288b797b-9d0d-435b-9de0-eecad97120c8', 33, 5, 7, 18, 113, 3, 18.81, 18.81, 0.00, 1);
INSERT INTO public.bi_fato_faturamento VALUES (71, '89517670-3440-43fd-a5b5-d753b5920828', 34, 5, 5, 19, 173, 4, 36.48, 0.00, 36.48, 1);
INSERT INTO public.bi_fato_faturamento VALUES (72, '8f51151a-dfcc-4ce6-a5ee-18c5c8a758c2', 34, 5, 5, 17, 173, 3, 15.84, 0.00, 15.84, 1);
INSERT INTO public.bi_fato_faturamento VALUES (73, 'ec2e813d-f850-4449-9cfb-344eb458fc58', 34, 5, 5, 9, 173, 3, 15.36, 0.00, 15.36, 1);
INSERT INTO public.bi_fato_faturamento VALUES (74, 'eb20ce15-3f16-4ccd-83d4-9c7cf1ee1058', 34, 5, 5, 10, 173, 3, 14.88, 0.00, 14.88, 1);
INSERT INTO public.bi_fato_faturamento VALUES (75, 'b5180427-c201-4282-a472-f43c404a3bb2', 34, 5, 5, 23, 60, 4, 43.20, 0.00, 43.20, 1);
INSERT INTO public.bi_fato_faturamento VALUES (76, '930c954a-193d-4c21-ab4e-1e15374ec492', 34, 5, 5, 17, 60, 3, 15.84, 0.00, 15.84, 1);
INSERT INTO public.bi_fato_faturamento VALUES (77, 'db0862d9-605a-4245-9f96-d852f10983e0', 33, 5, 7, 15, 165, 3, 13.36, 0.00, 13.36, 1);
INSERT INTO public.bi_fato_faturamento VALUES (78, 'ffbff5e1-4957-42bf-a185-f89417a4b290', 33, 5, 7, 14, 165, 3, 13.36, 4.00, 9.36, 1);
INSERT INTO public.bi_fato_faturamento VALUES (79, '55c5a108-6672-4ed7-80d7-d151d226be3b', 34, 2, 4, 21, 102, 4, 24.90, 0.00, 24.90, 1);
INSERT INTO public.bi_fato_faturamento VALUES (80, '61cc6805-a314-4744-8341-0ea24d9a4658', 34, 2, 4, 29, 102, 6, 43.16, 0.00, 43.16, 1);
INSERT INTO public.bi_fato_faturamento VALUES (81, '4ee07d81-f2fe-4a68-96de-3bb34fa49002', 34, 2, 4, 2, 102, 2, 12.45, 0.00, 12.45, 1);
INSERT INTO public.bi_fato_faturamento VALUES (82, 'ff99fe6b-bac6-4e7c-8c2c-bc4a9fbdf09d', 34, 2, 4, 9, 102, 3, 13.28, 0.00, 13.28, 1);
INSERT INTO public.bi_fato_faturamento VALUES (83, 'e45ed40f-bfad-42d8-adbd-3219e7d480e4', 34, 5, 4, 24, 100, 4, 39.84, 0.00, 39.84, 1);
INSERT INTO public.bi_fato_faturamento VALUES (84, '92794f30-f136-453a-bce4-2dfb937d042b', 34, 5, 4, 11, 100, 3, 9.13, 4.56, 4.57, 1);
INSERT INTO public.bi_fato_faturamento VALUES (85, 'b48840fb-a09f-4883-9fbf-2fd62ceb11ef', 62, 4, 8, 20, 107, 4, 37.44, 0.00, 37.44, 1);
INSERT INTO public.bi_fato_faturamento VALUES (86, '47654533-76ba-4b8a-b535-8052d930cd0c', 62, 4, 8, 26, 107, 4, 49.14, 24.57, 24.57, 1);
INSERT INTO public.bi_fato_faturamento VALUES (87, 'cff4ba8e-d2aa-442d-9738-e539dac1c84a', 62, 4, 8, 14, 107, 3, 15.80, 0.00, 15.80, 1);
INSERT INTO public.bi_fato_faturamento VALUES (88, '320e0cb4-268c-43ad-abe6-a39a9e240579', 62, 4, 8, 27, 107, 4, 24.57, 0.00, 24.57, 1);
INSERT INTO public.bi_fato_faturamento VALUES (89, '29838958-711c-4e1b-96c3-15c0ce0eb5d9', 53, 3, 5, 20, 18, 4, 30.72, 0.00, 30.72, 1);
INSERT INTO public.bi_fato_faturamento VALUES (90, '8fd2e5e4-0b50-4b35-8b63-78ccff60a052', 53, 3, 5, 29, 18, 6, 49.92, 0.00, 49.92, 1);
INSERT INTO public.bi_fato_faturamento VALUES (91, '05e217c5-a330-4ba8-9208-738c2b35690c', 62, 3, 7, 30, 108, 6, 22.77, 0.00, 22.77, 1);
INSERT INTO public.bi_fato_faturamento VALUES (92, 'a4935bbf-1559-4cd2-8a7a-bfc5e04a6279', 62, 3, 7, 12, 108, 3, 11.38, 0.00, 11.38, 1);
INSERT INTO public.bi_fato_faturamento VALUES (93, 'a03fb8ab-7ab9-482e-9900-92ae31a8bf94', 62, 3, 7, 14, 108, 3, 13.36, 0.00, 13.36, 1);
INSERT INTO public.bi_fato_faturamento VALUES (94, '91b392e3-45df-4832-9e11-32f80a223c52', 62, 3, 7, 16, 108, 3, 16.83, 0.00, 16.83, 1);
INSERT INTO public.bi_fato_faturamento VALUES (95, '3aaa0d1a-dbe9-45d4-ab2e-28fa9129916d', 62, 3, 7, 21, 108, 4, 29.70, 0.00, 29.70, 1);
INSERT INTO public.bi_fato_faturamento VALUES (96, '45fa18c4-f07a-4e90-ada7-76a7a6af8f57', 62, 3, 8, 14, 212, 3, 15.80, 0.00, 15.80, 1);
INSERT INTO public.bi_fato_faturamento VALUES (97, 'd04825dc-303f-44a2-a41e-8f189659403e', 62, 3, 8, 13, 212, 3, 15.21, 0.00, 15.21, 1);
INSERT INTO public.bi_fato_faturamento VALUES (98, '0a6ddc63-8179-43a0-b7f9-2f1c8ec9ec08', 62, 3, 8, 18, 212, 3, 22.23, 0.00, 22.23, 1);
INSERT INTO public.bi_fato_faturamento VALUES (99, '47cb2904-e7f3-49a7-a79f-254d43bd5a08', 62, 3, 8, 25, 212, 4, 30.42, 0.00, 30.42, 1);
INSERT INTO public.bi_fato_faturamento VALUES (100, '1be78466-055f-496b-90a3-a9a72c513f2f', 64, 3, 3, 24, 76, 4, 51.36, 0.00, 51.36, 1);
INSERT INTO public.bi_fato_faturamento VALUES (101, '13995b7d-f762-47cc-ade2-eb6d8937a2cd', 64, 3, 3, 23, 76, 4, 48.15, 0.00, 48.15, 1);
INSERT INTO public.bi_fato_faturamento VALUES (102, '92d5894c-9035-4533-b4f7-507cd216b3bb', 64, 3, 3, 10, 76, 3, 16.58, 0.00, 16.58, 1);
INSERT INTO public.bi_fato_faturamento VALUES (103, '459230eb-a64b-49c4-8f01-1aaa4a9076ec', 64, 3, 3, 1, 76, 2, 30.50, 30.50, 0.00, 1);
INSERT INTO public.bi_fato_faturamento VALUES (104, '72625690-d33a-4ff9-9c64-da5fd81376bd', 64, 3, 3, 30, 76, 6, 24.61, 12.30, 12.31, 1);
INSERT INTO public.bi_fato_faturamento VALUES (105, 'a3f8a5df-3970-4fe7-a1bb-c44ebdc1e1fb', 59, 3, 4, 27, 54, 4, 17.43, 0.00, 17.43, 1);
INSERT INTO public.bi_fato_faturamento VALUES (106, '80803543-f686-49fd-91b2-c6b73a5ea8cf', 59, 3, 4, 9, 54, 3, 13.28, 0.00, 13.28, 1);
INSERT INTO public.bi_fato_faturamento VALUES (107, '49e494b5-e0ea-45fd-9b2f-be072e21755b', 59, 3, 4, 12, 54, 3, 9.54, 0.00, 9.54, 1);
INSERT INTO public.bi_fato_faturamento VALUES (108, 'f48154ab-25c4-438c-b837-07c46ebd8a6f', 59, 3, 4, 11, 54, 3, 9.13, 0.00, 9.13, 1);
INSERT INTO public.bi_fato_faturamento VALUES (109, '4e15bb87-0f7e-4db7-88e8-f703b40db236', 62, 2, 1, 15, 185, 3, 14.58, 0.00, 14.58, 1);
INSERT INTO public.bi_fato_faturamento VALUES (110, '9f932661-7ed6-477f-8485-bd9b1ba1bb66', 62, 2, 1, 11, 185, 3, 11.88, 0.00, 11.88, 1);
INSERT INTO public.bi_fato_faturamento VALUES (111, '37d2bcec-5f37-4d9a-9e0d-f39752c70060', 62, 2, 1, 17, 185, 3, 17.82, 0.00, 17.82, 1);
INSERT INTO public.bi_fato_faturamento VALUES (112, '3f8bf2bf-94f2-43c6-96ae-a39c0089b865', 62, 2, 1, 5, 185, 2, 36.72, 0.00, 36.72, 1);
INSERT INTO public.bi_fato_faturamento VALUES (113, '273212f8-ebda-4228-bcef-5449718b2d74', 62, 5, 7, 4, 143, 2, 23.76, 23.76, 0.00, 1);
INSERT INTO public.bi_fato_faturamento VALUES (114, 'a8eeca11-07c2-45db-a87b-c7a5b23e03ae', 62, 5, 7, 16, 143, 3, 16.83, 0.00, 16.83, 1);
INSERT INTO public.bi_fato_faturamento VALUES (115, '311191b0-2f72-473a-9b2a-8287b0e539fe', 62, 5, 7, 25, 143, 4, 25.74, 0.00, 25.74, 1);
INSERT INTO public.bi_fato_faturamento VALUES (116, '7c1db2d6-214e-4d27-aed1-210c28c89152', 62, 4, 8, 7, 145, 3, 16.38, 0.00, 16.38, 1);
INSERT INTO public.bi_fato_faturamento VALUES (117, '8e7706a4-e1ec-4ff3-963b-d6cdb812cd1f', 62, 4, 8, 24, 145, 4, 56.16, 0.00, 56.16, 1);
INSERT INTO public.bi_fato_faturamento VALUES (118, 'a579dc39-7a20-467c-a310-d67600cfd04a', 62, 4, 8, 13, 145, 3, 15.21, 0.00, 15.21, 1);
INSERT INTO public.bi_fato_faturamento VALUES (119, '7ae97584-7c4a-4c4e-8b7f-cad783d208e6', 62, 4, 8, 11, 145, 3, 12.87, 0.00, 12.87, 1);
INSERT INTO public.bi_fato_faturamento VALUES (120, '8ad761bd-8a20-43dd-a5a2-b5be316245c9', 59, 3, 4, 28, 177, 5, 14.94, 0.00, 14.94, 1);
INSERT INTO public.bi_fato_faturamento VALUES (121, 'c6a268f7-d579-4854-a9d6-f9ed5546685e', 59, 3, 4, 11, 177, 3, 9.13, 0.00, 9.13, 1);
INSERT INTO public.bi_fato_faturamento VALUES (122, '826029de-3446-47cd-adc1-7ec9dc381b13', 62, 2, 7, 10, 95, 3, 15.34, 0.00, 15.34, 1);
INSERT INTO public.bi_fato_faturamento VALUES (123, 'f0567daf-390e-4177-aea6-6fcd54b9f949', 62, 2, 7, 25, 95, 4, 25.74, 0.00, 25.74, 1);
INSERT INTO public.bi_fato_faturamento VALUES (124, '9b3cb3f1-7260-4bdc-a1ab-59f02384bcf0', 62, 2, 7, 3, 95, 2, 21.78, 0.00, 21.78, 1);
INSERT INTO public.bi_fato_faturamento VALUES (125, '3a6f4686-5c53-4bbf-b688-d6ce1fa0878c', 62, 2, 7, 1, 95, 2, 28.22, 0.00, 28.22, 1);
INSERT INTO public.bi_fato_faturamento VALUES (126, '4592e7ba-c21e-4f5f-a158-9a7bd1c4e97c', 62, 2, 7, 13, 118, 3, 12.87, 0.00, 12.87, 1);
INSERT INTO public.bi_fato_faturamento VALUES (127, '95e5fdec-d08b-4c28-8662-aa49a9103dad', 62, 2, 7, 25, 118, 4, 25.74, 0.00, 25.74, 1);
INSERT INTO public.bi_fato_faturamento VALUES (128, '1a37c714-0353-4ef1-a101-b03cf5fc9bfe', 62, 2, 7, 4, 118, 2, 23.76, 23.76, 0.00, 1);
INSERT INTO public.bi_fato_faturamento VALUES (129, '52780bc7-4345-4363-a153-879f8fea1eca', 62, 2, 7, 17, 118, 3, 16.34, 16.34, 0.00, 1);
INSERT INTO public.bi_fato_faturamento VALUES (130, 'd31d147d-87cf-4d59-be8a-b0678dc24417', 62, 2, 7, 21, 118, 4, 29.70, 0.00, 29.70, 1);
INSERT INTO public.bi_fato_faturamento VALUES (131, '38197d8f-320b-4a22-bc01-3e5e8693cf68', 59, 2, 4, 5, 53, 2, 28.22, 0.00, 28.22, 1);
INSERT INTO public.bi_fato_faturamento VALUES (132, 'b622dcb0-f147-4cf2-a0c4-70fbe266ea29', 59, 2, 4, 29, 53, 6, 43.16, 0.00, 43.16, 1);
INSERT INTO public.bi_fato_faturamento VALUES (133, 'db6c795f-bb72-4080-9b29-39f49866adcf', 59, 2, 4, 27, 53, 4, 17.43, 0.00, 17.43, 1);
INSERT INTO public.bi_fato_faturamento VALUES (134, 'bad9859a-b725-4ef3-8fc3-3fc0cc686d54', 62, 3, 8, 3, 12, 2, 25.74, 0.00, 25.74, 1);
INSERT INTO public.bi_fato_faturamento VALUES (135, '75df1509-cd49-4c33-91f6-833f3ea51714', 62, 3, 8, 9, 12, 3, 18.72, 0.00, 18.72, 1);
INSERT INTO public.bi_fato_faturamento VALUES (136, 'ac731d33-3d2d-4cdc-a637-f8c5264e3e75', 62, 3, 8, 20, 12, 4, 37.44, 0.00, 37.44, 1);
INSERT INTO public.bi_fato_faturamento VALUES (137, '25a7cde9-e894-4dfb-adf7-1540253e220b', 62, 3, 8, 12, 12, 3, 13.46, 0.00, 13.46, 1);
INSERT INTO public.bi_fato_faturamento VALUES (138, 'b919d5f1-1d85-4bfc-b4fc-f7082cfcc78d', 62, 3, 8, 11, 12, 3, 12.87, 6.43, 6.44, 1);
INSERT INTO public.bi_fato_faturamento VALUES (139, '00620f69-d455-4215-989d-3d2479d703e7', 53, 2, 5, 10, 54, 3, 14.88, 0.00, 14.88, 1);
INSERT INTO public.bi_fato_faturamento VALUES (140, 'b53b27f9-d923-4c44-a10d-47546c25cf3c', 53, 2, 5, 18, 54, 3, 18.24, 0.00, 18.24, 1);
INSERT INTO public.bi_fato_faturamento VALUES (141, '786f310c-3875-485c-822d-61f3a227adf2', 53, 2, 5, 23, 54, 4, 43.20, 0.00, 43.20, 1);
INSERT INTO public.bi_fato_faturamento VALUES (142, 'ad7193f8-a6e6-4bb5-8840-ee480eec1897', 53, 2, 5, 13, 54, 3, 12.48, 0.00, 12.48, 1);
INSERT INTO public.bi_fato_faturamento VALUES (143, '7e425bea-7293-492a-96df-31b99370f144', 64, 2, 3, 26, 151, 4, 44.94, 0.00, 44.94, 1);
INSERT INTO public.bi_fato_faturamento VALUES (144, '6a0bea2b-b4ab-4d17-a35c-35297db44711', 64, 2, 3, 5, 151, 2, 36.38, 0.00, 36.38, 1);
INSERT INTO public.bi_fato_faturamento VALUES (145, 'bf7451c3-3804-47ee-9d88-3aafb59e25ed', 64, 2, 3, 15, 151, 3, 14.44, 14.44, 0.00, 1);
INSERT INTO public.bi_fato_faturamento VALUES (146, 'faaf783e-3e6e-4020-ae8c-d07693c10df5', 64, 2, 3, 18, 151, 3, 20.33, 0.00, 20.33, 1);
INSERT INTO public.bi_fato_faturamento VALUES (147, '25e41b3b-f45d-4470-b201-a67d44375f94', 62, 3, 7, 3, 73, 2, 21.78, 0.00, 21.78, 1);
INSERT INTO public.bi_fato_faturamento VALUES (148, '482d3621-6767-4600-82ab-8b66e8111f0a', 62, 3, 7, 18, 73, 3, 18.81, 0.00, 18.81, 1);
INSERT INTO public.bi_fato_faturamento VALUES (149, '98e1a8b9-74dd-47fc-81d7-1bc9b6393e8c', 62, 3, 7, 17, 73, 3, 16.34, 0.00, 16.34, 1);
INSERT INTO public.bi_fato_faturamento VALUES (150, '897e8a50-d05c-496f-8f6c-bf30b5078d2a', 62, 3, 7, 27, 73, 4, 20.79, 0.00, 20.79, 1);
INSERT INTO public.bi_fato_faturamento VALUES (151, 'c5da3158-a03e-4783-a2ef-879e5fafe049', 62, 3, 7, 21, 73, 4, 29.70, 14.85, 14.85, 1);
INSERT INTO public.bi_fato_faturamento VALUES (152, 'a627322a-6a2e-49ea-b347-5c5ee8c365e0', 62, 4, 7, 13, 165, 3, 12.87, 0.00, 12.87, 1);
INSERT INTO public.bi_fato_faturamento VALUES (153, 'c836f1da-0ea8-4a5d-a0d9-d7f1ce59771d', 62, 4, 7, 14, 165, 3, 13.36, 0.00, 13.36, 1);
INSERT INTO public.bi_fato_faturamento VALUES (154, '3c9fa656-421b-49ff-8903-232216fadffd', 62, 4, 7, 22, 165, 4, 61.38, 0.00, 61.38, 1);
INSERT INTO public.bi_fato_faturamento VALUES (155, '09f09d37-1820-4542-8d57-934b22790fff', 62, 4, 7, 9, 165, 3, 15.84, 0.00, 15.84, 1);
INSERT INTO public.bi_fato_faturamento VALUES (156, '7913ba0d-7ef9-43ac-ab07-2f1d7cb77ff7', 62, 4, 7, 16, 165, 3, 16.83, 16.83, 0.00, 1);
INSERT INTO public.bi_fato_faturamento VALUES (157, '0354e5d4-e5ec-4ecf-8232-14047219369b', 62, 4, 8, 9, 114, 3, 18.72, 0.00, 18.72, 1);
INSERT INTO public.bi_fato_faturamento VALUES (158, 'f1963f41-1bca-4f0f-8aba-64d2927746e6', 62, 4, 8, 8, 114, 3, 18.72, 0.00, 18.72, 1);
INSERT INTO public.bi_fato_faturamento VALUES (159, '52494924-dfec-4dab-9b02-d5be1f1ef14e', 62, 4, 8, 10, 114, 3, 18.14, 0.00, 18.14, 1);
INSERT INTO public.bi_fato_faturamento VALUES (160, 'd918ba20-bc89-4bcf-a221-54ed9538e29f', 62, 4, 8, 16, 114, 3, 19.89, 0.00, 19.89, 1);
INSERT INTO public.bi_fato_faturamento VALUES (161, 'bd703e28-7a7f-42db-a88b-1c51f1673822', 53, 4, 5, 4, 25, 2, 23.04, 0.00, 23.04, 1);
INSERT INTO public.bi_fato_faturamento VALUES (162, '746f677e-c0dc-4936-bbc8-42dd53e0ac4f', 53, 4, 5, 25, 25, 4, 24.96, 0.00, 24.96, 1);
INSERT INTO public.bi_fato_faturamento VALUES (163, 'afa3fbcf-97d0-4288-9230-633472a57d41', 53, 4, 5, 16, 25, 3, 16.32, 0.00, 16.32, 1);
INSERT INTO public.bi_fato_faturamento VALUES (164, '546972b4-ed78-4ccd-b912-1e8a011e7399', 62, 5, 1, 26, 205, 4, 45.36, 0.00, 45.36, 1);
INSERT INTO public.bi_fato_faturamento VALUES (165, 'c66c78d8-a6ce-4223-baa4-86e7c5aa51a3', 62, 5, 1, 3, 205, 2, 23.76, 23.76, 0.00, 1);
INSERT INTO public.bi_fato_faturamento VALUES (166, '485e12ed-db90-4565-b26d-424515e76fcd', 62, 5, 1, 6, 205, 3, 13.50, 0.00, 13.50, 1);
INSERT INTO public.bi_fato_faturamento VALUES (167, 'cc128084-6e3c-4eec-9ec4-2a0d0883ada1', 62, 5, 1, 11, 205, 3, 11.88, 0.00, 11.88, 1);
INSERT INTO public.bi_fato_faturamento VALUES (168, 'dfb7c0f1-4011-43c9-8810-e6d06961c8f4', 59, 5, 4, 12, 61, 3, 9.54, 0.00, 9.54, 1);
INSERT INTO public.bi_fato_faturamento VALUES (169, 'e4f24ed2-5811-42c2-b645-72ec773d3b90', 59, 5, 4, 1, 61, 2, 23.66, 0.00, 23.66, 1);
INSERT INTO public.bi_fato_faturamento VALUES (170, '49cb5246-3d6a-4980-931c-d5bc18942837', 53, 2, 5, 26, 54, 4, 40.32, 0.00, 40.32, 1);
INSERT INTO public.bi_fato_faturamento VALUES (171, '00f83e36-42a9-4592-ae97-896ba99ae1c7', 53, 2, 5, 24, 54, 4, 46.08, 0.00, 46.08, 1);
INSERT INTO public.bi_fato_faturamento VALUES (172, '39754809-e3cf-4897-8e90-f0c9a55d80b8', 53, 2, 5, 22, 124, 4, 59.52, 0.00, 59.52, 1);
INSERT INTO public.bi_fato_faturamento VALUES (173, 'c309d0e8-6186-44f1-9cd6-8ee258fdfa28', 53, 2, 5, 7, 124, 3, 13.44, 0.00, 13.44, 1);
INSERT INTO public.bi_fato_faturamento VALUES (174, '969e4f26-6833-434e-a1f9-9fb951ec3c1b', 53, 2, 5, 6, 124, 3, 12.00, 0.00, 12.00, 1);
INSERT INTO public.bi_fato_faturamento VALUES (175, '9d79c774-edfb-40ad-a291-697118fc3092', 53, 2, 5, 10, 124, 3, 14.88, 0.00, 14.88, 1);
INSERT INTO public.bi_fato_faturamento VALUES (176, '6736c399-b1ef-4587-8aed-03ff0564e334', 53, 2, 5, 27, 124, 4, 20.16, 0.00, 20.16, 1);
INSERT INTO public.bi_fato_faturamento VALUES (177, 'c55024c5-65d1-4cb2-8b24-efd54fc57f50', 62, 5, 1, 10, 73, 3, 16.74, 5.02, 11.72, 1);
INSERT INTO public.bi_fato_faturamento VALUES (178, '3a37e50a-cd1e-4dde-9db6-7059f45d6002', 62, 5, 1, 1, 73, 2, 30.78, 0.00, 30.78, 1);
INSERT INTO public.bi_fato_faturamento VALUES (179, '6ea0c635-0c21-48d1-9253-326a84a08e70', 62, 5, 1, 13, 73, 3, 14.04, 0.00, 14.04, 1);
INSERT INTO public.bi_fato_faturamento VALUES (180, '9e8c20ab-6d0f-43c5-914e-02b63a3b5cda', 62, 5, 1, 4, 73, 2, 25.92, 12.96, 12.96, 1);
INSERT INTO public.bi_fato_faturamento VALUES (181, '416e494c-22dd-446f-bbfe-cdf92260a7af', 62, 5, 7, 14, 57, 3, 13.36, 0.00, 13.36, 1);
INSERT INTO public.bi_fato_faturamento VALUES (182, '069aaded-cc5a-432b-b11b-d7ebffe8e17a', 62, 5, 7, 28, 57, 5, 17.82, 0.00, 17.82, 1);
INSERT INTO public.bi_fato_faturamento VALUES (183, 'e2ecee20-d601-4dbf-8a99-a4ad4e4843c2', 62, 5, 7, 26, 57, 4, 41.58, 0.00, 41.58, 1);
INSERT INTO public.bi_fato_faturamento VALUES (184, '57475909-3504-4421-837e-f463bde941f5', 62, 5, 7, 18, 57, 3, 18.81, 0.00, 18.81, 1);
INSERT INTO public.bi_fato_faturamento VALUES (185, 'f85f74c2-40df-41ae-89d3-9e5a78ed675e', 64, 5, 3, 22, 130, 4, 66.34, 0.00, 66.34, 1);
INSERT INTO public.bi_fato_faturamento VALUES (186, 'ed9d2c23-0e4c-44a4-8bca-b2d75c665eeb', 64, 5, 3, 24, 130, 4, 51.36, 0.00, 51.36, 1);
INSERT INTO public.bi_fato_faturamento VALUES (187, 'fa42367f-c3fb-4f5e-a033-c42a4c7c97bb', 64, 5, 3, 15, 130, 3, 14.44, 14.44, 0.00, 1);
INSERT INTO public.bi_fato_faturamento VALUES (188, '69481262-c174-4eb9-a087-384d32903aa5', 64, 5, 3, 30, 130, 6, 24.61, 0.00, 24.61, 1);
INSERT INTO public.bi_fato_faturamento VALUES (189, 'c212ee5e-1be4-4c4b-8d47-06522bea4ea7', 53, 5, 5, 24, 77, 4, 46.08, 0.00, 46.08, 1);
INSERT INTO public.bi_fato_faturamento VALUES (190, '3037ecf7-37fa-4e9d-be7b-e688022873d8', 53, 5, 5, 3, 77, 2, 21.12, 0.00, 21.12, 1);
INSERT INTO public.bi_fato_faturamento VALUES (191, '1d139a56-8e19-48ba-aba4-f33df0cb4ece', 53, 5, 5, 5, 77, 2, 32.64, 16.32, 16.32, 1);
INSERT INTO public.bi_fato_faturamento VALUES (192, '4b21f3b7-e814-4eca-924b-d51ac3a856a2', 62, 3, 8, 12, 58, 3, 13.46, 0.00, 13.46, 1);
INSERT INTO public.bi_fato_faturamento VALUES (193, 'd7825d9a-ab45-48e2-b6cf-6deda6e97deb', 62, 3, 8, 19, 194, 4, 44.46, 0.00, 44.46, 1);
INSERT INTO public.bi_fato_faturamento VALUES (194, '622d34eb-38cd-4e19-8c64-aa0305fb5cd5', 62, 3, 8, 6, 194, 3, 14.62, 0.00, 14.62, 1);
INSERT INTO public.bi_fato_faturamento VALUES (195, 'e2ae55db-572e-4d46-b017-adcc53f2a31f', 62, 3, 8, 3, 194, 2, 25.74, 0.00, 25.74, 1);
INSERT INTO public.bi_fato_faturamento VALUES (196, '9d358c4c-cfe6-4582-8ed2-2e754f66a8e5', 64, 3, 3, 12, 156, 3, 12.30, 0.00, 12.30, 1);
INSERT INTO public.bi_fato_faturamento VALUES (197, 'a7590c77-b24a-435a-a4ca-3c4c26c1d6d8', 64, 3, 3, 15, 156, 3, 14.44, 0.00, 14.44, 1);
INSERT INTO public.bi_fato_faturamento VALUES (198, 'b569d1d3-68f4-438b-958e-69f3c527c844', 62, 4, 1, 8, 204, 3, 17.28, 0.00, 17.28, 1);
INSERT INTO public.bi_fato_faturamento VALUES (199, '2cfcdf2a-8033-4532-b593-bbd55fce8813', 62, 4, 1, 14, 204, 3, 14.58, 0.00, 14.58, 1);
INSERT INTO public.bi_fato_faturamento VALUES (200, '23ac067d-e09a-4c29-ab14-fbf3395ae4db', 62, 2, 1, 27, 182, 4, 22.68, 0.00, 22.68, 1);
INSERT INTO public.bi_fato_faturamento VALUES (201, 'bde5d7fc-3420-4080-b231-426bca44be9d', 62, 2, 1, 18, 182, 3, 20.52, 10.26, 10.26, 1);
INSERT INTO public.bi_fato_faturamento VALUES (202, 'ac455b33-2d02-4a8c-86bf-db6165f9fa4f', 62, 2, 1, 4, 182, 2, 25.92, 0.00, 25.92, 1);
INSERT INTO public.bi_fato_faturamento VALUES (203, '79373223-308c-4b9c-97b4-c61138a09b88', 62, 3, 1, 14, 150, 3, 14.58, 0.00, 14.58, 1);
INSERT INTO public.bi_fato_faturamento VALUES (204, 'ed7e21a0-62fd-47f3-82e7-be91841d9abd', 62, 3, 1, 12, 150, 3, 12.42, 0.00, 12.42, 1);
INSERT INTO public.bi_fato_faturamento VALUES (205, 'af20d8d1-2396-4dcd-a407-b7680dc0c6ad', 62, 3, 1, 1, 150, 2, 30.78, 0.00, 30.78, 1);
INSERT INTO public.bi_fato_faturamento VALUES (206, 'da3b976f-3c27-431f-8f4b-496e0b15a516', 62, 3, 1, 15, 150, 3, 14.58, 0.00, 14.58, 1);
INSERT INTO public.bi_fato_faturamento VALUES (207, '80bafeb6-f90c-4baa-80fe-f3e77cdf9279', 62, 3, 7, 28, 10, 5, 17.82, 0.00, 17.82, 1);
INSERT INTO public.bi_fato_faturamento VALUES (208, 'd4b033e3-8797-4859-9dd9-e31a78075939', 62, 3, 7, 7, 10, 3, 13.86, 0.00, 13.86, 1);
INSERT INTO public.bi_fato_faturamento VALUES (209, '1b917343-4919-4e46-b2ff-b5c294c6a0fe', 62, 3, 7, 6, 180, 3, 12.38, 0.00, 12.38, 1);
INSERT INTO public.bi_fato_faturamento VALUES (210, '63546258-aa8a-45ee-8704-b1d6de295fdf', 62, 3, 7, 11, 180, 3, 10.89, 0.00, 10.89, 1);
INSERT INTO public.bi_fato_faturamento VALUES (211, '8eee0aec-3a46-42fe-b443-42a9455ea9ce', 62, 3, 7, 16, 180, 3, 16.83, 0.00, 16.83, 1);
INSERT INTO public.bi_fato_faturamento VALUES (212, '4eab5eca-e23d-4626-8cf2-b96ec2226092', 62, 4, 8, 21, 154, 4, 35.10, 0.00, 35.10, 1);
INSERT INTO public.bi_fato_faturamento VALUES (213, '2bab5283-c838-429d-a8bc-bbfbd33e98b9', 62, 4, 8, 16, 154, 3, 19.89, 5.96, 13.93, 1);
INSERT INTO public.bi_fato_faturamento VALUES (214, '22375ee2-82ef-4a6c-a2ca-f592db4b0a8d', 62, 4, 8, 5, 154, 2, 39.78, 0.00, 39.78, 1);
INSERT INTO public.bi_fato_faturamento VALUES (215, 'd60c8b5d-9a62-474b-994b-f5be2329849d', 64, 5, 3, 1, 151, 2, 30.50, 0.00, 30.50, 1);
INSERT INTO public.bi_fato_faturamento VALUES (216, '85bfdaec-2602-4530-bd40-95b7b44031d8', 64, 5, 3, 3, 151, 2, 23.54, 0.00, 23.54, 1);
INSERT INTO public.bi_fato_faturamento VALUES (217, 'd7ef26dd-b002-4e2b-9f3d-508d789a66e9', 64, 5, 3, 30, 151, 6, 24.61, 0.00, 24.61, 1);
INSERT INTO public.bi_fato_faturamento VALUES (218, '10c26525-1c11-4f8c-bda7-664afc9924ea', 64, 5, 3, 13, 151, 3, 13.91, 0.00, 13.91, 1);
INSERT INTO public.bi_fato_faturamento VALUES (219, 'f1b7d6c3-50be-4b0f-b91b-c7c69cfc7be2', 59, 5, 4, 16, 118, 3, 14.11, 0.00, 14.11, 1);
INSERT INTO public.bi_fato_faturamento VALUES (220, '7e17dae9-5b9f-4dd6-9eb4-5e001ba12725', 59, 5, 4, 18, 118, 3, 15.77, 0.00, 15.77, 1);
INSERT INTO public.bi_fato_faturamento VALUES (221, 'a1b2e9b1-54b8-4dbb-9045-4f199dfdf34c', 59, 5, 4, 9, 118, 3, 13.28, 0.00, 13.28, 1);
INSERT INTO public.bi_fato_faturamento VALUES (222, '31f507c0-e527-41b8-a2c2-e3f250fcf29c', 62, 5, 7, 7, 51, 3, 13.86, 0.00, 13.86, 1);
INSERT INTO public.bi_fato_faturamento VALUES (223, '2842fc9b-b5da-46ac-aee5-d45860183f4c', 62, 5, 7, 28, 51, 5, 17.82, 0.00, 17.82, 1);
INSERT INTO public.bi_fato_faturamento VALUES (224, '28d6a403-7c77-4740-8961-b74586dfd625', 62, 5, 7, 21, 51, 4, 29.70, 0.00, 29.70, 1);
INSERT INTO public.bi_fato_faturamento VALUES (225, 'f9e96b57-00f7-452d-b117-85e22703474c', 62, 5, 7, 12, 51, 3, 11.38, 0.00, 11.38, 1);
INSERT INTO public.bi_fato_faturamento VALUES (226, '3b910b79-a47d-465b-aa98-c1c32987aef7', 62, 2, 8, 22, 171, 4, 72.54, 0.00, 72.54, 1);
INSERT INTO public.bi_fato_faturamento VALUES (227, '63711571-2931-47f2-b14d-8a1d8f381526', 62, 2, 8, 7, 171, 3, 16.38, 0.00, 16.38, 1);
INSERT INTO public.bi_fato_faturamento VALUES (228, 'd7079b75-9acd-4a2d-aa29-deee02a22244', 64, 2, 3, 30, 24, 6, 24.61, 0.00, 24.61, 1);
INSERT INTO public.bi_fato_faturamento VALUES (229, 'b726c241-7ccf-4042-bc62-d89c9cb6aee8', 64, 2, 3, 5, 24, 2, 36.38, 0.00, 36.38, 1);
INSERT INTO public.bi_fato_faturamento VALUES (230, '0b39186a-5a8d-4d93-92db-3f3f0926ecdb', 90, 5, 5, 5, 29, 2, 32.64, 0.00, 32.64, 1);
INSERT INTO public.bi_fato_faturamento VALUES (231, '79f1cfe8-d327-4ecc-9dd7-afb1caed318d', 90, 5, 5, 27, 29, 4, 20.16, 0.00, 20.16, 1);
INSERT INTO public.bi_fato_faturamento VALUES (232, '556cc0e7-c73c-42ce-9cba-f9521d323730', 92, 5, 6, 4, 207, 2, 26.88, 0.00, 26.88, 1);
INSERT INTO public.bi_fato_faturamento VALUES (233, '77ceb486-55e2-47bb-bc79-2f7abe4da34c', 92, 5, 6, 20, 207, 4, 35.84, 0.00, 35.84, 1);
INSERT INTO public.bi_fato_faturamento VALUES (234, '6e819040-1b6b-4799-b799-2d374819ba4c', 92, 5, 6, 1, 207, 2, 31.92, 0.00, 31.92, 1);
INSERT INTO public.bi_fato_faturamento VALUES (235, 'b5cbaf06-c8e5-4715-ad1c-786133cec745', 90, 3, 5, 25, 157, 4, 24.96, 0.00, 24.96, 1);
INSERT INTO public.bi_fato_faturamento VALUES (236, 'ef0aca13-f560-4cfd-8f1d-0e13a9fcb668', 90, 3, 5, 30, 157, 6, 22.08, 0.00, 22.08, 1);
INSERT INTO public.bi_fato_faturamento VALUES (237, '3cc88bb5-869c-4bed-a2ef-3b047953ea8a', 90, 3, 5, 22, 157, 4, 59.52, 0.00, 59.52, 1);
INSERT INTO public.bi_fato_faturamento VALUES (238, 'ee8935de-b658-40fc-babe-7f9ee2800887', 90, 3, 5, 15, 157, 3, 12.96, 0.00, 12.96, 1);
INSERT INTO public.bi_fato_faturamento VALUES (239, '5371f2a6-511c-42a0-b33e-9602082b4a4a', 94, 3, 4, 29, 76, 6, 43.16, 0.00, 43.16, 1);
INSERT INTO public.bi_fato_faturamento VALUES (240, 'b0d32b7b-84b4-4f04-aecc-7552ded665eb', 94, 3, 4, 28, 76, 5, 14.94, 7.47, 7.47, 1);
INSERT INTO public.bi_fato_faturamento VALUES (241, '4cfd3632-2945-411f-bf7c-0ea966549520', 94, 3, 4, 24, 76, 4, 39.84, 0.00, 39.84, 1);
INSERT INTO public.bi_fato_faturamento VALUES (242, '07dbab6e-ab6e-4a1b-ab1e-6cea9e7bd487', 94, 3, 4, 17, 76, 3, 13.70, 0.00, 13.70, 1);
INSERT INTO public.bi_fato_faturamento VALUES (243, 'c2faece9-8861-45da-a0cb-1a4a92fe8f77', 92, 5, 6, 29, 60, 6, 58.24, 0.00, 58.24, 1);
INSERT INTO public.bi_fato_faturamento VALUES (244, 'ac0d7c5a-adee-4a92-9a7a-b3dff9b2eddf', 94, 3, 4, 5, 9, 2, 28.22, 0.00, 28.22, 1);
INSERT INTO public.bi_fato_faturamento VALUES (245, 'b4ef5e28-5663-409d-9fa5-3d85d2646b51', 94, 3, 4, 21, 9, 4, 24.90, 0.00, 24.90, 1);
INSERT INTO public.bi_fato_faturamento VALUES (246, '1d6d15aa-9231-4bac-a896-3557f9f692c3', 94, 3, 4, 26, 9, 4, 34.86, 0.00, 34.86, 1);
INSERT INTO public.bi_fato_faturamento VALUES (247, 'ed4eaf1e-aebe-48a8-b97d-c7db8537e7ac', 94, 3, 4, 16, 9, 3, 14.11, 14.11, 0.00, 1);
INSERT INTO public.bi_fato_faturamento VALUES (248, 'd9cd22fd-43a0-449b-b233-bb8e2ec0ea05', 94, 3, 4, 30, 9, 6, 19.09, 5.72, 13.37, 1);
INSERT INTO public.bi_fato_faturamento VALUES (249, 'a68c7dc7-0a6b-4764-9772-895e44bf0849', 94, 2, 4, 20, 30, 4, 26.56, 0.00, 26.56, 1);
INSERT INTO public.bi_fato_faturamento VALUES (250, 'cd13bd50-299e-42a7-89d0-a21569de48b4', 94, 2, 4, 1, 30, 2, 23.66, 0.00, 23.66, 1);
INSERT INTO public.bi_fato_faturamento VALUES (251, '94109799-fd64-459f-b835-50fd67e7b500', 92, 2, 6, 8, 28, 3, 17.92, 0.00, 17.92, 1);
INSERT INTO public.bi_fato_faturamento VALUES (252, '52a89ba5-99b5-4f68-955e-2d75e4dcbd8e', 92, 2, 6, 4, 28, 2, 26.88, 0.00, 26.88, 1);
INSERT INTO public.bi_fato_faturamento VALUES (253, '2c93586a-3670-43d2-bff3-64a13df6fcda', 92, 2, 6, 29, 28, 6, 58.24, 0.00, 58.24, 1);
INSERT INTO public.bi_fato_faturamento VALUES (254, '35d8f2cc-c3aa-4bb9-844e-7b9ba5d0c149', 92, 2, 6, 28, 28, 5, 20.16, 0.00, 20.16, 1);
INSERT INTO public.bi_fato_faturamento VALUES (255, 'd93c461d-a1ae-419a-8a49-153017921e1a', 90, 2, 5, 22, 77, 4, 59.52, 0.00, 59.52, 1);
INSERT INTO public.bi_fato_faturamento VALUES (256, '4f3b7f10-40d5-4f30-9a33-b2ed2f67057b', 90, 2, 5, 24, 77, 4, 46.08, 0.00, 46.08, 1);
INSERT INTO public.bi_fato_faturamento VALUES (257, 'c71104de-d020-4eef-a842-f5ec53f9909c', 90, 2, 5, 15, 77, 3, 12.96, 0.00, 12.96, 1);
INSERT INTO public.bi_fato_faturamento VALUES (258, 'a0855d25-08a5-482d-9506-b460f2c14351', 90, 2, 5, 13, 77, 3, 12.48, 0.00, 12.48, 1);
INSERT INTO public.bi_fato_faturamento VALUES (259, '0e378ca9-e8c7-4343-8e6c-76fccb58a8fa', 92, 5, 6, 21, 168, 4, 33.60, 0.00, 33.60, 1);
INSERT INTO public.bi_fato_faturamento VALUES (260, '5e94f5d1-9bed-4590-97bf-e8fc4212d021', 92, 5, 6, 10, 168, 3, 17.36, 0.00, 17.36, 1);
INSERT INTO public.bi_fato_faturamento VALUES (261, '74e88b04-b914-44b1-ba64-c92bf919ab20', 92, 5, 6, 19, 168, 4, 42.56, 0.00, 42.56, 1);
INSERT INTO public.bi_fato_faturamento VALUES (262, 'f11826bb-6848-4029-8885-79afaee3f370', 94, 5, 4, 16, 132, 3, 14.11, 0.00, 14.11, 1);
INSERT INTO public.bi_fato_faturamento VALUES (263, 'cf05a196-e26a-40eb-aa1e-53f1ec0ff822', 94, 5, 4, 11, 132, 3, 9.13, 0.00, 9.13, 1);
INSERT INTO public.bi_fato_faturamento VALUES (264, '21878925-31da-4c47-82e0-ccdfe5d2e717', 94, 5, 4, 6, 132, 3, 10.38, 0.00, 10.38, 1);
INSERT INTO public.bi_fato_faturamento VALUES (265, '2c376178-2fc8-41e7-aabb-6ce53f4e5486', 94, 5, 4, 22, 132, 4, 51.46, 0.00, 51.46, 1);
INSERT INTO public.bi_fato_faturamento VALUES (266, '1acf59bd-c030-4f36-9236-284e1c4b4ba6', 92, 3, 6, 29, 89, 6, 58.24, 0.00, 58.24, 1);
INSERT INTO public.bi_fato_faturamento VALUES (267, 'f62313a5-63d2-42d3-9276-928b0e14ff23', 92, 3, 6, 10, 89, 3, 17.36, 0.00, 17.36, 1);
INSERT INTO public.bi_fato_faturamento VALUES (268, 'cb867c33-f48e-4bfe-8f37-d0e03bcb30af', 92, 3, 6, 25, 89, 4, 29.12, 0.00, 29.12, 1);
INSERT INTO public.bi_fato_faturamento VALUES (269, '911d7835-0362-4b8b-b260-7c66b8999a68', 94, 4, 4, 25, 137, 4, 21.58, 0.00, 21.58, 1);
INSERT INTO public.bi_fato_faturamento VALUES (270, '36b68b91-1d75-4838-bf27-394e2d68ce52', 94, 4, 4, 12, 137, 3, 9.54, 0.00, 9.54, 1);
INSERT INTO public.bi_fato_faturamento VALUES (271, 'fc2bf93e-1dff-4e2a-baad-efbbfff4290f', 92, 5, 6, 14, 39, 3, 15.12, 0.00, 15.12, 1);
INSERT INTO public.bi_fato_faturamento VALUES (272, '9bf61196-f79b-44f7-81bc-f1175ba896d6', 92, 5, 6, 9, 39, 3, 17.92, 0.00, 17.92, 1);
INSERT INTO public.bi_fato_faturamento VALUES (273, 'aa66a741-fea6-42c9-93b8-d9ce3f157a9e', 92, 5, 6, 29, 39, 6, 58.24, 0.00, 58.24, 1);
INSERT INTO public.bi_fato_faturamento VALUES (274, 'f3d8c33d-afeb-4014-b7d1-7389db44e2cc', 92, 5, 6, 24, 39, 4, 53.76, 0.00, 53.76, 1);
INSERT INTO public.bi_fato_faturamento VALUES (275, 'f828cfab-f08c-4e7c-af12-48f0179d6ae5', 93, 5, 1, 7, 173, 3, 15.12, 0.00, 15.12, 1);
INSERT INTO public.bi_fato_faturamento VALUES (276, 'ef44cf28-8f59-4add-b978-e28585d611fa', 93, 5, 1, 2, 173, 2, 16.20, 0.00, 16.20, 1);
INSERT INTO public.bi_fato_faturamento VALUES (277, '47e44070-6bc6-44ba-9401-a62609c1f02b', 92, 4, 6, 15, 85, 3, 15.12, 15.12, 0.00, 1);
INSERT INTO public.bi_fato_faturamento VALUES (278, '9807462a-a85e-4442-9a9e-08b7772619d0', 92, 4, 6, 14, 85, 3, 15.12, 7.56, 7.56, 1);
INSERT INTO public.bi_fato_faturamento VALUES (279, '88fe99b5-35df-4f41-b5de-1c908ed8cb9a', 92, 5, 6, 24, 140, 4, 53.76, 0.00, 53.76, 1);
INSERT INTO public.bi_fato_faturamento VALUES (280, '0750ecc9-c19e-47ff-bc69-ff3faf741a44', 92, 5, 6, 26, 140, 4, 47.04, 0.00, 47.04, 1);
INSERT INTO public.bi_fato_faturamento VALUES (281, '6fd6304a-4354-443e-a83e-abb5b71b627e', 92, 5, 6, 20, 72, 4, 35.84, 35.84, 0.00, 1);
INSERT INTO public.bi_fato_faturamento VALUES (282, '2a4abda1-f8ca-487c-8483-495ef8f4a3c5', 92, 5, 6, 29, 72, 6, 58.24, 0.00, 58.24, 1);
INSERT INTO public.bi_fato_faturamento VALUES (283, '6c40302b-c8a9-464e-aaff-9efc340b67a4', 92, 5, 6, 16, 72, 3, 19.04, 0.00, 19.04, 1);
INSERT INTO public.bi_fato_faturamento VALUES (284, '863c89bc-e81d-4b6c-86d0-1dfe1c12deca', 93, 5, 1, 5, 140, 2, 36.72, 0.00, 36.72, 1);
INSERT INTO public.bi_fato_faturamento VALUES (285, 'e8ef9767-4ed3-4940-929a-1751c35cca14', 93, 5, 1, 26, 140, 4, 45.36, 0.00, 45.36, 1);
INSERT INTO public.bi_fato_faturamento VALUES (286, 'db0f8a09-7bef-43aa-b228-99e6bb41258f', 93, 5, 1, 22, 140, 4, 66.96, 0.00, 66.96, 1);
INSERT INTO public.bi_fato_faturamento VALUES (287, '8562a9af-5d18-4b64-967f-103c6a81fee0', 94, 5, 4, 20, 205, 4, 26.56, 0.00, 26.56, 1);
INSERT INTO public.bi_fato_faturamento VALUES (288, '71a84296-41e6-419c-bbeb-934eb201cd7c', 94, 5, 4, 8, 205, 3, 13.28, 0.00, 13.28, 1);
INSERT INTO public.bi_fato_faturamento VALUES (289, '51533ede-e35f-4d1e-8565-cd71a2818bfe', 92, 3, 3, 29, 40, 6, 55.64, 0.00, 55.64, 1);
INSERT INTO public.bi_fato_faturamento VALUES (290, 'c366c7df-6792-4f06-ac9b-95c0497be1e9', 92, 3, 3, 8, 40, 3, 17.12, 0.00, 17.12, 1);
INSERT INTO public.bi_fato_faturamento VALUES (291, '90cedd11-cc16-43d6-a79e-77341d257f2a', 92, 3, 3, 21, 40, 4, 32.10, 0.00, 32.10, 1);
INSERT INTO public.bi_fato_faturamento VALUES (292, '04d360b2-87da-4c95-aa13-52ae92393edc', 92, 3, 3, 12, 40, 3, 12.30, 0.00, 12.30, 1);
INSERT INTO public.bi_fato_faturamento VALUES (293, 'cd538bb7-5124-48ef-a218-87322da1b3d0', 92, 3, 3, 11, 40, 3, 11.77, 0.00, 11.77, 1);
INSERT INTO public.bi_fato_faturamento VALUES (294, '5ad88682-6113-4630-8e4f-f75f5c6e70a3', 94, 3, 4, 7, 202, 3, 11.62, 3.48, 8.14, 1);
INSERT INTO public.bi_fato_faturamento VALUES (295, '1d28271e-d295-4a82-822f-4d6abda1b06e', 94, 3, 4, 4, 202, 2, 19.92, 5.97, 13.95, 1);
INSERT INTO public.bi_fato_faturamento VALUES (296, '4c7da579-7728-4368-ab8c-084e49713989', 92, 4, 3, 16, 196, 3, 18.19, 0.00, 18.19, 1);
INSERT INTO public.bi_fato_faturamento VALUES (297, 'e7f48a87-214e-4cef-af02-954242df57f3', 92, 4, 3, 5, 196, 2, 36.38, 0.00, 36.38, 1);
INSERT INTO public.bi_fato_faturamento VALUES (298, '565baddf-c9c8-4700-8e71-ed9604b3b96c', 92, 4, 3, 28, 196, 5, 19.26, 0.00, 19.26, 1);
INSERT INTO public.bi_fato_faturamento VALUES (299, '2bf750f9-c694-4eb9-9432-d818ee37c746', 92, 4, 3, 24, 80, 4, 51.36, 0.00, 51.36, 1);
INSERT INTO public.bi_fato_faturamento VALUES (300, '6c3d9af6-dce3-4b16-9970-c9d8e4fd3a4c', 92, 4, 3, 3, 80, 2, 23.54, 0.00, 23.54, 1);
INSERT INTO public.bi_fato_faturamento VALUES (301, '72a609d5-3118-42a8-82e4-52414cbe0adc', 92, 3, 6, 9, 209, 3, 17.92, 0.00, 17.92, 1);
INSERT INTO public.bi_fato_faturamento VALUES (302, '649fe931-f08a-47fe-af01-13e551c175a3', 92, 3, 6, 21, 209, 4, 33.60, 0.00, 33.60, 1);
INSERT INTO public.bi_fato_faturamento VALUES (303, 'b1fb2362-b804-4465-aa58-32b86245176d', 92, 3, 6, 8, 70, 3, 17.92, 8.96, 8.96, 1);
INSERT INTO public.bi_fato_faturamento VALUES (304, '7defaed6-5a0e-4f68-a4b7-833065450b0c', 92, 3, 6, 4, 70, 2, 26.88, 0.00, 26.88, 1);
INSERT INTO public.bi_fato_faturamento VALUES (305, '913006f4-92bb-404b-bcef-ea9626c59633', 92, 3, 6, 29, 70, 6, 58.24, 0.00, 58.24, 1);
INSERT INTO public.bi_fato_faturamento VALUES (306, '6b5daf44-8a0f-4f26-a47a-38a225700008', 90, 3, 5, 27, 210, 4, 20.16, 0.00, 20.16, 1);
INSERT INTO public.bi_fato_faturamento VALUES (307, '4169124d-dc05-45cd-9375-95ea20a46666', 90, 3, 5, 20, 210, 4, 30.72, 0.00, 30.72, 1);
INSERT INTO public.bi_fato_faturamento VALUES (308, '038de0aa-396b-4e74-a9ea-e8582f91a72d', 90, 3, 5, 28, 210, 5, 17.28, 0.00, 17.28, 1);
INSERT INTO public.bi_fato_faturamento VALUES (309, '44a5e426-6ebf-4cc7-b6aa-3a8aa5781c87', 93, 3, 1, 18, 182, 3, 20.52, 0.00, 20.52, 1);
INSERT INTO public.bi_fato_faturamento VALUES (310, '8c7d7b5d-416c-48d2-aa93-4843d86a1b50', 90, 3, 5, 12, 217, 3, 11.04, 3.31, 7.73, 1);
INSERT INTO public.bi_fato_faturamento VALUES (311, '244b9a4f-13ff-49a7-a9d1-acbcf7cfa260', 90, 3, 5, 6, 217, 3, 12.00, 0.00, 12.00, 1);
INSERT INTO public.bi_fato_faturamento VALUES (312, '9e587f21-5737-4ad9-b64b-3fb696c53b19', 90, 3, 5, 15, 217, 3, 12.96, 0.00, 12.96, 1);
INSERT INTO public.bi_fato_faturamento VALUES (313, 'ef9466ef-6984-4f5f-bc65-4f9d576020ff', 92, 3, 6, 29, 90, 6, 58.24, 0.00, 58.24, 1);
INSERT INTO public.bi_fato_faturamento VALUES (314, 'fa380337-0490-4436-b10c-2eedd8625580', 92, 3, 6, 21, 90, 4, 33.60, 0.00, 33.60, 1);
INSERT INTO public.bi_fato_faturamento VALUES (315, '5f6cd301-149b-4a25-9922-cd688e9ebf2e', 92, 3, 6, 12, 90, 3, 12.88, 0.00, 12.88, 1);
INSERT INTO public.bi_fato_faturamento VALUES (316, '6b8c2ed4-49df-473d-ae40-074c5ec0a8c7', 92, 3, 6, 14, 90, 3, 15.12, 0.00, 15.12, 1);
INSERT INTO public.bi_fato_faturamento VALUES (317, 'cb40a512-df27-4918-933a-704fe533fb5a', 93, 4, 1, 19, 143, 4, 41.04, 0.00, 41.04, 1);
INSERT INTO public.bi_fato_faturamento VALUES (318, '932cccb3-1aae-49c8-993d-e3599fd8485b', 93, 4, 1, 8, 143, 3, 17.28, 5.18, 12.10, 1);
INSERT INTO public.bi_fato_faturamento VALUES (319, '6d29fafd-d706-4942-980d-c8ca3ffa0da8', 93, 4, 1, 23, 143, 4, 48.60, 0.00, 48.60, 1);
INSERT INTO public.bi_fato_faturamento VALUES (320, 'd457a38f-83fb-4831-95f8-9e94bcebae11', 93, 4, 1, 25, 143, 4, 28.08, 14.04, 14.04, 1);
INSERT INTO public.bi_fato_faturamento VALUES (321, '2c5c2562-9cb4-4990-ae6b-7b28d1600aff', 90, 2, 5, 12, 25, 3, 11.04, 0.00, 11.04, 1);
INSERT INTO public.bi_fato_faturamento VALUES (322, 'b4ea9d99-a48d-4804-9b4f-5bb2067bdd20', 90, 2, 5, 16, 25, 3, 16.32, 4.89, 11.43, 1);
INSERT INTO public.bi_fato_faturamento VALUES (323, 'e6850d19-e6b4-457f-a505-e2d49c41a5cc', 94, 2, 4, 28, 26, 5, 14.94, 0.00, 14.94, 1);
INSERT INTO public.bi_fato_faturamento VALUES (324, '394deff7-668e-4d9f-aa54-867f8eadd590', 92, 2, 3, 26, 32, 4, 44.94, 0.00, 44.94, 1);
INSERT INTO public.bi_fato_faturamento VALUES (325, '889902ec-ba74-448f-a426-b26b69a4e259', 92, 2, 3, 16, 32, 3, 18.19, 0.00, 18.19, 1);
INSERT INTO public.bi_fato_faturamento VALUES (326, '081d9d34-4d52-495b-99b6-92afb6e2c209', 92, 2, 3, 8, 32, 3, 17.12, 5.13, 11.99, 1);
INSERT INTO public.bi_fato_faturamento VALUES (327, '718afa68-3651-4184-ba6e-ec267d9fca37', 92, 2, 3, 29, 32, 6, 55.64, 0.00, 55.64, 1);
INSERT INTO public.bi_fato_faturamento VALUES (328, 'cf8e3e66-0940-473a-a2a3-2169be0865bd', 92, 4, 3, 8, 96, 3, 17.12, 0.00, 17.12, 1);
INSERT INTO public.bi_fato_faturamento VALUES (329, '0d1bf717-31da-418f-a529-7cb65dedc265', 92, 4, 3, 21, 96, 4, 32.10, 0.00, 32.10, 1);
INSERT INTO public.bi_fato_faturamento VALUES (330, '9fa97053-9f7c-48ba-815c-575ec2db831a', 92, 4, 3, 18, 96, 3, 20.33, 20.33, 0.00, 1);
INSERT INTO public.bi_fato_faturamento VALUES (331, '65058f1a-1f60-4d5d-905a-e0bb99069b62', 92, 4, 3, 27, 96, 4, 22.47, 0.00, 22.47, 1);
INSERT INTO public.bi_fato_faturamento VALUES (332, 'eadd0e7c-7a4b-4a82-a6b2-e89662420a44', 92, 4, 3, 3, 96, 2, 23.54, 0.00, 23.54, 1);
INSERT INTO public.bi_fato_faturamento VALUES (333, '74cc5120-ea0d-460d-b41e-39dd80c00af3', 94, 3, 4, 1, 13, 2, 23.66, 0.00, 23.66, 1);
INSERT INTO public.bi_fato_faturamento VALUES (334, '2a30bfbf-3b7e-4728-9101-d812b3c02c7c', 94, 3, 4, 24, 13, 4, 39.84, 0.00, 39.84, 1);
INSERT INTO public.bi_fato_faturamento VALUES (335, 'e3d46898-4265-4de6-a475-1410a72c491e', 94, 3, 4, 19, 13, 4, 31.54, 0.00, 31.54, 1);
INSERT INTO public.bi_fato_faturamento VALUES (336, 'a8579691-1517-47fa-b4f3-6c753e9cfa64', 94, 3, 4, 9, 13, 3, 13.28, 0.00, 13.28, 1);
INSERT INTO public.bi_fato_faturamento VALUES (337, '03806641-28ff-4c57-8ae5-ad80af4f9e1e', 94, 3, 4, 17, 13, 3, 13.70, 0.00, 13.70, 1);
INSERT INTO public.bi_fato_faturamento VALUES (338, '7a721d4c-d568-4faa-85af-144c547e9eab', 92, 3, 6, 6, 74, 3, 14.00, 0.00, 14.00, 1);
INSERT INTO public.bi_fato_faturamento VALUES (339, 'd3c7e902-cdab-4188-9cdc-0fa36b9397ea', 92, 3, 6, 2, 74, 2, 16.80, 0.00, 16.80, 1);
INSERT INTO public.bi_fato_faturamento VALUES (340, '3fe47994-ed87-43b6-97ad-0b86aa075dcc', 92, 3, 6, 8, 74, 3, 17.92, 0.00, 17.92, 1);
INSERT INTO public.bi_fato_faturamento VALUES (341, '9d3aa7f1-38c3-4e48-aa32-5c8bb60f6610', 92, 3, 6, 24, 74, 4, 53.76, 0.00, 53.76, 1);
INSERT INTO public.bi_fato_faturamento VALUES (342, '06a6adf8-7565-424a-92c4-bd5a3f5bbd84', 92, 3, 6, 17, 156, 3, 18.48, 0.00, 18.48, 1);
INSERT INTO public.bi_fato_faturamento VALUES (343, 'f77e61dc-cd44-4138-b627-7825b6d06cca', 92, 3, 6, 25, 156, 4, 29.12, 0.00, 29.12, 1);
INSERT INTO public.bi_fato_faturamento VALUES (344, '441addc6-f4f6-4ccb-a825-d90d3d094d6a', 93, 4, 1, 7, 177, 3, 15.12, 0.00, 15.12, 1);
INSERT INTO public.bi_fato_faturamento VALUES (345, 'fc0e7c70-3bf5-4867-931c-9794b4bd8aec', 93, 4, 1, 6, 177, 3, 13.50, 0.00, 13.50, 1);
INSERT INTO public.bi_fato_faturamento VALUES (346, 'ee93599f-5a8e-45bd-930a-3da27fd861a8', 90, 2, 5, 11, 102, 3, 10.56, 0.00, 10.56, 1);
INSERT INTO public.bi_fato_faturamento VALUES (347, '5e6198a2-c532-4282-9def-efbe6641afc1', 90, 2, 5, 5, 102, 2, 32.64, 0.00, 32.64, 1);
INSERT INTO public.bi_fato_faturamento VALUES (348, '7f71b1d4-6a4c-4bd6-9fe9-1c336fbfccd6', 90, 2, 5, 3, 102, 2, 21.12, 0.00, 21.12, 1);
INSERT INTO public.bi_fato_faturamento VALUES (349, '050f7b29-2832-44f5-9dd6-fa095a36d3a9', 93, 4, 1, 18, 177, 3, 20.52, 0.00, 20.52, 1);
INSERT INTO public.bi_fato_faturamento VALUES (350, 'e3bc1cea-5363-4ab9-b682-90a2eb3d6104', 92, 5, 3, 26, 217, 4, 44.94, 0.00, 44.94, 1);
INSERT INTO public.bi_fato_faturamento VALUES (351, '705fbeb9-76ba-4e1d-a96d-450b326c81a0', 92, 5, 3, 13, 217, 3, 13.91, 0.00, 13.91, 1);
INSERT INTO public.bi_fato_faturamento VALUES (352, 'ad3f2ee0-40af-475c-a3f4-d9b3b24a2e0b', 92, 5, 3, 22, 152, 4, 66.34, 0.00, 66.34, 1);
INSERT INTO public.bi_fato_faturamento VALUES (353, 'be6d542a-a983-477f-b762-3de451869fc7', 92, 5, 3, 28, 152, 5, 19.26, 0.00, 19.26, 1);
INSERT INTO public.bi_fato_faturamento VALUES (354, 'fce04ae9-6e00-448a-bfcc-4314a32de311', 92, 5, 3, 17, 152, 3, 17.66, 0.00, 17.66, 1);
INSERT INTO public.bi_fato_faturamento VALUES (355, 'be789827-0f4c-474c-9c16-e0582523b071', 93, 5, 1, 24, 179, 4, 51.84, 51.84, 0.00, 1);
INSERT INTO public.bi_fato_faturamento VALUES (356, 'cd73cc45-531f-4d24-b773-33cd69af074f', 93, 5, 1, 5, 179, 2, 36.72, 0.00, 36.72, 1);
INSERT INTO public.bi_fato_faturamento VALUES (357, '9bd66bed-3f3d-4544-aedc-9f8453f939b9', 94, 3, 4, 7, 48, 3, 11.62, 0.00, 11.62, 1);
INSERT INTO public.bi_fato_faturamento VALUES (358, 'a99158ae-b825-4028-8e63-35dbd3a56e07', 94, 3, 4, 21, 48, 4, 24.90, 0.00, 24.90, 1);
INSERT INTO public.bi_fato_faturamento VALUES (359, '15a45d19-1708-4f42-9453-9317de6a50ff', 94, 3, 4, 25, 48, 4, 21.58, 0.00, 21.58, 1);
INSERT INTO public.bi_fato_faturamento VALUES (360, '100061b5-1717-4a66-9246-a43686de293f', 94, 3, 4, 17, 48, 3, 13.70, 0.00, 13.70, 1);
INSERT INTO public.bi_fato_faturamento VALUES (361, '24e7ea31-bf8b-4d4d-8ad4-849ae8eecc6b', 92, 3, 6, 15, 95, 3, 15.12, 0.00, 15.12, 1);
INSERT INTO public.bi_fato_faturamento VALUES (362, '54367da0-1b3e-4b22-8f32-972b01eadd46', 92, 3, 6, 2, 95, 2, 16.80, 0.00, 16.80, 1);
INSERT INTO public.bi_fato_faturamento VALUES (363, '2f3f8a51-af4f-4275-a066-7a4f787201ff', 92, 3, 6, 1, 95, 2, 31.92, 0.00, 31.92, 1);
INSERT INTO public.bi_fato_faturamento VALUES (364, '461825e9-0c30-4deb-8e54-e3997fd2d79d', 92, 3, 6, 22, 95, 4, 69.44, 34.72, 34.72, 1);
INSERT INTO public.bi_fato_faturamento VALUES (365, 'e156bb45-81ea-40a8-8d3c-400dcd38c18e', 34, 4, 5, 22, 218, 4, 59.52, 0.00, 59.52, 1);
INSERT INTO public.bi_fato_faturamento VALUES (366, 'bdce779b-2896-4f7d-a2f1-a5c59cf8e179', 34, 4, 5, 27, 218, 4, 20.16, 0.00, 20.16, 1);
INSERT INTO public.bi_fato_faturamento VALUES (367, '4b04482c-09e7-489d-98b6-8d5a0c276b7f', 34, 4, 5, 29, 218, 6, 49.92, 14.97, 34.95, 1);
INSERT INTO public.bi_fato_faturamento VALUES (368, '5b8ac452-5bac-42e0-a71e-da26f935077d', 34, 4, 5, 11, 218, 3, 10.56, 0.00, 10.56, 1);
INSERT INTO public.bi_fato_faturamento VALUES (369, 'dfc74afa-b018-4a50-a657-98370977dbc7', 34, 4, 5, 7, 218, 3, 13.44, 0.00, 13.44, 1);
INSERT INTO public.bi_fato_faturamento VALUES (370, '4dd62b72-6583-49d0-a32c-7505b8bab613', 34, 4, 5, 5, 14, 2, 32.64, 0.00, 32.64, 1);
INSERT INTO public.bi_fato_faturamento VALUES (371, 'deaa4686-31fb-4cd6-962b-8749e75709c7', 33, 4, 7, 3, 206, 2, 21.78, 0.00, 21.78, 1);
INSERT INTO public.bi_fato_faturamento VALUES (372, '70e51f2e-0215-4262-b73b-8c0d0cd3908e', 34, 5, 5, 24, 191, 4, 46.08, 0.00, 46.08, 1);
INSERT INTO public.bi_fato_faturamento VALUES (373, '0c3e8a88-8594-49fb-a143-babc6821b46e', 34, 5, 5, 7, 191, 3, 13.44, 13.44, 0.00, 1);
INSERT INTO public.bi_fato_faturamento VALUES (374, '46bea6ce-299f-460a-853e-12253e742728', 32, 5, 6, 10, 170, 3, 17.36, 0.00, 17.36, 1);
INSERT INTO public.bi_fato_faturamento VALUES (375, '78af58b2-a1c1-4756-a9f3-eb5dabc78772', 32, 5, 6, 1, 170, 2, 31.92, 31.92, 0.00, 1);
INSERT INTO public.bi_fato_faturamento VALUES (376, 'af15d8c7-06dc-4123-9a63-88beb4995515', 34, 2, 4, 29, 164, 6, 43.16, 0.00, 43.16, 1);
INSERT INTO public.bi_fato_faturamento VALUES (377, '99ec23b1-ae16-42a0-9969-786850ac6be1', 34, 5, 5, 22, 10, 4, 59.52, 0.00, 59.52, 1);
INSERT INTO public.bi_fato_faturamento VALUES (378, '5e72f721-7ca0-4ebc-a191-a384bdd0e3e2', 34, 5, 5, 6, 173, 3, 12.00, 0.00, 12.00, 1);
INSERT INTO public.bi_fato_faturamento VALUES (379, '23a4b796-d54c-4358-929f-2c5c3d21aa4c', 33, 5, 7, 24, 2, 4, 47.52, 0.00, 47.52, 1);
INSERT INTO public.bi_fato_faturamento VALUES (380, 'fd668a03-c038-4a39-bf8b-406eebbbf1e0', 33, 5, 7, 19, 2, 4, 37.62, 0.00, 37.62, 1);
INSERT INTO public.bi_fato_faturamento VALUES (381, '7094ac44-5a86-45f2-8b76-ad62583b72fb', 33, 5, 7, 4, 2, 2, 23.76, 0.00, 23.76, 1);
INSERT INTO public.bi_fato_faturamento VALUES (382, '760f0e8f-1157-498b-8611-efb943376ee4', 33, 5, 7, 16, 2, 3, 16.83, 0.00, 16.83, 1);
INSERT INTO public.bi_fato_faturamento VALUES (383, '4c2be54f-b081-4eed-a661-2dd3b9348cd5', 34, 2, 4, 5, 102, 2, 28.22, 0.00, 28.22, 1);
INSERT INTO public.bi_fato_faturamento VALUES (384, '98b5239b-7b29-4f47-8337-7f655aab0a7b', 34, 2, 4, 18, 102, 3, 15.77, 0.00, 15.77, 1);
INSERT INTO public.bi_fato_faturamento VALUES (385, '808601ac-8a14-4f25-afcb-e7a6df0438cd', 62, 3, 7, 19, 108, 4, 37.62, 0.00, 37.62, 1);
INSERT INTO public.bi_fato_faturamento VALUES (386, 'f8f8b758-6f37-4407-a9bc-05fd68a44702', 62, 2, 1, 27, 185, 4, 22.68, 0.00, 22.68, 1);
INSERT INTO public.bi_fato_faturamento VALUES (387, 'd6de1256-8cd1-43ef-8c25-10024831518b', 59, 2, 4, 9, 81, 3, 13.28, 0.00, 13.28, 1);
INSERT INTO public.bi_fato_faturamento VALUES (388, '69aaeb1f-85df-4cd8-bb52-a8f12080f9e6', 59, 2, 4, 1, 81, 2, 23.66, 0.00, 23.66, 1);
INSERT INTO public.bi_fato_faturamento VALUES (389, '11d25918-b84c-4e28-aaf7-39b1e942e911', 59, 2, 4, 10, 81, 3, 12.86, 0.00, 12.86, 1);
INSERT INTO public.bi_fato_faturamento VALUES (390, '6856af0a-9e41-4ee9-881b-607e380fd7ea', 59, 2, 4, 20, 81, 4, 26.56, 0.00, 26.56, 1);
INSERT INTO public.bi_fato_faturamento VALUES (391, '1594da6d-5687-4dbd-9d5a-db97be6f61cf', 59, 2, 4, 25, 81, 4, 21.58, 0.00, 21.58, 1);
INSERT INTO public.bi_fato_faturamento VALUES (392, '5baaa605-ada1-40c5-8b99-bcd522aee222', 59, 2, 4, 13, 81, 3, 10.79, 0.00, 10.79, 1);
INSERT INTO public.bi_fato_faturamento VALUES (393, '50d25bb3-6618-4098-a47d-8959056f2bc5', 62, 2, 7, 2, 118, 2, 14.85, 0.00, 14.85, 1);
INSERT INTO public.bi_fato_faturamento VALUES (394, '32305fda-efe6-4e69-bea8-d63764a5dc7f', 53, 5, 5, 3, 194, 2, 21.12, 0.00, 21.12, 1);
INSERT INTO public.bi_fato_faturamento VALUES (395, '36ca4e7e-b923-45b9-add1-eaa47f0d2233', 53, 5, 5, 7, 194, 3, 13.44, 0.00, 13.44, 1);
INSERT INTO public.bi_fato_faturamento VALUES (396, '2692304e-d9bb-4daf-b99e-9dad7a6305e1', 53, 5, 5, 29, 194, 6, 49.92, 0.00, 49.92, 1);
INSERT INTO public.bi_fato_faturamento VALUES (397, 'd8b3b597-32a9-415e-86db-427f3d36daec', 53, 5, 5, 18, 194, 3, 18.24, 0.00, 18.24, 1);
INSERT INTO public.bi_fato_faturamento VALUES (398, '4d3fc65f-34fe-43a9-849a-6a84e1e998bb', 53, 5, 5, 13, 194, 3, 12.48, 0.00, 12.48, 1);
INSERT INTO public.bi_fato_faturamento VALUES (399, '19041d12-7948-43be-9941-991a5c45531b', 62, 4, 8, 20, 145, 4, 37.44, 0.00, 37.44, 1);
INSERT INTO public.bi_fato_faturamento VALUES (400, '26ea586a-e28b-4240-9491-2f883d7fb84d', 62, 4, 8, 8, 145, 3, 18.72, 0.00, 18.72, 1);
INSERT INTO public.bi_fato_faturamento VALUES (401, 'c9d2362b-d17a-405a-b0fd-8ca8b30d372e', 62, 3, 8, 18, 12, 3, 22.23, 22.23, 0.00, 1);
INSERT INTO public.bi_fato_faturamento VALUES (402, 'b31ce839-2e12-495c-bfc7-98c07b113826', 64, 2, 3, 19, 151, 4, 40.66, 12.19, 28.47, 1);
INSERT INTO public.bi_fato_faturamento VALUES (403, 'e81e3bea-d7b4-4827-a83f-a7411db5ac65', 64, 2, 3, 12, 151, 3, 12.30, 0.00, 12.30, 1);
INSERT INTO public.bi_fato_faturamento VALUES (404, '5708eee3-9ee5-4be7-b698-46f40e4888c2', 62, 5, 1, 4, 73, 2, 25.92, 0.00, 25.92, 1);
INSERT INTO public.bi_fato_faturamento VALUES (405, 'bad79b6b-da06-4dbd-a5ab-cfe3d0f6772d', 62, 5, 1, 22, 73, 4, 66.96, 0.00, 66.96, 1);
INSERT INTO public.bi_fato_faturamento VALUES (406, '1430c390-47fe-4e7e-a933-9aa36de090b9', 62, 5, 1, 13, 73, 3, 14.04, 0.00, 14.04, 1);
INSERT INTO public.bi_fato_faturamento VALUES (407, '31faec65-7897-4ce3-9b93-f414e456ec46', 62, 4, 7, 17, 165, 3, 16.34, 0.00, 16.34, 1);
INSERT INTO public.bi_fato_faturamento VALUES (408, '9ddd0436-c6a5-467e-be3d-4daa1c936b81', 62, 5, 1, 16, 205, 3, 18.36, 0.00, 18.36, 1);
INSERT INTO public.bi_fato_faturamento VALUES (409, 'fde29d28-a6b2-4cd0-a9bd-1cc03affde0e', 62, 5, 1, 8, 205, 3, 17.28, 0.00, 17.28, 1);
INSERT INTO public.bi_fato_faturamento VALUES (410, '85197daf-ad9b-4b1f-9655-eb99758ea7ce', 64, 5, 3, 5, 130, 2, 36.38, 0.00, 36.38, 1);
INSERT INTO public.bi_fato_faturamento VALUES (411, '12fe9793-6067-48ae-b93b-134edf0b5b14', 62, 2, 1, 20, 182, 4, 34.56, 0.00, 34.56, 1);
INSERT INTO public.bi_fato_faturamento VALUES (412, '69ed5ae5-8025-4e35-bd47-7de81717d92c', 62, 3, 8, 17, 194, 3, 19.30, 0.00, 19.30, 1);
INSERT INTO public.bi_fato_faturamento VALUES (413, 'dcfe6f4e-2789-40d6-85b6-55533d27e204', 62, 3, 8, 22, 194, 4, 72.54, 0.00, 72.54, 1);
INSERT INTO public.bi_fato_faturamento VALUES (414, '6f39b478-32ec-4435-ab75-9a303b2b15f6', 62, 4, 8, 9, 154, 3, 18.72, 0.00, 18.72, 1);
INSERT INTO public.bi_fato_faturamento VALUES (415, 'd87191b2-cb40-4aef-9453-00101c1f2fef', 59, 5, 4, 29, 118, 6, 43.16, 0.00, 43.16, 1);
INSERT INTO public.bi_fato_faturamento VALUES (416, 'fc4490ea-fc30-4e43-af06-42a25618f028', 59, 5, 4, 23, 118, 4, 37.35, 0.00, 37.35, 1);
INSERT INTO public.bi_fato_faturamento VALUES (417, '3057e789-b6bd-4474-b26c-2590abce5597', 94, 3, 4, 3, 76, 2, 18.26, 0.00, 18.26, 1);
INSERT INTO public.bi_fato_faturamento VALUES (418, 'c370de21-5a6a-45a1-b223-21bf6cf9f36a', 94, 3, 4, 10, 76, 3, 12.86, 0.00, 12.86, 1);
INSERT INTO public.bi_fato_faturamento VALUES (419, 'f6495a28-17c5-4fd1-88ec-ae72a3276897', 92, 5, 6, 20, 60, 4, 35.84, 0.00, 35.84, 1);
INSERT INTO public.bi_fato_faturamento VALUES (420, '266caad8-54af-412f-811b-e4d5a945f79d', 92, 5, 6, 24, 60, 4, 53.76, 53.76, 0.00, 1);
INSERT INTO public.bi_fato_faturamento VALUES (421, '02856505-fe59-4e1c-8989-f61dd8a0ca7b', 92, 5, 6, 1, 60, 2, 31.92, 0.00, 31.92, 1);
INSERT INTO public.bi_fato_faturamento VALUES (422, '3bfe707d-50c8-496b-b32e-7ce98d1df22d', 92, 5, 6, 16, 168, 3, 19.04, 0.00, 19.04, 1);
INSERT INTO public.bi_fato_faturamento VALUES (423, '2503b453-e7a2-4a2d-bd09-889847455f26', 92, 5, 6, 13, 168, 3, 14.56, 0.00, 14.56, 1);
INSERT INTO public.bi_fato_faturamento VALUES (424, '599f0d03-7be5-4779-9042-dabec3530e47', 92, 5, 6, 29, 168, 6, 58.24, 0.00, 58.24, 1);
INSERT INTO public.bi_fato_faturamento VALUES (425, '95d9168c-c7cb-4d73-8de2-1748626e6da1', 90, 2, 5, 1, 77, 2, 27.36, 0.00, 27.36, 1);
INSERT INTO public.bi_fato_faturamento VALUES (426, '0c762c4e-59c8-4af9-bc98-b8f8d82aa04d', 92, 2, 3, 25, 136, 4, 27.82, 0.00, 27.82, 1);
INSERT INTO public.bi_fato_faturamento VALUES (427, '33b68d11-403c-4556-941b-6dd3d5847de4', 92, 2, 3, 10, 136, 3, 16.58, 16.58, 0.00, 1);
INSERT INTO public.bi_fato_faturamento VALUES (428, '103d8490-893c-416c-a1a4-aba49275fc66', 92, 2, 3, 14, 136, 3, 14.44, 0.00, 14.44, 1);
INSERT INTO public.bi_fato_faturamento VALUES (429, 'cca1908a-fdbb-4645-922f-a4693e833773', 92, 2, 3, 26, 136, 4, 44.94, 0.00, 44.94, 1);
INSERT INTO public.bi_fato_faturamento VALUES (430, 'a137c307-621a-4637-b43d-ea22269c465c', 92, 3, 3, 3, 40, 2, 23.54, 0.00, 23.54, 1);
INSERT INTO public.bi_fato_faturamento VALUES (431, 'f6715ad8-3aa2-4dda-b033-e3b87c6daa30', 90, 3, 5, 14, 210, 3, 12.96, 0.00, 12.96, 1);
INSERT INTO public.bi_fato_faturamento VALUES (432, '494a43ae-d801-47db-bb01-ef66edb5ae66', 90, 3, 5, 6, 210, 3, 12.00, 0.00, 12.00, 1);
INSERT INTO public.bi_fato_faturamento VALUES (433, '51b6c573-df63-44ed-86b7-8af138815d4d', 90, 3, 5, 12, 210, 3, 11.04, 0.00, 11.04, 1);
INSERT INTO public.bi_fato_faturamento VALUES (434, '834d5ff0-cf9e-42e5-92c0-c90b8eb8146f', 92, 3, 6, 6, 90, 3, 14.00, 0.00, 14.00, 1);
INSERT INTO public.bi_fato_faturamento VALUES (435, '3dae66ec-5b78-411b-9211-5766d271f2dd', 93, 4, 1, 12, 143, 3, 12.42, 12.42, 0.00, 1);
INSERT INTO public.bi_fato_faturamento VALUES (436, 'b36f1f0d-3086-407c-ab49-f8eeed24d9da', 93, 4, 1, 4, 143, 2, 25.92, 0.00, 25.92, 1);
INSERT INTO public.bi_fato_faturamento VALUES (437, '553f3e83-0a16-49fa-80fa-7f966155d32d', 92, 3, 6, 5, 74, 2, 38.08, 0.00, 38.08, 1);
INSERT INTO public.bi_fato_faturamento VALUES (438, '0b57a645-8cbf-4d94-9d6e-275823266ba9', 92, 3, 6, 3, 95, 2, 24.64, 0.00, 24.64, 1);


--
-- Data for Name: bi_fato_financeiro; Type: TABLE DATA; Schema: public; Owner: labvida
--

INSERT INTO public.bi_fato_financeiro VALUES (1, 'PREVISTO', 'titulos_receber', 'd8712706-e200-4aa8-8221-82aab526902b', 124, 1, 4, 'ENTRADA', 710.50, 0.00, false);
INSERT INTO public.bi_fato_financeiro VALUES (2, 'PREVISTO', 'titulos_receber', 'f247ae84-1350-4268-b073-4cc96d6329fa', 92, 1, 8, 'ENTRADA', 965.85, 0.00, false);
INSERT INTO public.bi_fato_financeiro VALUES (3, 'PREVISTO', 'titulos_receber', '9959a033-11db-4fa0-9d9f-f3b83c5ecb1f', 122, 1, 3, 'ENTRADA', 818.54, 0.00, false);
INSERT INTO public.bi_fato_financeiro VALUES (4, 'PREVISTO', 'titulos_receber', 'a1a97960-242d-485d-ba50-24bfc5c4c4ac', 122, 1, 6, 'ENTRADA', 1711.36, 0.00, false);
INSERT INTO public.bi_fato_financeiro VALUES (5, 'PREVISTO', 'titulos_receber', '6bf71db8-c6b1-4b40-a842-13b5cd7960bf', 120, 1, 5, 'ENTRADA', 562.56, 0.00, false);
INSERT INTO public.bi_fato_financeiro VALUES (6, 'PREVISTO', 'titulos_receber', '9ad1b2d4-4c1e-4bc3-892e-44c4b69a7ec2', 123, 1, 1, 'ENTRADA', 511.92, 0.00, false);
INSERT INTO public.bi_fato_financeiro VALUES (7, 'PREVISTO', 'titulos_receber', '63dc6813-5abe-4e1d-aaad-5c79edff406e', 49, 1, 8, 'ENTRADA', 45.63, 0.00, true);
INSERT INTO public.bi_fato_financeiro VALUES (8, 'PREVISTO', 'titulos_receber', '73d98f32-663b-4dfe-ab13-6127956a0752', 61, 1, 1, 'ENTRADA', 192.78, 0.00, true);
INSERT INTO public.bi_fato_financeiro VALUES (9, 'PREVISTO', 'titulos_receber', 'b3e47882-e544-44e9-9cc4-ade36273bea2', 62, 1, 6, 'ENTRADA', 374.64, 0.00, true);
INSERT INTO public.bi_fato_financeiro VALUES (10, 'PREVISTO', 'titulos_receber', 'ed3f1ffa-3440-43ef-9dcc-b835e2e3573a', 63, 1, 7, 'ENTRADA', 555.38, 0.00, true);
INSERT INTO public.bi_fato_financeiro VALUES (11, 'PREVISTO', 'titulos_receber', '9849139b-af87-4653-ba8d-251768147e60', 64, 1, 5, 'ENTRADA', 727.68, 0.00, true);
INSERT INTO public.bi_fato_financeiro VALUES (12, 'PREVISTO', 'titulos_receber', '402f1860-9f4a-45eb-bb3c-9c6d88ea7b32', 64, 1, 4, 'ENTRADA', 495.91, 0.00, true);
INSERT INTO public.bi_fato_financeiro VALUES (13, 'PREVISTO', 'titulos_receber', '75ba20fe-8371-411d-b1ba-e45a45974a16', 83, 1, 5, 'ENTRADA', 655.20, 0.00, true);
INSERT INTO public.bi_fato_financeiro VALUES (14, 'PREVISTO', 'titulos_receber', '0458f0be-868c-468e-9d2c-cfe2f8b192f0', 89, 1, 4, 'ENTRADA', 427.86, 0.00, true);
INSERT INTO public.bi_fato_financeiro VALUES (15, 'PREVISTO', 'titulos_receber', 'a1604a72-df2f-455a-98d8-833649058890', 92, 1, 1, 'ENTRADA', 636.12, 0.00, true);
INSERT INTO public.bi_fato_financeiro VALUES (16, 'PREVISTO', 'titulos_receber', '9c2f7622-dadb-4c8e-aa4c-1d5de73e480b', 92, 1, 7, 'ENTRADA', 892.48, 0.00, true);
INSERT INTO public.bi_fato_financeiro VALUES (17, 'PREVISTO', 'titulos_receber', '564aca28-317a-4689-8dc7-1573ad29cd4b', 94, 1, 3, 'ENTRADA', 713.67, 0.00, true);
INSERT INTO public.bi_fato_financeiro VALUES (18, 'PREVISTO', 'titulos_pagar', '9b78e4f6-ee4b-4d47-b7c0-f3a300d89d2b', 102, 1, NULL, 'SAIDA', 780.60, 0.00, false);
INSERT INTO public.bi_fato_financeiro VALUES (19, 'PREVISTO', 'titulos_pagar', 'de7efd38-29bb-41b8-af2b-20f1c35a71d3', 71, 1, NULL, 'SAIDA', 138.12, 0.00, false);
INSERT INTO public.bi_fato_financeiro VALUES (20, 'PREVISTO', 'titulos_pagar', '409c1c6f-e962-4eb8-b161-c88c3cf25274', 41, 1, NULL, 'SAIDA', 652.53, 0.00, false);
INSERT INTO public.bi_fato_financeiro VALUES (21, 'PREVISTO', 'titulos_pagar', '8aa78aa5-0c44-4014-8bd9-8ba0753beaf0', 41, 1, NULL, 'SAIDA', 348.09, 0.00, false);
INSERT INTO public.bi_fato_financeiro VALUES (22, 'PREVISTO', 'titulos_pagar', '191e45f5-9f86-4a0f-bbaf-aae4088c1d16', 41, 1, NULL, 'SAIDA', 139.97, 0.00, true);
INSERT INTO public.bi_fato_financeiro VALUES (23, 'PREVISTO', 'titulos_pagar', 'f5c1c84b-8fe0-43a8-ad96-23231a9245b6', 41, 1, NULL, 'SAIDA', 210.49, 0.00, true);
INSERT INTO public.bi_fato_financeiro VALUES (24, 'PREVISTO', 'titulos_pagar', 'b2b7c1f4-9f46-446b-a150-f415819d339f', 41, 1, NULL, 'SAIDA', 253.17, 0.00, true);
INSERT INTO public.bi_fato_financeiro VALUES (25, 'PREVISTO', 'titulos_pagar', '4ef9baf2-1421-4619-941a-8ec2fdab5854', 41, 1, NULL, 'SAIDA', 192.60, 0.00, true);
INSERT INTO public.bi_fato_financeiro VALUES (26, 'PREVISTO', 'titulos_pagar', '97302a6f-f19e-41cb-825a-f791b1c24880', 41, 1, NULL, 'SAIDA', 1658.32, 0.00, true);
INSERT INTO public.bi_fato_financeiro VALUES (27, 'PREVISTO', 'titulos_pagar', '0fcf6402-3354-48fa-a9b4-3f204c42a8d7', 71, 1, NULL, 'SAIDA', 208.33, 0.00, true);
INSERT INTO public.bi_fato_financeiro VALUES (28, 'PREVISTO', 'titulos_pagar', '50adf9eb-5902-4c63-b95d-7339c90f4d1a', 71, 1, NULL, 'SAIDA', 241.80, 0.00, true);
INSERT INTO public.bi_fato_financeiro VALUES (29, 'PREVISTO', 'titulos_pagar', '8731cc1a-1478-4344-ad6e-306ed8ba1f23', 71, 1, NULL, 'SAIDA', 365.45, 0.00, true);
INSERT INTO public.bi_fato_financeiro VALUES (30, 'PREVISTO', 'titulos_pagar', 'f2dd8f6a-d756-4b6a-87e6-0fe15d379fb4', 71, 1, NULL, 'SAIDA', 183.62, 0.00, true);
INSERT INTO public.bi_fato_financeiro VALUES (31, 'PREVISTO', 'titulos_pagar', '40362736-545f-4704-b43b-47f8ab2f1d9b', 71, 1, NULL, 'SAIDA', 793.04, 0.00, true);
INSERT INTO public.bi_fato_financeiro VALUES (32, 'PREVISTO', 'titulos_pagar', '3b4e6c3b-8361-4bd9-bf41-c9671f8f6ea5', 71, 1, NULL, 'SAIDA', 1687.55, 0.00, true);
INSERT INTO public.bi_fato_financeiro VALUES (33, 'PREVISTO', 'titulos_pagar', '4543e40b-be45-4fee-9fe9-a3c6f3f235e8', 102, 1, NULL, 'SAIDA', 166.77, 0.00, true);
INSERT INTO public.bi_fato_financeiro VALUES (34, 'PREVISTO', 'titulos_pagar', '4422a98d-7622-48c5-8621-16bcfd51b5a2', 102, 1, NULL, 'SAIDA', 176.79, 0.00, true);
INSERT INTO public.bi_fato_financeiro VALUES (35, 'PREVISTO', 'titulos_pagar', '3a99c818-7c40-4a43-af1a-2a3c462a5c3f', 102, 1, NULL, 'SAIDA', 237.61, 0.00, true);
INSERT INTO public.bi_fato_financeiro VALUES (36, 'PREVISTO', 'titulos_pagar', 'f6036a0f-2a87-4121-b8cc-a72289eb3d5a', 102, 1, NULL, 'SAIDA', 341.36, 0.00, true);
INSERT INTO public.bi_fato_financeiro VALUES (37, 'PREVISTO', 'titulos_pagar', 'cd5096b2-21c7-4cc0-a600-f5fec69b42ea', 102, 1, NULL, 'SAIDA', 169.34, 0.00, true);
INSERT INTO public.bi_fato_financeiro VALUES (38, 'PREVISTO', 'titulos_pagar', '1c9dc92f-1c60-449b-bfbf-ecd10f6c78a7', 102, 1, NULL, 'SAIDA', 1894.87, 0.00, true);
INSERT INTO public.bi_fato_financeiro VALUES (39, 'PREVISTO', 'titulos_pagar', '8c76c90c-72c6-4486-9ee8-8af26834f9f0', 116, 1, NULL, 'SAIDA', 259.92, 0.00, false);
INSERT INTO public.bi_fato_financeiro VALUES (40, 'PREVISTO', 'titulos_pagar', 'f39385b6-f4e2-4948-b5b3-d4a81513e385', 112, 1, NULL, 'SAIDA', 570.00, 0.00, false);
INSERT INTO public.bi_fato_financeiro VALUES (41, 'PREVISTO', 'titulos_pagar', 'cef140c2-b047-4137-9c79-d10ab93df41a', 43, 1, NULL, 'SAIDA', 654.68, 0.00, false);
INSERT INTO public.bi_fato_financeiro VALUES (42, 'PREVISTO', 'titulos_pagar', 'b782070c-a88c-4b95-b365-5e7dfa23fe81', 111, 1, NULL, 'SAIDA', 739.84, 0.00, false);
INSERT INTO public.bi_fato_financeiro VALUES (43, 'PREVISTO', 'titulos_pagar', '5a89fed2-73c5-42db-aa48-c499881ac6b0', 57, 1, NULL, 'SAIDA', 729.44, 0.00, false);
INSERT INTO public.bi_fato_financeiro VALUES (44, 'PREVISTO', 'titulos_pagar', '42ab183e-3137-41ce-b9f2-30dbfedff1a6', 54, 1, NULL, 'SAIDA', 568.98, 0.00, false);
INSERT INTO public.bi_fato_financeiro VALUES (45, 'PREVISTO', 'titulos_pagar', 'f5a45121-6670-46a5-9d44-d22a24d52836', 109, 1, NULL, 'SAIDA', 578.48, 0.00, false);
INSERT INTO public.bi_fato_financeiro VALUES (46, 'PREVISTO', 'titulos_pagar', '659f5fbe-03d3-463b-8e7c-59a937e1c336', 121, 1, NULL, 'SAIDA', 659.94, 0.00, false);
INSERT INTO public.bi_fato_financeiro VALUES (47, 'PREVISTO', 'titulos_pagar', '3e60139b-c06e-46cc-8dc9-d1572667f04a', 123, 1, NULL, 'SAIDA', 384.57, 0.00, false);
INSERT INTO public.bi_fato_financeiro VALUES (48, 'PREVISTO', 'titulos_pagar', 'f9b7eabd-5358-458e-84f8-c13940230591', 72, 1, NULL, 'SAIDA', 471.64, 0.00, false);
INSERT INTO public.bi_fato_financeiro VALUES (49, 'PREVISTO', 'titulos_pagar', '1755bbb4-5444-4249-8bfa-b5a22b6d8f72', 57, 1, NULL, 'SAIDA', 245.76, 0.00, false);
INSERT INTO public.bi_fato_financeiro VALUES (50, 'PREVISTO', 'titulos_pagar', 'ff783707-2f94-4437-8a79-c04a778f3e91', 49, 1, NULL, 'SAIDA', 630.82, 0.00, false);
INSERT INTO public.bi_fato_financeiro VALUES (51, 'PREVISTO', 'titulos_pagar', '6ca055dd-2bbb-4bc0-8cfd-6c9f825e9f31', 55, 1, NULL, 'SAIDA', 734.36, 0.00, false);
INSERT INTO public.bi_fato_financeiro VALUES (52, 'PREVISTO', 'titulos_pagar', '410726e8-d02c-40fb-be8d-13540138ee43', 65, 1, NULL, 'SAIDA', 1062.78, 0.00, false);
INSERT INTO public.bi_fato_financeiro VALUES (53, 'PREVISTO', 'titulos_pagar', '11aadaab-2627-4e66-9070-b9be20560831', 88, 1, NULL, 'SAIDA', 334.74, 0.00, false);
INSERT INTO public.bi_fato_financeiro VALUES (54, 'PREVISTO', 'titulos_pagar', 'ab6e5347-1e77-48a3-bbc4-904dc3480dc0', 88, 1, NULL, 'SAIDA', 96.69, 0.00, false);
INSERT INTO public.bi_fato_financeiro VALUES (55, 'PREVISTO', 'titulos_pagar', 'f1979186-3dc7-47c3-b428-b210a6bdad9b', 88, 1, NULL, 'SAIDA', 839.53, 0.00, false);
INSERT INTO public.bi_fato_financeiro VALUES (56, 'PREVISTO', 'titulos_pagar', '913ab651-3f8e-478c-9634-57b2ed0c87e1', 124, 1, NULL, 'SAIDA', 145.04, 0.00, false);
INSERT INTO public.bi_fato_financeiro VALUES (57, 'PREVISTO', 'titulos_pagar', 'fd5b85db-41f9-47bb-acb1-780863bf76bf', 74, 1, NULL, 'SAIDA', 453.55, 0.00, false);
INSERT INTO public.bi_fato_financeiro VALUES (58, 'PREVISTO', 'titulos_pagar', '255880fd-9496-474d-9bd6-2ee13a4e0203', 55, 1, NULL, 'SAIDA', 418.20, 0.00, false);
INSERT INTO public.bi_fato_financeiro VALUES (59, 'PREVISTO', 'titulos_pagar', '42ed46ef-bdef-402a-ba52-7715f1f99fbe', 94, 1, NULL, 'SAIDA', 193.42, 0.00, false);
INSERT INTO public.bi_fato_financeiro VALUES (60, 'CAIXA', 'movimentos_caixa', '11749b4f-a081-441e-b0ea-04df60aa51cd', 53, 1, 8, 'ENTRADA', 0.00, 45.63, true);
INSERT INTO public.bi_fato_financeiro VALUES (61, 'CAIXA', 'movimentos_caixa', '12741f78-1f19-4fe7-96d6-3743c3227a7a', 68, 1, 1, 'ENTRADA', 0.00, 144.95, true);
INSERT INTO public.bi_fato_financeiro VALUES (62, 'CAIXA', 'movimentos_caixa', '972a1a4c-33d8-4a67-84b4-676767c54e15', 62, 1, 6, 'ENTRADA', 0.00, 374.64, true);
INSERT INTO public.bi_fato_financeiro VALUES (63, 'CAIXA', 'movimentos_caixa', '40d99163-4cb3-41b7-86cd-0de4528cc329', 71, 1, 7, 'ENTRADA', 0.00, 555.38, true);
INSERT INTO public.bi_fato_financeiro VALUES (64, 'CAIXA', 'movimentos_caixa', '964394ea-63f1-49db-8cdb-1e658ab5af12', 70, 1, 5, 'ENTRADA', 0.00, 727.68, true);
INSERT INTO public.bi_fato_financeiro VALUES (65, 'CAIXA', 'movimentos_caixa', '70fd9cb5-2aac-44bb-a12a-3ae2cbd4ef85', 68, 1, 4, 'ENTRADA', 0.00, 495.91, true);
INSERT INTO public.bi_fato_financeiro VALUES (66, 'CAIXA', 'movimentos_caixa', '41dab178-7fa9-4834-b8a7-44d662476a20', 88, 1, 5, 'ENTRADA', 0.00, 552.89, true);
INSERT INTO public.bi_fato_financeiro VALUES (67, 'CAIXA', 'movimentos_caixa', '8ba80c7a-341d-42a4-ad62-dff0fc47df57', 91, 1, 4, 'ENTRADA', 0.00, 427.86, true);
INSERT INTO public.bi_fato_financeiro VALUES (68, 'CAIXA', 'movimentos_caixa', 'a3c83f97-580b-48e8-9e7c-10980dd323fb', 95, 1, 1, 'ENTRADA', 0.00, 636.12, true);
INSERT INTO public.bi_fato_financeiro VALUES (69, 'CAIXA', 'movimentos_caixa', 'f49af4cb-f879-4954-97f7-7cf7cb829960', 99, 1, 7, 'ENTRADA', 0.00, 726.92, true);
INSERT INTO public.bi_fato_financeiro VALUES (70, 'CAIXA', 'movimentos_caixa', '182f9557-700d-4788-a27e-2b1e347357ad', 96, 1, 3, 'ENTRADA', 0.00, 713.67, true);
INSERT INTO public.bi_fato_financeiro VALUES (71, 'CAIXA', 'movimentos_caixa', 'c6fcf474-b7c9-48da-a466-110cfdb70875', 41, 1, NULL, 'SAIDA', 0.00, 139.97, true);
INSERT INTO public.bi_fato_financeiro VALUES (72, 'CAIXA', 'movimentos_caixa', '739e8feb-c76d-4825-aefa-bf8eef96be43', 47, 1, NULL, 'SAIDA', 0.00, 210.49, true);
INSERT INTO public.bi_fato_financeiro VALUES (73, 'CAIXA', 'movimentos_caixa', '1444f996-01b7-4e3b-9eea-df3c959b19da', 45, 1, NULL, 'SAIDA', 0.00, 253.17, true);
INSERT INTO public.bi_fato_financeiro VALUES (74, 'CAIXA', 'movimentos_caixa', '0321a296-d08e-4dd4-bc78-174b3d05ffa9', 46, 1, NULL, 'SAIDA', 0.00, 192.60, true);
INSERT INTO public.bi_fato_financeiro VALUES (75, 'CAIXA', 'movimentos_caixa', '14ad2134-759d-49d6-b7a7-8fac85308232', 50, 1, NULL, 'SAIDA', 0.00, 1658.32, true);
INSERT INTO public.bi_fato_financeiro VALUES (76, 'CAIXA', 'movimentos_caixa', 'a1e298e6-e4c2-4319-a319-6b9680a99ba4', 74, 1, NULL, 'SAIDA', 0.00, 208.33, true);
INSERT INTO public.bi_fato_financeiro VALUES (77, 'CAIXA', 'movimentos_caixa', 'aa90b5af-c153-4b62-9280-5b80dcac4e26', 80, 1, NULL, 'SAIDA', 0.00, 241.80, true);
INSERT INTO public.bi_fato_financeiro VALUES (78, 'CAIXA', 'movimentos_caixa', '48154c04-0529-4317-ae16-90789daf20ce', 75, 1, NULL, 'SAIDA', 0.00, 365.45, true);
INSERT INTO public.bi_fato_financeiro VALUES (79, 'CAIXA', 'movimentos_caixa', 'e29ef225-441c-4f73-a610-7395561cbbbc', 75, 1, NULL, 'SAIDA', 0.00, 183.62, true);
INSERT INTO public.bi_fato_financeiro VALUES (80, 'CAIXA', 'movimentos_caixa', 'f0426f0d-3de2-451e-a7f9-66a09d704f09', 80, 1, NULL, 'SAIDA', 0.00, 793.04, true);
INSERT INTO public.bi_fato_financeiro VALUES (81, 'CAIXA', 'movimentos_caixa', 'b7461fd5-f350-47d3-b08d-bbfa7a34bee1', 74, 1, NULL, 'SAIDA', 0.00, 1687.55, true);
INSERT INTO public.bi_fato_financeiro VALUES (82, 'CAIXA', 'movimentos_caixa', 'c2e5d73d-2181-4c62-93f2-f636c89fa9e3', 102, 1, NULL, 'SAIDA', 0.00, 166.77, true);
INSERT INTO public.bi_fato_financeiro VALUES (83, 'CAIXA', 'movimentos_caixa', '2e5d0915-c988-45ee-bc4c-79be5bd701f2', 102, 1, NULL, 'SAIDA', 0.00, 176.79, true);
INSERT INTO public.bi_fato_financeiro VALUES (84, 'CAIXA', 'movimentos_caixa', '03f0ba14-00f2-4b2f-8e0f-aaaeac2acb36', 102, 1, NULL, 'SAIDA', 0.00, 237.61, true);
INSERT INTO public.bi_fato_financeiro VALUES (85, 'CAIXA', 'movimentos_caixa', '0aebaa78-8c05-4f22-8dfa-23e12f5293d1', 102, 1, NULL, 'SAIDA', 0.00, 341.36, true);
INSERT INTO public.bi_fato_financeiro VALUES (86, 'CAIXA', 'movimentos_caixa', '148bcfff-2c89-4790-8a1b-ac7007afb034', 101, 1, NULL, 'SAIDA', 0.00, 169.34, true);
INSERT INTO public.bi_fato_financeiro VALUES (87, 'CAIXA', 'movimentos_caixa', '91e04f11-2fb5-49c4-bb00-20e482bb2675', 102, 1, NULL, 'SAIDA', 0.00, 1894.87, true);


--
-- Data for Name: bi_fato_glosa; Type: TABLE DATA; Schema: public; Owner: labvida
--

INSERT INTO public.bi_fato_glosa VALUES (1, '7563aded-0005-4a76-8f46-da0c6120123f', 102, 5, 4, 21, 4, 12.45, 24.90, 1);
INSERT INTO public.bi_fato_glosa VALUES (2, '4497a51c-b1b6-4b39-b366-eff5c6c04040', 102, 5, 4, 11, 4, 4.56, 9.13, 1);
INSERT INTO public.bi_fato_glosa VALUES (3, 'fd9eca11-f4ad-462e-be11-b4befef34f34', 102, 5, 4, 24, 6, 11.95, 39.84, 1);
INSERT INTO public.bi_fato_glosa VALUES (4, '2167a585-5164-4a5f-96cb-e7620980e8e9', 102, 3, 4, 4, 3, 5.97, 19.92, 1);
INSERT INTO public.bi_fato_glosa VALUES (5, 'b81e5931-4a9e-4c8b-a322-c9f9f498dc41', 102, 3, 4, 7, 9, 3.48, 11.62, 1);
INSERT INTO public.bi_fato_glosa VALUES (6, '3e31f3cb-62e0-4b52-aa7d-98be67d5f4d4', 102, 3, 4, 28, 5, 7.47, 14.94, 1);
INSERT INTO public.bi_fato_glosa VALUES (7, '463de3d7-36f4-4332-a5df-c31533596f28', 102, 3, 4, 30, 3, 5.72, 19.09, 1);
INSERT INTO public.bi_fato_glosa VALUES (8, '822c776f-c8d1-4428-b980-b1dd1f2bce59', 102, 3, 4, 16, 9, 14.11, 14.11, 1);
INSERT INTO public.bi_fato_glosa VALUES (9, '9f3f3015-c8e9-43dc-b46f-99cc90eb9dad', 102, 4, 7, 11, 5, 5.44, 10.89, 1);
INSERT INTO public.bi_fato_glosa VALUES (10, 'c0361290-de72-4c56-83e3-9a99cdbfac44', 102, 5, 7, 27, 9, 20.79, 20.79, 1);
INSERT INTO public.bi_fato_glosa VALUES (11, '5570e7b5-391e-49d5-9fd0-f27eb0acd369', 102, 4, 7, 23, 9, 13.36, 44.55, 1);
INSERT INTO public.bi_fato_glosa VALUES (12, '50387ece-1e90-4f61-a3af-6498ef14cdfd', 102, 5, 7, 14, 7, 4.00, 13.36, 1);
INSERT INTO public.bi_fato_glosa VALUES (13, '6d6edc37-7b50-48a7-bb08-90239af40523', 102, 5, 7, 18, 6, 18.81, 18.81, 1);
INSERT INTO public.bi_fato_glosa VALUES (14, 'b828e3ac-c0ea-4fc3-ae80-915810cfdc78', 102, 5, 7, 1, 7, 28.22, 28.22, 1);
INSERT INTO public.bi_fato_glosa VALUES (15, 'b7648cb7-9c8a-4792-81a9-e4e8aa33610f', 102, 2, 7, 4, 3, 23.76, 23.76, 1);
INSERT INTO public.bi_fato_glosa VALUES (16, '57aa3b8a-9369-4c1f-b3db-74fe086dc500', 102, 5, 7, 4, 8, 23.76, 23.76, 1);
INSERT INTO public.bi_fato_glosa VALUES (17, '1fee556f-8917-40fc-a733-eea36a9df571', 102, 3, 7, 21, 6, 14.85, 29.70, 1);
INSERT INTO public.bi_fato_glosa VALUES (18, 'de35a8ac-0e7f-4161-bc90-06578a62bf0f', 102, 2, 7, 17, 5, 16.34, 16.34, 1);
INSERT INTO public.bi_fato_glosa VALUES (19, '8f131048-ea3e-4ad3-92fe-6e11ee3b19e5', 102, 4, 7, 16, 8, 16.83, 16.83, 1);
INSERT INTO public.bi_fato_glosa VALUES (20, '3302963b-1bef-47f5-aa33-af9e610364fa', 102, 4, 8, 26, 5, 24.57, 49.14, 1);
INSERT INTO public.bi_fato_glosa VALUES (21, '6ad3d612-f2c5-43e6-85a3-b0da3139e5a5', 102, 4, 8, 16, 6, 5.96, 19.89, 1);
INSERT INTO public.bi_fato_glosa VALUES (22, '9f8e007d-1fea-4139-8b3c-41cd070ccb9e', 102, 3, 8, 11, 9, 6.43, 12.87, 1);
INSERT INTO public.bi_fato_glosa VALUES (23, '908efb25-1e8a-467f-8d27-43ab4c7387c6', 102, 3, 8, 18, 3, 22.23, 22.23, 1);
INSERT INTO public.bi_fato_glosa VALUES (24, '99f6a924-a400-4b16-bb66-a3d409f029c1', 102, 3, 3, 30, 4, 12.30, 24.61, 1);
INSERT INTO public.bi_fato_glosa VALUES (25, '87d89f45-a15b-461a-93d6-4b5de2b71e0f', 102, 2, 3, 19, 6, 12.19, 40.66, 1);
INSERT INTO public.bi_fato_glosa VALUES (26, 'f8afb55c-f454-462e-a40d-a1c2833213cc', 102, 2, 3, 8, 7, 5.13, 17.12, 1);
INSERT INTO public.bi_fato_glosa VALUES (27, '52d8bbf5-bcb4-42ee-9d1d-3934d26a0322', 102, 3, 3, 1, 6, 30.50, 30.50, 1);
INSERT INTO public.bi_fato_glosa VALUES (28, 'ff2cae2b-ce0f-4f57-9331-b4a513bf74bf', 102, 2, 3, 15, 6, 14.44, 14.44, 1);
INSERT INTO public.bi_fato_glosa VALUES (29, '38259a00-6cc0-4816-92a5-c479af27e94e', 102, 5, 3, 15, 7, 14.44, 14.44, 1);
INSERT INTO public.bi_fato_glosa VALUES (30, '5874ac1c-ce50-49fe-8105-4bf4ecddd3b4', 102, 2, 3, 10, 8, 16.58, 16.58, 1);
INSERT INTO public.bi_fato_glosa VALUES (31, '2003e4be-50f4-4be3-a463-3ff323dd5f1b', 102, 4, 3, 18, 9, 20.33, 20.33, 1);
INSERT INTO public.bi_fato_glosa VALUES (32, '3ad90ecd-8098-4aa6-806a-8de7d7ff980d', 102, 2, 6, 2, 4, 16.80, 16.80, 1);
INSERT INTO public.bi_fato_glosa VALUES (33, '70075059-a7b8-4e79-b4aa-6cc1799800ac', 102, 5, 6, 1, 3, 31.92, 31.92, 1);
INSERT INTO public.bi_fato_glosa VALUES (34, '360880de-00c3-4c00-b5e3-18c59f4cbf1a', 102, 5, 6, 24, 3, 53.76, 53.76, 1);
INSERT INTO public.bi_fato_glosa VALUES (35, '9672b5ec-bff0-4e7f-a849-18cbdf2fb460', 102, 3, 6, 22, 3, 34.72, 69.44, 1);
INSERT INTO public.bi_fato_glosa VALUES (36, '87712950-ad86-40b4-8d82-bf7060bb4145', 102, 4, 6, 14, 8, 7.56, 15.12, 1);
INSERT INTO public.bi_fato_glosa VALUES (37, 'f3ed7631-a67f-4aef-9647-e921dc8cd4af', 102, 3, 6, 8, 8, 8.96, 17.92, 1);
INSERT INTO public.bi_fato_glosa VALUES (38, '217e67fb-9504-42d4-a01a-6789b0840863', 102, 4, 6, 15, 5, 15.12, 15.12, 1);
INSERT INTO public.bi_fato_glosa VALUES (39, '8f253379-881b-42a9-a73c-d1747ac1367a', 102, 5, 6, 20, 8, 35.84, 35.84, 1);
INSERT INTO public.bi_fato_glosa VALUES (40, 'bbffa9e4-eb28-47e9-aa19-bd8bf5345e3d', 102, 5, 5, 11, 8, 3.16, 10.56, 1);
INSERT INTO public.bi_fato_glosa VALUES (41, 'ab3557e5-9748-47f4-9c53-92009d952c0f', 102, 4, 5, 29, 9, 14.97, 49.92, 1);
INSERT INTO public.bi_fato_glosa VALUES (42, 'ace1f5ea-29a5-49c1-a345-e8c6d7be2d81', 102, 5, 5, 7, 9, 13.44, 13.44, 1);
INSERT INTO public.bi_fato_glosa VALUES (43, '564a3225-4a6d-4690-ba7b-9f82832969a3', 102, 5, 5, 1, 2, 8.20, 27.36, 1);
INSERT INTO public.bi_fato_glosa VALUES (44, 'ca9f9e4e-3149-4a20-9c02-b65b1bf1b4dc', 102, 5, 5, 5, 7, 16.32, 32.64, 1);
INSERT INTO public.bi_fato_glosa VALUES (45, '7b1a4680-01a1-4ca9-86c6-31e78cf2cde4', 102, 3, 5, 12, 5, 3.31, 11.04, 1);
INSERT INTO public.bi_fato_glosa VALUES (46, '0e239f19-fe91-49f0-82c8-597dfa915945', 102, 2, 5, 16, 2, 4.89, 16.32, 1);
INSERT INTO public.bi_fato_glosa VALUES (47, '41a72fcb-d9fa-4534-a550-b68f21a3fc1e', 102, 5, 1, 15, 3, 14.58, 14.58, 1);
INSERT INTO public.bi_fato_glosa VALUES (48, '4d540db8-5545-4baa-a16c-acfd4efc196f', 102, 5, 1, 3, 7, 23.76, 23.76, 1);
INSERT INTO public.bi_fato_glosa VALUES (49, 'b54e47be-eb11-41cd-8516-dec2c23e8987', 102, 5, 1, 4, 8, 12.96, 25.92, 1);
INSERT INTO public.bi_fato_glosa VALUES (50, '2553881b-66cd-4f95-bc0a-5c1193c6368f', 102, 2, 1, 18, 7, 10.26, 20.52, 1);
INSERT INTO public.bi_fato_glosa VALUES (51, '73b66ac9-a007-4633-ad57-8d481ea22f48', 102, 5, 1, 10, 2, 5.02, 16.74, 1);
INSERT INTO public.bi_fato_glosa VALUES (52, '356bc9ac-cd96-4df2-82ce-fcce919fb8d8', 102, 4, 1, 8, 6, 5.18, 17.28, 1);
INSERT INTO public.bi_fato_glosa VALUES (53, 'c4bd7bd1-8d4c-435f-87e6-e961af55c1f5', 102, 4, 1, 25, 8, 14.04, 28.08, 1);
INSERT INTO public.bi_fato_glosa VALUES (54, '61c4964b-0dce-4cb7-80ea-2da906335f2a', 102, 4, 1, 12, 5, 12.42, 12.42, 1);
INSERT INTO public.bi_fato_glosa VALUES (55, 'f42db046-1afc-4224-ac33-622521541f07', 102, 5, 1, 24, 4, 51.84, 51.84, 1);


--
-- Data for Name: bi_fato_logistica; Type: TABLE DATA; Schema: public; Owner: labvida
--

INSERT INTO public.bi_fato_logistica VALUES (1, '4a93e967-607d-423f-8ea6-3d6ab7799876', 20, 4, 1, 1, 1.17, 4.40, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (2, 'ce8fc2c9-bfcf-4f0d-a119-14558b00a95c', 20, 4, 1, 1, 1.17, 10.05, true, 1, 'REJEITADA');
INSERT INTO public.bi_fato_logistica VALUES (3, 'ff953cda-1e97-4315-a368-e74079781b20', 20, 4, 1, 1, 1.17, 7.88, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (4, '5d1c2560-f402-4900-80fc-2f829b800095', 17, 4, 1, 1, 3.54, 18.68, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (5, '5f1d17de-a49b-41f7-8a4d-1900e0ccc49f', 17, 4, 1, 1, 3.54, 11.70, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (6, '5fa27c09-d7c2-475e-b385-12765ba0a528', 17, 4, 1, 1, 3.54, 11.38, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (7, '9ea04880-534f-4f95-a022-032c823702e2', 17, 4, 1, 1, 3.54, 8.60, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (8, 'c22894cc-98ca-4104-a312-0c73dbfa02b5', 17, 4, 1, 1, 3.54, 17.56, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (9, 'a4d46c7b-d7d5-41cc-8a83-a4193cbca9b4', 15, 3, 1, 1, 2.99, 7.92, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (10, 'ba1bd1bc-5c11-4334-831e-2d4d963c1a31', 15, 3, 1, 1, 2.99, 7.73, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (11, 'fbac52c6-4cfe-47ae-b87c-fddb6b93a13d', 15, 3, 1, 1, 2.99, 7.15, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (12, 'b08d9949-1223-47d7-8f80-e3410b795ecf', 26, 5, 1, 1, 4.10, 12.73, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (13, 'ec324dca-c66b-4d48-84c3-b10433fe337a', 26, 5, 1, 1, 4.10, 9.82, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (14, '71be3c28-f74f-4c1b-b2bf-16a3f7e5bd17', 16, 5, 1, 1, 3.39, 12.74, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (15, '992399e2-d524-404e-be64-142d66337c1f', 16, 5, 1, 1, 3.39, 5.57, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (16, '019483d6-51cb-49f6-a785-afb4c197f855', 20, 5, 1, 1, 3.57, 12.57, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (17, '01d75b28-3f0b-4bf0-883d-0193f25e6858', 20, 5, 1, 1, 3.57, 14.56, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (18, '450b06bc-41ac-4257-9a31-7a1ba320446a', 20, 5, 1, 1, 3.57, 13.98, true, 1, 'REJEITADA');
INSERT INTO public.bi_fato_logistica VALUES (19, 'a2768339-f07b-4a8d-98f6-0d84e2571c0a', 20, 5, 1, 1, 3.57, 9.14, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (20, '82a931ea-26d1-4009-a664-b1ad7977f77a', 20, 5, 1, 1, 2.52, 8.26, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (21, '025bd3e9-2a62-4e50-98fd-5908e8d52c6c', 21, 5, 1, 1, 3.44, 10.29, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (22, '0fde57ef-550d-4f22-b3ae-f992ef9c3ff3', 21, 5, 1, 1, 3.44, 11.38, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (23, '32f4387c-5204-481d-ac4b-dbb0bcfca577', 21, 5, 1, 1, 3.44, 7.73, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (24, '6d9ac63c-5248-4ea8-a57d-11775dcae0fb', 21, 5, 1, 1, 3.44, 7.75, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (25, '024c36de-cc0f-4fdd-9de8-6c7bcbe48699', 27, 4, 1, 1, 1.86, 5.65, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (26, 'db93b270-07a2-47c3-96db-1373da0e4b1a', 27, 4, 1, 1, 1.86, 12.55, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (27, '3854f161-5bc8-40a1-a68d-1dd5c66e5323', 25, 5, 1, 1, 3.50, 20.24, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (28, '6abee82a-96f8-4f9e-adc6-43b9e7ae7660', 25, 5, 1, 1, 3.50, 7.58, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (29, 'b05939a5-732d-44fb-9d68-bcb90315c2e2', 25, 5, 1, 1, 3.50, 11.11, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (30, 'ebd80de2-a051-4b80-a2c3-b6fc5ee4f3e4', 25, 5, 1, 1, 3.50, 15.02, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (31, '37f69d2f-0a8e-4875-994b-e78ad5e83407', 28, 2, 1, 1, 1.98, 4.10, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (32, 'c0a931f4-f1c6-43eb-b0fb-842914aa857d', 28, 2, 1, 1, 1.98, 12.51, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (33, 'd1d511a5-1cac-483c-9b77-b82fe931500a', 28, 2, 1, 1, 1.98, 3.49, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (34, 'd6b2974f-71f4-4c29-9a53-1f77384256a0', 28, 2, 1, 1, 1.98, 8.36, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (35, 'dd5da1da-18b7-4a04-9eba-2461f8e9c06f', 28, 2, 1, 1, 1.98, 8.45, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (36, '823f5757-ada8-4fdd-8e42-5d70e6608a1f', 31, 2, 1, 1, 4.06, 8.32, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (37, '02071ab5-1017-48e9-b68e-c97d7994a585', 30, 5, 1, 1, 4.67, 14.51, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (38, '8e129d10-2dfc-41f7-a214-6909532a98db', 30, 5, 1, 1, 4.67, 8.92, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (39, '3c83d32c-4f4c-4781-a098-4751319aa61b', 27, 5, 1, 1, 2.90, 8.90, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (40, '418d5f9d-38f0-4708-8c6e-be59d23a7354', 27, 5, 1, 1, 2.90, 6.18, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (41, '6f7f8917-0ae8-4464-991d-5778264af0bd', 27, 5, 1, 1, 2.90, 11.10, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (42, 'b37c06ce-c0a2-4f83-96d0-bf804e05f228', 27, 5, 1, 1, 2.90, 12.09, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (43, '458ad56c-2519-425f-8cf2-2a2f4ef62b31', 30, 2, 1, 1, 4.97, 6.29, true, 1, 'REJEITADA');
INSERT INTO public.bi_fato_logistica VALUES (44, 'a503e97e-94d0-4ad4-90c4-4e06e3c1adc4', 30, 2, 1, 1, 4.97, 7.22, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (45, 'c74d1fae-00ea-4835-814c-04516ea95240', 30, 5, 1, 1, 4.67, 12.84, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (46, 'ef48cc6f-d6cb-4e89-89d9-cc62468018ad', 37, 3, 1, 1, 3.17, 8.73, true, 1, 'REJEITADA');
INSERT INTO public.bi_fato_logistica VALUES (47, '3d6571dd-e0e7-4f3b-a656-eef0ab810b55', 37, 3, 1, 1, 1.51, 4.56, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (48, '097925f2-fe06-49c4-88ff-58bac03de62e', 32, 4, 1, 1, 3.95, 7.12, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (49, '38eb198d-fbf6-4cd5-a373-cf4926beb6a6', 32, 4, 1, 1, 3.95, 6.16, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (50, 'af582513-5930-4efc-89e3-18bb025f46f8', 32, 4, 1, 1, 3.95, 12.81, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (51, '7585d0ff-1d32-4265-9716-43a16bd07d35', 37, 3, 1, 1, 1.51, 5.27, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (52, 'a5ebfead-ec16-41d6-b522-8616abcffaad', 20, 3, 1, 1, 3.15, 7.22, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (53, '872bffe2-0fbb-414c-81c7-20bf51fbeb9f', 37, 3, 1, 1, 1.51, 6.52, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (54, '93682f3f-ca88-479b-8268-8193f281b0ca', 37, 3, 1, 1, 1.51, 6.63, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (55, '952206a4-122d-4201-b245-d13962946ae6', 37, 3, 1, 1, 1.51, 11.50, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (56, 'ea88e02a-ab17-4fd7-8487-53df754f5f66', 37, 3, 1, 1, 1.51, 11.09, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (57, '73d617b0-5308-4b18-b75e-03de666d9837', 31, 2, 1, 1, 4.06, 7.25, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (58, '37aa6f18-3ee4-4af1-8b21-54689766c4e6', 33, 5, 1, 1, 3.00, 6.89, true, 1, 'REJEITADA');
INSERT INTO public.bi_fato_logistica VALUES (59, '32006a8e-e169-4c36-80e9-b0a1f5a8a9e7', 38, 2, 1, 1, 4.99, 9.05, true, 1, 'REJEITADA');
INSERT INTO public.bi_fato_logistica VALUES (60, '54f7cd32-8f55-46d0-ba43-edc5e5ecb068', 38, 2, 1, 1, 4.99, 7.11, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (61, '973f16b9-407f-4540-9256-2f4a5f742e2a', 33, 5, 1, 1, 3.00, 12.42, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (62, 'b8881b92-f774-4437-aeee-c228180176e0', 33, 5, 1, 1, 3.00, 8.59, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (63, '2391a637-9f7f-471c-9555-552b8acdb534', 45, 2, 1, 1, 3.66, 7.89, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (64, '214c3ae5-403e-4fa8-8eb8-24978c285b1e', 42, 2, 1, 1, 1.52, 9.51, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (65, '2eb55343-7fd8-40d8-b3d9-7c18f0986515', 42, 2, 1, 1, 1.52, 11.10, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (66, '8f6d7a98-2707-44ac-b59e-acbc39606687', 42, 2, 1, 1, 1.52, 4.93, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (67, 'b40c48cd-1593-4d98-ab0c-1890c39909e2', 42, 2, 1, 1, 1.52, 14.93, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (68, 'bed84d70-1427-4992-8dae-5ad57f8d32ff', 42, 2, 1, 1, 1.52, 5.87, true, 1, 'REJEITADA');
INSERT INTO public.bi_fato_logistica VALUES (69, 'a8286528-d132-4269-9eff-229700b62c19', 45, 2, 1, 1, 3.66, 15.80, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (70, '603ca4c0-1eca-4154-b019-71ff0eebf467', 46, 5, 1, 1, 3.99, 10.89, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (71, '0ce882f1-378b-4cc4-8091-73a864404265', 34, 4, 1, 1, 4.21, 8.29, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (72, '8d0e3a0a-5bf7-425c-9f28-252b568db407', 34, 4, 1, 1, 4.21, 7.61, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (73, '0d03e46e-c635-48eb-8862-28b8c458749d', 39, 3, 1, 1, 2.01, 4.86, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (74, '24c4783f-87f3-43f7-bee5-4c2d8873cade', 39, 3, 1, 1, 2.01, 14.91, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (75, '8402aaf3-6fc4-4446-973e-77ad6c35c150', 39, 3, 1, 1, 2.01, 7.16, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (76, 'cb33db6f-bcfa-4ade-8b91-38229d38ff4d', 39, 3, 1, 1, 2.01, 12.24, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (77, '16142f66-3318-49b6-b9c7-cda24237abc9', 46, 2, 1, 1, 4.93, 9.67, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (78, '8572e7aa-7054-4c3f-80cd-2fa2be429729', 46, 2, 1, 1, 4.93, 6.43, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (79, '87ecb7d2-c37c-4c9b-990b-b57142fc729c', 46, 2, 1, 1, 4.93, 15.18, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (80, '4dc810ce-c942-41fb-b560-dec221c7aad8', 44, 5, 1, 1, 2.58, 15.42, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (81, '763f9e5a-7cb3-4515-92e6-13527b363004', 44, 5, 1, 1, 2.58, 17.54, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (82, 'cc159022-fa94-4411-aecf-ade99f153483', 44, 5, 1, 1, 2.58, 13.68, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (83, 'd868164f-43af-4e34-95ef-08e94a2f8988', 44, 5, 1, 1, 2.58, 7.30, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (84, '162baddc-671f-405b-a310-db7516ef84e4', 50, 5, 1, 1, 2.54, 7.11, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (85, '5d675d7f-937f-4de3-9f06-115aeb18afb9', 46, 3, 1, 1, 1.59, 7.47, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (86, '77ae21d9-f827-41ff-8ffa-b6a943fb33d1', 46, 3, 1, 1, 1.59, 5.22, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (87, 'bb3deffa-5afb-4d66-aa58-6c61f5bf74b5', 46, 3, 1, 1, 1.59, 11.49, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (88, 'd5231d7c-8da6-4a67-b6ad-e9c0f4fa8a14', 46, 3, 1, 1, 1.59, 15.95, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (89, 'a638972d-81d2-4f5d-82e9-859428950a59', 60, 4, 1, 1, 2.58, 4.42, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (90, 'c050f5ed-a732-4390-a555-c94aa12c8c37', 60, 4, 1, 1, 2.58, 4.60, true, 1, 'REJEITADA');
INSERT INTO public.bi_fato_logistica VALUES (91, '186c1a75-4f3e-43bd-bd70-86f8e7d13cf5', 55, 5, 1, 1, 1.60, 7.18, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (92, 'acc1c538-792b-4826-8afe-9b3c067c089a', 55, 5, 1, 1, 1.60, 3.46, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (93, '0841a58f-39bf-4cdc-b7f6-13214dff4fcb', 48, 4, 1, 1, 2.63, 8.13, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (94, '32d3e326-1567-4a18-a9d7-49ffdd952396', 48, 4, 1, 1, 2.63, 3.97, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (95, 'dd5cdaa1-de57-405d-b570-1a18f5f48bbd', 48, 4, 1, 1, 2.63, 8.75, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (96, 'e973e038-fb18-45e9-a155-98baa5fd562a', 48, 4, 1, 1, 2.63, 6.00, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (97, 'e9ec5605-3a4d-4249-9b79-f7f1017e4dd3', 48, 4, 1, 1, 2.63, 3.84, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (98, 'e98ac1b9-c74e-421e-921e-b60fe19fceae', 55, 5, 1, 1, 1.60, 4.66, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (99, 'e73f61f0-b75b-4c61-90fe-1bb796675399', 46, 5, 1, 1, 3.99, 5.60, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (100, 'fdd9c311-c326-44c6-b450-6437a920ecf0', 56, 5, 1, 1, 1.56, 3.74, true, 1, 'REJEITADA');
INSERT INTO public.bi_fato_logistica VALUES (101, '2450094c-5716-4259-9142-f05bf9eb8796', 50, 5, 1, 1, 3.96, 7.58, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (102, '375afbb5-78ae-4427-8955-9361217d8191', 50, 5, 1, 1, 3.96, 19.00, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (103, '48148bce-0b48-4f35-9f5f-dc9570b2e5ea', 50, 5, 1, 1, 3.96, 14.77, true, 1, 'REJEITADA');
INSERT INTO public.bi_fato_logistica VALUES (104, '4bcb329f-95dd-440b-ad2b-b644a51140ba', 50, 5, 1, 1, 3.96, 15.34, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (105, 'ee8052e5-0c75-494d-a043-ed7a401afd80', 50, 5, 1, 1, 3.96, 7.98, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (106, '04095fef-f046-492d-860d-1e315b41e8ae', 53, 3, 1, 1, 3.67, 9.89, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (107, 'a9eda96f-0b85-4d91-8db0-df33f5f840c3', 53, 3, 1, 1, 3.67, 8.35, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (108, '81bd9b95-a385-41ca-b955-9888a4a0812f', 59, 2, 1, 1, 4.40, 9.71, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (109, '0ce6ed3d-8334-44ff-942b-7f58469f589b', 57, 3, 1, 1, 2.71, 5.94, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (110, '5ae96030-b270-4f91-abc5-d8a095e25108', 57, 3, 1, 1, 2.71, 7.12, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (111, '4959adf2-0f0c-4160-aff0-e7ea20f9498d', 55, 3, 1, 1, 3.75, 4.77, true, 1, 'REJEITADA');
INSERT INTO public.bi_fato_logistica VALUES (112, '72542455-2462-4806-b318-c95e787e3ee9', 55, 3, 1, 1, 3.75, 14.72, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (113, 'bc495411-2672-47fd-ba8c-7e725690ac72', 55, 3, 1, 1, 3.75, 9.52, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (114, 'c53ba90a-9d3f-45cd-ade8-4ca32dd82d20', 55, 3, 1, 1, 3.75, 10.80, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (115, 'd21abde0-6ab3-49c6-b489-4750d1bc1c87', 55, 3, 1, 1, 3.75, 4.76, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (116, 'c2c95dee-3fbe-46de-897b-6419cce57211', 59, 3, 1, 1, 3.93, 6.02, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (117, 'b21d8458-7959-4bca-b830-b238f4d48168', 46, 2, 1, 1, 4.93, 11.77, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (118, 'da01c9fd-e384-4c40-ab42-dfb2bb6b6b29', 46, 2, 1, 1, 4.93, 11.69, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (119, 'd311fb0d-0fd6-4d30-9c69-253ff14bb7fa', 59, 3, 1, 1, 3.93, 9.87, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (120, '580ca99c-c6c6-4a32-b1c4-d9d1b65c17ac', 58, 3, 1, 1, 3.33, 8.53, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (121, 'ae091e75-f3e3-4b3c-b8b1-2bdcffffaea9', 58, 3, 1, 1, 3.33, 5.32, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (122, '7bb3d25d-bf9c-4408-9323-f7bf7feab862', 50, 4, 1, 1, 3.06, 4.32, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (123, '1f75617d-18ec-4139-9aa2-8498070e804b', 65, 5, 1, 1, 4.95, 6.76, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (124, '5a7e5a69-c4bd-40e0-950f-d2b020d7114d', 60, 4, 1, 1, 2.58, 6.95, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (125, '960ea98b-092d-4967-952d-f9b7205c2afa', 60, 4, 1, 1, 2.58, 7.11, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (126, '40f40d99-85df-4665-a005-ff96b495640e', 65, 5, 1, 1, 4.95, 8.02, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (127, '5e6ad944-b4b1-49b2-adc4-b6eb27f84282', 65, 5, 1, 1, 4.95, 17.82, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (128, '163f6e00-5ce7-4377-819b-3ec0764d0fe7', 62, 3, 1, 1, 1.58, 10.69, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (129, '126ec509-bdf6-47a2-a2fb-bf23d3cf2c58', 57, 5, 1, 1, 4.34, 9.81, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (130, '2fd44474-2b88-4558-8b55-96756b626211', 57, 5, 1, 1, 4.34, 9.05, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (131, 'c49deeb5-141a-4c2d-bb0e-ee4ec03834e0', 57, 5, 1, 1, 4.34, 11.10, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (132, '1e6202df-481d-43c3-8284-94f59fd08216', 59, 2, 1, 1, 4.40, 9.53, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (133, '5cbb4638-e730-4d42-b895-07ff7c143fee', 59, 2, 1, 1, 4.40, 21.63, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (134, '337a5646-a9aa-48fc-b6c1-9527db58e38f', 62, 3, 1, 1, 1.58, 4.53, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (135, '58dc0350-740d-47de-b91a-7f9d81af9551', 62, 3, 1, 1, 1.58, 8.63, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (136, 'e684cde2-54e4-40b7-a87b-cc8a5b456866', 60, 4, 1, 1, 4.38, 6.63, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (137, '307a9152-4296-48c8-ac6f-e2641a925560', 69, 5, 1, 1, 2.52, 12.88, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (138, '34da1fd1-608c-4a12-8d1f-3d3633a2593c', 69, 5, 1, 1, 2.52, 14.69, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (139, '34ec50f7-2e8e-4ccb-8fd3-db0a4bf4030a', 69, 5, 1, 1, 2.52, 13.87, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (140, '4ed012f2-3302-4da6-95a1-536d7eea618b', 69, 5, 1, 1, 2.52, 6.07, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (141, 'a9af3a44-ec91-4c5a-a674-b28273c47092', 69, 5, 1, 1, 2.52, 10.16, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (142, 'b3b20e96-c676-4785-bab4-8c8cf6f4ddea', 69, 5, 1, 1, 2.52, 8.12, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (143, 'def542f6-3997-4c52-bbcb-39708ba1f4e9', 69, 5, 1, 1, 2.52, 11.79, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (144, '1c5cfd54-c672-457a-b1a5-e83f9c87f4ce', 69, 3, 1, 1, 2.56, 10.92, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (145, 'dc47f7db-dcea-4a67-a304-3c558f9be4ee', 69, 3, 1, 1, 2.56, 11.50, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (146, 'fa5c04b3-9f02-42cc-a127-604429c8a0b9', 69, 3, 1, 1, 2.56, 6.90, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (147, '5ae89103-6a82-4ce6-93e6-cb32ae61910b', 71, 4, 1, 1, 2.18, 9.17, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (148, '6580f65c-e5ea-4565-8387-7950b651055a', 71, 3, 1, 1, 4.41, 11.86, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (149, '8f13f4cc-16c9-4271-a862-f01289378fca', 70, 4, 1, 1, 3.95, 12.36, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (150, '952b3c13-877f-4246-8d9d-f9f4c111f321', 70, 4, 1, 1, 3.95, 12.82, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (151, '9560b599-59aa-4af4-92f7-f1814d51e056', 70, 4, 1, 1, 3.95, 7.85, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (152, '3811e6c9-2aff-4351-a2a0-f1e7fa3fd478', 69, 5, 1, 1, 2.75, 8.64, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (153, '4d7c6867-f91e-4887-b332-83fbd7627f78', 69, 5, 1, 1, 2.75, 13.79, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (154, 'ea25c5ab-08ed-4cd4-a67b-e412faf902dd', 69, 5, 1, 1, 2.75, 11.20, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (155, '65ee9560-cfeb-47f5-bb97-228a5ec15d44', 71, 3, 1, 1, 4.41, 6.10, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (156, '1d79f4d9-67d8-4295-8c1d-ff15e4aa1f31', 66, 2, 1, 1, 2.04, 6.51, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (157, '3c67040b-587b-4cc2-afd1-e22c1b485b78', 66, 2, 1, 1, 2.04, 15.47, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (158, '46e309dc-f807-46bd-a74a-0b2ce9797872', 66, 2, 1, 1, 2.04, 4.15, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (159, '96e52203-a199-4423-a2a5-e31f398e8b5c', 66, 2, 1, 1, 2.04, 10.21, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (160, 'e8c03a43-9b02-4cf4-9d2e-12873fed96b4', 70, 4, 1, 1, 3.95, 9.03, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (161, 'f585d905-ee81-4766-8d0c-325f5fbbe7a8', 70, 4, 1, 1, 3.95, 11.58, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (162, '11804405-51c2-4164-9052-ca5379508c17', 71, 5, 1, 1, 3.37, 8.76, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (163, '5e688794-d239-496a-8d79-2efc674671db', 71, 5, 1, 1, 3.37, 15.51, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (164, 'c3fb1dae-7725-4d9d-b763-00e700066b98', 71, 5, 1, 1, 3.37, 10.80, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (165, 'f2adb0f0-c1cc-4812-bf00-9d5194f13642', 71, 5, 1, 1, 3.37, 15.79, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (166, '037e5240-8571-4ccd-91ad-2e9d27af0a97', 86, 2, 1, 1, 4.70, 20.20, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (167, '1b0b4675-3e47-4910-bb8f-9d7f5a802895', 86, 2, 1, 1, 4.70, 18.53, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (168, '970fed4d-75c2-4ba3-9834-77519d9a63da', 72, 2, 1, 1, 4.60, 10.25, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (169, '9a6560e9-46b6-41ac-a76b-18e042fff6e1', 72, 2, 1, 1, 4.60, 7.66, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (170, 'cafbfa88-e063-4ce6-835e-10e0a5339e1a', 75, 3, 1, 1, 1.29, 6.63, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (171, 'd04116f2-76af-429d-b456-e9c796113af9', 75, 3, 1, 1, 1.29, 13.50, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (172, 'db40f5f1-3683-4a53-a79f-189e463c1dca', 75, 3, 1, 1, 1.29, 17.50, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (173, 'ebfc8b73-4463-4574-866a-c09a796b8601', 75, 3, 1, 1, 1.29, 15.62, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (174, '2e2b03d5-3458-4b71-96b0-a441bab73ada', 86, 2, 1, 1, 4.70, 9.98, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (175, '79f058e1-d362-46f6-b0ab-8bd02715a630', 86, 2, 1, 1, 4.70, 14.99, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (176, '11cba21e-f96b-4599-8b12-cb51074512cb', 77, 3, 1, 1, 1.69, 10.36, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (177, '3d68aa08-1b0d-4e8a-92d3-8c1ccc91e941', 77, 3, 1, 1, 1.69, 12.29, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (178, '917197f5-41ed-4c31-8263-7d9f4665ef29', 77, 3, 1, 1, 1.69, 5.75, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (179, 'e4e5ad4d-b481-45ec-9234-2b88d140af60', 77, 3, 1, 1, 1.69, 5.73, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (180, 'f1cf81a5-fa8c-4f22-b3a3-0b4174ab34e6', 77, 3, 1, 1, 1.69, 8.98, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (181, '902be314-ead9-4f2d-83a7-a3faf129d1f6', 86, 2, 1, 1, 4.70, 18.90, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (182, '84c54a58-9bfa-42d1-a4ec-0364d3471f2f', 84, 2, 1, 1, 3.28, 15.32, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (183, 'b6393a26-ec1c-4546-bd56-b6c8f0a98b1a', 84, 2, 1, 1, 3.28, 8.38, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (184, 'c747e811-9c32-41db-bbf6-34d04dc4bf0d', 84, 2, 1, 1, 3.28, 11.89, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (185, '253aa284-8705-45ff-9a06-ba6bb1114ee9', 78, 3, 1, 1, 2.62, 11.23, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (186, '3898ab52-7655-4295-9682-b68f5e1792dc', 78, 3, 1, 1, 2.62, 9.30, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (187, '9d8d5b1d-4d8e-4a79-84a3-76c545661539', 78, 3, 1, 1, 2.62, 6.12, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (188, 'a292d0b4-fd54-4250-878c-5161f5b898fb', 78, 3, 1, 1, 2.62, 4.63, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (189, 'f2a1888c-5a9e-4195-8e55-aa5310cd7e3b', 78, 3, 1, 1, 2.62, 3.72, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (190, 'cb6b9847-b9e9-4100-8c73-0555dffcf7be', 84, 2, 1, 1, 3.28, 11.90, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (191, '041fece6-6cc3-4d7d-b5e9-370da51aa26b', 82, 3, 1, 1, 3.09, 7.69, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (192, '232c5920-32a1-4f91-8e93-f5435141086f', 71, 4, 1, 1, 2.18, 6.10, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (193, '62c7450b-cd79-41ba-a5ae-ab47d4da79a9', 71, 4, 1, 1, 2.18, 3.24, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (194, 'a143060b-563a-4706-bfbb-48e249dfe777', 71, 4, 1, 1, 2.18, 5.03, true, 1, 'REJEITADA');
INSERT INTO public.bi_fato_logistica VALUES (195, 'cf1e53db-e69f-4fb3-9a4e-34aa9603e4c3', 71, 4, 1, 1, 2.18, 8.42, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (196, 'f325aa0d-44e6-435e-8c2f-e8ecb3df30be', 71, 4, 1, 1, 2.18, 3.26, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (197, '0f46d81f-2156-48d9-8999-4c3582252694', 82, 3, 1, 1, 3.09, 6.93, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (198, '4f31f15f-6e2c-49c6-a9bc-a519d68077e8', 87, 4, 1, 1, 3.34, 10.03, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (199, '0ea8cccd-8a42-494a-8c17-9e430dce0f8a', 71, 5, 1, 1, 1.80, 5.74, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (200, '12181e10-1713-41d1-938d-7b563fd87c26', 82, 4, 1, 1, 3.60, 8.87, true, 1, 'REJEITADA');
INSERT INTO public.bi_fato_logistica VALUES (201, '3353553a-93d3-4675-a2bb-b14d4c337a5e', 85, 3, 1, 1, 4.44, 7.56, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (202, '5d74b470-13fb-41da-882f-0e0ff655b6fe', 85, 3, 1, 1, 4.44, 5.74, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (203, 'a81e5b22-6407-46b0-8139-82e5d2b89912', 85, 3, 1, 1, 4.44, 9.91, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (204, 'f1745f1e-f893-44be-8cba-14170416dc9f', 85, 3, 1, 1, 4.44, 7.61, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (205, '7c54f3f0-2202-4231-b384-60016699a3b5', 92, 2, NULL, 1, NULL, NULL, false, 0, 'COLETADA');
INSERT INTO public.bi_fato_logistica VALUES (206, 'be755288-32ca-4318-af1c-6f13e121dd6a', 82, 4, 1, 1, 3.60, 5.50, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (207, 'c8649a49-165d-4d91-9739-47a99e1982f0', 82, 4, 1, 1, 3.60, 7.39, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (208, '70376337-cbca-4718-a7a4-ed5f0930831b', 87, 4, 1, 1, 3.34, 4.78, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (209, '1709270c-cfc4-44fa-8234-30ab64ee1ff7', 85, 3, 1, 1, 3.08, 6.67, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (210, 'f5388486-edcc-4a31-b118-1523618170f6', 85, 3, 1, 1, 3.08, 4.45, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (211, 'f783a2fb-0b09-4ae5-87b3-ae4da86fa145', 87, 4, 1, 1, 3.34, 9.67, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (212, 'cb060ddd-f3c6-4bda-b5f5-f29dfed2ff50', 93, 4, NULL, 1, NULL, NULL, false, 0, 'COLETADA');
INSERT INTO public.bi_fato_logistica VALUES (213, '738348fd-868e-4d76-bd20-4091581d3519', 87, 2, 1, 1, 3.31, 15.53, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (214, '934c0bdf-fa31-4650-9128-71fc2d28d4f8', 87, 2, 1, 1, 3.31, 6.19, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (215, 'a86a78ba-671e-4e4a-a49c-5c7e5612c84d', 87, 2, 1, 1, 3.31, 17.56, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (216, '5c0c3d8d-f963-4013-b0e3-910ba57af77c', 92, 2, 1, 1, NULL, NULL, false, 0, 'EM_TRANSITO');
INSERT INTO public.bi_fato_logistica VALUES (217, 'ec43e010-0939-4e61-8dfa-9a727a45e8d1', 92, 2, 1, 1, NULL, NULL, false, 0, 'EM_TRANSITO');
INSERT INTO public.bi_fato_logistica VALUES (218, 'c09d1bdf-cf8a-4204-941c-e358c7eeb5d0', 93, 4, NULL, 1, NULL, NULL, false, 0, 'COLETADA');
INSERT INTO public.bi_fato_logistica VALUES (219, 'e1ed001f-ff79-4c18-b696-120ac9c35eab', 93, 4, NULL, 1, NULL, NULL, false, 0, 'COLETADA');
INSERT INTO public.bi_fato_logistica VALUES (220, '09d3255f-92a1-4a4b-87a3-d2937282c551', 94, 5, NULL, 1, NULL, NULL, false, 0, 'COLETADA');
INSERT INTO public.bi_fato_logistica VALUES (221, '206aac9b-d357-4521-a21e-6becf77b825b', 93, 4, 1, 1, 2.49, 9.20, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (222, '65226050-7f95-4c82-ba85-2940cefbddc6', 93, 4, 1, 1, 2.49, 7.65, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (223, '7a375c89-2860-4361-a315-f1bac90b1e12', 93, 4, 1, 1, 2.49, 7.99, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (224, 'c5d5dc99-a98e-4d42-9c50-53f735221ce5', 93, 4, 1, 1, 2.49, 6.59, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (225, '97a0ab25-5128-4ab0-beb7-1d09ea3a2d7c', 89, 5, 1, 1, 3.15, 8.05, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (226, 'a4e22cd9-738e-409c-84bf-2d0b095260a9', 89, 5, 1, 1, 3.15, 9.23, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (227, 'cf12bbf2-88fd-47b7-a62e-28293efab620', 89, 5, 1, 1, 3.15, 14.48, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (228, 'de2202b8-b4ad-4a4f-9e98-31cb140744a4', 89, 5, 1, 1, 3.15, 12.10, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (229, '02a79a7c-88f4-4bed-a644-94ecc0295734', 94, 5, NULL, 1, NULL, NULL, false, 0, 'COLETADA');
INSERT INTO public.bi_fato_logistica VALUES (230, 'f2dc705c-3c38-4c94-bf31-db8e447c29b3', 93, 2, 1, 1, NULL, NULL, false, 0, 'EM_TRANSITO');
INSERT INTO public.bi_fato_logistica VALUES (231, '9dd7b23b-8451-47e1-95f3-d4d0114d5d24', 94, 3, 1, 1, 3.89, 7.68, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (232, 'c98f813c-dbe4-45d5-a320-63ccf6839109', 92, 2, 1, 1, 1.50, 3.62, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (233, '409ddae1-4d97-43bb-acdf-52a289ecea1b', 89, 3, 1, 1, 1.49, 12.85, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (234, '72f6250a-5b34-4f5c-bda7-bfca1017e828', 89, 3, 1, 1, 1.49, 13.27, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (235, '75aa1f8d-d405-483f-b7d0-5559c5980aaa', 89, 3, 1, 1, 1.49, 16.85, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (236, '6752a2aa-bb15-4ff8-a4fa-784fba462ff0', 94, 5, 1, 1, NULL, NULL, false, 0, 'EM_TRANSITO');
INSERT INTO public.bi_fato_logistica VALUES (237, '50bb7584-216c-4861-b53f-5c9e1ed7cb40', 93, 4, 1, 1, 2.94, 5.16, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (238, '1010b091-c7be-4bb8-a4a6-271a30bc6b3f', 94, 5, 1, 1, 1.42, 6.05, true, 1, 'REJEITADA');
INSERT INTO public.bi_fato_logistica VALUES (239, '7864fb13-16a4-47eb-8a76-cbe71753351c', 94, 5, 1, 1, 1.42, 3.61, true, 1, 'REJEITADA');
INSERT INTO public.bi_fato_logistica VALUES (240, 'fa149fab-1060-4855-ab09-4a9034645aca', 94, 5, 1, 1, NULL, NULL, false, 0, 'EM_TRANSITO');
INSERT INTO public.bi_fato_logistica VALUES (241, 'a4adb43e-a97e-4ddd-81f2-392168195b9b', 89, 3, 1, 1, 1.49, 4.64, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (242, '41d156da-9dce-4755-af7b-7c62c16a6684', 94, 3, 1, 1, 3.89, 8.60, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (243, 'f9f03e3d-b3cf-4d09-8275-d7883ce4e2fa', 94, 3, 1, 1, NULL, NULL, false, 0, 'EM_TRANSITO');
INSERT INTO public.bi_fato_logistica VALUES (244, 'd7b41fbf-ab6c-4989-abc0-ce9c27784b1b', 95, 3, NULL, 1, NULL, NULL, false, 0, 'COLETADA');
INSERT INTO public.bi_fato_logistica VALUES (245, 'bb505572-771b-4623-b186-1028fbba0d1d', 96, 2, NULL, 1, NULL, NULL, false, 0, 'COLETADA');
INSERT INTO public.bi_fato_logistica VALUES (246, 'c1c4af4b-03b9-4620-9ca2-c55f92748a7c', 95, 3, 1, 1, NULL, NULL, false, 0, 'EM_TRANSITO');
INSERT INTO public.bi_fato_logistica VALUES (247, 'd4123247-4c59-4af5-aaae-767972d70494', 95, 3, 1, 1, NULL, NULL, false, 0, 'EM_TRANSITO');
INSERT INTO public.bi_fato_logistica VALUES (248, '434713fc-2f28-4d2d-83f9-c80fd511b614', 95, 3, 1, 1, 1.38, 8.32, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (249, '464f8700-648c-4841-996c-8595ee8ae1d9', 95, 3, 1, 1, 1.38, 5.86, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (250, 'd07a2795-b98d-4cb4-a3f4-4a4afab34beb', 97, 5, NULL, 1, NULL, NULL, false, 0, 'COLETADA');
INSERT INTO public.bi_fato_logistica VALUES (251, '51c5d9d3-0cce-44c1-9ae7-658be28eee2c', 96, 2, 1, 1, NULL, NULL, false, 0, 'EM_TRANSITO');
INSERT INTO public.bi_fato_logistica VALUES (252, '283ad797-5a61-4ebb-852b-225c14094b9d', 97, 2, 1, 1, NULL, NULL, false, 0, 'EM_TRANSITO');
INSERT INTO public.bi_fato_logistica VALUES (253, '6777b646-e07f-48d9-8e7d-38f642808fe7', 96, 2, 1, 1, 1.09, 6.97, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (254, 'e718396b-3edf-491b-b904-8a45b663fde1', 96, 2, 1, 1, 1.09, 11.52, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (255, 'ed644326-9ba1-4213-a383-b3871d51853c', 96, 2, 1, 1, 1.09, 7.90, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (256, '8d5d5cc0-36e4-4540-ac87-866957f06e81', 97, 2, NULL, 1, NULL, NULL, false, 0, 'COLETADA');
INSERT INTO public.bi_fato_logistica VALUES (257, 'fa95c2bc-4843-41ad-9e75-19f4fc517ca1', 96, 3, 1, 1, 1.14, 6.22, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (258, '08f2e5a4-d9c4-495c-98b6-72030419ea87', 96, 3, 1, 1, NULL, NULL, false, 0, 'EM_TRANSITO');
INSERT INTO public.bi_fato_logistica VALUES (259, '12234b05-5e8e-4540-b061-2617ceaa20b3', 101, 5, 1, 1, 3.46, 11.01, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (260, '0806b05c-5991-4195-b071-f556c0e84017', 97, 2, 1, 1, 3.38, 7.15, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (261, 'd0f2710e-fdcf-47db-860a-fe0acced3d4e', 97, 2, 1, 1, 3.38, 11.99, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (262, '02d6f767-2ed0-49b7-af36-7ae533640048', 97, 5, 1, 1, 2.95, 14.13, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (263, '7db78855-287f-44ff-9625-76b5ba73fba6', 97, 5, 1, 1, 2.95, 5.83, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (264, '8d965f9b-941d-4bfb-9747-7fc48466d1e2', 97, 5, 1, 1, 2.95, 15.12, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (265, '1ca8a35e-0ef5-4c23-b420-7f149477938f', 98, 5, NULL, 1, NULL, NULL, false, 0, 'COLETADA');
INSERT INTO public.bi_fato_logistica VALUES (266, 'df290837-fa82-403d-bb4e-e13d6aee94d2', 101, 2, NULL, 1, NULL, NULL, false, 0, 'COLETADA');
INSERT INTO public.bi_fato_logistica VALUES (267, 'a4f27c7c-8e35-45a8-aec5-06690c9afb97', 97, 4, 1, 1, 2.20, 5.90, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (268, 'a4d22f95-cd5d-4bec-b264-a9a28798da31', 99, 4, NULL, 1, NULL, NULL, false, 0, 'COLETADA');
INSERT INTO public.bi_fato_logistica VALUES (269, '28824c5b-ac0f-44e3-8fa9-0667f02145d4', 97, 4, 1, 1, NULL, NULL, false, 0, 'EM_TRANSITO');
INSERT INTO public.bi_fato_logistica VALUES (270, '74710de1-6726-466d-bba9-e481427e7703', 99, 4, NULL, 1, NULL, NULL, false, 0, 'COLETADA');
INSERT INTO public.bi_fato_logistica VALUES (271, '90e10bc6-9451-4ad7-b2d3-db6bd7648132', 99, 4, 1, 1, NULL, NULL, false, 0, 'EM_TRANSITO');
INSERT INTO public.bi_fato_logistica VALUES (272, '19d68c8a-f6e0-4bc1-9b53-1c92704589ad', 101, 5, 1, 1, 3.46, 8.53, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (273, '2c11a60e-d911-48dc-8509-16af9df6a32c', 98, 5, 1, 1, 4.44, 6.94, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (274, '4ebeaa7a-da73-4903-aa5e-76a82edb3313', 99, 4, 1, 1, 1.09, 5.05, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (275, 'a16fd8df-7876-403e-abdd-79cbb5363565', 99, 4, 1, 1, 1.09, 2.92, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (276, 'dd37f237-f71c-491b-a80d-8959c321e8a4', 99, 4, 1, 1, 1.09, 6.04, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (277, '61b3be09-35f7-4b43-98ec-0ab4179aefd0', 98, 5, 1, 1, NULL, NULL, false, 0, 'EM_TRANSITO');
INSERT INTO public.bi_fato_logistica VALUES (278, '41bded05-3529-470c-a19a-da57db685424', 101, 5, NULL, 1, NULL, NULL, false, 0, 'COLETADA');
INSERT INTO public.bi_fato_logistica VALUES (279, '993da3f3-3366-4819-a022-26cd76e614ed', 101, 3, NULL, 1, NULL, NULL, false, 0, 'COLETADA');
INSERT INTO public.bi_fato_logistica VALUES (280, '3e3c4581-a2d5-44a5-8dc7-692aa1793e37', 101, 5, 1, 1, 3.46, 12.21, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (281, 'bd5173dc-de2a-4e4c-b0e7-ec88dd6bae1b', 101, 2, 1, 1, 1.20, 7.11, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (282, '0cde602a-d50d-421d-b6f8-f15646428d79', 98, 3, 1, 1, 1.16, 7.37, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (283, '4abb11b5-cbbe-4eea-956d-0f173fa3ee95', 98, 3, 1, 1, 1.16, 3.59, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (284, '390046c3-2740-4542-b8b8-8426d69a5298', 101, 5, NULL, 1, NULL, NULL, false, 0, 'COLETADA');
INSERT INTO public.bi_fato_logistica VALUES (285, 'd07c8729-f2ec-476a-af22-0cced31729cd', 101, 5, NULL, 1, NULL, NULL, false, 0, 'COLETADA');
INSERT INTO public.bi_fato_logistica VALUES (286, 'be7da1e7-5b85-4d1f-9387-ba9a9a3a4140', 100, 4, 1, 1, NULL, NULL, false, 0, 'EM_TRANSITO');
INSERT INTO public.bi_fato_logistica VALUES (287, 'd497a3b6-e084-406a-a8ad-0017d592be63', 100, 4, 1, 1, NULL, NULL, false, 0, 'EM_TRANSITO');
INSERT INTO public.bi_fato_logistica VALUES (288, '2183581e-16c4-42f4-95cd-97b0f2926baf', 102, 4, NULL, 1, NULL, NULL, false, 0, 'COLETADA');
INSERT INTO public.bi_fato_logistica VALUES (289, '03943cb6-69fe-4f55-9e75-d69c2e3216d6', 100, 4, 1, 1, 4.65, 9.52, true, 1, 'REJEITADA');
INSERT INTO public.bi_fato_logistica VALUES (290, '071ff881-c7ab-4e9c-9a81-8401b3c6dfa0', 100, 4, 1, 1, 4.65, 10.43, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (291, '5bdd118b-787c-461d-ac9a-29a87493800e', 100, 4, 1, 1, 4.65, 10.61, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (292, '9c258aa3-6e39-4f40-b951-5c99b1c9b37c', 100, 4, 1, 1, 4.65, 11.34, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (293, '05b121f0-ea11-4130-8507-524003f7ff7f', 101, 3, 1, 1, 2.23, 12.27, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (294, '2634e67d-9552-4dec-b307-fffb841a1c86', 101, 3, 1, 1, 2.23, 11.72, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (295, '2c39b6e7-2d68-4e4c-8f92-f84ff9c14fc5', 101, 3, 1, 1, 2.23, 9.07, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (296, 'b30faa90-e1e1-4cca-b7d6-ba175eecc046', 101, 2, 1, 1, NULL, NULL, false, 0, 'EM_TRANSITO');
INSERT INTO public.bi_fato_logistica VALUES (297, 'be9a4614-d09f-463f-aedd-9dca3ae8ed69', 101, 2, 1, 1, NULL, NULL, false, 0, 'EM_TRANSITO');
INSERT INTO public.bi_fato_logistica VALUES (298, '3e3b59eb-8d88-4d3c-b920-e2f0ec0905a4', 102, 4, 1, 1, NULL, NULL, false, 0, 'EM_TRANSITO');
INSERT INTO public.bi_fato_logistica VALUES (299, 'b848bb60-99e1-462a-8fec-fe5bf23b2a83', 102, 4, 1, 1, NULL, NULL, false, 0, 'EM_TRANSITO');
INSERT INTO public.bi_fato_logistica VALUES (300, '3bc279d0-ccb0-422c-840c-ee4284e97d91', 101, 3, 1, 1, 2.23, 8.77, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (301, '8514816a-91b2-4b74-9578-95ec1075766d', 101, 3, 1, 1, 2.23, 7.82, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (302, '2b0e0440-f5c2-465a-b55f-ae59c5bc42a5', 102, 4, 1, 1, 2.56, 7.48, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (303, '89da8b27-8442-4362-b3bf-0747515437d2', 102, 4, 1, 1, 2.56, 7.99, false, 0, 'RECEBIDA');
INSERT INTO public.bi_fato_logistica VALUES (304, 'e536c6e6-5e35-4800-bb19-e10d0f90a51d', 101, 5, 1, 1, NULL, NULL, false, 0, 'EM_TRANSITO');
INSERT INTO public.bi_fato_logistica VALUES (305, '266e36d6-c0cb-4738-b831-b9fc45355b77', 98, 3, 1, 1, NULL, NULL, false, 0, 'EM_TRANSITO');
INSERT INTO public.bi_fato_logistica VALUES (306, 'a4f1e30e-dcf2-43f6-bd2b-f4ed97143285', 98, 3, 1, 1, NULL, NULL, false, 0, 'EM_TRANSITO');


--
-- Data for Name: bi_fato_ordem_servico; Type: TABLE DATA; Schema: public; Owner: labvida
--

INSERT INTO public.bi_fato_ordem_servico VALUES (1, '7c9b672f-0269-46b6-b601-8356c6ab7913', 21, 5, 5, 159, 1, 6, 0, 134.88, 23.82, 11.38, 12.44, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (2, '9266e280-b45c-4afc-9d40-20f5fe101d93', 21, 5, 1, 96, 5, 2, 0, 46.98, NULL, 10.29, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (3, 'd66ce4cb-471e-4575-8ed0-1d5e5201e1ad', 16, 5, 3, 31, 6, 3, 0, 62.06, 22.90, 5.57, 17.33, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (4, '8e7f34ce-8c75-4433-92f5-eebc7d5c8730', 20, 5, 6, 170, 2, 6, 0, 108.08, 26.23, 12.57, 13.65, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (5, '3b1d2eca-12e7-4555-91e9-7bc72eec5497', 27, 4, 2, 199, 5, 3, 0, 41.71, 21.60, 5.65, 15.95, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (6, '3014807c-9e54-4e8b-aaa9-606b2e4ad357', 20, 5, 4, 177, 6, 6, 0, 127.41, NULL, 13.98, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (7, '74b30c99-d3cb-45e6-acc4-8d856a88746b', 27, 5, 5, 173, 6, 5, 0, 94.56, 19.03, 8.90, 10.14, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (8, 'b494ad87-4461-4119-973f-17285e4c7fdd', 20, 4, 1, 70, 1, 4, 0, 98.28, 26.47, 7.88, 18.59, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (9, '6392755f-178c-4a21-89f3-1450a2b8f5eb', 17, 4, 5, 14, 6, 5, 0, 101.28, 32.32, 18.68, 13.64, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (10, '649b2df8-6cda-41a9-a99d-ce18f7bebdfa', 20, 5, 4, 152, 6, 4, 0, 83.42, 21.11, 8.26, 12.85, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (11, 'ea29a8cc-ce20-40bf-98f7-15ec2bbe60cb', 20, 5, 2, 202, 4, 5, 0, 178.49, 23.07, 14.56, 8.51, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (12, '08884ee8-f9ef-42ad-ae88-de6d94fefd04', 20, 5, 7, 120, 2, 2, 0, 42.08, 16.29, 9.14, 7.15, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (13, 'b9380a57-458a-4cef-bccc-830f9a024f0f', 15, 3, 6, 29, 6, 2, 0, 43.68, 17.74, 7.92, 9.82, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (14, '6b1a1a1f-84ff-4e28-852f-9b616fe0c5cf', 17, 4, 2, 88, 6, 6, 0, 119.80, 20.62, 11.70, 8.92, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (15, '6c57f789-ff86-4fbd-b717-4f2fb9afd980', 17, 4, 7, 206, 6, 6, 0, 138.60, 25.94, 11.38, 14.56, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (16, '03bf6955-a5df-4b47-9454-659a48e697c4', 17, 4, 2, 127, 4, 4, 0, 103.30, 23.43, 8.60, 14.83, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (17, 'd9342065-c40e-4978-a377-cb8fac880b4f', 17, 4, 6, 186, 6, 4, 0, 120.96, 27.00, 17.56, 9.44, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (18, '185b5c7e-18d5-4d8d-805e-d7695828026b', 15, 3, 3, 106, 1, 2, 0, 39.05, NULL, 7.73, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (19, 'ec274603-300c-4737-af17-4ee43edad9cb', 15, 3, 8, 16, 4, 2, 0, 45.63, 23.65, 7.15, 16.50, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (20, 'aa12eed1-7a5c-4216-9776-59e132ebb509', 26, 5, 3, 88, 6, 4, 0, 139.64, 21.47, 9.82, 11.65, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (21, 'fdf58429-433f-47eb-8fae-02ad4ba51be7', 20, 4, 2, 29, 6, 6, 0, 131.93, NULL, 10.05, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (22, '6e07f5a4-5c65-4cf6-a51b-a019e55f79d9', 31, 2, 6, 71, 3, 4, 0, 64.40, 24.93, 7.25, 17.68, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (23, '9e9a644c-bc18-4450-ba26-af833adba78f', 31, 2, 6, 24, 4, 2, 0, 48.16, 22.00, 8.32, 13.68, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (24, 'ed75d2ac-1f75-479c-af9d-59375e475ee8', 27, 4, 2, 164, 6, 3, 0, 88.76, 27.04, 12.55, 14.49, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (25, '69d68b91-a79e-40bb-85a1-a98c294a50ad', 20, 4, 5, 45, 6, 2, 0, 44.64, NULL, NULL, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (26, '0e70c7a5-8847-44a8-9fbb-ddaa3949ebe5', 21, 5, 4, 109, 6, 4, 0, 66.40, 16.51, 7.73, 8.78, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (27, '755d751f-e740-47d8-8580-87edc48b252c', 32, 4, 8, 107, 4, 4, 0, 126.95, 20.25, 6.16, 14.10, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (28, '8de76c9f-51dc-4eb3-941c-9c73568fdef6', 16, 5, 5, 191, 5, 6, 0, 118.56, 30.39, 12.74, 17.66, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (29, 'ba0b83ec-6dbd-4181-bb94-7dbe940dde97', 26, 5, 1, 200, 6, 4, 0, 76.68, 30.49, 12.73, 17.75, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (30, '5525f778-bb2a-4dc7-9e30-1623c22b134e', 25, 5, 7, 103, 4, 3, 0, 91.08, 20.00, 7.58, 12.42, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (31, 'b5b6ba3d-41f9-4eae-8aec-8b477b9f4f2d', 21, 5, 1, 209, 3, 2, 0, 55.62, 27.48, 7.75, 19.73, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (32, '7def0840-27af-41e8-b3bf-bbf1da9e9660', 25, 5, 4, 58, 6, 2, 0, 22.40, 31.54, 11.11, 20.43, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (33, '6981f31f-3483-41f3-9cb4-723b1bc23bb1', 28, 2, 2, 16, 4, 5, 0, 155.69, 20.20, 4.10, 16.10, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (34, '84655b22-edd9-420f-a7a5-5483e6769fb6', 25, 5, 8, 128, 4, 5, 0, 102.37, NULL, 15.02, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (35, '3f18a504-49dd-451d-986d-b73a18b481d9', 27, 5, 7, 165, 6, 5, 0, 83.15, 18.84, 11.10, 7.74, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (36, 'a84b8c31-72a9-488f-ae8a-99369898de22', 20, 4, 5, 218, 6, 5, 0, 153.60, 18.36, 4.40, 13.96, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (37, '6190ed66-bc2e-463c-b673-e5e84b7a70e1', 32, 4, 5, 141, 3, 3, 0, 71.52, NULL, 7.12, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (38, '75c7b279-52f7-431f-b4d6-675469374ad4', 32, 4, 2, 186, 6, 4, 0, 63.54, 24.31, 12.81, 11.50, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (39, '4bad2d4e-4036-46cc-9f97-386c35d54183', 30, 2, 4, 16, 4, 4, 0, 80.92, NULL, NULL, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (40, '0d06e8f6-3bf9-4151-80f1-ae637e821fb5', 20, 3, 3, 41, 6, 6, 0, 201.70, 19.02, 7.22, 11.80, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (41, '98a7424d-ea9b-46cc-8b90-ee4a8ce7e4ac', 30, 2, 4, 102, 3, 6, 0, 137.78, 18.51, 7.22, 11.30, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (42, 'ed02214c-0717-44f7-ab89-6d67ce51b433', 28, 2, 3, 110, 6, 2, 0, 29.42, 21.38, 8.36, 13.03, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (43, 'fee8a6c8-4b7b-4a63-abb8-6d752f44ad91', 30, 2, 8, 216, 3, 3, 0, 163.80, NULL, 6.29, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (44, '89e58c90-b205-48f8-babb-8ff9445fdae3', 28, 2, 4, 164, 6, 5, 0, 136.94, 30.99, 12.51, 18.48, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (45, 'e7d88245-924b-474f-8f73-05ab70aea4c5', 28, 2, 6, 213, 5, 5, 0, 134.96, 23.17, 3.49, 19.68, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (46, 'af71292d-9e7f-47f4-b552-db5f63bdd30e', 28, 2, 3, 156, 5, 4, 0, 98.44, 22.07, 8.45, 13.62, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (47, '5347d15e-19f4-4d65-be75-0046eb5d4c49', 27, 5, 5, 60, 6, 2, 0, 59.04, 25.69, 6.18, 19.50, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (48, '01e1fcbd-b4b8-45c0-afd8-f5b2f5191da8', 27, 5, 7, 2, 4, 6, 0, 152.46, 33.75, 12.09, 21.66, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (49, 'a9934fa6-1e72-4a01-8994-df37773fe98c', 33, 5, 1, 218, 6, 3, 0, 49.68, NULL, 12.42, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (50, '4af033ce-4d71-4652-9166-a9852073a0fa', 27, 4, 2, 176, 4, 4, 4, 122.22, NULL, NULL, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (51, '00fedbb1-8d85-4911-8be0-6012a47a4ba8', 30, 5, 7, 113, 6, 3, 0, 48.01, 19.58, 8.92, 10.66, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (52, '535ac89a-8afe-4b86-9735-6a132a1df1e3', 25, 5, 2, 17, 6, 3, 0, 50.44, 39.20, 20.24, 18.96, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (53, 'dd7ab9b9-492e-48fc-9cbb-d1c4c3a26935', 50, 4, 2, 49, 2, 2, 2, 84.39, NULL, NULL, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (54, '3fa8f0fc-3ae1-46a6-aa8b-eb5b929b7c7e', 33, 5, 4, 54, 3, 5, 0, 90.05, NULL, 6.89, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (55, '4f216ee9-df8b-44ec-bfd3-5da383ba0309', 39, 3, 8, 12, 5, 6, 0, 130.46, 22.96, 4.86, 18.10, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (56, '81b6b4af-694a-4833-8ac2-e02d013ba231', 50, 5, 5, 77, 6, 3, 0, 99.84, 20.61, 15.34, 5.27, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (57, 'b0fc3740-e641-49e6-ad7d-1858db0dc579', 44, 5, 6, 75, 4, 6, 0, 147.84, 22.15, 7.30, 14.85, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (58, 'fcc5aedb-b77e-42fd-9343-ee47f7bec7e9', 30, 5, 5, 10, 5, 5, 0, 126.72, 27.75, 14.51, 13.24, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (59, '98a38ac8-e430-496f-b3dc-cc1b4233a1e0', 33, 5, 7, 143, 6, 3, 0, 66.33, 18.98, 8.59, 10.39, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (60, '3c1ecb60-c24d-4697-bcc6-33ef496e136d', 37, 3, 8, 212, 4, 4, 0, 83.66, 16.61, 6.63, 9.98, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (61, 'bf5927f7-3640-4886-aaf6-66ce6a26bdba', 37, 3, 3, 76, 2, 5, 0, 171.20, 25.31, 11.50, 13.80, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (62, '2c5ca3af-dc30-4cf8-b0a0-adcadcb8048d', 37, 3, 7, 108, 6, 6, 0, 131.66, 26.46, 6.52, 19.95, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (63, '93da9b05-d6aa-4717-9bdb-b9afee59befa', 37, 3, 5, 18, 5, 4, 0, 105.60, 19.14, 5.27, 13.87, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (64, 'c6dd3be5-f862-486f-b4e9-457ff94dc799', 37, 3, 4, 54, 3, 4, 0, 49.38, 21.23, 11.09, 10.14, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (65, '3fb70fc6-5ca1-4dbf-b73d-f20e30faaec4', 38, 2, 1, 185, 1, 5, 0, 103.68, 11.05, 7.11, 3.94, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (66, '68f8b20d-c13b-451b-84cb-588c10e8ea17', 37, 3, 3, 13, 1, 2, 0, 36.92, NULL, 8.73, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (67, '40fb243d-73c3-4c84-b7ce-2823a25b54ea', 37, 3, 8, 214, 2, 5, 0, 150.92, NULL, NULL, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (68, '0072ecd4-9644-4d3f-b4b8-3d481e5dcffb', 33, 5, 8, 210, 6, 5, 5, 131.63, NULL, NULL, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (69, 'dab0e2be-7823-4101-a736-59c26b2dd20e', 38, 2, 7, 141, 3, 2, 0, 37.62, NULL, 9.05, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (70, '45084c4b-21d5-467d-9b70-354db561eb59', 42, 2, 7, 118, 4, 6, 0, 123.26, 20.16, 4.93, 15.23, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (71, '3735d2f3-01d8-49ab-92ca-9a2e81879c72', 42, 2, 3, 123, 4, 5, 0, 112.88, NULL, 9.51, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (72, 'a0c847ec-0110-4de8-80cc-43dbaff877c2', 48, 4, 7, 165, 6, 6, 0, 136.62, 14.18, 8.13, 6.05, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (73, '5857e701-b372-4b87-b310-a38f0a1fd0a9', 46, 5, 5, 194, 1, 5, 0, 115.20, 17.89, 10.89, 7.00, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (74, '5a5abfa7-b13a-4ddb-a756-6aefe5442b6d', 42, 2, 5, 29, 6, 2, 0, 65.28, NULL, 5.87, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (75, '80d59f25-8ad3-41ad-952f-8940ad94eb04', 42, 2, 4, 53, 4, 5, 0, 114.13, 26.11, 14.93, 11.18, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (76, '2ac631ef-51a5-4ee3-9e42-a9f4d4ba6047', 34, 4, 8, 145, 3, 6, 0, 156.78, 25.82, 7.61, 18.20, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (77, '628ddaf7-ee0a-4919-9d0d-f0f92c00ba22', 39, 3, 6, 203, 4, 5, 0, 193.20, 28.48, 12.24, 16.24, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (78, '5f84efa2-180f-49e9-8016-2ffc44fbc9c0', 45, 2, 4, 81, 5, 6, 0, 108.73, 19.74, 7.89, 11.84, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (79, '06a3baca-0218-45a6-bce5-630a447027b3', 30, 5, 4, 100, 4, 2, 0, 48.97, 22.50, 12.84, 9.65, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (80, 'bb1abea4-f5aa-4fe3-a0ab-e252181cbe61', 39, 3, 4, 177, 6, 2, 0, 24.07, 27.15, 14.91, 12.24, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (81, '0c440028-f9ef-420e-ab19-03c16dc050ef', 46, 2, 2, 145, 3, 4, 0, 84.88, 23.97, 9.67, 14.30, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (82, '095321ae-0462-489f-ad8c-7c15a50f31bb', 50, 4, 1, 204, 5, 2, 0, 31.86, 11.40, 4.32, 7.07, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (83, '7128ff53-84ad-4257-b5b1-53531acdaed3', 37, 3, 6, 63, 4, 5, 0, 178.64, 19.29, 4.56, 14.74, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (84, '247864d7-e3ff-4e3e-98f0-cdaef62673b6', 45, 2, 6, 180, 1, 6, 0, 189.84, NULL, 15.80, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (85, '32a7fe50-6136-4d90-9c55-9bb69bb0fdd2', 42, 2, 7, 95, 6, 4, 0, 91.08, 21.02, 11.10, 9.92, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (86, '708bbe85-d8c5-48bc-9bf9-a5f95dadd8a3', 44, 5, 2, 113, 6, 4, 0, 157.14, NULL, 15.42, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (87, '258c65f0-07d6-4a58-8acd-94de62170d5d', 39, 3, 2, 197, 6, 2, 0, 51.90, 15.12, 7.16, 7.96, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (88, '71990e06-b42e-4a2d-a357-36d398caa975', 44, 5, 1, 184, 1, 2, 0, 40.50, NULL, 17.54, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (89, '5b807a53-701b-4b1d-9023-0e7a35a02d2c', 46, 3, 7, 73, 6, 5, 0, 107.42, 20.59, 5.22, 15.37, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (90, 'cf66998c-b849-4d82-9eb1-e2155f07220c', 44, 5, 5, 83, 6, 3, 0, 117.12, NULL, 13.68, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (91, '3a62bb1a-8184-458b-b55d-e670dab7ff29', 46, 3, 6, 77, 6, 3, 0, 57.12, 32.51, 15.95, 16.56, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (92, '682b8aad-36a8-434b-9ebb-909558542bc1', 48, 4, 8, 114, 1, 4, 0, 75.47, 29.97, 8.75, 21.23, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (93, '657c35db-9c8d-41d4-962b-2e04aa156175', 46, 3, 7, 121, 4, 5, 0, 150.97, NULL, 7.47, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (94, 'c5571f72-93a4-4585-a11a-d0c085d2399f', 46, 3, 5, 191, 5, 6, 0, 149.28, NULL, 11.49, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (95, '243b10fd-c2fd-4d87-b529-03bbf76e25c7', 34, 4, 6, 147, 6, 3, 0, 82.88, NULL, 8.29, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (96, 'c4568575-ad8b-450e-8c2a-fdcfb0b01041', 48, 4, 1, 99, 3, 3, 0, 71.82, NULL, NULL, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (97, '9b44569c-ec96-443d-9a52-c2c20c88c8a7', 48, 4, 2, 73, 6, 3, 0, 86.82, 12.94, 3.84, 9.10, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (98, '084b0038-81e5-40ca-873d-946c505dfaa3', 48, 4, 5, 25, 1, 2, 0, 62.88, NULL, 3.97, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (99, '60e524b9-a255-4c30-ac09-ba448a17a34e', 48, 4, 5, 25, 1, 3, 0, 64.32, 23.46, 6.00, 17.47, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (100, '494d13b8-a74b-4afe-9adb-08caaaf8a79c', 46, 5, 1, 205, 4, 6, 0, 130.14, 19.66, 5.60, 14.06, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (101, '9fe1a124-210d-4c91-88a1-4a180dd65399', 46, 2, 5, 54, 3, 6, 0, 175.20, 26.19, 11.77, 14.42, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (102, '3a1888c7-0bc9-4147-a62d-2aab360846a5', 50, 5, 5, 135, 6, 4, 0, 110.40, NULL, 14.77, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (103, '46783f5c-03f2-40eb-855d-0a7bc7a18d8f', 55, 5, 1, 73, 6, 4, 0, 68.04, 23.38, 3.46, 19.92, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (104, 'b071e1a1-1f22-4335-8fe5-0493a9ae8219', 55, 5, 7, 57, 3, 4, 0, 91.57, 22.04, 4.66, 17.38, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (105, 'fc8c414e-5a30-44a9-8c22-16ad1b189665', 50, 5, 3, 130, 6, 5, 0, 193.13, 17.36, 7.58, 9.78, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (106, 'a6e8116a-5f36-4ee6-85cf-9e9990ae4942', 53, 3, 6, 131, 6, 3, 0, 70.00, 12.92, 9.89, 3.04, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (107, 'ffe191c7-d751-4dd2-bfdf-d4e007a09be4', 50, 5, 4, 61, 1, 2, 0, 33.20, 30.78, 19.00, 11.79, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (108, '2ce86a0f-92c2-4e8e-b0d3-a4911b122584', 59, 2, 6, 81, 5, 3, 3, 54.88, NULL, NULL, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (109, '3e4d30b3-42bd-4bee-8b97-05fa6e172529', 53, 3, 3, 187, 5, 4, 0, 69.01, NULL, NULL, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (110, '9ccb8ad5-804b-4656-bd8a-aa737622807e', 62, 3, 7, 162, 4, 6, 0, 115.83, NULL, NULL, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (111, '37e7522a-9a07-4591-9a9d-4ce5e518ffe6', 69, 3, 4, 9, 5, 5, 0, 121.18, 14.94, 10.92, 4.02, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (112, 'c8d090f3-e29d-43e2-a3fd-689f6eb12204', 59, 2, 1, 182, 4, 4, 0, 103.68, 23.74, 9.71, 14.03, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (113, 'e6276fca-b688-466b-a930-83213da5e710', 53, 3, 8, 58, 6, 2, 0, 38.03, 16.83, 8.35, 8.48, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (114, '6b4060cf-a915-45ad-ab5a-c5e4006d80d4', 55, 3, 2, 95, 6, 6, 0, 119.32, NULL, 4.77, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (115, 'd24a053b-7702-4603-bada-92c80b633ab4', 57, 3, 6, 73, 6, 5, 0, 120.40, 17.58, 5.94, 11.64, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (116, '3de6bb8f-0504-4912-9a1c-c31c99219233', 55, 3, 2, 139, 5, 4, 0, 84.38, 13.72, 4.76, 8.97, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (117, 'b01f0161-707d-45a3-8393-e5093e960e04', 59, 3, 6, 86, 4, 3, 0, 127.12, 17.76, 6.02, 11.74, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (118, '6e4d5fa9-320c-43bb-a166-f7a88f85dfe5', 55, 3, 5, 68, 4, 5, 0, 166.08, NULL, 14.72, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (119, '3db97adf-4a28-4634-a636-4a6938f38fff', 55, 3, 3, 156, 5, 2, 0, 26.74, 21.65, 10.80, 10.85, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (120, '6388635a-5e99-430c-8400-30aa3de58f9b', 57, 5, 7, 51, 5, 4, 0, 72.76, 20.20, 11.10, 9.09, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (121, '255f787a-57be-4e3a-bc45-f8a09647e967', 65, 5, 5, 29, 6, 2, 0, 52.80, 25.23, 6.76, 18.47, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (122, '5e613cca-e530-4e70-9dce-91fd60655666', 50, 5, 5, 22, 6, 6, 0, 129.60, NULL, 7.11, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (123, '46c2bb66-cbc2-4619-bc36-ce6b02577c5f', 60, 4, 8, 154, 4, 4, 0, 113.49, 17.69, 7.11, 10.57, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (124, '2fd03de5-a899-47b0-95d5-2dbf81307f1f', 58, 3, 7, 180, 1, 3, 0, 40.10, 19.66, 5.32, 14.35, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (125, 'b199d208-5ae8-437d-babc-370f4ba8efbc', 55, 3, 8, 194, 1, 5, 0, 176.66, 17.20, 9.52, 7.67, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (126, '17e275ba-fdf8-45b9-aae7-0b2424bdc6e4', 65, 5, 2, 181, 4, 5, 0, 77.11, 18.68, 8.02, 10.65, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (127, '3c531a4e-4efe-4c6c-bf38-ccd54f3fb5a5', 56, 5, 6, 147, 6, 3, 0, 107.52, NULL, 3.74, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (128, 'b825017e-69b7-426d-bf7b-62728dd63a1c', 57, 3, 1, 150, 4, 4, 0, 72.36, 21.90, 7.12, 14.78, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (129, '25cb8349-1004-4314-89f1-a255383b604c', 57, 5, 3, 151, 6, 4, 0, 92.56, 28.32, 9.81, 18.51, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (130, '48501cd6-6e5f-41b6-ad0e-a81a304b6822', 60, 4, 1, 3, 6, 6, 0, 135.00, NULL, 4.42, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (131, '21b9087c-2d1a-4eed-a7cc-201581e0ce36', 62, 3, 4, 76, 2, 6, 0, 142.76, 22.80, 8.63, 14.18, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (132, 'a490a208-060b-48ea-8b2a-e84e1c5aa10b', 46, 2, 7, 109, 6, 5, 0, 91.57, NULL, 15.18, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (133, 'ba6b5f1c-2b40-409b-bae1-e43803e472b3', 66, 2, 6, 188, 5, 3, 3, 87.92, NULL, NULL, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (134, 'e4596106-eee4-45c3-87f6-31b24e068117', 60, 4, 6, 83, 6, 5, 0, 173.60, NULL, NULL, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (135, '0d0c7f3d-d53b-4309-aefb-eeb0bfdef846', 60, 4, 3, 117, 4, 4, 0, 151.40, NULL, 4.60, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (136, '6b71701e-21e1-452c-8732-cfafca31f6e1', 66, 2, 6, 28, 2, 4, 0, 123.20, 10.46, 4.15, 6.31, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (137, 'd719773e-d21f-43a9-85fb-8a3c821c67a8', 46, 2, 3, 151, 6, 6, 0, 169.05, 14.27, 6.43, 7.83, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (138, '6051090d-0f7f-46b2-b6c6-81759b4f5407', 58, 3, 6, 80, 4, 2, 0, 47.04, 19.05, 8.53, 10.52, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (139, 'c67ca19e-600a-4205-94b8-95d8fabbc1a9', 46, 2, 5, 124, 6, 5, 0, 120.00, 24.45, 11.69, 12.77, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (140, 'a95bc090-dec9-4e91-95f7-132283d9f25c', 60, 4, 4, 53, 4, 5, 0, 97.10, NULL, 6.63, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (141, 'fbe23eaa-0699-4371-a0fa-5fd170f8d4a1', 57, 5, 4, 118, 4, 5, 0, 123.67, 25.75, 9.05, 16.70, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (142, 'b2f21e79-62f3-457f-8456-e5f3faeee80e', 59, 2, 8, 171, 1, 2, 0, 88.92, 21.73, 9.53, 12.20, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (143, '014bf8d9-5ce1-4e9c-abb5-7f759b8db3c4', 69, 3, 2, 183, 1, 3, 0, 89.73, 19.08, 11.50, 7.58, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (144, '31985737-9851-4a78-957c-0d4d75e0bea2', 59, 2, 3, 24, 4, 4, 0, 93.09, 34.57, 21.63, 12.94, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (145, '1e58a6c9-2ea0-465c-860c-ac161c114502', 62, 3, 5, 157, 6, 4, 0, 119.52, 19.44, 4.53, 14.91, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (146, 'afed971e-0c84-4ba1-a5e7-6bfa96e90961', 55, 5, 1, 73, 6, 5, 0, 154.44, 21.80, 7.18, 14.62, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (147, '2ff77a1b-c92c-4363-9a18-56ae5aaf016d', 50, 5, 2, 88, 6, 4, 0, 101.85, 27.41, 7.98, 19.43, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (148, '8084b0f6-bc7d-4a06-a248-4b7115b77c5b', 59, 3, 7, 10, 5, 2, 0, 31.68, 28.03, 9.87, 18.16, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (149, '315f869d-6ef0-4bec-b5a2-62a850021284', 66, 2, 5, 77, 6, 5, 0, 158.40, 16.89, 10.21, 6.68, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (150, '92db1bab-3aed-48fc-a67c-c67357984d98', 69, 5, 6, 60, 6, 4, 0, 179.76, 17.08, 12.88, 4.19, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (151, '7926368c-a016-4c10-b8e8-687a0d8e9637', 62, 3, 3, 127, 4, 6, 0, 217.21, NULL, 10.69, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (152, '74c79ca4-c993-4d60-9e12-522de65d875d', 66, 2, 4, 30, 4, 4, 0, 75.54, 23.18, 6.51, 16.66, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (153, '43d3c6ce-0d63-4b64-a653-0a81679071ac', 60, 4, 6, 179, 4, 2, 0, 71.12, 24.26, 6.95, 17.31, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (154, '8e38e950-a981-4619-a387-2d600b1bedc9', 65, 5, 6, 207, 4, 5, 0, 160.16, 29.46, 17.82, 11.64, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (155, 'c5c91c37-adb3-4a5c-a49d-c51d43ecfa1b', 78, 3, 5, 210, 6, 6, 0, 104.16, 23.82, 11.23, 12.60, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (156, 'bd1de4a9-6806-4daf-8e3f-69446fcdff26', 72, 2, 5, 67, 4, 4, 0, 93.60, NULL, 7.66, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (157, 'fdcaf3fb-a525-40a3-a02a-8fef78874386', 71, 5, 6, 72, 6, 3, 0, 113.12, 29.56, 15.51, 14.05, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (158, 'ebd9589d-0be9-4a0e-aef1-2201ababa495', 70, 4, 7, 138, 4, 5, 0, 111.37, 21.93, 12.82, 9.11, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (159, '016fa673-57f5-4d1e-89fb-38f2c9bdd8f5', 69, 5, 6, 39, 4, 4, 0, 145.04, 29.53, 13.79, 15.74, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (160, '1b828a9d-41a2-4657-96c9-f38acbf2ee6c', 70, 4, 6, 85, 6, 2, 0, 30.24, 24.91, 11.58, 13.33, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (161, 'b57536c1-656b-4226-b49e-3cf7937efa52', 70, 4, 2, 211, 1, 3, 0, 90.69, 23.27, 7.85, 15.42, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (162, '5e7d8ab2-82c2-4a63-985d-0e3a325aa1c8', 69, 5, 7, 131, 6, 6, 0, 178.20, NULL, 10.16, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (163, 'fc035b64-9bbd-4c3b-a704-7b4c5e6f5c95', 69, 3, 8, 80, 4, 5, 0, 157.37, 12.47, 6.90, 5.57, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (164, 'a025305b-33da-4788-9bbe-b5232927a95b', 69, 5, 6, 209, 3, 6, 0, 202.72, NULL, 11.79, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (165, '7394aed7-9d22-4f9f-9bbc-ababa58678bb', 69, 5, 4, 132, 4, 4, 0, 85.08, 21.48, 8.12, 13.36, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (166, 'f491973a-20b3-4cfb-8bdc-2f68f241605e', 69, 5, 4, 59, 4, 4, 0, 61.43, NULL, 14.69, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (167, 'ff98053c-4f4d-410a-b4ff-23a242e11f14', 69, 5, 7, 23, 3, 2, 0, 32.17, 17.26, 6.07, 11.18, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (168, '7fc1b823-2a27-4202-b145-bdeb69e673f9', 71, 3, 6, 89, 4, 3, 0, 104.72, 29.89, 11.86, 18.03, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (169, 'eaad8cfb-492b-4c42-9e1a-69ad1f101eb7', 71, 5, 3, 54, 3, 6, 0, 113.42, NULL, 5.74, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (170, 'cfc59b89-ebee-4283-87c7-a2613ba1134c', 75, 3, 7, 47, 6, 5, 0, 93.06, 20.11, 6.63, 13.47, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (171, '9f96572d-61f9-4086-8580-92fda1ebd4fc', 71, 5, 4, 205, 4, 4, 0, 86.32, 27.48, 15.79, 11.68, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (172, 'd34ce524-7fad-4741-a63d-568e07f9df11', 71, 5, 6, 140, 3, 3, 0, 126.56, 24.05, 8.76, 15.29, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (173, '33990304-0d80-4658-8ef4-101b0adfd2b0', 71, 5, 1, 140, 3, 3, 0, 149.04, 26.69, 10.80, 15.88, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (174, '4692f1af-6308-43b5-897a-184b8bf8f78f', 78, 3, 8, 54, 3, 3, 3, 75.47, NULL, NULL, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (175, '26b1cc39-c994-4486-8cbe-f26ab7a074bf', 71, 4, 7, 123, 4, 5, 0, 103.46, NULL, 5.03, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (176, '8c63fe90-5be5-4465-aaef-b001ffd7e8c2', 82, 4, 6, 133, 4, 2, 0, 65.52, NULL, 8.87, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (177, 'e528c934-58ed-4ee3-a193-0d4532cd6e9e', 69, 5, 6, 168, 1, 6, 0, 185.36, 27.21, 13.87, 13.34, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (178, '13727629-f961-4227-89b9-b3d9bc0a713d', 84, 2, 5, 162, 4, 2, 0, 25.92, NULL, 15.32, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (179, '58b334d8-9d09-4913-a0bb-9bcfb8025c39', 71, 3, 2, 149, 6, 6, 0, 143.56, 28.27, 6.10, 22.16, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (180, '5858f386-ba01-4034-8b47-ec616b48719b', 69, 5, 2, 83, 6, 5, 0, 114.45, 24.62, 8.64, 15.97, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (181, '6560d817-61af-4336-83ca-812fee2733c7', 69, 5, 1, 173, 6, 4, 0, 63.18, 19.34, 11.20, 8.14, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (182, '7b4fe51b-36e8-48b6-9d9c-7da45730136e', 76, 5, 7, 120, 2, 5, 0, 154.44, NULL, NULL, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (183, '9955284d-78a2-45ca-adaa-a09493dd9e7e', 82, 3, 5, 217, 5, 5, 0, 84.48, 21.15, 7.69, 13.46, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (184, 'c97b3ada-3179-4b44-90ce-c980f4f92694', 71, 4, 3, 80, 4, 2, 0, 74.90, 10.96, 3.26, 7.70, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (185, '9e1dead1-860f-4458-b0bf-f6cd357b6db9', 66, 2, 7, 114, 1, 2, 0, 57.92, 21.06, 15.47, 5.59, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (186, '33b1dab4-4d9b-4bec-ba4b-48bdfa71402a', 70, 4, 4, 137, 6, 2, 0, 31.12, 25.92, 12.36, 13.56, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (187, 'c50a931a-4596-4138-85d4-bcfc5ad1759b', 75, 3, 4, 202, 4, 2, 0, 31.54, 25.67, 15.62, 10.05, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (188, '17ca207f-e23c-46bd-bae4-62c87651c70b', 77, 3, 7, 205, 4, 3, 0, 62.86, 20.46, 10.36, 10.10, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (189, '97609c52-cc66-4468-940f-fd79fa6806d4', 75, 3, 3, 40, 6, 6, 0, 152.47, 24.13, 13.50, 10.63, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (190, 'dfe1143b-50a8-4d45-82ff-327ee927dec0', 75, 3, 3, 16, 4, 4, 0, 79.71, NULL, 17.50, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (191, 'baf2b75a-81e1-4422-9901-628027c9977f', 77, 3, 2, 121, 4, 3, 0, 97.00, 17.92, 5.73, 12.20, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (192, 'dd61ce77-139a-4a27-a611-219380e0dce1', 71, 4, 3, 196, 5, 3, 0, 73.83, 8.39, 3.24, 5.15, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (193, '399a218e-1f33-4fd5-ac37-48fd87f51b73', 77, 3, 8, 195, 6, 5, 0, 136.30, NULL, 12.29, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (194, 'fcad89a4-3ea2-4eca-b901-3855ef304273', 82, 3, 6, 90, 2, 5, 0, 133.84, 27.05, 6.93, 20.12, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (195, '3e5763b8-b91c-4eaa-a37d-cf0d655872a6', 77, 3, 6, 209, 3, 3, 0, 87.36, 22.65, 5.75, 16.90, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (196, '7665def4-f0fd-42a4-9b83-a713e569a2f3', 77, 3, 6, 70, 1, 5, 0, 164.08, 22.39, 8.98, 13.41, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (197, '3124e765-efcf-4d57-b3ce-ed7b246bc0e3', 71, 4, 7, 13, 1, 4, 0, 90.09, 22.05, 9.17, 12.88, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (198, '73cae412-84c2-4eff-b4df-93ca91d13320', 78, 3, 8, 134, 5, 4, 0, 174.33, 16.18, 4.63, 11.55, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (199, '22afbd90-74e9-40c0-ab00-9e88e718e25f', 78, 3, 1, 182, 4, 2, 0, 37.80, 27.01, 9.30, 17.71, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (200, '28991448-81ff-46c8-8a23-bf4b5bdb85bd', 78, 3, 7, 195, 6, 6, 0, 210.87, NULL, 3.72, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (201, 'b7fd0c11-9418-4045-a155-2535af01670b', 71, 4, 8, 174, 5, 6, 0, 221.13, 24.47, 6.10, 18.37, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (202, '40768da7-95d7-41a8-aadf-1536c5a31832', 78, 3, 2, 147, 6, 2, 0, 45.59, 17.13, 6.12, 11.01, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (203, '4175fb71-cc17-41c6-a5c2-04c744afcb98', 71, 4, 8, 201, 3, 5, 0, 193.05, 25.56, 8.42, 17.14, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (204, 'bcde04be-37fd-43a2-99c3-0ff01b7be92f', 70, 4, 8, 136, 4, 5, 0, 132.22, 17.21, 9.03, 8.18, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (205, 'ac1440e9-90e8-4964-b01c-cc07693d891b', 82, 4, 1, 143, 6, 6, 0, 173.34, 26.32, 7.39, 18.93, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (206, '705c6e52-1eb9-400b-922a-b2ccc8fefe9a', 86, 2, 5, 25, 1, 2, 0, 27.36, 31.58, 18.53, 13.04, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (207, 'e547e99f-4417-4663-81eb-50873f7ff7ae', 72, 2, 8, 220, 5, 2, 0, 113.49, 17.01, 10.25, 6.76, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (208, 'cbc26d5f-638b-4259-beeb-a1b2ce32d29a', 86, 2, 4, 105, 4, 2, 0, 47.31, NULL, 18.90, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (209, '999d8c22-b378-4ccd-9ad9-74d1425086f1', 84, 2, 3, 32, 3, 4, 0, 135.89, 28.54, 11.90, 16.64, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (210, '31984848-6af5-4b51-a71c-2bbbd4db2d5b', 84, 2, 8, 67, 4, 3, 0, 99.45, 30.32, 11.89, 18.43, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (211, '9eeef1c2-62f4-4465-a5fb-28a11bccc399', 87, 4, 3, 96, 5, 5, 0, 115.56, 22.73, 10.03, 12.70, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (212, 'fd3cb4da-d87e-499e-af66-49aba4a0a31a', 84, 2, 4, 26, 6, 2, 0, 27.39, 22.20, 8.38, 13.82, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (213, '372081e3-ca22-4790-9963-f404e6f3a2c9', 92, 2, 5, 177, 6, 6, 6, 156.96, NULL, NULL, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (214, 'd8380462-02ec-44d8-82f5-9409453c2848', 87, 2, 2, 207, 4, 2, 0, 62.08, 21.13, 6.19, 14.94, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (215, '162ee2d0-b046-4c5e-bf3a-466789c12b66', 87, 4, 2, 45, 6, 2, 0, 57.23, NULL, NULL, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (216, '7c251099-3906-4983-8eb0-eea1695d3e2e', 85, 3, 7, 6, 4, 6, 0, 144.53, NULL, 7.61, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (217, '861f93fa-50ed-4c2b-b780-20351a800fac', 85, 3, 4, 19, 4, 2, 0, 31.96, NULL, 7.56, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (218, '6912be68-d91b-4ff9-a0c5-44b5219388e8', 87, 4, 7, 132, 4, 5, 0, 116.32, 20.62, 4.78, 15.83, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (219, 'fbb3b652-4e7f-4126-ae59-64fe0e119d6e', 85, 3, 5, 19, 4, 3, 0, 93.12, NULL, 5.74, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (220, '697be523-f9e6-4198-84b0-38e03ee0f1a0', 89, 5, 3, 217, 5, 2, 0, 58.85, 20.93, 8.05, 12.88, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (221, 'fcf9c9e2-5cb7-4db2-829b-2c12af1fdf07', 82, 4, 8, 82, 4, 6, 0, 158.54, 24.14, 5.50, 18.64, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (222, '93451fe2-5e0c-4eb8-a59d-7b47bbd9b7dc', 87, 2, 5, 102, 3, 3, 0, 64.32, 35.04, 17.56, 17.48, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (223, 'a737510f-301e-4c11-8670-340b064ca5c9', 93, 4, 7, 95, 6, 3, 0, 49.50, NULL, NULL, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (224, 'c469341b-1f95-4350-98b3-40e4c0b4d597', 94, 5, 8, 29, 6, 3, 0, 73.12, NULL, NULL, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (225, 'de12c570-31fd-4100-b0a8-457c46ab6f0c', 93, 4, 6, 57, 3, 5, 0, 138.88, NULL, NULL, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (226, '2f1deb3f-7425-4408-89b1-d99317160e10', 86, 2, 6, 179, 4, 4, 0, 104.16, NULL, 14.99, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (227, 'b622f336-5db2-4f81-b8a5-9f97aa929c93', 94, 3, 7, 163, 1, 4, 0, 99.00, 13.71, 7.68, 6.03, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (228, '331da878-7743-4434-bf29-e8ce8f07f0e3', 85, 3, 6, 156, 5, 2, 0, 47.60, 21.32, 4.45, 16.87, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (229, '3a857ab3-8182-4029-b1d5-e99a6e7c9741', 87, 4, 1, 177, 6, 3, 0, 49.14, 22.87, 9.67, 13.20, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (230, 'f997d928-b948-4238-9afa-a33918392392', 92, 2, 6, 191, 5, 6, 0, 142.80, NULL, NULL, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (231, '9d5f3b5f-ed6c-420b-bc93-30e0a8dff40c', 89, 3, 8, 187, 5, 5, 0, 150.93, 32.40, 12.85, 19.56, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (232, 'baaeca03-eebe-43ee-b22d-46405fce9c97', 92, 2, 4, 69, 6, 4, 0, 78.02, NULL, NULL, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (233, '2a2c53c2-1330-4d34-98f4-705115e62785', 93, 4, 4, 182, 4, 4, 0, 70.97, NULL, 5.16, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (234, '65fdee0c-3964-43ad-b245-a13dd4f7175d', 86, 2, 3, 136, 4, 4, 0, 103.78, 27.20, 20.20, 7.00, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (235, 'ef9e8d8c-dee0-4da6-8bec-39b5f0fe0115', 92, 2, 5, 35, 1, 4, 0, 72.96, NULL, NULL, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (236, 'd9123641-7040-4112-ada6-34994770cf84', 86, 2, 2, 214, 2, 6, 0, 123.68, 30.47, 9.98, 20.48, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (237, 'ef1a1677-ad93-467d-ac3b-319c23845778', 89, 5, 1, 179, 4, 2, 0, 88.56, 29.61, 12.10, 17.51, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (238, 'ad91abbf-34b0-4aad-968b-a3f8bff13eae', 85, 3, 4, 13, 1, 5, 0, 122.02, 24.18, 9.91, 14.27, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (239, '82477c05-3145-4106-b95a-c85c1b8aa202', 93, 4, 1, 205, 4, 3, 0, 43.74, 31.97, 9.20, 22.78, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (240, '985fee20-66bb-406c-b797-e9bad5fb0843', 87, 2, 7, 18, 5, 6, 0, 148.50, 25.38, 15.53, 9.85, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (241, '12537d6f-842a-46a9-a253-936297cb732b', 85, 3, 6, 74, 5, 5, 0, 140.56, 22.05, 6.67, 15.38, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (242, '899be6f9-85b9-40f0-8aca-8dffd4e748a2', 93, 4, 4, 214, 2, 6, 0, 136.11, 24.52, 7.65, 16.87, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (243, '4492553b-3382-4f7b-b097-adea729746aa', 93, 4, 3, 94, 4, 6, 0, 136.96, NULL, NULL, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (244, '4b8efde4-df2d-42c9-91fd-77685eb379d9', 93, 2, 8, 79, 5, 6, 0, 109.40, NULL, NULL, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (245, '8f7baea5-2f5b-4e55-8f62-03c59c98cc30', 93, 2, 4, 196, 5, 4, 0, 85.90, NULL, NULL, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (246, '7e0e5a3f-7d88-4ed2-808e-eb15e6dce11d', 94, 5, 2, 148, 6, 5, 0, 134.83, NULL, 6.05, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (247, '851123ec-db5a-4e19-acbb-615e25683099', 93, 4, 6, 119, 5, 5, 0, 106.96, 17.05, 7.99, 9.05, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (248, 'f03fcba4-a149-4acb-8a9d-e00436b772d4', 93, 4, 1, 81, 5, 5, 0, 149.58, 22.25, 6.59, 15.66, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (249, '5abe9e09-717c-4500-a761-ce632c02e2d5', 89, 5, 8, 35, 1, 6, 0, 169.65, 17.98, 9.23, 8.74, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (250, '6da74184-676b-41e5-bb7f-bb0ec8c84804', 92, 2, 5, 207, 4, 6, 0, 163.20, 16.57, 3.62, 12.95, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (251, '189cab76-ada7-40a0-a4b5-a36d5279325a', 89, 5, 3, 152, 6, 6, 0, 153.55, 32.37, 14.48, 17.89, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (252, '0ba680f4-0c28-4e61-a9e3-bc2e4d835607', 89, 3, 4, 48, 4, 4, 0, 71.80, 31.26, 13.27, 18.00, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (253, '0bed9435-7c66-4679-8966-a90fa8a58149', 94, 5, 8, 111, 5, 4, 0, 149.18, NULL, NULL, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (254, '333c4df4-5a2f-49f3-9d6e-c7c04c7096d3', 94, 5, 7, 96, 5, 4, 0, 97.02, NULL, 3.61, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (255, '366297ee-d6c1-48a9-9df0-526278b5bd58', 94, 5, 2, 41, 6, 3, 0, 114.46, NULL, NULL, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (256, 'dd4c4bf5-98db-4082-bbc5-5001c23c36b3', 94, 5, 5, 117, 4, 2, 0, 35.52, NULL, NULL, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (257, '729404a9-072b-42e9-939e-5012f663d3a6', 89, 3, 8, 132, 4, 3, 0, 80.73, 22.10, 16.85, 5.26, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (258, 'b2c2f678-850f-4867-9d8b-4e71cd6ddf8a', 98, 5, 3, 22, 6, 3, 0, 62.60, NULL, NULL, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (259, 'ee45cc89-a420-450c-bc40-b9b58836a12c', 89, 3, 6, 95, 6, 5, 0, 157.92, 26.78, 4.64, 22.14, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (260, '4d4d7310-2e1c-4b66-a7f2-f79df1755849', 94, 3, 7, 84, 6, 2, 0, 54.45, NULL, NULL, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (261, '9c0ece82-afcf-4c6a-b3ad-b2bf31d76970', 95, 3, 3, 148, 6, 4, 0, 132.14, 12.20, 8.32, 3.88, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (262, 'f00247f5-5b3b-408d-9dd3-be15be853b6d', 95, 3, 3, 209, 3, 4, 0, 131.61, NULL, NULL, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (263, 'b0747e4a-e361-4a44-b2ae-0836f0b09458', 97, 5, 4, 109, 6, 4, 0, 44.41, NULL, NULL, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (264, '3ae34c71-db62-480d-8259-a4a92fb44f96', 95, 3, 8, 57, 3, 3, 0, 61.43, NULL, NULL, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (265, 'a88eb47a-2d96-434e-a8ba-ddeac068f9e8', 97, 5, 7, 152, 6, 5, 0, 113.36, 32.86, 14.13, 18.73, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (266, 'e3d35d18-ea4b-4bc9-9c7f-7903307d58e3', 95, 3, 5, 24, 4, 2, 0, 48.96, NULL, NULL, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (267, '0cfffc41-099b-4d70-a127-b2d51c647525', 99, 4, 3, 92, 1, 4, 4, 75.97, NULL, NULL, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (268, '3c55dd4d-02cf-458c-aa68-c9c9a8ccf982', 95, 5, 8, 88, 6, 4, 0, 88.34, NULL, NULL, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (269, 'd9d4f4ce-f4a3-49a7-945e-b6589bf08641', 98, 5, 2, 74, 5, 3, 0, 82.45, 17.81, 6.94, 10.87, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (270, '720b0ba3-abd2-42e1-b12d-5d264dce55f2', 100, 4, 7, 3, 6, 2, 0, 59.40, NULL, 11.34, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (271, 'b29e003b-9cab-4b9e-aa88-4717a614acb1', 97, 2, 1, 41, 6, 2, 0, 54.00, NULL, NULL, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (272, 'd1f1a6bb-9a00-4023-83d9-7f75ad3e51f3', 96, 2, 5, 137, 6, 3, 0, 65.28, NULL, NULL, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (273, 'b013b9ae-ffbf-4fe6-9fd4-6d3cadb47a27', 95, 5, 3, 49, 2, 5, 5, 116.09, NULL, NULL, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (274, 'cfdc632b-8b59-4555-bbd3-11d55c97baf5', 96, 2, 4, 88, 6, 6, 0, 73.05, NULL, NULL, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (275, 'f59dd2a7-a131-4025-a6bc-cd7d3ec673a3', 96, 3, 7, 88, 6, 3, 0, 62.37, NULL, NULL, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (276, '685ecf18-73ea-479a-8e3b-9ee6f3aac3f5', 100, 4, 2, 163, 1, 5, 0, 125.12, NULL, NULL, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (277, '0a86f16a-0699-4e86-a843-c7bf764d0c71', 96, 2, 6, 83, 6, 2, 0, 33.60, 23.45, 11.52, 11.93, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (278, '3e605907-e221-4357-9ce6-9005ba2aaa18', 95, 3, 1, 216, 3, 6, 0, 131.76, 15.49, 5.86, 9.63, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (279, 'd3899957-d30f-421c-b9dd-8bd0803e909b', 98, 3, 6, 4, 4, 5, 0, 175.28, NULL, NULL, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (280, '5588392b-ad2f-4aa1-a8a7-9a0017c2054b', 100, 4, 5, 33, 6, 6, 0, 174.24, 32.09, 10.61, 21.48, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (281, '02f5b42b-cd8a-4ac6-b9d4-6d225b392ee5', 96, 2, 1, 205, 4, 3, 0, 55.08, 16.98, 6.97, 10.02, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (282, 'f619dbe9-14aa-42cf-b952-4f5adc4cfbde', 96, 2, 5, 135, 6, 3, 0, 45.12, 21.47, 7.90, 13.56, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (283, '677bf3cb-df75-4910-9cb5-e05c2879d1a1', 96, 3, 1, 4, 4, 3, 0, 73.44, 15.61, 6.22, 9.39, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (284, '899e4917-ac4d-4ff6-87d2-8e8cc8bc832d', 97, 2, 3, 87, 6, 6, 0, 148.74, NULL, NULL, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (285, 'd0011d04-ebd5-4898-8559-37eac18f3416', 99, 4, 5, 1, 3, 6, 0, 170.40, NULL, NULL, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (286, '37800cb9-7959-4e83-a316-f0231c931c8d', 97, 4, 7, 88, 6, 5, 0, 146.52, NULL, NULL, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (287, 'c1a58720-7ef4-4705-895c-612bbcd68381', 98, 3, 8, 169, 6, 3, 0, 83.07, NULL, NULL, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (288, '101a6f10-7977-46f3-a457-06ff5d603ffe', 99, 4, 4, 188, 5, 6, 0, 143.58, NULL, NULL, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (289, '148495e1-bac8-4052-975f-e6e55aa24ee6', 98, 3, 6, 46, 6, 3, 0, 79.52, NULL, 7.37, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (290, '19d64828-f0d9-4521-a563-39dc7bfb7a99', 98, 3, 6, 83, 6, 5, 0, 122.08, NULL, 3.59, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (291, 'd6f0faf1-43e7-4fbb-949b-b42d4fa93980', 97, 5, 3, 97, 6, 3, 0, 87.20, 32.03, 15.12, 16.91, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (292, 'a0dd5e23-0821-495e-8396-e4ce0565865f', 97, 5, 4, 23, 3, 3, 0, 41.50, 25.20, 5.83, 19.37, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (293, 'c9db06b2-3013-422b-81c1-d8551fa17621', 97, 4, 2, 50, 1, 5, 0, 157.62, 15.83, 5.90, 9.94, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (294, '390464b5-a39b-47bf-816b-dc2a6909be6b', 98, 5, 7, 15, 4, 6, 0, 205.43, NULL, NULL, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (295, 'e60fd544-bce6-49fe-a5c8-a354fa06e9a4', 99, 4, 8, 84, 6, 3, 0, 121.68, NULL, NULL, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (296, 'e82f4f6e-fd2e-4a1a-8cce-ee9882dd1d39', 94, 3, 8, 160, 4, 6, 6, 244.53, NULL, NULL, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (297, '0707c6fb-d7eb-4532-b8c2-d4e19b591f7c', 100, 4, 8, 197, 6, 2, 2, 60.84, NULL, NULL, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (298, '8b1abbea-741c-4c0a-a680-1fb35093f8ae', 99, 4, 7, 127, 4, 4, 0, 84.14, NULL, NULL, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (299, '2ef69da8-cb5b-489e-8db4-893ec0b540d9', 100, 4, 6, 59, 4, 6, 0, 179.20, NULL, 9.52, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (300, '56670639-238a-475e-86b3-89364433fa62', 99, 4, 5, 177, 6, 4, 0, 96.48, NULL, 5.05, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (301, '8c0885fa-4ade-445f-a16a-3c4bbfc0e8b5', 99, 4, 6, 97, 6, 5, 0, 131.04, NULL, 6.04, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (302, 'f3e9a86d-d6eb-4232-af73-fa09f54ae7a8', 99, 4, 8, 52, 5, 2, 0, 36.27, 21.82, 2.92, 18.90, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (303, 'efcec1a2-35c8-4a8c-b4b0-590f62a46693', 97, 2, 8, 32, 3, 6, 6, 128.71, NULL, NULL, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (304, '3025a1fa-4fb8-48e0-a302-382394a3f0b5', 100, 4, 8, 140, 3, 3, 0, 94.18, NULL, NULL, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (305, '7669ae05-101e-4a6b-bc36-ce5a398a5299', 94, 3, 6, 211, 1, 4, 0, 84.56, 31.37, 8.60, 22.78, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (306, '379e9d68-1b8b-4300-8f1e-2dd854975f6d', 100, 4, 7, 177, 6, 2, 0, 43.06, NULL, NULL, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (307, 'e54571c7-bb31-425b-8899-d667684a30e9', 100, 4, 7, 49, 2, 2, 0, 30.19, NULL, NULL, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (308, 'beaa2a96-f67a-472c-8a54-94ad26e6274d', 101, 2, 4, 164, 6, 2, 0, 29.05, NULL, NULL, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (309, 'c10f9898-ad9c-4674-b682-fb3a7bcd3723', 101, 2, 3, 32, 3, 6, 0, 188.31, NULL, NULL, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (310, '0bf37cc1-ed64-497a-a3b4-6576f012db92', 97, 2, 5, 105, 4, 5, 0, 87.84, 13.79, 7.15, 6.64, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (311, '2a886526-ed50-4bcb-9ba1-d74b8abfe210', 97, 2, 8, 203, 4, 5, 0, 99.46, 34.47, 11.99, 22.48, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (312, 'b8a569bc-d084-43af-95ab-1f589790c463', 102, 4, 8, 71, 3, 2, 0, 52.65, NULL, NULL, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (313, '0988e034-e6fd-4d6d-ba50-96d42a593d9e', 101, 2, 7, 100, 4, 3, 0, 94.54, NULL, NULL, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (314, '5ea88b98-a197-4dd5-824e-acbe38118f5f', 101, 2, 6, 205, 4, 5, 0, 125.44, NULL, NULL, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (315, '7238e1da-d4b6-4a43-a1b5-ea43fb9bd9ef', 102, 4, 8, 109, 6, 3, 0, 108.81, NULL, NULL, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (316, 'f79bf31a-308b-4e1f-9e14-35e56aaef60c', 101, 5, 4, 135, 6, 6, 0, 130.73, NULL, NULL, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (317, 'dcc56a27-35ee-48ec-b272-c49f7ebcd09f', 101, 5, 6, 1, 3, 5, 0, 97.44, NULL, NULL, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (318, '41e1cf22-231b-4da2-86c6-aeb821192dac', 101, 3, 4, 86, 4, 5, 0, 103.74, NULL, NULL, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (319, '94f77b10-c46f-4ef8-b5ae-27e5a96282f7', 101, 5, 7, 129, 6, 3, 0, 108.90, NULL, NULL, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (320, 'c1453d28-cb5a-48ce-a7ad-569d74927e86', 101, 5, 6, 160, 4, 4, 0, 108.08, NULL, NULL, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (321, 'bf7f0ca3-0137-4cda-8dd8-b7d4e978ce05', 101, 5, 7, 109, 6, 6, 0, 156.42, 29.74, 11.01, 18.73, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (322, '6ae1dc31-8f82-4066-9dc8-d5d358b8514e', 101, 3, 1, 171, 1, 2, 0, 50.22, NULL, 8.77, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (323, 'b63eed82-93f4-4002-9dc9-1e740402fef1', 102, 4, 6, 57, 3, 3, 0, 67.20, NULL, NULL, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (324, 'b0773f34-a453-4fbc-9633-07f3785e7760', 101, 3, 3, 19, 4, 4, 0, 119.31, NULL, 11.72, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (325, 'eb15fe77-e68f-4a01-b095-ed586c0682e2', 101, 5, 1, 102, 3, 4, 4, 96.12, NULL, NULL, NULL, false);
INSERT INTO public.bi_fato_ordem_servico VALUES (326, '893151d8-7f6b-4db4-a97d-73fe3f8a6295', 101, 5, 2, 110, 6, 4, 0, 69.85, 18.71, 8.53, 10.19, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (327, '3f1841f0-33fb-4a35-9608-f3b7bacd5d7c', 101, 5, 1, 123, 4, 4, 0, 132.30, 20.27, 12.21, 8.06, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (328, '3115e2fe-c047-48cf-ad87-d8865c290373', 101, 2, 7, 53, 4, 4, 0, 72.26, 17.14, 7.11, 10.03, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (329, 'ed9b71ac-1a71-4d3e-9a1c-0c990bc89a3d', 100, 4, 4, 56, 4, 3, 0, 41.49, 22.39, 10.43, 11.97, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (330, 'f448d34a-55c8-441d-999d-31dfbfe803ba', 101, 3, 7, 52, 5, 6, 0, 130.69, 26.50, 12.27, 14.23, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (331, '99a17640-54e1-48b9-9c23-360cd477f3c5', 101, 3, 1, 110, 6, 2, 0, 38.88, 24.78, 9.07, 15.71, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (332, 'f8654b7c-e6a6-4c27-a1d1-e18f22ae729d', 101, 3, 1, 115, 6, 5, 0, 131.22, 12.49, 7.82, 4.67, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (333, '422afcf0-f5c8-44a6-a59c-fc6ad3ab792e', 102, 4, 4, 56, 4, 3, 0, 82.17, 25.86, 7.48, 18.39, true);
INSERT INTO public.bi_fato_ordem_servico VALUES (334, '18503eb4-63d9-463a-82de-46119113c739', 102, 4, 5, 114, 1, 2, 0, 83.52, 21.37, 7.99, 13.38, true);


--
-- Data for Name: coletas; Type: TABLE DATA; Schema: public; Owner: labvida
--



--
-- Data for Name: competencias; Type: TABLE DATA; Schema: public; Owner: labvida
--



--
-- Data for Name: lotes_faturamento; Type: TABLE DATA; Schema: public; Owner: labvida
--



--
-- Data for Name: titulos_receber; Type: TABLE DATA; Schema: public; Owner: labvida
--



--
-- Data for Name: conciliacoes_pagamento; Type: TABLE DATA; Schema: public; Owner: labvida
--



--
-- Data for Name: setores; Type: TABLE DATA; Schema: public; Owner: labvida
--



--
-- Data for Name: equipamentos; Type: TABLE DATA; Schema: public; Owner: labvida
--



--
-- Data for Name: insumos_materiais; Type: TABLE DATA; Schema: public; Owner: labvida
--



--
-- Data for Name: estoque_movimentos; Type: TABLE DATA; Schema: public; Owner: labvida
--



--
-- Data for Name: fornecedores; Type: TABLE DATA; Schema: public; Owner: labvida
--



--
-- Data for Name: guias_tiss; Type: TABLE DATA; Schema: public; Owner: labvida
--



--
-- Data for Name: procedimentos; Type: TABLE DATA; Schema: public; Owner: labvida
--



--
-- Data for Name: os_itens; Type: TABLE DATA; Schema: public; Owner: labvida
--



--
-- Data for Name: laudos; Type: TABLE DATA; Schema: public; Owner: labvida
--



--
-- Data for Name: guias_itens; Type: TABLE DATA; Schema: public; Owner: labvida
--



--
-- Data for Name: glosas; Type: TABLE DATA; Schema: public; Owner: labvida
--



--
-- Data for Name: malotes; Type: TABLE DATA; Schema: public; Owner: labvida
--



--
-- Data for Name: malotes_amostras; Type: TABLE DATA; Schema: public; Owner: labvida
--



--
-- Data for Name: solicitacoes_compra; Type: TABLE DATA; Schema: public; Owner: labvida
--



--
-- Data for Name: pedidos_compra; Type: TABLE DATA; Schema: public; Owner: labvida
--



--
-- Data for Name: titulos_pagar; Type: TABLE DATA; Schema: public; Owner: labvida
--



--
-- Data for Name: movimentos_caixa; Type: TABLE DATA; Schema: public; Owner: labvida
--



--
-- Data for Name: os_status_historico; Type: TABLE DATA; Schema: public; Owner: labvida
--



--
-- Data for Name: pedidos_itens; Type: TABLE DATA; Schema: public; Owner: labvida
--



--
-- Data for Name: permissoes; Type: TABLE DATA; Schema: public; Owner: labvida
--



--
-- Data for Name: perfil_permissao; Type: TABLE DATA; Schema: public; Owner: labvida
--



--
-- Data for Name: procedimento_analitos; Type: TABLE DATA; Schema: public; Owner: labvida
--



--
-- Data for Name: procedimento_valores; Type: TABLE DATA; Schema: public; Owner: labvida
--



--
-- Data for Name: procedimentos_insumos; Type: TABLE DATA; Schema: public; Owner: labvida
--



--
-- Data for Name: protocolos_recebimento; Type: TABLE DATA; Schema: public; Owner: labvida
--



--
-- Data for Name: recebimentos_insumo; Type: TABLE DATA; Schema: public; Owner: labvida
--



--
-- Data for Name: resultados; Type: TABLE DATA; Schema: public; Owner: labvida
--



--
-- Data for Name: resultados_auditoria; Type: TABLE DATA; Schema: public; Owner: labvida
--



--
-- Data for Name: valores_referencia; Type: TABLE DATA; Schema: public; Owner: labvida
--



--
-- Name: bi_dim_convenio_sk_convenio_seq; Type: SEQUENCE SET; Schema: public; Owner: labvida
--

SELECT pg_catalog.setval('public.bi_dim_convenio_sk_convenio_seq', 8, true);


--
-- Name: bi_dim_faixa_etaria_sk_faixa_etaria_seq; Type: SEQUENCE SET; Schema: public; Owner: labvida
--

SELECT pg_catalog.setval('public.bi_dim_faixa_etaria_sk_faixa_etaria_seq', 7, true);


--
-- Name: bi_dim_motivo_glosa_sk_motivo_glosa_seq; Type: SEQUENCE SET; Schema: public; Owner: labvida
--

SELECT pg_catalog.setval('public.bi_dim_motivo_glosa_sk_motivo_glosa_seq', 9, true);


--
-- Name: bi_dim_paciente_anon_sk_paciente_seq; Type: SEQUENCE SET; Schema: public; Owner: labvida
--

SELECT pg_catalog.setval('public.bi_dim_paciente_anon_sk_paciente_seq', 220, true);


--
-- Name: bi_dim_procedimento_sk_procedimento_seq; Type: SEQUENCE SET; Schema: public; Owner: labvida
--

SELECT pg_catalog.setval('public.bi_dim_procedimento_sk_procedimento_seq', 30, true);


--
-- Name: bi_dim_setor_sk_setor_seq; Type: SEQUENCE SET; Schema: public; Owner: labvida
--

SELECT pg_catalog.setval('public.bi_dim_setor_sk_setor_seq', 6, true);


--
-- Name: bi_dim_tempo_sk_tempo_seq; Type: SEQUENCE SET; Schema: public; Owner: labvida
--

SELECT pg_catalog.setval('public.bi_dim_tempo_sk_tempo_seq', 124, true);


--
-- Name: bi_dim_unidade_sk_unidade_seq; Type: SEQUENCE SET; Schema: public; Owner: labvida
--

SELECT pg_catalog.setval('public.bi_dim_unidade_sk_unidade_seq', 5, true);


--
-- Name: bi_fato_atendimento_sk_fato_seq; Type: SEQUENCE SET; Schema: public; Owner: labvida
--

SELECT pg_catalog.setval('public.bi_fato_atendimento_sk_fato_seq', 1345, true);


--
-- Name: bi_fato_faturamento_sk_fato_seq; Type: SEQUENCE SET; Schema: public; Owner: labvida
--

SELECT pg_catalog.setval('public.bi_fato_faturamento_sk_fato_seq', 438, true);


--
-- Name: bi_fato_financeiro_sk_fato_seq; Type: SEQUENCE SET; Schema: public; Owner: labvida
--

SELECT pg_catalog.setval('public.bi_fato_financeiro_sk_fato_seq', 87, true);


--
-- Name: bi_fato_glosa_sk_fato_seq; Type: SEQUENCE SET; Schema: public; Owner: labvida
--

SELECT pg_catalog.setval('public.bi_fato_glosa_sk_fato_seq', 55, true);


--
-- Name: bi_fato_logistica_sk_fato_seq; Type: SEQUENCE SET; Schema: public; Owner: labvida
--

SELECT pg_catalog.setval('public.bi_fato_logistica_sk_fato_seq', 306, true);


--
-- Name: bi_fato_ordem_servico_sk_fato_seq; Type: SEQUENCE SET; Schema: public; Owner: labvida
--

SELECT pg_catalog.setval('public.bi_fato_ordem_servico_sk_fato_seq', 334, true);


--
-- PostgreSQL database dump complete
--

\unrestrict r9mpLnDEXRg6lUWW6201AfEJAhf8Q8SXnJVVGUKyey3wFscuIcQQUXiMSu1ixOv

