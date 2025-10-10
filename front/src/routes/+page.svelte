<script lang="ts">
  import { getTranslate } from "@tolgee/svelte";
  import { page } from "$app/state";
  import UserCard from "$lib/components/UserCard.svelte";
  import Post from "$lib/components/Post.svelte";

  const user = page.data.user;
  const posts = page.data.posts;
  const { t } = getTranslate();
</script>

<div class="container df">
  <aside class="aside df">
    <h5 class="aside__header">{$t("favorites")}</h5>
    <div class="aside__items df">
      {#each user.follows.objects as follow}
        <UserCard user={follow} />
      {/each}
    </div>
  </aside>
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
    justify-content: space-between;
  }
  .aside {
    height: 1000px;
    width: 250px;
    background-color: var(--primary);
    padding: 10px;
    border-radius: 10px;
    flex-direction: column;
    justify-content: flex-start;
    align-items: start;
    gap: 10px;

    &__header {
      width: 100%;
      text-align: center;
    }

    &__items {
      flex-direction: column;
      align-items: flex-start;
      gap: 10px;
    }
  }

  .content {
    width: auto;
    &__items {
      flex-direction: column;
      gap: 10px;
    }
  }
</style>
