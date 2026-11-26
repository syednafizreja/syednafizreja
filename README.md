# Syed Nafiz Reja Hasib

BEng Civil Engineering, Southwest Petroleum University. Two years of experimental cyclic-durability testing on superelastic NiTi components at Denco Manufacturing.

That testing led to independent research in computational solid mechanics, seismic systems, thin-shell stability, and embodied carbon.

[Portfolio website](https://syednafizreja.github.io/) · [ORCID 0009-0002-7162-7890](https://orcid.org/0009-0002-7162-7890)

## Flagship research

| Project | Mechanics and methods | Key finding and observed limitation | Code and preprint |
| --- | --- | --- | --- |
| Diagrid frames with superelastic NiTi | Auricchio-Sacco 1D return map, PyTorch inverse identification, OpenSeesPy, Gaussian-process surrogate and NSGA-II | Residual drift fell from 0.0659% to 0.0175%. Peak drift rose from 1.79% to 3.40%, and embodied carbon rose by 620.9 kgCO2e. The constitutive model is 1D and isothermal. | [Code](https://github.com/syednafizreja/diagrid-seismic-opt) · [10.5281/zenodo.24559613](https://doi.org/10.5281/zenodo.24559613) |
| Equal-volume shell buckling | CalculiX linear buckling, Scordelis-Lo and Zoelly benchmarks, mode-1 geometric imperfections | Stress-line ribs lost 31.10% of buckling capacity. An optimised thickness field gained 25.74%, and 15.03% once a mode-1 imperfection is included. The analysis is elastic only. | [Code](https://github.com/syednafizreja/stress-line-ribs-shell-buckling) · [10.5281/zenodo.24560903](https://doi.org/10.5281/zenodo.24560903) |
| ShellBench | OpenSeesPy and CalculiX across 5,184 shell-floor designs, with 287 tests | Median whole-building A1-A3 carbon fell by 5.7% on 32 of 33 reinforced-concrete frames. Floor-only gains are diluted by seismic frame demands. | [Code](https://github.com/syednafizreja/ShellBench) |
| ShellForm and ShellLab | Force-density form-finding, with a Three.js solver in the browser | 79 of 84 seismic pairs stay within 5% carbon. Buckling and minimum thickness govern over the form-finding choice. | [ShellForm](https://github.com/syednafizreja/ShellForm) · [ShellLab](https://github.com/syednafizreja/ShellLab) · [Live tool](https://syednafizreja.github.io/ShellLab/) |

## Open research questions (2027-2029 graduate focus)

- **STRAINS.** Three-dimensional thermomechanical constitutive models and cyclic fatigue of shape-memory alloys. The diagrid result uses a 1D isothermal return map, so temperature coupling and 3D cyclic degradation are outside it.
- **MS2.** Imperfection-sensitive shell stability, homogenisation, and enriched continua. The rib comparison is elastic, and a mode-1 imperfection already cuts the thickness gain from 25.74% to 15.03%.
- **FRP++.** Lightweight fibre-reinforced composite and hybrid low-carbon structural systems. Shell floors cut median whole-building A1-A3 carbon by 5.7% on 32 of 33 frames, while the NiTi devices added 620.9 kgCO2e. The frame and the device still bound the saving.

## Technical stack

Solvers and mechanics: OpenSeesPy, CalculiX, force-density form-finding, Auricchio-Sacco return mapping.

Scientific Python and machine learning: PyTorch inverse identification, Gaussian-process surrogates, NSGA-II.

Verification and web: the ShellBench suite (287 tests), and ShellLab in Three.js checked against ShellForm.
