# Protocol for Qualitative Analysis of Test Technical Debt Discussions in Pull Requests

Version: 1.0

---

# 1. Purpose

This protocol defines the qualitative analysis procedure used to identify and classify discussions related to **Test Technical Debt (Test TD)** in Pull Requests (PRs).

Its primary objective is to provide a standardized decision-making process that enables a Large Language Model (LLM) to perform classifications consistently, transparently, and reproducibly.

The protocol was designed to minimize subjective interpretations by establishing explicit decision rules, classification criteria, positive examples, negative examples, ambiguous scenarios, and evidence requirements.

Every classification produced by the LLM must be directly supported by the information contained in the Pull Request discussion.

No external knowledge may be used.

---

# 2. Scope

This protocol applies to Pull Requests from open-source software repositories.

The analysis is performed **at the Pull Request level**, not at the individual review thread level.

Each Pull Request must receive exactly one classification for every variable defined in the analysis schema.

The objective is not to evaluate code quality itself, but rather to analyze the discussion between contributors and reviewers regarding improvements to the software tests.

Consequently, classifications must always reflect what was discussed, not what actually exists in the source code.

For example:

- if a PR contains poor tests but nobody comments about them, Test Technical Debt is considered **not discussed**.

Likewise,

- if reviewers discuss improving the tests, Test Technical Debt is considered discussed, regardless of whether the implementation is eventually changed.

---

# 3. Analysis Inputs

The LLM will receive the following information for each Pull Request.

## Pull Request metadata

- Repository name
- Pull Request number
- Pull Request title
- Pull Request description

## Discussion

The complete discussion associated with the Pull Request, including:

- review comments;
- review threads;
- replies from reviewers;
- replies from contributors;
- maintainer comments.

Every comment must be considered part of the discussion.

No distinction should be made between comments written by authors, reviewers, or maintainers.

---

## SonarQube Rules

The LLM will also receive the list of SonarQube rules associated with that Pull Request.

These rules are provided solely to determine whether they were discussed during the review.

The model **must never infer additional SonarQube rules** that are not present in the provided list.

---

# 4. General Decision Rules

The following rules apply to every classification produced by the LLM.

Failure to follow these rules invalidates the analysis.

---

## Rule 1 — Evidence-based Classification

Every classification that concerns the review discussion must be supported by one or more review comments.

Variables that are explicitly defined to use Pull Request metadata may also use the title and description according to their classification rules.

The absence of review comments must not be treated as evidence for Test Technical Debt.

A classification without textual evidence should never be produced.

---

## Rule 2 — Discussion over Code

The analysis concerns **what reviewers discuss**, not the actual quality of the source code.

The LLM must never inspect the code mentally or infer problems that reviewers never mention.

Correct:

> "The reviewer requested additional unit tests."

Incorrect:

> "The implementation probably needs more tests."

The second statement is an unsupported inference.

---

## Rule 3 — No External Knowledge

The LLM must ignore:

- previous knowledge about the project;
- previous knowledge about the repository;
- common programming practices;
- assumptions regarding software quality.

Only the information explicitly contained in the Pull Request may be used.

---

## Rule 4 — Evidence-Based Classification with Minimal Use of UNKNOWN

UNKNOWN must be used only as a last resort.

The LLM must actively evaluate all available evidence in the Pull Request discussion before assigning UNKNOWN.

The absence of an exact keyword, phrase, or explicit statement is not, by itself, sufficient reason to assign UNKNOWN.

When the discussion provides sufficient contextual evidence to support a reasonable classification, the LLM must classify the case, including when the classification requires a justified implicit interpretation.

The LLM must distinguish between:

evidence-based interpretation, which is allowed and should be used when supported by the discussion; and
unsupported speculation, which is prohibited.

UNKNOWN should be assigned only when:

the relevant information cannot reasonably be determined from the Pull Request discussion;
no available category can reasonably represent the evidence; and
selecting another value would require unsupported speculation.

The objective is to maximize evidence-supported classifications while avoiding unsupported guesses.

Before assigning UNKNOWN, the LLM must ask:

"Is there enough evidence in the discussion to reasonably select one of the available categories?"

If YES → select the most appropriate category.

If NO → use UNKNOWN.

---

## Rule 5 — Evidence Priority

Explicit evidence always has priority over inferred evidence.

If reviewers explicitly state something, their statement overrides any possible interpretation.

For example,

Reviewer:

> "This test should be refactored."

The discussion is explicitly about improving the tests.

No further interpretation is necessary.

---

## Rule 6 — Multiple Comments

If multiple comments contribute to the same classification, all relevant comments should be included as evidence.

The LLM must not select only the first comment if subsequent comments clarify the discussion.

---

## Rule 7 — Final State

When determining Agreement or Resolution, the LLM should consider the entire discussion.

Early comments may be contradicted later.

The final outcome of the Pull Request always takes precedence.

---

# 5. Definition of Test Technical Debt

For this study, Test Technical Debt (Test TD) refers to deficiencies in the **test code** that reduce its quality, maintainability, readability, effectiveness, robustness, or long-term evolution.

The discussion must concern the quality of the tests themselves.

The focus is **not** whether production code is correct.

Instead, the focus is whether reviewers identify shortcomings in the existing tests or suggest improvements to the testing artifacts.

Test Technical Debt may involve:

- missing tests;
- incomplete tests;
- weak assertions;
- duplicated tests;
- fragile tests;
- flaky tests;
- excessive mocking;
- difficult maintenance;
- poor readability;
- low coverage;
- missing edge cases;
- incorrect setup or teardown;
- test refactoring;
- improving test organization;
- simplifying complex tests;
- improving test reliability.

In all these situations, the discussion concerns the quality of the test suite rather than the implementation under test.

---

# 6. Fundamental Principle

A discussion should be classified as Test Technical Debt **only if the requested improvement is directed at the test code itself.**

The following question should always be asked before classifying a discussion as Test TD.

> Is the reviewer asking for an improvement to the quality, completeness, maintainability, readability, reliability, or effectiveness of the tests?

If the answer is **YES**, the discussion involves Test Technical Debt.

If the answer is **NO**, the discussion does not involve Test Technical Debt.

This principle takes precedence over every specific example presented later in this protocol.

Whenever uncertainty exists, the LLM should first apply this principle before considering any specific classification category.

---

# 7. Identifying Test Technical Debt

Correctly identifying discussions about Test Technical Debt (Test TD) is the most important task performed by the LLM.

A discussion should only be classified as Test Technical Debt when reviewers identify deficiencies in the **test code** or request improvements that increase the quality, maintainability, completeness, robustness, or effectiveness of the test suite.

The discussion does **not** need to explicitly mention the term "Technical Debt."

