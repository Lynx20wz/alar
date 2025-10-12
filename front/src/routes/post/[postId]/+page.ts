import type { PostInfo } from "$lib/types/Post";
import type { PageLoad } from "./$types";

export const load: PageLoad = async ({ fetch, params }) => {
  const postId = params.postId;

  let post: PostInfo | undefined = undefined;
  try {
    const response = await fetch(`/api/posts/${postId}`);
    if (response.ok) {
      const json = await response.json();
      post = json;
    }
  } catch (error) {
    console.error(error);
  }

  return { post };
};
