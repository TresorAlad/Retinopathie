import os
import tempfile

_tmp = tempfile.mkdtemp(prefix="blockchain_unit_")
os.environ["BLOCKCHAIN_DATA_DIR"] = _tmp
os.environ["BLOCKCHAIN_POW_DIFFICULTY"] = "2"
