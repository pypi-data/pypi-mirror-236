# Welcome to REMix

REMix is addressing research questions in the field of energy system analysis.
The main focus is on the broad techno-economical assessment of possible future
energy system designs and analysis of interactions between technologies.

```{figure} /_static/images/DLR_Logo_REMix_full.svg
:class: only-light
:scale: 200 %
:alt: REMix logo
```

```{figure} /_static/images/DLR_Logo_REMix_full_darkmode.svg
:class: only-dark
:scale: 200 %
:alt: REMix logo
```

This will allow system analysts to inform policy makers and technology
researchers to gain a better understanding of both the system and individual
components.

(remix_key_features)=

## Key Features

To know if REMix is apt for your project take into account these key features:

**Large Models**:
REMix is developed with large models in mind.
This means high spatial and technological resolutions.

**Path Optimization**:
Multi-year analyses are built into the framework.

**Custom accounting approaches**:
The indicator module allows for a very flexible definition of what contributes to the objective functions.

**Flexible modeling**:
There is not a single way of modeling technologies in REMix.
With the {ref}`core modules<modeling_concept_label>` you can find the best way of integrating your modeling needs.

**Multi-criteria optimization**:
Apart from running a cost minimization, also other criteria like ecological or resilience indicators can be taken into account in the objective function.

## Navigation

`````{grid} 4
````{grid-item-card}  About REMix
:link: about_label
:link-type: ref

- What is REMix?
- Feature Overview

````
````{grid-item-card}  Getting Started
:link: getting_started_label
:link-type: ref

- Installation
- Learning REMix
- Tutorials
- Example Applications

````
````{grid-item-card}  Documentation
:link: documentation_label
:link-type: ref

- Modeling Concepts
- API Documentation
- Literature References

````
````{grid-item-card}  Contributing
:link: contributing_label
:link-type: ref

- What to contribute
- How to contribute

````
`````

## Installation

Install with:

```
pip install remix.framework
```

To get git versions:

```
git clone [TODO]
pip install -e ./framework
```

## Recent Publications

-   [Wetzel et al. (2023): "Green energy carriers and energy sovereignty in a climate neutral European energy system"](10.1016/j.renene.2023.04.015)
-   [Gils et al. (2022): "Model-related outcome differences in power system models with sector coupling - quantification and drivers"](10.1016/j.rser.2022.112177)[^1]
-   [Gils et al. (2021): "Interaction of hydrogen infrastructures with other sector coupling options towards a zero-emission energy system in Germany"](10.1016/j.renene.2021.08.016)[^1]
-   [Sasanpour et al. (2021): "Strategic policy targets and the contribution of hydrogen in a 100% renewable European power system"](10.1016/j.egyr.2021.07.005)[^1]

## Contact

Do not hesitate to ask questions about REMix in the [openmod forum](https://forum.openmod.org/tag/remix).

## License

```{eval-rst}
.. include:: /../LICENSE
```

```{toctree}
:maxdepth: 3
:hidden:

about/index
```

```{toctree}
:maxdepth: 3
:hidden:

getting-started/index
```

```{toctree}
:maxdepth: 3
:hidden:

documentation/index
```

```{toctree}
:maxdepth: 3
:hidden:

contributing/index
```

## Acknowledgments

The development of the REMix model version published open source was made
possible by the funding of BMWK and BMBF in the projects UNSEEN (BMWK, FKZ
03EI1004A), Sesame Seed (BMWK, FKZ 03EI1021B), Fahrplan Gaswende (BMWK, FKZ
03EI1030B), ReMoDigital (BMWK, FKZ 03EI1020B), MuSeKo (BMWK, FKZ 03ET4038B),
INTEEVER-II (BMWK, FKZ 03ET4069A), START (BMBF, FKZ 03EK3046D), HINT (BMBF, FKZ
03SF0690) as well as the DLR internal projects NaGsys and CarnotBat
(Programmorientierte Förderung der Helmholtz-Gemeinschaft).

## Footnotes

[^1]: These papers were still using a non-open legacy version of the REMix framework
