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
INSERT INTO experiment_run VALUES(1,'2023-10-16-13:26:18','2023-10-16-13:26:18',1697455578,0,'month',4,0,8,0,0,0,0,0,'{"CONFIG": {"AUTOSUBMIT_VERSION": "4.0.0", "MAXWAITINGJOBS": 20, "TOTALJOBS": 20, "SAFETYSLEEPTIME": 10, "RETRIALS": 0}, "MAIL": {"NOTIFICATIONS": false, "TO": null}, "STORAGE": {"TYPE": "pkl", "COPY_REMOTE_LOGS": true}, "EXPERIMENT": {"DATELIST": 20220401, "MEMBERS": "fc0", "CHUNKSIZEUNIT": "month", "CHUNKSIZE": 4, "NUMCHUNKS": 2, "CHUNKINI": "", "CALENDAR": "standard"}, "PROJECT_FILES": {"FILE_PROJECT_CONF": "", "FILE_JOBS_CONF": "", "JOB_SCRIPTS_TYPE": ""}, "RERUN": {"RERUN": false, "RERUN_JOBLIST": ""}, "JOBS": {"LOCAL_SETUP": {"FILE": "templates/local_setup.sh", "PLATFORM": "LOCAL", "RUNNING": "once", "DEPENDENCIES": {}, "ADDITIONAL_FILES": []}, "SYNCHRONIZE": {"FILE": "templates/synchronize.sh", "PLATFORM": "LOCAL", "DEPENDENCIES": {"LOCAL_SETUP": {}}, "RUNNING": "once", "ADDITIONAL_FILES": []}, "REMOTE_SETUP": {"FILE": "templates/remote_setup.sh", "DEPENDENCIES": {"SYNCHRONIZE": {}}, "WALLCLOCK": "00:05", "RUNNING": "once", "ADDITIONAL_FILES": []}, "INI": {"FILE": "templates/ini.sh", "DEPENDENCIES": {"REMOTE_SETUP": {}}, "RUNNING": "member", "WALLCLOCK": "00:05", "ADDITIONAL_FILES": []}, "SIM": {"FILE": "templates/sim.sh", "DEPENDENCIES": {"INI": {}}, "RUNNING": "chunk", "WALLCLOCK": "00:05", "ADDITIONAL_FILES": []}, "POST": {"FILE": "templates/post.sh", "DEPENDENCIES": {"SIM": {}}, "RUNNING": "once", "WALLCLOCK": "00:05", "ADDITIONAL_FILES": []}, "CLEAN": {"FILE": "templates/clean.sh", "DEPENDENCIES": {"POST": {}}, "RUNNING": "once", "WALLCLOCK": "00:05", "ADDITIONAL_FILES": []}}, "PLATFORMS": {"MARENOSTRUM4": {"TYPE": "slurm", "HOST": "mn1.bsc.es", "PROJECT": "bsc32", "USER": "bsc32070", "QUEUE": "debug", "SCRATCH_DIR": "/gpfs/scratch", "ADD_PROJECT_TO_HOST": false, "MAX_WALLCLOCK": "48:00", "TEMP_DIR": ""}, "MARENOSTRUM_ARCHIVE": {"TYPE": "ps", "HOST": "dt02.bsc.es", "PROJECT": "bsc32", "USER": "bsc32xxx", "SCRATCH_DIR": "/gpfs/scratch", "ADD_PROJECT_TO_HOST": false, "TEST_SUITE": false}, "TRANSFER_NODE": {"TYPE": "ps", "HOST": "dt01.bsc.es", "PROJECT": "bsc32", "USER": "bsc32xxx", "ADD_PROJECT_TO_HOST": false, "SCRATCH_DIR": "/gpfs/scratch"}, "TRANSFER_NODE_BSCEARTH000": {"TYPE": "ps", "HOST": "bscearth000", "USER": "dbeltran", "PROJECT": "Earth", "ADD_PROJECT_TO_HOST": false, "QUEUE": "serial", "SCRATCH_DIR": "/esarchive/scratch"}, "BSCEARTH000": {"TYPE": "ps", "HOST": "bscearth000", "USER": "dbeltran", "PROJECT": "Earth", "ADD_PROJECT_TO_HOST": false, "QUEUE": "serial", "SCRATCH_DIR": "/esarchive/scratch"}, "NORD3": {"TYPE": "SLURM", "HOST": "nord1.bsc.es", "PROJECT": "bsc32", "USER": "bsc32xxx", "QUEUE": "debug", "SCRATCH_DIR": "/gpfs/scratch", "MAX_WALLCLOCK": "48:00"}, "ECMWF-XC40": {"TYPE": "ecaccess", "VERSION": "pbs", "HOST": "cca", "USER": "c3d", "PROJECT": "spesiccf", "ADD_PROJECT_TO_HOST": false, "SCRATCH_DIR": "/scratch/ms", "QUEUE": "np", "SERIAL_QUEUE": "ns", "MAX_WALLCLOCK": "48:00"}}, "ROOTDIR": "/home/dbeltran/new_autosubmit/a01s", "PROJDIR": "/home/dbeltran/new_autosubmit/a01s/proj/project_files", "DEFAULT": {"EXPID": "a01s", "HPCARCH": "local", "CUSTOM_CONFIG": "/home/dbeltran/new_autosubmit/a01s/proj/git_project/as_conf"}, "PROJECT": {"PROJECT_TYPE": "git", "PROJECT_DESTINATION": "git_project"}, "GIT": {"PROJECT_ORIGIN": "https://earth.bsc.es/gitlab/dbeltran/edito-vanilla", "PROJECT_BRANCH": "main", "PROJECT_COMMIT": "", "PROJECT_SUBMODULES": "", "FETCH_SINGLE_BRANCH": true}}');
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
