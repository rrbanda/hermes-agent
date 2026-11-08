declare global {
  interface Window {
    __HERMES_PRODUCT_NAME__?: string;
  }
}

const FALLBACK = "Hermes Agent";

/** Display name injected by the dashboard server from brand.json. */
export function dashboardProductName(): string {
  if (typeof window === "undefined") return FALLBACK;
  const name = window.__HERMES_PRODUCT_NAME__?.trim() ?? "";
  return name || FALLBACK;
}

/** Two-line sidebar mark. ``Xyz Agent`` becomes ``Xyz`` / ``Agent``. */
export function dashboardProductLines(name = dashboardProductName()): [string, string] {
  const suffix = " Agent";
  if (name.endsWith(suffix) && name.length > suffix.length) {
    return [name.slice(0, -suffix.length), "Agent"];
  }
  return [name, ""];
}

export function dashboardDocumentTitle(name = dashboardProductName()): string {
  return `${name} - Dashboard`;
}
