<p align="center">
  <img src="./assets/hero.svg" width="100%" alt="Syed Nafiz Reja Hasib. Computational structural mechanics: shells, superelastic alloys, and low-carbon seismic design. The spine runs from the alloy to the shell, the frame, and the form.">
</p>

I cycled superelastic NiTi at Denco Manufacturing until the parts failed in ways a clean datasheet would skip. The degree before that was civil engineering at Southwest Petroleum University. These repositories are the argument I wrote next: a mechanism, then the number, then the place the mechanism stops.

<p>
  <a href="https://syednafizreja.github.io/"><kbd>Portfolio</kbd></a>
  &nbsp;
  <a href="https://orcid.org/0009-0002-7162-7890"><kbd>ORCID</kbd></a>
  &nbsp;
  <a href="https://doi.org/10.5281/zenodo.24559613"><kbd>NiTi preprint</kbd></a>
  &nbsp;
  <a href="https://doi.org/10.5281/zenodo.24560903"><kbd>Shell preprint</kbd></a>
</p>

## Research spine

Alloy, then surface, then building, then form. The figure carries the result. The links open the code.

<p align="center">
  <img src="./assets/spine.svg" width="100%" alt="01 NiTi diagrid: residual drift 0.0659% to 0.0175%, peak drift 1.79% to 3.40%, carbon up 620.9 kgCO2e, 1D isothermal limit. 02 Ribs versus thickness: ribs minus 31.10%, optimised thickness plus 25.74%, plus 15.03% with a mode-1 imperfection, elastic only. 03 ShellBench: median whole-building A1-A3 carbon minus 5.7% on 32 of 33 frames, 5184 designs, 287 tests. 04 ShellForm and ShellLab: 79 of 84 seismic pairs within 5% carbon. Buckling and minimum thickness govern.">
</p>

<table>
  <tr>
    <td width="25%" valign="top"><a href="https://github.com/syednafizreja/diagrid-seismic-opt"><strong>01 NiTi diagrid</strong></a><br><a href="https://doi.org/10.5281/zenodo.24559613">Preprint</a></td>
    <td width="25%" valign="top"><a href="https://github.com/syednafizreja/stress-line-ribs-shell-buckling"><strong>02 Ribs vs thickness</strong></a><br><a href="https://doi.org/10.5281/zenodo.24560903">Preprint</a></td>
    <td width="25%" valign="top"><a href="https://github.com/syednafizreja/ShellBench"><strong>03 ShellBench</strong></a><br>OpenSeesPy and CalculiX</td>
    <td width="25%" valign="top"><a href="https://github.com/syednafizreja/ShellForm"><strong>04 ShellForm</strong></a><br><a href="https://github.com/syednafizreja/ShellLab">ShellLab</a> · <a href="https://syednafizreja.github.io/ShellLab/">Live tool</a></td>
  </tr>
</table>

## Still open

- A return map with temperature and a third dimension, plus a fatigue count that is still meaningful after the first earthquake. The diagrid bar is isothermal and one-dimensional.
- A shell that knows it is dented. One mode-1 imperfection already cuts the thickness gain from 25.74% to 15.03%, and the whole comparison is elastic.
- A lighter structural system that does not hand its carbon saving back to the seismic system. The floor saved a median 5.7% on 32 of 33 frames. The NiTi devices cost 620.9 kgCO2e.

## Toolbox

<kbd>OpenSeesPy</kbd> &nbsp; <kbd>CalculiX</kbd> &nbsp; <kbd>Python / PyTorch</kbd> &nbsp; <kbd>Gmsh</kbd> &nbsp; <kbd>Three.js</kbd> &nbsp; <kbd>LaTeX</kbd>
