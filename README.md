# LAMMPS Data Extraction Tool

This tool gathers diffusivity, rdf, uncertainties, and settling data for CCT curves in LAMMPS. A specific file format is needed along with directory structure for this tool to work.

## Getting Started

To attain all analysis scripts run

```
git clone git@github.com:leschultz/data_extraction_LAMMPS.git
```

### Prerequisites

Python 3.6.6 along with standard packages is required. This includes PyQt5 (pip install PyQt5). Anaconda is NOT recomended. The following packages are required:

```
numpy
scipy
pandas
PyQt5
matplotlib
```

Additionally, Ovito 3.0.0 is used for self diffusion and RDF calcualtions. Make sure to install Ovito and modify PYTHO
NPATH to point to the following directory:

```
ovito/lib/ovito/plugins/python
```

Any data analysed must have the following format (note that trajectories are unwrapped):

```
./testdata
└── runnamefolder
    ├── dep.in
    ├── test.out
    └── unwrappedcoordinatestraj.lammpstrj
```

### Installing

Clone the repository. For instance, 
```
git clone git@github.com:leschultz/data_extraction_LAMMPS.git
```

Modify PYTHONPATH to point to the directory cloned. It is preferable to modify environment variables in the .bashrc or .zshrc files in the home directory. For instance,

```
export PYTHONPATH=/home/myname/tools/data_extraction_LAMMPS:$PYTHONPATH
```

## Running

There are three main scripts for this tool that can be run independelty or together. Within the tool, there is a samplefile directory that containts a sample run. The commands in the following sections should work to create a sample export if they are run in the tool directory.

### Ovito Data Collection

This tool calculates the mean squared displacement (MSD), diffusion, and radial distribution function (RDF), for a trajectory file exported by LAMMPS. Additionally, error propagation of data is done using various methods on multiple origins data on diffusion from MSD. Methods to determine when data is settled for analysis is also implemented.
The following line can be used to gather self diffusion and RDF data from Ovito:

The following line can be used to run the tool:

```
python3 -m runtypes.runsteps -i ./samplefiles/sampledata -o ./samplefiles/sampleexport -p ./samplefiles/templateinputfile.txt
```

The option -i points to the folder where data was collected from LAMMPS. Option -o points to the folder where data is to be exported. Option -p points to a file that has certain parameters for analysis. A template is provided under samplefiles.

## Coding Style

Python scripts follow PEP 8 guidelines. A usefull tool to use to check a coding style is pycodestyle.

```
pycodestyle script.py
```

## Authors

* **Lane Schultz** - *Initial work* - [leschultz](https://github.com/leschultz)

* **Benjamin Afflerback** - *CCT runs* - [bafflerbach](https://github.com/bafflerbach)

## Acknowledgments

* The Computational Materials Group (CMG) at the University of Wisconsin - Madison
* Dr. Dane Morgan for computational material science guidence
* Dr. Izabela Szlufarska for computational material science guidence
