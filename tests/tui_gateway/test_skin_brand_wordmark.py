"""The chat banner's block letters follow brand.json when a skin has no logo of its own."""


def test_a_renamed_checkout_owns_the_session_figure():
    from hermes_constants import brand_cli, brand_hero
    from tui_gateway.change_watcher import skin_payload

    branding = skin_payload({})["branding"]
    if brand_cli() == "hermes":
        assert "hero" not in branding
        return
    assert branding["hero"] == brand_hero()


def test_a_renamed_checkout_owns_the_banner_tagline():
    from hermes_constants import brand_cli, brand_tagline
    from tui_gateway.change_watcher import skin_payload

    branding = skin_payload({})["branding"]
    if brand_cli() == "hermes":
        assert "tagline" not in branding
        return
    assert branding["tagline"] == brand_tagline()


def test_default_skin_wordmark_follows_the_checkout_brand():
    from hermes_cli.banner_wordmark import wordmark_rows
    from hermes_constants import brand_cli, brand_display_name
    from tui_gateway.change_watcher import skin_payload

    payload = skin_payload({})
    name = brand_display_name()
    assert payload["branding"]["agent_name"] == name
    if brand_cli() == "hermes":
        assert payload["banner_logo"] == ""
        return
    assert wordmark_rows(name)[0] in payload["banner_logo"]
    assert wordmark_rows("Hermes Agent")[0] not in payload["banner_logo"]


def test_a_skin_logo_is_not_replaced(monkeypatch):
    class _Skin:
        name = "custom"
        colors = {}
        light_colors = {}
        dark_colors = {}
        branding = {"agent_name": "Acme Agent", "help_header": ""}
        banner_logo = "CUSTOM LOGO"
        banner_hero = ""
        tool_prefix = ""
        custom_css = ""

    monkeypatch.setattr("hermes_cli.skin_engine.init_skin_from_config", lambda _config: None)
    monkeypatch.setattr("hermes_cli.skin_engine.get_active_skin", lambda: _Skin())
    from tui_gateway.change_watcher import skin_payload

    assert skin_payload({})["banner_logo"] == "CUSTOM LOGO"
