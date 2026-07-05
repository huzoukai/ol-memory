import React, { useEffect, useState } from "react";
import { createRoot } from "react-dom/client";
import { AlertTriangle, BookOpen, Check, Download, FileText, Play, RefreshCw, Save, Shield, Sparkles, Terminal } from "lucide-react";
import "./styles.css";

const groups = [
  { id: "dashboard", label: "首页", files: [] },
  { id: "profile", label: "我的档案", files: ["profile/personal-profile.md", "profile/role-and-responsibilities.md", "profile/work-preferences.md"] },
  { id: "company", label: "公司资料", files: ["profile/company-profile.md", "knowledge/capabilities.md", "knowledge/forbidden-claims.md"] },
  { id: "cases", label: "项目案例", files: ["knowledge/project-cases.md"] },
  { id: "style", label: "写作风格", files: ["style/writing-style.md", "style/favorite-phrases.md", "style/disliked-phrases.md", "style/audience-profiles.md"] },
  { id: "leader", label: "上级偏好", files: ["knowledge/leader-shared-materials.md", "style/leader-signals.md", "knowledge/leader-talking-points.md"] },
  { id: "scenarios", label: "场景模板", files: ["scenarios/bid-materials.md", "scenarios/weekly-report.md", "scenarios/monthly-report.md", "scenarios/company-intro.md", "scenarios/project-summary.md", "scenarios/meeting-minutes.md"] },
  { id: "learning", label: "学习收件箱", files: ["learning/learning-inbox.md", "learning/learning-log.md", "learning/rejected-learning.md"] },
  { id: "settings", label: "设置", files: [] }
];

const api = import.meta.env.VITE_OFFICE_MEMORY_API || "http://127.0.0.1:4177/api";

const statusLabels = {
  HEALTHY: "健康 / HEALTHY",
  WARNING: "警告 / WARNING",
  BLOCKED: "阻塞 / BLOCKED",
  ERROR: "错误 / ERROR",
  UNKNOWN: "未知 / UNKNOWN",
  "NOT INITIALIZED": "未初始化 / NOT INITIALIZED"
};

async function parseJsonOrError(res) {
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    throw new Error(data.error || `请求失败 / Request failed: HTTP ${res.status}`);
  }
  return data;
}