Instead, the LLM must determine whether the requested change aims to improve the tests themselves.

---

# 7.1 What SHOULD be considered Test Technical Debt

The following situations must be classified as Test Technical Debt.

## Missing Tests

The reviewer requests tests that do not currently exist.

Examples:

> Please add a unit test.

> This change needs an integration test.

> We should have a regression test for this bug.

> Add tests covering this new functionality.

Reason:

The discussion requests increasing the completeness of the test suite.

---

## Missing Scenarios

Existing tests are considered insufficient.

Examples:

> We should also test invalid inputs.

> Please include boundary cases.

> This edge case is missing.

> Can we add a negative test?

Reason:

The reviewer identifies incomplete testing.

---

## Weak Assertions

The reviewer requests stronger validation.

Examples:

> The test should verify the returned value.

> We should assert the exception message.

> Please verify every field.

> The assertion is too weak.

Reason:

The discussion aims to improve test effectiveness.

---

## Fragile Tests

The reviewer identifies tests that are unstable or easily broken.

Examples:

> This test is fragile.

> This test is easily broken when the implementation changes.

> This test is sensitive to changes in the implementation.



Reason:

The discussion concerns test reliability.

---

## Duplicate Tests

Examples:

> This test duplicates another one.

> These two tests verify exactly the same behavior.

Reason:

The discussion concerns maintainability.

---

## Test Refactoring

Examples:

> This test should be refactored.

> Please simplify this test.

> Split this test into smaller ones.

> The setup is too complicated.

Reason:

The reviewer proposes improving maintainability.

---

## Poor Test Readability

Examples:

> Rename this test.

> The test is difficult to understand.

> The structure is confusing.

> Please improve readability.

Reason:

The discussion concerns maintainability.

---

## Excessive Complexity

Examples:

> This test is doing too much.

> Break this into independent tests.

> The setup is overly complex.

Reason:

The reviewer requests simpler tests.

---

## Poor Test Isolation

Examples:

> This test depends on another test.

> Tests should be independent.

> Avoid shared state.

Reason:

The discussion concerns robustness.

---

## Excessive Mocking

Examples:

> Too many mocks are being used.

> This mock is unnecessary.

> The mocking strategy is making the test difficult to maintain.

Reason:

The discussion concerns maintainability.

---

## Test Organization

Examples:

> Move this test to another class.

> These tests belong together.

> Reorganize the test suite.

Reason:

The reviewer discusses improving test structure.

---

## Regression Tests

Examples:

> Please add a regression test.

> This bug should have a dedicated regression test.

Reason:

Regression tests improve long-term quality.

---

## Test Coverage

Examples:

> Coverage is too low.

> More scenarios should be tested.

> We are not testing this branch.

Reason:

The discussion concerns test completeness.

---

# 7.2 What should NOT be considered Test Technical Debt

The following situations must NEVER be classified as Test Technical Debt.

---

## Production Code Problems

Examples:

> This implementation is wrong.

> The algorithm is incorrect.

> The logic contains a bug.

Reason:

The discussion concerns production code.

---

## Production Refactoring

Examples:

> Move this method.

> Rename this variable.

> Extract a helper class.

Reason:

The discussion concerns implementation.

---

## Performance Improvements

Examples:

> This implementation is slow.

> The algorithm can be optimized.

Reason:

Performance improvements are unrelated to test quality.

---

## Documentation

Examples:

> Update the README.

> Improve documentation.

Reason:

Documentation is not test code.

---

## Formatting

Examples:

> Fix indentation.

> Remove trailing spaces.

Reason:

Formatting does not affect test quality.

---

## CI or Build Problems

Examples:

> CI is failing.

> Jenkins failed.

> GitHub Actions failed.

Reason:

Infrastructure issues are not Test Technical Debt.

---

## Production Code Breaking Existing Tests

Examples:

> This implementation breaks the current tests.

> Update the tests after fixing the implementation.

Reason:

The problem lies in production code.

The tests are correctly detecting a defect.

This situation **must not** be classified as Test Technical Debt.

---

## Failing Tests Without Quality Discussion

Examples:

> One test is failing.

> The tests are currently red.

Reason:

A failing test does not imply poor test quality.

The reviewer must explicitly discuss improving the tests themselves.

---

## Static Analysis Warnings in Test Code

Examples:

> SpotBugs reports a warning.

> SonarQube flags this line.

> PMD reports an issue.

> Checkstyle complains about this statement.

> This violates a static analysis rule.

Reason:

The mere existence of a static analysis warning in test code does not imply Test Technical Debt.

Only classify the discussion as Test Technical Debt if the reviewer explicitly requests improving the quality, maintainability, readability, robustness, completeness, or effectiveness of the tests themselves.

If the discussion is limited to satisfying a static analysis tool, fixing a warning, or complying with a coding rule, Test Technical Debt = NO unless the reviewer clearly frames the discussion as a test quality improvement.

---

## Removing Tests

Examples:

> Remove this obsolete test.

Reason:

Removing obsolete tests is maintenance.

It is not necessarily evidence of Technical Debt.

Only classify as Test TD if the reviewer explicitly argues that the existing test is problematic and should be improved or refactored.

---

# 7.3 Ambiguous Situations

Some discussions require careful interpretation.

---

### Example 1

> Could you add another assertion?

Classification:

✅ Test Technical Debt

Reason:

The reviewer requests improving the effectiveness of the test.

---

### Example 2

> This bug should have a regression test.

Classification:

✅ Test Technical Debt

Reason:

The reviewer requests improving the test suite.

---

### Example 3

> The implementation causes this test to fail.

Classification:

❌ Not Test Technical Debt

Reason:

The discussion concerns production code.

---

### Example 4

> Update the expected value.

Classification:

Not Test Technical Debt

Reason:

The comment only requests updating the expected value. There is no evidence that the test itself is considered deficient or requires a quality improvement.

---

### Example 5

> This test no longer reflects the expected behavior.

Classification:

Test Technical Debt

Reason:

The reviewer explicitly identifies that the test no longer reflects the expected behavior, indicating that the test is outdated relative to the expected behavior.

Test Technical Debt Type:

OUTDATED_TEST

---

### Example 6

> We should verify one more scenario.

Classification:

✅ Test Technical Debt

Reason:

The reviewer identifies incomplete testing.

---

### Example 7

> Please cover this edge case.

Classification:

✅ Test Technical Debt

Reason:

The reviewer requests increasing test completeness.

---

# 7.4 Decision Flow

Before classifying Test Technical Debt, apply the following reasoning.

1. Is the discussion about the test code?

- No → Test TD = NO.

- Yes → Continue.

2. Is the reviewer requesting an improvement to the tests?

