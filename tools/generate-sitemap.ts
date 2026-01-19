import { readdir, writeFile } from "node:fs/promises"
import { join, parse } from "node:path"

const DATA_DIR = join(process.cwd(), "src", "data")
const PUBLIC_DIR = join(process.cwd(), "public")
const BASE_URL = "https://preguntas-test.vercel.app"

async function main() {
  console.log("Generating sitemap.xml and robots.txt...")

  try {
    const files = await readdir(DATA_DIR)
    const jsonFiles = files.filter((f) => f.endsWith(".json"))
    const routes = ["/"]

    for (const file of jsonFiles) {
      const id = parse(file).name
      routes.push(`/test/${id}`)
      routes.push(`/repository/${id}`)
    }

    const sitemap = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${routes
  .map(
    (route) => `  <url>
    <loc>${BASE_URL}${route}</loc>
    <changefreq>weekly</changefreq>
    <priority>${route === "/" ? "1.0" : "0.8"}</priority>
  </url>`
  )
  .join("\n")}
</urlset>`

    await writeFile(join(PUBLIC_DIR, "sitemap.xml"), sitemap)
    console.log(`Generated sitemap.xml with ${routes.length} URLs.`)

    const robots = `User-agent: *
Allow: /
Sitemap: ${BASE_URL}/sitemap.xml
`
    await writeFile(join(PUBLIC_DIR, "robots.txt"), robots)
    console.log("Generated robots.txt")
  } catch (error) {
    console.error("Error generating sitemap:", error)
    process.exit(1)
  }
}

main()
