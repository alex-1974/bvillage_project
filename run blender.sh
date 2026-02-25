#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
exec blender --factory-startup --no-window-frame --python ./run_in_blender.py "$@"
