---
name: Warm Human Health
colors:
  surface: '#fff8f5'
  surface-dim: '#dfd9d6'
  surface-bright: '#fff8f5'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f9f2ef'
  surface-container: '#f3ede9'
  surface-container-high: '#ede7e4'
  surface-container-highest: '#e8e1de'
  on-surface: '#1d1b19'
  on-surface-variant: '#53433f'
  inverse-surface: '#33302e'
  inverse-on-surface: '#f6efec'
  outline: '#86736e'
  outline-variant: '#d8c2bc'
  surface-tint: '#8d4d3b'
  primary: '#8d4d3b'
  on-primary: '#ffffff'
  primary-container: '#f4a38c'
  on-primary-container: '#713726'
  inverse-primary: '#ffb5a0'
  secondary: '#406749'
  on-secondary: '#ffffff'
  secondary-container: '#bfeac5'
  on-secondary-container: '#446b4d'
  tertiary: '#815508'
  on-tertiary: '#ffffff'
  tertiary-container: '#e5ad5c'
  on-tertiary-container: '#644100'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#ffdbd1'
  primary-fixed-dim: '#ffb5a0'
  on-primary-fixed: '#380c02'
  on-primary-fixed-variant: '#703625'
  secondary-fixed: '#c1edc8'
  secondary-fixed-dim: '#a6d1ad'
  on-secondary-fixed: '#00210c'
  on-secondary-fixed-variant: '#284f33'
  tertiary-fixed: '#ffddb3'
  tertiary-fixed-dim: '#f6bc6a'
  on-tertiary-fixed: '#291800'
  on-tertiary-fixed-variant: '#633f00'
  background: '#fff8f5'
  on-background: '#1d1b19'
  surface-variant: '#e8e1de'
typography:
  display:
    fontFamily: Plus Jakarta Sans
    fontSize: 40px
    fontWeight: '700'
    lineHeight: 48px
    letterSpacing: -0.02em
  display-mobile:
    fontFamily: Plus Jakarta Sans
    fontSize: 32px
    fontWeight: '700'
    lineHeight: 40px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 30px
    fontWeight: '700'
    lineHeight: 38px
    letterSpacing: -0.015em
  headline-lg-mobile:
    fontFamily: Plus Jakarta Sans
    fontSize: 26px
    fontWeight: '700'
    lineHeight: 34px
    letterSpacing: -0.015em
  headline-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 22px
    fontWeight: '600'
    lineHeight: 30px
    letterSpacing: -0.01em
  headline-sm:
    fontFamily: Plus Jakarta Sans
    fontSize: 18px
    fontWeight: '600'
    lineHeight: 26px
  body-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 17px
    fontWeight: '400'
    lineHeight: 26px
  body-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 15px
    fontWeight: '400'
    lineHeight: 23px
  body-sm:
    fontFamily: Plus Jakarta Sans
    fontSize: 13px
    fontWeight: '500'
    lineHeight: 19px
  label-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 16px
    fontWeight: '600'
    lineHeight: 22px
  label-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 14px
    fontWeight: '600'
    lineHeight: 20px
  label-sm:
    fontFamily: Plus Jakarta Sans
    fontSize: 12px
    fontWeight: '700'
    lineHeight: 16px
    letterSpacing: 0.02em
rounded:
  sm: 0.5rem
  DEFAULT: 1rem
  md: 1.5rem
  lg: 2rem
  xl: 3rem
  full: 9999px
spacing:
  gutter: 1rem
  gutter-tablet: 1.5rem
  margin: 1.25rem
  margin-tablet: 2rem
  space-xs: 0.375rem
  space-sm: 0.75rem
  space-md: 1.25rem
  space-lg: 1.75rem
  space-xl: 2.5rem
---

## Brand & Style

This design system is tailored for an approachable, supportive, and stress-reducing health screening experience. Rather than clinical detachment or sterile medical tropes, it balances the warmth of holistic wellness with the clarity of clinical utility.

### Emotional Foundation
- **Reassuring & Calm:** Mitigates health-related anxiety through soothing, tactile elements and gentle color transitions.
- **Human & Empathetic:** Speaks with clarity, warmth, and supportive validation at every step of testing or screening.
- **Trustworthy & Capable:** Delivers medical data, screening results, and diagnostic guidance with unambiguous legibility and accessible structures.

### Aesthetic Direction: Tactile Organic Warmth
The aesthetic combines soft-touch surfaces, generous breathing room, organic contours, and welcoming typography. Interfaces lean into subtle surface elevation, warm paper-like substrates, and comforting feedback loops rather than clinical grids and harsh lines.

## Colors

The palette grounds the interface in comforting, non-threatening tones while maintaining strict WCAG 2.1 AA/AAA contrast ratios for health data readability.

### Roles & Semantic Application
- **Primary (`#F4A38C` — Soft Coral/Peach):** Core actions, onboarding accents, focal cards, key interactive triggers, and welcoming celebratory milestones.
- **Secondary (`#8FB996` — Sage Green):** Restorative, normal, completed, and healthy screening indicators. Conveys progress, positive results, and calm confirmations without the clinical intensity of neon green.
- **Tertiary (`#F2B866` — Warm Amber):** Non-alarmist attention states, upcoming appointments, reminders, and monitoring indicators. Guides attention gently without inducing panic.
- **Neutral Surface Canvas (`#FFF9F3` — Warm Off-White):** Default base background layer. Replaces sterile cool white with a parchment-like, restorative surface.
- **Neutral Dark Typography (`#3D3A38` — Dark Warm Gray):** Primary typographic tone and high-contrast structural borders, ensuring deep readability with soft, warm undertones.

## Typography

