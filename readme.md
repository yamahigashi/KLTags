``` vimrc.vim
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
