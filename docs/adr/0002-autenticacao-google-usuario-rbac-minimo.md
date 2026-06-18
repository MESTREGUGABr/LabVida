# Autenticacao com Google para rastreabilidade

Status: accepted

O LabVida mantera o login via Google OAuth (atraves do Auth0) como requisito de autenticacao do projeto para identificar quem executou cada acao do sistema e manter rastreabilidade e auditoria. Na primeira versao, todos os usuarios autenticados terao o mesmo nivel de acesso funcional, sem controle de permissao por perfil; o valor do login e associar cadastro, alteracao e exclusao a uma identidade conhecida.

Consequencias: o projeto atende ao requisito academico de login com Google, preserva rastreabilidade por usuario e evita um sistema de gestao de acessos mais pesado do que o necessario para a demo inicial.
