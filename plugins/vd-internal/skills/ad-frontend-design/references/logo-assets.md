# Vibedata Logo Assets — Machine-Readable Manifest

<!-- source_svgs_path: branding/logo/archive/svg_sources/ -->
<!-- source_svgs: icon-dark.svg, icon-light.svg, icon-monochrome.svg, logo-dark.svg, logo-light.svg, logo-icon-lockup-dark.svg, logo-icon-lockup-light.svg -->
<!-- Schema: logo_color describes the artwork color. background_for is the required background type. -->
<!-- logo_color: light=white/light strokes | dark=dark strokes | monochrome=single-color mask -->
<!-- background_for: dark-bg=requires dark/colored bg | light-bg=requires light/white bg | any=works on any bg -->
<!-- width_px / height_px: pixel dimensions for raster; nominal display size for h-named SVGs; — for fully scalable vectors -->
<!-- cdn_base_url: http://assets.acceleratedata.ai/logo/ — url column = cdn_base_url + path -->
<!-- design_system_skill: branding/ad-frontend-design/SKILL.md -->
<!-- design_system_description: Complete frontend design system with color tokens, typography, spacing, component patterns, and logo usage guidelines -->

<!-- naming_patterns:
  icons:    icon-{dark|light}.svg (unsized vector) OR icon-{dark|light}-{size}.png (sized raster: 16,20,24,28,32,40,48,64,96,128,256,512)
  wordmarks: logo-{dark|light}-h{size}.svg (sized by height: 20,24,32,40,48,64,80,96,128) — ONLY wordmarks use the "h" prefix
  lockups:  logo-icon-lockup-{dark|light}-{size}.svg (sized by bounding box: 48,64,80,96,128,160,192) — NO "h" prefix, minimum 48px
  favicons: web/favicons/ — mixed naming, always look up exact path from table
-->

<!-- common_mistakes:
  WRONG: icon-dark-32.svg  → sized icon SVGs do not exist; use icon-dark.svg (vector) or icon-dark-32.png (raster)
  WRONG: logo-icon-lockup-dark-h48.svg → lockups do not use "h" prefix; correct: logo-icon-lockup-dark-48.svg
  WRONG: logo-icon-lockup-dark-32.svg → lockup minimum size is 48; smallest is logo-icon-lockup-dark-48.svg
  RULE: Always look up the exact "url" column from the table below. Do not construct URLs by pattern interpolation.
-->

