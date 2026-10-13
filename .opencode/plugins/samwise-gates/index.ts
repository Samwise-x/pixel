import { Plugin } from "@opencode/plugin"

// OpenCode V2 policy: deterministic veto at the permission admission seam.
// Guard both shell requests and post-tool observability without relying on model instructions.
const destructive = /(^|[;&| ]+)(?:sudo\s+)?(?:rm\s+-[A-Za-z]*r[A-Za-z]*f|git\s+(?:reset\s+--hard|clean\s+-[A-Za-z]*f)|(?:mkfs(?:\.[A-Za-z0-9_-]+)?|dd)\s)/i
const protectedPaths = /(?:\/home\/droid\/samwise\/docs\/|\/\.ssh\/|\/etc\/sudoers)/i

export default Plugin.define({
  id: "samwise-gates",
  async setup(ctx) {
    await ctx.permission.hook("evaluate", (event) => {
      const resources = event.resources.join(" ")
      if (event.action === "shell" && (destructive.test(resources) || protectedPaths.test(resources))) {
        event.effect = "deny"
        event.message = "SAMWISE: command denied by execution policy"
      }
      if (event.action === "edit" && protectedPaths.test(resources)) {
        event.effect = "deny"
        event.message = "SAMWISE: protected namespace"
      }
    })
    await ctx.tool.hook("execute.after", (event) => {
      if (event.status === "error") {
        console.error("[samwise-gates] tool failure", event.tool, event.error.message)
      }
    })
    await ctx.session.hook("context", (event) => {
      event.system.push({
        type: "text",
        text: "Source policy: AGENTS.md. Confirm tests and repo status before proposing commits. Never promote an unverified artifact.",
      })
    })
    await ctx.session.hook("compaction", (event) => {
      event.system.push({
        type: "text",
        text: "Keep project invariants, unresolved verification steps, and current Git evidence in the compaction summary.",
      })
    })
  },
})
