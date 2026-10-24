#!/bin/bash
# Usage: tools/gallery.sh ~/Downloads/photos/*.jpg  -> converts to WebP in img/gallery and rebuilds gallery.json
cd "$(dirname "$0")/.."
for f in "$@"; do b=$(basename "${f%.*}"); python3 -c "from PIL import Image,ImageOps;im=ImageOps.exif_transpose(Image.open('$f')).convert('RGB');im.thumbnail((1600,1600));im.save('img/gallery/$b.webp','WEBP',quality=78)"; done
python3 -c "import os,json;print(json.dumps([{'file':f,'alt':'תמונה מהמוסך א.ל שירותי תעבורה'} for f in sorted(os.listdir('img/gallery')) if f.endswith('.webp')],ensure_ascii=False))" > img/gallery/gallery.json
