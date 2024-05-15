$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")
if (!$isAdmin) {
    Write-Host "Please run this script as administrator."
    exit
}

if (Get-Command ffmpeg -ErrorAction SilentlyContinue) {
    Write-Host "ffmpeg is already installed."
    exit
}

if (!(Get-Command 7z -ErrorAction SilentlyContinue)) {
    Write-Host "7zip is not installed. Please install it first."
}

Write-Host "Downloading ffmpeg..."
Invoke-WebRequest -Uri "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.7z" -OutFile "ffmpeg.7z"

Write-Host "Extracting..."
7z x -y -o"C:\" "ffmpeg.7z"

$ffmpegFolder = Get-ChildItem -Path "C:\" -Filter "ffmpeg-*" -Directory
Rename-Item -Path $ffmpegFolder -NewName "ffmpeg"

Write-Host "Adding ffmpeg to PATH..."
$envPath = [Environment]::GetEnvironmentVariable("PATH", "Machine")
[Environment]::SetEnvironmentVariable("PATH", $envPath + ";C:\ffmpeg\bin", "Machine")

Write-Host "ffmpeg is installed. Following commands are available: ffmpeg, ffplay, ffprobe"