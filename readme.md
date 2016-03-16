
## klctags

klctags generator


## Install

* clone or download repo
* append "klctags" directory to $PATH or (%PATH% in windows)
* apply patches, see patches folder

    * ASTWrapper.diff
    * Directive.diff
    
    in Fabric distributed python folder respectively.
    
#### patching instruction

* open command prompt as Admin
* cd Fabric's Python directory (%FABRIC_DIR%/Python/2.7/FabricEngine/Sphinx/ASTWrapper)
* ```patch < your_klctags_cloned_folder/patches/ASTWrapper.diff```
* cd Python/2.7/FabricEngine/Sphinx/Directives
* ```patch < your_klctags_cloned_folder/patches/Directives.diff```
* done!

``` console
d:\>cd fabric\latest\Python\2.7\FabricEngine\Sphinx\ASTWrapper

d:\fabric\latest\Python\2.7\FabricEngine\Sphinx\ASTWrapper>patch < d:\fabric\tools\klctags\patches\ASTWrapper.diff
patching file KLFileImpl.py
patching file KLManagerImpl.py

d:\fabric\latest\Python\2.7\FabricEngine\Sphinx\ASTWrapper>cd ..\Directives

d:\fabric\latest\Python\2.7\FabricEngine\Sphinx\Directives>patch < d:\fabric\tools\klctags\patches\Directive.diff
patching file KLBaseDirectiveImpl.py
patching file KLConstantDirectiveImpl.py
patching file KLCssDirectiveImpl.py
patching file KLExtensionConstantListDirectiveImpl.py
patching file KLExtensionFileListDirectiveImpl.py
patching file KLExtensionFunctionListDirectiveImpl.py
patching file KLExtensionInterfaceListDirectiveImpl.py
patching file KLExtensionListDirectiveImpl.py
patching file KLExtensionTypeListDirectiveImpl.py
patching file KLFileDirectiveImpl.py
patching file KLFileExampleDirectiveImpl.py
patching file KLFunctionDirectiveImpl.py
patching file KLInheritanceDirectiveImpl.py
patching file KLInterfaceDirectiveImpl.py
patching file KLMethodDirectiveImpl.py
patching file KLMethodListDirectiveImpl.py
patching file KLTypeDirectiveImpl.py
patching file KLXRefRoleImpl.py

d:\fabric\latest\Python\2.7\FabricEngine\Sphinx\Directives>
```

## Usage

* source your fabric engine environment.bat for access fe core client via python scripts.
* see help, run ```klctags -h ```

``` console
D:\fabric>klctags -h
usage: klctags.py [-h] [-b] [-c] [-f [FILE]] [-o [OUTPUT]]

optional arguments:
  -h, --help            show this help message and exit
  -b, --builtin         generate tags for builtin exts
  -c, --custom          generate tags for user exts, inculded under
                        "os.environ['FABRIC_EXTS_PATH'].split(os.pathsep)[1:]"
  -f [FILE], --file [FILE]
                        a input kl file to generate
  -o [OUTPUT], --output [OUTPUT]
                        output tags file name. if not output specified and -b
                        enabled, using kl.builtin.ctags as default if not
                        output specified and -c enabled, using kl.user.ctags
                        as default if not output specified and -f enabled,
                        using stdout as default output
```

* ```klctags -b``` generates kl.builtin.ctags for built extensions.
* ```klctags -c``` generates kl.user.ctags for user extensions.
    These extension is that included in envvar ```FABRIC_EXT_PATH``` but exclude the builtin.
* ```klctags -f some.kl``` output some.kl's tags on stdout.
* ```klctgas -f some.kl -o some.ctags``` generates some.ctags for some.kl


## Using with Vim

* sample _vimrc for Tagbar
``` vim
""" Fabric Engine + Tagbar integration
let $FABRIC_DIR="D:/fabric/release"
let $PATH=$FABRIC_DIR."/bin;".$PATH
let $PYTHONPATH=$FABRIC_DIR."/Python/2.7;".$PYTHONPATH

let $FABRIC_EXTS_PATH=$FABRIC_DIR."/Exts;".$FABRIC_DIR."/Tests"
let $FABRIC_DFG_PATH=$FABRIC_DIR."/Presets/DFG"

let g:tagbar_type_kl = {
    \ 'ctagsbin'  : 'klctags_sub.py',
    \ 'ctagsargs' : '-f',
    \ 'kinds' : [
        \ 'r:require:0:0',
        \ 'f:free function:0:1',
        \ 'p:free operator:0:1',
        \ 'o:object:0:1',
        \ 's:struct:0:1',
        \ 'i:interface:0:1',
        \ 'm:method:0:1',
        \ 'v:member:0:0',
    \ ],
    \ 'sro': '.',
    \ 'kind2scope': {
        \ 'o': 'object',
        \ 's': 'struct',
        \ 'm': 'method',
    \ },
    \ 'scope2kind' : {
        \ 'object':  'o',
        \ 'struct':  's',
        \ 'method':  'm',
    \ }
\}
```


## license

MIT
