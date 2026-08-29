#!/usr/bin/env node
/**
 * Fail-open ethics hint on the incoming prompt. Never blocks the agent
 * because this script crashed. Emits permission=ask on restricted cues.
 */
import { stdin } from "node:process";

const RESTRICTED =
  /bioweapon|pathogen enhance|nerve agent|csam|ransomware|undetectable phishing|weaponize/i;

async function readStdin() {
  const chunks = [];
  for await (const chunk of stdin) chunks.push(chunk);
  return Buffer.concat(chunks).toString("utf8");
}

async function main() {
  try {
    const raw = await readStdin();
    const payload = raw.trim() ? JSON.parse(raw) : {};
    const text = JSON.stringify(payload);
    if (RESTRICTED.test(text)) {
      console.log(
        JSON.stringify({
          permission: "ask",
          user_message:
            "Prompt matches a restricted research category. Confirm this is legitimate CS research before continuing.",
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
