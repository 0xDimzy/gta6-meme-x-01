// gta6-meme-x-01 entry program (Node 22, standard library only).
// The entry is the X post itself; this program only hands POST.json to the
// gate by copying it from the repository root to the output directory.
// The house reads the post from X and builds the dossier the judge sees.
//
// Local run, the way the grader does it:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

const botDir = process.env.MAKEFUN_BOT_DIR ?? '/bot';
const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const postPath = join(botDir, 'POST.json');

// Fail here, not at the gate, if POST.json is not a JSON object naming a url.
try {
  const post = JSON.parse(readFileSync(postPath, 'utf8')) as { url?: unknown };
  if (typeof post.url !== 'string' || post.url.length === 0) {
    throw new Error('POST.json has no "url" string');
  }
} catch (err) {
  console.error(`POST.json is not usable: ${(err as Error).message}`);
  process.exit(1);
}

mkdirSync(outputDir, { recursive: true });
try {
  copyFileSync(postPath, join(outputDir, 'POST.json'));
} catch (err) {
  console.error(`could not copy POST.json from ${botDir}: ${(err as Error).message}`);
  process.exit(1);
}
