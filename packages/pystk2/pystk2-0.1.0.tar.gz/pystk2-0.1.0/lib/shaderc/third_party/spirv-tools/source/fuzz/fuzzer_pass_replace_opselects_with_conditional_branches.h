// Copyright (c) 2020 Google LLC
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#ifndef SOURCE_FUZZ_FUZZER_PASS_REPLACE_OPSELECTS_WITH_CONDITIONAL_BRANCHES_H_
#define SOURCE_FUZZ_FUZZER_PASS_REPLACE_OPSELECTS_WITH_CONDITIONAL_BRANCHES_H_

#include "source/fuzz/fuzzer_pass.h"

namespace spvtools {
namespace fuzz {

// A fuzzer pass to replace OpSelect instructions (where the condition is a
// scalar boolean) with conditional branches and OpPhi instructions.
class FuzzerPassReplaceOpSelectsWithConditionalBranches : public FuzzerPass {
 public:
  FuzzerPassReplaceOpSelectsWithConditionalBranches(
      opt::IRContext* ir_context, TransformationContext* transformation_context,
      FuzzerContext* fuzzer_context,
      protobufs::TransformationSequence* transformations,
      bool ignore_inapplicable_transformations);

  void Apply() override;

 private:
  // Returns true if any of the following holds:
  // - the instruction is not the first in its block
  // - the block containing it is a merge block
  // - the block does not have a unique predecessor
  // - the predecessor of the block is the header of a construct
  // - the predecessor does not branch unconditionally to the block
  // If this function returns true, the block must be split before the
  // instruction for TransformationReplaceOpSelectWithConditionalBranch to be
  // applicable.
  // Assumes that the instruction is OpSelect.
  bool InstructionNeedsSplitBefore(opt::Instruction* instruction);
};

}  // namespace fuzz
}  // namespace spvtools

#endif  // SOURCE_FUZZ_FUZZER_PASS_REPLACE_OPSELECTS_WITH_CONDITIONAL_BRANCHES_H_
