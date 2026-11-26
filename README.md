![Syed Nafiz Reja Hasib](assets/hero.svg)

<p align="center">
  <a href="https://syednafizreja.github.io/">Portfolio</a>
  &nbsp;·&nbsp;
  <a href="https://orcid.org/0009-0002-7162-7890">ORCID</a>
  &nbsp;·&nbsp;
  <a href="https://doi.org/10.5281/zenodo.24559613">NiTi preprint</a>
  &nbsp;·&nbsp;
  <a href="https://doi.org/10.5281/zenodo.24560903">Shell preprint</a>
  &nbsp;·&nbsp;
  <a href="https://syednafizreja.github.io/ShellLab/">Launch ShellLab</a>
</p>

## About

I started by cycling and breaking real superelastic NiTi components in a precision manufacturing lab (Denco Manufacturing, 2024-2026) after a BEng in Civil Engineering (SWPU). Now I write verified computational mechanics solvers to test where clean structural theory collides with messy reality: earthquakes, buckling imperfections, and embodied carbon. Most of my repos exist to answer a simple question: does an efficient idea still hold up when you stop ignoring the inconvenient physics?

## Milestones

| When | Record |
| --- | --- |
| 2026, preprint | 1D Auricchio-Sacco NiTi return map and 80-canopy seismic-carbon trade-offs. [Zenodo](https://doi.org/10.5281/zenodo.24559613) |
| 2026, preprint | Equal-volume concrete shell buckling: stress-line ribs against optimised thickness. [Zenodo](https://doi.org/10.5281/zenodo.24560903) |
| 2026, dataset | ShellBench: 5,184 coupled seismic RC-frame and thin-shell floor designs, 287 automated tests. [Code](https://github.com/syednafizreja/ShellBench) · [Dataset](https://doi.org/10.5281/zenodo.24194144) |
| 2026, web solver | ShellLab: browser force-density form-finding, matching Python to 10^-13 m. [Launch](https://syednafizreja.github.io/ShellLab/) |
| 2024-2026, lab | Cyclic-durability testing, micro-CNC metrology, and failure analysis of superelastic NiTi, Denco Manufacturing. |

## What this GitHub is about

<table>
  <tr>
    <td width="50%" valign="top">
      <h3>diagrid-seismic-opt</h3>
      <p>Superelastic NiTi recentring sounds free until you track peak drift and carbon. A 1D return map (tangent error 1.85e-10), PyTorch inverse identification (7.28% max error at 3% noise), and 80 paired 0.40 g canopies cut residual drift from 0.0659% to 0.0175%. Peak drift rises from 1.79% to 3.40%, cradle-to-gate carbon rises by 620.9 kgCO2e, and the GP screen is false-safe on 0 of 160 rows.</p>
      <p><a href="https://github.com/syednafizreja/diagrid-seismic-opt">Code</a> · <a href="https://doi.org/10.5281/zenodo.24559613">DOI</a></p>
    </td>
    <td width="50%" valign="top">
      <h3>Stress-line ribs versus thickness</h3>
      <p>Ribs along principal stress lines look efficient until constant volume starves the shell of bending stiffness. On a 12x12 m pinned shell in 0.2 g sway, CalculiX (Scordelis-Lo and Zoelly checked) shows stress-line ribs drop capacity by 31.10%. Smooth thickness optimisation gains 25.74%, and 15.03% with a mode-1 imperfection.</p>
      <p><a href="https://github.com/syednafizreja/stress-line-ribs-shell-buckling">Code</a> · <a href="https://doi.org/10.5281/zenodo.24560903">DOI</a></p>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <h3>ShellBench</h3>
      <p>A lighter floor means little if the seismic frame spends the saving. OpenSeesPy frames of 3 to 8 storeys and CalculiX shell floors, 5,184 designs and 287 tests, cut whole-building A1-A3 carbon by a median 5.7% in 32 of 33 frames. Floors alone were 14.3%.</p>
      <p><a href="https://github.com/syednafizreja/ShellBench">Code</a> · <a href="https://doi.org/10.5281/zenodo.24194144">Dataset</a></p>
    </td>
    <td width="50%" valign="top">
      <h3>ShellForm and ShellLab</h3>
      <p>Gravity-only against seismic-aware force density, 168 shells from 0 to 0.6 g: 79 of 84 carbon pairs stay within 5%, because buckling and minimum thickness govern. ShellLab is the same equilibrium in Three.js, within 10^-13 m of the Python solver.</p>
      <p><a href="https://github.com/syednafizreja/ShellForm">ShellForm</a> · <a href="https://github.com/syednafizreja/ShellLab">ShellLab</a> · <a href="https://syednafizreja.github.io/ShellLab/">Live tool</a></p>
    </td>
  </tr>
</table>

## What I am trying to figure out next

- A 1D isothermal return map is not a 3D thermomechanical model, and it does not yet carry cyclic fatigue.
- Imperfection-sensitive shell stability, homogenisation of ribbed surfaces, and enriched continua, where the classical shell stops being accurate. One mode-1 dent already cuts the thickness gain from 25.74% to 15.03%.
- Lightweight composite and hybrid systems whose seismic detailing does not wipe out the embodied-carbon gain.

## Toolbox

Solvers and mechanics: OpenSeesPy · CalculiX · Gmsh · force-density form-finding

Scientific stack: Python · NumPy · SciPy · PyTorch · pytest · Three.js · LaTeX / Tectonic
