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
INSERT INTO experiment_run VALUES(1,'2023-07-24-08:33:34','2023-07-24-08:33:34',1690180414,0,'month',2,0,15,0,0,0,0,0,'{"JOBS": {"LOCAL_SETUP": {"FILE": "templates/local_setup.sh", "PLATFORM": "LOCAL", "RUNNING": "once", "DEPENDENCIES": {}, "ADDITIONAL_FILES": []}, "SYNCHRONIZE": {"FILE": "templates/synchronize.sh", "DEPENDENCIES": {"LOCAL_SETUP": {}}, "PLATFORM": "LOCAL", "RUNNING": "once", "ADDITIONAL_FILES": []}, "REMOTE_SETUP": {"FILE": "templates/remote_setup.sh", "DEPENDENCIES": {"SYNCHRONIZE": {}}, "RUNNING": "once", "PLATFORM": "Lumi-login", "WALLCLOCK": "00:05", "ADDITIONAL_FILES": []}, "DN": {"FILE": "templates/dn.sh", "DEPENDENCIES": {"REMOTE_SETUP": {}, "DN-1": {}}, "RUNNING": "chunk", "WALLCLOCK": "00:05", "PLATFORM": "Lumi-login", "ADDITIONAL_FILES": ["conf/applications/urban/request.yml"]}, "OPA": {"DEPENDENCIES": {"DN": {}, "OPA-1": {}}, "FILE": "templates/opa.sh", "RUNNING": "chunk", "SPLITS": "2", "WALLCLOCK": "00:05", "PLATFORM": "Lumi", "ADDITIONAL_FILES": []}, "APP": {"FILE": "templates/application.sh", "DEPENDENCIES": {"OPA": {}}, "RUNNING": "chunk", "WALLCLOCK": "00:05", "PLATFORM": "Lumi", "ADDITIONAL_FILES": []}}, "PLATFORMS": {"MARENOSTRUM4": {"TYPE": "slurm", "HOST": "bsc", "PROJECT": "bsc32", "USER": "bsc32070", "QUEUE": "debug", "SCRATCH_DIR": "/gpfs/scratch", "ADD_PROJECT_TO_HOST": "False", "MAX_WALLCLOCK": "48:00", "TEMP_DIR": "", "MAX_PROCESSORS": "2400", "PROCESSORS_PER_NODE": "48", "SERIAL_QUEUE": "debug"}, "MARENOSTRUM4-LOGIN": {"TYPE": "slurm", "HOST": "mn4-cluster", "PROJECT": "dese28", "USER": "<to-be-overloaded-in-user-conf>", "QUEUE": "debug", "SCRATCH_DIR": "/gpfs/scratch", "ADD_PROJECT_TO_HOST": false, "MAX_WALLCLOCK": "00:55"}, "JUWELS-LOGIN": {"TYPE": "ps", "HOST": "juwels-cluster", "PROJECT": "hhb19", "USER": "<to-be-overloaded-in-user-conf>", "SCRATCH_DIR": "/p/scratch", "SCRATCH_PROJECT_DIR": "chhb19", "ADD_PROJECT_TO_HOST": false, "TEMP_DIR": ""}, "JUWELS": {"TYPE": "slurm", "HOST": "juwels-cluster", "PROJECT": "hhb19", "USER": "<to-be-overloaded-in-user-conf>", "QUEUE": "", "CUSTOM_DIRECTIVES": "#SBATCH -p standard -N 1 --ntasks-per-node=24 --cpus-per-task=2", "SCRATCH_DIR": "/p/scratch", "SCRATCH_PROJECT_DIR": "chhb19", "PARTITION": "devel", "ADD_PROJECT_TO_HOST": false, "MAX_WALLCLOCK": "48:00", "TEMP_DIR": "", "PROCESSORS_PER_NODE": 24}, "LUMI-LOGIN": {"TYPE": "ps", "HOST": "lumi-cluster", "PROJECT": "project_465000454", "USER": "<to-be-overloaded-in-user-conf>", "SCRATCH_DIR": "/scratch", "ADD_PROJECT_TO_HOST": false, "TEMP_DIR": ""}, "LUMI": {"CUSTOM_DIRECTIVES": "[''#SBATCH -p standard'']", "TYPE": "slurm", "HOST": "lumi-cluster", "PROJECT": "project_465000454", "USER": "<to-be-overloaded-in-user-conf>", "QUEUE": "", "SCRATCH_DIR": "/scratch", "ADD_PROJECT_TO_HOST": false, "MAX_WALLCLOCK": "48:00", "TEMP_DIR": "", "PROCESSORS_PER_NODE": 1, "BUDGET": "project_465000454", "PARTITION": "small"}, "LEVANTE": {"TYPE": "slurm", "HOST": "levante.dkrz.de", "USER": "b382351", "PROJECT": "bb1153", "SCRATCH_DIR": "/work", "PARTITION": "interactive"}, "LEVANTE-LOGIN": {"TYPE": "slurm", "HOST": "levante.dkrz.de", "USER": "b382351", "PROJECT": "bb1153", "SCRATCH_DIR": "/work", "PARTITION": "interactive"}, "MARENOSTRUM0": {"TYPE": "slurm", "HOST": "marenostrum0", "PROJECT": "bsc32", "USER": "bsc32070", "SCRATCH_DIR": "/gpfs/scratch", "MAX_WALLCLOCK": "48:00", "MAX_PROCESSORS": "2400", "PROCESSORS_PER_NODE": "48", "SERIAL_QUEUE": "debug", "QUEUE": "debug"}, "MARENOSTRUM_ARCHIVE": {"TYPE": "ps", "HOST": "dt01.bsc.es", "PROJECT": "bsc32", "USER": "bsc32070", "SCRATCH_DIR": "/gpfs/scratch", "ADD_PROJECT_TO_HOST": "False", "TEST_SUITE": "False"}, "TRANSFER_NODE": {"TYPE": "ps", "HOST": "dt01.bsc.es", "PROJECT": "bsc32", "USER": "bsc32070", "ADD_PROJECT_TO_HOST": "false", "SCRATCH_DIR": "/gpfs/scratch"}}, "EXPERIMENT": {"DATELIST": 20211201, "MEMBERS": "fc0", "CHUNKSIZEUNIT": "month", "CHUNKSIZE": 2, "NUMCHUNKS": 3, "CALENDAR": "standard"}, "GSVREQUEST": {"DOMAIN": "g", "CLASS": "rd", "TYPE": "fc", "EXPVER": "hz9n", "STREAM": "lwda", "ANOFFSET": 9, "LEVTYPE": "sfc", "DATE": "%CHUNK_START_DATE%/to/%CHUNK_SECOND_TO_LAST_DATE%", "TIME": "0000/to/2300/by/0800", "STEP": ["0"], "PARAM": ["100v"], "GRID": "1/1", "METHOD": "nn"}, "APP": {"OTHER": "empty"}, "OPAREQUEST": {"NSTATS": "2", "1": {"VARIABLE": "2t", "STAT": "mean", "STAT_FREQ": "monthly", "OUTPUT_FREQ": "monthly", "TIME_STEP": 480, "SAVE": true, "CHECKPOINT": true, "CHECKPOINT_FILEPATH": "/scratch/project_465000454/tmp/a00w/", "OUT_FILEPATH": "/scratch/project_465000454/tmp/a00w/"}, "2": {"VARIABLE": "100u", "STAT": "raw", "STAT_FREQ": "monthly", "OUTPUT_FREQ": "monthly", "TIME_STEP": 480, "SAVE": true, "CHECKPOINT": true, "CHECKPOINT_FILEPATH": "/scratch/project_465000454/tmp/a00w/", "OUT_FILEPATH": "/scratch/project_465000454/tmp/a00w/"}}, "RUN": {"APP": "urban"}, "CONFIG": {"AUTOSUBMIT_VERSION": "4.0.0b", "TOTALJOBS": 20, "MAXWAITINGJOBS": 20}, "ROOTDIR": "/home/dbeltran/new_autosubmit/a00w", "PROJDIR": "/home/dbeltran/new_autosubmit/a00w/proj/project_files", "DEFAULT": {"EXPID": "a00w", "HPCARCH": "Lumi", "CUSTOM_CONFIG": {"PRE": "/home/dbeltran/new_autosubmit/a00w/proj/workflow/conf,/home/dbeltran/new_autosubmit/a00w/proj/workflow/conf/simulation/%RUN.SIMULATION%.yml,/home/dbeltran/new_autosubmit/a00w/proj/project_files/conf/parameter/%RUN.PARAMETER%.yml,/home/dbeltran/new_autosubmit/a00w/proj/project_files/conf/model/%RUN.MODEL%/%RUN.MODEL%.yml,/home/dbeltran/new_autosubmit/a00w/proj/project_files/conf/model/%RUN.MODEL%/%RUN.GRID%.yml,/home/dbeltran/new_autosubmit/a00w/proj/project_files/conf/applications/urban/gsvrequest.yml,/home/dbeltran/new_autosubmit/a00w/proj/project_files/conf/applications/urban/oparequest.yml,/home/dbeltran/new_autosubmit/a00w/proj/project_files/conf/applications/urban/request.yml", "POST": "~/platforms.yml"}}, "PROJECT": {"PROJECT_TYPE": "git", "PROJECT_DESTINATION": "workflow"}, "GIT": {"PROJECT_ORIGIN": "https://earth.bsc.es/gitlab/digital-twins/de_340/workflow.git", "PROJECT_BRANCH": "app-subworkflow-tmp", "PROJECT_COMMIT": "", "PROJECT_SUBMODULES": "", "FETCH_SINGLE_BRANCH": true}, "STORAGE": {}}');
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
