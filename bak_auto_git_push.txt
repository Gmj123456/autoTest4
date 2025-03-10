#!/bin/bash

# 定义提交信息，默认为 "Auto commit"
COMMIT_MSG=${1:-"Auto commit"}

# 检查是否在 Git 仓库中
if ! git rev-parse --is-inside-work-tree > /dev/null 2>&1; then
    echo "当前目录不是一个 Git 仓库，请在 Git 仓库目录下运行此脚本。"
    exit 1
fi

# 检查是否有文件变更
if [ -z "$(git status --porcelain)" ]; then
    echo "没有文件变更，无需提交。"
    exit 0
fi

# 添加所有更改到暂存区
git add .

# 提交更改到本地仓库
git commit -m "$COMMIT_MSG"

# 拉取远程仓库的最新更改并合并
git pull --rebase origin main

# 处理合并冲突（如果有）
if [ $? -ne 0 ]; then
    echo "合并过程中出现冲突，请手动解决冲突后再次运行脚本。"
    exit 1
fi

# 推送本地仓库的更改到远程仓库
git push origin main

# 检查推送是否成功
if [ $? -eq 0 ]; then
    echo "代码已成功推送到远程仓库。"
else
    echo "推送失败，请检查网络连接或权限设置。"
fi    