- No → Test TD = NO.

- Yes → Continue.

3. Is there sufficient textual or contextual evidence to reasonably determine whether the discussion concerns Test Technical Debt?

- Yes → Test TD = YES.

- No → Test TD = NO 

The LLM should not use UNKNOWN for Test Technical Debt Mentioned merely because the evidence is implicit or because the discussion is ambiguous.

Test Technical Debt Mentioned should be YES only when the discussion provides evidence that the test code itself is being improved or identified as problematic.

If such evidence is not present, classify Test Technical Debt Mentioned = NO.

The term "Technical Debt" does not need to appear explicitly.

---

# 7.5 Priority Rules

When uncertainty exists, apply the following priorities.

1. Explicit reviewer statements override inferred interpretations.

2. Improvements to test quality always take precedence over implementation details.

3. Discussions exclusively about production code are never Test Technical Debt.

4. A failing test alone is not evidence of Test Technical Debt.

5. Missing, incomplete, fragile, duplicated, difficult-to-maintain, or poorly organized tests are always considered Test Technical Debt when explicitly discussed.

6. UNKNOWN must be used only as a last resort. If the discussion provides sufficient contextual evidence to reasonably select a category, the LLM must make the classification.

7. The absence of explicit terminology does not prevent an implicit classification when the discussion provides sufficient evidence.

8. When Test Technical Debt is clearly present but does not fit any specific predefined category, use OTHER rather than UNKNOWN.

# 8. Classification Guidelines

This section defines the classification criteria for every variable produced by the LLM.

Each variable must be classified independently.

Every classification must be supported by textual evidence extracted from the Pull Request discussion.

The LLM should use the available evidence as completely as possible and should not require explicit wording when the intended classification can be reasonably determined from the discussion.

UNKNOWN is a last-resort value and must not be used merely because the evidence is implicit, indirect, contextual, or lacks an exact keyword.

When the evidence supports a reasonable classification, the LLM must select the most appropriate available value.

When Test Technical Debt is clearly discussed but no specific Test Technical Debt category fits, use OTHER.

---

# 8.1 Primary PR Objective

The Primary PR Objective represents the main maintenance goal addressed by the Pull Request.

The objective should be determined by considering the PR title, description, discussion, and final outcome.

Possible values are:

- BUG
- IMP
- REQ
- NONE

---

## BUG

A Pull Request whose primary objective is to correct an incorrect behavior.

Typical indicators include:

- fixing a defect;
- correcting an exception;
- correcting incorrect output;
- restoring expected behavior.

Examples

> Fix NullPointerException.

> Correct incorrect comparison.

> Prevent crash.

---

## IMP

A Pull Request whose primary objective is improving an existing implementation without introducing new functionality.

Typical indicators include:

- refactoring;
- optimization;
- readability improvements;
- maintainability improvements;
- performance improvements.

Examples

> Refactor cache implementation.

> Improve readability.

> Simplify logic.

---

## REQ

A Pull Request introducing new functionality.

Typical indicators include:

- new feature;
- new API;
- additional capability;
- support for new behavior.

Examples

> Add support for JSON.

> Implement new command.

> Add authentication.

---

## NONE

Use `NONE` when the Pull Request discussion does not provide a sufficient basis to identify a BUG, IMP, or REQ objective.

---

# Decision Rules

If multiple objectives appear in the same PR, classify according to the primary motivation of the Pull Request rather than secondary modifications.

---

# 8.2 Suggestion Type

Suggestion Type describes how the Test Technical Debt improvement is expressed in the discussion.

Possible values:

- EXPLICIT
- IMPLICIT
- NONE

---

## EXPLICIT

The discussion directly identifies or requests an improvement to the tests.

Examples

> Add a unit test.

> This test should be refactored.

> Remove this duplicate test.

> This assertion is weak.

The reviewer directly references the test.

---

## IMPLICIT

The discussion concerns an improvement to the tests, but the test-quality problem or improvement is not stated directly in the terminology used by the classification.

Examples

> Could we also verify this scenario?

> Please cover this edge case.

> This needs to work with another input.

> Add another assertion here.

The LLM must use contextual evidence to determine whether the suggestion concerns Test Technical Debt.

---

## NONE

Use `NONE` when no suggestion is present in the review discussion.

---

# Decision Rules

Suggestion Type must be classified independently from Test Technical Debt Mentioned.

Suggestion Type describes how the proposed change or improvement is expressed in the review discussion.

Use EXPLICIT when the reviewer directly proposes or requests a change, action, modification, addition, removal, refactoring, or other concrete action.

Use IMPLICIT when the reviewer identifies a problem, deficiency, or desired improvement without directly formulating a concrete action.

Use NONE when no suggestion or proposed change is present in the review discussion.

Do not determine Suggestion Type based on whether Test Technical Debt is mentioned.

The presence or absence of Test Technical Debt must not affect the classification of Suggestion Type.

UNKNOWN must not be used for Suggestion Type.

The LLM must determine whether the evidence supports an explicit, implicit, or no-suggestion classification. The absence of an exact keyword or phrase is not sufficient reason to avoid classification.

---

# 8.3 Agreement

Agreement describes whether reviewers and contributors reached consensus regarding the proposed Test Technical Debt improvement.

Possible values:

- AGREED
- REJECTED
- POSTPONED
- IGNORED
- UNKNOWN

---

## AGREED

The participants accepted the proposed improvement.

Typical evidence:

> Good point.

> I'll update it.

> Done.

> Thanks, fixed.

---

## REJECTED

The proposal was explicitly refused.

Examples

> I disagree.

> This is unnecessary.

> We intentionally chose this approach.

---

## POSTPONED

Participants agree the improvement is valid but decide to postpone it.

Examples

> Let's address this in another PR.

> We'll improve this later.

---

## IGNORED

The suggestion receives no meaningful response.

Examples

The reviewer proposes a change, but the discussion ends without acknowledgement.

---

## UNKNOWN

There is insufficient evidence to determine the outcome.

Use `UNKNOWN` only when a suggestion exists but the discussion does not provide enough evidence to determine whether it was agreed, rejected, postponed, or ignored.

---

# Decision Rules

Always consider the final state of the discussion.

Later comments override earlier ones.

Agreement concerns whether the proposed Test Technical Debt improvement was accepted by the participants.

Agreement may be established from comments written by any participant, including reviewers, contributors, authors, or maintainers.

The author does not need to be the person who explicitly agrees with a suggestion.

UNKNOWN should be used only when the discussion contains a proposed improvement but the available evidence does not allow the final agreement state to be determined.

---

# 8.4 Resolution

Resolution describes the final state of the proposed improvement or action discussed in the Pull Request.

