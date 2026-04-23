# KID-AT Framework — Master Index

**Dokument:** MASTER_INDEX.md  
**Scope:** Querverweise zwischen allen KID-AT-Dokumenten  
**Status:** Aktuell (2026-04-23)

---

## Navigationshilfe

Dieser Index verknüpft Theoreme, Definitionen und Konzepte über alle KID-AT-Dokumente hinweg. Bei Unterschieden in der Nummerierung gilt die **Hauptsynthese** (`KID_AT_Final_Synthesis.md`) als autoritativ.

---

## Theorem-Index (Cross-Document)

### Theoreme aus der Hauptsynthese (`KID_AT_Final_Synthesis.md`)

| # | Theorem | Quelle in Synthese | Entsprechung ICP | Entsprechung Thermodynamik | Entsprechung Meta-Analyse |
|---|---------|-------------------|------------------|---------------------------|--------------------------|
| 1.1 | Kolmogorov-Adäquatheit | Def. 1.1 | — | — | Axiom K-1, Axiom U-1 |
| 1.2 | Dimensionslosigkeit von $C$ | Def. 1.2 | Def. 0.1, Theorem 5.1 | — | Axiom U-3 |
| 1.3 | AI-KID Monotonie | Def. 1.3 | — | Lemma 5.5 | Axiom I-5, Theorem 2.3 |
| 1.4 | Tricritical-Ising Unterscheidbarkeit | Def. 1.4 | Theorem 2.5 | — | — |
| 1.5 | Effizienzmaximum bei $C=1$ | Def. 1.6 | Theorem 4.1 | Theorem 4.1 | Axiom U-5 |
| 1.6 | Pitchfork bei kognitiver Kondensation | Def. 1.8 | Theorem 1.1, Theorem 4.3 | Theorem 7.1 | — |
| 1.7 | $K \to \psi$ RG-Fluss | — | — | — | — |
| 1.8 | Gültigkeit der Brücke | — | — | — | — |
| 1.9 | Stationäre Verteilung (Master-Gleichung) | Def. 1.9 | — | Master Equation (§8) | — |
| 1.10 | AI-Maximum (2. Hauptsatz) | Theorem 1.10 | — | Corollary 5.3 | — |
| 1.11 | Physikalische Selbstmessungsgrenze | Theorem 1.11 | Axiom 0.4 | Lemma 7.5 | Axiom U-7 |
| 3.1 | Potenzgesetzverhalten am ICP | §3.2 | Theorem 3.2 | — | — |
| 3.2 | Divergenz der Korrelationslänge | §3.3 | Theorem 1.2 | — | — |
| 3.3 | Stabilität der Attraktoren | §3.5 | Theorem 4.3, Theorem 4.4 | Theorem 7.1 | — |

### Theoreme aus dem ICP-Dokument (`informational_condensation_point.md`)

| # | Theorem | Quelle ICP | Entsprechung Synthese | Bemerkung |
|---|---------|-----------|----------------------|-----------|
| 0.1 | Dimensionslose Kondensationszahl | Def. 0.1 | Def. 1.2 | Identisch |
| 0.4 | Physikalische Selbstmessungsgrenze | Axiom 0.4 | Theorem 1.11 | Heuristik, nicht Theorem |
| 1.1 | Existenz des ICP | Def. 1.2 | Def. 1.4 | LG-Funktional mit $\psi^6$ in Synthese |
| 1.2 | ICP als Instabilitätspunkt | Def. 1.3 | Def. 3.1 | Korrelationslänge divergiert |
| 1.3 | Kritisches Verlangsamen | — | — | Dynamischer Exponent $z=2$ |
| 2.1 | RG-Flussgleichungen | §2.1 | — | Wilsonsche RG |
| 2.2 | Gaußscher Fixpunkt | Theorem 2.2 | — | Stabil für $d > 4$ |
| 2.3 | Wilson-Fisher-Fixpunkt | Theorem 2.3 | — | Nicht-trivialer Fixpunkt |
| 2.4 | Kritische Exponenten | Theorem 2.4 | Def. 1.5 | $O(\epsilon)$-Näherung vs. Monte-Carlo |
| 2.5 | Universalitätsklasse (Ising) | Theorem 2.5 | Def. 1.5 | Skalar, $\mathbb{Z}_2$ |
| 2.6 | Obere kritische Dimension | Theorem 2.6 | — | $d_c = 4$ |
| 3.1 | SOC-Avalanchen | Def. 3.1 | §3.2 | BTW-Sandpile-Abbildung |
| 3.2 | KID-Potenzgesetz | Theorem 3.2 | §3.2 | $\alpha \approx 1.73$ (Fluktuationen, nicht SOC) |
| 4.1 | Kaskade von Phasenübergängen | Theorem 4.1 | Def. 1.7 | Emergenz-Hierarchie |
| 4.2 | Kritische KID-Werte | Theorem 4.2 | Def. 1.7 | Normiert auf $[0,1]$ |
| 4.3 | Multi-Level-Freie Energie | Theorem 4.3 | — | Kaskade von Pitchforks |
| 4.4 | Symmetriebrechung | Theorem 4.4 | — | $\mathbb{Z}_2$ pro Stufe |
| 4.5 | Gehirn als kritisches System | Theorem 4.5 | §3.5 | Jirsa-Sheheitli-Framework |
| 5.1 | Phasenübergang in dimensionslosen Variablen | Theorem 5.1 | Def. 1.2 | Identisch |
| 5.2 | Zustandsgleichung | Theorem 5.2 | — | Skalierungshypothese |
| 5.3 | Thermodynamische Konsistenz | Theorem 5.3 | Def. 1.5 | — |

