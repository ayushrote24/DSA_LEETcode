# LeetCode → GitHub automatic sync

Target repository: https://github.com/ayushrote24/DSA_LEETcode  
Target branch: `main`

## 1. Install the browser extension

Install [LeetHub: LeetCode to GitHub Sync from the Chrome Web Store](https://chromewebstore.google.com/detail/leethub-leetcode-to-githu/igcdoidkkmchcpanpfbpcghbfldjfjfo).

Use the same Chrome profile where you are signed in to LeetCode.

## 2. Create a narrowly scoped GitHub token

1. Open [GitHub fine-grained personal access tokens](https://github.com/settings/personal-access-tokens/new).
2. Give it a name such as `LeetCode Sync - DSA_LEETcode`.
3. Set repository access to **Only select repositories** and select **DSA_LEETcode**.
4. Under Repository permissions, set **Contents: Read and write**. Leave other permissions at no access.
5. Create the token and copy it directly into the extension's settings.

Never paste this token into chat, a README, source code, or a public repository. The Chrome Web Store listing says this extension stores it in local extension storage and uses it for GitHub API requests. Review the extension's current permissions and privacy details before authorizing it.

## 3. Connect the repository

In the extension settings:

- GitHub owner: `ayushrote24`
- Repository: `DSA_LEETcode`
- Select the existing initialized repository.
- Enable automatic uploads.

Keep the repository's default branch as `main`.

## 4. Test one accepted submission

1. Open a LeetCode problem in the same browser.
2. Submit a solution and wait for the **Accepted** result.
3. Check the repository for the newly committed solution and problem details.
4. Check the extension's latest-sync view if the commit does not appear.

The extension is intended to sync accepted solutions. Do not expect wrong answers or in-progress submissions to be uploaded. Its listing also describes manually syncing an older accepted submission from its detail page or submission ID/URL; it does not advertise a bulk import of the entire account history.

## 5. LeetCode statistics in the root README

The repository also has a GitHub Actions workflow:

- Workflow: `.github/workflows/leetcode-stats.yml`
- Script: `scripts/update_leetcode_readme.py`
- Scheduled refresh: daily at 07:47 India time
- Manual refresh: GitHub repository → **Actions** → **Refresh LeetCode dashboard** → **Run workflow**

The workflow reads public profile statistics only. It does not need your LeetCode password, session cookie, or a GitHub personal token. It has only `contents: write` permission so it can update the README.

**Username assumption:** the workflow currently uses `ayushrote24` as the LeetCode username because that is your connected GitHub handle. Change `LEETCODE_USERNAME` in the workflow if your LeetCode handle is different.

## What this setup syncs

| Data | How it updates |
|---|---|
| Accepted solution source code | Browser extension, after an Accepted submission |
| Problem details | Browser extension |
| Public solved counts and global rank | GitHub Actions, daily |
| Activity heatmap image | External LeetCard image linked in README |

LeetCode and third-party extensions can change their page/API behavior. After setup, verify the first accepted submission and check the Actions run for the statistics refresh.
