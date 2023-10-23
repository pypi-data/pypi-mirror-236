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
INSERT INTO experiment_run VALUES(1,'2023-05-03-10:11:42','2023-05-03-10:11:42',1683101502,0,'month',4,0,13,0,0,0,0,0,'{"CONFIG": {"AUTOSUBMIT_VERSION": "3.14.0", "EXPID": "a00c", "MAXWAITINGJOBS": "3", "TOTALJOBS": "6", "SAFETYSLEEPTIME": "5", "RETRIALS": 0, "OUTPUT": "pdf", "PRESUBMISSION": "FALSE"}, "MAIL": {"NOTIFICATIONS": "False", "TO": ""}, "COMMUNICATIONS": {"API": "paramiko"}, "STORAGE": {"TYPE": "pkl", "COPY_REMOTE_LOGS": "True"}, "MIGRATE": {"TO_USER": ""}, "DEFAULT": {"EXPID": "a00c", "HPCARCH": "MARENOSTRUM4", "CUSTOM_CONFIG": {"POST": "~/platforms.yml"}}, "EXPERIMENT": {"DATELIST": "20000101", "MEMBERS": "fc0", "CHUNKSIZEUNIT": "month", "CHUNKSIZE": 4, "NUMCHUNKS": 2, "CHUNKINI": "", "CALENDAR": "standard", "RUN_ONLY_MEMBERS": ""}, "PROJECT": {"PROJECT_TYPE": "none", "PROJECT_DESTINATION": ""}, "GIT": {"PROJECT_ORIGIN": "", "PROJECT_BRANCH": "", "PROJECT_COMMIT": "", "PROJECT_SUBMODULES": "", "FETCH_SINGLE_BRANCH": "true"}, "SVN": {"PROJECT_URL": "", "PROJECT_REVISION": ""}, "LOCAL": {"PROJECT_PATH": ""}, "PROJECT_FILES": {"FILE_PROJECT_CONF": "", "FILE_JOBS_CONF": "", "JOB_SCRIPTS_TYPE": ""}, "RERUN": {"RERUN": "FALSE", "CHUNKLIST": ""}, "JOBS": {"LOCAL_SETUP": {"FILE": "LOCAL_SETUP.sh", "PLATFORM": "LOCAL", "DEPENDENCIES": {}, "ADDITIONAL_FILES": []}, "REMOTE_SETUP": {"FILE": "REMOTE_SETUP.sh", "DEPENDENCIES": {"LOCAL_SETUP": {}}, "WALLCLOCK": "00:05", "CUSTOM_DIRECTIVES": "\"\"", "ADDITIONAL_FILES": []}, "INI": {"FILE": "INI.sh", "DEPENDENCIES": {"REMOTE_SETUP": {}}, "RUNNING": "member", "WALLCLOCK": "00:05", "CUSTOM_DIRECTIVES": "\"\"", "ADDITIONAL_FILES": []}, "SIM": {"FILE": "SIM.sh", "DEPENDENCIES": {"INI": {}, "SIM-1": {}}, "RUNNING": "chunk", "WALLCLOCK": "08:00", "PROCESSORS": "2400", "THREADS": "1", "CUSTOM_DIRECTIVES": "\"\"", "ADDITIONAL_FILES": []}, "DATA_NOTIFY": {"FILE": "POST.sh", "DEPENDENCIES": {"SIM": {}}, "RUNNING": "chunk", "WALLCLOCK": "00:05", "CUSTOM_DIRECTIVES": "\"\"", "ADDITIONAL_FILES": []}, "OPA": {"FILE": "CLEAN.sh", "DEPENDENCIES": {"DATA_NOTIFY": {}}, "RUNNING": "chunk", "WALLCLOCK": "00:05", "CUSTOM_DIRECTIVES": "\"\"", "ADDITIONAL_FILES": []}, "APPLICATION": {"FILE": "TRANSFER.sh", "DEPENDENCIES": {"OPA": {}}, "RUNNING": "chunk", "ADDITIONAL_FILES": []}, "AQUA_DIAGNOSTIC": {"FILE": "LOCALPOST.sh", "DEPENDENCIES": {"OPA": {}}, "RUNNING": "chunk", "WALLCLOCK": "00:05", "ADDITIONAL_FILES": []}}, "ROOTDIR": "/home/dbeltran/new_autosubmit/a00c", "PROJDIR": "/home/dbeltran/new_autosubmit/a00c/proj/", "PLATFORMS": {"LEVANTE": {"TYPE": "slurm", "HOST": "levante.dkrz.de", "USER": "b382351", "PROJECT": "bb1153", "SCRATCH_DIR": "/work"}, "LEVANTE-LOGIN": {"TYPE": "slurm", "HOST": "levante.dkrz.de", "USER": "b382351", "PROJECT": "bb1153", "SCRATCH_DIR": "/work", "PARTITION": "interactive"}, "MARENOSTRUM0": {"TYPE": "slurm", "HOST": "marenostrum0", "PROJECT": "bsc32", "USER": "bsc32070", "SCRATCH_DIR": "/gpfs/scratch", "MAX_WALLCLOCK": "48:00", "MAX_PROCESSORS": "2400", "PROCESSORS_PER_NODE": "48", "SERIAL_QUEUE": "debug", "QUEUE": "debug"}, "MARENOSTRUM4": {"TYPE": "slurm", "HOST": "bsc", "PROJECT": "bsc32", "USER": "bsc32070", "SCRATCH_DIR": "/gpfs/scratch", "ADD_PROJECT_TO_HOST": "False", "MAX_WALLCLOCK": "48:00", "MAX_PROCESSORS": "2400", "PROCESSORS_PER_NODE": "48", "SERIAL_QUEUE": "debug", "QUEUE": "debug"}, "MARENOSTRUM_ARCHIVE": {"TYPE": "ps", "HOST": "dt01.bsc.es", "PROJECT": "bsc32", "USER": "bsc32070", "SCRATCH_DIR": "/gpfs/scratch", "ADD_PROJECT_TO_HOST": "False", "TEST_SUITE": "False"}, "TRANSFER_NODE": {"TYPE": "ps", "HOST": "dt01.bsc.es", "PROJECT": "bsc32", "USER": "bsc32070", "ADD_PROJECT_TO_HOST": "false", "SCRATCH_DIR": "/gpfs/scratch"}}}');
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
