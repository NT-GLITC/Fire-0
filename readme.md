# 🌲 Fire 0 - Sistema de Monitoramento contra Incêndios

O **Fire 0** é uma plataforma focada na preservação ambiental do **Parque Estadual do Juquery**. Através da análise de indicadores climáticos, o sistema calcula o risco de incêndio e automatiza alertas para a população e autoridades, visando mitigar queimadas na região.

---

## 🛠️ Tecnologias Utilizadas

O projeto foi construído utilizando tecnologias modernas para garantir leveza e eficiência:

* **Linguagem:** Python 3.x
* **Web Framework:** Flask
* **Template Engine:** Jinja2
* **Banco de Dados:** SQLite
* **Comunicação:** Protocolo SMTP (`smtplib`)
* **Frontend:** HTML5, CSS3 (Animações Keyframes) e JavaScript Vanilla



---

## 🚀 Funcionalidades Principais

* **Cálculo FMA (Fórmula de Monte Alegre):** Classifica o risco em 5 níveis (*Nulo, Pequeno, Médio, Alto e Muito Alto*) baseando-se em temperatura e umidade.
* **Pop-ups Dinâmicos:** Exibição centralizada com cores temáticas de acordo com o nível de perigo detectado.
* **Sistema de Newsletter:** Cadastro simples de e-mail para recebimento de alertas.
* **Automação de E-mails:** Envio de e-mails em HTML com tópicos de recomendações automáticas para todos os inscritos.

---

## 📂 Estrutura de Arquivos

```text
├── main.py            # Inicialização do Flask e definição de rotas
├── database.py        # Funções de inserção e consulta ao SQLite
├── comunicacao.py     # Composição e envio de e-mails via SMTP
├── static/            # Arquivos de estilo e imagens
│   └── style.css      # CSS com animações e layout responsivo
├── templates/         # Arquivos HTML (Jinja2)
│   └── index.html     # Página principal da aplicação
└── alertas.db         # Banco de dados gerado automaticamente
```
## 1. Preparar o ambiente
```
python -m venv venv
```
## 2. Ativar o Ambiente Virtual
No Windows:
```
venv\Scripts\activate
```

No Linux/Mac:

```
source venv/bin/activate
```
## 3. Instalar Dependências
```
pip install flask requests
```
## 4. Executar a Aplicação
```
python main.py
```

Acesse o sistema em seu navegador: http://127.0.0.1:5000