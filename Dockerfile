# syntax=docker/dockerfile:1
FROM rust:1.98.1-bookworm AS engine
WORKDIR /src
ENV CARGO_BUILD_JOBS=1
COPY Cargo.toml Cargo.lock ./
COPY crates ./crates
RUN cargo build --release --locked -p proofserve

FROM debian:bookworm-slim AS lean
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates curl git zstd python3 build-essential binutils libgmp-dev \
    && rm -rf /var/lib/apt/lists/*
COPY checker/lean-toolchain /opt/checker-toolchain
ENV PATH="/opt/lean/bin:$PATH" LEAN_SYSROOT="/opt/lean"
RUN mkdir -p /opt/lean /opt/repl /opt/mathlib && \
    version="$(sed -n 's#leanprover/lean4:v##p' /opt/checker-toolchain)" && \
    test -n "$version" && \
    curl -fL "https://github.com/leanprover/lean4/releases/download/v$version/lean-$version-linux.tar.zst" \
    | tar --zstd -x --strip-components=1 -C /opt/lean
ARG REPL_REVISION=193cf4bb9a22bb3fc6d25774f0fe6a70db1fd6ee
ARG MATHLIB_REVISION=d13f23b723b8a846827a245b89c10fc7d3f11612
RUN curl -fL "https://codeload.github.com/leanprover-community/repl/tar.gz/$REPL_REVISION" \
    | tar -xz --strip-components=1 -C /opt/repl
# Upstream REPL v4.34.0 is compiled with the exact SDK required by our checker.
COPY checker/lean-toolchain /opt/repl/lean-toolchain
WORKDIR /opt/repl
RUN lake build
RUN curl -fL "https://codeload.github.com/leanprover-community/mathlib4/tar.gz/$MATHLIB_REVISION" \
    | tar -xz --strip-components=1 -C /opt/mathlib
WORKDIR /opt/mathlib
RUN python3 -c "from pathlib import Path; assert Path('lean-toolchain').read_text().strip() == Path('/opt/checker-toolchain').read_text().strip(), 'Mathlib/checker toolchains differ'"
RUN lake exe cache get
COPY checker /opt/checker
WORKDIR /opt/checker
RUN lake build
RUN printf 'lean-%s-mathlib-%s-repl-%s' "$(cat /opt/checker-toolchain)" "$MATHLIB_REVISION" "$REPL_REVISION" > /opt/proofserve-context

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates libgmp10 libstdc++6 python3 git && rm -rf /var/lib/apt/lists/*
COPY --from=lean /opt/lean/ /opt/proofserve/
COPY --from=engine /src/target/release/proofserve /opt/proofserve/bin/proofserve
COPY --from=lean /opt/checker/.lake/build/bin/proofserve-check /opt/proofserve/libexec/proofserve-check
COPY --from=lean /opt/checker-toolchain /opt/proofserve/share/proofserve/lean-toolchain
COPY --from=lean /opt/proofserve-context /opt/proofserve-context
COPY --from=lean /opt/repl /opt/repl
COPY --from=lean /opt/mathlib /opt/mathlib
COPY packaging/proofserve-check /opt/proofserve/bin/proofserve-check
COPY packaging/proofserve-audit /opt/proofserve/bin/proofserve-audit
COPY tools/audit/audit.py /opt/proofserve/libexec/proofserve-audit.py
COPY LICENSE /opt/proofserve/share/proofserve/LICENSE
COPY packaging/start-proofserve /usr/local/bin/start-proofserve
COPY packaging/container_smoke.py /opt/container_smoke.py
COPY clients/python/proofserve /opt/client/proofserve
ENV PATH="/opt/proofserve/bin:$PATH" \
    LEAN_SYSROOT="/opt/proofserve" LD_LIBRARY_PATH="/opt/proofserve/lib/lean" \
    PYTHONPATH="/opt/client"
WORKDIR /opt/mathlib
EXPOSE 3000
ENTRYPOINT ["/bin/sh", "/usr/local/bin/start-proofserve"]
CMD ["--help"]
RUN --network=none python3 /opt/container_smoke.py --self-test
