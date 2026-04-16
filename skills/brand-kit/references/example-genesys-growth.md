# Genesys Growth Design System

> Extracted from: https://genesysgrowth.com/
> Date: December 26, 2025
> Platform: Framer

---

## Visual description

> **For vibe coding and AI-assisted design reproduction.** Use this section to prompt AI tools to recreate this design aesthetic.

### Mood & atmosphere

Dark, confident, and premium. The design exudes the energy of a late-night strategy session in a high-end co-working space — focused, ambitious, and subtly luxurious. There's a sense of controlled intensity: professional enough for Series A founders, but with enough edge to feel like you're working with someone who actually ships, not just advises. The darkness isn't cold or intimidating — it's the comfortable darkness of a cinema before the main feature, promising something compelling is about to happen.

### Visual metaphors

This design feels like **a premium cinema lobby at midnight** — dark velvet backgrounds with strategic spotlights picking out what matters. There are echoes of **a high-end developer tool's marketing site** (think Linear, Raycast, or Vercel) but warmer and more human. It's **the visual equivalent of a founder who wears a quality black t-shirt instead of a suit** — clearly competent, deliberately understated, quietly expensive. The purple gradient rays evoke **light leaks from a neon sign glimpsed through rain** — atmospheric, slightly mysterious, unmistakably modern.

### Color story

