import { defineCollection, z } from "astro:content";
import { glob } from "astro/loaders";

const journal = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/journal" }),
  schema: z.object({
    date: z.coerce.date(),
    title: z
      .string()
      .nullish()
      .transform((v) => (v ?? "").trim()),
    tags: z.array(z.string()).default([]),
    mood: z.string().optional(),
    cover: z.string().optional(),
    draft: z.boolean().default(false),
  }),
});

const moments = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/moments" }),
  schema: z.object({
    date: z.coerce.date(),
    title: z
      .string()
      .nullish()
      .transform((v) => (v ?? "").trim()),
    text: z
      .string()
      .nullish()
      .transform((v) => (v ?? "").trim()),
    tags: z.array(z.string()).default([]),
    photos: z
      .array(
        z.object({
          src: z.string(),
          w: z.number(),
          h: z.number(),
        })
      )
      .default([]),
    draft: z.boolean().default(false),
  }),
});

export const collections = { journal, moments };
