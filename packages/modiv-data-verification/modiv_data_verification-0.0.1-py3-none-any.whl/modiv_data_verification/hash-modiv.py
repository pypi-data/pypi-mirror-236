from verify import Verify
import sys

verifier = Verify(sys.argv[1], sys.argv[2], sys.argv[3])
verifier.hash_modiv_records()