from __future__ import annotations

from gradio.themes.base import Base
from typing import Iterable
from gradio.themes.utils import colors, sizes, fonts
from AinaTheme.utils import custom_colors


class AinaGradioTheme(Base):
    css = """
    div.meta-text { color: #000000; }
    .dark div.meta-text { color: #FFFFFF; }

    .textbox textarea { background: #f5f5f5; }
    .dark .textbox textarea { color: #000000; }

    div.label-wrap { color: #000000; }
    .dark div.label-wrap { color: #FFFFFF; }

    button.label-wrap { color: #000000; }
    .dark button.label-wrap { color: #FFFFFF; }
    
    div.table-wrap {color: #000000}
    .dark div.table-wrap {color: #FFFFFF;}

    textarea[data-testid="textbox"] { border: 1px solid #e5e5e5;}

    div.gallery { color: #000000; }
    .dark div.gallery { color: #FFFFFF; }
    
    .no-cat span.text  { color: #000000; }
    .dark .no-cat span.text { color: #FFFFFF; }
    """

    def __init__(
            self,
            *,
            # primary_hue: colors.Color | str = colors.indigo,
            primary_hue: str = custom_colors.primary,
            secondary_hue: str = custom_colors.secondary,
            neutral_hue: colors.Color | str = colors.neutral,
            spacing_size: sizes.Size | str = sizes.spacing_md,
            radius_size: sizes.Size | str = sizes.radius_md,
            text_size: sizes.Size | str = sizes.text_md,
            font: fonts.Font
                  | str
                  | Iterable[fonts.Font | str] = (
                    fonts.GoogleFont("Quicksand"),
                    "ui-sans-serif",
                    "sans-serif",
            ),
            font_mono: fonts.Font
                       | str
                       | Iterable[fonts.Font | str] = (
                    fonts.GoogleFont("IBM Plex Mono"),
                    "ui-monospace",
                    "monospace",
            ),
    ):
        super().__init__(
            primary_hue=primary_hue,
            secondary_hue=secondary_hue,
            neutral_hue=neutral_hue,
            spacing_size=spacing_size,
            radius_size=radius_size,
            text_size=text_size,
            font=font,
            font_mono=font_mono,
        )
        super().set(
            background_fill_primary="*neutral_50",
            slider_color="*primary_500",
            slider_color_dark="*primary_600",
            shadow_drop="0 1px 4px 0 rgb(0 0 0 / 0.1)",
            shadow_drop_lg="0 2px 5px 0 rgb(0 0 0 / 0.1)",
            block_background_fill="white",
            block_label_padding="*spacing_md *spacing_lg",
            block_label_background_fill="*primary_100",
            block_label_background_fill_dark="*primary_600",
            block_label_radius="*radius_md",
            block_label_text_size="*text_md",
            block_label_text_weight="600",
            block_label_text_color="black",
            block_label_text_color_dark="white",
            block_title_radius="*block_label_radius",
            block_title_padding="*block_label_padding",
            block_title_background_fill="*primary_700",
            block_title_text_weight="600",
            block_title_text_color="white",
            block_title_text_color_dark="white",
            block_label_margin="*spacing_md",
            input_placeholder_color="black",
            input_background_fill="white",
            input_border_color="*neutral_50",
            input_shadow="*shadow_drop",
            input_shadow_focus="*shadow_drop_lg",
            checkbox_shadow="none",

            # Color accents
            color_accent="*secondary_800",
            color_accent_soft="*neutral_100",
            border_color_accent_dark="*color_accent",

            # Buttons
            shadow_spread="6px",
            button_shadow="*shadow_drop_lg",
            button_shadow_hover="*shadow_drop_lg",
            button_shadow_active="*shadow_inset",
            button_primary_background_fill="*primary_800",
            button_primary_background_fill_hover="*secondary_700",
            button_primary_text_color_hover="white",
            button_primary_background_fill_hover_dark="*secondary_800",
            button_primary_text_color="white",
            button_secondary_background_fill="*button_primary_background_fill",
            button_secondary_background_fill_dark="*button_primary_background_fill",
            button_secondary_background_fill_hover="*button_primary_background_fill_hover",
            button_secondary_background_fill_hover_dark="*secondary_800",
            button_secondary_text_color="*button_primary_text_color",
            button_cancel_background_fill="*button_secondary_background_fill",
            button_cancel_background_fill_hover="*button_secondary_background_fill_hover",
            button_cancel_background_fill_hover_dark="*button_secondary_background_fill_hover",
            button_cancel_text_color="*button_secondary_text_color",
            button_transition="background-color 0.4s ease",
            # Checkbox
            checkbox_label_shadow="*shadow_drop_lg",
            checkbox_label_background_fill_selected="*primary_100",
            checkbox_label_background_fill_selected_dark="*primary_600",
            checkbox_border_width="2px",
            checkbox_border_width_dark="2px",
            checkbox_border_color="gray",
            checkbox_border_color_dark="*primary_800",
            checkbox_background_color_selected="*primary_600",
            checkbox_background_color_selected_dark="*primary_700",
            checkbox_border_color_focus="*primary_500",
            checkbox_border_color_focus_dark="*primary_600",
            checkbox_border_color_selected="black",
            checkbox_border_color_selected_dark="*primary_700",
            checkbox_label_text_color_selected="black",
            checkbox_label_text_color_selected_dark="white",
            checkbox_label_text_weight="600",
            checkbox_label_background_fill="*neutral_100",

            # Links
            link_text_color="*primary_950",
            link_text_color_hover="*secondary_950",
            # Borders
            block_border_width="0px",
            panel_border_width="1px",
        )

    def get_kwargs(self):
        return {'css': self.css, 'theme': self}
