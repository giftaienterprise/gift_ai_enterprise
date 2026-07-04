export function validateSettings<T extends { phone: string }>(settings: T): T {
  if (settings.phone && !/^[+\d][\d\s-]{4,29}$/.test(settings.phone)) {
    throw new Error('INVALID_PHONE')
  }
  return settings
}
