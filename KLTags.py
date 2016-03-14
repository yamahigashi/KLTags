#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
#
import os
import re
import sys
import textwrap
import argparse

from FabricEngine.Sphinx.ASTWrapper.KLManagerImpl import KLManager


##############################################################################
class KLObjectCTagsParser(object):

    file_scope = ""
    identifier = ""

    @classmethod
    def _get_line_number(self, file_path, lookup_exp):
        """ return line number where lookup matches.

        file_path:
            filepath string
        lookup_exp:
            typeof comiled RegExp
        """

        with open(file_path) as f:
            for num, line in enumerate(f, 1):
                if lookup_exp.search(line):
                    return str(num)
            else:
                # print "not match {} in {}".format(lookup_exp.pattern, file_path)
                return ""

    @classmethod
    def get_exp_for_pattern(self, tag_name):
        return "{}.*[ \t.]+{}[^\w\d]".format(self.identifier, tag_name)

    @classmethod
    def get_member(self, kl_objs):
        res = []
        for kl in kl_objs:

            kl_file = kl.getKLFile()
            ext_name = kl.getExtension()

            print kl_file

            # method
            methods = kl.getMethods()
            res.extend(MethodParser.run(kl_file, ext_name, methods))

            # member
            members = kl.getMembers()
            res.extend(MemberParser.run(kl_file, ext_name, members))

        return res

    @classmethod
    def run(self, file_path, ext, kl_objs):

        res = []
        for kl in kl_objs:

            tag_name = kl.getName()
            where = file_path

            # ex_cmds
            line_number = self._get_line_number(
                file_path,
                re.compile(self.get_exp_for_pattern(tag_name)))

            if not line_number:
                # print "continue no line_number {}".format(tag_name)
                continue

            ex_cmd = "{};\"".format(line_number)

            # extension_fields
            file_scope = self.file_scope
            access = "access:public"
            namespace = "namespace:{}".format(ext)
            extension_fields = "\t".join([file_scope, access, namespace])

            res.append("{tag_name}\t{file_name}\t{ex_cmd}\t{extension_fields}".format(
                tag_name=tag_name,
                file_name=where,
                ex_cmd=ex_cmd,
                extension_fields=extension_fields
            ))

        return res


'''
kind        Kind of tag.  The value depends on the language.  For C and
        C++ these kinds are recommended:
        c    class name
        d    define (from #define XXX)
        e    enumerator
        f    function or method name
        F    file name
        g    enumeration name
        m    member (of structure or class data)
        p    function prototype
        s    structure name
        t    typedef
        u    union name
        v    variable
        When this field is omitted, the kind of tag is undefined.

'''


class InterfacesParser(KLObjectCTagsParser):
    file_scope = "i"
    identifier = "interface"


class StructParser(KLObjectCTagsParser):
    file_scope = "s"
    identifier = "struct"

    @classmethod
    def run(self, file_path, ext, kl_objs):
        res = super(StructParser, self).run(file_path, ext, kl_objs)
        res.extend(self.get_member(kl_objs))
        return res


class ObjectParser(KLObjectCTagsParser):
    file_scope = "c"
    identifier = "object"

    @classmethod
    def run(self, file_path, ext, kl_objs):
        res = super(ObjectParser, self).run(file_path, ext, kl_objs)
        res.extend(self.get_member(kl_objs))
        return res


class FunctionParser(KLObjectCTagsParser):
    file_scope = "f"
    identifier = "function"


class MethodParser(KLObjectCTagsParser):
    file_scope = "f"
    identifier = "function"


class MemberParser(KLObjectCTagsParser):
    file_scope = "m"
    identifier = ""

    @classmethod
    def get_exp_for_pattern(self, tag_name):
        return r"[\d\w]+[\s\t]+{}([^\w\d]+=|;)".format(tag_name)


class OperatorParser(KLObjectCTagsParser):
    file_scope = "f"
    identifier = "operator"


##############################################################################


def header():
    h = textwrap.dedent("""
        !_TAG_FILE_ENCODING	UTF-8	//
        !_TAG_FILE_FORMAT	2	/extended format; --format=1 will not append ;" to lines/
        !_TAG_FILE_SORTED	1	/0=unsorted, 1=sorted, 2=foldcase/
    """)

    return h


