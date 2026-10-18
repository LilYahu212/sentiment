"""Раз в час: процент лонгов розницы по брокерам (FXSSI current-ratios) -> data/fxssi_YYYY-MM.csv
Столбцы: t_utc, broker, symbol, long_pct. Без логина, только стандартная библиотека."""
import csv, json, os, urllib.request
from datetime import datetime, timezone
URL = 'https://c.fxssi.com/api/current-ratios'
req = urllib.request.Request(URL, headers={'User-Agent': 'Mozilla/5.0 (research recorder, hourly)', 'Referer': 'https://fxssi.com/tools/current-ratio'})
d = json.loads(urllib.request.urlopen(req, timeout=60).read().decode('utf8'))
now = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M')
rows = [(now, b, s, v) for b, sym in d.get('brokers', {}).items() for s, v in sym.items()]
os.makedirs('data', exist_ok=True)
f = f"data/fxssi_{datetime.now(timezone.utc):%Y-%m}.csv"; new = not os.path.exists(f)
with open(f, 'a', newline='') as fh:
    w = csv.writer(fh)
    if new: w.writerow(['t_utc', 'broker', 'symbol', 'long_pct'])
    w.writerows(rows)
print(now, 'записано строк:', len(rows), '->', f)
