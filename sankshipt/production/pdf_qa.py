"""Independent PDF structural/font/image/render QA. Does not modify PDF."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import argparse,json,subprocess,shutil,hashlib,re
from pypdf import PdfReader
from pypdf.generic import ContentStream
from PIL import Image,ImageChops

def deref(x):return x.get_object()if hasattr(x,'get_object')else x
def font_receipts(resources,seen=None):
 seen=seen or set();result=[]
 resources=deref(resources or {})
 for name,ref in deref(resources.get('/Font',{})).items():
  f=deref(ref);key=str(f.get('/BaseFont',name))+str(f.get('/Subtype'))
  if key in seen:continue
  seen.add(key);subtype=str(f.get('/Subtype'));program=False
  if subtype=='/Type3':program=bool(deref(f.get('/CharProcs',{})))
  descendants=deref(f.get('/DescendantFonts',[]))
  for candidate in [f]+[deref(d)for d in descendants]:
   fd=deref(candidate.get('/FontDescriptor',{}))
   if any(fd.get(k)for k in ['/FontFile','/FontFile2','/FontFile3']):program=True
  result.append({'name':str(f.get('/BaseFont',name)),'subtype':subtype,'embedded_or_type3_selfcontained':program,'type3_charprocs':len(deref(f.get('/CharProcs',{})))if subtype=='/Type3'else None})
 for ref in deref(resources.get('/XObject',{})).values():
  x=deref(ref)
  if x.get('/Subtype')=='/Form':result+=font_receipts(x.get('/Resources',{}),seen)
 return result

def mul(a,b):
 return [a[0]*b[0]+a[2]*b[1],a[1]*b[0]+a[3]*b[1],a[0]*b[2]+a[2]*b[3],a[1]*b[2]+a[3]*b[3],a[0]*b[4]+a[2]*b[5]+a[4],a[1]*b[4]+a[3]*b[5]+a[5]]

def image_placements(stream,resources,reader,ctm=None,depth=0):
 if depth>12:return []
 ctm=list(ctm or [1,0,0,1,0,0]);stack=[];rows=[];resources=deref(resources or {});xobjects=deref(resources.get('/XObject',{}))
 try:ops=ContentStream(stream,reader).operations
 except Exception:return []
 for args,op in ops:
  if op==b'q':stack.append(ctm.copy())
  elif op==b'Q':ctm=stack.pop()if stack else [1,0,0,1,0,0]
  elif op==b'cm':ctm=mul(ctm,[float(n)for n in args])
  elif op==b'Do'and args and args[0]in xobjects:
   x=deref(xobjects[args[0]])
   if x.get('/Subtype')=='/Image':
    wpt=(ctm[0]**2+ctm[1]**2)**.5;hpt=(ctm[2]**2+ctm[3]**2)**.5;w=int(x.get('/Width',0));h=int(x.get('/Height',0))
    rows.append({'resource':str(args[0]),'width_px':w,'height_px':h,'width_pt':round(wpt,3),'height_pt':round(hpt,3),'effective_dpi_x':round(w*72/wpt,2)if wpt else None,'effective_dpi_y':round(h*72/hpt,2)if hpt else None,'color_space':str(x.get('/ColorSpace')),'bits':x.get('/BitsPerComponent'),'mask':bool(x.get('/ImageMask',False))})
   elif x.get('/Subtype')=='/Form':rows+=image_placements(x,x.get('/Resources',resources),reader,mul(ctm,[float(n)for n in x.get('/Matrix',[1,0,0,1,0,0])]),depth+1)
 return rows

def native_page_text(pdf, expected_pages):
 """Use Poppler's page-delimited text output when the tool is available."""
 executable=shutil.which('pdftotext')
 if not executable:
  return None
 try:
  result=subprocess.run([executable,'-enc','UTF-8','-raw',str(pdf),'-'],check=True,capture_output=True,timeout=120)
 except (subprocess.SubprocessError,OSError):
  return None
 pages=result.stdout.decode('utf-8',errors='replace').split('\f')
 if pages and not pages[-1].strip():
  pages.pop()
 return pages if len(pages)==expected_pages else None

