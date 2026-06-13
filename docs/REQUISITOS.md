
# Requisitos — Terê Verde Online

Este documento lista os requisitos funcionais e não funcionais do MVP (site web em Flask + SQLite).

---

## 1. Requisitos funcionais

### Site público
- Página inicial apresentando o projeto.  
- Listagem de trilhas com nome, dificuldade, descrição e status de visitação.  
- Listagem de eventos com data, horário, vagas e indicador de disponibilidade.  
- Listagem de biodiversidade com nome, tipo e descrição.  
- Quando não houver registros, mostrar mensagem amigável em vez de lista vazia.  

### Autenticação
- Login de administrador em `/admin/login`.  
- Sessão mantida até logout ou expiração.  
- Logout limpa dados da sessão.  
- Rotas protegidas redirecionam para login.  
- Criar administradores via CLI (`flask create-admin`).  

### Painel administrativo
- CRUD completo para trilhas, eventos e biodiversidade.  
- Campos de disponibilidade editáveis.  
- Mensagens de confirmação após ações.  

---

## 2. Requisitos não funcionais

### Desempenho
- Consultas otimizadas ao banco.  
- Cache em memória com invalidação após alterações.  
- SQLite em modo WAL e índices para melhor leitura concorrente.  

### Segurança
- Senhas com hash seguro.  
- Uso de `SECRET_KEY` forte em produção.  
- Cookies de sessão com boas práticas (HTTP-only, SameSite, Secure).  
- Validação de formulários antes de salvar.  

### Usabilidade
- Interface responsiva, pensada para celular.  
- Navegação simples e clara.  
- Mensagens de erro e sucesso em português.  

### Manutenção
- Código organizado em módulos (rotas, modelos, autenticação, banco, etc.).  
- Templates Jinja2 e CSS centralizado.  

### Confiabilidade
- Banco inicializado automaticamente na primeira execução.  
- Sessões de banco fechadas após uso.  
