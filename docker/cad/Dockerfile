ARG PYTHON_IMAGE
FROM ${PYTHON_IMAGE}

ARG SOLIDCRAFT_VERSION
ARG SCPF_URL
ARG SCPF_SHA
ARG SCPC_URL
ARG SCPC_SHA

ENV DEBIAN_FRONTEND=noninteractive \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    SOLIDCRAFT_GPU=cpu \
    SOLIDCRAFT_VERSION=${SOLIDCRAFT_VERSION} \
    SCPF_COMMIT=${SCPF_SHA} \
    SCPC_COMMIT=${SCPC_SHA} \
    PATH=/opt/solidcraft/bin:$PATH

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
        git \
        jq \
        libdbus-1-3 \
        libegl1 \
        libfontconfig1 \
        libglib2.0-0 \
        libgl1 \
        libice6 \
        libsm6 \
        libx11-6 \
        libx11-xcb1 \
        libxcb-cursor0 \
        libxcb-xinerama0 \
        libxcb1 \
        libxext6 \
        libxi6 \
        libxkbcommon-x11-0 \
        libxkbcommon0 \
        libxrender1 \
    && rm -rf /var/lib/apt/lists/*

RUN set -eux; \
    archive="solidcraft-${SOLIDCRAFT_VERSION}-linux-x86_64.tar.gz"; \
    base="https://github.com/tangency-labs/solidcraft/releases/download/v${SOLIDCRAFT_VERSION}"; \
    mkdir -p /opt/solidcraft /tmp/solidcraft; \
    cd /tmp/solidcraft; \
    curl --proto '=https' -fsSLO "${base}/SHA256SUMS.txt"; \
    curl --proto '=https' -fsSLO "${base}/${archive}"; \
    grep "  ${archive}$" SHA256SUMS.txt | sha256sum -c -; \
    tar -xzf "${archive}" --strip-components=1 -C /opt/solidcraft; \
    test -x /opt/solidcraft/bin/solidcraft-cli; \
    rm -rf /tmp/solidcraft

RUN set -eux; \
    mkdir -p /opt/src/scpf /opt/src/scpc; \
    git -C /opt/src/scpf init; \
    git -C /opt/src/scpf remote add origin "${SCPF_URL}"; \
    git -C /opt/src/scpf fetch --depth 1 origin "${SCPF_SHA}"; \
    git -C /opt/src/scpf checkout --detach FETCH_HEAD; \
    test "$(git -C /opt/src/scpf rev-parse HEAD)" = "${SCPF_SHA}"; \
    git -C /opt/src/scpc init; \
    git -C /opt/src/scpc remote add origin "${SCPC_URL}"; \
    git -C /opt/src/scpc fetch --depth 1 origin "${SCPC_SHA}"; \
    git -C /opt/src/scpc checkout --detach FETCH_HEAD; \
    test "$(git -C /opt/src/scpc rev-parse HEAD)" = "${SCPC_SHA}"; \
    python -m pip install --upgrade pip setuptools wheel; \
    python -m pip install /opt/src/scpf/scpf /opt/src/scpc pillow pyyaml

RUN solidcraft-cli --version \
    && python --version \
    && python -c "import scpf, scpc" \
    && python -c "from scpf.version import check_cli_version; check_cli_version(require_cli=True)"

WORKDIR /workspace
