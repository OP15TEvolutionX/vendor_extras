from pathlib import Path
import subprocess,re
root=Path('/home/ivan/evolutionX'); product=root/'out/target/product/fairlady';host=root/'out/host/linux-x86/bin';target=root/'vendor/gms/system_ext/packages/privileged_apps/NexusLauncherRelease/NexusLauncherRelease.apk';output=root/'pixel_grid_probe/padding-idmaps';output.mkdir(exist_ok=True)
for value in [24,28,36,48]:
 apk=product/f'product/overlay/PixelLauncherBottomPadding{value}.apk'
 xml=subprocess.check_output([str(host/'aapt2'),'dump','xmltree','--file','res/xml/spec_handheld_hotseat_5_col.xml',str(apk)],text=True)
 edges=re.findall(r'E: edgePadding[^\n]*\n\s+A:[^\n]*fixedSize\([^\n]*?\)=([0-9.]+)dp',xml)
 assert [float(x) for x in edges]==[float(value),0.0],edges
 manifest=subprocess.check_output([str(host/'aapt2'),'dump','xmltree','--file','AndroidManifest.xml',str(apk)],text=True)
 assert 'targetName' not in manifest and 'isStatic' in manifest and '=false' in manifest and 'bottom_padding' in manifest
 idmap=output/f'padding{value}.idmap'
 subprocess.run([str(host/'idmap2'),'create','--target-apk-path',str(target),'--overlay-apk-path',str(apk),'--idmap-path',str(idmap),'--policy','product','--policy','public'],check=True)
 mapping=subprocess.check_output([str(host/'idmap2'),'dump','--idmap-path',str(idmap)],text=True)
 resource_lines=[l for l in mapping.splitlines() if ' -> ' in l and '0x7f' in l]
 assert len(resource_lines)==1 and 'xml/spec_handheld_hotseat_5_col' in resource_lines[0],mapping
 print(f'PASS {value}dp: mutable, shared category, no targetName, product policy accepted, only hotseat spec mapped')
base=product/'product/overlay/PixelLauncherOverlayCustom.apk'
xml=subprocess.check_output([str(host/'aapt2'),'dump','xmltree','--file','res/xml/spec_handheld_hotseat_5_col.xml',str(base)],text=True)
edges=re.findall(r'E: edgePadding[^\n]*\n\s+A:[^\n]*fixedSize\([^\n]*?\)=([0-9.]+)dp',xml)
assert [float(x) for x in edges]==[28.0,0.0]
print('PASS base default 28dp')