# Component Examples

Input/output examples showing how to implement AD-branded components.

## Example 1: Primary Button

**Input**: "Create a primary call-to-action button"

**Output**:
```html
<button class="btn-primary">
  Get Started
</button>

<style>
.btn-primary {
  background: #00b4d8;
  color: white;
  padding: 8px 16px;
  border-radius: 6px;
  font-weight: 500;
  height: 40px;
  border: none;
  cursor: pointer;
  transition: background 150ms cubic-bezier(0.25, 1, 0.5, 1);
}
.btn-primary:hover {
  background: #0096b4;
}
</style>
```

## Example 2: Card Component

**Input**: "Create a content card for light mode"

**Output**:
```html
<div class="card">
  <h3>Card Title</h3>
  <p>Card content goes here.</p>
</div>

<style>
.card {
  background: white;
  border: 1px solid #f2f2f2;
  border-radius: 8px;
  padding: 24px;
  box-shadow: 0 1px 2px rgba(0,0,0,0.05);
}
.card h3 {
  color: #03045e;
  font-size: 16px;
  font-weight: 600;
  margin: 0 0 8px 0;
}
.card p {
  color: #03045e;
  font-size: 14px;
  margin: 0;
}
</style>
```

## Example 3: Input Field with Error

**Input**: "Create a form input with error state"

**Output**:
```html
<div class="input-group error">
  <label for="email">Email</label>
  <input type="email" id="email" placeholder="Enter email">
  <span class="error-message">Please enter a valid email</span>
</div>

<style>
.input-group label {
  display: block;
  font-weight: 500;
  font-size: 14px;
  color: #03045e;
  margin-bottom: 4px;
}
.input-group input {
  width: 100%;
  height: 40px;
  padding: 8px 12px;
  border: 1px solid #f2f2f2;
  border-radius: 6px;
  font-size: 14px;
}
.input-group.error input {
  border-color: #ef4444;
  box-shadow: 0 0 0 2px rgba(239, 68, 68, 0.2);
}
.error-message {
  font-size: 12px;
  color: #ef4444;
  margin-top: 4px;
}
</style>
```

## Example 4: Dark Mode Card

**Input**: "Create a card for dark mode"

**Output**:
```html
<div class="card-dark">
  <h3>Card Title</h3>
  <p>Card content goes here.</p>
</div>

<style>
.card-dark {
  background: #1e2329;
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 8px;
  padding: 24px;
}
.card-dark h3 {
  color: #f2f2f2;
  font-size: 16px;
  font-weight: 600;
  margin: 0 0 8px 0;
}
.card-dark p {
  color: #f2f2f2;
  font-size: 14px;
  opacity: 0.8;
  margin: 0;
}
</style>
```

## Example 5: Navigation Item

**Input**: "Create a sidebar navigation item with active state"

**Output**:
```html
<nav class="sidebar">
  <a href="#" class="nav-item">Dashboard</a>
  <a href="#" class="nav-item active">Analytics</a>
  <a href="#" class="nav-item">Settings</a>
</nav>

<style>
.sidebar {
  width: 240px;
  background: #171c21;
  padding: 16px 0;
}
.nav-item {
  display: block;
  padding: 8px 16px;
  color: #f2f2f2;
  text-decoration: none;
  font-size: 14px;
  border-left: 3px solid transparent;
  transition: all 150ms cubic-bezier(0.25, 1, 0.5, 1);
}
.nav-item:hover {
  background: rgba(255,255,255,0.05);
}
.nav-item.active {
  color: #00b4d8;
  border-left-color: #00b4d8;
  background: rgba(0, 180, 216, 0.1);
}
</style>
```
