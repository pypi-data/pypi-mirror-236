.. image:: https://img.pterclub.com/images/2023/01/06/logo.png

*mdapy* : Molecular Dynamics Analysis with Python
=====================================================

Overview
--------

The **mdapy** python library provides an array of powerful, flexible, and straightforward 
tools to analyze atomic trajectories generated from Molecular Dynamics (MD) simulations. The library is fully 
cross-platform, making it accessible to users in **Windows, Linux, and Mac OS**. 
Benefited by the `TaiChi <https://github.com/taichi-dev/taichi>`_ project, 
we can effectively accelerate the pure python code, bringing it closer to the speed of code written in C++. 
Furthermore, **mdapy** is highly parallelized, allowing users to leverage the resources of both multicore CPU and GPU. 
**mdapy** can directly handle the DUMP and DATA formats in `LAMMPS <https://www.lammps.org/>`_. 
Besides, all data in **mdapy** is stored in NDARRAY format in `NumPy <https://numpy.org/>`_\ , which enables easy integration 
with the scientific ecosystem in python and facilitates collaboration with other post-progressing 
tools such as `OVITO <https://www.ovito.org/>`_ and `freud <https://github.com/glotzerlab/freud>`_.


Resources
----------

- Homepage: `https://github.com/mushroomfire/mdapy <https://github.com/mushroomfire/mdapy>`_
- Documentation: `https://mdapy.readthedocs.io/ <https://mdapy.readthedocs.io/>`_
- Issue Tracker: `https://github.com/mushroomfire/mdapy/issues <https://github.com/mushroomfire/mdapy/issues>`_

Dependencies
------------

* `python <https://www.python.org/>`_ (3.8-3.11)
* `taichi>=1.6.0 <https://github.com/taichi-dev/taichi>`_
* `numpy <https://numpy.org/>`_
* `scipy <https://scipy.org/>`_
* `polars>=0.19.0 <https://pola-rs.github.io/polars/>`_
* `matplotlib <https://matplotlib.org/>`_

Optional Dependencies
----------------------

* `SciencePlots <https://github.com/garrettj403/SciencePlots>`_ (Optional, for plotting results)
* `tqdm <https://github.com/tqdm/tqdm>`_ (Optional, for progress bar when reading/saving multi DUMP files)
* `pyfftw <https://github.com/pyFFTW/pyFFTW>`_ (Optional, for fast FFT)
* `pyfnntw>=0.4.1 <https://github.com/cavemanloverboy/FNNTW>`_ (Optional, for fast KNN search)


Installation
-------------

Install from pip (recommended).
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   pip install mdapy

Install from source code.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- You should have a C++ compilation environment (-std=c++11 or newer) and openmp supports. 
  Tested by MSVC in Windows 10, GCC in Ubuntu, Clang in MAC OS M1.

- Download the source code and installation.
   
   .. code-block:: bash

      git clone https://github.com/mushroomfire/mdapy.git
      cd mdapy 
      pip install .

Check Installation
^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   python -c "import mdapy as mp; mp.init(); print('mdapy version is:', mp.__version__)"


Usage
------

.. code-block:: python

   import mdapy as mp
   mp.init('cpu') # use cpu, mp.init('gpu') will use gpu to compute.

   system = mp.System('./example/CoCuFeNiPd-4M.dump') # read dump file to generate a system class
   system.cal_centro_symmetry_parameter() # calculate the centrosymmetry parameters
   system.cal_atomic_entropy() # calculate the atomic entropy
   system.write_dump() # save results to a new dump file


Main Features
--------------

1. Structure Analysis
   
   - `Ackland Jones Analysis <https://mdapy.readthedocs.io/en/latest/mdapy.html#module-mdapy.ackland_jones_analysis>`_
   - `CentroSymmetry Parameter <https://mdapy.readthedocs.io/en/latest/mdapy.html#module-mdapy.centro_symmetry_parameter>`_ 
   - `Common Neighbor Analysis <https://mdapy.readthedocs.io/en/latest/mdapy.html#module-mdapy.common_neighbor_analysis>`_ 
   - `Common Neighbor Parameter <https://mdapy.readthedocs.io/en/latest/mdapy.html#module-mdapy.common_neighbor_parameter>`_
   - `Atomic Structure Entropy <https://mdapy.readthedocs.io/en/latest/mdapy.html#module-mdapy.entropy>`_ 
   - `Steinhardt Bondorder <https://mdapy.readthedocs.io/en/latest/mdapy.html#module-mdapy.steinhardt_bond_orientation>`_ 
   - `Radiul Distribution Function <https://mdapy.readthedocs.io/en/latest/mdapy.html#module-mdapy.pair_distribution>`_
   - `Polyhedral Template Matching <https://mdapy.readthedocs.io/en/latest/mdapy.html#module-mdapy.polyhedral_template_matching>`_
   - `Identify stacking faults (SFs) and twinning boundary (TBs) <https://mdapy.readthedocs.io/en/latest/mdapy.html#module-mdapy.identify_SFs_TBs>`_