Possible values:

- FIXED
- P-FIXED
- UNFIXED
- NONE
- UNKNOWN

---

## FIXED

Use `FIXED` when the proposed improvement or requested change was implemented.

Evidence may include:

- reviewer confirmation that the change was made;
- contributor confirmation that the change was made;
- explicit statements such as "Fixed", "Done", or "Implemented";
- a response confirming that the requested change was addressed;
- an explicit reference to a commit or change that implements the suggestion.

Examples:

> Fixed.

> Done.

> Added the requested tests.

> Updated as requested.

---

## P-FIXED

Use `P-FIXED` when only part of the proposed improvement was implemented.

Examples:

> I added one test but not the remaining scenarios.

> I fixed the first issue, but the second one remains.

---

## UNFIXED

Use `UNFIXED` when the proposed improvement was not implemented.

This includes cases where the suggestion was:

- rejected;
- explicitly declined;
- postponed;
- ignored;
- left unresolved;
- explicitly stated to remain unchanged.

Examples:

> I prefer to keep the current version.

> We won't change this.

> Let's address this later.

> This will not be changed in this PR.

If a suggestion is explicitly rejected, postponed, ignored, or left unresolved, classify Resolution as `UNFIXED` rather than `UNKNOWN`.

---

## NONE

Use `NONE` when there is no suggestion, proposed improvement, or action whose implementation needs to be classified.

If `Suggestion Type = NONE`, Resolution MUST be `NONE`.

---

## UNKNOWN

Use `UNKNOWN` only as an absolute last resort.

`UNKNOWN` is appropriate only when:

1. a suggestion or proposed improvement clearly exists;
2. the suggestion is not clearly rejected, postponed, ignored, or left unresolved;
3. there is no evidence that it was implemented;
4. there is no evidence that it was partially implemented; and
5. the available discussion genuinely does not allow determining whether the suggestion was implemented.

Do NOT use `UNKNOWN` merely because:

- the reviewer did not explicitly say "fixed";
- the contributor did not explicitly say "done";
- there is no final comment explicitly confirming completion;
- the discussion is short;
- the suggestion was accepted but the implementation is not described in the exact same words as the suggestion.

When the available evidence supports a reasonable classification as `FIXED`, `P-FIXED`, `UNFIXED`, or `NONE`, use that classification instead of `UNKNOWN`.

---

# Decision Rules

Agreement and Resolution are different concepts.

Agreement indicates whether participants accepted the proposed improvement.

Resolution indicates the final implementation state of the proposed improvement.

A suggestion may be `AGREED` without being implemented in the current Pull Request.

A suggestion may also be implemented even when the discussion does not contain an explicit statement such as "Fixed", provided that the discussion contains sufficient evidence that the requested change was addressed.

Use evidence from the entire review discussion, including reviewer comments, contributor responses, maintainer comments, and explicit references to completed changes or commits.

Decision order:

1. If `Suggestion Type = NONE` → `Resolution = NONE`.
2. If the suggestion was explicitly rejected, declined, postponed, ignored, or left unresolved → `Resolution = UNFIXED`.
3. If the suggestion was fully implemented → `Resolution = FIXED`.
4. If the suggestion was partially implemented → `Resolution = P-FIXED`.
5. Use `UNKNOWN` only if none of the previous rules can determine the resolution.

The absence of an explicit "fixed" statement is NOT sufficient reason to classify Resolution as `UNKNOWN`.

---

# 8.5 Test Technical Debt Mentioned

Determines whether the Pull Request discussion contains Test Technical Debt.

Possible values

- YES
- NO

---

## YES

At least one discussion requests improving the quality, completeness, maintainability, robustness, readability or effectiveness of the tests.

---

## NO

No discussion concerns improving the tests.

Comments about production code, CI, documentation or implementation do not count.

---

# Decision Rules

YES must be assigned when the discussion provides evidence that the quality, completeness, maintainability, robustness, readability, organization, assertions, coverage, reliability, or effectiveness of the test code itself is being improved or discussed as a problem.

NO must be assigned when the discussion does not concern an improvement or problem in the test code itself.

A test may be mentioned without Test Technical Debt being present.

For example:

The implementation breaks the existing test.

This is NO because the discussion concerns a production-code problem rather than a deficiency in the test.

The term "Technical Debt" does not need to appear in the discussion.

A reasonable evidence-based implicit interpretation is allowed.

Test Technical Debt Mentioned must be classified as YES when the discussion provides evidence that the test code itself is being improved or identified as problematic.

Otherwise, classify it as NO.

UNKNOWN should not be used for Test Technical Debt Mentioned.

---

# 8.6 Mention Type

Mention Type describes whether the Test Technical Debt discussion is explicit or implicit.

Possible values:

- EXPLICIT
- IMPLICIT
- NOT_APPLICABLE

## EXPLICIT

The discussion directly identifies the test-related problem or explicitly requests an improvement to the tests.

Examples:

> Add tests.

> Improve this test.

> This assertion is weak.

> This test is difficult to maintain.

## IMPLICIT

The discussion does not directly describe the issue using explicit Test Technical Debt terminology, but the available contextual evidence clearly indicates a Test Technical Debt issue.

Examples:

> Cover this edge case.

> Verify this scenario.

> This needs another test.

The LLM may use contextual interpretation when the evidence supports it.

## NOT_APPLICABLE

Use when:

- Test Technical Debt Mentioned = NO.

There is no Test Technical Debt discussion whose form of mention needs to be classified.

## Decision Rules

If Test Technical Debt Mentioned = YES, Mention Type must be either EXPLICIT or IMPLICIT.

UNKNOWN must never be used for Mention Type.

If Test Technical Debt Mentioned = NO, Mention Type must be NOT_APPLICABLE.

The LLM must determine whether the discussion is explicit or implicit based on the available evidence.

The absence of an exact keyword is not sufficient reason to use UNKNOWN.

---

# 8.7 Test Technical Debt Type

Test Technical Debt Type identifies the primary type of Test Technical Debt discussed in the Pull Request.

Exactly one category must be selected.

When multiple types are discussed, select the category that best represents the primary problem or improvement requested by the discussion.

Possible values:

- FRAGILE_TEST
- HARD_TO_MAINTAIN_TEST
- LOW_COVERAGE
- MISSING_TEST
- BROKEN_TEST
- SLOW_TEST
- ENVIRONMENT_DEPENDENCY
- OUTDATED_TEST
- TEST_DESIGN
- TEST_DATA
- WEAK_INSUFFICIENT_ASSERTION
- UNNECESSARY_REDUNDANT_TEST_CODE
- FLAKY_TEST
- TEST_COMPATIBILITY
- TEST_STABILITY
- TEST_CLEANUP
- OTHER
- NOT_APPLICABLE

