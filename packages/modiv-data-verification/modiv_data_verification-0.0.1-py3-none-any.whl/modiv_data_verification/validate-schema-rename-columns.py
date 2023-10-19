from verify import Verify
import sys

verifier = Verify(sys.argv[1], sys.argv[2], sys.argv[3])
verifier.verify_schema_map_columns()