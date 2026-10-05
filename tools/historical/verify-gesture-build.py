from pathlib import Path
import subprocess, re, hashlib, zipfile
root=Path('/home/ivan/evolutionX')
product=root/'out/target/product/fairlady'
apk=product/'product/overlay/PixelLauncherOverlayCustom.apk'
aapt=root/'out/host/linux-x86/bin/aapt2'
xml=subprocess.check_output([str(aapt),'dump','xmltree','--file','res/xml/device_profiles.xml',str(apk)],text=True)
for block in xml.split('E: grid-option ')[1:]:
    name=re.search(r':name\([^\n]*?\)="([^"]+)"',block)
    if name and name[1] in ('small','custom_5x6','custom_5x7') and re.search(r':deviceCategory\([^\n]*?\)=1\n',block):
        cols=re.search(r':numColumns\([^\n]*?\)=(\d+)',block)
        rows=re.search(r':numRows\([^\n]*?\)=(\d+)',block)
        assert cols and rows
        expected={'small':('5','5'),'custom_5x6':('5','6'),'custom_5x7':('5','7')}[name[1]]
        assert (cols[1],rows[1])==expected
        print(name[1],cols[1]+'x'+rows[1], 'PASS')
assert len(xml.split('E: grid-option '))-1==13
files=product/'obj/PACKAGING/target_files_intermediates/lineage_fairlady-target_files'
for installed, target in [('product/overlay/PixelLauncherOverlayCustom.apk','PRODUCT/overlay/PixelLauncherOverlayCustom.apk'),('system_ext/priv-app/SystemUIGoogle/SystemUIGoogle.apk','SYSTEM_EXT/priv-app/SystemUIGoogle/SystemUIGoogle.apk')]:
    assert hashlib.sha256((product/installed).read_bytes()).digest()==hashlib.sha256((files/target).read_bytes()).digest()
    print('Target-files match:',installed)