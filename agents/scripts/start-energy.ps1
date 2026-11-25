# Demenova - start Claude Code in ENERGY-SAVING mode.
# Forces every subagent (custom, built-in and ECC) onto Claude Opus 5.5 and runs the
# main session on Opus 5.5. Agent files are not touched; their effort setting still applies.
# Requires Claude Code v2.1.257 or later (CLAUDE_CODE_SUBAGENT_MODEL_FORCE).
# Run from the repository root:
#   powershell -ExecutionPolicy Bypass -File .\scripts\start-energy.ps1
#
# The alias "opus" resolves to the newest Opus your account allows (Opus 5.5).
# To pin the exact model instead, replace "opus" with "claude-opus-5-5" on both lines.
$env:CLAUDE_CODE_SUBAGENT_MODEL = "opus"
$env:CLAUDE_CODE_SUBAGENT_MODEL_FORCE = "1"
$env:PYTHONUTF8 = "1"

Write-Host "Demenova: ENERGY mode (Opus 5.5 for main session and all subagents)" -ForegroundColor Yellow
claude --model opus @args
