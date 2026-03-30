"""
Brand application module for Accelerate Data document styling.
Applies consistent AD branding to Excel, PowerPoint, and PDF documents.

All color and font values are sourced from the authoritative brand_book.
"""

from typing import Any, Dict, List


class BrandFormatter:
    """Apply Accelerate Data brand guidelines to documents."""

    # Brand color definitions from brand_book (AUTHORITATIVE SOURCE)
    # Pages 2-3: Digital Sophistication palette
    COLORS = {
        "primary": {
            "pacific": {"hex": "#00b4d8", "rgb": (0, 180, 216)},      # DOMINANT - technology, innovation
            "navy": {"hex": "#03045e", "rgb": (3, 4, 94)},            # SUB-DOMINANT - depth, stability
            "seafoam": {"hex": "#00dd92", "rgb": (0, 221, 146)},      # ACCENT - energy, creativity
        },
        "secondary": {
            "powder": {"hex": "#caf0f8", "rgb": (202, 240, 248)},     # Breakers, light backgrounds
            "arctic": {"hex": "#90e0ef", "rgb": (144, 224, 239)},     # Graphics, icons
            "ocean": {"hex": "#0077b6", "rgb": (0, 119, 182)},        # Breakers, backgrounds
        },
        "neutrals": {
            "pearl": {"hex": "#f2f2f2", "rgb": (242, 242, 242)},      # Sub-headers, body copy, light bg
            "smoke": {"hex": "#171c21", "rgb": (23, 28, 33)},         # Body copy, dark mode base
            "white": {"hex": "#ffffff", "rgb": (255, 255, 255)},
        },
        "semantic": {
            "success": {"hex": "#00dd92", "rgb": (0, 221, 146)},      # Seafoam for brand alignment
            "warning": {"hex": "#f59e0b", "rgb": (245, 158, 11)},     # Amber for universal recognition
            "error": {"hex": "#ef4444", "rgb": (239, 68, 68)},        # Red for immediate attention
            "info": {"hex": "#00b4d8", "rgb": (0, 180, 216)},         # Pacific for brand alignment
        },
    }

    # Font definitions aligned with brand personality
    # Clean, geometric, systems-minded aesthetic
    FONTS = {
        "primary": "Geist",
        "fallback": ["SF Pro", "system-ui", "-apple-system", "sans-serif"],
        "monospace": ["Geist Mono", "SF Mono", "Menlo", "monospace"],
        "sizes": {
            "display": 32,
            "h1": 24,
            "h2": 18,
            "h3": 16,
            "body": 14,
            "body_small": 13,
            "caption": 12,
            "micro": 11,
        },
        "weights": {"regular": 400, "medium": 500, "semibold": 600},
    }

    # Company information
    COMPANY = {
        "name": "Accelerate Data",
        "tagline": "vibeData",
        "copyright": "2026 Accelerate Data. All rights reserved.",
        "logo_cdn_base": "http://assets.acceleratedata.ai/logo/",
    }

    def __init__(self):
        """Initialize brand formatter with AD standard settings."""
        self.colors = self.COLORS
        self.fonts = self.FONTS
        self.company = self.COMPANY

    def format_excel(self, workbook_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Apply AD brand formatting to Excel workbook configuration.

        Args:
            workbook_config: Excel workbook configuration dictionary

        Returns:
            Branded workbook configuration
        """
        branded_config = workbook_config.copy()

        # Apply header formatting - Pacific background per brand_book
        branded_config["header_style"] = {
            "font": {
                "name": self.fonts["primary"],
                "size": self.fonts["sizes"]["body"],
                "bold": True,
                "color": self.colors["neutrals"]["white"]["hex"],
            },
            "fill": {"type": "solid", "color": self.colors["primary"]["pacific"]["hex"]},
            "alignment": {"horizontal": "center", "vertical": "center"},
            "border": {"style": "thin", "color": self.colors["neutrals"]["pearl"]["hex"]},
        }

        # Apply subheader formatting - Navy text
        branded_config["subheader_style"] = {
            "font": {
                "name": self.fonts["primary"],
                "size": self.fonts["sizes"]["body"],
                "bold": True,
                "color": self.colors["primary"]["navy"]["hex"],
            },
        }

        # Apply data cell formatting
        branded_config["cell_style"] = {
            "font": {
                "name": self.fonts["primary"],
                "size": self.fonts["sizes"]["body"],
                "color": self.colors["primary"]["navy"]["hex"],
            },
            "alignment": {"horizontal": "left", "vertical": "center"},
        }

        # Apply alternating row colors for readability
        branded_config["alternating_rows"] = {
            "enabled": True,
            "color": self.colors["neutrals"]["pearl"]["hex"],
        }

        # Chart color scheme using brand palette
        branded_config["chart_colors"] = [
            self.colors["primary"]["pacific"]["hex"],
            self.colors["primary"]["seafoam"]["hex"],
            self.colors["secondary"]["ocean"]["hex"],
            self.colors["primary"]["navy"]["hex"],
            self.colors["secondary"]["arctic"]["hex"],
            self.colors["secondary"]["powder"]["hex"],
        ]

        return branded_config

    def format_powerpoint(self, presentation_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Apply AD brand formatting to PowerPoint presentation configuration.

        Args:
            presentation_config: PowerPoint configuration dictionary

        Returns:
            Branded presentation configuration
        """
        branded_config = presentation_config.copy()

        # Slide master settings
        branded_config["master"] = {
            "background_color": self.colors["neutrals"]["white"]["hex"],
            "title_area": {
                "font": self.fonts["primary"],
                "size": self.fonts["sizes"]["h1"],
                "weight": self.fonts["weights"]["semibold"],
                "color": self.colors["primary"]["pacific"]["hex"],
                "position": {"x": 0.5, "y": 0.15, "width": 9, "height": 1},
            },
            "content_area": {
                "font": self.fonts["primary"],
                "size": self.fonts["sizes"]["body"],
                "color": self.colors["primary"]["navy"]["hex"],
                "position": {"x": 0.5, "y": 2, "width": 9, "height": 5},
            },
            "footer": {
                "show_slide_number": True,
                "show_date": True,
                "company_name": self.company["name"],
            },
        }

        # Title slide template - Pacific background
        branded_config["title_slide"] = {
            "background": self.colors["primary"]["pacific"]["hex"],
            "title_color": self.colors["neutrals"]["white"]["hex"],
            "subtitle_color": self.colors["neutrals"]["white"]["hex"],
            "include_logo": True,
            "logo_url": f"{self.company['logo_cdn_base']}product/ui/logo-light-h48.svg",
        }

        # Section divider slide - Navy background
        branded_config["section_divider"] = {
            "background": self.colors["primary"]["navy"]["hex"],
            "title_color": self.colors["neutrals"]["white"]["hex"],
        }

        # Content slide template
        branded_config["content_slide"] = {
            "title_bar": {
                "background": self.colors["primary"]["pacific"]["hex"],
                "text_color": self.colors["neutrals"]["white"]["hex"],
                "height": 1,
            },
            "content_background": self.colors["neutrals"]["pearl"]["hex"],
            "bullet_style": {"level1": "bullet", "level2": "circle", "level3": "square", "indent": 0.25},
        }

        # Chart defaults
        branded_config["charts"] = {
            "color_scheme": [
                self.colors["primary"]["pacific"]["hex"],
                self.colors["primary"]["seafoam"]["hex"],
                self.colors["secondary"]["ocean"]["hex"],
                self.colors["primary"]["navy"]["hex"],
            ],
            "gridlines": {"color": self.colors["neutrals"]["pearl"]["hex"], "width": 0.5},
            "font": {"name": self.fonts["primary"], "size": self.fonts["sizes"]["caption"]},
            "no_3d_effects": True,
            "no_gradients": True,
        }

        return branded_config

    def format_pdf(self, document_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Apply AD brand formatting to PDF document configuration.

        Args:
            document_config: PDF document configuration dictionary

        Returns:
            Branded document configuration
        """
        branded_config = document_config.copy()

        # Page layout
        branded_config["page"] = {
            "margins": {"top": 1, "bottom": 1, "left": 1, "right": 1},
            "size": "letter",
            "orientation": "portrait",
            "line_spacing": 1.15,
            "paragraph_spacing": 12,
        }

        # Header configuration
        branded_config["header"] = {
            "height": 0.75,
            "content": {
                "left": {
                    "type": "logo",
                    "url": f"{self.company['logo_cdn_base']}product/ui/logo-dark-h32.svg",
                    "width": 1.5,
                },
                "center": {
                    "type": "text",
                    "content": document_config.get("title", "Document"),
                    "font": self.fonts["primary"],
                    "size": self.fonts["sizes"]["body"],
                    "color": self.colors["primary"]["navy"]["hex"],
                },
                "right": {"type": "page_number", "format": "Page {page} of {total}"},
            },
        }

        # Footer configuration
        branded_config["footer"] = {
            "height": 0.5,
            "content": {
                "left": {
                    "type": "text",
                    "content": self.company["copyright"],
                    "font": self.fonts["primary"],
                    "size": self.fonts["sizes"]["micro"],
                    "color": self.colors["neutrals"]["smoke"]["hex"],
                },
                "center": {"type": "date", "format": "%B %d, %Y"},
                "right": {"type": "text", "content": "Confidential"},
            },
        }

        # Text styles per brand_book guidance
        branded_config["styles"] = {
            "heading1": {
                "font": self.fonts["primary"],
                "size": self.fonts["sizes"]["h1"],
                "weight": self.fonts["weights"]["semibold"],
                "color": self.colors["primary"]["pacific"]["hex"],
                "spacing_after": 12,
            },
            "heading2": {
                "font": self.fonts["primary"],
                "size": self.fonts["sizes"]["h2"],
                "weight": self.fonts["weights"]["semibold"],
                "color": self.colors["primary"]["navy"]["hex"],
                "spacing_after": 10,
            },
            "heading3": {
                "font": self.fonts["primary"],
                "size": self.fonts["sizes"]["h3"],
                "weight": self.fonts["weights"]["semibold"],
                "color": self.colors["primary"]["navy"]["hex"],
                "spacing_after": 8,
            },
            "body": {
                "font": self.fonts["primary"],
                "size": self.fonts["sizes"]["body"],
                "weight": self.fonts["weights"]["regular"],
                "color": self.colors["primary"]["navy"]["hex"],
                "line_spacing": 1.15,
                "paragraph_spacing": 12,
            },
            "caption": {
                "font": self.fonts["primary"],
                "size": self.fonts["sizes"]["caption"],
                "weight": self.fonts["weights"]["medium"],
                "color": self.colors["neutrals"]["smoke"]["hex"],
            },
        }

        # Table formatting
        branded_config["table_style"] = {
            "header": {
                "background": self.colors["primary"]["pacific"]["hex"],
                "text_color": self.colors["neutrals"]["white"]["hex"],
                "bold": True,
            },
            "rows": {
                "alternating_color": self.colors["neutrals"]["pearl"]["hex"],
                "border_color": self.colors["neutrals"]["pearl"]["hex"],
                "text_color": self.colors["primary"]["navy"]["hex"],
            },
        }

        return branded_config

    def validate_colors(self, colors_used: List[str]) -> Dict[str, Any]:
        """
        Validate that colors match AD brand guidelines.

        Args:
            colors_used: List of color codes used in document

        Returns:
            Validation results with corrections if needed
        """
        results = {"valid": True, "corrections": [], "warnings": []}

        approved_colors = []
        for category in self.colors.values():
            for color in category.values():
                approved_colors.append(color["hex"].upper())

        for color in colors_used:
            color_upper = color.upper()
            if color_upper not in approved_colors:
                results["valid"] = False
                closest = self._find_closest_brand_color(color)
                results["corrections"].append(
                    {
                        "original": color,
                        "suggested": closest,
                        "message": f"Non-brand color {color} should be replaced with {closest}",
                    }
                )

        return results

    def _find_closest_brand_color(self, color: str) -> str:
        """Find the closest AD brand color to a given color."""
        # Simplified - in production would calculate color distance
        return self.colors["primary"]["pacific"]["hex"]

    def apply_watermark(self, document_type: str) -> Dict[str, Any]:
        """
        Generate watermark configuration for documents.

        Args:
            document_type: Type of document (draft, confidential, etc.)

        Returns:
            Watermark configuration
        """
        watermarks = {
            "draft": {
                "text": "DRAFT",
                "color": self.colors["neutrals"]["smoke"]["hex"],
                "opacity": 0.1,
                "angle": 45,
                "font_size": 72,
            },
            "confidential": {
                "text": "CONFIDENTIAL",
                "color": self.colors["semantic"]["error"]["hex"],
                "opacity": 0.1,
                "angle": 45,
                "font_size": 60,
            },
            "sample": {
                "text": "SAMPLE",
                "color": self.colors["semantic"]["warning"]["hex"],
                "opacity": 0.15,
                "angle": 45,
                "font_size": 72,
            },
        }

        return watermarks.get(document_type, watermarks["draft"])

    def get_chart_palette(self, num_series: int = 4) -> List[str]:
        """
        Get AD brand color palette for charts.

        Args:
            num_series: Number of data series

        Returns:
            List of hex color codes
        """
        palette = [
            self.colors["primary"]["pacific"]["hex"],
            self.colors["primary"]["seafoam"]["hex"],
            self.colors["secondary"]["ocean"]["hex"],
            self.colors["primary"]["navy"]["hex"],
            self.colors["secondary"]["arctic"]["hex"],
            self.colors["secondary"]["powder"]["hex"],
        ]

        return palette[:num_series]

    def format_number(self, value: float, format_type: str = "general") -> str:
        """
        Format numbers according to AD brand standards.

        Args:
            value: Numeric value to format
            format_type: Type of formatting (currency, percentage, general)

        Returns:
            Formatted string
        """
        if format_type == "currency":
            return f"${value:,.2f}"
        elif format_type == "percentage":
            return f"{value:.1f}%"
        elif format_type == "large_number":
            if value >= 1_000_000:
                return f"{value / 1_000_000:.1f}M"
            elif value >= 1_000:
                return f"{value / 1_000:.1f}K"
            else:
                return f"{value:.0f}"
        else:
            return f"{value:,.0f}" if value >= 1000 else f"{value:.2f}"


def apply_brand_to_document(document_type: str, config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Main function to apply AD branding to any document type.

    Args:
        document_type: Type of document ('excel', 'powerpoint', 'pdf')
        config: Document configuration

    Returns:
        Branded configuration
    """
    formatter = BrandFormatter()

    if document_type.lower() == "excel":
        return formatter.format_excel(config)
    elif document_type.lower() in ["powerpoint", "pptx"]:
        return formatter.format_powerpoint(config)
    elif document_type.lower() == "pdf":
        return formatter.format_pdf(config)
    else:
        raise ValueError(f"Unsupported document type: {document_type}")


# Example usage
if __name__ == "__main__":
    # Example Excel configuration
    excel_config = {"title": "Quarterly Report", "sheets": ["Summary", "Details"]}

    branded_excel = apply_brand_to_document("excel", excel_config)
    print("Branded Excel Configuration:")
    print(branded_excel)

    # Example PowerPoint configuration
    ppt_config = {"title": "Business Review", "num_slides": 10}

    branded_ppt = apply_brand_to_document("powerpoint", ppt_config)
    print("\nBranded PowerPoint Configuration:")
    print(branded_ppt)
