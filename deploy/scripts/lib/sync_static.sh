#!/usr/bin/env bash
# Sync a built frontend directory into an immutable release directory.
# Uses rsync when available, otherwise cp.

sync_release_dir() {
  local source_dir=$1
  local target_dir=$2

  if [[ ! -d "$source_dir" ]]; then
    echo "Source directory is missing: $source_dir" >&2
    return 1
  fi

  install -d "$target_dir"

  if command -v rsync >/dev/null 2>&1; then
    rsync -a --delete "$source_dir/" "$target_dir/"
  else
    find "$target_dir" -mindepth 1 -maxdepth 1 -exec rm -rf {} +
    cp -a "$source_dir/." "$target_dir/"
  fi
}
