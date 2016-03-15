## klctags

klctags generator


## Install

* clone or dowrload repo
* append "klctags" directory to $PATH or (%PATH% in windows)
 

## Usage

* source your fabric engine environment.bat for access fe core client via python scripts.
* run ```klctags -h ```

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
                        output tags file name. if not supplyed and enabled -b,
                        using kl.builtin.ctags as default if not supplyed and
                        enabled -c, using kl.user.ctags as default if not
                        supplyed and enabled -f, using stdout as default
                        output

```


## Using with Vim

* sample _vimrc for Tagbar
``` vim
""" fabric engine + tagbar integration
let $FABRIC_DIR="D:/fabric/release"
let $PATH=$FABRIC_DIR."/bin;".$PATH
let $PYTHONPATH=$FABRIC_DIR."/Python/2.7;".$PYTHONPATH

let $FABRIC_EXTS_PATH=$FABRIC_DIR."/Exts;".$FABRIC_DIR."/Tests"
let $FABRIC_DFG_PATH=$FABRIC_DIR."/Presets/DFG"

let g:tagbar_type_kl = {
    \ 'ctagsbin'  : 'klctags.py',
    \ 'ctagsargs' : '-f',
    \ 'kinds' : [
        \ 'o:object:0:1',
        \ 's:struct:0:1',
        \ 'i:interface:0:1',
        \ 'm:method:0:1',
        \ 'v:member:0:0',
        \ 'f:function:0:1',
        \ 'p:operator:0:1'
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
