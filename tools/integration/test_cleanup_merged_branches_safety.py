"""Safety contract tests for the merged-branch cleanup workflow."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WORKFLOW = ROOT / ".github/workflows/cleanup-merged-branches.yml"


def require(condition: bool, message: str, failures: list[str]) -> None:
    if not condition:
        failures.append(message)


def main() -> None:
    source = WORKFLOW.read_text(encoding="utf-8")
    failures: list[str] = []

    require('const protectedNames = new Set(["main"]);' in source,
            "main must be the only permanently protected branch", failures)
    require("reviewedSupersededBranches" not in source,
            "manual SHA exceptions must not be allowed to delete branches", failures)
    require('state: "open"' in source and 'state: "closed"' in source,
            "the workflow must inspect both open and closed pull requests", failures)
    require("activeRefs.add(pr.head.ref)" in source and
            "activeRefs.add(pr.base.ref)" in source and
            "activeRefs.has(name)" in source,
            "branches used by open pull requests must be retained", failures)
    require("!pr.merged_at" in source and 'pr.base.ref !== "main"' in source,
            "only PRs merged into main can qualify by exact merged head", failures)
    require("github.rest.repos.compareCommitsWithBasehead({" in source and
            'basehead: "main..." + name' in source,
            "branch ancestry must use the current Octokit compare endpoint", failures)
    require("comparison.data.ahead_by === 0" in source,
            "a branch may only be deleted after proving it has zero commits ahead of main", failures)
    require('branches.find((branch) => branch.name === "main")' in source and
            "const mainTreeSha = mainCommit.data.tree.sha;" in source,
            "the workflow must obtain the current main Git tree before cleanup", failures)
    require("branchCommit.data.tree.sha === mainTreeSha" in source,
            "a history-diverged branch may be deleted only when its complete Git tree equals main", failures)
    require("Commit-history comparison failed for " in source and
            "unable to verify its Git tree" in source and
            "still contains commits not merged into main" in source,
            "unknown or unmerged branches must be kept with a diagnostic", failures)
    delete_guard = source.rfind("if (!safeToDelete) {")
    delete_call = source.find("github.rest.git.deleteRef({")
    require(delete_guard >= 0 and delete_call > delete_guard,
            "the delete API must remain behind the final safeToDelete guard", failures)
    require("github.rest.git.deleteRef({" in source and
            '"heads/" + name' in source,
            "deletion must target only the explicitly validated branch ref", failures)
    require("github.event.pull_request.merged == true" in source and
            "types:" in source and "- closed" in source,
            "a PR-close trigger must clean branches only after a successful merge", failures)

    if failures:
        raise SystemExit("\n".join(failures))
    print("PASS: branch cleanup protects main/open PRs and deletes only proven-merged branch tips")


if __name__ == "__main__":
    main()
