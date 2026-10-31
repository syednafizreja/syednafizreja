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

<!-- AUTO:badges -->
[![Website](https://img.shields.io/badge/Website-syednafizreja.github.io-0ea5e9?style=flat-square&logo=githubpages&logoColor=white)](https://syednafizreja.github.io/)
[![ORCID](https://img.shields.io/badge/ORCID-0009--0002--7162--7890-a6ce39?style=flat-square&logo=orcid&logoColor=white)](https://orcid.org/0009-0002-7162-7890)
[![ResearchGate](https://img.shields.io/badge/ResearchGate-Syed_Nafiz_Reja_Hasib-00CCBB?style=flat-square&logo=researchgate&logoColor=white)](https://www.researchgate.net/profile/Syed-Nafiz-Reja-Hasib)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-syednafizreja-0a66c2?style=flat-square)](https://www.linkedin.com/in/syednafizreja)
[![Email](https://img.shields.io/badge/Email-syednafiz2811%40gmail.com-0284c7?style=flat-square&logo=gmail&logoColor=white)](mailto:syednafiz2811@gmail.com)
![Location](https://img.shields.io/badge/Location-Guangdong%2C_China-475569?style=flat-square&logo=googlemaps&logoColor=white)
[![Status](https://img.shields.io/badge/Status-Open_to_PhD_%2F_MScR_Collaborations-0284c7?style=flat-square)](https://syednafizreja.github.io/)
<!-- /AUTO:badges -->

</div>

---

### Research Profile

I design lightweight concrete shell structures that stay safe during seismic excitation while cutting material volume and lifecycle embodied carbon through open, verified computation. My undergraduate thesis was the hand calculation and capacity design of a four-storey reinforced concrete frame building in Panzhihua, Sichuan (Seismic Intensity 7, 0.10 g) under Chinese design codes (GB 50009, GB 50010, GB 50011).

I run two open computational structural mechanics projects extending that baseline:
* **[ShellBench](https://github.com/syednafizreja/ShellBench)** evaluates how thin-shell floor topologies reduce whole-building A1-A3 embodied carbon in seismic RC frames across varying storey counts and peak ground accelerations (0.05-0.40 g).
* **[ShellForm](https://github.com/syednafizreja/Shellform)** quantifies the embodied carbon penalty of seismic resilience in form-found concrete shells, testing whether seismic-aware form-finding outperforms post-hoc thickening of gravity-only equilibrium geometries.

Prior to graduate research, I worked for <!-- AUTO:tenure -->2 years 10 months<!-- /AUTO:tenure --> as a project engineer in precision manufacturing and micro-CNC operations. I managed automated inspection lines, defect detection, and fatigue-life testing under strict Root-Cause Failure Analysis (CAPA) frameworks — an experience that reinforced my commitment never to trust a numerical structural model until it has been verified against independent analytical solutions, physical hand calculations, and rigorous unit testing.

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

<!-- AUTO:projects -->
#### [`ShellBench: Whole-Building Embodied Carbon of Thin-Shell Floors`](https://github.com/syednafizreja/ShellBench)
*Lead Researcher & Developer · Python, OpenSeesPy, CalculiX, Gmsh · Open-Source (MIT)*
* **Research Problem:** How significantly do funicular concrete shell floors reduce A1-A3 embodied carbon in code-designed RC frame structures across 3–8 storeys when strict diaphragm action, perimeter ties, and seismic chord demands are enforced?
* **Validation Baseline:** Audited my hand-calculated thesis frame building and turned its results into automated verification targets.
* **Verification Pipeline:** Automated suite of 132 continuous integration tests checking internal moments, shear distributions, and lateral drift limits under gravity, wind, and response-spectrum seismic excitation.
* **Planned:** Pre-registered parametric sweep over ground accelerations (0.05-0.40 g), a Zenodo DOI from v0.1, and machine-learning surrogate models.
* **Status (31 Oct 2026):** Week 1 complete. Anchor model built and checked, shell floor work started, first release v0.0.1.

#### [`ShellForm: Seismic Resilience vs. Carbon Cost in Form-Found Shells`](https://github.com/syednafizreja/Shellform)
*Lead Researcher & Developer · Python, CalculiX, Three.js*
* **Research Problem:** Measures the direct embodied-carbon consequence of making form-found shell geometries earthquake-resistant, extending the seismic form-finding methods of Michiels & Adriaenssens (2017–2018) with standardized carbon accounting (GB/T 51366 and ICE inventory).
* **Computational Scope:** Parametric matrix of 168 sized shells defined across support topologies, rise-to-span ratios, and ground acceleration ranges (0-0.6 g). Runs are planned.
* **Deliverables:** Open-access interactive Three.js design space explorer, in development.
* **Status (31 Oct 2026):** Pre-registration approved 30 Oct 2026. One shell analysed in CalculiX (static, modal, buckling), 31 tests, both form-finding strategies implemented and tested.

#### [`Parametric Aviation-Terminal Canopy Optimization`](https://github.com/syednafizreja/parametric-canopy-carbon-optimization)
*Independent Computational Design Prototype · JavaScript, Python, WebGL*
* Live web prototype linking canopy curvature to real-time structural proxy metrics and A1-A3 embodied carbon estimates. A simplified, screening-level research demo.
* **Live demo:** [syednafizreja.github.io/parametric-canopy-carbon-optimization](https://syednafizreja.github.io/parametric-canopy-carbon-optimization/)

#### [`Nano-Modified Warm-Mix Asphalt: Durability & Life-Cycle Assessment`](https://github.com/syednafizreja/nano-wma-lca-model)
*Sole Researcher · Python, Finite Element Modeling, LCA*
* Built an object-oriented Python engine linking empirical moisture-damage laboratory metrics (Tensile Strength Ratio) with climate-driven weathering models.
* Comparative cradle-to-gate LCA found a 5.2% production GWP decrease (61.31 to 58.15 kg CO2e/t). With a 15% service-life extension, annualized lifecycle GWP falls by **17.5%**.
* **Related:** [FE + LCA pavement model](https://github.com/syednafizreja/nano-wma-pavement-carbon)
<!-- /AUTO:projects -->

---

### Selected Publications & Preprints

#### Peer-Reviewed Journal Articles
<!-- AUTO:publications -->
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
<!-- /AUTO:publications -->

#### Manuscripts Under Review & In Preparation
<!-- AUTO:manuscripts -->
* **A climate-driven moisture-damage model for nano-modified warm mix asphalt with BIM-ready outputs**  
  **S. N. R. Hasib** (Sole Author). *Under review, Discover Civil Engineering* (Submitted Oct 2026).
* **Coupled finite-element and life-cycle assessment of nano-silica warm mix asphalt pavements**  
  **S. N. R. Hasib** (Sole Author). *In preparation* (Planned submission Nov 2026).
* **Whole-building embodied carbon of thin-shell floors in seismic RC frames (ShellBench, Paper 1)**  
  **S. N. R. Hasib** (Sole Author). *In preparation* (Planned submission Nov 2026).
* **The carbon cost of seismic resilience: gravity-only versus seismic-aware form-finding of concrete shells (ShellForm)**  
  **S. N. R. Hasib** (Sole Author). *In preparation*.
<!-- /AUTO:manuscripts -->

#### Technical Reports & Open Preprints
<!-- AUTO:reports -->
* **Lateral-Load Analysis and Capacity Design of a 4-Storey RC Frame Under GB 50011-2010: Fully Documented Case Study from Panzhihua, Sichuan** (Complete thesis drawings & calculations)  
  `doi:` [10.13140/RG.2.2.26247.15522](https://doi.org/10.13140/RG.2.2.26247.15522)
* **Quantifying the Environmental Benefit of Nano-Modified Warm Mix Asphalt: A Comparative LCA Linked to Durability Performance**  
  `doi:` [10.13140/RG.2.2.12376.46089](https://doi.org/10.13140/RG.2.2.12376.46089)
<!-- /AUTO:reports -->

---

### Technical Matrix

| Domain | Methods, Frameworks & Tooling |
| :--- | :--- |
| **Structural Engineering** | Seismic RC frame design (GB 50009, GB 50010, GB 50011, GB 55002); D-value lateral analysis; Response spectrum analysis (RSA); Capacity design & drift limits; Force Density Method (FDM) |
| **Computation & Simulation** | **Python** (NumPy, SciPy, Matplotlib, pytest); **OpenSeesPy**; **CalculiX** (FEA shell elements); **Gmsh** (parametric mesh generation); Three.js / JavaScript; LaTeX |
| **BIM & CAD Systems** | **AutoCAD** (Advanced drafting & structural detailing); **Autodesk Revit** & lightweight BIM digital-twin pipelines |
| **Embodied Carbon & LCA** | A1-A3 cradle-to-gate Life-Cycle Assessment; Carbon factors via **GB/T 51366** & **ICE Inventory** |
| **Research & Open Science** | Continuous Integration with GitHub Actions; Pre-registered hypotheses; Analytical benchmark checks; Versioned releases |
| **Quality & Manufacturing** | Micro-CNC program control; automated inspection QC; alloy fatigue-life analysis; Root-Cause Failure Analysis (CAPA) |

---

### Education & Professional Experience

<!-- AUTO:timeline -->
* **Southwest Petroleum University (SWPU)** · Chengdu, China (Sep 2019 – Jun 2023)  
  *B.Eng. in Civil Engineering* · Weighted Average: **84.05/100** (GPA 3.41/5.0)  
  *Awarded full Chinese Government Scholarship (CSC)*  
  *Thesis:* Structural design of a four-storey RC frame building in Panzhihua, Sichuan (Seismic Intensity 7, 0.10 g). Grade: **87/100**.
* **Denco Medical** · Guangdong, China (Jan 2024 – Oct 2026, 2 yr 10 mo)  
  *Project Engineer — Precision Manufacturing & Quality Engineering*  
  Managed automated lines, dimensional micro-tolerances, alloy heat-treatment fatigue evaluation, and CAPA resolution pipelines.
* **Foreign Language Corner, SWPU** · Chengdu, China (Oct 2019 – Jun 2023)  
  *Senior ESL Instructor & Event Coordinator*
<!-- /AUTO:timeline -->

---

### Professional Affiliations, Languages & Continuing Education

* **Affiliations:** Member, Institution of Engineers, Bangladesh (IEB)
* **Certifications:** *Bayesian Statistics: From Concept to Data Analysis* (UC Santa Cruz) · *AutoCAD for Design & Drafting* (Autodesk Certified)
* **Languages:** Bengali (Native) · English (Full Professional) · Chinese (Intermediate, ~B1) · Hindi (Conversational) · French (Beginner)
* **Discipline & Conditioning:** Muay Thai and Mixed Martial Arts (MMA) training; systematic inquiry into behavioral decision-making and human psychology.

<div align="center">
  <sub>Generated with open Python & SMIL vector generators. Updated automatically via daily GitHub Actions CI.</sub>
</div>