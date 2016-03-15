#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# TODO: write comment here
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
                    # return str(num)
                    return "/^{}$/".format(line.rstrip())
            else:
                # print "not match {} in {}".format(lookup_exp.pattern, file_path)
                return ""

    @classmethod
    def get_exp_for_pattern(self, tag_name):
        return "{}.*[ \t.]+{}[^\w\d]".format(self.identifier, tag_name)

    @classmethod
    def get_members(self, kl_objs):
        res = []
        for kl in kl_objs:

            kl_file = kl.getKLFile()
            ext_name = kl.getExtension()

            # method
            methods = kl.getMethods()
            res.extend(MethodParser.run(kl_file, ext_name, methods, kl))

            # member
            members = kl.getMembers()
            res.extend(MemberParser.run(kl_file, ext_name, members, kl))

        return res

    @classmethod
    def get_extension_field_elements(self, ext, kl, parent=None):
        file_scope = "kind:{}".format(self.file_scope)
        access = "access:public"
        namespace = "namespace:None"  # "namespace:{}".format(ext)

        return [file_scope, access, namespace]

    @classmethod
    def get_extension_field(self, ext, kl, parent=None):
        extension_fields = "\t".join(self.get_extension_field_elements(ext, kl, parent))

        return extension_fields

    @classmethod
    def run(self, file_path, ext, kl_objs, parent=None):

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

            ex_cmd = '{};"'.format(line_number)

            # extension_fields
            extension_fields = self.get_extension_field(ext, kl, parent)

            res.append("{tag_name}\t{file_name}\t{ex_cmd}\t{extension_fields}".format(
                tag_name=tag_name,
                file_name=where,
                ex_cmd=ex_cmd,
                extension_fields=extension_fields
            ))

        return res


class InterfacesParser(KLObjectCTagsParser):
    file_scope = "i"
    identifier = "interface"


class StructParser(KLObjectCTagsParser):
    file_scope = "s"
    identifier = "struct"

    @classmethod
    def run(self, file_path, ext, kl_objs):
        res = super(StructParser, self).run(file_path, ext, kl_objs)
        res.extend(self.get_members(kl_objs))
        return res


class ObjectParser(KLObjectCTagsParser):
    file_scope = "o"
    identifier = "object"

    @classmethod
    def run(self, file_path, ext, kl_objs):
        res = super(ObjectParser, self).run(file_path, ext, kl_objs)
        res.extend(self.get_members(kl_objs))
        return res


class FunctionParser(KLObjectCTagsParser):
    """ free function """

    file_scope = "f"
    identifier = "function"


class MethodParser(KLObjectCTagsParser):
    file_scope = "m"
    identifier = "function"

    @classmethod
    def get_extension_field_elements(self, ext, kl, parent=None):
        file_scope = "kind:{}".format(self.file_scope)
        access = "access:public"
        namespace = "namespace:{}".format(ext)
        if parent and "KLObject" in str(type(parent)):
            parent_type = "object"
        elif parent and "KLObject" in str(type(parent)):
            parent_type = "struct"
        else:
            parent_type = "class"
        klass = "{}:{}".format(parent_type, kl.getThisType())

        return [file_scope, access, namespace, klass]


class MemberParser(KLObjectCTagsParser):
    file_scope = "v"
    identifier = ""

    @classmethod
    def get_exp_for_pattern(self, tag_name):
        return r"[\d\w]+[\s\t]+{}([^\w\d]+=|;)".format(tag_name)

    @classmethod
    def get_extension_field_elements(self, ext, kl, parent=None):
        file_scope = "kind:{}".format(self.file_scope)
        access = "access:public"
        namespace = "namespace:{}".format(ext)
        if parent and "KLObject" in str(type(parent)):
            parent_type = "object"
        elif parent and "KLObject" in str(type(parent)):
            parent_type = "struct"
        else:
            parent_type = "class"
        klass = "{}:{}".format(parent_type, parent.getName())

        return [file_scope, access, namespace, klass]


class OperatorParser(KLObjectCTagsParser):
    file_scope = "p"
    identifier = "operator"


##############################################################################