## FRAGILE_TEST

Use when the test is fragile, unstable, or easily broken by changes or conditions.

## HARD_TO_MAINTAIN_TEST

Use when the test is difficult to maintain, overly complex, difficult to understand, or contains excessive duplication that makes maintenance difficult.

## LOW_COVERAGE

Use when test coverage is insufficient or additional coverage is needed.

## MISSING_TEST

Use when functionality or existing code lacks an appropriate test and the discussion identifies or requests the missing test.

## BROKEN_TEST

Use when a test is failing or broken and the test itself is identified as the problem that needs to be corrected.

Do not use this category merely because production-code changes cause valid tests to fail.

## SLOW_TEST

Use when a test is excessively slow or its execution time is explicitly identified as a problem.

## ENVIRONMENT_DEPENDENCY

Use when the test depends on external environment configuration or conditions, such as locale, operating-system configuration, environment variables, external services, or similar conditions.

## OUTDATED_TEST

Use when the test is outdated relative to the current implementation or expected behavior and needs to be updated.

## TEST_DESIGN

Use when the problem concerns the structure, organization, architecture, or design of the test itself.

## TEST_DATA

Use when the problem concerns test data, fixtures, mocks, input data, expected data, or other data used by the test.

## WEAK_INSUFFICIENT_ASSERTION

Use when assertions are weak, incomplete, or insufficient to adequately validate the expected behavior.

## UNNECESSARY_REDUNDANT_TEST_CODE

Use when test code contains unnecessary, redundant, unused, or duplicated elements that should be removed or cleaned up.

## FLAKY_TEST

Use when the test exhibits non-deterministic behavior and may pass or fail depending on timing, concurrency, execution order, garbage collection, or similar conditions.

## TEST_COMPATIBILITY

Use when the problem concerns compatibility of tests with changes in programming-language versions, platforms, frameworks, libraries, or other version-related environments.

## TEST_STABILITY

Use when external conditions make the test result unreliable or inconsistent, when the problem is specifically about test stability/reliability and does not more specifically fit FLAKY_TEST or ENVIRONMENT_DEPENDENCY.

## TEST_CLEANUP

Use when the discussion requests removal or cleanup of unnecessary, obsolete, or unused elements in test code without directly changing the test's logic or coverage.

## OTHER

Use when Test Technical Debt is clearly present but none of the predefined categories adequately represents the primary problem.

OTHER should be preferred over forcing an incorrect predefined category.

## NOT_APPLICABLE

Use when:

- Test Technical Debt Mentioned = NO

There is no Test Technical Debt type to classify.

## Decision Rules

If Test Technical Debt Mentioned = YES, Test Technical Debt Type must be one of the predefined categories or OTHER.

UNKNOWN must never be used for Test Technical Debt Type.

If Test Technical Debt Mentioned = NO, Test Technical Debt Type must be NOT_APPLICABLE.

When several categories apply, select the category representing the primary Test Technical Debt discussed.

# 9. SonarQube Rule Analysis

Besides classifying the Pull Request according to the predefined variables, the LLM must determine whether the SonarQube rules associated with the Pull Request were discussed during the review.

The purpose of this analysis is **not** to identify new SonarQube violations, but only to verify whether reviewers explicitly or implicitly discussed the issues represented by the rules already provided.

The model must never infer or invent additional SonarQube rules.

Only the rules supplied as input may be analyzed.

---

## 9.1 Objective

For each SonarQube rule received as input, determine whether the discussion:

- explicitly mentions the issue represented by the rule;
- implicitly discusses the same issue;
- does not discuss the issue.

Each rule must be analyzed independently.

---

## 9.2 Mentioned = TRUE

A rule is considered discussed when at least one review comment addresses the software quality issue represented by that rule.

The reviewer does not need to reference the rule identifier.

For example, if the provided rule is

```
java:S106
```

and a reviewer says

> Printing directly to the console is discouraged.

the rule should be considered discussed even though "S106" never appears.

---

## 9.3 Mentioned = FALSE

A rule should be marked as not discussed when no comment addresses the quality issue represented by that rule.

The mere existence of the violation does not imply discussion.

If a rule is classified as not discussed:

- mentioned = FALSE
- mention_type = NOT_APPLICABLE
- evidence = []

Do not populate the evidence field with unrelated review comments.
---

## 9.4 SonarQube Relationship

For each SonarQube issue provided for the Pull Request, determine the relationship between the issue identified by SonarQube and the Test Technical Debt discussed in the Pull Request review.

The relationship must be classified independently for each SonarQube issue.

Possible values:

- SAME
- COMPLEMENTARY
- DIFFERENT
- NOT_DISCUSSED

### SAME

Use `SAME` when the Test Technical Debt discussed in the review represents essentially the same problem identified by the SonarQube issue.

The discussion does not need to mention the SonarQube rule, rule identifier, or exact SonarQube wording.

The classification should be based on whether the underlying test-related problem is substantially the same.

Example:

SonarQube:
> Tests should contain assertions.

Review:
> This test only executes the method. Please add an assertion to verify the returned value.

Classification:

- mentioned = TRUE
- mention_type = IMPLICIT
- relationship = SAME

### COMPLEMENTARY

Use `COMPLEMENTARY` when the review discussion identifies a Test Technical Debt issue that is related to the SonarQube issue but addresses an additional or complementary aspect of the test quality problem.

The issues should be related, but they should not represent exactly the same problem.

Example:

SonarQube:
> Tests should contain assertions.

Review:
> Add an assertion for the returned value and also cover the case where the value is null.

The assertion issue corresponds to the SonarQube issue, while the additional scenario represents a complementary testing concern.

Use `COMPLEMENTARY` only when the discussion provides evidence of an additional or related concern beyond the SonarQube issue.

### DIFFERENT

Use `DIFFERENT` when the review discussion concerns Test Technical Debt, but the problem is distinct from the problem identified by the SonarQube issue.

Example:

SonarQube:
> Tests should contain assertions.

Review:
> This test is duplicated in several classes. Please refactor the common setup.

The SonarQube issue concerns assertions, while the review discussion concerns redundant or duplicated test code.

Classification:

- mentioned = TRUE
- mention_type = IMPLICIT
- relationship = DIFFERENT

### NOT_DISCUSSED

Use `NOT_DISCUSSED` when the SonarQube issue is not discussed in the Pull Request review.

This means that no review comment provides sufficient evidence that the problem represented by the SonarQube issue was discussed.

When:

- mentioned = FALSE

then:

- mention_type = NOT_APPLICABLE
- relationship = NOT_DISCUSSED

### Decision Rules

