<div align="center">

<h3><code>nafiz@formfoundry:~/structures$ ./visualize_dispatch.sh --palette=fea-cyan</code></h3>

<img src="./contrib-heatmap.svg" width="920" alt="53-Week Continuous Computational Structural Engineering Commit Timeline" />

<br><br>

<h3><code>nafiz@formfoundry:~/structures$ neofetch --profile=academic</code></h3>

<table border="0" cellpadding="0" cellspacing="0">
  <tr>
    <td width="420" valign="top" align="center">
      <img src="./structural-shell.svg" width="410" alt="Parametric Funicular Vault & Finite Element Stress Mesh" />
    </td>
    <td width="15"></td>
    <td width="520" valign="top" align="center">
      <img src="./info-card.svg" width="510" alt="Neofetch Terminal Researcher Profile — Syed Nafiz Reja Hasib" />
    </td>
  </tr>
</table>

<br>

[![ORCID](https://img.shields.io/badge/ORCID-0009--0002--7162--7890-a6ce39?style=flat-square&logo=orcid&logoColor=white)](https://orcid.org/0009-0002-7162-7890)
[![ResearchGate](https://img.shields.io/badge/ResearchGate-Syed_Nafiz_Reja_Hasib-00CCBB?style=flat-square&logo=researchgate&logoColor=white)](https://www.researchgate.net/profile/Syed-Nafiz-Reja-Hasib)
[![Email](https://img.shields.io/badge/Email-syednafiz2811%40gmail.com-0284c7?style=flat-square&logo=gmail&logoColor=white)](mailto:syednafiz2811@gmail.com)
[![Location](https://img.shields.io/badge/Location-Guangdong%2C_China-475569?style=flat-square&logo=googlemaps&logoColor=white)](https://maps.google.com)
[![Status](https://img.shields.io/badge/Status-Open_to_PhD_%2F_MScR_Collaborations-0284c7?style=flat-square)](#)

</div>

---

### Research Profile

I design lightweight concrete shell structures that stay safe during seismic excitation while cutting material volume and lifecycle embodied carbon through open, verified computation. My undergraduate thesis was the hand calculation and capacity design of a four-storey reinforced concrete frame building in Panzhihua, Sichuan (Seismic Intensity 7, 0.10 g) under Chinese design codes (GB 50009, GB 50010, GB 50011).

I run two open computational structural mechanics projects extending that baseline:
* **[ShellBench](https://github.com/syednafizreja/ShellBench)** evaluates how thin-shell floor topologies reduce whole-building A1-A3 embodied carbon in seismic RC frames across varying storey counts and peak ground accelerations (0.05-0.40 g).
* **[ShellForm](https://github.com/syednafizreja/ShellForm)** quantifies the embodied carbon penalty of seismic resilience in form-found concrete shells, testing whether seismic-aware form-finding outperforms post-hoc thickening of gravity-only equilibrium geometries.

Prior to graduate research, I worked for 2.5 years as a project engineer in precision manufacturing and micro-CNC operations. I managed automated inspection lines, defect detection, and fatigue-life testing under strict Root-Cause Failure Analysis (CAPA) frameworks — an experience that reinforced my commitment never to trust a numerical structural model until it has been verified against independent analytical solutions, physical hand calculations, and rigorous unit testing.

```
Primary Inquiries:
├── Computational form-finding & structural optimization (Force Density Method)
├── Seismic demand vs. embodied carbon tradeoffs (GB 50011, Eurocode 8, GB/T 51366, ICE)
├── Open, tested, reproducible FEA workflows (OpenSeesPy, CalculiX, Gmsh, pytest)
├── Machine-learning surrogates for early-stage structural decision support
└── Resilient, low-carbon infrastructure for extreme environments
```

---

### Active Research Projects & Software

#### [`ShellBench: Whole-Building Embodied Carbon of Thin-Shell Floors`](https://github.com/syednafizreja/ShellBench)
*Lead Researcher & Developer · Python, OpenSeesPy, CalculiX, Gmsh · Open-Source (MIT)*
* **Research Problem:** How significantly do funicular concrete shell floors reduce A1-A3 embodied carbon in code-designed RC frame structures across 3–8 storeys when strict diaphragm action, perimeter ties, and seismic chord demands are enforced?
* **Validation Baseline:** Fully audited my hand-calculated thesis frame building, resolving 16 input ambiguities, cataloging 21 doubtful printed values, and establishing 8 thesis result matrices as automated verification targets.
* **Verification Pipeline:** Automated suite of 114 continuous integration tests checking internal moments, shear distributions, and lateral drift limits under gravity, wind, and response-spectrum seismic excitation.
* **Release:** Pre-registered parametric study swept over ground accelerations (0.05-0.40 g) with Zenodo DOI and machine-learning surrogate models.

#### [`ShellForm: Seismic Resilience vs. Carbon Cost in Form-Found Shells`](https://github.com/syednafizreja/ShellForm)
*Lead Researcher & Developer · Python, CalculiX, Three.js*
* **Research Problem:** Measures the direct embodied-carbon consequence of making form-found shell geometries earthquake-resistant, extending the seismic form-finding methods of Michiels & Adriaenssens (2017–2018) with standardized carbon accounting (GB/T 51366 and ICE inventory).
* **Computational Scope:** Parametric matrix of 168 sized shells spanning varying support topologies, rise-to-span ratios, and ground acceleration ranges (0-0.6 g).
* **Deliverables:** Open-access interactive Three.js geometric design space explorer, validated against the Scordelis-Lo roof and pinched hemisphere benchmarks.

#### [`Parametric Aviation-Terminal Canopy Optimization`](https://github.com/syednafizreja)
*Independent Computational Design Prototype · JavaScript, Python, WebGL*
* Live web prototype linking complex canopy curvature to real-time structural proxy metrics and A1-A3 embodied carbon estimates to explore structural trade-offs instantaneously.

#### [`Nano-Modified Warm-Mix Asphalt: Durability & Life-Cycle Assessment`](https://github.com/syednafizreja)
*Sole Researcher · Python, Finite Element Modeling, LCA*
* Built an object-oriented Python engine linking empirical moisture-damage laboratory metrics (Tensile Strength Ratio) with climate-driven weathering models.
* Comparative cradle-to-gate LCA proved a 5.2% production GWP decrease (61.31 to 58.15 kg CO2e/t). A verified 15% service-life extension resulted in a **17.5% drop in annualized lifecycle GWP**.

---

### Selected Publications & Preprints

#### Peer-Reviewed Journal Articles
1. **Edge AI and IoT for Real-Time Structural Health Monitoring**  
   M. A. Hossain, M. G. Mostofa, M. A. Babu, **S. N. R. Hasib**, H. Arafat  
   *Journal of Artificial Intelligence and Technological Development*, 2(5), 80–111, 2026.  
   `doi:` [10.59324/jaitd.2026.2(5).07](https://doi.org/10.59324/jaitd.2026.2(5).07)

2. **Integration of Nano-Additives in Warm Mix Asphalt: Enhancing Moisture Resistance and Long-Term Durability**  
   P. M. S. Raihan, **S. N. R. Hasib**, M. Phiri  
   *European Journal of Theoretical and Applied Sciences*, 2(6), 451–461, 2024.  
   `doi:` [10.59324/ejtas.2024.2(6).39](https://doi.org/10.59324/ejtas.2024.2(6).39)

3. **Application of BIM in Civil Engineering**  
   S. A. Shimky, **S. N. R. Hasib**, S. M. W. Karim, S. Parven, M. Imran, M. E. H. Parvez, A. Ali  
   *European Journal of Theoretical and Applied Sciences*, 2(4), 595–622, 2024.  
   `doi:` [10.59324/ejtas.2024.2(4).51](https://doi.org/10.59324/ejtas.2024.2(4).51)

#### Manuscripts Under Review & In Preparation
* **A climate-driven moisture-damage model for nano-modified warm mix asphalt with BIM-ready outputs**  
  **S. N. R. Hasib** (Sole Author). *Under review, Discover Civil Engineering* (Submitted Oct 2026).
* **Coupled finite-element and life-cycle assessment of nano-silica warm mix asphalt pavements**  
  **S. N. R. Hasib** (Sole Author). *In preparation* (Planned submission Nov 2026).
* **Whole-building embodied carbon of thin-shell floors in seismic RC frames (ShellBench, Paper 1)**  
  **S. N. R. Hasib** (Sole Author). *In preparation* (Planned submission Nov 2026).
* **The carbon cost of seismic resilience: gravity-only versus seismic-aware form-finding of concrete shells (ShellForm)**  
  **S. N. R. Hasib** (Sole Author). *In preparation*.

#### Technical Reports & Open Preprints
* **Lateral-Load Analysis and Capacity Design of a 4-Storey RC Frame Under GB 50011-2010: Fully Documented Case Study from Panzhihua, Sichuan** (Complete thesis drawings & calculations)  
  `doi:` [10.13140/RG.2.2.26247.15522](https://doi.org/10.13140/RG.2.2.26247.15522)
* **Quantifying the Environmental Benefit of Nano-Modified Warm Mix Asphalt: A Comparative LCA Linked to Durability Performance**  
  `doi:` [10.13140/RG.2.2.12376.46089](https://doi.org/10.13140/RG.2.2.12376.46089)

---

### Technical Matrix

| Domain | Methods, Frameworks & Tooling |
| :--- | :--- |
| **Structural Engineering** | Seismic RC frame design (GB 50009, GB 50010, GB 50011, GB 55002); D-value lateral analysis; Response spectrum analysis (RSA); Capacity design & drift limits; Force Density Method (FDM) |
| **Computation & Simulation** | **Python** (NumPy, SciPy, Matplotlib, pytest); **OpenSeesPy**; **CalculiX** (FEA shell elements); **Gmsh** (parametric mesh generation); Three.js / JavaScript; LaTeX |
| **BIM & CAD Systems** | **AutoCAD** (Advanced drafting & structural detailing); **Autodesk Revit** & lightweight BIM digital-twin pipelines |
| **Embodied Carbon & LCA** | A1-A3 cradle-to-gate Life-Cycle Assessment; Carbon factors via **GB/T 51366** & **ICE Inventory** |
| **Research & Open Science** | Continuous Integration with GitHub Actions; Pre-registered hypotheses; Analytical benchmark checks; Versioned releases via Zenodo |
| **Quality & Manufacturing** | Micro-CNC program control; automated inspection QC; alloy fatigue-life analysis; Root-Cause Failure Analysis (CAPA) |

---

### Education & Professional Experience

* **Southwest Petroleum University (SWPU)** · Chengdu, China (Sep 2019 – Jun 2023)  
  *B.Eng. in Civil Engineering* · Weighted Average: **84.05/100** (GPA 3.41/5.0)  
  *Awarded full Chinese Government Scholarship (CSC)*  
  *Thesis:* Structural design of a four-storey RC frame building in Panzhihua, Sichuan (Seismic Intensity 7, 0.10 g). Grade: **87/100**.
* **Denco Medical** · Guangdong, China (Jan 2024 – Oct 2026)  
  *Project Engineer — Precision Manufacturing & Quality Engineering*  
  Managed automated lines, dimensional micro-tolerances, alloy heat-treatment fatigue evaluation, and CAPA resolution pipelines.
* **Foreign Language Corner, SWPU** · Chengdu, China (Oct 2019 – Jun 2023)  
  *Senior ESL Instructor & Event Coordinator*

---

### Professional Affiliations, Languages & Continuing Education

* **Affiliations:** Member, Institution of Engineers, Bangladesh (IEB)
* **Certifications:** *Bayesian Statistics: From Concept to Data Analysis* (UC Santa Cruz) · *AutoCAD for Design & Drafting* (Autodesk Certified)
* **Languages:** Bengali (Native) · English (Full Professional) · Chinese (Intermediate, ~B1) · Hindi (Conversational) · French (Beginner)
* **Discipline & Conditioning:** Muay Thai and Mixed Martial Arts (MMA) training; systematic inquiry into behavioral decision-making and human psychology.

<div align="center">
  <sub>Generated with open Python & SMIL vector generators. Updated automatically via daily GitHub Actions CI.</sub>
</div>