2. Potential Analysis 

   - `Generate EAM/alloy Potential <https://mdapy.readthedocs.io/en/latest/mdapy.html#module-mdapy.eam_generate>`_
   - `Read EAM/alloy Potential <https://mdapy.readthedocs.io/en/latest/mdapy.html#module-mdapy.potential>`_
   - `Average EAM/alloy Potential <https://mdapy.readthedocs.io/en/latest/mdapy.html#module-mdapy.eam_average>`_
   - `Calculate Atomic Force and Energy by EAM/alloy <https://mdapy.readthedocs.io/en/latest/mdapy.html#module-mdapy.calculator>`_

3. Melting Analysis 

   - `Mean Squared Displacement <https://mdapy.readthedocs.io/en/latest/mdapy.html#module-mdapy.mean_squared_displacement>`_
   - `Lindemann Parameter <https://mdapy.readthedocs.io/en/latest/mdapy.html#module-mdapy.lindemann_parameter>`_
   - `Identify Solid/Liquid Phase <https://mdapy.readthedocs.io/en/latest/mdapy.html#module-mdapy.steinhardt_bond_orientation>`_

4. Geometry Structure Creation 

   - `Generate Standard Lattice Structure <https://mdapy.readthedocs.io/en/latest/mdapy.html#module-mdapy.lattice_maker>`_
   - `Generate Polycrystal <https://mdapy.readthedocs.io/en/latest/mdapy.html#mdapy.create_polycrystalline.CreatePolycrystalline>`_

5. Neighbor Search 

   - `Neighbor Atoms within Fixed Distance <https://mdapy.readthedocs.io/en/latest/mdapy.html#module-mdapy.neighbor>`_
   - `Neighbor Atoms within Fixed Number <https://mdapy.readthedocs.io/en/latest/mdapy.html#module-mdapy.nearest_neighbor>`_

6. Other 

   - `Void Distribution <https://mdapy.readthedocs.io/en/latest/mdapy.html#module-mdapy.void_distribution>`_
   - `Cluster Analysis <https://mdapy.readthedocs.io/en/latest/mdapy.html#module-mdapy.cluser_analysis>`_
   - `Replication <https://mdapy.readthedocs.io/en/latest/mdapy.html#module-mdapy.replicate>`_
   - `Warren Cowley Parameter <https://mdapy.readthedocs.io/en/latest/mdapy.html#module-mdapy.warren_cowley_parameter>`_
   - `Average Atomic Temperature <https://mdapy.readthedocs.io/en/latest/mdapy.html#module-mdapy.temperature>`_
   - `Atomic Voronoi Volume <https://mdapy.readthedocs.io/en/latest/mdapy.html#module-mdapy.voronoi_analysis>`_
   - `Multi-dimensional Spatial Binning <https://mdapy.readthedocs.io/en/latest/mdapy.html#module-mdapy.spatial_binning>`_
   - `Parallelly Compress file to .gz format <https://mdapy.readthedocs.io/en/latest/mdapy.html#module-mdapy.pigz>`_


Citation
---------
If you find **mdapy** useful, you can `star it! <https://github.com/mushroomfire/mdapy>`_
If you use **mdapy** in your scientific publications, please `cite the paper: <https://doi.org/10.1016/j.cpc.2023.108764>`_