1. Compare the underlying problem represented by the SonarQube issue with the problem discussed in the review.

2. Do not classify a rule as `SAME` merely because the general topic is similar.

3. `SAME` requires the underlying Test Technical Debt problem to be substantially the same.

4. Use `COMPLEMENTARY` when the review identifies a related problem that adds another aspect of Test Technical Debt.

5. Use `DIFFERENT` when the review discusses Test Technical Debt but the underlying problem differs from the SonarQube issue.

6. Use `NOT_DISCUSSED` when there is no sufficient evidence that the SonarQube issue was discussed.

7. The SonarQube rule identifier does not need to appear in the review discussion.

8. The LLM must compare the SonarQube issue's rule, message, type, and relevant context with the review discussion.

9. Do not assume that a SonarQube issue was discussed merely because it exists in the Pull Request.

10. Do not assume that a review comment concerns a SonarQube issue merely because both concern tests.

11. When multiple review comments discuss the same Test Technical Debt issue, consider the complete discussion before determining the relationship.

12. The relationship must describe the relationship between the specific SonarQube issue and the Test Technical Debt discussed in the review, not the overall quality of the Pull Request.

13. If the review directly addresses the same underlying problem identified by the SonarQube issue, classify the relationship as SAME even if the discussion also contains additional testing concerns.

14. Use COMPLEMENTARY only when the discussion identifies an additional Test Technical Debt concern that is related to, but distinct from, the SonarQube issue.

### Consistency Rules

If:

`mentioned = FALSE`

then:

`mention_type = NOT_APPLICABLE`

and:

`relationship = NOT_DISCUSSED`.

If:

`mentioned = TRUE`

then:

`mention_type` must be either `EXPLICIT` or `IMPLICIT`.

If:

`mentioned = TRUE`

then:

`relationship` must be one of:

- `SAME`
- `COMPLEMENTARY`
- `DIFFERENT`

`NOT_DISCUSSED` must not be used when `mentioned = TRUE`.

---

## 9.5 Explicit Mention

An explicit mention occurs when reviewers clearly describe the quality issue represented by the rule.

Examples

> Remove this duplicated code.

> Avoid printing to the console.

> This method is too complex.

> This string literal should be extracted into a constant.

---

## 9.6 Implicit Mention

An implicit mention occurs when reviewers discuss the same quality problem without directly describing the SonarQube recommendation.

Example

Rule:

```
java:S3776
```

Reviewer:

> This method is becoming difficult to understand.

Although Cognitive Complexity is never mentioned, the discussion concerns the same issue.

---

## 9.7 SonarQube Relationship and Mention Type — No Discussion

When a SonarQube issue is not discussed in the Pull Request review:

- `mentioned = FALSE`
- `mention_type = NOT_APPLICABLE`
- `relationship = NOT_DISCUSSED`

`NOT_APPLICABLE` must be used for `mention_type` because there is no discussion whose form of mention can be classified.

`NOT_DISCUSSED` must be used for `relationship` because there is no evidence that the specific SonarQube issue was discussed.

`UNKNOWN` must not be used for `mention_type` in this situation.

If the SonarQube issue is discussed, then:

- `mentioned = TRUE`
- `mention_type = EXPLICIT` or `IMPLICIT`
- `relationship = SAME`, `COMPLEMENTARY`, or `DIFFERENT`

`UNKNOWN` must not be used for SonarQube `mention_type` or `relationship`.

---

# 10. Evidence Selection

Every classification produced by the LLM must be supported by textual evidence extracted from the Pull Request discussion.

Evidence serves two purposes:

- making the decision explainable;
- allowing manual verification.

---

## 10.1 Selecting Evidence

The selected comments should directly justify the assigned classification.

Whenever possible, choose the shortest comments that completely support the decision.

---

## 10.2 Multiple Evidence Items

Some classifications require multiple comments.

Example

Reviewer A proposes adding tests.

Developer agrees.

Reviewer later confirms the update.

All three comments together justify:

Agreement = AGREED

Resolution = FIXED

---

## 10.3 Avoid Redundant Evidence

Do not include comments that merely repeat previous information.

Only comments contributing to the final decision should be selected.

---

## 10.4 No Evidence

The LLM must never fabricate evidence.

Before assigning UNKNOWN, the LLM must consider the complete Pull Request discussion and determine whether sufficient contextual evidence exists to make a reasonable classification.

If sufficient evidence exists, the LLM must classify the case.

UNKNOWN must only be used as a last resort for variables where UNKNOWN is an allowed value.

When a variable has a defined NOT_APPLICABLE value and its condition is satisfied, use NOT_APPLICABLE rather than UNKNOWN.

When Test Technical Debt is clearly present but no predefined Test Technical Debt category fits, use OTHER rather than UNKNOWN.

---

# 11. Frequent Classification Errors

The following mistakes must be avoided.

---

## Error 1

Confusing production code discussions with Test Technical Debt.

Incorrect

> The implementation contains a bug.

↓

Test TD = YES

Correct

Test TD = NO

---

## Error 2

Assuming every discussion involving tests concerns Test Technical Debt.

Incorrect

> The tests are failing.

↓

Test TD = YES

Correct

Test TD = NO

Reason

The discussion concerns execution results rather than improving the tests.

---

## Error 3

Inferring information not present in the Pull Request.

Incorrect

> The implementation probably requires additional tests.

The reviewer never stated this.

---

## Error 4

Ignoring the final discussion outcome.

Later comments always override earlier interpretations.

---

## Error 5

Confusing Agreement with Resolution.

Example

Developer

> Good suggestion.

Agreement = AGREED

However,

if no implementation occurs,

Resolution ≠ FIXED.

---

## Error 6

Selecting evidence unrelated to the assigned classification.

Every evidence item must directly support the corresponding decision.

---

# 12. Final Validation Checklist

Before producing the final JSON, verify the following questions.

---

## General

- Was every decision based exclusively on the Pull Request discussion?

- Was external knowledge avoided?

- Does every classification have supporting evidence?

- Were unsupported assumptions avoided?

---

## Test Technical Debt

- Is the discussion really about the test code?

- Is the requested improvement directed at the tests?

- Is the discussion actually about production code instead?

- Could this be a CI or infrastructure issue?

- Is there sufficient evidence to classify Test Technical Debt?

---

## Classification Variables

- Is the Primary PR Objective supported by the discussion?

- Does Suggestion Type match the evidence?

- Does Agreement reflect the final discussion?

- Does Resolution reflect the final outcome?

- Is Mention Type compatible with Test Technical Debt Mentioned?

- Was only one Test Technical Debt Type selected?

- Was UNKNOWN used only as a last resort?

- If Test Technical Debt = YES, is Mention Type classified as EXPLICIT or IMPLICIT?

