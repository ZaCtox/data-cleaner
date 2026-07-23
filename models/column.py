from dataclasses import dataclass

import customtkinter as ctk


@dataclass
class Column:
    original: str
    nuevo: str
    checkbox: ctk.BooleanVar | None = None
    entry: ctk.StringVar | None = None
