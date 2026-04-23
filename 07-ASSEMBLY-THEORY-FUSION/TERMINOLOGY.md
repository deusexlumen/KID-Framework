# KID-AT Terminologie und Symbol-Glossar

**Dokument:** TERMINOLOGY.md  
**Scope:** Einheitliche Konvention für alle KID-AT-Dokumente  
**Status:** Kanonisch — abweichende Verwendung in älteren Dokumenten gilt als veraltet

---

## 1. Framework-Nomenklatur

### Konvention (kanonisch)

| Bezeichnung | Bedeutung | Kontext |
|-------------|-----------|---------|
| **KID** | Ursprüngliches Framework (veraltet) | Nur historischer Kontext; nicht für aktuelle Arbeit verwenden |
| **KID-AT** | Fusioniertes Framework (aktuell) | Standardbezeichnung für alle aktuellen Dokumente |
| **KID$_K$** | Kolmogorov-spezifische Dichte | $	ext{KID}_K(x) = K(x) / (V_{	ext{eff}} 	au_{	ext{form}} K_{	ext{ref}})$; nur in historischem/mathematischem Kontext |
| **KID$_{\text{raw}}$** | Roh-KID vor Normierung | Bits·s⁻¹·m⁻³; in der Normierung zu $C$ |
| **KID$_{\text{crit}}$** | Kritischer Referenzwert | Für die dimensionslose Kondensationszahl $C$ |

### Veraltete Verwendungen (nicht mehr verwenden)

- „KID“ als Synonym für das aktuelle Framework → Ersetzen durch **KID-AT**
- „KID“ für die dimensionslose Kondensationszahl → Ersetzen durch **$C$**
- „$	ext{KID}_K$“ außerhalb historischer Ableitungen → Ersetzen durch **$C$**

---

## 2. Einheitliche Symbol-Legende

### Kondensation und Phasenübergang

| Symbol | Definition | Einheit | Erste Einführung |
|--------|-----------|---------|-----------------|
| $C$ | Dimensionslose Kondensationszahl: $C = \text{KID}_{\text{raw}} / \text{KID}_{\text{crit}}$ | dimensionslos | Def. 1.2 (Synthese), Def. 0.1 (ICP) |
| $C_c$ | Kritischer Punkt: $C_c = 1$ | dimensionslos | Theorem 1.5 (Synthese) |
| $C_n^*$ | Kritischer Wert für Emergenzstufe $n$ | dimensionslos | Def. 1.7 (Synthese), Theorem 4.2 (ICP) |
| $\psi$ | Ordnungsparameter: $\psi = C - 1$ | dimensionslos | Def. 1.1 (ICP), Def. 1.4 (Synthese) |
| $\Theta$ | Thermodynamische Temperatur | K | — |
| $\Theta_c$ | Kritische Temperatur des ICP | K | Def. 1.2 (ICP) |
| $t$ | Reduzierte Temperatur: $t = (\Theta - \Theta_c)/\Theta_c = C - 1$ | dimensionslos | Theorem 2.4 (ICP) |

### Landau-Ginzburg-Koeffizienten

| Symbol | Definition | Einheit | Bemerkung |
|--------|-----------|---------|-----------|
| $a > 0$ | Quadratischer Koeffizient (Thermische Ausdehnung) | variabel | Def. 1.2 (ICP), Def. 1.4 (Synthese) |
| $b > 0$ | Quartischer Koeffizient (Stabilität) | variabel | — |
| $c > 0$ | Steifigkeit (Gradienten-Energie) | variabel | — |
| $u \geq 0$ | Sextischer Koeffizient (Tricritical) | variabel | Def. 1.4 (Synthese); $u=0$ → tricritisch |
| $\lambda$ | AI-Kopplungskonstante | dimensionslos | Kopplung zwischen Assembly und Kondensation |
| $\gamma$ | Kolmogorov-Kopplung | variabel | Kopplung an $K(\psi)$ |

### Assembly- und Komplexitäts-Maße