### Theoreme aus der Thermodynamik (`kid_at_thermodynamic_analysis.tex`)

| # | Theorem | Quelle Thermodynamik | Entsprechung Synthese | Entsprechung ICP |
|---|---------|---------------------|----------------------|-----------------|
| 3.1 | Entropy-Export-Schranke | Theorem 3.1 | Theorem 1.10 | — |
| 3.2 | Kosten pro AI-Einheit | Corollary 3.2 | — | — |
| 3.3 | Superlineare Skalierung | Proposition 3.3 | — | — |
| 4.1 | Toast-optimale Effizienz | Theorem 4.1 | Def. 1.6, Theorem 1.5 | Theorem 4.1 |
| 5.1 | KID-Freie-Energie-Beziehung | Theorem 5.1 | — | — |
| 5.2 | FEP treibt KID/AI-Zunahme | Theorem 5.2 | Def. 1.9 (Master-Gleichung) | — |
| 5.3 | FEP-Assembly-Kopplung | Corollary 5.3 | Theorem 1.10 | — |
| 5.4 | Attention als Entropie-Export-Optimierung | Proposition 5.4 | — | — |
| 6.1 | Effizienz-Grat bei $T=1$ | Theorem 6.1 | Theorem 1.5 | — |
| 6.2 | Stabilität auf dem Grat | Theorem 6.2 | — | — |
| 6.3 | Dynamik abseits des Grats | Corollary 6.3 | — | — |
| 7.1 | Mehrere High-AI-Attraktoren | Theorem 7.1 | Def. 1.8 | Theorem 4.3 |
| 7.5 | Physikalische Selbstmessungsgrenze | Lemma 7.5 | Theorem 1.11 | Axiom 0.4 |

---

## Axiom-Index (Cross-Document)

| Axiom | Synthese | ICP | Thermodynamik | Meta-Analyse |
|-------|----------|-----|---------------|--------------|
| U-1 (Kolmogorov-Fundament) | §2.1 | Def. 0.3 | — | K-1, U-1 |
| U-2 (Kondensations-Irreversibilität) | §2.2 | — | — | — |
| U-3 (Landauer-Bound) | §2.3 | — | §3.1, §5 | — |
| U-4 (Pfadabhängigkeit / AT) | §2.4 | — | — | A-2, A-4 |
| U-5 (Emergenz hinreichend, nicht notwendig) | §2.5 | Axiom 0.2 | §7 | — |
| U-6 (FEP) | §2.6 | — | §5 | — |
| U-7 (Physikalische Selbstmessungsgrenze) | §2.7 | Axiom 0.4 | Lemma 7.5 | U-7 |

---

## Definition-Index (Cross-Document)

| Definition | Synthese | ICP | Thermodynamik |
|-----------|----------|-----|---------------|
| Dimensionslose Kondensationszahl $C$ | Def. 1.2 | Def. 0.1 | — |
| Assembly-Index AI | Def. 1.3 | Def. (Cronin-Walker) | Def. (§1.1) |
| LG-Funktional | Def. 1.4 | Def. 1.2 | — |
| Kritische Exponenten | Def. 1.5 | Theorem 2.4 | — |
| Toast-Effizienz $\eta_{\text{thermo}}$ | Def. 1.6 | Def. 5.3 | Theorem 4.1 |
| Emergenz-Hierarchie (6 Stufen) | Def. 1.7 | Theorem 4.2 | — |
| Drei Attraktoren | Def. 1.8 | Theorem 4.3, 4.4 | Theorem 7.1 |
| Master-Gleichung | Def. 1.9 | — | Master Equation (§8) |
| Ordnungsparameter $\psi$ | — | Def. 1.1 | — |
| Informationskondensationspunkt (ICP) | Def. 3.1 | Def. 1.3 | — |

