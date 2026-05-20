#!/usr/bin/env bash
# Génère un .docx par simulateur, à partir de docs/specs-metier/<simulateur>/spec.md.
# Les images référencées dans le spec.md sont résolues depuis le sous-dossier du simulateur.
# Usage : ./build.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DIST_DIR="$SCRIPT_DIR/dist"
TEMPLATE="$SCRIPT_DIR/reference.docx"

if ! command -v pandoc >/dev/null 2>&1; then
  echo "Erreur : pandoc n'est pas installé."
  echo "  → brew install pandoc"
  exit 1
fi

mkdir -p "$DIST_DIR"

REF_ARGS=()
if [[ -f "$TEMPLATE" ]]; then
  REF_ARGS=(--reference-doc="$TEMPLATE")
  echo "Style admin : $TEMPLATE"
else
  echo "Note : aucun reference.docx trouvé, style pandoc par défaut utilisé."
fi

shopt -s nullglob
count=0
for spec in "$SCRIPT_DIR"/*/spec.md; do
  sim_dir="$(dirname "$spec")"
  sim_name="$(basename "$sim_dir")"
  out="$DIST_DIR/${sim_name}-spec.docx"
  echo "→ $sim_name/spec.md  →  dist/$(basename "$out")"

  pandoc "$spec" \
    --from=markdown+yaml_metadata_block+pipe_tables+tex_math_dollars \
    --to=docx \
    --resource-path="$sim_dir" \
    --toc \
    --toc-depth=2 \
    ${REF_ARGS[@]+"${REF_ARGS[@]}"} \
    -o "$out"

  count=$((count + 1))
done

if [[ $count -eq 0 ]]; then
  echo "Aucun spec.md trouvé. Crée d'abord un sous-dossier <simulateur>/ avec un spec.md."
  exit 1
fi

echo ""
echo "OK : $count fichier(s) généré(s) dans $DIST_DIR"
