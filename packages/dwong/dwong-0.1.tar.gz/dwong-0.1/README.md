# dwong, a package for DarkQuest.

dwong is a comprehensive Python package, created by student Dowling Wong, tailored for data analysis and neural network-based particle identification in the DarkQuest experiment. The aim of this project is to streamline DarkQuest's data analysis process by providing exemplary data-processing functions.

The package mainly contains four modules: dwong, dplot, dcsv and dkeras.
* dwong
  * emcal_bytuple
  * multi_clusters
  * h4_bytuple
  * prepare_data_bytuple
* dplot
  * emcal_evt(x, y, eng)
  * emcal_pdf(ntuple_name, filename, path)
* dkeras
* dcsv

  
![scheme](/logo/darkquest_schematic.png " inline image")
dwong is the main module for data analysis, developed with a high efficiency sequence of functions acquisiten data from n-tuple and 



[The source for this project is available here][src].

The metadata for a Python project is defined in the `pyproject.toml` file,
an example of which is included in this project. You should edit this file
accordingly to adapt this sample project to your needs.

----

This is the README file for the project.

The file should use UTF-8 encoding and can be written using
[reStructuredText][rst] or [markdown][md use] with the appropriate [key set][md
use]. It will be used to generate the project webpage on PyPI and will be
displayed as the project homepage on common code-hosting services, and should be
written for that purpose.

Typical contents for this file would include an overview of the project, basic
usage examples, etc. Generally, including the project changelog in here is not a
good idea, although a simple “What's New” section for the most recent version
may be appropriate.

[packaging guide]: https://packaging.python.org
[distribution tutorial]: https://packaging.python.org/tutorials/packaging-projects/
[src]: https://github.com/pypa/sampleproject
[rst]: http://docutils.sourceforge.net/rst.html
[md]: https://tools.ietf.org/html/rfc7764#section-3.5 "CommonMark variant"
[md use]: https://packaging.python.org/specifications/core-metadata/#description-content-type-optional
