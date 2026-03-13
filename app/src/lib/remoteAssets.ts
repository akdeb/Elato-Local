const GLOBAL_PERSONALITY_IMAGE_BASE_URL = "https://pub-a64cd21521e44c81a85db631f1cdaacc.r2.dev";
const REMOTE_ASSET_VERSION = (import.meta as any).env?.VITE_REMOTE_ASSET_VERSION || "20260314";

function withVersion(url: string): string {
  const sep = url.includes("?") ? "&" : "?";
  return `${url}${sep}v=${encodeURIComponent(REMOTE_ASSET_VERSION)}`;
}

export function globalPersonalityImageUrl(id: string): string {
  return withVersion(`${GLOBAL_PERSONALITY_IMAGE_BASE_URL}/${encodeURIComponent(id)}.png`);
}

export function versionedRemoteUrl(url: string): string {
  return withVersion(url);
}
