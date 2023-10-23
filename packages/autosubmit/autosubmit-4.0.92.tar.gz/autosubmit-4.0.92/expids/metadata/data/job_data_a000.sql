PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE experiment_run (
      run_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
      created TEXT NOT NULL,
      modified TEXT NOT NULL,
      start INTEGER NOT NULL,
      finish INTEGER,
      chunk_unit TEXT NOT NULL,
      chunk_size INTEGER NOT NULL,
      completed INTEGER NOT NULL,
      total INTEGER NOT NULL,
      failed INTEGER NOT NULL,
      queuing INTEGER NOT NULL,
      running INTEGER NOT NULL,
      submitted INTEGER NOT NULL,
      suspended INTEGER NOT NULL DEFAULT 0,
      metadata TEXT
      );
INSERT INTO experiment_run VALUES(1,'2023-07-10-15:19:10','2023-07-10-15:19:10',1688995150,0,'hour',4,0,18,0,0,0,0,0,'{"platforms": {"moore": {"QUEUE": "serial", "PROJECT": "Earth", "SCRATCH_DIR": "/esarchive/scratch", "HOST": "moore", "USER": "", "TYPE": "slurm", "ADD_PROJECT_TO_HOST": "false"}, "ecmwf-cca": {"QUEUE": "np", "PROCESSORS_PER_NODE": "36", "PROJECT": "spesiccf", "SCRATCH_DIR": "/scratch/ms", "HOST": "cca", "VERSION": "pbs", "USER": "c3a", "TEST_SUITE": "True", "TYPE": "ecaccess", "ADD_PROJECT_TO_HOST": "false"}, "marenostrum3": {"QUEUE": "debug", "PROCESSORS_PER_NODE": "16", "PROJECT": "bsc32", "SCRATCH_DIR": "/gpfs/scratch", "HOST": "mn", "TEST_SUITE": "True", "USER": "bsc32070", "TYPE": "lsf", "ADD_PROJECT_TO_HOST": "true"}, "marenostrum4": {"QUEUE": "debug", "MAX_WALLCLOCK": "02:00", "PROCESSORS_PER_NODE": "48", "PROJECT": "bsc32", "SCRATCH_DIR": "/gpfs/scratch", "HOST": "mn1.bsc.es", "USER": "bsc32070", "MAX_PROCESSORS": "720", "TYPE": "slurm", "ADD_PROJECT_TO_HOST": "false"}, "power9": {"QUEUE": "debug", "SERIAL_QUEUE": "debug", "PROJECT": "bsc32", "SCRATCH_DIR": "/gpfs/scratch", "HOST": "plogin1.bsc.es", "TEST_SUITE": "False", "USER": "bsc32070", "TYPE": "slurm", "ADD_PROJECT_TO_HOST": "False"}, "marenostrum_archive": {"QUEUE": "debug", "MAX_WALLCLOCK": "02:00", "PROCESSORS_PER_NODE": "48", "PROJECT": "bsc32", "SCRATCH_DIR": "/gpfs/scratch", "HOST": "mn1.bsc.es", "USER": "bsc32070", "MAX_PROCESSORS": "720", "TYPE": "slurm", "ADD_PROJECT_TO_HOST": "false"}}, "jobs": {"POST": {"QUEUE": "debug", "RUNNING": "member", "DEPENDENCIES": "SIM", "FILE": "templates/post.sh", "WALLCLOCK": "00:02"}, "SIM": {"TASKS": "1", "RUNNING": "chunk", "DEPENDENCIES": "INI POST-1", "FILE": "templates/sim.sh", "WALLCLOCK": "00:10"}}, "exp": {"svn": {"HPCARCH": "marenostrum4", "EXPID": "a000", "PROJECT_REVISION": "", "PROJECT_URL": ""}, "git": {"HPCARCH": "marenostrum4", "EXPID": "a000", "PROJECT_BRANCH": "''dev_mgali''", "PROJECT_ORIGIN": "''https://earth.bsc.es/gitlab/cp/genetic_algorithm_pisces1d.git''", "PROJECT_COMMIT": ""}, "project": {"HPCARCH": "marenostrum4", "EXPID": "a000", "PROJECT_DESTINATION": "autosubmit", "PROJECT_TYPE": "git"}, "experiment": {"HPCARCH": "marenostrum4", "CHUNKSIZEUNIT": "hour", "CHUNKSIZE": "4", "CHUNKINI": "", "NUMCHUNKS": "5", "DATELIST": "19600101", "EXPID": "a000", "MEMBERS": "fc[0000-0002]", "CALENDAR": "standard"}, "project_files": {"FILE_JOBS_CONF": "", "HPCARCH": "marenostrum4", "JOB_SCRIPTS_TYPE": "", "FILE_PROJECT_CONF": "templates/t023_conf_proj_t023.conf", "EXPID": "a000"}, "rerun": {"HPCARCH": "marenostrum4", "CHUNKLIST": "", "EXPID": "a000", "RERUN": "FALSE"}, "local": {"EXPID": "a000", "HPCARCH": "marenostrum4", "PROJECT_PATH": "/home/Earth/mfalls/pisces1d/project/genetic_algorithm_pisces1d/templates"}}, "conf": {"migrate": {"TO_USER": ""}, "storage": {"TYPE": "pkl", "COPY_REMOTE_LOGS": "True"}, "wrapper": {"JOBS_IN_WRAPPER": "SIM&POST", "MIN_WRAPPED_H": "5", "MIN_WRAPPED_V": "5", "TYPE": "horizontal-vertical", "MACHINEFILES": "STANDARD"}, "communications": {"API": "paramiko"}, "mail": {"NOTIFICATIONS": "False", "TO": ""}, "config": {"EXPID": "a000", "TOTALJOBS": "10100", "MAXWAITINGJOBS": "10100", "RETRIALS": "3", "AUTOSUBMIT_VERSION": "3.14.0", "SAFETYSLEEPTIME": "10"}}, "proj": {"lpjg": {"PISCES_timestep": "", "LPJG": "FALSE", "MODEL_EXTRACT": "", "LPJG_CONFIG": "lpjg:fdbck", "MODEL_CLEAN": "", "LOCAL_SCRATCH_DIR": "", "SAVEMMA": "FALSE", "NEMO_timestep": "", "RUN_coupFreq": "", "LIM_timestep": "", "IFS_timestep": ""}, "ECMWF_SYNCHRONIZATION": {"UPDATE_MODEL": "TRUE", "MODEL_EXTRACT": "TRUE", "DTHOSTMACHINE": "", "DT_USER": "", "DT_HOST": "", "USE_DT_MACHINE": "FALSE"}, "ifs": {"XLCOR_SPPT": "", "ATM_ini_member": "", "ATM_SH_LEVELS": "", "LTAPER_SPPT": "", "ATM_ini": "", "LHVOLCA": "TRUE", "NS_SPPT": "", "LCMIP5": "", "PTAPER_BOT": "", "ATM_SH_CODES": "", "LSPPT": "FALSE", "ATM_refnud": "", "SAVEDDA": "FALSE", "ATM_REDUCED_OUTPUT": "", "NRCP": "", "NFRP": "6", "ATM_NUDGING": "FALSE", "PTAPER_TOP": "", "LWRITE_ARP": "", "ATM_ini_member_perturb": "FALSE", "ATM_GG_LEVELS": "", "SDEV_SPPT": "", "ATM_GG_CODES": "", "TAU_SPPT": "", "IFS_VEG_SOURCE": "cmip6", "NFIXYR": "0", "XCLIP_SPPT": ""}, "save_ic": {"SAVE_IC": "FALSE", "SAVE_IC_OFFSET": "\"+1 month\" \"+4 month\" \"+ 7 month\" \"+ 10 month\" \"+ 12 month\"", "SAVE_IC_REPOS": "FALSE"}, "nemo": {"NEM_FIXED_FORCING_YEAR": "-1", "DATA_SURF_RESTO": "", "DATA_OCE_NUDG": "", "OCE_NUDG": "FALSE", "ADVSCH": "tvd", "OCEAN_NUDGING": "FALSE", "NEMO_remove_land": "TRUE", "NEM_FORCING_SET": "CoreII", "OCEAN_ini": "", "OCEAN_STORERST": "FALSE", "DATA_OCE_NUDG_member": "", "DATA_SURF_RESTO_member": "", "OCEAN_ini_member": "", "SURF_RESTO": "FALSE", "OCEAN_NUDDATA": ""}, "ice": {"ICE_ini": "", "ICE": "LIM3", "ICE_ini_member": ""}, "oasis": {"OASIS3": "yes", "OASIS_ini": "", "OASIS_nproc": "", "OASIS_flds": "", "OASIS_ini_member": ""}, "grid": {"NEMO_resolution": "ORCA1L75", "IFS_resolution": ""}, "common": {"CMORIZATION": "TRUE", "TEMPLATE_NAME": "nemo4", "MODEL": "ecearth", "FORCING": "", "MODEL_ID": "EC-Earth3-LR", "MODEL_output_remove": "TRUE", "CMOR_EXP": "piControl", "DELETE_RUN_DIR_ON_INI": "FALSE", "LPJG_NUMPROC": "", "ALLOW_CUSTOM_CMOR_EXP": "FALSE", "LONG_TERM_ARCHIVING": "FALSE", "ASSOCIATED_EXPERIMENT": "", "IFS_NUMPROC": "", "NEM_NUMPROC": "336", "DELETE_INI_DIR_ON_INI": "TRUE", "VERSION": "trunk", "CMIP6_OUTCLASS": "", "ADD_PROJECT_TO_HOST": "false", "XIO_NUMPROC": "96", "BSC_OUTCLASS": "reduced", "CMOR_REALIZATION_INDEX": "", "PRODUCTION_EXP": "false", "CMOR_ADD_STARTDATE": "true", "MODEL_RES": "LR"}, "diagnostics": {"ECE3_POSTPROC": "FALSE", "DATA_CONVENTION": "CMIP5", "PROJ_TYPE": "STANDARD", "DIAGS": "", "DIAGS_FREQ": "mon", "DIAGS_PATH": ""}, "pisces": {"PISCES_ini_member": "", "PISCES": "FALSE", "PISCES_ini": "", "PISCES_OFF": "FALSE", "PISCES_OFF_DYN": ""}}}');
CREATE TABLE job_data (
      id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
      counter INTEGER NOT NULL,
      job_name TEXT NOT NULL,
      created TEXT NOT NULL,
      modified TEXT NOT NULL,
      submit INTEGER NOT NULL,
      start INTEGER NOT NULL,
      finish INTEGER NOT NULL,
      status TEXT NOT NULL,
      rowtype INTEGER NOT NULL,
      ncpus INTEGER NOT NULL,
      wallclock TEXT NOT NULL,
      qos TEXT NOT NULL,
      energy INTEGER NOT NULL,
      date TEXT NOT NULL,
      section TEXT NOT NULL,
      member TEXT NOT NULL,
      chunk INTEGER NOT NULL,
      last INTEGER NOT NULL,
      platform TEXT NOT NULL,
      job_id INTEGER NOT NULL,
      extra_data TEXT NOT NULL,
      nnodes INTEGER NOT NULL DEFAULT 0,
      run_id INTEGER,
      MaxRSS REAL NOT NULL DEFAULT 0.0,
      AveRSS REAL NOT NULL DEFAULT 0.0,
      out TEXT NOT NULL,
      err TEXT NOT NULL,
      rowstatus INTEGER NOT NULL DEFAULT 0,
      children TEXT,
      platform_output TEXT,
      UNIQUE(counter,job_name)
      );
DELETE FROM sqlite_sequence;
INSERT INTO sqlite_sequence VALUES('experiment_run',1);
CREATE INDEX ID_JOB_NAME ON job_data(job_name);
COMMIT;
