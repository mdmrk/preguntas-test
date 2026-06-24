## Development

```bash
bun install
bun run dev        # dev server at http://localhost:5173
```

Other scripts:

```bash
bun run build      # generate sitemap + type-check + production build to dist/
bun run preview    # serve the production build at http://localhost:4173
bun run lint       # biome check
bun run lint:fix   # biome check + autofix
bun run format     # biome format --write
```

## Contributing

Each subject is a JSON file in `src/data/`. The filename (without `.json`) is the test **id** used in routes (`/test/<id>`).

### Question format

A file is an array of question objects:

```jsonc
{
  "id": 1, // unique number within the file
  "question": "Question text", // supports KaTeX math and code blocks
  "options": ["A", "B", "C", "D"], // 2+ choices
  "answer": 0, // 0-based index of the correct option
  "explanation": "Why it's right.", // optional
  "image": "gpi001.png", // optional, see below
  "tags": ["Enero 2025"], // optional, see below
}
```

Only `id`, `question`, `options` and `answer` are required.

### Adding a new subject

1. Create `src/data/<id>.json` with your array of questions.
2. Add a button for it in `src/views/HomeView.vue` (a `<MainButton id="<id>" ... />`). The `id` must match the filename.

### Images

1. Drop the image in `public/test/` (e.g. `public/test/gpi001.png`).
2. Reference just the filename in the question's `"image"` field. It's served from `/test/<filename>`.

### Year filtering (tags)

For subjects with per-year exams, tag each question with its exam period (e.g. `"tags": ["Enero 2025"]`) and add the years to the button:

```html
<MainButton id="redes" text="REDES" years="2026;2025;2024" />
```

Visiting `/test/<id>/<year>` shows only questions whose tags contain that year string.
