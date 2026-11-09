import customtkinter as ctk

import theme

COLUMN_SPECS = (
    ("primary", 180, 2),
    ("secondary", 200, 3),
    ("tertiary", 160, 2),
    ("quaternary", 200, 3),
)
ACTION_WIDTH = 144
CARD_HEIGHT = 94
FIRST_CELL_PAD_X = 20
CELL_PAD_X = 12
ACTION_PAD_RIGHT = 18


def configure_columns(frame, with_actions=True):
    for index, (_, minsize, weight) in enumerate(COLUMN_SPECS):
        frame.grid_columnconfigure(index, minsize=minsize, weight=weight)
    action_width = ACTION_WIDTH if with_actions else 0
    frame.grid_columnconfigure(len(COLUMN_SPECS), minsize=action_width, weight=0)


class DataCell(ctk.CTkFrame):
    def __init__(self, master, header, value, padx):
        super().__init__(master, fg_color="transparent", width=1, height=1)
        self.grid_propagate(False)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self._padx = padx

        self.header = ctk.CTkLabel(
            self,
            text=header,
            font=theme.small_font(),
            text_color=theme.COLORS["muted"],
            anchor="w",
            justify="left",
        )
        self.header.grid(row=0, column=0, sticky="ew", padx=padx, pady=(12, 2))

        self.value = ctk.CTkLabel(
            self,
            text=value,
            font=theme.body_font(),
            text_color=theme.COLORS["text"],
            anchor="nw",
            justify="left",
        )
        self.value.grid(row=1, column=0, sticky="new", padx=padx, pady=(0, 10))
        self.bind("<Configure>", self._resize_value)

    def _resize_value(self, event):
        wraplength = max(40, event.width - 2 * self._padx)
        self.value.configure(wraplength=wraplength)


class TableCard(ctk.CTkFrame):
    def __init__(self, master, values, with_actions=True):
        if len(values) != len(COLUMN_SPECS):
            raise ValueError("TableCard expects one value per column")
        super().__init__(
            master,
            fg_color=theme.COLORS["surface"],
            corner_radius=theme.RADIUS["card"],
            width=1,
            height=CARD_HEIGHT,
        )
        self.grid_propagate(False)
        self.grid_rowconfigure(0, weight=1)
        configure_columns(self, with_actions)

        self.cells = []
        for index, (header, value) in enumerate(values):
            padx = FIRST_CELL_PAD_X if index == 0 else CELL_PAD_X
            cell = DataCell(self, header, value, padx)
            cell.grid(row=0, column=index, sticky="nsew")
            self.cells.append(cell)

        self.action_rail = None
        if with_actions:
            self.action_rail = ctk.CTkFrame(
                self,
                fg_color="transparent",
                width=1,
                height=1,
            )
            self.action_rail.pack_propagate(False)
            self.action_rail.grid(
                row=0,
                column=len(values),
                sticky="nsew",
            )