def header():
    h = textwrap.dedent("""
        !_TAG_FILE_ENCODING	UTF-8	//
        !_TAG_FILE_FORMAT	2	/extended format; --format=1 will not append ;" to lines/
        !_TAG_FILE_SORTED	0	/0=unsorted, 1=sorted, 2=foldcase/
    """).lstrip()

    return h


def parse_file(kl_file):
    """ return lines included a file.

    Sample:
        UpdatePose	D:\fabric\Exts\Solvers\SpringStrandSolver.kl	337;"	kind:m	access:public	namespace:None	object:SpringStrand
        OffsetByCentroid	D:\fabric\Exts\Solvers\SpringStrandSolver.kl	358;"	kind:m	access:public	namespace:None	object:SpringStrand
        pinnedOnController	D:\fabric\Exts\Solvers\SpringStrandSolver.kl	297;"	kind:m	access:public	namespace:None	object:SpringStrand
        max_iteration	D:\fabric\Exts\Solvers\SpringStrandSolver.kl	27;"	kind:v	access:public	namespace:None	object:SpringStrand
        subBaseIndex	D:\fabric\Exts\Solvers\SpringStrandSolver.kl	14;"	kind:v	access:public	namespace:None	object:SpringStrand
        name	D:\fabric\Exts\Solvers\SpringStrandSolver.kl	10;"	kind:v	access:public	namespace:None	object:SpringStrand
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

    # KLFile.getFreeOperators is not exists by default. see readme.md
    try:
        operators = kl_file.getFreeOperators(includeInternal=True)
    except AttributeError:
        operators = None

    res = []
    res.extend(StructParser.run(filepath, ext_name, structs))
    res.extend(ObjectParser.run(filepath, ext_name, objects))
    res.extend(InterfacesParser.run(filepath, ext_name, interfaces))
    res.extend(FunctionParser.run(filepath, ext_name, funcs))
    if operators:
        res.extend(OperatorParser.run(filepath, ext_name, operators))

    return res


##############################################################################
#
##############################################################################
def generate_for_builtins(output):
    ''' generate tags for builtin extensions. '''

    res = []
    man = KLManager()

    for f in man.getKLFiles():
        res.extend(parse_file(f))

    res = list(set(res))
    output.write("\n".join(res).lstrip())


def generate_for_custom_exts(output):
    ''' genarte for '''

    paths = os.environ['FABRIC_EXTS_PATH'].split(os.pathsep)[1:]

    res = []
    man = KLManager(paths=paths)

    # for ex in man.getKLExtensions():
    #    print ex.getName()

    for f in man.getKLFiles():
        res.extend(parse_file(f))

    res = list(set(res))
    output.write("\n".join(res).lstrip())


def generate_for_one_file(input_path, output):
    output.write(header())

    res = []

    from FabricEngine.Sphinx.ASTWrapper.KLFileImpl import KLFile
    f = KLFile(input_path)
    res.extend(parse_file(f))

    res = list(set(res))
    # sys.stdout = sys.__stdout__
    output.write("\n".join(res).lstrip())


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
    help='''generate tags for user exts,
    inculded under "os.environ['FABRIC_EXTS_PATH'].split(os.pathsep)[1:]"
    ''',
)

parser.add_argument(
    '-f', '--file',
    nargs='?',
    type=argparse.FileType('r'),
    help='a input kl file to generate'
)

parser.add_argument(
    '-o', '--output',
    nargs='?',
    type=argparse.FileType('w'),
    help='''output tags file name.
        if not supplyed and enabled -b, using kl.builtin.ctags as default
        if not supplyed and enabled -c, using kl.user.ctags as default
        if not supplyed and enabled -f, using stdout as default output
    '''
)
##############################################################################

if __name__ == '__main__':
    args = parser.parse_args()

    if args.output:
        output = args.output
    else:
        output = sys.stdout

    if args.builtin:
        if not output:
            with open("kl.builtin.ctags") as f:
                generate_for_builtins(f)
        else:
            generate_for_builtins(output)

    if args.custom:
        if not output:
            with open("kl.user.ctags") as f:
                generate_for_custom_exts(f)
        else:
            generate_for_custom_exts(output)

    if args.file:
        input = args.file.name

        generate_for_one_file(input, output)
