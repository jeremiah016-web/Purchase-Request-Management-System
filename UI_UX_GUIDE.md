# UI/UX Design Guide
## Purchase Request Management System

---

## 🎨 Design System Overview

The Purchase Request Management System features a modern, professional design system built with user experience at its core. The interface combines clean aesthetics with functional design patterns to create an intuitive and visually appealing application.

---

## Color Palette

### Primary Colors
- **Primary**: `#667eea` (Vibrant Purple-Blue)
- **Secondary**: `#764ba2` (Deep Purple)
- **Gradient**: Linear gradient from Primary to Secondary

### Semantic Colors
- **Success**: `#10b981` (Emerald Green)
- **Danger**: `#ef4444` (Red)
- **Warning**: `#f59e0b` (Amber)
- **Info**: `#3b82f6` (Blue)

### Neutral Colors
- **Dark**: `#1f2937` (Charcoal)
- **Light**: `#f9fafb` (Off-white)
- **Gray Scale**: `#6b7280`, `#9ca3af`, `#e5e7eb`

---

## Typography

### Font Family
- **Primary**: Inter (Google Fonts)
- **Fallback**: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif

### Font Sizes
- **H1**: 2.5rem (40px)
- **H2**: 2rem (32px)
- **H3**: 1.75rem (28px)
- **H4**: 1.5rem (24px)
- **H5**: 1.25rem (20px)
- **H6**: 1rem (16px)
- **Body**: 0.9375rem (15px)
- **Small**: 0.875rem (14px)

### Font Weights
- **Regular**: 400
- **Medium**: 500
- **Semibold**: 600
- **Bold**: 700

---

## Components

### Buttons

**Primary Button**
- Gradient background (Primary → Secondary)
- White text
- Rounded corners (10px)
- Hover: Lift effect with shadow
- Padding: 0.625rem 1.5rem

**Secondary Button**
- Outlined style
- Border: 2px solid Primary
- Hover: Filled with gradient

**Button Sizes**
- Small: 0.375rem 1rem
- Default: 0.625rem 1.5rem
- Large: 0.875rem 2rem

### Cards

**Standard Card**
- White background
- Border radius: 12px
- Box shadow: Subtle elevation
- Hover: Lift effect (translateY(-4px))
- Padding: 1.5rem

**Stat Card**
- Left border accent (4px gradient)
- Icon with colored background
- Large number display
- Descriptive label
- Hover: Enhanced shadow

### Forms

**Input Fields**
- Border radius: 10px
- Border: 2px solid #e5e7eb
- Focus: Primary color border with glow
- Padding: 0.75rem 1rem

**Labels**
- Font weight: 600
- Color: Dark
- Margin bottom: 0.5rem

### Tables

**Header**
- Gradient background
- White text
- Uppercase labels
- Letter spacing: 0.5px

**Rows**
- Hover: Light gray background
- Subtle scale effect
- Border bottom: Light gray

### Badges

**Style**
- Rounded pill shape (20px radius)
- Padding: 0.5rem 1rem
- Uppercase text
- Font weight: 600
- Letter spacing: 0.5px

**Status Colors**
- Open: Blue
- Pending: Amber
- Approval: Green
- Closed: Gray
- On Hold: Red

### Alerts

**Design**
- Rounded corners (12px)
- Left border accent (4px)
- Icon included
- Slide-down animation
- Auto-dismiss after 5 seconds

---

## Layout

### Navigation Bar
- Fixed position at top
- Gradient background
- Box shadow for depth
- Responsive collapse on mobile
- Smooth hover transitions

### Main Content
- Padding top: 100px (navbar clearance)
- Container max-width: 1140px
- Responsive padding

### Cards & Sections
- Consistent spacing: 1.5rem - 2rem
- Margin bottom: 2rem
- Responsive grid layouts

---

## Animations & Transitions

### Standard Transition
```css
transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
```

### Hover Effects
- **Buttons**: Lift (translateY(-2px)) + Shadow
- **Cards**: Lift (translateY(-4px)) + Enhanced shadow
- **Links**: Color change + Scale
- **Table Rows**: Background + Scale

### Page Animations
- **Slide Down**: Alerts
- **Fade In**: Content sections
- **Slide In**: Side panels

---

## Responsive Design