.. code-block:: bibtex

   @article{mdapy2023,
      title = {mdapy: A flexible and efficient analysis software for molecular dynamics simulations},
      journal = {Computer Physics Communications},
      pages = {108764},
      year = {2023},
      issn = {0010-4655},
      doi = {https://doi.org/10.1016/j.cpc.2023.108764},
      url = {https://www.sciencedirect.com/science/article/pii/S0010465523001091},
      author = {Yong-Chao Wu and Jian-Li Shao},
      keywords = {Simulation analysis, Molecular dynamics, Polycrystal, TaiChi, Parallel computing}
      }


Trouble Shoot
-------------

If you encounter ImportError in Linux: 

.. code-block:: bash

   version 'GLIBCXX_3.4.29' not found. 

You can try: 

.. code-block:: bash

   conda install -c conda-forge gxx_linux-64

Release Notes
--------------

V0.9.4 (10/20/2023)
^^^^^^^^^^^^^^^^^^^^^^^^^^

- Remove dependency for **Pandas** and **Pyarrow**. mdapy uses **Polars** to be the newer DataFrame structure.
- Updated Documentation.
- Improve the importing speed.
- Minor improvement on compilation speed.

V0.9.3 (10/19/2023)
^^^^^^^^^^^^^^^^^^^^^

- Support generating special crystalline orientations for FCC and BCC lattice.
- Fix bug for warpping positions.
- Fix bug for write dump.
- Fix bug for generate System class from np.ndarray.
- Update an example to calculate the Generalized Stacking Fault Energy (GSFE).

V0.9.2 (10/12/2023)
^^^^^^^^^^^^^^^^^^^^^^

- Fix capacity of cross-platform.
- Updated doc.

V0.9.1 (10/11/2023)
^^^^^^^^^^^^^^^^^^^^^^^^^^

- Add **Polars** as dependency package. Now we still use pandas, but mdapy maybe move to polars in the future.
- Optimize the performance of reading and saving Dump and Data file.
- Support loading/saving compressed Dump file (such as sample.dump.gz).
- Support the lowest python version to 3.8.0.
- Add pyproject.toml.

V0.9.0 (9/23/2023)
^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Support triclinic box now!!!
- Add Select feature.
- Rewrite the load and save module.
- Make many method suitable for small system.
- Fix some bugs.

V0.8.9 (9/5/2023)
^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Fix installation in python 3.11.5.


V0.8.8 (8/24/2023)
^^^^^^^^^^^^^^^^^^^^^^^^^^

- Fix memory leak in SpatialBinning class, not the correct issue.
- Fix bug in SteinhardtBondOrientation class.
- Fix bug in read data.
- Fix bug in spatial_binning.
- Updated the IdentifySFTBinFCC class to identify the twinning and extrinsic stacking fault.

V0.8.7 (5/25/2023)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Updated Taichi to 1.6.0, which decreases the import time and supports Python 3.11.
- Fix bug in read data.
- Updated mdapy citation. We are pleased that our article for mdapy has been accepted by **Computer Physics Communications**.

V0.8.6 (4/22/2023)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Add repr for System class.
- Add Replicate class.
- Improve the performance of **reading/writing DATA file with pyarrow**.
- Improve the performance of **building Voronoi diagram** with new version voro++. 

V0.8.5 (4/9/2023)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Compile it on MAC OS with M1. Now **mdapy** is fully cross-platform.
- Obviously improve the performance of **reading/writing DUMP with pyarrow**.
- Add **pyarrow** as a dependency package.
- Fix bug of **create_polycrystalline** module. One can give box with any number, the old version only works for positive float.
- Fix bug of **spatial_binning** module for empty region.
- Let **tqdm** as an Optional dependency. 

V0.8.4 (3/30/2023)
^^^^^^^^^^^^^^^^^^^

- Optimize **Pair Distribution** module.
- Optimize **Neighbor** module.
- Update many **Benchmark** cases.

V0.8.3 (3/20/2023)
^^^^^^^^^^^^^^^^^^^

- Make **Polyhedral Template Mathing** parallel.

V0.8.2
^^^^^^^^^

- Fix bugs of unwrap positions.
- Fix a typo error in msd.

V0.8.1
^^^^^^^

- Add **Steinhardt Bondorder Parameter** method, which can be used to identify the lattice structure and distinguish
  the solid/liquid phase during melting process.
- Add **Polyhedral Template Mathing** method.
- Add **IdentifySFsTBs** method to identify the stacking faults (SFs) and twinning boundary (TBs) in FCC lattice.


V0.8.0
^^^^^^^

- Add **Ackland Jones Analysis (AJA)** method.
- Add **Common Neighbor Parameter (CNP)** method.
- Update the nearest neighbor search in CSP method.

V0.7.9
^^^^^^^

- Fix bug of create_polycrystalline module in Linux.

V0.7.8
^^^^^^^

- Update TaiChi version to 1.4.0.
- Set SciencePlots as a optional package.
- Fix bug in create_polycrystalline.