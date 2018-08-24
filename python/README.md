Before using the tool, python setup.py needs to be run. Ovito 3 along with the
python module provided is required. Make sure to add from the COMPILED Ovito
folder the following paths:

    1) export PYTHONPATH=
                         <path to ovito>
                         /ovito/lib/ovito/plugins/python:$PYTHONPATH

    2) export QT_PLUGIN_PATH=
                              <path to ovito>
                              /ovito/lib/ovito/plugins_qt:$QT_PLUGIN_PATH

averages.py can be used to attain the averages between MSDs and it executes
analysis.py for all runs specifed in series. The variable value stores the
return value for steps and mean MSD.

	Usage: python3 -c 'from averages import avg;
                           value = avg(<series>, <start>, <stop>,
                           <time step used in LAMMPS>,
                           <list of steps to get RDF>,
                           <cut for RDF distance>
                           <number of bin for RDF>)'

            - series is the temperature at which all runs are averaged for MSD.
              For instance, 500K will average 500K_1, 500K_2, and so on.

            - start is the starting timestep for analysis

            - stop is the end timestep for analysis

            - time step used in LAAMPS is the amount of time per step

            - step is an optional argument that will default to None if not
              defined for RDF

            - cut is used to cut the maximum RDF analysis distance

            - bins is the number of bins used for RDF

	Example: python3 -c 'from averages import avg; value = avg("900K",
                            100000+33000, 100000+33000+36000, 0.001,
                            [100000, 100000+33000, 100000+33000+36000],
                            8, 50)'
