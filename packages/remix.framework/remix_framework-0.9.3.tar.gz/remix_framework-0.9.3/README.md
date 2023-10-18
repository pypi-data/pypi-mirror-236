# REMix

REMix is addressing research questions in the field of energy system analysis.
The main focus is on the broad techno-economical assessment of possible future
energy system designs and analysis of interactions between technologies. This
will allow system analysts to inform policy makers and technology researchers
to gain a better understanding of both the system and individual components.

The documentation of REMix is hosted online: [REMix docu](https://dlr-ve.gitlab.io/esy/remix/framework/).

Do not hesitate to ask questions about REMix in the [openmod forum](https://forum.openmod.org/tag/remix).

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
With the flexible [modelling concept](https://dlr-ve.gitlab.io/esy/remix/framework/dev/documentation/modeling-concept/index.html) you can find the best way of integrating your modeling needs.

**Multi-criteria optimization**:
Apart from running a cost minimization, also other criteria like ecological or resilience indicators can be taken into account in the objective function.

## How to use

To run a REMix model, users need a recent [GAMS](https://www.gams.com/)
installation (version 37 or above).

To install REMix, clone this repository, create a new Python environment and install it through pip.

Clone with ssh:

```bash
git clone git@gitlab.com:dlr-ve/esy/remix/framework.git
```

Clone with https:

```bash
git clone https://gitlab.com/dlr-ve/esy/remix/framework.git
```

```bash
cd framework
conda create -n remix-env python
conda activate remix-env
pip install -e .[dev]
```

Please find the extensive [installation instructions in the online documentation](https://dlr-ve.gitlab.io/esy/remix/framework/dev/getting-started/install-remix.html).

Additionally, a data project is required which contains the parametrization of
the model scope and technologies. We provide
[example projects](https://gitlab.com/dlr-ve/remix/projects), which can be used
to gain first experience with running the REMix optimization model.

To run your model, you can use the command line interface:

```bash
conda activate remix-env
remix run --datadir=/path/to/data/folder/of/your/model/data
```

All configuration options available with the command line tool are documented
in the [technical documentation](https://dlr-ve.gitlab.io/esy/remix/framework/dev/documentation/tech-docs/index.html).

## Latest publications using REMix

* [Wetzel et al. (2023): "Green energy carriers and energy sovereignty in a climate neutral European energy system"](https://doi.org/10.1016/j.renene.2023.04.015)
* [Gils et al. (2022): "Model-related outcome differences in power system models with sector coupling - quantification and drivers"](https://doi.org/10.1016/j.rser.2022.112177)[^1]
* [Gils et al. (2021): "Interaction of hydrogen infrastructures with other sector coupling options towards a zero-emission energy system in Germany"](https://doi.org/10.1016/j.renene.2021.08.016)[^1]
* [Sasanpour et al. (2021): "Strategic policy targets and the contribution of hydrogen in a 100% renewable European power system"](https://doi.org/10.1016/j.egyr.2021.07.005)[^1]

## Contribute to REMix

Contributions are welcome, and they are greatly appreciated! Every bit
helps, and credit will always be given. To learn how to contribute to REMix we
have included a respective section in our
[online documentation](https://dlr-ve.gitlab.io/esy/remix/framework/dev/contributing/index.html).

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