def render_sample(renderer,pdf,out,dpi,page):
 prefix=out/f'page-{page:04d}'
 subprocess.run([renderer,'-f',str(page),'-l',str(page),'-r',str(dpi),'-singlefile','-png',str(pdf),str(prefix)],check=True,capture_output=True,timeout=180)
 file=prefix.with_suffix('.png')
 with Image.open(file) as proof:
  image=proof.convert('RGB')
 red,green,blue=image.split()
 difference=max(ImageChops.difference(red,green).getextrema()[1],ImageChops.difference(red,blue).getextrema()[1])
 histogram=image.convert('L').histogram()
 return {'page':page,'file':str(file),'pixels':image.size,'max_channel_difference':difference,'nonwhite_fraction':sum(histogram[:250])/sum(histogram)}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--pdf',required=True);ap.add_argument('--out',required=True);ap.add_argument('--expected-pages',type=int,required=True);ap.add_argument('--sample-pages',nargs='*',default=[]);ap.add_argument('--dpi',type=int,default=110);ap.add_argument('--inventory');ap.add_argument('--native-text',action='store_true',help='Use Poppler text extraction, with pypdf fallback');ap.add_argument('--render-workers',type=int,choices=range(1,5),default=1);a=ap.parse_args()
 pdf=Path(a.pdf).resolve();out=Path(a.out).resolve();out.mkdir(parents=True,exist_ok=True)
 reader=PdfReader(pdf);problems=[];warnings=[];pages=[];fonts={};image_color_checks={}
 native_text=native_page_text(pdf,len(reader.pages)) if a.native_text else None
 text_engine='pdftotext' if native_text is not None else 'pypdf'
 if a.native_text and native_text is None:warnings.append('Poppler text extraction unavailable or page count disagreed; used pypdf')
 if len(reader.pages)!=a.expected_pages:problems.append(f'Page count {len(reader.pages)} != {a.expected_pages}')
 for i,p in enumerate(reader.pages,1):
  box=[float(v)for v in p.mediabox];width=box[2]-box[0];height=box[3]-box[1];text=(native_text[i-1] if native_text is not None else p.extract_text())or''
  if abs(width-468)>.05 or abs(height-684)>.05:problems.append(f'Page {i} wrong MediaBox {box}')
  if not text.strip():problems.append(f'Page {i} no extractable text; independently inspect for image-only matter')
  for f in font_receipts(p.get('/Resources',{})):
   fonts[f['name']+f['subtype']]=f
  images=image_placements(p.get_contents(),p.get('/Resources',{}),reader)
  if any(x['color_space'] not in ['/DeviceGray','None']for x in images):
   for im in p.images:
    key=hashlib.sha256(im.data).hexdigest()
    if key in image_color_checks:continue
    decoded=im.image.convert('RGB');ir,ig,ib=decoded.split();difference=max(ImageChops.difference(ir,ig).getextrema()[1],ImageChops.difference(ir,ib).getextrema()[1]);image_color_checks[key]={'first_page':i,'name':im.name,'pixels':decoded.size,'max_channel_difference':difference}
    if difference>2:problems.append(f'Image {im.name} page{i} contains color channel difference {difference}')
  low=[x for x in images if not x['mask']and min(x.get('effective_dpi_x')or 9999,x.get('effective_dpi_y')or 9999)<295]
  if low:problems.append(f'Page {i}: {len(low)} images below ~300 effective DPI')
  pages.append({'page':i,'mediabox':box,'text_characters':len(text),'text_preview':text[:90],'images':images})
  if i%50==0:print(json.dumps({'progress_page':i,'problems_so_far':len(problems),'image_pixel_checks':len(image_color_checks)}),flush=True)
 missing=[f for f in fonts.values()if not f['embedded_or_type3_selfcontained']]
 if missing:problems.append('Fonts lack embedded program/Type3 CharProcs: '+str([f['name']for f in missing]))
 requested=[]
 for v in a.sample_pages:
  for s in v.split(','):
   if s:requested.append(int(s))
 samples=sorted(set([1,len(reader.pages)]+requested));renders=[]
 renderer=shutil.which('pdftoppm')
 if not renderer:problems.append('pdftoppm unavailable; no independent PDF raster proof')
 else:
  valid_samples=[page for page in samples if 1<=page<=len(reader.pages)]
  warnings.extend(f'Skipped invalid sample {page}' for page in samples if page not in valid_samples)
  with ThreadPoolExecutor(max_workers=a.render_workers) as pool:
   renders=list(pool.map(lambda page:render_sample(renderer,pdf,out,a.dpi,page),valid_samples))
  for sample in renders:
   if sample['max_channel_difference']>2:problems.append(f"Page {sample['page']}: color channel difference {sample['max_channel_difference']}")
   if sample['nonwhite_fraction']<.0002:problems.append(f"Page {sample['page']}: visually near blank")
 info=shutil.which('pdfinfo')
 if info:
  p=subprocess.run([info,str(pdf)],capture_output=True,text=True);(out/'pdfinfo.txt').write_text(p.stdout+p.stderr,encoding='utf-8')
 source_changes=[]
 if a.inventory:
  inv=json.loads(Path(a.inventory).read_text(encoding='utf-8'));root=Path(inv['root'])
  for r in inv['records']:
   f=root/r['path'];current=hashlib.sha256(f.read_bytes()).hexdigest()if f.exists()else None
   if current!=r['sha256']:source_changes.append({'path':r['path'],'inventory_sha256':r['sha256'],'current_sha256':current})
  if source_changes:problems.append(f'{len(source_changes)} source files changed since inventory')
 result={'pdf':str(pdf),'sha256':hashlib.sha256(pdf.read_bytes()).hexdigest(),'pages':len(reader.pages),'expected_pages':a.expected_pages,'text_engine':text_engine,'page_receipts':pages,'fonts':list(fonts.values()),'non_gray_colorspace_image_pixel_checks':list(image_color_checks.values()),'sample_renders':renders,'source_changes':source_changes,'problems':problems,'warnings':warnings,'passed':not problems,'limitations':['Text extraction is not source-coverage proof.','Sample render grayscale checks do not constitute printer ICC/PDF-X certification.','PDF image CTM-based placements include nested Forms; unusual masks/tiling patterns require manual inspection.']}
 (out/'pdf-qa.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps({'passed':not problems,'page_count':len(reader.pages),'fonts':len(fonts),'rendered_samples':len(renders),'problems':problems},ensure_ascii=False));return 0 if not problems else 1
if __name__=='__main__':raise SystemExit(main())
