// Content collections — Astro v6+ loader API.
// Schema is the contract every JSON file must satisfy. Malformed content
// fails the build loudly rather than shipping a broken page.
import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

// ─── Landing page (src/content/landing.json) ────────────────────────────
// The thin 10-second pitch. Public, indexed, no role links.
const landing = defineCollection({
  loader: glob({ pattern: 'landing.json', base: './src/content' }),
  schema: z.object({
    name: z.string(),
    intro: z.string(),
    positioningLine: z.string(),
    contact: z.object({
      email: z.string(),
      github: z.string(),
      phone: z.string().optional(),
    }),
  }),
});

// ─── Per-role pages (src/content/roles/<slug>.json) ─────────────────────
// One file per role. Unlisted (noindex). Rich roles use the full template;
// stubs use the lighter "Selected Work" template.
const project = z.object({
  title: z.string(),
  focus: z.string(),
  techStack: z.array(z.string()),
  repoUrl: z.string().url(),
  projectKey: z.string(),
  image: z.string().optional(),
  videoPlaceholder: z.string().optional(),
  demoData: z.record(z.string(), z.unknown()).optional(),
});

const certification = z.object({
  name: z.string(),
  issuer: z.string().optional(),
  issueDate: z.string().optional(),
  url: z.string().url().optional(),
});

const roles = defineCollection({
  loader: glob({ pattern: '**/*.json', base: './src/content/roles' }),
  schema: z.object({
    slug: z.string(),
    roleCategory: z.string(),
    isRich: z.boolean(),
    expertNarrative: z.string().optional(),
    professionalSummary: z.string(),
    skills: z.array(z.string()).optional(),
    certifications: z.array(certification).optional(),
    projects: z.array(project),
  }),
});

export const collections = { landing, roles };
