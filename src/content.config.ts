import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const projects = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/projects' }),
  schema: ({ image }) =>
    z.object({
      // Identity
      id: z.string().regex(/^P-\d{3}$/),
      title: z.string(),
      tagline: z.string().max(120),

      // Classification
      tier: z.enum(['featured', 'standard', 'compact']),
      year: z.number().int().min(2015).max(2030),
      domain: z.enum([
        'Fintech',
        'Social Impact',
        'ERP',
        'Government',
        'E-commerce',
        'Education',
        'Healthcare',
        'Internal Tools',
      ]),

      // Role
      roles: z
        .array(
          z.enum([
            'Dev Lead',
            'Backend Developer',
            'Fullstack Developer',
            'Frontend Developer',
            'Mobile Developer',
            'System Analyst',
          ]),
        )
        .min(1),
      teamSize: z.number().int().optional(),
      duration: z.string().optional(),
      client: z.string().optional(),

      // Technical
      stack: z.array(z.string()).min(1),
      architecture: z.string().optional(),

      // Media
      cover: image(),
      screenshots: z
        .array(
          z.object({
            src: image(),
            caption: z.string(),
          }),
        )
        .default([]),

      // Links
      liveUrl: z.string().url().optional(),
      repoUrl: z.string().url().optional(),

      // Impact
      metrics: z
        .array(
          z.object({
            label: z.string(),
            value: z.string(),
          }),
        )
        .default([]),

      // Control
      featured: z.boolean().default(false),
      draft: z.boolean().default(false),
      order: z.number().default(999),

      // Extraction guard — present only while a file is still auto-generated
      _generated: z.boolean().optional(),
      _sourceSlide: z.number().optional(),
      _extractedAt: z.string().optional(),
    }),
});

export const collections = { projects };
