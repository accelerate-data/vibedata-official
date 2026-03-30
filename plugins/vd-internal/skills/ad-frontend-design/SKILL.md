---
name: ad-frontend-design
description: >
  Accelerate Data's unified front-end design system for vibeData. Enforces brand-compliant,
  premium UI across all surfaces - product, marketing, docs, and demos. Use when building
  any interface representing Accelerate Data brand, including vibeData Studio, marketing pages,
  documentation sites, demo applications, internal tools, or any UI for Accelerate Data.
tools: Read, Glob, Grep, Bash
type: domain
domain: Accelerate Data brand and frontend design
version: 1.0.0
---

# Accelerate Data Front End Design

This skill defines the visual language for all Accelerate Data interfaces. It synthesizes the brand book's authoritative guidelines with senior UI/UX principles to create a cohesive, premium design system. Apply these principles to every screen, component, and interaction.

## Brand Foundation

### Brand Personality
Accelerate Data embodies the **calm mastery and grounded authority of a senior data engineer**:

- **Precise, rational, deeply systems-minded** - every element has purpose
- **Quiet confidence** - steady, thoughtful, subtly futuristic
- **Clear and exact** - strips away ambiguity, simplifies complex structures
- **Governance over hype** - integrity and long-term reliability
- **The calm expert** you turn to when data must be done right

### Visual Expression
- Gravitate toward **dark neutrals, clean geometric lines, and subtle technical details**
- **Understated and intentional**: minimalist, premium, purely functional
- **Never logos or loud patterns** - restraint defines the aesthetic

## Implementation Workflow

Copy this checklist and track progress:

```
UI Implementation Progress:
- [ ] Step 1: Set up color tokens
- [ ] Step 2: Configure typography
- [ ] Step 3: Apply spacing system
- [ ] Step 4: Build components
- [ ] Step 5: Validate brand compliance
```

**Step 1: Set up color tokens**
Define CSS variables or framework config using colors from Color System section.

**Step 2: Configure typography**
Apply font stack and type scale. Verify Geist or SF Pro loads correctly.

**Step 3: Apply spacing system**
Use 4px grid tokens consistently. Check padding symmetry.

**Step 4: Build components**
Follow Component Patterns section. Use specified border radius and shadows.

**Step 5: Validate brand compliance**
Run through Brand Compliance Checklist below. If any item fails, return to relevant step.

## Color System

### Primary Colors
| Name | Hex | Role | Usage |
|------|-----|------|-------|
| Pacific | #00b4d8 | DOMINANT | Headers, backgrounds, CTAs, primary actions |
| Navy | #03045e | SUB-DOMINANT | Depth, stability, text, secondary elements |
| Seafoam | #00dd92 | ACCENT | Energy, creativity, highlights - use sparingly |

### Secondary Colors
| Name | Hex | Usage |
|------|-----|-------|
| Powder | #caf0f8 | Breakers, light backgrounds, subtle fills |
| Arctic | #90e0ef | Graphics, icons, decorative elements |
| Ocean | #0077b6 | Breakers, backgrounds, depth layers |

### Neutrals
| Name | Hex | Usage |
|------|-----|-------|
| Pearl | #f2f2f2 | Sub-headers, body copy, light mode backgrounds |
| Smoke | #171c21 | Body copy, dark mode base, primary dark surface |

### Semantic Colors (Brand-Tinted)
| State | Light Mode | Dark Mode | Notes |
|-------|------------|-----------|-------|
| Success | #00dd92 | #00c77f | Uses Seafoam for brand alignment |
| Warning | #f59e0b | #d97706 | Amber for universal recognition |
| Error | #ef4444 | #dc2626 | Red for immediate attention |
| Info | #00b4d8 | #0096b4 | Uses Pacific for brand alignment |

### Color Application Rules
1. **Pacific for technology/innovation** - primary CTAs, active states, links
2. **Navy for depth/stability/trust** - text, headers, grounding elements
3. **Seafoam ONLY for accent moments** - success states, highlights, never overuse
4. **Neutrals as backdrop** - let primary and secondary colors stand out
5. **Color for meaning only** - decorative color is noise
6. **Pick ONE accent color per context** - typically Pacific or Seafoam, not both

## Typography

### Font Stack
```
Primary: Geist, SF Pro, system-ui, -apple-system, sans-serif
Monospace: Geist Mono, SF Mono, Menlo, monospace
```

These fonts embody the brand's precise, rational, systems-minded personality with clean geometric lines.

