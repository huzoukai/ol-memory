const express = require("express");
const fs = require("fs");
const path = require("path");
const { spawnSync } = require("child_process");

const app = express();
const port = process.env.OFFICE_MEMORY_API_PORT || 4177;
const skillRoot = path.resolve(__dirname, "../..");
const dataDir = path.resolve(process.env.OFFICE_MEMORY_DATA || path.join(process.cwd(), "OL-Memory"));

const files = [
  "profile/personal-profile.md",
  "profile/company-profile.md",
  "profile/role-and-responsibilities.md",
  "profile/work-preferences.md",
  "knowledge/project-cases.md",
  "knowledge/capabilities.md",
  "knowledge/forbidden-claims.md",
  "knowledge/leader-shared-materials.md",
  "knowledge/leader-talking-points.md",
  "style/writing-style.md",
  "style/favorite-phrases.md",
  "style/disliked-phrases.md",
  "style/audience-profiles.md",
  "style/leader-signals.md",
  "scenarios/bid-materials.md",
  "scenarios/weekly-report.md",
  "scenarios/monthly-report.md",
  "scenarios/company-intro.md",
  "scenarios/project-summary.md",
  "scenarios/meeting-minutes.md",
  "learning/learning-inbox.md",
  "learning/learning-log.md",
  "learning/rejected-learning.md"
];

app.use(express.json({ limit: "2mb" }));
app.use((req, res, next) => {
  const origin = req.headers.origin || "";
  if (/^http:\/\/127\.0\.0\.1:\d+$/.test(origin) || /^http:\/\/localhost:\d+$/.test(origin)) {
    res.setHeader("Access-Control-Allow-Origin", origin);
  }
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");
  res.setHeader("Access-Control-Allow-Methods", "GET,POST,OPTIONS");
  if (req.method === "OPTIONS") return res.sendStatus(204);
  next();
});

function safePath(rel) {
  if (!files.includes(rel)) throw new Error("不支持编辑这个文件 / Unsupported file");
  const full = path.resolve(dataDir, rel);
  if (!full.startsWith(dataDir)) throw new Error("文件路径无效 / Invalid path");
  return full;
}

function runScript(name, args = []) {
  const script = path.join(skillRoot, "scripts", name);
  return spawnSync("python3", [script, ...args], { encoding: "utf-8" });
}

app.get("/api/state", (req, res) => {
  const exists = fs.existsSync(dataDir);
  const docs = {};
  for (const rel of files) {
    const full = path.join(dataDir, rel);
    docs[rel] = fs.existsSync(full) ? fs.readFileSync(full, "utf-8") : "";
  }
  let validation = null;
  if (exists) {
    const result = runScript("validate_memory.py", ["--data-dir", dataDir]);
    try {
      validation = JSON.parse(result.stdout);
    } catch {
      validation = {
        status: "ERROR",
        issues: [`资料库校验失败，请查看脚本输出 / Memory validation failed; check script output: ${result.stderr || result.stdout}`]
      };
    }
  }
  res.json({ dataDir, exists, files, docs, validation });
});

app.post("/api/init", (req, res) => {
  const args = ["--data-dir", dataDir];
  const result = runScript("init_workspace.py", args);
  res.status(result.status === 0 ? 200 : 500).json({
    stdout: result.stdout,
    stderr: result.stderr,
    error: result.status === 0 ? "" : `初始化失败 / Initialization failed: ${result.stderr || result.stdout}`
  });
});

app.post("/api/file", (req, res) => {
  try {
    const full = safePath(req.body.path);
    fs.mkdirSync(path.dirname(full), { recursive: true });
    fs.writeFileSync(full, req.body.content || "", "utf-8");
    res.json({ status: "saved", path: req.body.path });
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
});

app.post("/api/export-trae", (req, res) => {
  const out = path.resolve(req.body.outDir || path.join(path.dirname(dataDir), "trae-pack"));
  const result = runScript("export_trae_pack.py", ["--data-dir", dataDir, "--out-dir", out]);
  res.status(result.status === 0 ? 200 : 500).json({
    stdout: result.stdout,
    stderr: result.stderr,
    outDir: out,
    error: result.status === 0 ? "" : `导出失败 / Export failed: ${result.stderr || result.stdout}`
  });
});

app.listen(port, "127.0.0.1", () => {
  console.log(`Office Memory API running at http://127.0.0.1:${port}`);
  console.log(`Data dir: ${dataDir}`);
});