Typographic hierarchy relies on **Plus Jakarta Sans**, offering a balance of geometric openness, rounded geometry, and legibility across all medical screening context states.

- **Headlines:** Use deliberate weight (600–700) and compact negative tracking to feel grounded, confident, and conversational rather than cold.
- **Body:** Kept generous in leading (1.5x ratio minimum) to avoid cognitive fatigue when reading medical preparation steps or diagnostic explanations.
- **Labels & Interactive States:** Retain medium-to-bold weights to clearly communicate button triggers, test steps, status badges, and input prompts.

## Layout & Spacing

The layout model emphasizes airy, non-cramped compositions to support stress-free interactions.

### Layout Mechanics
- **Mobile First (4-column fluid):** 20px (`1.25rem`) screen margins with 16px (`1rem`) gutters between structural columns. Single-column stacks are preferred for test questionnaires and result cards.
- **Tablet / Large Handheld (8-column fluid):** 32px (`2rem`) margins with 24px (`1.5rem`) gutters, allowing side-by-side arrangement of screening metrics and visual summaries.
- **Touch Ergonomics:** All primary interactive elements maintain a vertical height and tap footprint of at least 56px to guarantee effortless physical usability during mobile hand-held operation.

## Elevation & Depth

Visual hierarchy uses warm, ambient, diffused drop shadows with subtle tinting derived from the neutral dark tone. Rather than cold gray drop shadows, layers float gently above the off-white canvas.

### Surface Elevation Levels
- **Canvas Base (`#FFF9F3`):** Flat foundation for main screen containers.
- **Layer 1 — Resting Cards & Inputs:**
  - Background: `#FFFFFF`
  - Shadow: `0px 4px 16px -2px rgba(61, 58, 56, 0.05), 0px 2px 6px -1px rgba(61, 58, 56, 0.03)`
- **Layer 2 — Active Cards, Floating Bars & Action Sheets:**
  - Background: `#FFFFFF`
  - Shadow: `0px 10px 28px -4px rgba(61, 58, 56, 0.08), 0px 4px 12px -2px rgba(61, 58, 56, 0.04)`
- **Layer 3 — Modals & Urgent Overlays:**
  - Background: `#FFFFFF`
  - Shadow: `0px 20px 40px -8px rgba(61, 58, 56, 0.12), 0px 8px 16px -4px rgba(61, 58, 56, 0.06)`
- **Accent Glow (Focus & Completion):**
  - Sage/Peach Accents: `0px 6px 20px 0px rgba(244, 163, 140, 0.35)` or `0px 6px 20px 0px rgba(143, 185, 150, 0.35)`

## Shapes

The shape system centers around high roundedness to promote safety, warmth, and organic comfort. 

- **Primary Cards & Containers:** Standardized with an extra-large corner radius (20px to 28px), removing sharp, intimidating corners.
- **Buttons & Interactive Tags:** Default to fully rounded, pill-shaped profiles or 24px radii for quick tactile recognition.
- **Modal Sheets:** Rounded on top edges with a 28px continuous corner radius for smooth presentation sheets.

## Components

### Buttons
- **Primary CTA:** Minimum height of 56px, fully rounded pill shape (`rounded-full`), background `#F4A38C`, text `#3D3A38` (semi-bold 16px), elevated with Layer 1 shadow. On press, scales slightly to 98% with an intensified peach ambient glow.
- **Secondary Action:** Minimum height of 56px, background `#FFFFFF`, border `1.5px solid rgba(61, 58, 56, 0.12)`, text `#3D3A38`.
- **Ghost/Tertiary:** Minimum height of 56px, transparent background, text `#3D3A38`, underline or subtle surface tint on press.

### Screening Cards
- **Base Card:** Crisp white surface (`#FFFFFF`) sitting on `#FFF9F3`, 24px corner radius, internal padding of 24px (`space-lg`), Layer 1 ambient shadow.
- **Status Indicator Card:** Includes a soft tinted banner or border indicator:
  - *Healthy/Normal:* Tinted `#8FB996` with 12% alpha surface and solid green accent pill.
  - *Needs Attention:* Tinted `#F2B866` with 15% alpha surface and warm amber badge.

### Form Inputs & Fields
- **Container:** Minimum height 56px, background `#FFFFFF`, border `1.5px solid rgba(61, 58, 56, 0.15)`, radius 20px, horizontal padding 20px.
- **Active / Focused:** Border turns to 2px solid `#F4A38C` with an ambient glow (`rgba(244, 163, 140, 0.25)`).
- **Labeling:** Floating or placed directly above input using `label-md` with `#3D3A38` at 85% opacity.

### Chips & Health Metric Badges
- **Status Badges:** Height 36px, radius 18px (pill), horizontal padding 14px.
  - *Normal:* `#8FB996` background with dark gray `#263628` text.
  - *Follow-up:* `#F2B866` background with dark warm `#3D3A38` text.
  - *Info/Neutral:* `#FFF9F3` surface with `1px solid rgba(61, 58, 56, 0.15)`.

### Selection Controls (Checkboxes & Radios)
- **Radio Buttons / Checkboxes:** Sized at 28px × 28px nested within a generous 56px touch tile container.
- **Selected State:** Border and fill transition to `#F4A38C` or `#8FB996` with a white checkmark or center circle.
- **Touch Target:** The entire surrounding list-item row (min height 64px, 20px radius) serves as the hit-area with active background feedback.

### Progress & Screening Steppers
- **Track:** 8px thickness, background `rgba(61, 58, 56, 0.08)`, radius 4px.
- **Indicator Fill:** Solid `#8FB996` or `#F4A38C` with rounded end caps and gentle animated progress transitions.