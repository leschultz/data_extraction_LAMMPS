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
                           <frequency of data acqusition>,
                           step=<list of steps to get RDF>,
                           interval=<tuple of RDF versus time interval>)'

            - series is the temperature at which all runs are averaged for MSD.
              For instance, 500K will average 500K_1, 500K_2, and so on.

            - step is an optional argument that will default to None if not
              defined.

            - interval is an optional argument that will default to
              (start, stop) if not defined

	Example: python3 -c 'from averages import avg;
                             value = avg("1K", 28000, 48000, 100,
                             step=[100, 20000], interval=(10000, 28000))'
