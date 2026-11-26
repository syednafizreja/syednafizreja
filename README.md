<p align="center">
  <img src="./assets/hero.svg" width="100%" alt="Syed Nafiz Reja Hasib. Computational structural mechanics: shells, superelastic alloys, and low-carbon seismic design. Animated thin-shell wireframe and a NiTi hysteresis loop.">
</p>

## About

I started by breaking things on purpose. After a civil engineering degree at Southwest Petroleum University, I spent two years at Denco Manufacturing cycling real superelastic NiTi components until they told me how they fail.

The solvers came after that. I wanted to see where a clean constitutive model, a thin shell, or a low-carbon floor meets earthquakes, buckling imperfections, and a carbon count that does not care how elegant the picture was.

The interesting part is usually the collision, not the diagram.

<p>
  <a href="https://syednafizreja.github.io/"><kbd>Portfolio</kbd></a>
  &nbsp;
  <a href="https://orcid.org/0009-0002-7162-7890"><kbd>ORCID</kbd></a>
  &nbsp;
  <a href="https://doi.org/10.5281/zenodo.24559613"><kbd>NiTi diagrid preprint</kbd></a>
  &nbsp;
  <a href="https://doi.org/10.5281/zenodo.24560903"><kbd>Shell buckling preprint</kbd></a>
</p>

## What this GitHub is about

<table>
  <tr>
    <td width="50%" valign="top">
      <h3>diagrid-seismic-opt</h3>
      <p>Auricchio-Sacco 1D return map, PyTorch inverse identification, OpenSeesPy, a Gaussian-process surrogate, and NSGA-II.</p>
      <p>Residual drift fell from 0.0659% to 0.0175%. Peak drift rose from 1.79% to 3.40%, and embodied carbon rose by 620.9 kgCO2e. The model is 1D and isothermal.</p>
      <p><a href="https://github.com/syednafizreja/diagrid-seismic-opt">Code</a> · <a href="https://doi.org/10.5281/zenodo.24559613">10.5281/zenodo.24559613</a></p>
    </td>
    <td width="50%" valign="top">
      <h3>Stress-line ribs versus thickness</h3>
      <p>CalculiX linear buckling, Scordelis-Lo and Zoelly benchmarks, and mode-1 geometric imperfections. Public repo: <code>stress-line-ribs-shell-buckling</code>.</p>
      <p>Stress-line ribs lost 31.10% of buckling capacity. An optimised thickness field gained 25.74%, and 15.03% with a mode-1 imperfection. Elastic only.</p>
      <p><a href="https://github.com/syednafizreja/stress-line-ribs-shell-buckling">Code</a> · <a href="https://doi.org/10.5281/zenodo.24560903">10.5281/zenodo.24560903</a></p>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <h3>ShellBench</h3>
      <p>OpenSeesPy and CalculiX on 5,184 shell-floor designs, checked by 287 tests.</p>
      <p>Median whole-building A1-A3 carbon fell by 5.7% on 32 of 33 reinforced-concrete frames. Floor-only gains are diluted by the seismic frame.</p>
      <p><a href="https://github.com/syednafizreja/ShellBench">Code</a></p>
    </td>
    <td width="50%" valign="top">
      <h3>ShellForm and ShellLab</h3>
      <p>Force-density form-finding, with the same solver in Three.js in the browser.</p>
      <p>79 of 84 seismic pairs stay within 5% carbon. Buckling and minimum thickness govern over the form-finding choice.</p>
      <p><a href="https://github.com/syednafizreja/ShellForm">ShellForm</a> · <a href="https://github.com/syednafizreja/ShellLab">ShellLab</a> · <a href="https://syednafizreja.github.io/ShellLab/">Live tool</a></p>
    </td>
  </tr>
</table>

## What I am trying to figure out next

- How a 1D isothermal shape-memory return map becomes a 3D thermomechanical model that can also carry cyclic fatigue. The diagrid result stops at the isothermal bar.
- How imperfection-sensitive shell stability, homogenisation of ribbed surfaces, and enriched continua change a buckling number. One mode-1 imperfection already cuts the thickness gain from 25.74% to 15.03%, and the comparison is still elastic.
- How a lightweight composite or hybrid system stays standing in an earthquake without giving back the carbon it saved. Shell floors cut median whole-building A1-A3 carbon by 5.7% on 32 of 33 frames. The NiTi devices added 620.9 kgCO2e.

## Toolbox

<kbd>OpenSeesPy</kbd> &nbsp; <kbd>CalculiX</kbd> &nbsp; <kbd>Python / PyTorch</kbd> &nbsp; <kbd>Gmsh</kbd> &nbsp; <kbd>Three.js</kbd> &nbsp; <kbd>LaTeX</kbd>
