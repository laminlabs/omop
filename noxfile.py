import nox
from laminci.nox import build_docs, install_lamindb, run_pre_commit, run_pytest

# we'd like to aggregate coverage information across sessions
# and for this the code needs to be located in the same
# directory in every github action runner
# this also allows to break out an installation section
nox.options.default_venv_backend = "none"


@nox.session
def lint(session: nox.Session) -> None:
    run_pre_commit(session)


@nox.session()
def build(session):
    install_lamindb(session, branch="main")
    session.run(*"uv pip install --system .[dev]".split())
    run_pytest(session)
    build_docs(session, strict=True)
