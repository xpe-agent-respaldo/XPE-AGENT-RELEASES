"""Tag -> versiones para el build. v1.2.15 -> 1.2.15 | v1.2.15-rc.1 -> 1.2.15-1 (prerelease).
El instalador MSI solo admite prerelease numerico, por eso rc.N se convierte en -N."""
import re, sys
tag = sys.argv[1].strip()
m = re.fullmatch(r"v?(\d+)\.(\d+)\.(\d+)(?:-(?:rc|beta|alpha)?\.?(\d+)?)?", tag)
if not m:
    sys.exit(f"Tag invalido: {tag} (usa vX.Y.Z o vX.Y.Z-rc.N)")
base = ".".join(m.group(i) for i in (1, 2, 3))
pre = "-" in tag
num = m.group(4) or "1"
print(f"tag={tag if tag.startswith('v') else 'v'+tag}")
print(f"version={base}-{num}" if pre else f"version={base}")
print(f"prerelease={'true' if pre else 'false'}")
