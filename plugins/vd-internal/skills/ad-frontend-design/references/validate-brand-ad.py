#!/usr/bin/env python3
"""
Brand Validation Script for Accelerate Data
Validates content against AD brand guidelines including colors, fonts, tone, and messaging.

All color and font values are sourced from the authoritative brand_book.
"""

import json
import re
from dataclasses import asdict, dataclass
from typing import Dict, List, Optional, Tuple


@dataclass
class BrandGuidelines:
    """Brand guidelines configuration"""

    brand_name: str
    primary_colors: List[str]
    secondary_colors: List[str]
    neutral_colors: List[str]
    fonts: List[str]
    tone_keywords: List[str]
    prohibited_words: List[str]
    tagline: Optional[str] = None
    logo_usage_rules: Optional[Dict] = None


@dataclass
class ValidationResult:
    """Result of brand validation"""

    passed: bool
    score: float
    violations: List[str]
    warnings: List[str]
    suggestions: List[str]


class BrandValidator:
    """Validates content against Accelerate Data brand guidelines"""

    def __init__(self, guidelines: BrandGuidelines):
        self.guidelines = guidelines

    def validate_colors(self, content: str) -> Tuple[List[str], List[str]]:
        """
        Validate color usage in content (hex codes, RGB, color names)
        Returns: (violations, warnings)
        """
        violations = []
        warnings = []

        # Find hex colors
        hex_pattern = r"#[0-9A-Fa-f]{6}|#[0-9A-Fa-f]{3}"
        found_colors = re.findall(hex_pattern, content)

        # Find RGB colors
        rgb_pattern = r"rgb\s*\(\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}\s*\)"
        found_colors.extend(re.findall(rgb_pattern, content, re.IGNORECASE))

        approved_colors = (
            self.guidelines.primary_colors
            + self.guidelines.secondary_colors
            + self.guidelines.neutral_colors
        )

        for color in found_colors:
            color_normalized = color.upper() if color.startswith("#") else color.lower()
            approved_normalized = [c.upper() for c in approved_colors]
            if color_normalized not in approved_normalized:
                violations.append(f"Unapproved color used: {color}")

        return violations, warnings

    def validate_fonts(self, content: str) -> Tuple[List[str], List[str]]:
        """
        Validate font usage in content
        Returns: (violations, warnings)
        """
        violations = []
        warnings = []

        # Common font specification patterns
        font_patterns = [
            r'font-family\s*:\s*["\']?([^;"\']+)["\']?',
            r"font:\s*[^;]*\s+([A-Za-z][A-Za-z\s]+)(?:,|;|\s+\d)",
        ]

        found_fonts = []
        for pattern in font_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            found_fonts.extend(matches)

        for font in found_fonts:
            font_clean = font.strip().lower()
            # Check if any approved font is in the found font string
            if not any(approved.lower() in font_clean for approved in self.guidelines.fonts):
                violations.append(f"Unapproved font used: {font}")

        return violations, warnings

    def validate_tone(self, content: str) -> Tuple[List[str], List[str]]:
        """
        Validate tone and messaging against AD brand personality
        Returns: (violations, warnings)
        """
        violations = []
        warnings = []

        # Check for prohibited words
        content_lower = content.lower()
        for word in self.guidelines.prohibited_words:
            if word.lower() in content_lower:
                violations.append(f"Prohibited word/phrase used: '{word}'")

        # Check for tone keywords (should have at least some for substantial content)
        tone_matches = sum(
            1 for keyword in self.guidelines.tone_keywords if keyword.lower() in content_lower
        )

        if tone_matches == 0 and len(content) > 100:
            warnings.append(
                f"Content may not align with AD brand tone. "
                f"Consider using terms like: {', '.join(self.guidelines.tone_keywords[:5])}"
            )

        return violations, warnings

    def validate_brand_name(self, content: str) -> Tuple[List[str], List[str]]:
        """
        Validate brand name usage and capitalization
        Returns: (violations, warnings)
        """
        violations = []
        warnings = []

        # Find all variations of the brand name
        brand_pattern = re.compile(re.escape(self.guidelines.brand_name), re.IGNORECASE)
        matches = brand_pattern.findall(content)

        for match in matches:
            if match != self.guidelines.brand_name:
                violations.append(
                    f"Incorrect brand name capitalization: '{match}' "
                    f"should be '{self.guidelines.brand_name}'"
                )

        return violations, warnings

    def calculate_score(self, violations: List[str], warnings: List[str]) -> float:
        """Calculate compliance score (0-100)"""
        violation_penalty = len(violations) * 10
        warning_penalty = len(warnings) * 3

        score = max(0, 100 - violation_penalty - warning_penalty)
        return round(score, 2)

    def generate_suggestions(self, violations: List[str], warnings: List[str]) -> List[str]:
        """Generate helpful suggestions based on violations and warnings"""
        suggestions = []

        if any("color" in v.lower() for v in violations):
            suggestions.append(
                f"Use approved AD colors: Primary: {', '.join(self.guidelines.primary_colors[:3])}"
            )

        if any("font" in v.lower() for v in violations):
            suggestions.append(f"Use approved fonts: {', '.join(self.guidelines.fonts[:3])}")

        if any("tone" in w.lower() for w in warnings):
            suggestions.append(
                f"Incorporate AD brand tone keywords: {', '.join(self.guidelines.tone_keywords[:5])}"
            )

        if any("brand name" in v.lower() for v in violations):
            suggestions.append(f"Always capitalize brand name as: {self.guidelines.brand_name}")

        return suggestions

    def validate(self, content: str) -> ValidationResult:
        """
        Perform complete brand validation
        Returns: ValidationResult
        """
        all_violations = []
        all_warnings = []

        # Run all validation checks
        color_v, color_w = self.validate_colors(content)
        all_violations.extend(color_v)
        all_warnings.extend(color_w)

        font_v, font_w = self.validate_fonts(content)
        all_violations.extend(font_v)
        all_warnings.extend(font_w)

        tone_v, tone_w = self.validate_tone(content)
        all_violations.extend(tone_v)
        all_warnings.extend(tone_w)

        brand_v, brand_w = self.validate_brand_name(content)
        all_violations.extend(brand_v)
        all_warnings.extend(brand_w)

        # Calculate score and generate suggestions
        score = self.calculate_score(all_violations, all_warnings)
        suggestions = self.generate_suggestions(all_violations, all_warnings)

        return ValidationResult(
            passed=len(all_violations) == 0,
            score=score,
            violations=all_violations,
            warnings=all_warnings,
            suggestions=suggestions,
        )


