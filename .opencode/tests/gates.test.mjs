import assert from "node:assert/strict"
import { test } from "node:test"
import plugin from "../plugins/samwise-gates/index.ts"

async function hooks() {
  const registered = new Map()
  const domain = (prefix) => ({ hook: async (name, fn) => registered.set(prefix + "." + name, fn) })
  await plugin.setup({
    permission: domain("permission"),
    tool: domain("tool"),
    session: domain("session"),
  })
  return registered
}

test("v2 hooks register at the right seams", async () => {
  const h = await hooks()
  for (const name of ["permission.evaluate", "tool.execute.after", "session.context", "session.compaction"]) {
    assert.equal(typeof h.get(name), "function", name)
  }
})

test("destructive commands denied; safe inspection allowed", async () => {
  const h = await hooks()
  for (const command of ["rm -rf /tmp/work", "git reset --hard HEAD", "git clean -fd", "sudo mkfs.ext4 /dev/sda"]) {
    const event = { action: "shell", resources: [command], effect: "ask" }
    await h.get("permission.evaluate")(event)
    assert.equal(event.effect, "deny", command)
  }
  const safe = { action: "shell", resources: ["git status --short"], effect: "allow" }
  await h.get("permission.evaluate")(safe)
  assert.equal(safe.effect, "allow")
})

test("protected paths denied", async () => {
  const h = await hooks()
  const event = { action: "edit", resources: ["/home/droid/samwise/docs/CONTEXT.md"], effect: "ask" }
  await h.get("permission.evaluate")(event)
  assert.equal(event.effect, "deny")
})

test("context and compaction preserve source and evidence instructions", async () => {
  const h = await hooks()
  for (const hook of ["session.context", "session.compaction"]) {
    const event = { system: [] }
    await h.get(hook)(event)
    assert.equal(event.system.length, 1)
    assert.equal(event.system[0].type, "text")
  }
})
