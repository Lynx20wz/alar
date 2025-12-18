import { formatDistanceToNow, type Locale } from "date-fns";
import { enUS } from "date-fns/locale";

export const publicRouters = ["/login", "/registration"];
const locales: Record<string, Locale> = {
  en: enUS,
  ru: enUS,
};

export function isPublicRoute(path: string): boolean {
  return publicRouters.includes(path);
}

export function formatTimeAgo(date: Date, locale?: string, timezone: boolean = true): string {
  if (timezone) {
    date = new Date(date.getTime() - new Date().getTimezoneOffset() * 60 * 1000);
  }
  return formatDistanceToNow(date, {
    addSuffix: true,
    locale: locale ? locales[locale] : enUS,
    includeSeconds: true,
  });
}