def load_guidelines_from_json(filepath: str) -> BrandGuidelines:
    """
    Load brand guidelines from JSON file

    Args:
        filepath: Path to JSON file containing brand guidelines

    Returns:
        BrandGuidelines object

    Raises:
        FileNotFoundError: If the file doesn't exist
        json.JSONDecodeError: If the file contains invalid JSON
        TypeError: If required fields are missing
    """
    try:
        with open(filepath) as f:
            data = json.load(f)
        return BrandGuidelines(**data)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Brand guidelines file not found: {filepath}") from e
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(
            f"Invalid JSON in brand guidelines file: {e.msg}", e.doc, e.pos
        ) from e
    except TypeError as e:
        raise TypeError(f"Missing required fields in brand guidelines: {e}") from e


def get_accelerate_data_guidelines() -> BrandGuidelines:
    """
    Get Accelerate Data brand guidelines.

    All values sourced from brand_book (AUTHORITATIVE SOURCE).

    Returns:
        BrandGuidelines object with Accelerate Data standards
    """
    return BrandGuidelines(
        brand_name="Accelerate Data",
        # Primary colors from brand_book Page 3
        primary_colors=[
            "#00b4d8",  # Pacific (DOMINANT)
            "#03045e",  # Navy (SUB-DOMINANT)
            "#00dd92",  # Seafoam (ACCENT)
        ],
        # Secondary colors from brand_book Page 2-3
        secondary_colors=[
            "#caf0f8",  # Powder
            "#90e0ef",  # Arctic
            "#0077b6",  # Ocean
        ],
        # Neutral colors from brand_book Page 3
        neutral_colors=[
            "#f2f2f2",  # Pearl
            "#171c21",  # Smoke
            "#ffffff",  # White
        ],
        # Fonts aligned with brand personality
        fonts=[
            "Geist",
            "SF Pro",
            "system-ui",
            "-apple-system",
            "sans-serif",
            "Geist Mono",
            "SF Mono",
            "Menlo",
            "monospace",
        ],
        # Tone keywords from brand_book Page 1 - brand personality
        tone_keywords=[
            "calm",
            "mastery",
            "precision",
            "data",
            "governance",
            "reliable",
            "expert",
            "rational",
            "systems",
            "authority",
            "quality",
            "integrity",
            "efficient",
            "clear",
            "exact",
        ],
        # Words that conflict with "calm mastery" brand personality
        prohibited_words=[
            "hype",
            "disrupt",
            "revolutionary",
            "game-changing",
            "groundbreaking",
            "explosive",
            "skyrocket",
            "unstoppable",
            "insane",
            "crazy",
            "wild",
        ],
        tagline="vibeData",
    )


def main():
    """Example usage demonstrating AD brand validation"""
    # Load Accelerate Data brand guidelines
    guidelines = get_accelerate_data_guidelines()

    # Example content to validate (intentionally contains violations for demonstration)
    test_content = """
    Welcome to accelerate data!

    We are a revolutionary solution provider with game-changing technology.

    Our calm mastery and precision in data governance are trusted by many enterprises.

    Contact us at: font-family: 'Comic Sans MS'
    Color scheme: #FF0000
    Background: rgb(255, 0, 0)
    """

    # Validate
    validator = BrandValidator(guidelines)
    result = validator.validate(test_content)

    # Print results
    print("=" * 60)
    print("ACCELERATE DATA BRAND VALIDATION REPORT")
    print("=" * 60)
    print(f"\nOverall Status: {'PASSED' if result.passed else 'FAILED'}")
    print(f"Compliance Score: {result.score}/100")

    if result.violations:
        print(f"\nVIOLATIONS ({len(result.violations)}):")
        for i, violation in enumerate(result.violations, 1):
            print(f"  {i}. {violation}")

    if result.warnings:
        print(f"\nWARNINGS ({len(result.warnings)}):")
        for i, warning in enumerate(result.warnings, 1):
            print(f"  {i}. {warning}")

    if result.suggestions:
        print("\nSUGGESTIONS:")
        for i, suggestion in enumerate(result.suggestions, 1):
            print(f"  {i}. {suggestion}")

    print("\n" + "=" * 60)

    # Return JSON for programmatic use
    return asdict(result)


if __name__ == "__main__":
    main()
