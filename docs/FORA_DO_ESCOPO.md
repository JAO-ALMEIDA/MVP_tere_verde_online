# Fora do escopo — Terê Verde Online

Este documento deixa claro o que **não** faz parte do MVP atual.

---

## O que não está incluído

- **Aplicativo nativo** (Android/iOS) ou desktop.  
- **Modo offline/PWA**.  
- **Pagamentos ou reservas online** (vagas são apenas informativas).  
- **Integrações externas** (mapas, clima, redes sociais, APIs).  
- **Hospedagem e deploy automatizado** (CI/CD, Docker).  
- **Backup automático** (recomendado copiar manualmente o arquivo `app.db`).  
- **Upload de imagens ou arquivos**.  
- **Tradução para outros idiomas** (interface apenas em português).  
- **Perfis diferentes de administrador** (há apenas um tipo de usuário).  
- **Recuperação de senha por e-mail**.  
- **Autenticação em dois fatores (2FA)**.  
- **Testes automatizados obrigatórios**.  

---

## Resumo

O **Terê Verde Online** é um MVP web com painel administrativo e banco SQLite local, voltado para divulgar trilhas, eventos e biodiversidade.  
Tudo que não está descrito nas funcionalidades principais — como app nativo, pagamentos ou integrações externas — fica fora do escopo desta versão.