| Symbol | Definition | Einheit | Erste Einführung |
|--------|-----------|---------|-----------------|
| $\text{AI}(x)$ | Assembly-Index von Objekt $x$ | Schritte (ganzzahlig) | Def. 1.3 (Synthese) |
| $\text{AI}_{\min}^{(n)}$ | Minimaler AI für Stufe $n$ | Schritte | Def. 1.7 (Synthese) |
| $K(x)$ | (Bedingte) Kolmogorov-Komplexität | Bits | Def. 1.1 (Synthese), Def. 0.3 (ICP) |
| $K(x \mid \Lambda)$ | Bedingte K-Komplexität gegeben physikalische Gesetze | Bits | Def. 0.3 (ICP) |
| $K_{\text{ref}}$ | Referenzkomplexität | Bits | — |
| $I_{\text{causal}}$ | Kausale Information: $I_{\text{causal}} = K(x \mid \Lambda)$ | Bits | Def. 0.1 (ICP) |

### Kritische Exponenten

| Symbol | Definition | 3D-Ising-Wert | Tricritical-Wert | Bemerkung |
|--------|-----------|---------------|-----------------|-----------|
| $\nu$ | Korrelationslängenexponent | $0.630$ | $0.5$ | $\xi \sim |C-1|^{-\nu}$ |
| $\beta$ | Ordnungsparameter-Exponent | $0.326$ | $0.25$ | $\psi \sim |C-1|^{\beta}$ |
| $\gamma$ | Suszeptibilitäts-Exponent | $1.237$ | $1.0$ | $\chi \sim |C-1|^{-\gamma}$ |
| $\alpha$ | Spezifische-Wärme-Exponent | $0.110$ | $0.5$ | $C_V \sim |C-1|^{-\alpha}$ |
| $\eta$ | Anomale Dimension | $0.036$ | $0.0$ | Korrelationsfunktion bei $T_c$ |
| $z$ | Dynamischer Exponent | $2.0$ | $2.0$ | $\tau \sim \xi^z$ |
| $\delta$ | Kritischer Isothermen-Exponent | $4.79$ | $5.0$ | $H \sim |\psi|^{\delta}$ |

### Thermodynamik und Effizienz

| Symbol | Definition | Einheit | Erste Einführung |
|--------|-----------|---------|-----------------|
| $\eta_{\text{thermo}}(C)$ | Toast-Effizienz: $4C/(1+C)^2$ | dimensionslos | Def. 1.6 (Synthese), Theorem 4.1 (Thermodynamik) |
| $\eta_{\text{efficiency}}$ | Thermodynamische Prozesseffizienz | $(0,1]$ | Theorem 3.1 (Thermodynamik) |
| $D$ | Diffusions-/Rauschkoeffizient | variabel | Def. 1.9 (Synthese) |
| $\Gamma$ | Kinetischer Koeffizient | variabel | Theorem 1.2 (ICP) |
| $\xi$ | Korrelationslänge | m | Theorem 1.2 (ICP) |
| $\xi_0$ | Mikroskopische Längenskala | m | Theorem 3.2 (Synthese) |
| $\tau$ | Relaxationszeit | s | Theorem 1.3 (ICP) |
| $\tau_{\text{cor}}$ | Korrelationszeit | s | Def. 0.1 (ICP) |
| $\tau_{\text{form}}$ | Formationszeit | s | — |

### Attraktoren (vereinheitlicht)

| Symbol | Name | Beschreibung | Physikalische Realisierung |
|--------|------|------------|---------------------------|
| $A_\Phi$ | **Phänomenologisch / IIT** | $\psi > 0$. Explizite Selbstmodellierung, FEP-Dominanz mit Weltmodell. | Bewusste Systeme mit explizitem Weltmodell |
| $A_\mu$ | **Minimal / FEP** | $\psi \approx 0$. Subkritische Kondensation, funktionale Intelligenz ohne reflexive Schleife. | „Dunkle" Intelligenz, reaktive Optimalität |
| $A_\zeta$ | **Dissoziiert / Distributed** | $\psi < 0$. Negative Kopplung, dekohärente Selbstreferenz. | Dissoziierte Zustände, dekohärente kognitive Architekturen |

