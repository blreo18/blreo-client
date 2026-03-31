"""manifest.json 자동 갱신 스크립트"""
import hashlib, json, os

base = os.path.dirname(os.path.abspath(__file__))
manifest = {"files": {}}

skip_dirs = {".git", "temp", "Screenshots", "PatchClient"}
skip_files = {".gitignore", "manifest.json", "gen_manifest.py", "update.bat"}

for root, dirs, files in os.walk(base):
    dirs[:] = [d for d in dirs if d not in skip_dirs]
    for f in files:
        full = os.path.join(root, f)
        rel = os.path.relpath(full, base).replace("\\", "/")
        if rel in skip_files:
            continue
        if f == "Sprite.NZspr.Pool":
            continue
        h = hashlib.sha256()
        with open(full, "rb") as fh:
            while True:
                chunk = fh.read(65536)
                if not chunk:
                    break
                h.update(chunk)
        manifest["files"][rel] = h.hexdigest()

sprite_path = os.path.join(base, "Sprite.NZspr.Pool")
if os.path.exists(sprite_path):
    h = hashlib.sha256()
    with open(sprite_path, "rb") as fh:
        while True:
            chunk = fh.read(65536)
            if not chunk:
                break
            h.update(chunk)
    manifest["release_files"] = {
        "Sprite.NZspr.Pool": {
            "sha256": h.hexdigest(),
            "url": "https://github.com/blreo18/blreo-client/releases/download/1.0/Sprite.NZspr.Pool"
        }
    }

out = os.path.join(base, "manifest.json")
with open(out, "w") as f:
    json.dump(manifest, f, indent=2, ensure_ascii=False)

print(f"[OK] manifest.json: {len(manifest['files'])} files + {len(manifest.get('release_files', {}))} release files")
