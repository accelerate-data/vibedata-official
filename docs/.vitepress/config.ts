import { existsSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

import { defineConfig, type DefaultTheme } from 'vitepress';

// The release page is generated (and left uncommitted) by .github/workflows/publish.yml
// from the `studio-release` dispatch payload. Local builds do not have it, so the
// release entry only appears when the file is present.
const configDir = dirname(fileURLToPath(import.meta.url));
const releasePath = resolve(configDir, '..', 'release.md');
const hasReleasePage = existsSync(releasePath);

const gettingStarted: DefaultTheme.SidebarItem[] = [
  { text: 'Overview', link: '/' },
  { text: '01a · Microsoft Entra admin', link: '/01a-prereqs-entra-admin' },
  { text: '01b · Microsoft Fabric admin', link: '/01b-prereqs-fabric-admin' },
  { text: '01c · GitHub organisation owner', link: '/01c-prereqs-github-org-owner' },
  { text: '01d · Azure infrastructure owner', link: '/01d-prereqs-azure-infra' },
  { text: '01e · MotherDuck organisation admin', link: '/01e-prereqs-motherduck-admin' },
  { text: '02 · Operator setup', link: '/02-prereqs-operator' },
  { text: '03 · Deploy: Local Docker', link: '/03-deploy-docker' },
  { text: '04 · Deploy: Kubernetes on Azure', link: '/04-deploy-kubernetes-azure' },
  { text: '05 · Configure the organisation', link: '/05-configure-org' },
  { text: '06 · Create your first domain', link: '/06-first-domain' },
  { text: '07 · Confirm you are done', link: '/07-verify' },
  { text: '08 · Domain contributor', link: '/08-getting-started-contributor' },
  { text: '09 · Worked example', link: '/09-worked-example-salesforce' },
  { text: '90 · Troubleshooting', link: '/90-troubleshooting' },
];

const operate: DefaultTheme.SidebarItem[] = [
  { text: 'Update Studio', link: '/update' },
  { text: 'Roll back a release', link: '/rollback' },
  { text: 'Cloud installer', link: '/cloud-installer' },
];

const latestRelease: DefaultTheme.SidebarItem[] = [
  { text: 'Release notes', link: '/release' },
];

export default defineConfig({
  title: 'VibeData Studio Operator Guide',
  description: 'Install, operate, and troubleshoot a VibeData Studio deployment.',
  // GitHub Pages project site for accelerate-data/vibedata-official.
  base: '/vibedata-official/',
  // VitePress only treats index.md as the root route; rewrite README.md onto it so
  // the repository-view README is also the site index.
  rewrites: { 'README.md': 'index.md' },
  // Release notes arrive as raw model-generated text in the generated release page.
  // Disable raw HTML so a crafted PR title or body cannot inject markup onto the
  // Pages origin; Markdown syntax still renders. No page uses raw HTML.
  markdown: { html: false },

  themeConfig: {
    nav: [
      { text: 'Getting started', link: '/' },
      { text: 'Operate', link: '/update' },
      ...(hasReleasePage ? [{ text: 'Release notes', link: '/release' }] : []),
    ],
    sidebar: [
      { text: 'Getting started', items: gettingStarted },
      { text: 'Operate', items: operate },
      ...(hasReleasePage ? [{ text: 'Latest release', items: latestRelease }] : []),
    ],
    socialLinks: [{ icon: 'github', link: 'https://github.com/accelerate-data/vibedata-official' }],
  },
});
