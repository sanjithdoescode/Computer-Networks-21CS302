const puppeteer = require("puppeteer-core");
const fs = require("fs");
const path = require("path");
const crypto = require("crypto");

const files = [
  { prefix: "u1_short", file: "UNIT - 1/short_questions_answers.md" },
  { prefix: "u1_long", file: "UNIT - 1/long_questions_answers.md" },
  { prefix: "u2_long", file: "UNIT - 2/long_questions_answers.md" },
  { prefix: "u3_long", file: "UNIT - 3/long_questions_answers.md" },
  { prefix: "u4_long", file: "UNIT - 4/long_questions_answers.md" },
  { prefix: "u5_long", file: "UNIT - 5/long_questions_answers.md" }
];

const diagramsDir = path.resolve(__dirname, "diagrams");
if (!fs.existsSync(diagramsDir)) {
  fs.mkdirSync(diagramsDir, { recursive: true });
}

async function main() {
  console.log("Launching Chromium to render all Mermaid diagrams...");
  const browser = await puppeteer.launch({
    executablePath: "/usr/bin/chromium",
    args: ["--no-sandbox", "--disable-setuid-sandbox", "--disable-gpu"]
  });

  const page = await browser.newPage();
  const mermaidPath = path.resolve(__dirname, "node_modules/mermaid/dist/mermaid.min.js");
  const mermaidJs = fs.readFileSync(mermaidPath, "utf8");

  await page.setContent(`
    <!DOCTYPE html>
    <html>
      <head>
        <script>${mermaidJs}</script>
        <style>
          body { font-family: Inter, system-ui, -apple-system, sans-serif; }
        </style>
      </head>
      <body>
        <div id="diagram-container"></div>
      </body>
    </html>
  `);

  await page.evaluate(() => {
    mermaid.initialize({
      startOnLoad: false,
      securityLevel: "loose",
      theme: "neutral",
      themeVariables: {
        fontFamily: "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
        fontSize: "13px",
        primaryColor: "#eff6ff",
        primaryTextColor: "#0f172a",
        primaryBorderColor: "#3b82f6",
        lineColor: "#334155",
        secondaryColor: "#f0fdf4",
        secondaryBorderColor: "#16a34a",
        secondaryTextColor: "#0f172a",
        tertiaryColor: "#fefce8",
        tertiaryBorderColor: "#d97706",
        tertiaryTextColor: "#0f172a",
        noteBkgColor: "#fffbeb",
        noteTextColor: "#78350f",
        noteBorderColor: "#f59e0b",
        actorBkg: "#eff6ff",
        actorBorder: "#2563eb",
        actorTextColor: "#0f172a",
        signalColor: "#1e40af",
        signalTextColor: "#0f172a",
        labelBoxBkgColor: "#ffffff",
        labelBoxBorderColor: "#94a3b8",
        labelTextColor: "#0f172a",
        edgeLabelBackground: "#ffffff",
        clusterBkg: "#f8fafc",
        clusterBorder: "#cbd5e1"
      }
    });
  });

  const manifest = {};
  let totalCount = 0;
  let successCount = 0;
  let errorCount = 0;

  for (const { prefix, file } of files) {
    const fullPath = path.resolve(__dirname, "..", file);
    const content = fs.readFileSync(fullPath, "utf8");
    const regex = /```mermaid\n([\s\S]*?)```/g;
    let match;
    let index = 0;

    console.log(`Processing ${file}...`);

    while ((match = regex.exec(content)) !== null) {
      totalCount++;
      index++;
      const code = match[1].trim();
      const id = `${prefix}_${index}`;
      const hash = crypto.createHash("md5").update(code).digest("hex");

      const svgPath = path.join(diagramsDir, `${id}.svg`);

      try {
        const renderResult = await page.evaluate(async (diagramCode, domId) => {
          try {
            const { svg } = await mermaid.render("d_" + domId, diagramCode);
            return { ok: true, svg };
          } catch (err) {
            return { ok: false, error: err.message || String(err) };
          }
        }, code, `${id}_${Date.now()}`);

        if (renderResult.ok) {
          // Clean up and optimize SVG
          let svg = renderResult.svg;
          // Ensure viewBox is preserved and width/height are responsive
          if (!svg.includes("viewBox") && svg.includes("width=") && svg.includes("height=")) {
            const widthMatch = svg.match(/width="([\d\.]+)(?:px)?"/);
            const heightMatch = svg.match(/height="([\d\.]+)(?:px)?"/);
            if (widthMatch && heightMatch) {
              const w = widthMatch[1];
              const h = heightMatch[1];
              svg = svg.replace("<svg", `<svg viewBox="0 0 ${w} ${h}"`);
            }
          }
          // Make responsive
          svg = svg.replace(/<svg\b([^>]*)>/, (m, attrs) => {
            let newAttrs = attrs;
            if (!newAttrs.includes('style="')) {
              newAttrs += ' style="max-width: 100%; height: auto; display: block; margin: 0 auto;"';
            }
            return `<svg${newAttrs}>`;
          });

          fs.writeFileSync(svgPath, svg, "utf8");
          manifest[hash] = {
            id,
            file,
            index,
            svgPath: `${id}.svg`,
            size: svg.length
          };
          successCount++;
        } else {
          console.error(`Error rendering ${id} in ${file}:`, renderResult.error);
          errorCount++;
        }
      } catch (err) {
        console.error(`Puppeteer error rendering ${id}:`, err.message);
        errorCount++;
      }
    }
  }

  fs.writeFileSync(
    path.join(diagramsDir, "manifest.json"),
    JSON.stringify(manifest, null, 2),
    "utf8"
  );

  console.log(`\n==========================================`);
  console.log(`Render complete!`);
  console.log(`Total diagrams: ${totalCount}`);
  console.log(`Successfully rendered: ${successCount}`);
  console.log(`Errors: ${errorCount}`);
  console.log(`Saved to: ${diagramsDir}`);
  console.log(`==========================================\n`);

  await browser.close();
}

main().catch(err => {
  console.error("Fatal error:", err);
  process.exit(1);
});
