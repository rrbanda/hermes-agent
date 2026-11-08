import { describe, expect, it } from 'vitest'

import { bannerSlogan, sessionHero } from '../banner.js'
import type { ThemeColors } from '../theme.js'
import { wordmarkRows } from '../wordmark.js'

describe('wordmarkRows', () => {
  it('spells the brand instead of the Hermes wordmark', () => {
    const branded = wordmarkRows('Xyz Agent')
    const hermes = wordmarkRows('Hermes Agent')

    expect(branded).toHaveLength(6)
    expect(branded[0]?.startsWith('██╗  ██╗██╗   ██╗███████╗')).toBe(true)
    expect(branded[0]).not.toBe(hermes[0])
  })
})

describe('bannerSlogan', () => {
  const catalog = 'Nous Research · Messenger of the Digital Gods'

  it('hides the Hermes slogan for a renamed product until one is set', () => {
    expect(bannerSlogan('Xyz Agent', undefined, catalog)).toBeNull()
    expect(bannerSlogan('Xyz Agent', '', catalog)).toBeNull()
    expect(bannerSlogan('Xyz Agent', '  ', catalog)).toBeNull()
    expect(bannerSlogan('Xyz Agent', 'Your banner line', catalog)).toBe('Your banner line')
  })

  it('keeps the catalog slogan for Hermes and its built-in personas', () => {
    expect(bannerSlogan('Hermes Agent', undefined, catalog)).toBe(catalog)
    expect(bannerSlogan('Ares Agent', undefined, catalog)).toBe(catalog)
    expect(bannerSlogan('Hermes Agent', '', catalog)).toBeNull()
  })
})

describe('sessionHero', () => {
  const colors = { accent: 'a', border: 'b', muted: 'm', primary: 'p' } as ThemeColors

  it('hides the caduceus for a renamed product until a figure is set', () => {
    expect(sessionHero(colors, '', undefined, 'Xyz Agent')).toBeNull()
    expect(sessionHero(colors, '', '', 'Xyz Agent')).toBeNull()
    expect(sessionHero(colors, '', 'Hi', 'Xyz Agent')?.[0]?.[1]).toBe('Hi')
    expect(sessionHero(colors, '[#fff]Skin[/]', '', 'Xyz Agent')?.[0]?.[1]).toBe('Skin')
  })

  it('keeps the caduceus for Hermes', () => {
    expect((sessionHero(colors, '', undefined, 'Hermes Agent') ?? []).length).toBeGreaterThan(1)
  })
})
