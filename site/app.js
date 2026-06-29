const owner = "altibo";
const repository = "MyAndroidApp";
const apiUrl = `https://api.github.com/repos/${owner}/${repository}/releases/latest`;

const versionElement = document.querySelector("#version");
const dateElement = document.querySelector("#release-date");
const downloadElement = document.querySelector("#download");
const statusElement = document.querySelector("#status");

async function loadLatestRelease() {
  try {
    const response = await fetch(apiUrl, {
      headers: { Accept: "application/vnd.github+json" },
    });

    if (!response.ok) {
      throw new Error(`GitHub API: ${response.status}`);
    }

    const release = await response.json();
    const apk = release.assets.find((asset) => asset.name.endsWith(".apk"));

    versionElement.textContent = release.tag_name;
    dateElement.textContent = new Intl.DateTimeFormat("de-DE", {
      day: "2-digit",
      month: "long",
      year: "numeric",
    }).format(new Date(release.published_at));

    if (apk) {
      downloadElement.href = apk.browser_download_url;
      statusElement.textContent =
        `${(apk.size / 1024 / 1024).toFixed(1)} MB · Direkt aus GitHub Releases`;
    } else {
      throw new Error("Das Release enthält keine APK.");
    }
  } catch (error) {
    versionElement.textContent = "Neueste Version";
    dateElement.textContent = "Direkter Release-Download";
    statusElement.textContent =
      "Versionsdetails sind gerade nicht erreichbar – der Download funktioniert weiterhin.";
    console.warn(error);
  } finally {
    downloadElement.classList.remove("is-loading");
  }
}

loadLatestRelease();
