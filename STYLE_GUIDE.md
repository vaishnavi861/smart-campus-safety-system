# Style Guide - Smart Campus Safety System

## Color Palette (Inspired by CMRTC)

### Primary Colors
- **Primary Blue 1**: `#003d82` - Main branding color
- **Primary Blue 2**: `#1a5fa0` - Gradient secondary
- **Accent Red**: `#ff6b6b` / `#ff5252` - Emergency/alerts
- **White**: `#FFFFFF` - Cards, backgrounds
- **Light Gray**: `#f5f5f5` - Page background
- **Dark Gray**: `#666` - Text secondary
- **Black**: `#1a1a1a` - Footer background

### Gradients
- **Header Gradient**: `linear-gradient(135deg, #003d82 0%, #1a5fa0 100%)`
- **Emergency Gradient**: `linear-gradient(135deg, #ff6b6b 0%, #ff5252 100%)`

## Typography

### Font Stack
```css
font-family: 'Segoe UI', 'Helvetica Neue', sans-serif;
```

### Font Sizes
- **Page Title (h1)**: 3em, Bold (700)
- **Section Title (h2)**: 2.2em, Bold (700)
- **Card Title (h3)**: 1.4em, SemiBold (600)
- **Body Text**: 1em, Regular (400)
- **Small Text**: 0.95em, Regular (400)

### Line Height
- Headings: 1.2
- Body: 1.6
- Labels: 1.4

## Spacing System

### Padding
- Section Padding: `80px 20px` (desktop)
- Card Padding: `40px`
- Navbar Padding: `15px 0`
- Button Padding: `15px 35px`

### Margins
- Section Bottom: `60px`
- Card Gap: `30px`
- Nav Gap: `30px`

## Components

### Buttons

**Primary Button**
```css
background: #ff6b6b;
color: white;
padding: 15px 35px;
border-radius: 5px;
font-weight: bold;
```

**Secondary Button**
```css
background: white;
color: #003d82;
padding: 15px 35px;
border-radius: 5px;
font-weight: bold;
```

### Cards
```css
background: white;
border-radius: 10px;
box-shadow: 0 4px 15px rgba(0,0,0,0.08);
border-top: 4px solid #1a5fa0;
transition: transform 0.3s;
```

### Badges
```css
background: #f9f9f9;
border: 2px solid #1a5fa0;
border-radius: 10px;
padding: 40px;
```

## Hover Effects

### Card Hover
```css
transform: translateY(-8px);
box-shadow: 0 8px 25px rgba(0,0,0,0.12);
```

### Badge Hover
```css
transform: scale(1.05);
```

### Button Hover
```css
transform: translateY(-2px);
box-shadow: 0 5px 20px rgba(255,107,107,0.3);
```

## Animations

### Pulse Animation (Emergency Button)
```css
@keyframes pulse {
    0%, 100% { box-shadow: 0 0 0 0 rgba(255,255,255,0.7); }
    50% { box-shadow: 0 0 0 10px rgba(255,255,255,0); }
}
```

### Transitions
- Default: `0.3s` (all properties)
- Smooth: `cubic-bezier(0.4, 0, 0.2, 1)`

## Breakpoints (Responsive)

### Desktop
- Width: > 1024px
- Grid: `repeat(auto-fit, minmax(300px, 1fr))`

### Tablet
- Width: 768px - 1024px
- Grid: `repeat(auto-fit, minmax(280px, 1fr))`

### Mobile
- Width: < 768px
- Layout: Single column, stacked content

## Shadows

### Light Shadow
```css
box-shadow: 0 4px 15px rgba(0,0,0,0.08);
```

### Medium Shadow
```css
box-shadow: 0 8px 25px rgba(0,0,0,0.12);
```

### Heavy Shadow
```css
box-shadow: 0 20px 60px rgba(0,0,0,0.2);
```

## Border Radius
- Navbar/Footer: `0px`
- Cards: `10px`
- Buttons: `5px`
- Buttons (round): `50px`

## Z-Index Hierarchy
- Navbar: `1000`
- Modals: `2000` (if added)
- Tooltips: `3000` (if added)

## Accessibility

### Color Contrast
- Dark text on white: WCAG AAA compliant
- White text on blue: WCAG AA compliant
- Red on white: WCAG AA compliant

### Focus States
- All interactive elements have visible focus states
- Button focus: `outline: 2px solid #003d82;`

## Design Pattern Library

### Section Layout
```html
<section class="section-name">
    <div class="section-content">
        <h2 class="section-title">Title</h2>
        <div class="grid-class">
            <div class="item">Content</div>
        </div>
    </div>
</section>
```

### Card Layout
```html
<div class="card-item">
    <div class="icon">🎯</div>
    <h3>Title</h3>
    <p>Description</p>
</div>
```

### Button Usage
```html
<button class="btn btn-primary">Primary Action</button>
<button class="btn btn-secondary">Secondary Action</button>
```

## Performance Considerations

- No external fonts (uses system fonts)
- No image assets required (uses emojis and CSS)
- Minimal CSS (optimized for speed)
- No JavaScript required for styling
- Optimized for 60 FPS animations

## Mobile-First Approach

1. Base styles for mobile
2. Media queries for tablet (768px)
3. Additional features for desktop (1024px)

---

**This style guide maintains consistency with cmrtc.ac.in while being optimized for your Smart Campus Safety System.**
