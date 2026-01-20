# 如何将 GitHub 更新同步到您的电脑

您好！我已经将所有最新的代码、一键安装脚本和文档都推送到了您的 GitHub 仓库。现在，您只需按照以下步骤将这些更新同步到您的本地电脑即可。

---

## 场景一：您之前已经克隆过项目

如果您已经在电脑上拥有 `ufo-galaxy` 文件夹，请按照以下步骤操作：

1.  **打开命令行工具**
    -   在 Windows 上，打开 **PowerShell** 或 **CMD**。

2.  **进入项目目录**
    ```powershell
    cd path\to\your\ufo-galaxy
    ```
    (请将 `path\to\your\ufo-galaxy` 替换为您项目实际的文件夹路径)

3.  **拉取最新更新**
    运行以下命令，它会自动从 GitHub 下载所有最新的文件和更改：
    ```powershell
    git pull origin master
    ```

4.  **完成！**
    现在您的本地文件夹已经和 GitHub 完全同步了。您可以直接运行新的一键安装脚本。

---

## 场景二：您是第一次在电脑上设置项目

如果您是第一次在电脑上部署这个项目，请按照以下步骤操作：

1.  **安装 Git**
    -   如果您的电脑还没有安装 Git，请先从 [git-scm.com](https://git-scm.com/download/win) 下载并安装。

2.  **打开命令行工具**
    -   在 Windows 上，打开 **PowerShell** 或 **Git Bash**。

3.  **选择一个位置**
    -   选择一个您想存放项目的文件夹，例如 `C:\Projects`。
    ```powershell
    cd C:\Projects
    ```

4.  **克隆仓库**
    运行以下命令，它会从 GitHub 下载整个项目：
    ```powershell
    git clone https://github.com/DannyFish-11/ufo-galaxy.git
    ```

5.  **进入项目目录**
    ```powershell
    cd ufo-galaxy
    ```

6.  **完成！**
    现在项目已经完整地下载到您的电脑。您可以开始运行一键安装脚本了。

---

## 下一步：启动系统

无论您是更新还是全新克隆，下一步都是一样的：

1.  确保您在 `ufo-galaxy` 文件夹内。
2.  右键点击 `INSTALL_AND_START.bat` 文件。
3.  选择 **“以管理员身份运行”**。

系统将自动完成所有配置和启动。祝您在极客松比赛中取得好成绩！🚀
