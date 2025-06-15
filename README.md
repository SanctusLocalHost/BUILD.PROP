# BUILD.PROP - (БУИЛД.ПРОП)

Um editor de texto único que translitera Português para Cirílico Russo (com toques de Grego) em tempo real. Ele mantém o texto original para cópia e aplica formatação de cores estilo IDE.

## Preview
![Image](https://github.com/user-attachments/assets/0059ebec-ce67-423d-8127-baf9e97d4464)

## Destaques

*   **Transliteração Instantânea:** Digite em Português, veja em Russo Cirílico (com caracteres especiais como Ω, Ξ, α).
*   **Cópia em Português:** `CTRL+C` copia o texto **original em Português**, não o Cirílico.
*   **Colagem Transliterada:** `CTRL+V` cola texto (assumido como Português) e o exibe em Cirílico.
*   **Cores de IDE:** Realce visual para strings, comentários, números e palavras-chave.
*   **Interface Nano:** Barra de status e comandos na parte inferior.

## Como Funciona

Você digita em Português, mas vê em Russo na tela. Ao usar `CTRL+C`, o texto original em Português é copiado. Se colar algo (`CTRL+V`), esse texto é adicionado ao seu original em Português e a tela atualiza com a nova versão em Russo.

## Pré-requisitos

*   Python 3.x
*   Bibliotecas: `customtkinter`, `pyperclip`

## Instalação

1.  Certifique-se de ter o Python 3.
2.  Instale as dependências:
    ```bash
    pip install customtkinter pyperclip
    ```

## Como Usar

1.  Salve o código como um arquivo `.py` (ex: `editor_secreto.py`).
2.  Execute no terminal:
    ```bash
    python editor_secreto.py
    ```

## Atalhos Chave

*   **`CTRL + A`**: Seleciona tudo.
*   **`CTRL + C`**: Copia o texto original (Português).
*   **`CTRL + V`**: Cola texto (será transliterado).
*   **`CTRL + X`**: Recorta (copia o original em Português).
*   *Outros atalhos são exibidos na barra inferior.*

---

Divirta-se!
