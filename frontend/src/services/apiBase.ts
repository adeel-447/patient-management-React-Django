/** API base URL: Vite proxy (`/api`) in dev, or absolute URL from env in production builds. */
export function getApiBase(): string {
  const raw = import.meta.env.VITE_API_URL?.replace(/\/$/, "") ?? "";
  return raw ? `${raw}/api` : "/api";
}