| asset_id | logo_type | logo_color | background_for | format | width_px | height_px | path | url |
|----------|-----------|------------|----------------|--------|----------|-----------|------|-----|
| logo-light-docs | logo | light | dark-bg | SVG | — | — | docs/assets/logo-light.svg | http://assets.acceleratedata.ai/logo/docs/assets/logo-light.svg |
| avatar-400 | icon | light | dark-bg | PNG | 400 | 400 | marketing/social/avatar-400.png | http://assets.acceleratedata.ai/logo/marketing/social/avatar-400.png |
| azure-logo-large-216 | icon | light | dark-bg | PNG | 216 | 216 | marketplaces/azure/azure-logo-large-216.png | http://assets.acceleratedata.ai/logo/marketplaces/azure/azure-logo-large-216.png |
| azure-logo-large-350 | icon | light | dark-bg | PNG | 350 | 350 | marketplaces/azure/azure-logo-large-350.png | http://assets.acceleratedata.ai/logo/marketplaces/azure/azure-logo-large-350.png |
| azure-logo-medium-90 | icon | light | dark-bg | PNG | 90 | 90 | marketplaces/azure/azure-logo-medium-90.png | http://assets.acceleratedata.ai/logo/marketplaces/azure/azure-logo-medium-90.png |
| azure-logo-small-48 | icon | light | dark-bg | PNG | 48 | 48 | marketplaces/azure/azure-logo-small-48.png | http://assets.acceleratedata.ai/logo/marketplaces/azure/azure-logo-small-48.png |
| email-logo-h32@2x | logo | light | dark-bg | PNG | 683 | 64 | ops/email/email-logo-h32@2x.png | http://assets.acceleratedata.ai/logo/ops/email/email-logo-h32@2x.png |
| icon-dark-svg | icon | dark | light-bg | SVG | — | — | product/ui/icon-dark.svg | http://assets.acceleratedata.ai/logo/product/ui/icon-dark.svg |
| icon-dark-16 | icon | dark | light-bg | PNG | 16 | 16 | product/ui/icon-dark-16.png | http://assets.acceleratedata.ai/logo/product/ui/icon-dark-16.png |
| icon-dark-20 | icon | dark | light-bg | PNG | 20 | 20 | product/ui/icon-dark-20.png | http://assets.acceleratedata.ai/logo/product/ui/icon-dark-20.png |
| icon-dark-24 | icon | dark | light-bg | PNG | 24 | 24 | product/ui/icon-dark-24.png | http://assets.acceleratedata.ai/logo/product/ui/icon-dark-24.png |
| icon-dark-28 | icon | dark | light-bg | PNG | 28 | 28 | product/ui/icon-dark-28.png | http://assets.acceleratedata.ai/logo/product/ui/icon-dark-28.png |
| icon-dark-32 | icon | dark | light-bg | PNG | 32 | 32 | product/ui/icon-dark-32.png | http://assets.acceleratedata.ai/logo/product/ui/icon-dark-32.png |
| icon-dark-40 | icon | dark | light-bg | PNG | 40 | 40 | product/ui/icon-dark-40.png | http://assets.acceleratedata.ai/logo/product/ui/icon-dark-40.png |
| icon-dark-48 | icon | dark | light-bg | PNG | 48 | 48 | product/ui/icon-dark-48.png | http://assets.acceleratedata.ai/logo/product/ui/icon-dark-48.png |
| icon-dark-64 | icon | dark | light-bg | PNG | 64 | 64 | product/ui/icon-dark-64.png | http://assets.acceleratedata.ai/logo/product/ui/icon-dark-64.png |
| icon-dark-96 | icon | dark | light-bg | PNG | 96 | 96 | product/ui/icon-dark-96.png | http://assets.acceleratedata.ai/logo/product/ui/icon-dark-96.png |
| icon-dark-128 | icon | dark | light-bg | PNG | 128 | 128 | product/ui/icon-dark-128.png | http://assets.acceleratedata.ai/logo/product/ui/icon-dark-128.png |
| icon-dark-256 | icon | dark | light-bg | PNG | 256 | 256 | product/ui/icon-dark-256.png | http://assets.acceleratedata.ai/logo/product/ui/icon-dark-256.png |
| icon-dark-512 | icon | dark | light-bg | PNG | 512 | 512 | product/ui/icon-dark-512.png | http://assets.acceleratedata.ai/logo/product/ui/icon-dark-512.png |
| icon-light-svg | icon | light | dark-bg | SVG | — | — | product/ui/icon-light.svg | http://assets.acceleratedata.ai/logo/product/ui/icon-light.svg |
| icon-light-16 | icon | light | dark-bg | PNG | 16 | 16 | product/ui/icon-light-16.png | http://assets.acceleratedata.ai/logo/product/ui/icon-light-16.png |
| icon-light-20 | icon | light | dark-bg | PNG | 20 | 20 | product/ui/icon-light-20.png | http://assets.acceleratedata.ai/logo/product/ui/icon-light-20.png |
| icon-light-24 | icon | light | dark-bg | PNG | 24 | 24 | product/ui/icon-light-24.png | http://assets.acceleratedata.ai/logo/product/ui/icon-light-24.png |
| icon-light-28 | icon | light | dark-bg | PNG | 28 | 28 | product/ui/icon-light-28.png | http://assets.acceleratedata.ai/logo/product/ui/icon-light-28.png |
| icon-light-32 | icon | light | dark-bg | PNG | 32 | 32 | product/ui/icon-light-32.png | http://assets.acceleratedata.ai/logo/product/ui/icon-light-32.png |
| icon-light-40 | icon | light | dark-bg | PNG | 40 | 40 | product/ui/icon-light-40.png | http://assets.acceleratedata.ai/logo/product/ui/icon-light-40.png |
| icon-light-48 | icon | light | dark-bg | PNG | 48 | 48 | product/ui/icon-light-48.png | http://assets.acceleratedata.ai/logo/product/ui/icon-light-48.png |
| icon-light-64 | icon | light | dark-bg | PNG | 64 | 64 | product/ui/icon-light-64.png | http://assets.acceleratedata.ai/logo/product/ui/icon-light-64.png |
| icon-light-96 | icon | light | dark-bg | PNG | 96 | 96 | product/ui/icon-light-96.png | http://assets.acceleratedata.ai/logo/product/ui/icon-light-96.png |
| icon-light-128 | icon | light | dark-bg | PNG | 128 | 128 | product/ui/icon-light-128.png | http://assets.acceleratedata.ai/logo/product/ui/icon-light-128.png |
| icon-light-256 | icon | light | dark-bg | PNG | 256 | 256 | product/ui/icon-light-256.png | http://assets.acceleratedata.ai/logo/product/ui/icon-light-256.png |
| icon-light-512 | icon | light | dark-bg | PNG | 512 | 512 | product/ui/icon-light-512.png | http://assets.acceleratedata.ai/logo/product/ui/icon-light-512.png |
| logo-dark-h20 | logo | dark | light-bg | SVG | — | 20 | product/ui/logo-dark-h20.svg | http://assets.acceleratedata.ai/logo/product/ui/logo-dark-h20.svg |
| logo-dark-h24 | logo | dark | light-bg | SVG | — | 24 | product/ui/logo-dark-h24.svg | http://assets.acceleratedata.ai/logo/product/ui/logo-dark-h24.svg |
| logo-dark-h24@2x | logo | dark | light-bg | PNG | 512 | 48 | product/ui/logo-dark-h24@2x.png | http://assets.acceleratedata.ai/logo/product/ui/logo-dark-h24@2x.png |
| logo-dark-h32 | logo | dark | light-bg | SVG | — | 32 | product/ui/logo-dark-h32.svg | http://assets.acceleratedata.ai/logo/product/ui/logo-dark-h32.svg |
| logo-dark-h32@2x | logo | dark | light-bg | PNG | 683 | 64 | product/ui/logo-dark-h32@2x.png | http://assets.acceleratedata.ai/logo/product/ui/logo-dark-h32@2x.png |
| logo-dark-h40 | logo | dark | light-bg | SVG | — | 40 | product/ui/logo-dark-h40.svg | http://assets.acceleratedata.ai/logo/product/ui/logo-dark-h40.svg |
| logo-dark-h48 | logo | dark | light-bg | SVG | — | 48 | product/ui/logo-dark-h48.svg | http://assets.acceleratedata.ai/logo/product/ui/logo-dark-h48.svg |
| logo-dark-h48@2x | logo | dark | light-bg | PNG | 1024 | 96 | product/ui/logo-dark-h48@2x.png | http://assets.acceleratedata.ai/logo/product/ui/logo-dark-h48@2x.png |
| logo-dark-h64 | logo | dark | light-bg | SVG | — | 64 | product/ui/logo-dark-h64.svg | http://assets.acceleratedata.ai/logo/product/ui/logo-dark-h64.svg |
| logo-dark-h64@2x | logo | dark | light-bg | PNG | 1366 | 128 | product/ui/logo-dark-h64@2x.png | http://assets.acceleratedata.ai/logo/product/ui/logo-dark-h64@2x.png |
| logo-dark-h80 | logo | dark | light-bg | SVG | — | 80 | product/ui/logo-dark-h80.svg | http://assets.acceleratedata.ai/logo/product/ui/logo-dark-h80.svg |
| logo-dark-h96 | logo | dark | light-bg | SVG | — | 96 | product/ui/logo-dark-h96.svg | http://assets.acceleratedata.ai/logo/product/ui/logo-dark-h96.svg |
| logo-dark-h96@2x | logo | dark | light-bg | PNG | 2049 | 192 | product/ui/logo-dark-h96@2x.png | http://assets.acceleratedata.ai/logo/product/ui/logo-dark-h96@2x.png |
| logo-dark-h128 | logo | dark | light-bg | SVG | — | 128 | product/ui/logo-dark-h128.svg | http://assets.acceleratedata.ai/logo/product/ui/logo-dark-h128.svg |
| logo-dark-h128@2x | logo | dark | light-bg | PNG | 2732 | 256 | product/ui/logo-dark-h128@2x.png | http://assets.acceleratedata.ai/logo/product/ui/logo-dark-h128@2x.png |
| logo-icon-lockup-dark-48 | logo+icon | dark | light-bg | SVG | 48 | 48 | product/ui/logo-icon-lockup-dark-48.svg | http://assets.acceleratedata.ai/logo/product/ui/logo-icon-lockup-dark-48.svg |
| logo-icon-lockup-dark-64 | logo+icon | dark | light-bg | SVG | 64 | 64 | product/ui/logo-icon-lockup-dark-64.svg | http://assets.acceleratedata.ai/logo/product/ui/logo-icon-lockup-dark-64.svg |
| logo-icon-lockup-dark-80 | logo+icon | dark | light-bg | SVG | 80 | 80 | product/ui/logo-icon-lockup-dark-80.svg | http://assets.acceleratedata.ai/logo/product/ui/logo-icon-lockup-dark-80.svg |
| logo-icon-lockup-dark-96 | logo+icon | dark | light-bg | SVG | 96 | 96 | product/ui/logo-icon-lockup-dark-96.svg | http://assets.acceleratedata.ai/logo/product/ui/logo-icon-lockup-dark-96.svg |
| logo-icon-lockup-dark-128 | logo+icon | dark | light-bg | SVG | 128 | 128 | product/ui/logo-icon-lockup-dark-128.svg | http://assets.acceleratedata.ai/logo/product/ui/logo-icon-lockup-dark-128.svg |
| logo-icon-lockup-dark-160 | logo+icon | dark | light-bg | SVG | 160 | 160 | product/ui/logo-icon-lockup-dark-160.svg | http://assets.acceleratedata.ai/logo/product/ui/logo-icon-lockup-dark-160.svg |
| logo-icon-lockup-dark-192 | logo+icon | dark | light-bg | SVG | 192 | 192 | product/ui/logo-icon-lockup-dark-192.svg | http://assets.acceleratedata.ai/logo/product/ui/logo-icon-lockup-dark-192.svg |
| logo-icon-lockup-light-48 | logo+icon | light | dark-bg | SVG | 48 | 48 | product/ui/logo-icon-lockup-light-48.svg | http://assets.acceleratedata.ai/logo/product/ui/logo-icon-lockup-light-48.svg |
| logo-icon-lockup-light-64 | logo+icon | light | dark-bg | SVG | 64 | 64 | product/ui/logo-icon-lockup-light-64.svg | http://assets.acceleratedata.ai/logo/product/ui/logo-icon-lockup-light-64.svg |
| logo-icon-lockup-light-80 | logo+icon | light | dark-bg | SVG | 80 | 80 | product/ui/logo-icon-lockup-light-80.svg | http://assets.acceleratedata.ai/logo/product/ui/logo-icon-lockup-light-80.svg |
| logo-icon-lockup-light-96 | logo+icon | light | dark-bg | SVG | 96 | 96 | product/ui/logo-icon-lockup-light-96.svg | http://assets.acceleratedata.ai/logo/product/ui/logo-icon-lockup-light-96.svg |
| logo-icon-lockup-light-128 | logo+icon | light | dark-bg | SVG | 128 | 128 | product/ui/logo-icon-lockup-light-128.svg | http://assets.acceleratedata.ai/logo/product/ui/logo-icon-lockup-light-128.svg |
| logo-icon-lockup-light-160 | logo+icon | light | dark-bg | SVG | 160 | 160 | product/ui/logo-icon-lockup-light-160.svg | http://assets.acceleratedata.ai/logo/product/ui/logo-icon-lockup-light-160.svg |
| logo-icon-lockup-light-192 | logo+icon | light | dark-bg | SVG | 192 | 192 | product/ui/logo-icon-lockup-light-192.svg | http://assets.acceleratedata.ai/logo/product/ui/logo-icon-lockup-light-192.svg |
| logo-light-h20 | logo | light | dark-bg | SVG | — | 20 | product/ui/logo-light-h20.svg | http://assets.acceleratedata.ai/logo/product/ui/logo-light-h20.svg |
| logo-light-h24 | logo | light | dark-bg | SVG | — | 24 | product/ui/logo-light-h24.svg | http://assets.acceleratedata.ai/logo/product/ui/logo-light-h24.svg |
| logo-light-h24@2x | logo | light | dark-bg | PNG | 512 | 48 | product/ui/logo-light-h24@2x.png | http://assets.acceleratedata.ai/logo/product/ui/logo-light-h24@2x.png |
| logo-light-h32 | logo | light | dark-bg | SVG | — | 32 | product/ui/logo-light-h32.svg | http://assets.acceleratedata.ai/logo/product/ui/logo-light-h32.svg |
| logo-light-h32@2x | logo | light | dark-bg | PNG | 683 | 64 | product/ui/logo-light-h32@2x.png | http://assets.acceleratedata.ai/logo/product/ui/logo-light-h32@2x.png |
| logo-light-h40 | logo | light | dark-bg | SVG | — | 40 | product/ui/logo-light-h40.svg | http://assets.acceleratedata.ai/logo/product/ui/logo-light-h40.svg |
| logo-light-h48 | logo | light | dark-bg | SVG | — | 48 | product/ui/logo-light-h48.svg | http://assets.acceleratedata.ai/logo/product/ui/logo-light-h48.svg |
| logo-light-h48@2x | logo | light | dark-bg | PNG | 1024 | 96 | product/ui/logo-light-h48@2x.png | http://assets.acceleratedata.ai/logo/product/ui/logo-light-h48@2x.png |
| logo-light-h64 | logo | light | dark-bg | SVG | — | 64 | product/ui/logo-light-h64.svg | http://assets.acceleratedata.ai/logo/product/ui/logo-light-h64.svg |
| logo-light-h64@2x | logo | light | dark-bg | PNG | 1366 | 128 | product/ui/logo-light-h64@2x.png | http://assets.acceleratedata.ai/logo/product/ui/logo-light-h64@2x.png |
| logo-light-h80 | logo | light | dark-bg | SVG | — | 80 | product/ui/logo-light-h80.svg | http://assets.acceleratedata.ai/logo/product/ui/logo-light-h80.svg |
| logo-light-h96 | logo | light | dark-bg | SVG | — | 96 | product/ui/logo-light-h96.svg | http://assets.acceleratedata.ai/logo/product/ui/logo-light-h96.svg |
| logo-light-h96@2x | logo | light | dark-bg | PNG | 2049 | 192 | product/ui/logo-light-h96@2x.png | http://assets.acceleratedata.ai/logo/product/ui/logo-light-h96@2x.png |
| logo-light-h128 | logo | light | dark-bg | SVG | — | 128 | product/ui/logo-light-h128.svg | http://assets.acceleratedata.ai/logo/product/ui/logo-light-h128.svg |
| logo-light-h128@2x | logo | light | dark-bg | PNG | 2732 | 256 | product/ui/logo-light-h128@2x.png | http://assets.acceleratedata.ai/logo/product/ui/logo-light-h128@2x.png |
| apple-touch-icon | icon | light | dark-bg | PNG | 180 | 180 | web/favicons/apple-touch-icon.png | http://assets.acceleratedata.ai/logo/web/favicons/apple-touch-icon.png |
| favicon-dark-ico | icon | dark | light-bg | ICO | 48 | 48 | web/favicons/favicon-dark.ico | http://assets.acceleratedata.ai/logo/web/favicons/favicon-dark.ico |
| favicon-light-ico | icon | light | dark-bg | ICO | 48 | 48 | web/favicons/favicon-light.ico | http://assets.acceleratedata.ai/logo/web/favicons/favicon-light.ico |
| favicon-16x16-dark | icon | dark | light-bg | PNG | 16 | 16 | web/favicons/favicon-16x16-dark.png | http://assets.acceleratedata.ai/logo/web/favicons/favicon-16x16-dark.png |
| favicon-16x16-light | icon | light | dark-bg | PNG | 16 | 16 | web/favicons/favicon-16x16-light.png | http://assets.acceleratedata.ai/logo/web/favicons/favicon-16x16-light.png |
| favicon-32x32-dark | icon | dark | light-bg | PNG | 32 | 32 | web/favicons/favicon-32x32-dark.png | http://assets.acceleratedata.ai/logo/web/favicons/favicon-32x32-dark.png |
| favicon-32x32-light | icon | light | dark-bg | PNG | 32 | 32 | web/favicons/favicon-32x32-light.png | http://assets.acceleratedata.ai/logo/web/favicons/favicon-32x32-light.png |
| favicon-icon-dark-svg | icon | dark | light-bg | SVG | — | — | web/favicons/icon-dark.svg | http://assets.acceleratedata.ai/logo/web/favicons/icon-dark.svg |
| favicon-icon-light-svg | icon | light | dark-bg | SVG | — | — | web/favicons/icon-light.svg | http://assets.acceleratedata.ai/logo/web/favicons/icon-light.svg |
| pwa-icon-192 | icon | light | dark-bg | PNG | 192 | 192 | web/favicons/pwa-icon-192x192.png | http://assets.acceleratedata.ai/logo/web/favicons/pwa-icon-192x192.png |
| pwa-icon-512 | icon | light | dark-bg | PNG | 512 | 512 | web/favicons/pwa-icon-512x512.png | http://assets.acceleratedata.ai/logo/web/favicons/pwa-icon-512x512.png |
| safari-pinned-tab | icon | monochrome | any | SVG | — | — | web/favicons/safari-pinned-tab.svg | http://assets.acceleratedata.ai/logo/web/favicons/safari-pinned-tab.svg |
