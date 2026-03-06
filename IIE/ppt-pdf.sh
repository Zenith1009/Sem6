#!/usr/bin/env bash
set -euo pipefail

INPUT_DIR="${1:-.}"
OUTPUT_DIR="${2:-$INPUT_DIR/pdfs}"

INPUT_DIR="$(cd "$INPUT_DIR" && pwd)"
mkdir -p "$OUTPUT_DIR"
OUTPUT_DIR="$(cd "$OUTPUT_DIR" && pwd)"

osascript <<'APPLESCRIPT' "$INPUT_DIR" "$OUTPUT_DIR"
on run argv
    set inputFolderPOSIX to item 1 of argv
    set outputFolderPOSIX to item 2 of argv

    set fileListRaw to do shell script "find " & quoted form of inputFolderPOSIX & " -maxdepth 1 -type f \\( -iname '*.ppt' -o -iname '*.pptx' \\) | sort"

    if fileListRaw is "" then
        return "No PPT/PPTX files found in: " & inputFolderPOSIX
    end if

    set fileList to paragraphs of fileListRaw
    set convertedCount to 0

    tell application "Keynote"
        activate
        repeat with p in fileList
            set inPath to contents of p
            set inAlias to (POSIX file inPath) as alias
            set baseName to do shell script "basename " & quoted form of inPath & " | sed -E 's/\\.[Pp][Pp][Tt][Xx]?$//'"
            set outPath to outputFolderPOSIX & "/" & baseName & ".pdf"

            open inAlias
            tell front document
                export to (POSIX file outPath) as PDF
                close saving no
            end tell

            set convertedCount to convertedCount + 1
        end repeat
    end tell

    return "Done. Converted " & convertedCount & " file(s) to: " & outputFolderPOSIX
end run
APPLESCRIPT