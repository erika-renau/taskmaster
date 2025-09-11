FROM mcr.microsoft.com/devcontainers/python:3.11
RUN apt-get update && apt-get install -y curl sudo \
    && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs
ARG USERNAME=vscode
USER ${USERNAME}
WORKDIR /workspace