- If Test Technical Debt = NO, is Mention Type set to NOT_APPLICABLE and Test Technical Debt Type set to NOT_APPLICABLE?

- Is Suggestion Type classified independently as EXPLICIT, IMPLICIT, or NONE?

- If Test Technical Debt = YES, is Test Technical Debt Type a predefined category or OTHER?

- Was an evidence-based implicit interpretation considered before using UNKNOWN?

- Was UNKNOWN avoided when a reasonable classification was supported by the discussion?

---

## SonarQube Rules

For every rule:

- Was only the provided rule analyzed?

- Is the rule actually discussed?

- Is the assigned mention type supported by the comments?

- Was evidence provided?

---

## Final Principle

The objective of this protocol is to maximize consistency, transparency, reproducibility, and evidence-supported classification.

UNKNOWN is a last-resort value.

Whenever sufficient evidence exists to support a reasonable classification, the LLM must classify the case.

Unsupported speculation is prohibited, but evidence-based implicit interpretation is allowed and should be used when justified.

# Appendix A – Complete Classification Examples

The following examples illustrate how the LLM should apply the protocol in practice.

These examples are normative.

When similar situations are encountered, the reasoning demonstrated below should be preferred.

---

# Example 1 – Missing Test

## Pull Request

Title

> Fix NullPointerException when username is null

Discussion

Reviewer

> Please add a regression test for this scenario.

Developer

> Done. Added a regression test covering null usernames.

---

Classification

Primary PR Objective

BUG

Suggestion Type

EXPLICIT

Agreement

AGREED

Resolution

FIXED

Test Technical Debt Mentioned

YES

Mention Type

EXPLICIT

Test Technical Debt Type

MISSING_TEST

Evidence

Reviewer:
> Please add a regression test for this scenario.

Developer:
> Done. Added a regression test covering null usernames.

---

Reasoning

The reviewer explicitly requests a new test.

The developer agrees and implements the requested improvement.

The discussion concerns improving the quality of the test suite.

---

# Example 2 – Missing Scenario

Discussion

Reviewer

> We should also verify the invalid input case.

Developer

> Good point. I'll add that scenario.

---

Classification

Primary PR Objective

UNKNOWN

Suggestion Type

IMPLICIT

Agreement

AGREED

Resolution

FIXED

Test Technical Debt Mentioned

YES

Mention Type

IMPLICIT

Test Technical Debt Type

LOW_COVERAGE

---

Reasoning

The reviewer requests additional coverage without explicitly discussing test quality.

---

# Example 3 – Weak Assertions

Discussion

Reviewer

> This test only verifies the status code.
>
> It should also verify the returned object.

Developer

> Added assertions.

---

Classification

Test Technical Debt Mentioned

YES

Mention Type

EXPLICIT

Test Technical Debt Type

WEAK_INSUFFICIENT_ASSERTION

---

Reasoning

The reviewer requests stronger assertions to improve test effectiveness.

---

# Example 4 – Test Refactoring

Discussion

Reviewer

> This test is difficult to understand.
>
> Could you split it into smaller tests?

Developer

> Refactored.

---

Classification

Test Technical Debt Mentioned

YES

Mention Type

EXPLICIT

Test Technical Debt Type

HARD_TO_MAINTAIN_TEST

---

Reasoning

The discussion concerns maintainability.

---

# Example 5 – Flaky Test

Discussion

Reviewer

> This test is flaky.
>
> It occasionally fails on CI.

Developer

> I removed the timing dependency.

---

Classification

Test Technical Debt Mentioned

YES

Mention Type

EXPLICIT

Test Technical Debt Type

FLAKY_TEST

---

Reasoning

The reviewer explicitly identifies an unstable test.

---

# Example 6 – UNNECESSARY_REDUNDANT_TEST_CODE

Discussion

Reviewer

> This test duplicates the previous one.

Developer

> Removed the duplicate.

---

Classification

Test Technical Debt Mentioned

YES

Mention Type

EXPLICIT

Test Technical Debt Type

UNNECESSARY_REDUNDANT_TEST_CODE

---

# Example 7 – Production Bug

Discussion

Reviewer

> The implementation is incorrect.

---

Classification

Test Technical Debt Mentioned

NO

Suggestion Type

NONE

Mention Type

NOT_APPLICABLE

Test Technical Debt Type

NOT_APPLICABLE

---

Reasoning

The discussion concerns production code.

---

# Example 8 – Production Code Breaks Tests

Discussion

Reviewer

> This implementation breaks the existing tests.

---

Classification

Test Technical Debt Mentioned

NO

Suggestion Type

NONE

Mention Type

NOT_APPLICABLE

Test Technical Debt Type

NOT_APPLICABLE

---

Reasoning

The tests correctly detect a production defect.

The reviewer is not requesting improvements to the tests.

---

# Example 9 – CI Failure

Discussion

Reviewer

> CI failed again.

---

Classification

Test Technical Debt Mentioned

NO

Suggestion Type

NONE

Mention Type

NOT_APPLICABLE

Test Technical Debt Type

NOT_APPLICABLE

---

Reasoning

Infrastructure issues are not Test Technical Debt.

---

# Example 10 – Unknown

Discussion

Reviewer

> Please update this.

---

Classification

Primary PR Objective
UNKNOWN

Suggestion Type
NONE

Agreement
UNKNOWN

Resolution
UNKNOWN

Test Technical Debt Mentioned
NO

Mention Type
NOT_APPLICABLE

Test Technical Debt Type
NOT_APPLICABLE

---

Reasoning

The comment is too vague to determine the Pull Request objective, agreement, or resolution. There is no evidence that Test Technical Debt is being discussed. Therefore, the Test Technical Debt-related fields are NOT_APPLICABLE.

---

# Appendix B – General Interpretation Principles

The following principles summarize the expected behavior of the LLM.

---

## Principle 1

Always classify what reviewers discuss.

Never classify what probably exists in the code.

---

## Principle 2

A Pull Request may contain Technical Debt without discussing it.

In this case,

Test Technical Debt Mentioned = NO.

---

## Principle 3

A reviewer does not need to use the expression

"Technical Debt"

for the discussion to concern Test Technical Debt.

The requested improvement is what matters.

---

## Principle 4

Discussions about production code are never Test Technical Debt.

Even when tests are mentioned.

---

## Principle 5

A failing test is not automatically evidence of Test Technical Debt.

Ask the following question:

"Is the reviewer asking to improve the test?"

If the answer is no,

Test Technical Debt = NO.

---

## Principle 6

When the discussion requests improving the quality, maintainability, completeness, readability, robustness, organization, assertions, coverage, or reliability of the tests,