# TODO: replace sample
def parse_file(kl_file):
    """ return lines included a file.

    Sample:
        SwipeRecognizerInspector	.\Assets\Plugins\Editor\FingerGestures\SwipeRecognizerInspector.cs	/^public class SwipeRecognizerInspector : GestureRecognizerInspector<SwipeRecognizer>$/;"	c
        ValidateValues	.\Assets\Plugins\Editor\FingerGestures\SwipeRecognizerInspector.cs	/^    protected override void ValidateValues()$/;"	m	class:SwipeRecognizerInspector
        ShowRequiredFingerCount	.\Assets\Plugins\Editor\FingerGestures\SwipeRecognizerInspector.cs	/^    protected override bool ShowRequiredFingerCount$/;"	p	class:SwipeRecognizerInspector
        LABEL_MaxDeviation	.\Assets\Plugins\Editor\FingerGestures\SwipeRecognizerInspector.cs	/^    protected static GUIContent LABEL_MaxDeviation = new GUIContent( "Max Deviation", "Maximum angle that the swipe direction is allowed to deviate from its initial direction (in degrees)" );$/;"	f	class:SwipeRecognizerInspector
        LABEL_MaxDistance	.\Assets\Plugins\Editor\FingerGestures\SwipeRecognizerInspector.cs	/^    protected static GUIContent LABEL_MaxDistance = new GUIContent( "Max Distance", "Finger travel distance beyond which the swipe recognition will fail.\\nSetting this to 0 disables the constraint" );$/;"	f	class:SwipeRecognizerInspector
        LABEL_MinVelocity	.\Assets\Plugins\Editor\FingerGestures\SwipeRecognizerInspector.cs	/^    protected static GUIContent LABEL_MinVelocity = new GUIContent( "Min Velocity", "Minimum speed the finger must maintain in order to produce a valid swipe gesture" );$/;"	f	class:SwipeRecognizerInspector
        LABEL_MinDistance	.\Assets\Plugins\Editor\FingerGestures\SwipeRecognizerInspector.cs	/^    protected static GUIContent LABEL_MinDistance = new GUIContent( "Min Distance", "Minimum distance the finger must travel in order to produce a valid swipe" );$/;"	f	class:SwipeRecognizerInspector
        OnSettingsUI	.\Assets\Plugins\Editor\FingerGestures\SwipeRecognizerInspector.cs	/^    protected override void OnSettingsUI()$/;"	m	class:SwipeRecognizerInspector
    """

    filepath = kl_file.getFilePath()
    if not os.path.exists(filepath):
        print "file not exists"
        # raise FileNotFoundError
        return ""

    try:
        ext_name = getattr(kl_file, "_KLFile__extension").getName()
    except AttributeError:
        ext_name = ""

    interfaces = kl_file.getInterfaces()
    structs = kl_file.getStructs()
    objects = kl_file.getObjects()
    funcs = kl_file.getFreeFunctions(includeInternal=True)

    res = []
    res.extend(StructParser.run(filepath, ext_name, structs))
    res.extend(ObjectParser.run(filepath, ext_name, objects))
    res.extend(InterfacesParser.run(filepath, ext_name, interfaces))
    res.extend(FunctionParser.run(filepath, ext_name, funcs))

    return res


##############################################################################
#
##############################################################################
def generate_for_builtins(output_path="kl.builtin.ctags"):
    ''' generate tags for builtin extensions. '''

    res = []
    man = KLManager()

    for f in man.getKLFiles():
        res.extend(parse_file(f))

    res = list(set(res))
    with open(output_path, 'w') as f:
        f.write("\n".join(res))


def generate_for_custom_exts(output_path="kl.user.ctags"):
    ''' genarte for '''

    paths = os.environ['FABRIC_EXTS_PATH'].split(os.pathsep)[1:]

    res = []
    man = KLManager(paths=paths)

    # for ex in man.getKLExtensions():
    #    print ex.getName()

    for f in man.getKLFiles():
        res.extend(parse_file(f))

    res = list(set(res))
    with open(output_path, 'w') as f:
        f.write("\n".join(res))


def generate_for_one_file(input_path, output_path):

    res = []

    from FabricEngine.Sphinx.ASTWrapper.KLFileImpl import KLFile
    f = KLFile(input_path)
    res.extend(parse_file(f))

    res = list(set(res))
    with open(output_path, 'w') as f:
        f.write("\n".join(res))


##############################################################################
# parser setup
##############################################################################
parser = argparse.ArgumentParser()

parser.add_argument(
    '-b', '--builtin',
    action='store_true',
    default=False,
    help='generate tags for builtin exts',
)

parser.add_argument(
    '-c', '--custom',
    action='store_true',
    default=False,
    help='generate tags for user exts',
)

parser.add_argument(
    '-f', '--file',
    nargs='?',
    type=argparse.FileType('r'),
    default=sys.stdin
)

parser.add_argument(
    '-o', '--output',
    nargs='?',
    type=argparse.FileType('r')
)
##############################################################################

if __name__ == '__main__':
    args = parser.parse_args()

    if args.output:
        output = args.output
    else:
        output = None

    if args.builtin:
        generate_for_builtins()

    if args.custom:
        generate_for_custom_exts()

    if args.file:
        input = args.file.name

        if not output:
            output = os.path.abspath(
                os.path.splitext(input)[0] + ".ctags")

        generate_for_one_file(input, output)
