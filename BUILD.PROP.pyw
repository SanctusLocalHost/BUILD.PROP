#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BUILD.PROP - Bloco de Notas Secreto
Translitera visualmente texto português para cirílico russo (com custom Greek rules)
e basic syntax highlighting.
Mantém o texto original para copiar/colar.
"""

# pip install customtkinter pyperclip

import customtkinter as ctk
import tkinter as tk 
import pyperclip
import re
from typing import Dict, List, Tuple, Optional

# --- Constants ---
COLOR_BLACK = "#000000"
COLOR_WHITE = "#FFFFFF"
COLOR_GREEN_PROMPT = "#00FF00"
COLOR_NANO_CMD_KEY = "#00FF00"
COLOR_NANO_CMD_TEXT = "#FFFFFF" # This is for the text itself, background should be black

FONT_CONSOLAS_NORMAL = ("Consolas", 14)
FONT_CONSOLAS_NANO = ("Consolas", 11)
FONT_CONSOLAS_PROMPT_BOLD = ("Consolas", 16, "bold")

UI_TEXT_HELP = "Help"; UI_TEXT_WRITE_OUT = "Write Out"; UI_TEXT_WHERE_IS = "Where Is"
UI_TEXT_CUT = "Cut"; UI_TEXT_EXECUTE = "Execute"; UI_TEXT_COPY = "Copy"
UI_TEXT_EXIT = "Exit"; UI_TEXT_READ_FILE = "Read File"; UI_TEXT_REPLACE = "Replace"
UI_TEXT_PASTE = "Paste"; UI_TEXT_JUSTIFY = "Justify"; UI_TEXT_GO_TO_LINE = "Go To Line"
UI_TEXT_LINE = "Line"; UI_TEXT_COL = "Col"; UI_TEXT_APP_TITLE = "BUILD.PROP"
UI_TEXT_COPIED_SUCCESS = "Texto original copiado!"; UI_TEXT_COPY_ERROR = "Erro ao copiar."

UI_TRANS_MAP: Dict[str, str] = { 
    'A': 'А', 'B': 'Б', 'C': 'К', 'D': 'Д', 'E': 'Э', 'F': 'Ф', 'G': 'Г', 'H': 'Х', 'I': 'И', 'J': 'ДЖ', 
    'K': 'К', 'L': 'Л', 'M': 'М', 'N': 'Н', 'O': 'О', 'P': 'П', 'Q': 'К', 'R': 'Р', 'S': 'С', 'T': 'Т', 
    'U': 'У', 'V': 'В', 'W': 'В', 'X': 'КС', 'Y': 'Ы', 'Z': 'З', 'a': 'а', 'b': 'б', 'c': 'к', 'd': 'д', 
    'e': 'э', 'f': 'ф', 'g': 'г', 'h': 'х', 'i': 'и', 'j': 'дж', 'k': 'к', 'l': 'л', 'm': 'м', 'n': 'н', 
    'o': 'о', 'p': 'п', 'q': 'к', 'r': 'р', 's': 'с', 't': 'т', 'u': 'у', 'v': 'в', 'w': 'в', 'x': 'кс', 
    'y': 'ы', 'z': 'з', '.': '.', ' ': ' ', '@': '@', '~': '~', '/': '/', '$': '$', '[': '[', ']': ']',
    '_': '_', '-': '-', '1': '1', '0': '0', ':':':', '|':'|', '^':'^', 'G':'Г', 'O':'О', 'F':'Ф', 
    'K':'К', 'T':'Т', 'X':'КС', 'R':'Р', 'L':'Л', 'U':'У', 'J':'Й', '\\':'\\'
}
NANO_CMD_TRANSLATIONS: Dict[str, str] = {
    UI_TEXT_HELP: "ПОМОЩЬ", UI_TEXT_WRITE_OUT: "ЗАПИСАТЬ", UI_TEXT_WHERE_IS: "НАЙТИ", UI_TEXT_CUT: "ВЫРЕЗАТЬ",
    UI_TEXT_EXECUTE: "ИСПОЛНИТЬ", UI_TEXT_COPY: "КОПИРОВАТЬ", UI_TEXT_EXIT: "ВЫХОД", UI_TEXT_READ_FILE: "ЧИТАТЬ ФАЙЛ",
    UI_TEXT_REPLACE: "ЗАМЕНИТЬ", UI_TEXT_PASTE: "ВСТАВИТЬ", UI_TEXT_JUSTIFY: "ВЫРОВНЯТЬ", UI_TEXT_GO_TO_LINE: "К ЛИНИИ",
    UI_TEXT_LINE: "ЛИНИЯ", UI_TEXT_COL: "КОЛ"
}
GENERAL_UI_TRANSLATIONS: Dict[str, str] = {
    UI_TEXT_APP_TITLE: "БУИЛД.ПРОП", UI_TEXT_COPIED_SUCCESS: "ТЭКСТО ОРИГИНАЛ КОПИАДО!", UI_TEXT_COPY_ERROR: "ЭРРО АО КОПИАР."
}

def transliterate_ui_text(text_key: str, is_nano_command_text: bool = False) -> str:
    if is_nano_command_text:
        translated = NANO_CMD_TRANSLATIONS.get(text_key)
        if translated: return translated
    translated = GENERAL_UI_TRANSLATIONS.get(text_key)
    if translated: return translated
    return "".join(UI_TRANS_MAP.get(char, char) for char in text_key)

class SecretNotepad:
    EDITOR_TRANS_MAP: Dict[str, str] = {
        'a': 'α', 'b': 'б', 'c': 'ск', 'd': 'д', 'e': 'э', 'f': 'ф', 'g': 'г', 'h': 'х', 'i': 'и', 'j': 'дж', 
        'k': 'к', 'l': 'л', 'm': 'м', 'n': 'н', 'o': 'о', 'p': 'п', 'q': 'к', 'r': 'р', 's': 'с', 't': 'т', 
        'u': 'у', 'v': 'в', 'w': 'в', 'x': 'ξ', 'y': 'ы', 'z': 'з', 'ç': 'с', 'A': 'А', 'B': 'Б', 'C': 'СК', 
        'D': 'Д', 'E': 'Э', 'F': 'Ф', 'G': 'Г', 'H': 'Х', 'I': 'И', 'J': 'ДЖ', 'K': 'К', 'L': 'Л', 'M': 'М', 
        'N': 'Н', 'O': 'Ω', 'P': 'П', 'Q': 'К', 'R': 'Р', 'S': 'С', 'T': 'Т', 'U': 'У', 'V': 'В', 'W': 'В', 
        'X': 'Ξ', 'Y': 'Ы', 'Z': 'З', 'Ç': 'С', 'á': 'α', 'à': 'α', 'ã': 'α', 'â': 'α', 'ä': 'α', 'é': 'э', 
        'è': 'э', 'ê': 'э', 'ë': 'э', 'í': 'и', 'ì': 'и', 'î': 'и', 'ï': 'и', 'ó': 'о', 'ò': 'о', 'õ': 'о', 
        'ô': 'о', 'ö': 'о', 'ú': 'у', 'ù': 'у', 'û': 'у', 'ü': 'у', 'Á': 'А', 'À': 'А', 'Ã': 'А', 'Â': 'А', 
        'Ä': 'А', 'É': 'Э', 'È': 'Э', 'Ê': 'Э', 'Ë': 'Э', 'Í': 'И', 'Ì': 'И', 'Î': 'И', 'Ï': 'И', 'Ó': 'Ω', 
        'Ò': 'Ω', 'Õ': 'Ω', 'Ô': 'Ω', 'Ö': 'Ω', 'Ú': 'У', 'Ù': 'У', 'Û': 'У', 'Ü': 'У',
    }
    HIGHLIGHT_COLORS: Dict[str, str] = {
        "string": "light sea green", "comment": "gray55", "bracket_delimiter": "orange", "paren_delimiter": "sky blue", 
        "brace_delimiter": "magenta", "bracket_content": "gold", "paren_content": "cyan", "brace_content": "lightcoral",
        "keyword": "orchid1", "number": "khaki1" 
    }
    HIGHLIGHT_PATTERNS: List[Tuple[str, str]] = [
        ("comment", r"#[^\n]*"), ("string", r'"[^"\\]*(?:\\.[^"\\]*)*"'), ("string", r"'[^'\\]*(?:\\.[^'\\]*)*'"), 
        ("number", r"\b\d+\.?\d*\b"), ("paren_content", r"\(([^()\\]*(?:\\.[^()\\]*)*)\)"), 
        ("bracket_content", r"\[([^\[\]\\]*(?:\\.[^\[\]\\]*)*)\]"), ("brace_content", r"\{([^\{\}\\]*(?:\\.[^\{\}\\]*)*)\}"),
        ("paren_delimiter", r"\(|\)"), ("bracket_delimiter", r"\[|\]"), ("brace_delimiter", r"\{|\}")
    ]

    def __init__(self):
        self.root = ctk.CTk()
        self.root.title(transliterate_ui_text(UI_TEXT_APP_TITLE)) 
        self.root.geometry("900x700")
        ctk.set_appearance_mode("dark")
        self.original_text: str = ""
        portuguese_keywords = ["if", "else", "elif", "for", "while", "def", "class", "return", "try", "except", "finally", 
                               "import", "from", "pass", "break", "continue", "True", "False", "None", "and", "or", 
                               "not", "in", "is", "lambda"]
        self.transliterated_keywords: List[str] = sorted(list(set(kw_trans for kw_trans in (self.transliterate(kw) for kw in portuguese_keywords) if kw_trans)), key=len, reverse=True)
        self._setup_ui(); self._bind_events(); self.update_status()

    def _define_highlight_tags(self):
        for tag_name, color in self.HIGHLIGHT_COLORS.items(): self.text_area.tag_config(tag_name, foreground=color)

    def _create_header(self, parent_frame: ctk.CTkFrame):
        header_frame = ctk.CTkFrame(parent_frame, fg_color=COLOR_BLACK)
        header_frame.pack(fill="x", padx=5, pady=(5, 10))
        ctk.CTkLabel(header_frame, text="SANCTUS@PARROT:~/BUILD.PROP$", font=FONT_CONSOLAS_PROMPT_BOLD, text_color=COLOR_GREEN_PROMPT).pack(side="left", padx=(0, 10))

    def _create_editor_area(self, parent_frame: ctk.CTkFrame):
        self.text_area = ctk.CTkTextbox(parent_frame, font=FONT_CONSOLAS_NORMAL, fg_color=COLOR_BLACK, text_color=COLOR_WHITE, wrap="word", border_width=0, undo=True)
        self.text_area.pack(fill="both", expand=True, padx=5, pady=0)
        self._define_highlight_tags()

    def _create_nano_bar(self, parent_frame: ctk.CTkFrame):
        nano_bar_bg = COLOR_BLACK # Explicitly use black for the nano bar background
        nano_main_bar_frame = ctk.CTkFrame(parent_frame, fg_color=nano_bar_bg, height=60)
        nano_main_bar_frame.pack(fill="x", side="bottom", pady=(2,0))
        self.nano_status_label = ctk.CTkLabel(nano_main_bar_frame, text="", font=FONT_CONSOLAS_NANO, text_color=COLOR_WHITE, fg_color=nano_bar_bg)
        self.nano_status_label.pack(fill="x", pady=2, padx=10)
        nano_commands = [
            [(UI_TEXT_HELP, "^G"), (UI_TEXT_WRITE_OUT, "^O"), (UI_TEXT_WHERE_IS, "^F"), (UI_TEXT_CUT, "^K"), (UI_TEXT_EXECUTE, "^T"), (UI_TEXT_COPY, "^C")],
            [(UI_TEXT_EXIT, "^X"), (UI_TEXT_READ_FILE, "^R"), (UI_TEXT_REPLACE, "^\\"), (UI_TEXT_PASTE, "^U"), (UI_TEXT_JUSTIFY, "^J"), (UI_TEXT_GO_TO_LINE, "^/")]
        ]
        for i, commands_row_keys in enumerate(nano_commands):
            row_frame = ctk.CTkFrame(nano_main_bar_frame, fg_color=nano_bar_bg)
            row_frame.pack(fill="x", pady=(0,2) if i == 1 else 0)
            for text_key, shortcut_key in commands_row_keys:
                cmd_frame = ctk.CTkFrame(row_frame, fg_color=nano_bar_bg)
                cmd_frame.pack(side="left", padx=(5,2))
                ctk.CTkLabel(cmd_frame, text=shortcut_key, font=FONT_CONSOLAS_NANO, text_color=COLOR_NANO_CMD_KEY, fg_color=nano_bar_bg).pack(side="left")
                ctk.CTkLabel(cmd_frame, text=" "+transliterate_ui_text(text_key, True), font=FONT_CONSOLAS_NANO, text_color=COLOR_NANO_CMD_TEXT, fg_color=nano_bar_bg).pack(side="left", padx=(0,5))
    
    def _setup_ui(self):
        self.root.configure(fg_color=COLOR_BLACK)
        editor_main_frame = ctk.CTkFrame(self.root, fg_color=COLOR_BLACK); editor_main_frame.pack(fill="both", expand=True)
        self._create_header(editor_main_frame); self._create_editor_area(editor_main_frame)
        self._create_nano_bar(self.root)

    def _bind_events(self):
        self.text_area.bind('<KeyPress>', self.on_key_press, add="+"); self.text_area.bind('<KeyRelease>', self.on_key_release, add="+")
        self.text_area.bind('<Control-v>', self.on_paste, add="+"); self.text_area.bind('<Control-V>', self.on_paste, add="+")

    def on_key_release(self, event: tk.Event):
        if event.keysym in ['Left', 'Right', 'Up', 'Down', 'Home', 'End', 'Prior', 'Next', 'BackSpace', 'Delete', 'Return'] or \
           (event.state & 0x4 and event.keysym.lower() in ['a','v','x']):
            self.update_status()
            if event.keysym in ['BackSpace', 'Delete', 'Return'] or (event.state & 0x4 and event.keysym.lower() == 'v'):
                 self.apply_syntax_highlighting()

    def on_key_press(self, event: tk.Event):
        nav_keys = ['Left', 'Right', 'Up', 'Down', 'Home', 'End', 'Prior', 'Next', 'Shift_L', 'Shift_R', 'Control_L', 'Control_R', 'Alt_L', 'Alt_R', 'Tab', 'Caps_Lock', 'Escape'] + [f'F{i}' for i in range(1, 13)]
        if event.keysym in nav_keys: return 
        is_ctrl_pressed = (event.state & 0x4) != 0
        if is_ctrl_pressed:
            key_lower = event.keysym.lower()
            if key_lower == 'a': self.select_all_text(); return "break" 
            if key_lower == 'c': self.copy_text(); return "break"
            if key_lower == 'v': self.on_paste(event); return "break" 
            if key_lower == 'x': 
                self.copy_text() 
                try:
                    sel_first_tk = self.text_area.index(tk.SEL_FIRST); sel_last_tk = self.text_area.index(tk.SEL_LAST)
                    orig_sel_start = self._get_original_pos_from_tk_idx_str(sel_first_tk); orig_sel_end = self._get_original_pos_from_tk_idx_str(sel_last_tk)
                    if orig_sel_start < orig_sel_end: self.original_text = self.original_text[:orig_sel_start] + self.original_text[orig_sel_end:]; self.update_display_and_cursor(orig_sel_start)
                except tk.TclError: pass
                return "break"
            if key_lower == 'z': return 
            return 
        final_orig_cursor_pos = -1 
        try: 
            sel_first_tk = self.text_area.index(tk.SEL_FIRST); sel_last_tk = self.text_area.index(tk.SEL_LAST)
            orig_sel_start = self._get_original_pos_from_tk_idx_str(sel_first_tk); orig_sel_end = self._get_original_pos_from_tk_idx_str(sel_last_tk)
            if orig_sel_start < orig_sel_end: 
                if event.keysym in ['BackSpace', 'Delete']: self.original_text = self.original_text[:orig_sel_start] + self.original_text[orig_sel_end:]; final_orig_cursor_pos = orig_sel_start
                elif event.char and event.char.isprintable(): self.original_text = self.original_text[:orig_sel_start] + event.char + self.original_text[orig_sel_end:]; final_orig_cursor_pos = orig_sel_start + len(event.char)
        except tk.TclError: 
            current_orig_cursor_pos = self._get_original_pos_from_tk_idx_str(self.text_area.index(tk.INSERT))
            if event.keysym == 'BackSpace':
                if current_orig_cursor_pos > 0: self.original_text = self.original_text[:current_orig_cursor_pos-1] + self.original_text[current_orig_cursor_pos:]; final_orig_cursor_pos = current_orig_cursor_pos - 1
            elif event.keysym == 'Delete':
                if current_orig_cursor_pos < len(self.original_text): self.original_text = self.original_text[:current_orig_cursor_pos] + self.original_text[current_orig_cursor_pos+1:]; final_orig_cursor_pos = current_orig_cursor_pos
            elif event.char and event.char.isprintable(): self.original_text = self.original_text[:current_orig_cursor_pos] + event.char + self.original_text[current_orig_cursor_pos:]; final_orig_cursor_pos = current_orig_cursor_pos + len(event.char)
            elif event.keysym == 'Return': self.original_text = self.original_text[:current_orig_cursor_pos] + '\n' + self.original_text[current_orig_cursor_pos:]; final_orig_cursor_pos = current_orig_cursor_pos + 1
        if final_orig_cursor_pos != -1: self.update_display_and_cursor(final_orig_cursor_pos); return "break"
        return 

    def _get_char_transliteration(self, char_to_trans: str, p_count: int, i_count: int, is_first_char_of_word: bool) -> str:
        if char_to_trans.lower() == 'p' and p_count == 2: return 'Ψ' if char_to_trans.isupper() else 'ψ'
        if is_first_char_of_word and char_to_trans == 'S': return 'Σ'
        if char_to_trans.lower() == 'i' and i_count == 2: return 'Й' if char_to_trans.isupper() else 'й'
        return self.EDITOR_TRANS_MAP.get(char_to_trans, char_to_trans)

    def _get_original_pos_from_tk_idx_str(self, tk_idx_str: str) -> int:
        try: self.text_area.index(tk_idx_str); cyrillic_prefix_target_len = len(self.text_area.get("0.0", tk_idx_str))
        except tk.TclError: cyrillic_prefix_target_len = 0 
        if cyrillic_prefix_target_len == 0: return 0
        current_transliterated_len = 0; original_idx_counter = 0 
        words_in_original = re.findall(r'\S+|\s+', self.original_text)
        if not self.original_text and cyrillic_prefix_target_len > 0: return 0
        for word_orig in words_in_original:
            if not word_orig.strip(): 
                for space_char in word_orig:
                    current_transliterated_len += len(space_char); original_idx_counter += 1
                    if current_transliterated_len >= cyrillic_prefix_target_len: return original_idx_counter
                continue
            i_count_in_word = 0; p_count_in_word = 0; is_first_char_of_word = True
            for orig_char_in_word in word_orig:
                if orig_char_in_word.lower() == 'i': i_count_in_word += 1
                if orig_char_in_word.lower() == 'p': p_count_in_word += 1
                trans_segment = self._get_char_transliteration(orig_char_in_word, p_count_in_word, i_count_in_word, is_first_char_of_word)
                is_first_char_of_word = False
                if current_transliterated_len + len(trans_segment) >= cyrillic_prefix_target_len: original_idx_counter += 1; return original_idx_counter
                current_transliterated_len += len(trans_segment); original_idx_counter += 1
        return original_idx_counter

    def update_display_and_cursor(self, new_original_cursor_position: int):
        new_original_cursor_position = max(0, min(new_original_cursor_position, len(self.original_text)))
        cyrillic_full_text = self.transliterate(self.original_text)
        current_yview = self.text_area.yview(); sel_orig_start, sel_orig_end = -1, -1
        try:
            sel_first_tk = self.text_area.index(tk.SEL_FIRST); sel_last_tk = self.text_area.index(tk.SEL_LAST)
            sel_orig_start = self._get_original_pos_from_tk_idx_str(sel_first_tk); sel_orig_end = self._get_original_pos_from_tk_idx_str(sel_last_tk)
        except tk.TclError: pass
        self.text_area.unbind('<KeyPress>')
        self.text_area.delete("0.0", tk.END); self.text_area.insert("0.0", cyrillic_full_text)
        self.text_area.bind('<KeyPress>', self.on_key_press, add="+")
        self.apply_syntax_highlighting(); self.text_area.yview_moveto(current_yview[0])
        cyrillic_prefix_to_cursor = self.transliterate(self.original_text[:new_original_cursor_position])
        new_tk_cursor_str = f"0.0 + {len(cyrillic_prefix_to_cursor)}c" 
        self.text_area.mark_set(tk.INSERT, new_tk_cursor_str); self.text_area.see(tk.INSERT) 
        if sel_orig_start != -1 and sel_orig_end != -1 and sel_orig_start < sel_orig_end:
            sel_cyr_start_text = self.transliterate(self.original_text[:sel_orig_start]); sel_cyr_end_text = self.transliterate(self.original_text[:sel_orig_end])
            tk_sel_start = f"0.0 + {len(sel_cyr_start_text)}c"; tk_sel_end = f"0.0 + {len(sel_cyr_end_text)}c"
            self.text_area.tag_add(tk.SEL, tk_sel_start, tk_sel_end)
        self.update_status()

    def transliterate(self, text: str) -> str:
        result_parts: List[str] = []; words_and_spaces = re.findall(r'\S+|\s+', text) 
        for segment in words_and_spaces:
            if not segment.strip(): result_parts.append(segment); continue
            word_result = ""; i_count = 0; p_count = 0; is_first_char_of_word = True
            for char_in_word in segment:
                if char_in_word.lower() == 'i': i_count += 1
                if char_in_word.lower() == 'p': p_count += 1
                word_result += self._get_char_transliteration(char_in_word, p_count, i_count, is_first_char_of_word)
                is_first_char_of_word = False
            result_parts.append(word_result)
        return "".join(result_parts)

    def apply_syntax_highlighting(self):
        if not hasattr(self, 'text_area') or not self.text_area.winfo_exists(): return
        current_insert = self.text_area.index(tk.INSERT); selection_ranges = self.text_area.tag_ranges(tk.SEL)
        for tag_name in self.HIGHLIGHT_COLORS.keys(): self.text_area.tag_remove(tag_name, "0.0", tk.END)
        current_displayed_text = self.text_area.get("0.0", tk.END)
        if not current_displayed_text.strip(): return
        for tag_name, pattern_str in [p for p in self.HIGHLIGHT_PATTERNS if tag_name in ["comment", "string"]]:
            for match in re.finditer(pattern_str, current_displayed_text, flags=re.UNICODE): self.text_area.tag_add(tag_name, f"0.0 + {match.start()}c", f"0.0 + {match.end()}c")
        for tag_name, pattern_str in [p for p in self.HIGHLIGHT_PATTERNS if tag_name == "number"]:
            for match in re.finditer(pattern_str, current_displayed_text, flags=re.UNICODE):
                if not any(t in self.text_area.tag_names(f"0.0 + {match.start()}c") for t in ["string", "comment"]): self.text_area.tag_add(tag_name, f"0.0 + {match.start()}c", f"0.0 + {match.end()}c")
        for tag_name, pattern_str in [p for p in self.HIGHLIGHT_PATTERNS if "_content" in tag_name]:
            for match in re.finditer(pattern_str, current_displayed_text, flags=re.UNICODE):
                if match.lastindex and match.lastindex >= 1:
                    content_start, content_end = match.span(1)
                    check_idx = f"0.0 + {content_start}c" if content_start == content_end else f"0.0 + {(content_start + content_end) // 2}c"
                    if not any(t in self.text_area.tag_names(check_idx) for t in ["string", "comment"]): self.text_area.tag_add(tag_name, f"0.0 + {content_start}c", f"0.0 + {content_end}c")
        for tag_name, pattern_str in [p for p in self.HIGHLIGHT_PATTERNS if "_delimiter" in tag_name]:
            for match in re.finditer(pattern_str, current_displayed_text, flags=re.UNICODE):
                if not any(t in self.text_area.tag_names(f"0.0 + {match.start()}c") for t in ["string", "comment"]): self.text_area.tag_add(tag_name, f"0.0 + {match.start()}c", f"0.0 + {match.end()}c")
        if self.transliterated_keywords:
            keyword_regex_str = r"\b(" + "|".join(re.escape(kw) for kw in self.transliterated_keywords) + r")\b"
            try:
                keyword_regex = re.compile(keyword_regex_str, flags=re.UNICODE)
                for match in keyword_regex.finditer(current_displayed_text):
                    start, end = match.span()
                    tags_at_start = self.text_area.tag_names(f"0.0 + {start}c")
                    higher_precedence_tags = ["string", "comment", "number", "paren_content", "bracket_content", "brace_content", "paren_delimiter", "bracket_delimiter", "brace_delimiter"]
                    if not any(htag in tags_at_start for htag in higher_precedence_tags): self.text_area.tag_add("keyword", f"0.0 + {start}c", f"0.0 + {end}c")
            except re.error: pass
        self.text_area.mark_set(tk.INSERT, current_insert)
        if selection_ranges: self.text_area.tag_add(tk.SEL, selection_ranges[0], selection_ranges[1])

    def on_paste(self, event: Optional[tk.Event] = None): 
        try:
            pasted_text = self.root.clipboard_get();
            if not pasted_text: return "break"
            current_tk_cursor_pos_str = self.text_area.index(tk.INSERT); orig_insert_pos = 0
            try: 
                sel_first_tk = self.text_area.index(tk.SEL_FIRST); sel_last_tk = self.text_area.index(tk.SEL_LAST)
                orig_sel_start = self._get_original_pos_from_tk_idx_str(sel_first_tk); orig_sel_end = self._get_original_pos_from_tk_idx_str(sel_last_tk)
                self.original_text = self.original_text[:orig_sel_start] + pasted_text + self.original_text[orig_sel_end:]; orig_insert_pos = orig_sel_start + len(pasted_text)
            except tk.TclError: 
                orig_insert_pos_at_cursor = self._get_original_pos_from_tk_idx_str(current_tk_cursor_pos_str)
                self.original_text = self.original_text[:orig_insert_pos_at_cursor] + pasted_text + self.original_text[orig_insert_pos_at_cursor:]; orig_insert_pos = orig_insert_pos_at_cursor + len(pasted_text)
            self.update_display_and_cursor(orig_insert_pos)
        except Exception: pass
        return "break" 

    def copy_text(self, event: Optional[tk.Event] = None):
        try:
            pyperclip.copy(self.original_text) 
            feedback_msg = transliterate_ui_text(UI_TEXT_COPIED_SUCCESS) 
            original_nano_status = self.nano_status_label.cget("text")
            self.nano_status_label.configure(text=f"[ {feedback_msg} ]")
            self.root.after(2000, lambda: self.nano_status_label.configure(text=original_nano_status) if hasattr(self, 'nano_status_label') and self.nano_status_label.winfo_exists() else self.update_status())
        except Exception:
            error_msg = transliterate_ui_text(UI_TEXT_COPY_ERROR)
            original_nano_status = self.nano_status_label.cget("text")
            self.nano_status_label.configure(text=f"[ {error_msg} ]")
            self.root.after(2000, lambda: self.nano_status_label.configure(text=original_nano_status) if hasattr(self, 'nano_status_label') and self.nano_status_label.winfo_exists() else self.update_status())
        return "break"

    def clear_all_text(self): self.original_text = ""; self.update_display_and_cursor(0)
    def select_all_text(self, event: Optional[tk.Event] = None): self.text_area.tag_add(tk.SEL, "0.0", tk.END); return "break" 

    def update_status(self):
        if not hasattr(self, 'nano_status_label') or not self.nano_status_label.winfo_exists(): return
        cursor_orig_pos = 0
        try: current_tk_insert = self.text_area.index(tk.INSERT); cursor_orig_pos = self._get_original_pos_from_tk_idx_str(current_tk_insert)
        except tk.TclError: cursor_orig_pos = len(self.original_text) 
        text_before_cursor_orig = self.original_text[:cursor_orig_pos]
        cursor_line_orig = text_before_cursor_orig.count('\n') + 1
        cursor_col_orig = len(text_before_cursor_orig.split('\n')[-1]) + 1
        total_lines_orig = self.original_text.count('\n') +1 if self.original_text else 1
        line_str = transliterate_ui_text(UI_TEXT_LINE, True); col_str = transliterate_ui_text(UI_TEXT_COL, True)
        self.nano_status_label.configure(text=f"[ {line_str} {cursor_line_orig}/{total_lines_orig}  {col_str} {cursor_col_orig} ]")

    def run(self): self.root.mainloop()

if __name__ == "__main__":
    app = SecretNotepad()
    app.run()