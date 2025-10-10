<script lang="ts">
  import type { PostInfo } from "$lib/types/Post";
  import UserCard from "./UserCard.svelte";

  export let post: PostInfo;
</script>

<div class="post df">
  <UserCard user={post.author} />
  <h4 class="post__title">{post.title}</h4>
  <p class="post__content">{post.content}</p>
</div>

<style lang="scss">
  .post {
    width: 100%;
    background-color: var(--primary);
    align-items: start;
    flex-direction: column;
    border-radius: 10px;
    padding: 12px 20px;
  }
</style>
