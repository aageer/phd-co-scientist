#!/usr/bin/env node
/** Fail-open shell guard. Asks on obvious dual-use / exploit tooling. */
import { stdin } from "node:process";

const RESTRICTED =
  /msfvenom|exploit-db|nmap\s+-sS|hashcat|aircrack|wget\s+.*malware/i;

async function readStdin() {
  const chunks = [];
  for await (const chunk of stdin) chunks.push(chunk);
  return Buffer.concat(chunks).toString("utf8");
}

async function main() {
  try {
    const raw = await readStdin();
    const payload = raw.trim() ? JSON.parse(raw) : {};
    const cmd = payload.command || payload.tool_input?.command || JSON.stringify(payload);
    if (RESTRICTED.test(String(cmd))) {
      console.log(
        JSON.stringify({
          permission: "ask",
          user_message: "Shell command looks like offensive tooling. Confirm before running.",
        }),
      );
      return;
    }
    console.log(JSON.stringify({ permission: "allow" }));
  } catch {
    console.log(JSON.stringify({ permission: "allow" }));
  }
}

main();
