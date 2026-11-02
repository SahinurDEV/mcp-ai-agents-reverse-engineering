"""bump_kind.py OLD.json NEW.json: which semver bump does a tool-contract change need?
Compares two tools.schema.json snapshots (Section 10). Removed or altered = MAJOR, only added = MINOR,
identical = PATCH at most. Description changes are reported separately: at least MINOR, say so."""
import json, sys

old, new = (json.load(open(p)) for p in sys.argv[1:3])
major, minor = [], []
for name in old:
    if name not in new:
        major.append(f"tool removed: {name}"); continue
    o, n = old[name]["inputSchema"], new[name]["inputSchema"]
    for arg in o.get("properties", {}):
        if arg not in n.get("properties", {}): major.append(f"{name}: argument removed: {arg}")
        elif o["properties"][arg] != n["properties"][arg]: major.append(f"{name}: argument changed: {arg}")
    for arg in n.get("properties", {}):
        if arg not in o.get("properties", {}):
            (major if arg in n.get("required", []) else minor).append(
                f"{name}: {'required' if arg in n.get('required', []) else 'optional'} argument added: {arg}")
    if old[name].get("outputSchema") != new[name].get("outputSchema"):
        oo, no = (set((x.get("outputSchema") or {}).get("properties", {})) for x in (old[name], new[name]))
        (minor if oo <= no else major).append(f"{name}: output fields {'added' if oo <= no else 'removed/changed'}")
    if old[name].get("description") != new[name].get("description"):
        minor.append(f"{name}: description changed (models may behave differently)")
minor += [f"tool added: {t}" for t in new if t not in old]
for line in major: print("MAJOR ", line)
for line in minor: print("MINOR ", line)
print("=> bump", "MAJOR" if major else "MINOR" if minor else "PATCH (or none)")