function App() {
  const [state, setState] = useState(null);
  const [active, setActive] = useState("dashboard");
  const [selected, setSelected] = useState("");
  const [content, setContent] = useState("");
  const [message, setMessage] = useState("");
  const [loadError, setLoadError] = useState("");

  async function load() {
    try {
      const res = await fetch(`${api}/state`);
      const data = await res.json();
      setState(data);
      setLoadError("");
      const currentFiles = groups.find((g) => g.id === active)?.files || [];
      const next = selected || currentFiles[0] || "";
      setSelected(next);
      setContent(next ? data.docs[next] || "" : "");
    } catch (error) {
      setLoadError("本地资料服务没有连接上。请重新运行启动命令后刷新页面。/ Local memory service is not connected. Run the launcher again, then refresh this page.");
    }
  }

  useEffect(() => { load(); }, []);

  const group = groups.find((g) => g.id === active);
  const score = state?.validation?.completeness_score ?? 0;
  const status = state?.validation?.status || (state?.exists ? "UNKNOWN" : "NOT INITIALIZED");

  async function init() {
    try {
      setMessage("正在初始化 / Initializing...");
      const res = await fetch(`${api}/init`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) });
      await parseJsonOrError(res);
      await load();
      setMessage("已初始化 OL-Memory / OL-Memory initialized");
    } catch (error) {
      setMessage(error.message || "初始化失败 / Initialization failed");
    }
  }

  async function save() {
    if (!selected) return;
    try {
      const res = await fetch(`${api}/file`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ path: selected, content }) });
      await parseJsonOrError(res);
      await load();
      setMessage(`已保存 / Saved: ${selected}`);
    } catch (error) {
      setMessage(error.message || "保存失败 / Save failed");
    }
  }

  async function exportTrae() {
    try {
      const res = await fetch(`${api}/export-trae`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) });
      const data = await parseJsonOrError(res);
      setMessage(`已导出 Trae 包 / Trae pack exported: ${data.outDir}`);
    } catch (error) {
      setMessage(error.message || "导出失败 / Export failed");
    }
  }

  function chooseTab(id) {
    setActive(id);
    const nextFiles = groups.find((g) => g.id === id)?.files || [];
    const next = nextFiles[0] || "";
    setSelected(next);
    setContent(next && state ? state.docs[next] || "" : "");
  }

  function chooseFile(file) {
    setSelected(file);
    setContent(state?.docs[file] || "");
  }

  return (
    <main className="app">
      {state && !state.exists && !loadError ? (
        <FirstRun state={state} init={init} />
      ) : (
      <>
        <aside className="sidebar">
        <div className="brand">
          <div className="mark"><Sparkles size={18} /></div>
          <div>
            <strong>办公室记忆助手</strong>
            <span>驯化你的 AI 同事</span>
          </div>
        </div>
        <nav>
          {groups.map((item) => (
            <button key={item.id} className={active === item.id ? "active" : ""} onClick={() => chooseTab(item.id)}>{item.label}</button>
          ))}
        </nav>
      </aside>

      <section className="workspace">
        <header>
          <div>
            <p className="path">{state?.dataDir || "OL-Memory"}</p>
            <h1>{group?.label}</h1>
          </div>
          <div className="actions">
            <button title="刷新" onClick={load}><RefreshCw size={18} /></button>
            <button title="保存" onClick={save} disabled={!selected}><Save size={18} /></button>
            <button title="导出 Trae 包" onClick={exportTrae}><Download size={18} /></button>
          </div>
        </header>

        {active === "dashboard" && (
          <Dashboard state={state} score={score} status={status} init={init} exportTrae={exportTrae} loadError={loadError} />
        )}

        {active === "settings" && (
          <div className="panel">
            <h2>设置</h2>
            <p>数据目录：{state?.dataDir}</p>
            <div className="button-row">
              <button onClick={init}>初始化 OL-Memory</button>
              <button onClick={exportTrae}>导出 Trae 使用包</button>
            </div>
            <CommandBox dataDir={state?.dataDir || "/absolute/path/to/OL-Memory"} />
            <p className="hint">Codex 使用：在项目中说“根据 OL-Memory 帮我写材料”。Trae 使用：导出后先阅读 TRAE_SYSTEM_PROMPT.md。</p>
          </div>
        )}

        {group?.files?.length > 0 && (
          <div className="editor-layout">
            <div className="file-list">
              {group.files.map((file) => (
                <button key={file} className={selected === file ? "active" : ""} onClick={() => chooseFile(file)}><FileText size={15} />{file}</button>
              ))}
            </div>
            <textarea value={content} onChange={(event) => setContent(event.target.value)} spellCheck={false} />
          </div>
        )}

        {message && <div className="toast"><Check size={16} />{message}</div>}
      </section>
      </>
      )}
    </main>
  );
}

function FirstRun({ state, init }) {
  return (
    <section className="first-run">
      <div className="first-run-inner">
        <div className="brand first-run-brand">
          <div className="mark"><Sparkles size={18} /></div>
          <div>
            <strong>OL-Memory</strong>
            <span>Office Life Memory · 你的本地职场记忆库</span>
          </div>
        </div>
        <div className="first-run-hero">
          <p className="path">{state?.dataDir || "OL-Memory"}</p>
          <h1>开始初始化 / Start Setup</h1>
          <p>安装 Skill 后，对 Codex 说“开始启动 OL”。Codex 会先问几个必填问题，写入第一版档案，再打开这个页面让你检查。</p>
          <p>After installing the Skill, tell Codex: "开始启动 OL". Codex will ask required intake questions, write the starter profile, then open this page for review.</p>
          <button onClick={init}>初始化 OL-Memory</button>
        </div>
        <StarterGuide dataDir={state?.dataDir || "OL-Memory"} />
      </div>
    </section>
  );
}

