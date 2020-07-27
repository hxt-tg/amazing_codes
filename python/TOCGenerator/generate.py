import re

rec = re.compile(r"<h([1-6])>.+?href=\"(.+?)\"><svg.+?</a>(.+?)</h[1-6]>")
for t in rec.findall(text):
    print(f"{'  '*(int(t[0])-2)}- [{t[2]}]({t[1]})".replace('<code>', '`').replace('</code>', '`'))

