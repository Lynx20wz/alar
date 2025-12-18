import type { LayoutLoad } from "./$types";

export const load: LayoutLoad = async (event) => {
  return {
    user: event.locals.user || null,
  };
};
