# Terê Verde Online

Um site simples e leve para divulgar **trilhas ecológicas**, **eventos** e **biodiversidade**, com painel administrativo para que a equipe possa atualizar o conteúdo de forma prática.

---

## Sobre o problema

Comunidades e áreas de conservação muitas vezes precisam reunir em um só espaço informações sobre trilhas, atividades e registros de fauna e flora. Normalmente, isso acaba espalhado em redes sociais ou documentos soltos.  
O **Terê Verde Online** resolve esse desafio com um site responsivo e um painel administrativo integrado, permitindo que visitantes consultem o que está disponível e que gestores mantenham tudo atualizado com segurança básica e banco local (SQLite).

---

## Funcionalidades principais

### Para visitantes
- Página inicial apresentando o projeto.
- Lista de **trilhas** com nome, dificuldade, descrição e status de visitação.
- Lista de **eventos** com data, horário, vagas e indicador de disponibilidade.
- Lista de **biodiversidade** com nome, tipo e descrição.
- Navegação simples e pensada primeiro para celular.

### Para administradores
- Login com usuário e senha.
- Criar, editar e excluir trilhas, eventos e biodiversidade.
- Definir se trilhas e eventos estão disponíveis ou não.
- Painel com listagens e ações rápidas.
- Logout e proteção de rotas internas.

---

## Tecnologias usadas
- **Python 3**  
- **Flask 3.x**  
- **SQLite + SQLAlchemy 2.x**  
- **HTML5 + CSS (mobile-first)**  
- **Jinja2** para templates  
- **Werkzeug** para segurança de senhas  

---

## Como rodar localmente

1. Instale Python 3.10 ou superior.  
2. Crie um ambiente virtual (`python -m venv .venv`).  
3. Ative o ambiente e instale dependências (`pip install -r requirements.txt`).  
4. Configure variáveis de ambiente (`SECRET_KEY`, `PYTHONPATH`).  
5. Rode o servidor com `python src/app.py` e acesse [http://127.0.0.1:5000](http://127.0.0.1:5000).  
6. Crie o primeiro administrador com:  
   ```bash
   flask create-admin usuario senha_segura

## Alternativa rápida no Windows: 
Na raiz do projeto existe o arquivo run.bat, que automatiza os passos básicos

## Equipe

João Vitor de Almeida Oliveira