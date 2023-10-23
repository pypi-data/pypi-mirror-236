from pkrhistoryreader.reader import HistoryReader
from datetime import datetime
import random
import threading

pkrreader = HistoryReader()
keys = [o.key for o in pkrreader.bucket.objects.filter(Prefix="data/histories/split/2023/08")]
key = keys[1000]
result = pkrreader.parse_history_from_key(key)
print(result.get("Winners"))
