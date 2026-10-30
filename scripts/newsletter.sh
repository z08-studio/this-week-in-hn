#!/bin/bash

BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)" || exit 1
DRAFTS_DIR="$BASE_DIR/drafts"
ARCHIVE_DIR="$BASE_DIR/archive"

function format_publication_date() {
    local publication_date=$1
    local format=$2

    # Support GNU date on Linux and BSD date on macOS.
    date -d "$publication_date" "$format" 2>/dev/null ||
        date -j -f "%Y-%m-%d" "$publication_date" "$format" 2>/dev/null
}

function is_valid_publication_date() {
    local publication_date=$1
    local normalized_date

    [[ "$publication_date" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]] &&
        normalized_date=$(format_publication_date "$publication_date" +%Y-%m-%d) &&
        [[ "$normalized_date" == "$publication_date" ]]
}

function is_regular_issue() {
    local filepath=$1
    local filename=${filepath##*/}

    [[ -f "$filepath" && ! -L "$filepath" ]] || return 1
    [[ "$filename" =~ ^([0-9]{4}-[0-9]{2}-[0-9]{2})-issue-[0-9]+\.md$ ]] || return 1
    is_valid_publication_date "${BASH_REMATCH[1]}"
}

function get_upcoming_friday() {
    local dow days_ahead

    # A Friday edition prepared on Friday belongs to today.
    dow=$(TZ=Asia/Shanghai date +%u) || return 1
    days_ahead=$(((5 - dow + 7) % 7))

    TZ=Asia/Shanghai date -d "+${days_ahead} days" +%Y-%m-%d 2>/dev/null ||
        TZ=Asia/Shanghai date -v+"${days_ahead}"d +%Y-%m-%d
}

function ensure_no_future_drafts() {
    local target_date=$1
    local filepath filename
    local future_drafts=()

    for filepath in "$DRAFTS_DIR"/*-issue-*.md; do
        is_regular_issue "$filepath" || continue
        filename=${filepath##*/}
        if [[ "${filename:0:10}" > "$target_date" ]]; then
            future_drafts+=("$filename")
        fi
    done

    if (( ${#future_drafts[@]} > 0 )); then
        echo "Found draft(s) dated after $target_date in $DRAFTS_DIR:" >&2
        printf ' - %s\n' "${future_drafts[@]}" >&2
        echo "Archive/remove them (or rename) before creating a new draft." >&2
        return 1
    fi
}

function get_next_issue_number() {
    local max_num=0
    local filepath filename num

    while IFS= read -r filepath; do
        is_regular_issue "$filepath" || continue
        filename=${filepath##*/}
        num=${filename##*-issue-}
        num=${num%.md}
        num=$((10#$num))
        if (( num > max_num )); then
            max_num=$num
        fi
    done < <(find "$DRAFTS_DIR" "$ARCHIVE_DIR" -type f -name '*-issue-*.md' 2>/dev/null)

    printf '%02d' "$((max_num + 1))"
}

function create_draft() {
    local publication_date=${1:-}
    local existing_file issue_num filepath

    if [[ -z "$publication_date" ]]; then
        publication_date=$(get_upcoming_friday) || return 1
    fi

    if ! is_valid_publication_date "$publication_date"; then
        echo "Invalid publication date: $publication_date. Use YYYY-MM-DD." >&2
        return 1
    fi

    ensure_no_future_drafts "$publication_date" || return 1

    for existing_file in "$DRAFTS_DIR"/"$publication_date"-issue-*.md \
        "$ARCHIVE_DIR"/"${publication_date%%-*}"/"$publication_date"-issue-*.md; do
        if [[ -e "$existing_file" || -L "$existing_file" ]]; then
            echo "An issue already exists for $publication_date: $existing_file" >&2
            return 1
        fi
    done

    issue_num=$(get_next_issue_number) || return 1
    filepath="$DRAFTS_DIR/${publication_date}-issue-${issue_num}.md"
    mkdir -p "$DRAFTS_DIR" || return 1

    # Create a blank file without replacing an existing draft.
    (set -o noclobber; : > "$filepath") || return 1
    echo "Created new draft: $filepath"
}

function archive_draft() {
    local filepath=${1:-}
    local candidate source_dir filename year target_dir target
    local drafts=()

    if [[ -z "$filepath" ]]; then
        for candidate in "$DRAFTS_DIR"/*-issue-*.md; do
            is_regular_issue "$candidate" || continue
            drafts+=("$candidate")
        done
        if (( ${#drafts[@]} == 0 )); then
            echo "No drafts found to archive." >&2
            return 1
        elif (( ${#drafts[@]} > 1 )); then
            echo "Multiple drafts found. Specify which one to archive:" >&2
            printf ' - %s\n' "${drafts[@]}" >&2
            return 1
        fi
        filepath=${drafts[0]}
    fi

    if [[ ! -e "$filepath" && ! -L "$filepath" ]]; then
        filepath="$DRAFTS_DIR/$filepath"
    fi

    if ! is_regular_issue "$filepath"; then
        echo "Only a regular draft file named YYYY-MM-DD-issue-NN.md with a valid date can be archived." >&2
        return 1
    fi
    source_dir=$(cd "$(dirname "$filepath")" && pwd -P) || return 1
    if [[ "$source_dir" != "$DRAFTS_DIR" ]]; then
        echo "Only a regular file in the drafts directory can be archived." >&2
        return 1
    fi

    filename=${filepath##*/}
    year=${filename:0:4}
    target_dir="$ARCHIVE_DIR/$year"
    target="$target_dir/$filename"
    mkdir -p "$target_dir" || return 1
    if [[ -e "$target" || -L "$target" ]]; then
        echo "Archive already exists: $target" >&2
        return 1
    fi

    mv -n "$filepath" "$target_dir/" || return 1
    if [[ -e "$filepath" ]]; then
        echo "Draft was not moved; archive may already exist." >&2
        return 1
    fi
    echo "Archived $filename to $target_dir/"
}

case "${1:-}" in
    new)
        create_draft "${2:-}"
        ;;
    archive)
        archive_draft "${2:-}"
        ;;
    *)
        echo "Usage: $0 {new [YYYY-MM-DD]|archive [filename]}" >&2
        exit 1
        ;;
esac