Deep navy-black (#0a0a0f) anchors everything, creating a stage for content to perform. The background isn't pure black — it has enough blue undertone to feel digital and alive rather than void-like. Purple and indigo accents (#6366f1, #8b5cf6) appear strategically: gradient rays behind the hero create atmospheric depth without demanding attention, while CTAs use these colors at full saturation to create unmissable action points. White text (#ffffff) creates stark, confident contrast for headlines. Secondary text uses zinc grays (#a1a1aa) that recede appropriately without disappearing. The color hierarchy is ruthlessly clear: dark backgrounds create calm, white creates importance, purple creates action.

### Typography personality

Sharp, geometric, and contemporary. Inter (or similar geometric sans-serif) carries everything with quiet confidence. Headlines use tighter tracking (-0.025em to -0.05em) creating density and visual weight that commands attention. The typography doesn't try to be friendly — it's direct, efficient, and slightly compressed, like a founder who values your time. Body copy breathes more, with comfortable line heights (1.5-1.6) that make longer passages scannable. Numbers and stats use heavier weights, making metrics pop. The overall effect is "senior operator who communicates precisely" — every word earns its place.

### Spatial rhythm

Generous but purposeful. Hero sections command full viewport attention with abundant breathing room. Content sections use consistent vertical rhythm with 64-96px between major blocks. Cards and components sit in comfortable grids with 24-32px gaps — close enough to feel related, far enough to be distinct. The page doesn't feel sparse or dense — it feels *curated*, like a carefully arranged portfolio where nothing is accidental. Horizontal scrolling logo bars and service tabs break the vertical flow, creating visual interest and implying breadth of work.

### Signature elements

1. **Gradient rays**: Soft purple/indigo gradients emanate from behind the hero text like light sources, creating atmospheric depth. These aren't hard geometric shapes — they're soft, diffused, almost ethereal.

2. **Logo marquee**: Client logos scroll horizontally in a continuous band, grayscale by default, creating a subtle proof bar that moves and lives.

3. **Tab-based service navigation**: Services (Positioning Sprint, Website Expansion, etc.) use a contained tab switcher with a dark pill-shaped background, making complex offerings feel organized and approachable.

4. **Metric callouts**: Large numbers (45+, $3M+, 2 weeks) appear in bold white with descriptive text beneath, turning statistics into visual anchors.

5. **Testimonial cards with avatars**: Circular profile photos with subtle borders, paired with company logos and pull quotes, creating human credibility moments.

6. **AI chatbot links in footer**: Unique element where visitors can click to ask AI assistants about the brand — reinforcing the "AI-enabled operator" positioning.

### Texture & depth

Layered but subtle. The base layer is near-black, creating depth. Cards float slightly above on a marginally lighter surface (#111118) with whisper-thin borders (#27272a) that catch just enough light to define edges. Shadows are present but restrained — dark theme shadows use high opacity blacks rather than the gray blurs common in light themes. The gradient rays add a sense of atmospheric perspective, like looking through slightly hazy air. There's no noise texture or grain — surfaces are clean and digital. Occasional glow effects around accent elements (button hover states, active tabs) add a subtle luminosity that makes interactive elements feel alive.

### Motion philosophy

Subtle and professional with moments of delight. Transitions are quick (150-200ms) with gentle easing — nothing bounces or overshoots. Hover states lift cards slightly (translateY -2px) and deepen shadows, creating a tactile "I can click this" response. The logo marquee creates continuous ambient motion without demanding attention. Tab switches feel instant. Navigation appears with minimal fanfare. The motion philosophy says "I respect your time" while still feeling polished and intentional. Nothing is static that should be interactive, but nothing moves that doesn't need to.

### Component character

**Buttons** feel decisive and pressable. Primary buttons use gradient fills that shift on hover, with subtle glow effects suggesting energy. They're sized generously (12px 24px padding) with rounded-lg corners — confident without being aggressive.

**Cards** feel like they're floating on a dark surface. Thin borders catch ambient light. Hover states create gentle lift. Content is well-padded (24-32px) giving text room to breathe. Cards group naturally — client logos, testimonials, service details — each type with its own subtle variation.

**Navigation** is minimal and assured. Links are subtle (zinc gray) until hovered (white). The logo stands alone. CTAs are clearly separated. Sticky header uses subtle backdrop blur, maintaining context without obscuring content.

**Testimonials** feel human and credible. Circular avatars, company logos, and pull quotes work together. The design makes social proof feel genuine rather than manufactured.

### Prompt for reproduction

> **Copy this prompt to recreate the design:**
>
> "Create a dark-themed B2B SaaS website with a premium, confident aesthetic. Use a near-black background (#0a0a0f) with subtle blue undertones. Add atmospheric depth with soft purple/indigo gradient rays emanating behind the hero section — these should feel like diffused light sources, not hard shapes. Use white (#ffffff) for headlines and primary text, zinc gray (#a1a1aa) for secondary text. Primary CTAs use a purple-to-indigo gradient (#6366f1 to #8b5cf6) with subtle glow on hover. Typography is geometric sans-serif (Inter or similar) with tight tracking on headlines. Cards float on slightly lighter surfaces (#111118) with thin zinc borders (#27272a) and subtle shadow elevation. Include a horizontally scrolling logo marquee for social proof, tab-based navigation for service offerings, and large metric callouts (bold numbers with descriptive text). Motion is subtle and professional — 200ms transitions, gentle hover lifts, no bouncing. The overall feeling should be 'senior operator who ships' — confident, precise, slightly luxurious but never flashy. Think Linear meets a high-end consulting firm, designed for Series A founders who value substance."

---

## Brand overview

- **Aesthetic direction**: Dark premium, operator-focused, confident minimalism
- **Industry context**: B2B SaaS consulting, product marketing, GTM strategy
- **Design framework detected**: Framer (custom implementation)
- **Confidence level**: 3/5 (Framer injects styles dynamically, values approximated from visual analysis)

---

## Typography

### Font families

3/5 Confidence: Medium (inferred from common Framer patterns)

```css
:root {
  /* Primary - Headlines and display text */
  --font-primary: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  
  /* Secondary - Body copy (same family, different weights) */
  --font-secondary: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  
  /* Mono - Code, technical content */
  --font-mono: 'SF Mono', 'Fira Code', 'Consolas', monospace;
}
```

**Font sources**: Inter via Google Fonts or system fonts

### Font scale

| Token | Size | Line Height | Usage | Confidence |
|-------|------|-------------|-------|------------|
| `--text-xs` | 12px / 0.75rem | 1.5 | Labels, captions, metadata | 3/5 |
| `--text-sm` | 14px / 0.875rem | 1.5 | Secondary text, navigation | 3/5 |
| `--text-base` | 16px / 1rem | 1.6 | Body copy | 3/5 |
| `--text-lg` | 18px / 1.125rem | 1.5 | Lead paragraphs | 3/5 |
| `--text-xl` | 20px / 1.25rem | 1.4 | Section subheadings | 3/5 |
| `--text-2xl` | 24px / 1.5rem | 1.3 | H4, card titles | 3/5 |
| `--text-3xl` | 30px / 1.875rem | 1.2 | H3 | 3/5 |
| `--text-4xl` | 36px / 2.25rem | 1.15 | H2 | 3/5 |
| `--text-5xl` | 48px / 3rem | 1.1 | H1, hero subheadlines | 3/5 |
| `--text-6xl` | 60px / 3.75rem | 1.05 | Hero headlines | 3/5 |
| `--text-7xl` | 72px / 4.5rem | 1.0 | Display, large hero text | 3/5 |

### Font weights

```css
:root {
  --font-normal: 400;
  --font-medium: 500;
  --font-semibold: 600;
  --font-bold: 700;
  --font-extrabold: 800;
}
```

### Letter spacing

```css
:root {
  --tracking-tighter: -0.05em;  /* Large headlines */
  --tracking-tight: -0.025em;   /* Subheadlines */
  --tracking-normal: 0;         /* Body text */
  --tracking-wide: 0.025em;     /* Labels, buttons */
  --tracking-wider: 0.05em;     /* Uppercase text */
}
```

---

## Colors

### Brand palette

3/5 Confidence: Medium (inferred from visual analysis)

```css
:root {
  /* Primary - Deep navy/dark blue-black */
  --primary: #0a0a0f;
  --primary-foreground: #ffffff;
  
  /* Secondary - Elevated dark surface */
  --secondary: #1a1a24;
  --secondary-foreground: #e5e5e5;
  
  /* Accent - Vibrant indigo */
  --accent: #6366f1;
  --accent-foreground: #ffffff;
  
  /* Brand - Purple highlight */
  --brand: #8b5cf6;
  --brand-foreground: #ffffff;
}
```

### Semantic colors

3/5 Confidence: Medium

```css
:root {
  /* Success */
  --success: #22c55e;
  --success-foreground: #ffffff;
  
  /* Warning */
  --warning: #f59e0b;
  --warning-foreground: #000000;
  
  /* Error / Destructive */
  --error: #ef4444;
  --error-foreground: #ffffff;
  
  /* Info */
  --info: #3b82f6;
  --info-foreground: #ffffff;
}
```

### Neutral palette

3/5 Confidence: Medium

```css
:root {
  /* Backgrounds */
  --background: #0a0a0f;
  --background-secondary: #111118;
  --background-tertiary: #1a1a24;
  
  /* Foregrounds */
  --foreground: #ffffff;
  --foreground-secondary: #a1a1aa;
  --foreground-muted: #71717a;
  
  /* Muted */
  --muted: #27272a;
  --muted-foreground: #a1a1aa;
  
  /* Cards */
  --card: #111118;
  --card-foreground: #ffffff;
  --card-hover: #1a1a24;
  
  /* Popovers */
  --popover: #18181b;
  --popover-foreground: #ffffff;
  
  /* Borders */
  --border: #27272a;
  --border-hover: #3f3f46;
  --border-focus: #6366f1;
  
  /* Inputs */
  --input: #27272a;
  --input-focus: #3f3f46;
  
  /* Ring (focus states) */
  --ring: #6366f1;
  --ring-offset: #0a0a0f;
}
```

### Gradients

3/5 Confidence: Medium

```css
:root {
  /* Hero background gradient rays */
  --gradient-ray-1: linear-gradient(135deg, rgba(139, 92, 246, 0.3) 0%, transparent 50%);
  --gradient-ray-2: linear-gradient(225deg, rgba(99, 102, 241, 0.2) 0%, transparent 50%);
  --gradient-ray-3: linear-gradient(315deg, rgba(168, 85, 247, 0.15) 0%, transparent 50%);
  
  /* Button gradients */
  --gradient-primary: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
  --gradient-primary-hover: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
  
  /* Card accent gradients */
  --gradient-card-glow: radial-gradient(circle at 50% 0%, rgba(139, 92, 246, 0.15) 0%, transparent 50%);
}
```

### Chart colors

```css
:root {
  --chart-1: #6366f1;  /* Indigo */
  --chart-2: #8b5cf6;  /* Purple */
  --chart-3: #a855f7;  /* Violet */
  --chart-4: #22c55e;  /* Green */
  --chart-5: #3b82f6;  /* Blue */
  --chart-6: #f59e0b;  /* Amber */
}
```

---

## Effects

### Border radius

3/5 Confidence: Medium

```css
:root {
  --radius-none: 0;
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --radius-xl: 16px;
  --radius-2xl: 24px;
  --radius-3xl: 32px;
  --radius-full: 9999px;
}
```

### Shadows

3/5 Confidence: Medium

```css
:root {
  /* Subtle shadows for dark theme */
  --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.3);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.4), 0 2px 4px -2px rgba(0, 0, 0, 0.3);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.5), 0 4px 6px -4px rgba(0, 0, 0, 0.4);
  --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.5), 0 8px 10px -6px rgba(0, 0, 0, 0.4);
  --shadow-2xl: 0 25px 50px -12px rgba(0, 0, 0, 0.6);
  
  /* Glow shadows for accent elements */
  --shadow-glow-sm: 0 0 10px rgba(99, 102, 241, 0.3);
  --shadow-glow-md: 0 0 20px rgba(99, 102, 241, 0.4);
  --shadow-glow-lg: 0 0 40px rgba(139, 92, 246, 0.3);
  
  /* Card shadows */
  --shadow-card: 0 4px 6px -1px rgba(0, 0, 0, 0.3), 0 0 0 1px rgba(255, 255, 255, 0.05);
  --shadow-card-hover: 0 10px 15px -3px rgba(0, 0, 0, 0.4), 0 0 0 1px rgba(255, 255, 255, 0.1);
}
```

### Borders

```css
:root {
  --border-width: 1px;
  --border-width-2: 2px;
  --border-style: solid;
}
```

---

## Spacing

### Scale

3/5 Confidence: Medium

```css
:root {
  --space-0: 0;
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-5: 20px;
  --space-6: 24px;
  --space-8: 32px;
  --space-10: 40px;
  --space-12: 48px;
  --space-16: 64px;
  --space-20: 80px;
  --space-24: 96px;
  --space-32: 128px;
}
```

### Container

```css
:root {
  --container-sm: 640px;
  --container-md: 768px;
  --container-lg: 1024px;
  --container-xl: 1200px;
  --container-2xl: 1400px;
  
  /* Content max-width */
  --content-max: 1200px;
  
  /* Padding */
  --container-padding: 24px;
  --container-padding-lg: 48px;
}
```

### Breakpoints

```css
--breakpoint-sm: 640px;
--breakpoint-md: 768px;
--breakpoint-lg: 1024px;
--breakpoint-xl: 1280px;
--breakpoint-2xl: 1536px;
```

---

## Components

### Buttons

**Primary button**
```css
.btn-primary {
  background: var(--gradient-primary);
  color: var(--primary-foreground);
  padding: 12px 24px;
  border-radius: var(--radius-lg);
  font-weight: var(--font-semibold);
  font-size: 14px;
  letter-spacing: 0.025em;
  border: none;
  cursor: pointer;
  transition: all 200ms ease;
}

.btn-primary:hover {
  background: var(--gradient-primary-hover);
  transform: translateY(-1px);
  box-shadow: var(--shadow-glow-sm);
}

.btn-primary:active {
  transform: translateY(0);
}
```

**Secondary button**
```css
.btn-secondary {
  background: var(--secondary);
  color: var(--secondary-foreground);
  padding: 12px 24px;
  border-radius: var(--radius-lg);
  font-weight: var(--font-medium);
  font-size: 14px;
  border: 1px solid var(--border);
  cursor: pointer;
  transition: all 200ms ease;
}

.btn-secondary:hover {
  background: var(--muted);
  border-color: var(--border-hover);
}
```

**Ghost button**
```css
.btn-ghost {
  background: transparent;
  color: var(--foreground);
  padding: 12px 24px;
  border-radius: var(--radius-lg);
  font-weight: var(--font-medium);
  font-size: 14px;
  border: none;
  cursor: pointer;
  transition: all 200ms ease;
}

.btn-ghost:hover {
  background: var(--muted);
}
```

### Cards

**Base card**
```css
.card {
  background: var(--card);
  color: var(--card-foreground);
  border: 1px solid var(--border);
  border-radius: var(--radius-xl);
  padding: var(--space-6);
  transition: all 200ms ease;
}

.card:hover {
  background: var(--card-hover);
  border-color: var(--border-hover);
  box-shadow: var(--shadow-card-hover);
  transform: translateY(-2px);
}
```

**Featured card**
```css
.card-featured {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: var(--radius-2xl);
  padding: var(--space-8);
  position: relative;
  overflow: hidden;
}

.card-featured::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 1px;
  background: var(--gradient-primary);
  opacity: 0.5;
}
```

### Inputs

```css
.input {
  background: var(--background-secondary);
  color: var(--foreground);
  border: 1px solid var(--input);
  border-radius: var(--radius-lg);
  padding: 12px 16px;
  font-size: 16px;
  width: 100%;
  transition: all 150ms ease;
}

.input::placeholder {
  color: var(--foreground-muted);
}

.input:focus {
  outline: none;
  border-color: var(--ring);
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.2);
}
```

### Navigation

```css
.nav {
  background: rgba(10, 10, 15, 0.8);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid var(--border);
  padding: 16px 24px;
  position: sticky;
  top: 0;
  z-index: 50;
}

.nav-link {
  color: var(--foreground-secondary);
  font-size: 14px;
  font-weight: var(--font-medium);
  padding: 8px 12px;
  border-radius: var(--radius-md);
  text-decoration: none;
  transition: all 150ms ease;
}

.nav-link:hover {
  color: var(--foreground);
  background: var(--muted);
}
```

### Tabs

```css
.tabs {
  display: flex;
  gap: 4px;
  background: var(--background-secondary);
  padding: 4px;
  border-radius: var(--radius-lg);
  border: 1px solid var(--border);
}

.tab {
  padding: 8px 16px;
  border-radius: var(--radius-md);
  font-size: 14px;
  font-weight: var(--font-medium);
  color: var(--foreground-muted);
  background: transparent;
  border: none;
  cursor: pointer;
  transition: all 150ms ease;
}

.tab:hover {
  color: var(--foreground-secondary);
}

.tab-active {
  background: var(--muted);
  color: var(--foreground);
}
```

### Badges

```css
.badge {
  display: inline-flex;
  align-items: center;
  padding: 4px 12px;
  border-radius: var(--radius-full);
  font-size: 12px;
  font-weight: var(--font-medium);
  letter-spacing: 0.025em;
}

.badge-primary {
  background: rgba(99, 102, 241, 0.2);
  color: var(--accent);
  border: 1px solid rgba(99, 102, 241, 0.3);
}
```

---

## Animations

### Transitions

```css
:root {
  --transition-fast: 150ms ease;
  --transition-base: 200ms ease;
  --transition-slow: 300ms ease;
  --transition-slower: 500ms ease;
}
```

### Easing functions

```css
:root {
  --ease-linear: linear;
  --ease-in: cubic-bezier(0.4, 0, 1, 1);
  --ease-out: cubic-bezier(0, 0, 0.2, 1);
  --ease-in-out: cubic-bezier(0.4, 0, 0.2, 1);
}
```

### Keyframe animations

**Fade in**
```css
@keyframes fade-in {
  from { opacity: 0; }
  to { opacity: 1; }
}
```

**Slide up**
```css
@keyframes slide-up {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
```

**Marquee (logo scroll)**
```css
@keyframes marquee {
  0% { transform: translateX(0); }
  100% { transform: translateX(-50%); }
}

.animate-marquee {
  animation: marquee 30s linear infinite;
}
```

**Hover lift**
```css
.hover-lift {
  transition: transform 200ms ease, box-shadow 200ms ease;
}

.hover-lift:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
}
```

**Glow pulse**
```css
@keyframes glow-pulse {
  0%, 100% { box-shadow: var(--shadow-glow-sm); }
  50% { box-shadow: var(--shadow-glow-md); }
}
```

---

## Dark mode

The site is dark-themed by default. Light mode inversion:

```css
.light {
  --background: #ffffff;
  --background-secondary: #f4f4f5;
  --background-tertiary: #e4e4e7;
  
  --foreground: #09090b;
  --foreground-secondary: #52525b;
  --foreground-muted: #a1a1aa;
  
  --card: #ffffff;
  --card-foreground: #09090b;
  
  --border: #e4e4e7;
  --input: #e4e4e7;
  
  --muted: #f4f4f5;
  --muted-foreground: #71717a;
}
```

---

## Tailwind config

```js
// tailwind.config.js
module.exports = {
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        background: 'var(--background)',
        foreground: 'var(--foreground)',
        primary: {
          DEFAULT: 'var(--primary)',
          foreground: 'var(--primary-foreground)',
        },
        secondary: {
          DEFAULT: 'var(--secondary)',
          foreground: 'var(--secondary-foreground)',
        },
        accent: {
          DEFAULT: 'var(--accent)',
          foreground: 'var(--accent-foreground)',
        },
        muted: {
          DEFAULT: 'var(--muted)',
          foreground: 'var(--muted-foreground)',
        },
        card: {
          DEFAULT: 'var(--card)',
          foreground: 'var(--card-foreground)',
        },
        border: 'var(--border)',
        input: 'var(--input)',
        ring: 'var(--ring)',
      },
      fontFamily: {
        sans: ['Inter', '-apple-system', 'BlinkMacSystemFont', 'sans-serif'],
        mono: ['SF Mono', 'Fira Code', 'monospace'],
      },
      borderRadius: {
        lg: 'var(--radius-lg)',
        md: 'var(--radius-md)',
        sm: 'var(--radius-sm)',
        xl: 'var(--radius-xl)',
        '2xl': 'var(--radius-2xl)',
      },
      boxShadow: {
        'glow-sm': 'var(--shadow-glow-sm)',
        'glow-md': 'var(--shadow-glow-md)',
        'glow-lg': 'var(--shadow-glow-lg)',
      },
      animation: {
        'fade-in': 'fade-in 300ms ease-out',
        'slide-up': 'slide-up 400ms ease-out',
        marquee: 'marquee 30s linear infinite',
      },
    },
  },
}
```

---

## Implementation notes

1. **Platform**: Built on Framer with dynamically injected styles. CSS variables aren't directly accessible, so values are approximated from visual analysis.

2. **Gradient rays**: The distinctive purple/indigo rays behind the hero use positioned PNG images with blend modes. To recreate, use `<div>` elements with gradient backgrounds, `position: absolute`, and `opacity: 0.2-0.3`.

3. **Logo marquee**: Uses CSS animation with duplicated content for seamless looping. Logos are grayscale by default, colored on hover.

4. **Tab component**: Service tabs use a contained design with dark background. Active state uses slightly lighter muted background.

5. **Card interactions**: All cards use subtle hover lift (translateY -2px) with shadow deepening. Border color also shifts lighter on hover.

6. **Typography**: Headlines use tighter tracking for density. Body copy uses comfortable line heights. Stats/metrics use bold weights.

7. **AI integration**: Footer includes direct links to query AI assistants — a unique pattern worth considering for similar sites.

## What couldn't be extracted

- **Exact font files**: Framer may use custom font loading. Inter is a reasonable assumption.
- **Precise color values**: No CSS variables exposed. Values approximated from visual inspection.
- **Animation timing functions**: Inferred from observed behavior, not from code.
- **Responsive breakpoints**: Standard breakpoints assumed, not verified from source.