Test Technical Debt = YES.

---

## Principle 7

Evidence is mandatory.

Every classification must be traceable to one or more review comments.

---

## Principle 8

UNKNOWN is a last-resort classification.

The LLM should maximize evidence-supported classifications while avoiding unsupported speculation.

The absence of an exact keyword or explicit statement does not automatically justify UNKNOWN.

When the discussion provides sufficient contextual evidence for a reasonable classification, the LLM must classify the case.

UNKNOWN must only be used when the relevant information genuinely cannot be determined from the discussion and no reasonable classification can be supported.

---

# Final Statement

This protocol defines a complete, evidence-based procedure for identifying and classifying discussions about Test Technical Debt in Pull Requests.

The LLM must prioritize evidence-supported classifications while avoiding unsupported speculation.

UNKNOWN must only be used when the available evidence genuinely does not permit a reasonable classification and no applicable alternative value exists.

# Appendix C – Decision Heuristics and Annotation Conventions

The following heuristics summarize recurring annotation patterns identified during the manual analysis of Pull Request discussions.

These conventions complement the previous sections of this protocol and should be applied whenever the corresponding situations occur.

---

# C.1 Pull Requests Without Review Comments

If a Pull Request has no review discussion or review comments:

Primary PR Objective:
Classify according to the available Pull Request information and the rules defined in Section 8.1.

Suggestion Type:
NONE

Agreement:
IGNORED

Resolution:
UNKNOWN

Test Technical Debt Mentioned:
NO

Mention Type:
NOT_APPLICABLE

Test Technical Debt Type:
NOT_APPLICABLE

Reasoning:

Without review comments, there is no review discussion from which a Test Technical Debt suggestion, mention type, or Test Technical Debt type can be identified.

Therefore:

- Suggestion Type = NOT_APPLICABLE
- Mention Type = NOT_APPLICABLE
- Test Technical Debt Type = NOT_APPLICABLE

Agreement = IGNORED because there is no review discussion in which a suggestion could be accepted, rejected, or postponed.

Resolution = UNKNOWN because there is no review discussion from which the resolution of a review suggestion can be determined.

---

# C.2 Simple Approval (LGTM)

Comments such as

> LGTM

> Looks good

> Approved

indicate reviewer approval of the Pull Request.

Classification

Agreement

AGREED

Resolution

UNKNOWN

Test Technical Debt Mentioned

NO

unless additional comments explicitly discuss Test Technical Debt.

Reasoning:

Simple approval comments do not constitute a Test Technical Debt discussion and do not provide evidence that a specific Test Technical Debt suggestion was implemented.

Therefore, when no Test Technical Debt suggestion exists:

- Test Technical Debt Mentioned = NO
- Suggestion Type = NONE
- Mention Type = NOT_APPLICABLE
- Test Technical Debt Type = NOT_APPLICABLE

Resolution should not be classified as FIXED merely because the Pull Request was approved.

---

# C.3 "Done", "Updated", or "Addressed"

When a reviewer requests a modification and the author responds with expressions such as

> Done

> Updated

> Addressed

> Fixed

or references a commit implementing the requested change,

the suggestion should be considered implemented.

Classification

Resolution

FIXED

provided there is no later discussion indicating otherwise.

---

# C.4 Final Discussion Prevails

When multiple comments disagree during the review process,

the final state of the discussion determines the annotation.

Earlier comments should not override the final outcome.

---

# C.5 Test Failures

The mere existence of failing tests does not indicate Test Technical Debt.

Examples

> Tests are failing.

> CI is red.

> Build failed.

These situations only indicate Test Technical Debt if reviewers explicitly discuss improving the tests themselves.

---

# C.6 Production Defects Detected by Tests

Comments indicating that tests correctly detected production defects should not be classified as Test Technical Debt.

Example

> This implementation breaks the existing tests.

The problem concerns production code rather than the quality of the tests.

---

# C.7 Refactoring Test Code

Suggestions requesting improvements such as

- removing duplication;
- improving readability;
- reorganizing helper methods;
- simplifying assertions;
- improving maintainability;

should be classified as discussions about Test Technical Debt whenever they target the test code itself.

---

# C.8 Requests for Additional Test Cases

Suggestions requesting

- new tests;
- regression tests;
- missing scenarios;
- edge cases;
- additional assertions;

should be classified as Test Technical Debt because they aim to improve the completeness or effectiveness of the test suite.

---

# C.9 Flaky or Unstable Tests

# C.9 Flaky Test

Flaky or non-deterministic tests should be classified as `FLAKY_TEST`.

Use `FLAKY_TEST` when the discussion indicates that a test may pass or fail depending on timing, execution order, concurrency, garbage collection, race conditions, or other non-deterministic conditions.

Use `FRAGILE_TEST` when the test is described as fragile or easily broken by changes or conditions, but the discussion does not indicate non-deterministic behavior.

Examples:

- "This test is flaky." → `FLAKY_TEST`
- "This test sometimes passes and sometimes fails." → `FLAKY_TEST`
- "This test fails depending on timing." → `FLAKY_TEST`
- "This test is fragile and breaks whenever this code changes." → `FRAGILE_TEST`

Do not classify every unstable or problematic test as `FLAKY_TEST`. The discussion must provide evidence of non-deterministic behavior for `FLAKY_TEST`.

---

# C.10 UNKNOWN as a Last Resort

UNKNOWN should only be used when the available Pull Request discussion does not provide enough evidence to make a reasonable classification.

The LLM must not assign UNKNOWN merely because:

- the concept is not explicitly named;
- the evidence is implicit;
- the reviewer uses different terminology;
- contextual interpretation is required;
- the exact category name does not appear in the discussion.

If sufficient evidence exists for a reasonable classification, the LLM must classify the case.

For Suggestion Type and Mention Type:

- Test TD = YES → EXPLICIT or IMPLICIT;
- Test TD = NO → NOT_APPLICABLE.

For Test Technical Debt Type:

- Test TD = YES → predefined category or OTHER;
- Test TD = NO → NOT_APPLICABLE.

UNKNOWN is not permitted for these three variables when their conditions above determine the appropriate value.

Evidence-based interpretation is allowed. Unsupported speculation is not.
---

# C.11 Review Discussions Are the Unit of Analysis

This protocol analyzes what reviewers discuss, not what exists in the source code.

Consequently,

a Pull Request may introduce, remove, or contain Test Technical Debt without any discussion about it.

In such cases,

Test Technical Debt Mentioned = NO.

---

# C.12 Evidence Always Prevails

Whenever a heuristic conflicts with explicit evidence found in the discussion,

the evidence must prevail.

These heuristics are intended only to standardize recurring situations and should never override direct textual evidence.