### Type Scale
| Level | Size | Weight | Letter-spacing | Usage |
|-------|------|--------|----------------|-------|
| Display | 32px | 600 | -0.02em | Page titles, hero text |
| H1 | 24px | 600 | -0.02em | Section headers |
| H2 | 18px | 600 | -0.02em | Subsection headers |
| H3 | 16px | 600 | -0.015em | Component headers |
| Body | 14px | 400 | 0 | Primary content |
| Body Small | 13px | 400 | 0 | Secondary content |
| Caption | 12px | 500 | 0.01em | Labels, metadata |
| Micro | 11px | 500 | 0.02em | Badges, tiny labels |

### Typography Rules
- Headlines: 600 weight, tight letter-spacing (-0.02em)
- Body: 400-500 weight, standard tracking
- Labels: 500 weight, slight positive tracking for uppercase
- **Monospace for data values**: numbers, IDs, codes, timestamps
- Use `tabular-nums` for columnar number alignment
- **Never** use decorative or display fonts for UI text

## Spacing System

Based on 4px grid for precision and consistency.

| Token | Value | Usage |
|-------|-------|-------|
| space-1 | 4px | Micro spacing (icon gaps, tight inline) |
| space-2 | 8px | Tight spacing (within components) |
| space-3 | 12px | Standard spacing (between related elements) |
| space-4 | 16px | Comfortable spacing (section padding) |
| space-6 | 24px | Generous spacing (between sections) |
| space-8 | 32px | Major separation (page sections) |
| space-12 | 48px | Extra large (hero sections) |

### Spacing Rules
- **Symmetrical padding**: TLBR must match unless content creates natural visual balance
- **Consistent component spacing**: same elements = same spacing everywhere
- **Generous whitespace**: let the interface breathe

## Component Patterns

### Buttons
```
Primary:   bg: Pacific, text: white, radius: 6px, padding: 8px 16px
Secondary: bg: transparent, border: 1px Navy, text: Navy, radius: 6px
Ghost:     bg: transparent, text: Pacific, hover: Pacific/10% bg
Danger:    bg: Error red, text: white, radius: 6px
```
- Height: 32px (small), 40px (default), 48px (large)
- Font weight: 500
- No spring/bounce animations on hover or click

### Cards
```
Light mode: bg: white, border: 1px Pearl, radius: 8px, shadow: 0 1px 2px rgba(0,0,0,0.05)
Dark mode:  bg: Smoke lighter, border: 1px rgba(255,255,255,0.1), radius: 8px
```
- Padding: 16px or 24px depending on content density
- Avoid heavy drop shadows

### Input Fields
```
Default:  bg: white/Smoke, border: 1px neutral, radius: 6px, padding: 8px 12px
Focus:    border: Pacific, ring: 2px Pacific/20%
Error:    border: Error red, ring: 2px Error/20%
Disabled: opacity: 0.5, cursor: not-allowed
```
- Height: 40px default
- Labels: 500 weight, positioned above input
- Error messages: 12px, Error color, below input

### Navigation
- **Sidebar**: Fixed width (240-280px), dark mode preferred (Smoke base)
- **Top nav**: Height 56-64px, sticky positioning
- Active state: Pacific text or Pacific left border indicator
- Hover: Subtle background shift, never dramatic color change

## Quick Decision Guide

