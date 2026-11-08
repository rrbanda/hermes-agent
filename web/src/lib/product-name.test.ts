import { afterEach, describe, expect, it } from "vitest";
import {
  dashboardDocumentTitle,
  dashboardProductLines,
  dashboardProductName,
} from "./product-name";

afterEach(() => {
  delete window.__HERMES_PRODUCT_NAME__;
});

describe("dashboardProductName", () => {
  it("uses the server-injected brand", () => {
    window.__HERMES_PRODUCT_NAME__ = "Acme Agent";
    expect(dashboardProductName()).toBe("Acme Agent");
    expect(dashboardProductLines()).toEqual(["Acme", "Agent"]);
    expect(dashboardDocumentTitle()).toBe("Acme Agent - Dashboard");
  });

  it("falls back to Hermes Agent when the server did not inject a name", () => {
    expect(dashboardProductName()).toBe("Hermes Agent");
    expect(dashboardProductLines("Hermes Agent")).toEqual(["Hermes", "Agent"]);
  });
});
