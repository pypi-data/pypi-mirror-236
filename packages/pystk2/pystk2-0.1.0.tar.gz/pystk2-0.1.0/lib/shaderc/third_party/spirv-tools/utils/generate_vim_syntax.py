#!/usr/bin/env python
# Copyright (c) 2016 Google Inc.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Generates Vim syntax rules for SPIR-V assembly (.spvasm) files"""

import json

PREAMBLE="""" Vim syntax file
" Language:   spvasm
" Generated by SPIRV-Tools

if version < 600
  syntax clear
elseif exists("b:current_syntax")
  finish
endif

syn case match
"""

POSTAMBLE="""

syntax keyword spvasmTodo TODO FIXME contained

syn match   spvasmIdNumber /%\d\+\>/

" The assembler treats the leading minus sign as part of the number token.
" This applies to integers, and to floats below.
syn match   spvasmNumber /-\?\<\d\+\>/

" Floating point literals.
" In general, C++ requires at least digit in the mantissa, and the
" floating point is optional.  This applies to both the regular decimal float
" case and the hex float case.

" First case: digits before the optional decimal, no trailing digits.
syn match   spvasmFloat  /-\?\d\+\.\?\(e[+-]\d\+\)\?/
" Second case: optional digits before decimal, trailing digits
syn match   spvasmFloat  /-\?\d*\.\d\+\(e[+-]\d\+\)\?/

" First case: hex digits before the optional decimal, no trailing hex digits.
syn match   spvasmFloat  /-\?0[xX]\\x\+\.\?p[-+]\d\+/
" Second case: optional hex digits before decimal, trailing hex digits
syn match   spvasmFloat  /-\?0[xX]\\x*\.\\x\+p[-+]\d\+/

syn match   spvasmComment /;.*$/ contains=spvasmTodo
syn region  spvasmString start=/"/ skip=/\\\\"/ end=/"/
syn match   spvasmId /%[a-zA-Z_][a-zA-Z_0-9]*/

" Highlight unknown constants and statements as errors
syn match   spvasmError /[a-zA-Z][a-zA-Z_0-9]*/


if version >= 508 || !exists("did_c_syn_inits")
  if version < 508
    let did_c_syn_inits = 1
    command -nargs=+ HiLink hi link <args>
  else
    command -nargs=+ HiLink hi def link <args>
  endif

  HiLink spvasmStatement Statement
  HiLink spvasmNumber Number
  HiLink spvasmComment Comment
  HiLink spvasmString String
  HiLink spvasmFloat Float
  HiLink spvasmConstant Constant
  HiLink spvasmIdNumber Identifier
  HiLink spvasmId Identifier
  HiLink spvasmTodo Todo

  delcommand HiLink
endif

let b:current_syntax = "spvasm"
"""

# This list is taken from the description of OpSpecConstantOp in SPIR-V 1.1.
# TODO(dneto): Propose that this information be embedded in the grammar file.
SPEC_CONSTANT_OP_OPCODES = """
        OpSConvert, OpFConvert
        OpSNegate, OpNot
        OpIAdd, OpISub
        OpIMul, OpUDiv, OpSDiv, OpUMod, OpSRem, OpSMod
        OpShiftRightLogical, OpShiftRightArithmetic, OpShiftLeftLogical
        OpBitwiseOr, OpBitwiseXor, OpBitwiseAnd
        OpVectorShuffle, OpCompositeExtract, OpCompositeInsert
        OpLogicalOr, OpLogicalAnd, OpLogicalNot,
        OpLogicalEqual, OpLogicalNotEqual
        OpSelect
        OpIEqual, OpINotEqual
        OpULessThan, OpSLessThan
        OpUGreaterThan, OpSGreaterThan
        OpULessThanEqual, OpSLessThanEqual
        OpUGreaterThanEqual, OpSGreaterThanEqual

        OpQuantizeToF16

        OpConvertFToS, OpConvertSToF
        OpConvertFToU, OpConvertUToF
        OpUConvert
        OpConvertPtrToU, OpConvertUToPtr
        OpGenericCastToPtr, OpPtrCastToGeneric
        OpBitcast
        OpFNegate
        OpFAdd, OpFSub
        OpFMul, OpFDiv
        OpFRem, OpFMod
        OpAccessChain, OpInBoundsAccessChain
        OpPtrAccessChain, OpInBoundsPtrAccessChain"""


def EmitAsStatement(name):
    """Emits the given name as a statement token"""
    print('syn keyword spvasmStatement', name)


def EmitAsEnumerant(name):
    """Emits the given name as an named operand token"""
    print('syn keyword spvasmConstant', name)


def main():
    """Parses arguments, then generates the Vim syntax rules for SPIR-V assembly
    on stdout."""
    import argparse
    parser = argparse.ArgumentParser(description='Generate SPIR-V info tables')
    parser.add_argument('--spirv-core-grammar', metavar='<path>',
                        type=str, required=True,
                        help='input JSON grammar file for core SPIR-V '
                        'instructions')
    parser.add_argument('--extinst-glsl-grammar', metavar='<path>',
                        type=str, required=False, default=None,
                        help='input JSON grammar file for GLSL extended '
                        'instruction set')
    parser.add_argument('--extinst-opencl-grammar', metavar='<path>',
                        type=str, required=False, default=None,
                        help='input JSON grammar file for OpenGL extended '
                        'instruction set')
    parser.add_argument('--extinst-debuginfo-grammar', metavar='<path>',
                        type=str, required=False, default=None,
                        help='input JSON grammar file for DebugInfo extended '
                        'instruction set')
    args = parser.parse_args()

    # Generate the syntax rules.
    print(PREAMBLE)

    core = json.loads(open(args.spirv_core_grammar).read())
    print('\n" Core instructions')
    for inst in core["instructions"]:
        EmitAsStatement(inst['opname'])
    print('\n" Core operand enums')
    for operand_kind in core["operand_kinds"]:
        if 'enumerants' in operand_kind:
            for e in operand_kind['enumerants']:
                EmitAsEnumerant(e['enumerant'])

    if args.extinst_glsl_grammar is not None:
        print('\n" GLSL.std.450 extended instructions')
        glsl = json.loads(open(args.extinst_glsl_grammar).read())
        # These opcodes are really enumerant operands for the OpExtInst
        # instruction.
        for inst in glsl["instructions"]:
            EmitAsEnumerant(inst['opname'])

    if args.extinst_opencl_grammar is not None:
        print('\n" OpenCL.std extended instructions')
        opencl = json.loads(open(args.extinst_opencl_grammar).read())
        for inst in opencl["instructions"]:
            EmitAsEnumerant(inst['opname'])

    if args.extinst_debuginfo_grammar is not None:
        print('\n" DebugInfo extended instructions')
        debuginfo = json.loads(open(args.extinst_debuginfo_grammar).read())
        for inst in debuginfo["instructions"]:
            EmitAsEnumerant(inst['opname'])
        print('\n" DebugInfo operand enums')
        for operand_kind in debuginfo["operand_kinds"]:
            if 'enumerants' in operand_kind:
                for e in operand_kind['enumerants']:
                    EmitAsEnumerant(e['enumerant'])

    print('\n" OpSpecConstantOp opcodes')
    for word in SPEC_CONSTANT_OP_OPCODES.split(' '):
        stripped = word.strip('\n,')
        if stripped != "":
            # Treat as an enumerant, but without the leading "Op"
            EmitAsEnumerant(stripped[2:])
    print(POSTAMBLE)


if __name__ == '__main__':
    main()
