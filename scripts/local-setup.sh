#!/bin/bash
set -e

function install_git_hooks {
  echo "Installing git hooks..."
  git config core.hooksPath scripts/hooks
}

install_git_hooks