### Breakpoints
- **Mobile**: < 768px
- **Tablet**: 768px - 1024px
- **Desktop**: > 1024px

### Mobile Optimizations
- Stacked layouts
- Larger touch targets
- Simplified navigation
- Reduced padding
- Single column grids

---

## Dashboard Design

### Stats Grid
- Auto-fit grid layout
- Minimum 250px columns
- Gap: 1.5rem
- Responsive to screen size

### Activity Feed
- Timeline-style layout
- Icon indicators
- Hover effects
- Timestamp display

### Quick Actions
- Grid of action cards
- Icon-based design
- Clear call-to-action
- Hover lift effect

---

## Accessibility

### Color Contrast
- WCAG AA compliant
- Minimum 4.5:1 ratio for text
- 3:1 for large text

### Focus States
- Visible focus indicators
- Keyboard navigation support
- Skip links for screen readers

### Semantic HTML
- Proper heading hierarchy
- ARIA labels where needed
- Alt text for images

---

## Best Practices

### Do's ✅
- Use consistent spacing (multiples of 0.25rem)
- Maintain visual hierarchy
- Provide clear feedback
- Use loading states
- Show error messages clearly
- Keep forms simple
- Use icons to enhance understanding

### Don'ts ❌
- Don't use too many colors
- Avoid cluttered layouts
- Don't hide important actions
- Avoid tiny touch targets on mobile
- Don't use low contrast text
- Avoid inconsistent spacing

---

## Component Examples

### Stat Card HTML
```html
<div class="stat-card">
  <div class="stat-card-icon primary">
    <i class="fas fa-file-alt"></i>
  </div>
  <div class="stat-card-value">24</div>
  <div class="stat-card-label">Total Requests</div>
  <div class="stat-card-change positive">
    <i class="fas fa-arrow-up"></i> 12% from last month
  </div>
</div>
```

### Button HTML
```html
<button class="btn btn-primary">
  <i class="fas fa-plus"></i>
  Create Request
</button>
```

### Alert HTML
```html
<div class="alert alert-success">
  <i class="fas fa-check-circle mr-2"></i>
  Your request has been submitted successfully!
</div>
```

---

## CSS Variables

```css
:root {
  --primary-color: #667eea;
  --secondary-color: #764ba2;
  --success-color: #10b981;
  --danger-color: #ef4444;
  --warning-color: #f59e0b;
  --info-color: #3b82f6;
  --dark-color: #1f2937;
  --light-color: #f9fafb;
  --border-radius: 12px;
  --box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
```

---

## File Structure

```
prs/static/prs/
├── main.css          # Core styles
├── dashboard.css     # Dashboard-specific styles
└── [future files]    # Additional style modules
```

---

## Browser Support

- Chrome (latest 2 versions)
- Firefox (latest 2 versions)
- Safari (latest 2 versions)
- Edge (latest 2 versions)
- Mobile browsers (iOS Safari, Chrome Mobile)

---

## Performance Optimizations

### CSS
- Minified in production
- Critical CSS inlined
- Non-critical CSS deferred

### Images
- Optimized file sizes
- Lazy loading
- Responsive images

### Animations
- GPU-accelerated transforms
- Will-change property for smooth animations
- Reduced motion support

---

## Future Enhancements

### Planned Features
- Dark mode support
- Custom theme builder
- More animation options
- Advanced data visualizations
- Micro-interactions
- Skeleton loading states

### Accessibility Improvements
- Enhanced keyboard navigation
- Better screen reader support
- High contrast mode
- Font size controls

---

## Resources

### Design Tools
- Figma (for mockups)
- Adobe XD (for prototypes)
- Coolors (for color palettes)

### Inspiration
- Dribbble
- Behance
- Awwwards
- Material Design

### Libraries Used
- Bootstrap 4
- Font Awesome 5
- Google Fonts (Inter)

---

## Maintenance

### Regular Updates
- Review color contrast
- Test on new browsers
- Update deprecated CSS
- Optimize performance
- Gather user feedback

### Version Control
- Document all changes
- Use semantic versioning
- Maintain changelog
- Test before deployment

---

**Design System Version**: 1.0.0
**Last Updated**: 2026
**Maintained By**: Development Team

---

For questions or suggestions about the UI/UX design, please contact the development team.