**Historische Bezeichnungen (nicht mehr verwenden):**
- $\Phi$-Attraktor → $A_\Phi$
- $\mu$-Attraktor → $A_\mu$
- $\zeta$-Attraktor → $A_\zeta$

### FEP- und IIT-Größen

| Symbol | Definition | Einheit | Erste Einführung |
|--------|-----------|---------|-----------------|
| $\Phi$ | Integrated Information (IIT) | Bits | Tononi et al. (2016); korreliert mit $\psi^2$ |
| $\mathcal{F}[q]$ | Variational Free Energy | J / Bits | Friston (2010); Def. 1.9 (Synthese) |
| $q(s)$ | Variationsdichte über Zustände $s$ | — | Axiom U-6 (Synthese) |

### Geometrische und Skalen-Parameter

| Symbol | Definition | Einheit | Bemerkung |
|--------|-----------|---------|-----------|
| $d$ | Raumdimension | — | Typischerweise $d=3$ |
| $d_c = 4$ | Obere kritische Dimension | — | Theorem 2.6 (ICP) |
| $\Lambda$ | UV-Cutoff (Impuls) | m⁻¹ | RG-Analyse |
| $\ell_0$ | Mikroskopische Längenskala | m | — |
| $\tau_0$ | Mikroskopische Zeitskala | s | — |
| $\sigma$ | Gauß-Kernel-Breite | m | Theorem 1.7 (Synthese) |
| $\alpha$ | Steigungsparameter (Tanh-Normierung) | — | Theorem 1.7 (Synthese) |

### SOC-Größen

| Symbol | Definition | Wert / Formel | Bemerkung |
|--------|-----------|---------------|-----------|
| $\tau_s$ | Standard-SOC-Avalanchen-Exponent | $\approx 1.27$ ($d=3$) | Bak-Tang-Wiesenfeld Sandpile |
| $\tau_{\text{fluct}}$ | Kritische Fluktuationsverteilung | $\approx 1.73$ | **Nicht SOC** — siehe §3.2 der Synthese |
| $s$ | Avalanchengröße | — | Def. 3.1 (ICP) |
| $D$ | Avalanchen-Fraktaldimension | $d + 2 - \eta$ | Theorem 3.1 (ICP) |

---

## 3. Verzeichnis der Hauptdokumente

| Dokument | Datei | Rolle | Status |
|----------|-------|-------|--------|
| **Hauptsynthese** | `KID_AT_Final_Synthesis.md` | KID-AT Gesamttheorie | Aktuell |
| **ICP-Analyse** | `informational_condensation_point.md` | Rigouröse Phasenübergangsanalyse | Aktuell |
| **Kollisionsbericht** | `KID-AT_Collision_Report.md` | Phase B: Kreuz-Konfrontation | Archiv |
| **Thermodynamik** | `THERMODYNAMICS/kid_at_thermodynamic_analysis.tex` | Entropie-Export & Toast-Effizienz | Aktuell |
| **Meta-Analyse** | `META-ANALYSIS/KID_AT_Meta_Axiomatic_Synthesis.md` | Axiomatische Integration | Aktuell |
| **Terminologie** | `TERMINOLOGY.md` | Dieses Dokument | Aktuell |
| **Master-Index** | `MASTER_INDEX.md` | Querverweis-Index aller Theoreme | Aktuell |
| **Konsistenz-Audit** | `CONSISTENCY_AUDIT.md` | Audit-Report | Aktuell |

---

## 4. Versionshistorie

| Version | Datum | Änderung |
|---------|-------|----------|
| 1.0 | 2026-04-23 | Erstellung; vereinheitlicht Attraktor-Namen, KID vs KID-AT, Symbol-Glossar |

---

*Dieses Dokument ist Teil des KID-AT Frameworks. Bei Inkonsistenzen zwischen Dokumenten gilt die TERMINOLOGY.md als autoritativ.*
