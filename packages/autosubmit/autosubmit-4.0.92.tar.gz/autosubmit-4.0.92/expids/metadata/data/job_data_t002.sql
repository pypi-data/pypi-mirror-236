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
INSERT INTO experiment_run VALUES(1,'2023-09-19-08:51:52','2023-09-19-08:54:22',1695106312,1695106462,'month',4,0,3,0,0,0,0,0,'{"CONFIG": {"AUTOSUBMIT_VERSION": "4.0.91", "MAXWAITINGJOBS": 20, "TOTALJOBS": 20, "SAFETYSLEEPTIME": 10, "RETRIALS": 0}, "MAIL": {"NOTIFICATIONS": false, "TO": null}, "STORAGE": {"TYPE": "pkl", "COPY_REMOTE_LOGS": true}, "DEFAULT": {"EXPID": "a01a", "HPCARCH": "marenostrum4", "CUSTOM_CONFIG": {"POST": "~/platforms.yml"}}, "EXPERIMENT": {"DATELIST": "20000101", "MEMBERS": "fc0", "CHUNKSIZEUNIT": "month", "CHUNKSIZE": 4, "NUMCHUNKS": 3, "CHUNKINI": "", "CALENDAR": "standard"}, "PROJECT": {"PROJECT_TYPE": "none", "PROJECT_DESTINATION": ""}, "GIT": {"PROJECT_ORIGIN": "", "PROJECT_BRANCH": "", "PROJECT_COMMIT": "", "PROJECT_SUBMODULES": "", "FETCH_SINGLE_BRANCH": true}, "SVN": {"PROJECT_URL": "", "PROJECT_REVISION": ""}, "LOCAL": {"PROJECT_PATH": ""}, "PROJECT_FILES": {"FILE_PROJECT_CONF": "", "FILE_JOBS_CONF": "", "JOB_SCRIPTS_TYPE": ""}, "RERUN": {"RERUN": false, "RERUN_JOBLIST": ""}, "WRAPPERS": {"WRAPPER_HETJOBS": {"JOBS_IN_WRAPPER": "HETJOB", "TYPE": "vertical"}}, "JOBS": {"HETJOB": {"FILE": "a", "PLATFORM": "marenostrum4dese", "DEPENDENCIES": {"HETJOB-1": {}}, "RUNNING": "chunk", "WALLCLOCK": "00:02", "MEMORY": [0, 0], "NODES": [3, 1], "TASKS": [32, 32], "THREADS": [4, 4], "CUSTOM_DIRECTIVES": "[[''#SBATCH --export=ALL'', ''#SBATCH --distribution=block:cyclic'', ''#SBATCH --exclusive''], [''#SBATCH --export=ALL'', ''#SBATCH --distribution=block:cyclic:fcyclic'', ''#SBATCH --exclusive'']]", "ADDITIONAL_FILES": []}}, "PLATFORMS": {"MARENOSTRUM4DESE": {"TYPE": "slurm", "HOST": "des", "PROJECT": "dese28", "USER": "dese28674", "QUEUE": "class_a", "SCRATCH_DIR": "/gpfs/scratch", "ADD_PROJECT_TO_HOST": false, "MAX_WALLCLOCK": "48:00", "TEMP_DIR": ""}, "MARENOSTRUM_ARCHIVE": {"TYPE": "ps", "HOST": "dt01.bsc.es", "PROJECT": "bsc32", "USER": "bsc32070", "SCRATCH_DIR": "/gpfs/scratch", "ADD_PROJECT_TO_HOST": "False", "TEST_SUITE": "False"}, "TRANSFER_NODE": {"TYPE": "ps", "HOST": "dt01.bsc.es", "PROJECT": "bsc32", "USER": "bsc32070", "ADD_PROJECT_TO_HOST": "false", "SCRATCH_DIR": "/gpfs/scratch"}, "TRANSFER_NODE_BSCEARTH000": {"TYPE": "ps", "HOST": "bscearth000", "USER": null, "PROJECT": "Earth", "ADD_PROJECT_TO_HOST": false, "QUEUE": "serial", "SCRATCH_DIR": "/esarchive/scratch"}, "BSCEARTH000": {"TYPE": "ps", "HOST": "bscearth000", "USER": null, "PROJECT": "Earth", "ADD_PROJECT_TO_HOST": false, "QUEUE": "serial", "SCRATCH_DIR": "/esarchive/scratch"}, "NORD3": {"TYPE": "SLURM", "HOST": "nord1.bsc.es", "PROJECT": "bsc32", "USER": null, "QUEUE": "debug", "SCRATCH_DIR": "/gpfs/scratch", "MAX_WALLCLOCK": "48:00"}, "ECMWF-XC40": {"TYPE": "ecaccess", "VERSION": "pbs", "HOST": "cca", "USER": null, "PROJECT": "spesiccf", "ADD_PROJECT_TO_HOST": false, "SCRATCH_DIR": "/scratch/ms", "QUEUE": "np", "SERIAL_QUEUE": "ns", "MAX_WALLCLOCK": "48:00"}, "ECMWF-HPC2020": {"TYPE": "ecaccess", "VERSION": "slurm", "HOST": "hpc-login", "QUEUE": "nf", "EC_QUEUE": "hpc", "BUDGET": null, "USER": "c3d", "SCRATCH_DIR": "/ec/res4/scratch/c3d", "PROJECT": "spesiccf", "ADD_PROJECT_TO_HOST": false, "MAX_WALLCLOCK": "48:00", "CUSTOM_DIRECTIVES": "#SBATCH --hint=nomultithread"}, "POWER9": {"TYPE": "slurm", "HOST": "plogin1.bsc.es", "USER": "bsc32070", "PROJECT": "bsc32", "SCRATCH_DIR": "/gpfs/scratch", "QUEUE": "debug"}, "LEVANTE": {"TYPE": "slurm", "HOST": "levante.dkrz.de", "USER": "b382351", "PROJECT": "bb1153", "SCRATCH_DIR": "/work"}, "LEVANTE-LOGIN": {"TYPE": "slurm", "HOST": "levante.dkrz.de", "USER": "b382351", "PROJECT": "bb1153", "SCRATCH_DIR": "/work", "PARTITION": "interactive"}, "MARENOSTRUM0": {"TYPE": "slurm", "HOST": "marenostrum0", "PROJECT": "bsc32", "USER": "bsc32070", "SCRATCH_DIR": "/gpfs/scratch", "MAX_WALLCLOCK": "48:00", "MAX_PROCESSORS": "2400", "PROCESSORS_PER_NODE": "48", "SERIAL_QUEUE": "debug", "QUEUE": "debug"}, "MARENOSTRUM4": {"TYPE": "slurm", "HOST": "bsc", "PROJECT": "bsc32", "USER": "bsc32070", "SCRATCH_DIR": "/gpfs/scratch", "ADD_PROJECT_TO_HOST": "False", "MAX_WALLCLOCK": "48:00", "MAX_PROCESSORS": "2400", "PROCESSORS_PER_NODE": "48", "SERIAL_QUEUE": "debug", "QUEUE": "debug"}}, "ROOTDIR": "/home/dbeltran/new_autosubmit/t002", "PROJDIR": "/home/dbeltran/new_autosubmit/t002/proj/"}');
INSERT INTO experiment_run VALUES(2,'2023-09-19-08:54:22','2023-09-19-08:57:15',1695106462,0,'month',4,3,3,0,0,0,0,0,'{"CONFIG": {"AUTOSUBMIT_VERSION": "4.0.91", "MAXWAITINGJOBS": 20, "TOTALJOBS": 20, "SAFETYSLEEPTIME": 10, "RETRIALS": 0}, "MAIL": {"NOTIFICATIONS": false, "TO": null}, "STORAGE": {"TYPE": "pkl", "COPY_REMOTE_LOGS": true}, "DEFAULT": {"EXPID": "a01a", "HPCARCH": "marenostrum4", "CUSTOM_CONFIG": {"POST": "~/platforms.yml"}}, "EXPERIMENT": {"DATELIST": "20000101", "MEMBERS": "fc0", "CHUNKSIZEUNIT": "month", "CHUNKSIZE": 4, "NUMCHUNKS": 3, "CHUNKINI": "", "CALENDAR": "standard"}, "PROJECT": {"PROJECT_TYPE": "none", "PROJECT_DESTINATION": ""}, "GIT": {"PROJECT_ORIGIN": "", "PROJECT_BRANCH": "", "PROJECT_COMMIT": "", "PROJECT_SUBMODULES": "", "FETCH_SINGLE_BRANCH": true}, "SVN": {"PROJECT_URL": "", "PROJECT_REVISION": ""}, "LOCAL": {"PROJECT_PATH": ""}, "PROJECT_FILES": {"FILE_PROJECT_CONF": "", "FILE_JOBS_CONF": "", "JOB_SCRIPTS_TYPE": ""}, "RERUN": {"RERUN": false, "RERUN_JOBLIST": ""}, "WRAPPERS": {"WRAPPER_HETJOBS": {"JOBS_IN_WRAPPER": "HETJOB", "TYPE": "vertical"}}, "JOBS": {"HETJOB": {"FILE": "a", "PLATFORM": "marenostrum4dese", "DEPENDENCIES": {"HETJOB-1": {}}, "RUNNING": "chunk", "WALLCLOCK": "00:02", "MEMORY": [0, 0], "NODES": [1, 1], "TASKS": [1, 2], "THREADS": [4, 2], "CUSTOM_DIRECTIVES": "[[''#SBATCH --export=ALL'', ''#SBATCH --distribution=block:cyclic'', ''#SBATCH --exclusive''], [''#SBATCH --export=ALL'', ''#SBATCH --distribution=block:cyclic:fcyclic'', ''#SBATCH --exclusive'']]", "ADDITIONAL_FILES": []}}, "PLATFORMS": {"MARENOSTRUM4DESE": {"TYPE": "slurm", "HOST": "des", "PROJECT": "dese28", "USER": "dese28674", "QUEUE": "class_a", "SCRATCH_DIR": "/gpfs/scratch", "ADD_PROJECT_TO_HOST": false, "MAX_WALLCLOCK": "48:00", "TEMP_DIR": ""}, "MARENOSTRUM_ARCHIVE": {"TYPE": "ps", "HOST": "dt01.bsc.es", "PROJECT": "bsc32", "USER": "bsc32070", "SCRATCH_DIR": "/gpfs/scratch", "ADD_PROJECT_TO_HOST": "False", "TEST_SUITE": "False"}, "TRANSFER_NODE": {"TYPE": "ps", "HOST": "dt01.bsc.es", "PROJECT": "bsc32", "USER": "bsc32070", "ADD_PROJECT_TO_HOST": "false", "SCRATCH_DIR": "/gpfs/scratch"}, "TRANSFER_NODE_BSCEARTH000": {"TYPE": "ps", "HOST": "bscearth000", "USER": null, "PROJECT": "Earth", "ADD_PROJECT_TO_HOST": false, "QUEUE": "serial", "SCRATCH_DIR": "/esarchive/scratch"}, "BSCEARTH000": {"TYPE": "ps", "HOST": "bscearth000", "USER": null, "PROJECT": "Earth", "ADD_PROJECT_TO_HOST": false, "QUEUE": "serial", "SCRATCH_DIR": "/esarchive/scratch"}, "NORD3": {"TYPE": "SLURM", "HOST": "nord1.bsc.es", "PROJECT": "bsc32", "USER": null, "QUEUE": "debug", "SCRATCH_DIR": "/gpfs/scratch", "MAX_WALLCLOCK": "48:00"}, "ECMWF-XC40": {"TYPE": "ecaccess", "VERSION": "pbs", "HOST": "cca", "USER": null, "PROJECT": "spesiccf", "ADD_PROJECT_TO_HOST": false, "SCRATCH_DIR": "/scratch/ms", "QUEUE": "np", "SERIAL_QUEUE": "ns", "MAX_WALLCLOCK": "48:00"}, "ECMWF-HPC2020": {"TYPE": "ecaccess", "VERSION": "slurm", "HOST": "hpc-login", "QUEUE": "nf", "EC_QUEUE": "hpc", "BUDGET": null, "USER": "c3d", "SCRATCH_DIR": "/ec/res4/scratch/c3d", "PROJECT": "spesiccf", "ADD_PROJECT_TO_HOST": false, "MAX_WALLCLOCK": "48:00", "CUSTOM_DIRECTIVES": "#SBATCH --hint=nomultithread"}, "POWER9": {"TYPE": "slurm", "HOST": "plogin1.bsc.es", "USER": "bsc32070", "PROJECT": "bsc32", "SCRATCH_DIR": "/gpfs/scratch", "QUEUE": "debug"}, "LEVANTE": {"TYPE": "slurm", "HOST": "levante.dkrz.de", "USER": "b382351", "PROJECT": "bb1153", "SCRATCH_DIR": "/work"}, "LEVANTE-LOGIN": {"TYPE": "slurm", "HOST": "levante.dkrz.de", "USER": "b382351", "PROJECT": "bb1153", "SCRATCH_DIR": "/work", "PARTITION": "interactive"}, "MARENOSTRUM0": {"TYPE": "slurm", "HOST": "marenostrum0", "PROJECT": "bsc32", "USER": "bsc32070", "SCRATCH_DIR": "/gpfs/scratch", "MAX_WALLCLOCK": "48:00", "MAX_PROCESSORS": "2400", "PROCESSORS_PER_NODE": "48", "SERIAL_QUEUE": "debug", "QUEUE": "debug"}, "MARENOSTRUM4": {"TYPE": "slurm", "HOST": "bsc", "PROJECT": "bsc32", "USER": "bsc32070", "SCRATCH_DIR": "/gpfs/scratch", "ADD_PROJECT_TO_HOST": "False", "MAX_WALLCLOCK": "48:00", "MAX_PROCESSORS": "2400", "PROCESSORS_PER_NODE": "48", "SERIAL_QUEUE": "debug", "QUEUE": "debug"}}, "ROOTDIR": "/home/dbeltran/new_autosubmit/t002", "PROJDIR": "/home/dbeltran/new_autosubmit/t002/proj/"}');
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
INSERT INTO job_data VALUES(1,0,'t002_20000101_fc0_1_HETJOB','2023-09-19-08:56:58','2023-09-19-08:56:58',1695106480,1695106589,1695106594,'COMPLETED',16951064679703,1,'00:02','class_a',0,'2000-01-01 00:00:00','HETJOB','fc0',1,1,'MARENOSTRUM4DESE',30216975,'',0,2,0.0,0.0,'','',5,'t002_20000101_fc0_2_HETJOB','');
DELETE FROM sqlite_sequence;
INSERT INTO sqlite_sequence VALUES('experiment_run',2);
INSERT INTO sqlite_sequence VALUES('job_data',1);
CREATE INDEX ID_JOB_NAME ON job_data(job_name);
COMMIT;