**Choosing a color:**
- Primary action/CTA -> Pacific (#00b4d8)
- Text/headers -> Navy (#03045e)
- Success/highlight accent -> Seafoam (#00dd92)
- Light background -> Pearl (#f2f2f2)
- Dark background -> Smoke (#171c21)
- Unsure? -> Default to Pacific for interactive, Navy for text

**Choosing a button variant:**
- Main action on page -> Primary (Pacific bg)
- Secondary action -> Secondary (Navy border)
- Tertiary/cancel -> Ghost (Pacific text)
- Destructive action -> Danger (Error red bg)

**Choosing logo variant:**
- On Smoke/Navy/dark surface -> Use `light` variant from CDN manifest
- On Pearl/white/light surface -> Use `dark` variant from CDN manifest
- Favicon or small space -> `icon-*` assets
- Full branding -> `logo-*-h{size}` wordmark assets
- Icon + wordmark combo -> `logo-icon-lockup-*` assets

**Light mode vs Dark mode:**
- Product interfaces -> Support both, default to user preference
- Marketing pages -> Light mode preferred
- Developer tools -> Dark mode preferred

## Depth & Elevation

**Approach**: Minimal subtle shadows - borders preferred over heavy shadows.

| Level | Usage | Light Mode | Dark Mode |
|-------|-------|------------|-----------|
| Flat | Default surfaces | No shadow | Border only |
| Raised | Cards, dropdowns | 0 1px 2px rgba(0,0,0,0.05) | 1px border |
| Floating | Modals, popovers | 0 4px 12px rgba(0,0,0,0.1) | 1px border + subtle glow |

### Elevation Rules
- Choose ONE approach and apply consistently
- Dark mode: borders over shadows (shadows less visible on dark backgrounds)
- The craft is in the choice, not the complexity

## Border Radius System

Sharp, technical approach aligned with brand personality.

| Token | Value | Usage |
|-------|-------|-------|
| radius-sm | 4px | Badges, small buttons, tags |
| radius-md | 6px | Buttons, inputs, small cards |
| radius-lg | 8px | Cards, modals, larger containers |
| radius-xl | 12px | Hero cards, feature sections (use sparingly) |

**Never**: Large border radius (16px+) on small elements - feels juvenile, not technical.

## Motion & Animation

### Timing
| Type | Duration | Usage |
|------|----------|-------|
| Micro | 150ms | Button states, toggles, icon changes |
| Standard | 200ms | Dropdowns, tooltips, small reveals |
| Emphasis | 250ms | Modals, page transitions, larger movements |

### Easing
```
Default: cubic-bezier(0.25, 1, 0.5, 1)
Enter:   cubic-bezier(0, 0, 0.2, 1)
Exit:    cubic-bezier(0.4, 0, 1, 1)
```

### Motion Rules
- **No spring/bouncy effects** - enterprise UI requires steady, controlled motion
- **Purposeful transitions** - every animation should communicate state change
- **Subtle over dramatic** - motion supports, never distracts
- Hover states: opacity or background shifts, not transform animations

## Dark Mode

Both light and dark modes are fully supported. Dark mode uses Smoke (#171c21) as the base.

### Dark Mode Surfaces
| Layer | Color | Usage |
|-------|-------|-------|
| Base | #171c21 (Smoke) | Page background |
| Surface | #1e2329 | Cards, panels |
| Elevated | #262c33 | Dropdowns, modals |

### Dark Mode Adjustments
- Use borders over shadows
- Reduce semantic color saturation slightly
- Maintain same contrast hierarchy: primary > secondary > muted > faint
- Pacific and Seafoam remain vibrant as accents

## Logo Usage

### Asset Source
All logo assets are served from the Accelerate Data CDN. The full manifest with every asset, size, format, and direct URL is in [references/logo-assets.md](references/logo-assets.md).

**CDN base URL**: `http://assets.acceleratedata.ai/logo/`

> **Important**: Always look up the exact URL from the manifest. Do not construct URLs by pattern interpolation.

### Asset Types
| Type | Description | Example asset_id |
|------|-------------|-----------------|
| icon | Logomark only (scalable SVG or sized PNG) | `icon-light-svg`, `icon-dark-64` |
| logo | Full wordmark, height-sized | `logo-dark-h32`, `logo-light-h48` |
| logo+icon | Lockup (icon + wordmark combined) | `logo-icon-lockup-dark-96` |

### Color Variants
- `dark` (dark-colored artwork) -> use on **light** backgrounds (Pearl, white)
- `light` (light-colored artwork) -> use on **dark** backgrounds (Navy, Smoke)

> **Note**: The dark/light label describes the **logo color**, not the background. A dark logo is visible on light surfaces; a light logo is visible on dark surfaces.

### Common Logo Choices
| Context | Recommended asset |
|---------|------------------|
| Top nav (light bg, 32px height) | `logo-dark-h32` |
| Top nav (dark bg, 32px height) | `logo-light-h32` |
| Sidebar icon (dark bg, 24px) | `icon-light-24` (PNG) or `icon-light-svg` |
| Favicon | `favicon-light-ico` (dark bg) or `favicon-dark-ico` (light bg) |
| Hero/marketing (large) | `logo-dark-h96` or `logo-light-h96` |
| App icon / PWA | `pwa-icon-192`, `pwa-icon-512` |

### Naming Patterns
```
Icons:    icon-{dark|light}.svg (vector) or icon-{dark|light}-{size}.png (raster)
Wordmarks: logo-{dark|light}-h{size}.svg (sized by height) — ONLY wordmarks use "h" prefix
Lockups:  logo-icon-lockup-{dark|light}-{size}.svg (sized by bounding box, min 48px) — no "h" prefix
Favicons: see manifest for exact paths (mixed naming)
```

### Logo Rules
- Minimum clear space: 1x the height of the logomark
- **Never** stretch, rotate, or recolor the logo
- Use `light` variant (light-colored logos) on dark backgrounds (Navy, Smoke)
- Use `dark` variant (dark-colored logos) on light backgrounds (Pearl, white)
- For retina displays, use `@2x` PNG variants where available

## Layout Approach

Structured, content-driven layouts that simplify complex structures.

### Layout Patterns
- **Dense grids**: For data-heavy interfaces (dashboards, tables)
- **Generous spacing**: For marketing and documentation
- **Sidebar navigation**: Primary navigation pattern for products
- **Top navigation**: Secondary pattern for simpler sites
- **Split panels**: For detail views and editing interfaces

### Responsive Behavior Tiers
| Tier | Behavior |
|------|----------|
| Compact | Single column, collapsed navigation, stacked components |
| Standard | Sidebar visible, two-column layouts, full navigation |
| Expanded | Three+ columns, side-by-side panels, maximum density |

Implementation chooses breakpoint values; the skill specifies behavior.

### Layout Rules
- Layout driven by content, not decoration
- Clean geometric lines - no diagonal flow or asymmetry
- Predictable patterns - users should never be surprised by navigation

## Icons

Use **Phosphor Icons** (`@phosphor-icons/react`).

### Icon Rules
- Icons clarify, not decorate
- If removing an icon loses no meaning, remove it
- Consistent weight throughout interface (regular or light)
- Size: 16px inline, 20px standalone, 24px navigation

## Component Examples

See [component-examples.md](references/component-examples.md) for complete input/output examples including:
- Primary button with hover state
- Light mode card
- Input field with error state
- Dark mode card
- Sidebar navigation with active state

## Anti-Patterns

### Never Do
- Generic system fonts without brand consideration
- Purple gradients on white backgrounds (AI slop aesthetic)
- Dramatic drop shadows
- Colors outside the AD palette
- Spring/bouncy animations
- Decorative elements with no purpose
- Loud patterns or textures
- Asymmetric or experimental layouts
- Large border radius on small elements

### Always Question
- Is this on-brand for Accelerate Data?
- Does this feel "calm mastery" or chaotic?
- Would a senior data engineer trust this interface?
- Does every element serve a purpose?

## Brand Compliance Checklist

Before finalizing any UI, verify:

```
Brand Compliance:
- [ ] All colors are from the AD palette (no off-brand colors)
- [ ] Primary CTAs use Pacific (#00b4d8)
- [ ] Text uses Navy (#03045e) or appropriate neutral
- [ ] Seafoam (#00dd92) used sparingly for accents only
- [ ] Typography uses Geist/SF Pro stack
- [ ] Headlines are 600 weight with tight letter-spacing
- [ ] Spacing follows 4px grid
- [ ] Border radius is 6px (buttons/inputs) or 8px (cards)
- [ ] No spring/bounce animations
- [ ] No dramatic drop shadows
- [ ] Logo uses correct variant for background color
- [ ] Overall feel is "calm mastery" not chaotic
```

If any item fails, return to the relevant section and correct before proceeding.

## Implementation Notes

This skill is **framework-agnostic**. Apply these principles whether using:
- React + Tailwind
- Vue + CSS
- Svelte
- Plain HTML/CSS
- Any other stack

The design system defines the **what** - your framework implements the **how**.

### Optional Tailwind Configuration
```js
colors: {
  pacific: '#00b4d8',
  navy: '#03045e',
  seafoam: '#00dd92',
  powder: '#caf0f8',
  arctic: '#90e0ef',
  ocean: '#0077b6',
  pearl: '#f2f2f2',
  smoke: '#171c21',
}
```

## Quick Reference

### Core Brand Values
- Calm mastery, grounded authority
- Minimalist, premium, purely functional
- Dark neutrals, clean geometric lines, subtle technical details
- Never logos or loud patterns

### Color Quick Pick
| Purpose | Color | Hex |
|---------|-------|-----|
| Primary action | Pacific | #00b4d8 |
| Text/depth | Navy | #03045e |
| Accent/highlight | Seafoam | #00dd92 |
| Light background | Pearl | #f2f2f2 |
| Dark background | Smoke | #171c21 |

### Component Defaults
| Property | Value |
|----------|-------|
| Border radius | 6px (standard), 8px (cards) |
| Transition | 150-200ms, cubic-bezier(0.25, 1, 0.5, 1) |
| Button height | 40px |
| Input height | 40px |
| Spacing unit | 4px |
