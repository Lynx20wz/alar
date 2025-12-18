<script lang="ts">
  import { page } from "$app/state";
  import Aside from "$lib/components/Aside.svelte";
  import Post from "$lib/components/Post.svelte";
  import { getTranslate } from "@tolgee/svelte";

  const { t } = getTranslate();
  const posts = page.data.posts;
</script>

<svelte:head>
  <title>{$t("home")}</title>
</svelte:head>

<div class="container df">
  <Aside />
  <main class="content df">
    <div class="content__items df">
      {#each posts as post}
        <Post {post} />
      {/each}
    </div>
  </main>
</div>

<style lang="scss">
  :global(.content) {
    font-family: "JetBrainsMono", sans-serif;
  }
  .container {
    gap: 15px;
    padding: 20px;
    flex-direction: row;
    align-items: start;
    justify-content: start;
  }

  .content {
    width: 100%;
    &__items {
      width: 100%;
      flex-direction: column;
      gap: 10px;
    }
  }
</style>
