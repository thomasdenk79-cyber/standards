[CmdletBinding(PositionalBinding = $false)]
param(
    [Parameter(Mandatory)]
    [ValidateSet("siemens", "ollama", "llama-cpp")]
    [string]$Provider,

    [Parameter(Mandatory)]
    [string]$Model,

    [Parameter(Mandatory)]
    [string]$Owner,

    [Parameter(ValueFromRemainingArguments)]
    [string[]]$WorkerCommand
)

$runtime = Join-Path $PSScriptRoot "ai_runtime.py"
if ($WorkerCommand.Count -eq 0) {
    throw "Pass the worker command after --, for example: -- opencode -m ollama/qwen3-coder:30b"
}

if ($WorkerCommand[0] -eq "--") {
    $WorkerCommand = $WorkerCommand[1..($WorkerCommand.Count - 1)]
}

if ($Provider -eq "siemens") {
    & python $runtime usage-record --runtime wrapper --provider $Provider --model $Model
    if ($LASTEXITCODE -ne 0) {
        exit $LASTEXITCODE
    }
    & $WorkerCommand[0] $WorkerCommand[1..($WorkerCommand.Count - 1)]
    exit $LASTEXITCODE
}

& python $runtime run --provider $Provider --model $Model --owner $Owner -- @WorkerCommand
exit $LASTEXITCODE
