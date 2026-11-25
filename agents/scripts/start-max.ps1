# Demenova - start Claude Code in MAX mode.
# Main session on Claude Fable 5.2; every custom subagent uses its own frontmatter
# (model: fable, effort: max). Run from the repository root:
#   powershell -ExecutionPolicy Bypass -File .\scripts\start-max.ps1
#
# Clears any energy-mode override left in this PowerShell window.
Remove-Item Env:CLAUDE_CODE_SUBAGENT_MODEL -ErrorAction SilentlyContinue
Remove-Item Env:CLAUDE_CODE_SUBAGENT_MODEL_FORCE -ErrorAction SilentlyContinue
$env:PYTHONUTF8 = "1"

Write-Host "Demenova: MAX mode (Fable 5.2 for main session and all custom agents)" -ForegroundColor Green
claude --model fable @args
