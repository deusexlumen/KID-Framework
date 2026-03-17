# 06: Archive Original | Archiv Original

> 📦 **This folder is intentionally empty in the distributed version.**

---

## Purpose | Zweck

This folder serves as a placeholder for **backup copies** of the original files before modifications.

In the development workflow:
- Original files are copied here before editing
- Enables version comparison
- Preserves historical reference

---

## For Users | Für Nutzer

**You don't need this folder** — all content is in the other directories:

| Original Location | Current Location |
|:------------------|:-----------------|
| Root folder | `01-PHILOSOPHICAL-FOUNDATIONS/`, `02-SCIENTIFIC-FORMALIZATION/`, etc. |

---

## For Developers | Für Entwickler

To populate this folder with backups:

```bash
# Copy current state before making changes
cp ../01-PHILOSOPHICAL-FOUNDATIONS/*.md ./
cp ../02-SCIENTIFIC-FORMALIZATION/*.md ./
# etc.
```

---

**Note:** This folder is excluded from release ZIPs to save space.