---

## Konzept-Index (Cross-Document)

| Konzept | Erste Einführung | Primäre Quelle | Sekundäre Quellen |
|---------|-----------------|---------------|-----------------|
| Toast-Effizienz / Toast-Gesetz | Synthese Def. 1.6 | Synthese | ICP Def. 5.3; Thermodynamik Theorem 4.1 |
| Tricritical-Ising-Kreuzung | Synthese Def. 1.4 | Synthese | ICP Theorem 2.4 (Fussnote) |
| Selbstorganisierte Kritikalität (SOC) | Synthese §3.2 | ICP §3 | Synthese §3.2 |
| Kritische Fluktuationsverteilung | Synthese §3.2 | Synthese | ICP Theorem 3.2 |
| Drei-Attraktor-Struktur | Synthese Def. 1.8 | Synthese | ICP Theorem 4.3; Thermodynamik Theorem 7.1 |
| Pitchfork-Bifurkation | Synthese Theorem 1.6 | Synthese | ICP Theorem 4.3 |
| CV-1 (Dimensionale Inkonsistenz) | Synthese Def. 1.2 | Synthese | ICP §5.1 |
| CV-2 (Emergenz-Non-Sequitur) | Synthese Axiom U-5 | Synthese | ICP Axiom 0.2; Thermodynamik §7 |
| CV-3 (Information braucht Interpreter) | Synthese Def. 1.1 | Synthese | ICP Def. 0.3; Meta-Analyse §4 |
| CV-4 (Gödel-Kategoriefehler) | Synthese Axiom U-7 | Synthese | ICP Axiom 0.4; Thermodynamik Lemma 7.5 |
| FD-1 (Messprotokoll) | Synthese §4.3 | Synthese | — |
| FD-2 (Berechenbare Schwellen) | Synthese Def. 1.7 | Synthese | — |
| FD-3 (Unterscheidbarkeit von FEP/IIT) | Synthese §5 | Synthese | — |

---

## Simulations-Index

| Hypothese | Algorithmus | Status | Primäre Quelle |
|-----------|-------------|--------|---------------|
| H1: Assembly-Phasenübergang | DAG-ASE | Entwurf abgeschlossen | Synthese §4.1 |
| H2: Toast-optimale Selbstorganisation | Ising-PA-Loop | Entwurf abgeschlossen | Synthese §4.2 |
| H3: Gehirn-AI | Neuroimaging-Analyse | Planungsphase | Synthese §7.2 |
| H4: Drei Attraktoren | Multi-Attraktor-Simulation | Konzeptionell | Synthese §7.2 |
| H5: Korrelationslänge | Finite-Size-Skalierung | Entwurf abgeschlossen | Synthese §7.2 |

---

## Daten-Index

| Datensatz | Ort | Typ | Status |
|-----------|-----|-----|--------|
| Literatur-Metadaten Assembly Theory | `DATA/REFERENCES/scholar_assembly_theory.csv` | Literatur-Metadaten | Aktuell |
| Literatur-Metadaten Attention | `DATA/REFERENCES/scholar_attention.csv` | Literatur-Metadaten | Aktuell |
| Literatur-Metadaten FEP | `DATA/REFERENCES/scholar_fep_phases.csv` | Literatur-Metadaten | Aktuell |
| Literatur-Metadaten IIT | `DATA/REFERENCES/scholar_iit_empirical.csv` | Literatur-Metadaten | Aktuell |
| Literatur-Metadaten Nichtgleichgewicht | `DATA/REFERENCES/scholar_non_equilibrium.csv` | Literatur-Metadaten | Aktuell |
| Simulationsdaten H1 | `DATA/SIMULATIONS/h1_phase_transition.csv` | Simulationsdaten | Blueprint-basiert |
| Simulationsdaten H2 | `DATA/SIMULATIONS/h2_toast_optimization.csv` | Simulationsdaten | Blueprint-basiert |

---

## Änderungshistorie

| Datum | Änderung | Autor |
|-------|----------|-------|
| 2026-04-23 | Erstellung; alle Querverweise zwischen Synthese, ICP, Thermodynamik, Meta-Analyse | Subagent |

---

*Dieser Index wird bei jeder moderaten oder kritischen Änderung am Framework aktualisiert. Die TERMINOLOGY.md definiert die kanonische Symbolik.*
