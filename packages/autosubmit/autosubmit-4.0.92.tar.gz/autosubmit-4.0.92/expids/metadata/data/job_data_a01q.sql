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
INSERT INTO experiment_run VALUES(1,'2023-10-05-13:54:59','2023-10-05-13:58:51',1696506899,1696507131,'month',1,0,1,0,0,0,0,0,'{"PROJECT": {"PROJECT_TYPE": "none", "PROJECT_DESTINATION": "auto-icon"}, "EXPERIMENT": {"DATELIST": 20000101, "MEMBERS": "default", "CHUNKSIZEUNIT": "month", "CHUNKSIZE": 1, "NUMCHUNKS": 1, "CHUNKINI": "", "CALENDAR": "standard"}, "NAMELIST": {"MASTER": "icon_master.namelist", "EXP": "%DEFAULT.TEMPLATE%.nml"}, "DIRECTORIES": {"ICONDIR": "%HPCROOTDIR%/icon", "INDIR": "my-updated-indir", "OUTDIR": "from_main", "TESTDIR": "another-dir", "TEST_FILE": "from_main"}, "JOBS": {"COPY_NAMELIST": {"FILE": "jobscripts/copy_namelist.sh", "RUNNING": "once", "DEPENDENCIES": {}, "ADDITIONAL_FILES": []}}, "PLATFORMS": {"LEVANTE": {"TYPE": "slurm", "HOST": "levante.dkrz.de", "USER": "b382351", "PROJECT": "bb1153", "SCRATCH_DIR": "/work", "MAX_WALLCLOCK": "08:00", "PROCESSORS_PER_NODE": 128, "QUEUE": "p", "PARTITION": "compute", "SERIAL_PLATFORM": "LEVANTE-SERIAL"}, "LEVANTE-SERIAL": {"TYPE": "slurm", "HOST": "levante.dkrz.de", "USER": "", "PROJECT": "", "SCRATCH_DIR": "/work", "MAX_WALLCLOCK": "08:00", "PROCESSORS_PER_NODE": 128, "QUEUE": "s", "PARTITION": "shared"}, "TEST-LOCAL": {"TYPE": "slurm", "HOST": "localhost", "USER": "dbeltran", "PROJECT": "whatever", "SCRATCH_DIR": "/home/dbeltran"}, "ECMWF-HPC2020": {"TYPE": "ecaccess", "VERSION": "slurm", "HOST": "hpc-login", "QUEUE": "nf", "EC_QUEUE": "hpc", "BUDGET": null, "USER": "c3d", "SCRATCH_DIR": "/ec/res4/scratch/c3d", "PROJECT": "spesiccf", "ADD_PROJECT_TO_HOST": false, "MAX_WALLCLOCK": "48:00", "CUSTOM_DIRECTIVES": "#SBATCH --hint=nomultithread"}, "POWER9": {"TYPE": "slurm", "HOST": "plogin1.bsc.es", "USER": "bsc32070", "PROJECT": "bsc32", "SCRATCH_DIR": "/gpfs/scratch", "QUEUE": "debug"}, "LEVANTE-LOGIN": {"TYPE": "slurm", "HOST": "levante.dkrz.de", "USER": "b382351", "PROJECT": "bb1153", "SCRATCH_DIR": "/work", "PARTITION": "interactive"}, "MARENOSTRUM0": {"TYPE": "slurm", "HOST": "marenostrum0", "PROJECT": "bsc32", "USER": "bsc32070", "SCRATCH_DIR": "/gpfs/scratch", "MAX_WALLCLOCK": "48:00", "MAX_PROCESSORS": "2400", "PROCESSORS_PER_NODE": "48", "SERIAL_QUEUE": "debug", "QUEUE": "debug"}, "MARENOSTRUM4": {"TYPE": "slurm", "HOST": "bsc", "PROJECT": "bsc32", "USER": "bsc32070", "SCRATCH_DIR": "/gpfs/scratch", "ADD_PROJECT_TO_HOST": "False", "MAX_WALLCLOCK": "48:00", "MAX_PROCESSORS": "2400", "PROCESSORS_PER_NODE": "48", "SERIAL_QUEUE": "debug", "QUEUE": "debug"}, "MARENOSTRUM_ARCHIVE": {"TYPE": "ps", "HOST": "dt01.bsc.es", "PROJECT": "bsc32", "USER": "bsc32070", "SCRATCH_DIR": "/gpfs/scratch", "ADD_PROJECT_TO_HOST": "False", "TEST_SUITE": "False"}, "TRANSFER_NODE": {"TYPE": "ps", "HOST": "dt01.bsc.es", "PROJECT": "bsc32", "USER": "bsc32070", "ADD_PROJECT_TO_HOST": "false", "SCRATCH_DIR": "/gpfs/scratch"}}, "TESTKEY": "abcd", "TOCHANGE": "eksdldf", "TESTKEY-TWO": "HPCARCH is levante", "TOLOAD": "from_testfile2", "TESTKEY-LEVANTE": "L-abcd", "TOLOAD2": "from_version", "CONFIG": {"AUTOSUBMIT_VERSION": "4.1.0b", "TOTALJOBS": 20, "MAXWAITINGJOBS": 20}, "ROOTDIR": "/home/dbeltran/new_autosubmit/a01q", "PROJDIR": "/home/dbeltran/new_autosubmit/a01q/proj/project_files", "DEFAULT": {"EXPID": "a00a", "HPCARCH": "levante", "CUSTOM_CONFIG": {"PRE": "/home/dbeltran/new_autosubmit/a01q/proj/auto-icon/config/common,/home/dbeltran/new_autosubmit/a01q/proj/auto-icon/config/testfile.yml,/home/dbeltran/new_autosubmit/a01q/proj/auto-icon/config/testfile2.yml,/home/dbeltran/new_autosubmit/a01q/proj/auto-icon/config/testfile-levante.yml", "POST": "~/platforms.yml"}}, "GIT": {"PROJECT_ORIGIN": "git@gitlab.dkrz.de:auto-icon/auto-icon.git", "PROJECT_BRANCH": "refactor-config-loading", "PROJECT_COMMIT": "", "PROJECT_SUBMODULES": "", "FETCH_SINGLE_BRANCH": true}, "STORAGE": {}}');
INSERT INTO experiment_run VALUES(2,'2023-10-05-13:58:51','2023-10-05-13:58:51',1696507131,0,'month',1,0,1,0,0,0,0,0,'{"PROJECT": {"PROJECT_TYPE": "none", "PROJECT_DESTINATION": "auto-icon"}, "EXPERIMENT": {"DATELIST": 20000101, "MEMBERS": "default", "CHUNKSIZEUNIT": "month", "CHUNKSIZE": 1, "NUMCHUNKS": 1, "CHUNKINI": "", "CALENDAR": "standard"}, "NAMELIST": {"MASTER": "icon_master.namelist", "EXP": "%DEFAULT.TEMPLATE%.nml"}, "DIRECTORIES": {"ICONDIR": "%HPCROOTDIR%/icon", "INDIR": "my-updated-indir", "OUTDIR": "from_main", "TESTDIR": "another-dir", "TEST_FILE": "from_main"}, "JOBS": {"COPY_NAMELIST": {"FILE": "jobscripts/copy_namelist.sh", "RUNNING": "once", "DEPENDENCIES": {}, "ADDITIONAL_FILES": []}}, "PLATFORMS": {"LEVANTE": {"TYPE": "slurm", "HOST": "levante.dkrz.de", "USER": "b382351", "PROJECT": "bb1153", "SCRATCH_DIR": "/work", "MAX_WALLCLOCK": "08:00", "PROCESSORS_PER_NODE": 128, "QUEUE": "p", "PARTITION": "compute", "SERIAL_PLATFORM": "LEVANTE-SERIAL"}, "LEVANTE-SERIAL": {"TYPE": "slurm", "HOST": "levante.dkrz.de", "USER": "", "PROJECT": "", "SCRATCH_DIR": "/work", "MAX_WALLCLOCK": "08:00", "PROCESSORS_PER_NODE": 128, "QUEUE": "s", "PARTITION": "shared"}, "TEST-LOCAL": {"TYPE": "slurm", "HOST": "localhost", "USER": "dbeltran", "PROJECT": "whatever", "SCRATCH_DIR": "/home/dbeltran"}, "ECMWF-HPC2020": {"TYPE": "ecaccess", "VERSION": "slurm", "HOST": "hpc-login", "QUEUE": "nf", "EC_QUEUE": "hpc", "BUDGET": null, "USER": "c3d", "SCRATCH_DIR": "/ec/res4/scratch/c3d", "PROJECT": "spesiccf", "ADD_PROJECT_TO_HOST": false, "MAX_WALLCLOCK": "48:00", "CUSTOM_DIRECTIVES": "#SBATCH --hint=nomultithread"}, "POWER9": {"TYPE": "slurm", "HOST": "plogin1.bsc.es", "USER": "bsc32070", "PROJECT": "bsc32", "SCRATCH_DIR": "/gpfs/scratch", "QUEUE": "debug"}, "LEVANTE-LOGIN": {"TYPE": "slurm", "HOST": "levante.dkrz.de", "USER": "b382351", "PROJECT": "bb1153", "SCRATCH_DIR": "/work", "PARTITION": "interactive"}, "MARENOSTRUM0": {"TYPE": "slurm", "HOST": "marenostrum0", "PROJECT": "bsc32", "USER": "bsc32070", "SCRATCH_DIR": "/gpfs/scratch", "MAX_WALLCLOCK": "48:00", "MAX_PROCESSORS": "2400", "PROCESSORS_PER_NODE": "48", "SERIAL_QUEUE": "debug", "QUEUE": "debug"}, "MARENOSTRUM4": {"TYPE": "slurm", "HOST": "bsc", "PROJECT": "bsc32", "USER": "bsc32070", "SCRATCH_DIR": "/gpfs/scratch", "ADD_PROJECT_TO_HOST": "False", "MAX_WALLCLOCK": "48:00", "MAX_PROCESSORS": "2400", "PROCESSORS_PER_NODE": "48", "SERIAL_QUEUE": "debug", "QUEUE": "debug"}, "MARENOSTRUM_ARCHIVE": {"TYPE": "ps", "HOST": "dt01.bsc.es", "PROJECT": "bsc32", "USER": "bsc32070", "SCRATCH_DIR": "/gpfs/scratch", "ADD_PROJECT_TO_HOST": "False", "TEST_SUITE": "False"}, "TRANSFER_NODE": {"TYPE": "ps", "HOST": "dt01.bsc.es", "PROJECT": "bsc32", "USER": "bsc32070", "ADD_PROJECT_TO_HOST": "false", "SCRATCH_DIR": "/gpfs/scratch"}}, "TESTKEY": "abcd", "TOCHANGE": "eksdldf", "TESTKEY-TWO": "HPCARCH is levante", "TOLOAD": "from_testfile2", "TESTKEY-LEVANTE": "L-abcd", "TOLOAD2": "from_version", "CONFIG": {"AUTOSUBMIT_VERSION": "4.1.0b", "TOTALJOBS": 20, "MAXWAITINGJOBS": 20}, "ROOTDIR": "/home/dbeltran/new_autosubmit/a01q", "PROJDIR": "/home/dbeltran/new_autosubmit/a01q/proj/project_files", "DEFAULT": {"EXPID": "a00a", "HPCARCH": "levante", "CUSTOM_CONFIG": {"PRE": "/home/dbeltran/new_autosubmit/a01q/proj/auto-icon/config/common,/home/dbeltran/new_autosubmit/a01q/proj/auto-icon/config/testfile.yml,/home/dbeltran/new_autosubmit/a01q/proj/auto-icon/config/testfile2.yml,/home/dbeltran/new_autosubmit/a01q/proj/auto-icon/config/testfile-levante.yml", "POST": "~/platforms.yml"}}, "GIT": {"PROJECT_ORIGIN": "git@gitlab.dkrz.de:auto-icon/auto-icon.git", "PROJECT_BRANCH": "refactor-config-loading", "PROJECT_COMMIT": "", "PROJECT_SUBMODULES": "", "FETCH_SINGLE_BRANCH": true}, "STORAGE": {}}');
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
INSERT INTO sqlite_sequence VALUES('experiment_run',2);
CREATE INDEX ID_JOB_NAME ON job_data(job_name);
COMMIT;
