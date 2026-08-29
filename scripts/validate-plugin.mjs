#!/usr/bin/env node
import { readFileSync, readdirSync, existsSync, statSync } from "node:fs";
import { join, extname } from "node:path";

const root = process.cwd();
let failed = 0;

function fail(msg) {
  console.error("FAIL", msg);
  failed += 1;
}

function ok(msg) {
  console.log("OK  ", msg);
}

function read(rel) {
  return readFileSync(join(root, rel), "utf8");
}

function frontmatter(text) {
  if (!text.startsWith("---\n")) return null;
  const end = text.indexOf("\n---\n", 4);
  if (end < 0) return null;
  const block = text.slice(4, end);
  const out = {};
  for (const line of block.split("\n")) {
    const m = line.match(/^([a-zA-Z0-9_]+):\s*(.*)$/);
    if (m) out[m[1]] = m[2].replace(/^["']|["']$/g, "");
  }
  return out;
}

const manifestPath = ".cursor-plugin/plugin.json";
if (!existsSync(join(root, manifestPath))) fail("missing " + manifestPath);
else {
  const man = JSON.parse(read(manifestPath));
  if (!/^[a-z0-9](?:[a-z0-9.-]*[a-z0-9])?$/.test(man.name)) fail("bad plugin name");
  else ok("plugin name " + man.name);
  if (man.logo && man.logo.includes("..")) fail("logo path escapes plugin");
  if (man.logo && !existsSync(join(root, man.logo))) fail("logo missing: " + man.logo);
  else ok("logo " + man.logo);
}

for (const dir of ["skills", "agents", "commands", "rules"]) {
  if (!existsSync(join(root, dir))) fail("missing " + dir);
}

const skills = readdirSync(join(root, "skills")).filter((n) =>
  statSync(join(root, "skills", n)).isDirectory(),
);
for (const name of skills) {
  const rel = `skills/${name}/SKILL.md`;
  if (!existsSync(join(root, rel))) {
    fail("missing " + rel);
    continue;
  }
  const fm = frontmatter(read(rel));
  if (!fm?.name || !fm?.description) fail(rel + " missing name/description");
  else if (fm.name !== name) fail(rel + " name != directory");
  else if (!fm.description.toLowerCase().includes("use when")) fail(rel + " description should start with Use when");
  else ok(rel);
}

for (const dir of ["agents", "commands"]) {
  for (const file of readdirSync(join(root, dir))) {
    if (![".md", ".mdc", ".markdown", ".txt"].includes(extname(file))) continue;
    const rel = `${dir}/${file}`;
    const fm = frontmatter(read(rel));
    if (!fm?.name || !fm?.description) fail(rel + " missing name/description");
    else ok(rel);
  }
}

for (const file of readdirSync(join(root, "rules"))) {
  const rel = `rules/${file}`;
  const fm = frontmatter(read(rel));
  if (!fm?.description) fail(rel + " missing description");
  else ok(rel);
}

const hooks = "hooks/hooks.json";
if (!existsSync(join(root, hooks))) fail("missing hooks");
else {
  const h = JSON.parse(read(hooks));
  for (const list of Object.values(h.hooks || {})) {
    for (const item of list) {
      const cmd = item.command.replace(/^\.\//, "");
      if (cmd.includes("..")) fail("hook escapes: " + cmd);
      if (!existsSync(join(root, cmd))) fail("hook missing: " + cmd);
      else ok("hook " + cmd);
    }
  }
}

if (failed) {
  console.error(`\n${failed} check(s) failed`);
  process.exit(1);
}
console.log("\nplugin ok");