function Dashboard({ state, score, status, init, exportTrae, loadError }) {
  const issues = state?.validation?.issues || [];
  const warnings = state?.validation?.warnings || [];
  const details = state?.validation?.completeness_detail || {};
  return (
    <div className="dashboard">
      {loadError && (
        <section className="panel alert-panel">
          <h2>本地服务未连接 / Local Service Disconnected</h2>
          <p>{loadError}</p>
          <CommandBox dataDir="/absolute/path/to/OL-Memory" />
        </section>
      )}
      <section className="score-card">
        <div>
          <span className="eyebrow">资料完整度</span>
          <strong>{score}%</strong>
          <p>{state?.validation?.next_suggestion || "先初始化资料库，然后补充个人、公司和案例资料。/ Initialize the library first, then fill profile, company, and case files."}</p>
        </div>
        <div className={`status ${status.toLowerCase()}`}><Shield size={17} />{statusLabels[status] || status}</div>
      </section>
      <section className="grid">
        {Object.entries(details).map(([name, item]) => (
          <div className="panel" key={name}>
            <span className="eyebrow">{name}</span>
            <h2>{item.score}/{item.max}</h2>
          </div>
        ))}
      </section>
      <section className="panel">
        <h2>风险 / 缺失提醒 / Risks & Missing Info</h2>
        {[...issues, ...warnings].length === 0 ? <p>暂无明显阻塞。/ No obvious blockers.</p> : [...issues, ...warnings].slice(0, 8).map((item) => <p className="warning" key={item}><AlertTriangle size={15} />{item}</p>)}
      </section>
      <section className="panel">
        <h2>快速操作</h2>
        <div className="button-row">
          <button onClick={init}>初始化 OL-Memory</button>
          <button onClick={exportTrae}>导出 Trae 包</button>
        </div>
      </section>
      <StarterGuide dataDir={state?.dataDir || "OL-Memory"} />
    </div>
  );
}

function StarterGuide({ dataDir }) {
  return (
    <section className="guide">
      <div className="guide-item">
        <BookOpen size={18} />
        <div>
          <h2>第一次怎么开始 / First start</h2>
          <p>先安装 Skill，然后对 Codex 说：“开始启动 OL”。Agent 会先问称呼、岗位、公司、案例、禁忌和风格，再帮你启动页面。</p>
          <p>Install the Skill, then tell Codex: "开始启动 OL". The Agent asks for name, role, company, one case, boundaries, and style before opening the page.</p>
        </div>
      </div>
      <div className="guide-item">
        <FileText size={18} />
        <div>
          <h2>前期怎么录入档案 / Profile intake</h2>
          <p>先在 Agent 聊天框回答必填问题。页面打开后，只需要检查和补充，不用从零开始填。</p>
          <p>Answer the required questions in the Agent chat first. After the page opens, review and refine instead of starting from zero.</p>
        </div>
      </div>
      <div className="guide-item">
        <Play size={18} />
        <div>
          <h2>正式怎么使用 / Daily use</h2>
          <p>日常就在 Agent 聊天框输入信息或任务。例如：根据 OL-Memory 写周报；或者：上级转发了这篇文章，帮我记住偏好。</p>
          <p>Daily use happens in the Agent chat box. Ask for drafts from OL-Memory, or paste new facts, corrections, and leader-shared material there.</p>
        </div>
      </div>
      <div className="guide-item">
        <Shield size={18} />
        <div>
          <h2>能帮你做什么 / What it can do</h2>
          <p>投标材料、公司介绍、周报、月报述职、项目总结、会议纪要转材料、去 AI 味、结合上级转发内容写出上级更容易接受的角度。</p>
          <p>Bid copy, company intros, reports, reviews, project summaries, meeting-note materials, style cleanup, and leader-signal-aware writing.</p>
        </div>
      </div>
      <div className="guide-item">
        <Terminal size={18} />
        <div>
          <h2>关机后怎么再打开 / Restart</h2>
          <p>数据不会丢，只是本地页面服务停了。重新运行下面命令，再打开终端打印出来的地址。</p>
          <p>Your data stays on disk. Only the local UI server stops. Run this command again and open the URL printed in Terminal.</p>
          <CommandBox dataDir={dataDir} />
        </div>
      </div>
    </section>
  );
}

function CommandBox({ dataDir }) {
  const command = `python3 ~/.codex/skills/office-memory-assistant/scripts/launch_ui.py --data-dir ${dataDir} --open`;
  async function copy() {
    await navigator.clipboard.writeText(command);
  }
  return (
    <div className="command-box">
      <code>{command}</code>
      <button onClick={copy}>复制</button>
    </div>
  );
}

createRoot(document.getElementById("root")).render(<App />);
