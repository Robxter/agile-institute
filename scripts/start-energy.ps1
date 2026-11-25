# Agile Institute - start Claude Code in ENERGY-SAVING mode.
# Forces every subagent (custom, built-in and ECC) onto Claude Opus 5.5 and runs the main session on Opus 5.5.
# Agent files are not touched; their effort setting still applies.
# Run from the repository root:
#   powershell -ExecutionPolicy Bypass -File .\scripts\start-energy.ps1
#
# To pin the exact model instead of the alias, replace "opus" with "claude-opus-5-5" on both lines.
$env:CLAUDE_CODE_SUBAGENT_MODEL = "opus"
$env:CLAUDE_CODE_SUBAGENT_MODEL_FORCE = "1"
$env:PYTHONUTF8 = "1"

Write-Host "Agile Institute: ENERGY mode (Opus 5.5 for main session and all subagents)" -ForegroundColor Yellow
claude --model opus @args
