"""Common helpers for simple pygame views."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

import pygame


class BaseView:
    """Provides shared drawing utilities for the shopping cart UI."""

    BG_COLOR = (250, 250, 250)
    TEXT_COLOR = (40, 40, 40)
    SUBTEXT_COLOR = (90, 90, 90)
    MESSAGE_COLOR = (200, 60, 60)
    SUCCESS_COLOR = (40, 140, 90)
    HIGHLIGHT_COLOR = (230, 240, 255)

    FONT_CANDIDATES: Iterable[str | None] = (
        "/System/Library/Fonts/PingFang.ttc",  # macOS traditional Chinese
        "/System/Library/Fonts/STHeiti Light.ttc",
        "/System/Library/Fonts/Helvetica.ttc",
        None,  # pygame default font fallback
    )

    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        pygame.font.init()
        self.title_font = self._load_font(32)
        self.body_font = self._load_font(22)
        self.small_font = self._load_font(18)

    def draw_title(self, text: str, y: int = 20) -> int:
        surface = self.title_font.render(text, True, self.TEXT_COLOR)
        self.screen.blit(surface, (40, y))
        return y + surface.get_height() + 10

    def draw_line(self, text: str, y: int, *, color=None, indent: int = 40, font=None) -> int:
        font = font or self.body_font
        surface = font.render(text, True, color or self.TEXT_COLOR)
        self.screen.blit(surface, (indent, y))
        return y + surface.get_height() + 6

    def draw_message(self, text: str, y: int, *, success: bool = False) -> int:
        if not text:
            return y
        color = self.SUCCESS_COLOR if success else self.MESSAGE_COLOR
        return self.draw_line(text, y, color=color, font=self.body_font)

    # Internal helpers -------------------------------------------------

    def _load_font(self, size: int) -> pygame.font.Font:
        for candidate in self.FONT_CANDIDATES:
            if candidate is None:
                break
            path = Path(candidate)
            if path.exists():
                try:
                    return pygame.font.Font(str(path), size)
                except OSError:
                    continue
        return pygame.font.Font(None, size)
