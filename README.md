# BUILD.PROP - (БУИЛД.ПРОП)

![Status](https://img.shields.io/badge/Status-Em%20Desenvolvimento-green)
![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

> Notas com transliteração visual para cirílico e grego, syntax highlighting e autenticação por login.

---

## Demonstracao

<img width="902" height="813" alt="image" src="https://github.com/user-attachments/assets/b4a43892-23c7-4ded-860c-a27f78f28c47" />

---

## Sobre o Projeto

**BUILD.PROP** opera como uma ferramenta de escrita discreta e segura. Tudo que o usuario digita e exibido na tela transliterado visualmente para cirílico russo e grego, tornando o conteudo ilegivel para qualquer pessoa que olhe para a tela sem conhecer o software.

O software exige autenticacao por login antes de iniciar. Sem a senha correta, a aplicacao nao abre.

---

## Funcionalidades

- Transliteracao em tempo real de texto para cirílico russo e grego
- Regras fonéticas especiais: `S` no inicio de palavra vira `Σ`, `pp` vira `Ψ`, `ii` vira `Й`
- Syntax highlighting com suporte a strings, comentarios, numeros, keywords, delimitadores e conteudo de blocos
- Interface visual inspirada no editor GNU nano, com fundo preto e prompt verde
- Preservacao total do texto original para copia correta via `Ctrl+C`
- Autenticacao por login antes de abrir a aplicacao
- Janela sem barra de console (extensao `.pyw`)

---

## Requisitos

- Python 3.8 ou superior
- Sistema operacional: Windows, Linux ou macOS

### Dependencias

Instale as dependencias com o seguinte comando:

```bash
pip install customtkinter pyperclip
```

---

## Como Executar

### No Windows

Clique duas vezes no arquivo `BUILD_PROP.pyw`.

Como o arquivo usa a extensao `.pyw`, o Python executa sem abrir janela de terminal (console oculto automaticamente).

### Via terminal (qualquer sistema)

```bash
python BUILD_PROP.pyw
```

---

## Autenticacao - Login de Acesso

Ao abrir o software, uma caixa de dialogo solicita o login. Sem a senha correta, o programa e encerrado imediatamente.

### Onde esta definida a senha

A senha de acesso esta definida na **linha 339** do arquivo `BUILD_PROP.pyw`, dentro da funcao `perform_login()`:

```python
# Linha 339
CORRECT_LOGIN = "sanctus@localhost"
```

Para alterar a senha, basta substituir o valor da variavel `CORRECT_LOGIN` pela senha desejada. A comparacao e feita em **letras minusculas**, entao o login digitado nao diferencia maiusculas de minusculas.

**Exemplo de alteracao:**

```python
# Linha 339 - substitua o valor abaixo pela senha que desejar
CORRECT_LOGIN = "sua_senha_aqui"
```

---

## Atalhos de Teclado

| Atalho        | Acao                                               |
|---------------|----------------------------------------------------|
| `Ctrl + C`    | Copia o texto original (nao o cirílico exibido)    |
| `Ctrl + V`    | Cola texto da area de transferencia                |
| `Ctrl + X`    | Recorta o texto selecionado                        |
| `Ctrl + A`    | Seleciona todo o texto                             |
| `Ctrl + Z`    | Desfaz a ultima acao                               |

---

## Estrutura do Codigo

```
BUILD_PROP.pyw
|
|-- Constantes de UI e cores
|-- UI_TRANS_MAP              # Mapa de transliteracao para a interface
|-- NANO_CMD_TRANSLATIONS     # Traducoes dos comandos da barra nano
|
|-- class SecretNotepad       # Classe principal do editor
|   |-- EDITOR_TRANS_MAP      # Mapa de transliteracao do conteudo digitado
|   |-- HIGHLIGHT_COLORS      # Cores do syntax highlighting
|   |-- HIGHLIGHT_PATTERNS    # Padroes regex para highlight
|   |-- _setup_ui()           # Monta a interface grafica
|   |-- _create_header()      # Prompt verde no topo
|   |-- _create_editor_area() # Area de texto principal
|   |-- _create_nano_bar()    # Barra inferior estilo nano
|   |-- transliterate()       # Converte texto original para cirílico/grego
|   |-- apply_syntax_highlighting() # Aplica cores ao texto exibido
|   |-- on_key_press()        # Intercepta teclas digitadas
|   |-- on_paste()            # Trata colagem de texto
|   |-- copy_text()           # Copia o texto original (nao o exibido)
|   |-- update_status()       # Atualiza linha/coluna na barra
|
|-- perform_login()           # Fluxo de autenticacao (senha na linha 339)
|-- __main__                  # Ponto de entrada da aplicacao
```

---

## Comportamento da Transliteracao

O texto digitado e exibido transliterado, mas nunca alterado internamente. Veja alguns exemplos:

| Texto original | Exibido na tela  |
|----------------|------------------|
| `senha`        | `Σэнха`          |
| `python`       | `Ψытхон`         |
| `login`        | `логин`          |
| `arquivo`      | `арquивоу`       |

A copia via `Ctrl+C` sempre retorna o texto original.

---

## Observacoes de Segurança

- A senha e armazenada em texto puro no proprio arquivo. Para uso em ambientes com mais rigor de seguranca, recomenda-se substituir a verificacao por um hash (`hashlib`) ou variavel de ambiente.
- O arquivo `.pyw` nao exibe console, o que ja dificulta a identificacao rapida do software por terceiros.
- O nome `BUILD.PROP` imita um arquivo de configuracao de sistema Android, contribuindo para o camuflamento.

---

## Licenca

Distribuido para uso pessoal. Sem restricoes de uso nao comercial.
