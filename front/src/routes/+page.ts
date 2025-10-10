import type { PageLoad } from "./$types";

export const load: PageLoad = async ({ fetch }) => {
  const response = await fetch("api/post/");
  if (!response.ok) {
    throw new Error("Failed to fetch posts");
  }
  const posts = await response.json();
  return { posts };
};
